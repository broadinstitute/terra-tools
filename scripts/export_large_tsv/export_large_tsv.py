# -*- coding: utf-8 -*-
"""Download a remote tsv from a Terra workspace data model when it is too large to export from Terra UI."""
from firecloud import api as fapi
from tqdm import tqdm
import argparse
import math

DEFAULT_PAGE_SIZE = 1000


def get_entity_by_page(project, workspace, entity_type, page, page_size=DEFAULT_PAGE_SIZE, sort_direction='asc', filter_terms=None):
    """Get entities from workspace by page given a page_size(number of entities/rows in entity table)."""
    # API = https://api.firecloud.org/#!/Entities/entityQuery
    response = fapi.get_entities_query(project, workspace, entity_type, page=page,
                                       page_size=page_size, sort_direction=sort_direction,
                                       filter_terms=filter_terms)

    if response.status_code != 200:
        print(response.text)
        exit(1)

    return(response.json())


def download_tsv_from_workspace(project, workspace, entity_type, tsv_name, page_size=DEFAULT_PAGE_SIZE, attr_list=None):
    """Download large TSV file from Terra workspace by designated number of rows."""
    # get all entity types in workspace using API call
    # API = https://api.firecloud.org/#!/Entities/getEntityTypes
    response = fapi.list_entity_types(project, workspace)
    if response.status_code != 200:
        print(response.text)
        exit(1)

    # get/report # of entities + associated attributes(column names) of input entity type
    entity_types_json = response.json()
    entity_count = entity_types_json[entity_type]["count"]
    entity_id = entity_types_json[entity_type]["idName"]
    # if user provided list of specific attributes to return, else return all attributes
    if attr_list:
        all_attribute_names = entity_types_json[entity_type]["attributeNames"]
        attribute_names = [attr for attr in all_attribute_names if attr in attr_list]
    else:
        attribute_names = entity_types_json[entity_type]["attributeNames"]

    # add the entity_id value to list of attributes (not a default attribute of API response)
    attribute_names.insert(0, entity_id)

    print(f'{entity_count} {entity_type}(s) to export.')

    with open(tsv_name, "w") as tsvout:
        # add header with attribute values to tsv
        tsvout.write("\t".join(attribute_names) + "\n")
        # set starting row value and calculate number of pages
        row_num = 0
        num_pages = int(math.ceil(float(entity_count) / page_size))

        # get entities by page where each page has page_size # of rows using API call
        print(f'Getting all {num_pages} pages of entity data.')
        all_page_responses = []
        for page in tqdm(range(1, num_pages + 1)):
            all_page_responses.append(get_entity_by_page(project, workspace, entity_type, page, page_size))

        # for each response(page) in all_page_responses[] - contains parameter metadata
        print(f'Writing {entity_count} attributes to tsv file.')
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

                    values.append(str(value))

                tsvout.write("\t".join(values) + "\n")
                row_num += 1

    print(f'Finished exporting {entity_type}(s) to tsv with name {tsv_name}.')


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description="Exports/downloadload a TSV file from Terra when it is too large to download via the UI.")
    # application arguments
    parser.add_argument('-p', '--project', type=str, required=True, help='Terra namespace/project of workspace.')
    parser.add_argument('-w', '--workspace', type=str, required=True, help='Name of Terra workspace.')
    parser.add_argument('-e', '--entity_type', type=str, required=True, help='Entity type being requested for tsv export to local destination.')
    parser.add_argument('-f', '--tsv_filename', type=str, required=True, help='Name of tsv file to be exported from Terra to local destination.')
    parser.add_argument('-n', '--page_size', type=int, default=DEFAULT_PAGE_SIZE, help='Number of entities/rows to export per page.')
    parser.add_argument('-a', '--attribute_list', nargs='+', help='column names to return - separated by spaces. ex. -a col1 col2')

    args = parser.parse_args()
    download_tsv_from_workspace(args.project, args.workspace, args.entity_type, args.tsv_filename, args.page_size, args.attribute_list)
