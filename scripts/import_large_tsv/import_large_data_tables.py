# -*- coding: utf-8 -*-
"""Upload multiple local tsv to a Terra workspace data model when they are too large to import using the Terra UI."""
import argparse
from import_large_tsv import upload_tsv_to_workspace

def import_large_tsvs(tsv, project, workspace):
    """Import all load files listed in the input tsv file."""

    with open(tsv, 'r') as load_files:
        load_tsvs = [line.rstrip() for line in load_files]
        for data_table in load_tsvs:
            print(f"Starting upload of data table at path: {data_table}")
            upload_tsv_to_workspace(data_table, project, workspace)


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description="Exports/downloadloads large TSV files from Terra when they are too large to download via the UI.")
    # application arguments
    parser.add_argument('-t', '--tsv', type=str, required=True, help='path to tsv file with paths to data table load file (tsv).')
    parser.add_argument('-p-', '--project', type=str, action='store', required=True, help='Terra namespace/project of workspace.')
    parser.add_argument('-w', '--workspace', type=str, action='store', required=True, help='Name of Terra workspace.')

    args = parser.parse_args()
    import_large_tsvs(args.tsv, args.project, args.workspace)

