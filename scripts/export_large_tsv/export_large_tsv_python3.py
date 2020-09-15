# -*- coding: utf-8 -*-
"""Download a remote tsv from a Terra workspace data model when it is too large to export from Terra UI."""
import argparse
from firecloud import api as fapi
from tqdm import tqdm
import math
import requests


def download_tsv_from_workspace(project, workspace, entity, tsv_name):
    """Download large TSV file from Terra workspace."""
    # get list of entity types in workspace using API call
    # API = https://api.firecloud.org/#!/Entities/getEntityTypes
    request = fapi.list_entity_types(project, workspace)
    if request.status_code != 200:
        print(request.text)

    # get (and report) number of entities + associated attributes of chosen entity type
    entity_types_json = request.json()
    entity_count = entity_types_json[entity]["count"]
    attribute_names = entity_types_json[entity]["attributeNames"]

    print(f'{entity_count} {entity}(s) to export.')

    with open(tsv_name, "w") as tsvout:
        tsvout.write("\t".join(attribute_names) + "\n")
        # initiate list that will contain n items where each n = rows of output tsv data
        entity_data = []
        # set starting row value and number of rows in single page
        row_num = 0
        page_size = 1000
        # calculate number of pages
        num_pages = int(math.ceil(float(entity_count) / page_size))

        # get entities per page - where each page where page_size = #rows using API call
        # API = https://api.firecloud.org/#!/Entities/entityQuery
        page_entity_responses = []
        for i in range(1, num_pages + 1):
            page_entity_responses.append(get_entity_by_page(project, workspace, entity, i, page_size))

        # for each request(by page) in entity_requests
        for page_response in tqdm(page_entity_responses):
            print(page_response)
            exit(1)
            for entity_json in requests.get(timeout=100)["results"]:
                attributes = entity_json["attributes"]
                values = []
                for attribute_name in attribute_names:
                    value = ""

                    if attribute_name in attributes:
                        value = attributes[attribute_name]
                    if attribute_name == "participant" or attribute_name == "sample":
                        value = value["entityName"]

                    values.append(value)

                tsvout.write("\t".join(values) + "\n")
                row_num += 1


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

    args = parser.parse_args()
    download_tsv_from_workspace(args.project, args.workspace, args.entity, args.tsv_filename)
