# -*- coding: utf-8 -*-
"""Upload a local tsv to a Terra workspace data model."""

import argparse
# import pandas as pd
# import re
import pprint

from firecloud import api as fapi

from common import call_fiss


def list_entities(project, workspace):
    """Retrieve a list of existing entities with details from the workspace."""
    response = call_fiss(fapi.list_entity_types, 200, project, workspace)

    return response


def get_entities_of_type(project, workspace, etype, save_as=None, save_loc='/files'):
    """Download all entities of the input entity_type to a local tsv."""
    # check that the entity type entered exists in this workspace
    response = list_entities(project, workspace)
    if etype not in response.keys():
        existing_entities = ', '.join(list(response.keys()))
        message = f'\n\nError: requested entity type "{etype}" was not found in workspace.\n' + \
                  f'Existing entity types in this workspace are: {existing_entities}.\n\n' + \
                  f'To list the entity types in this workspace, run the following command:\n' + \
                  f'\t python3 scripts/download_tsv.py --project {project} --workspace {workspace} --list'
        raise Exception(message)

    # retrieve those entities
    response = fapi.get_entities_tsv(project, workspace, etype, attrs=None, model='flexible')

    if response.status_code != 200:
        message = f'\n\nError: Response code {response.status_code}, {response.text}'
        raise Exception(message)

    if save_as is None:
        save_as = f'{etype}.tsv'
    elif not save_as.endswith('.tsv'):
        save_as += '.tsv'

    if save_loc is None:
        save_loc = ''
    elif len(save_loc) > 0 and not save_loc.endswith('/'):
        save_loc += '/'

    with open(save_loc + save_as, 'w') as f:
        f.write(response.text)

    print(f'Data saved to {save_loc + save_as}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data warehousing script")
    parser.add_argument(
        '--project',
        type=str,
        help='Terra namespace/project of destination workspace')
    parser.add_argument(
        '--workspace',
        type=str,
        help='Name of destination Terra workspace')
    parser.add_argument(
        '--list',
        action='store_true',
        help='Get a list of entities in the workspace')
    parser.add_argument(
        '--etype',
        default=None,
        help='Download all entities of indicated type')
    parser.add_argument(
        '--save_as',
        default=None,
        help='Optional name to save downloaded tsv')
    parser.add_argument(
        '--save_loc',
        default='files/',
        help='Directory to save downloaded tsv')

    args = parser.parse_args()

    if args.list:
        entities_json = list_entities(args.project, args.workspace)
        pprint.pprint(entities_json)
    elif args.etype:
        get_entities_of_type(args.project, args.workspace, args.etype, args.save_as, args.save_loc)
