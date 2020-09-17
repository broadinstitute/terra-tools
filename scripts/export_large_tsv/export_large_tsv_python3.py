# -*- coding: utf-8 -*-
"""Download a remote tsv from a Terra workspace data model when it is too large to export from Terra UI."""
from firecloud import api as fapi
from tqdm import tqdm
import argparse
import math


def download_tsv_from_workspace(project, workspace, entity, tsv_name, page_size):
    """Download large TSV file from Terra workspace by designated number of rows."""
    # get all entity types in workspace using API call
    # API = https://api.firecloud.org/#!/Entities/getEntityTypes
    request = fapi.list_entity_types(project, workspace)
    if request.status_code != 200:
        print(request.text)

    # get/report # of entities + associated attributes(column names) of input entity type
    entity_types_json = request.json()
    entity_count = entity_types_json[entity]["count"]
    attribute_names = entity_types_json[entity]["attributeNames"]
    entity_id = entity_types_json[entity]["idName"]
    # add the entity_id value to list of attributes (not a default attribute of API response)
    attribute_names.insert(0, entity_id)

    print(f'{entity_count} {entity}(s) to export.')

    with open(tsv_name, "w") as tsvout:
        # add header with attribute values to tsv
        tsvout.write("\t".join(attribute_names) + "\n")
        # set starting row value and calculate number of pages
        row_num = 0
        num_pages = int(math.ceil(float(entity_count) / page_size))

        # get entities by page where each page has page_size # of rows using API call
        # API = https://api.firecloud.org/#!/Entities/entityQuery
        all_page_responses = []
        for page in range(1, num_pages + 1):
            all_page_responses.append(get_entity_by_page(project, workspace, entity, page, page_size))

        # for each response(page) in all_page_responses[] - contains parameter metadata
        for page_response in tqdm(all_page_responses):
            # for each set of attributes in results (no parameters) get attribute names and entity_id(name)
            for entity_json in page_response["results"]:
                attributes = entity_json["attributes"]
                name = entity_json["name"]
                # add name and value to dictionary of attributes
                attributes[entity_id] = name

                values = []
                # for each attribute(column name) in list of attribute names(all columns for entity)
                for attribute_name in attribute_names:
                    value = ""
                    # if entity's attribute(column) is in list of attributes from response, set response's attribute value
                    if attribute_name in attributes:
                        value = attributes[attribute_name]

                    values.append(value)

                tsvout.write("\t".join(values) + "\n")
                row_num += 1
    print(f'Finished exporting {entity}(s) to tsv with name {tsv_name}.')


def get_entity_by_page(project, workspace, entity, page, page_size, sort_direction='asc', filter_terms=None):
    """Get entities from workspace by page given a page_size(number of entities/rows in entity table)."""
    response = fapi.get_entities_query(project, workspace, entity, page=page,
                                       page_size=page_size, sort_direction=sort_direction,
                                       filter_terms=filter_terms)
    return(response.json())


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description="Exports/downloadload a TSV file from Terra when it is too large to download via the UI.")
    # application arguments
    parser.add_argument(
        '--project',
        type=str,
        action='store',
        required=True,
        help='Terra namespace/project of workspace.')
    parser.add_argument(
        '--workspace',
        type=str,
        action='store',
        required=True,
        help='Name of Terra workspace.')
    parser.add_argument(
        '--entity',
        type=str,
        action='store',
        required=True,
        help='Type of entity being requested for tsv export to local destination.')
    parser.add_argument(
        '--tsv_filename',
        type=str,
        action='store',
        required=True,
        help='Name of tsv file to be exported from Terra to local destination.')
    parser.add_argument(
        '--page_size',
        type=int,
        default=1000,
        action='store',
        help='Number of entities/rows to export per page.')

    args = parser.parse_args()
    download_tsv_from_workspace(args.project, args.workspace, args.entity, args.tsv_filename, args.page_size)
