# -*- coding: utf-8 -*-
"""Upload a local tsv to a Terra workspace data model."""

import argparse
import pandas as pd
import re

from firecloud import api as fapi


def upload_tsv_to_workspace(tsv_file_path, project, workspace):
    """Upload a local tsv file to a Terra workspace's data model."""

    # check that the TSV is formatted properly to be read by Terra
    df_data = pd.read_csv(tsv_file_path, delimiter='\t')
    headers = list(df_data.columns)
    first_column_header = headers[0]
    extracted_entity = re.search('entity:(.*)_id', first_column_header)

    if extracted_entity:
        print(f'Uploading file {tsv_file_path} to {extracted_entity.group(1)} table in '
              f'Terra workspace {project}/{workspace}.')
    else:
        message = f'Poorly formed entity tsv. The first header must be of the format ' + \
                  f'`entity:<entity_type>_id`, but in {tsv_file_path}, the first header is ' + \
                  f'`{first_column_header}`.'
        raise ValueError(message)

    # call the API to upload the tsv
    response = fapi.upload_entities_tsv(project, workspace, tsv_file_path, model='flexible')

    if response.status_code != 200:
        print(f'Error with upload: {response.text}')
    else:
        print('Success!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data warehousing script")
    parser.add_argument(
        '--tsv',
        type=str,
        help='path to local tsv file to upload')
    parser.add_argument(
        '--project',
        type=str,
        help='Terra namespace/project of destination workspace')
    parser.add_argument(
        '--workspace',
        type=str,
        help='Name of destination Terra workspace')
    args = parser.parse_args()

    upload_tsv_to_workspace(args.tsv, args.project, args.workspace)
