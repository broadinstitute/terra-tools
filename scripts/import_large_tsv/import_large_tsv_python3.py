# -*- coding: utf-8 -*-
"""Upload a local tsv to a Terra workspace data model when it is too large to import from Terra UI."""
import argparse
from firecloud import api as fapi
from tqdm import tqdm


def upload_tsv_to_workspace(tsv, project, workspace):
    """Split large TSV file and upload individual smaller TSV files to Terra workspace."""
    tsv_strings = []

    # open input tsv file
    with open(tsv, "r") as tsvfile:
        headers = tsvfile.readline()
        tsv_data = headers

        # for each line in tsv line, add to header. chunk by 5000 lines.
        for i, line in enumerate(tsvfile):
            tsv_data += line

            if i > 0 and i % 5000 == 0:
                tsv_strings.append(tsv_data)
                tsv_data = headers

        # catch the last lines from the tsv file that aren't caught by the % above
        tsv_strings.append(tsv_data)

        # for each chunk of 5000 rows(tsv_string) in tsv_strings, upload using API call
        for tsv_string in tqdm(tsv_strings):
            request = fapi.upload_entities(project, workspace, tsv_string, model='flexible')
            if request.status_code != 200:
                print(request.text)

    print("Upload of entities complete.")


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description="Imports/upload a TSV file to Terra when it is too large to upload via the UI.")
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
        '--tsv',
        type=str,
        action='store',
        required=True,
        help='Path to local tsv file to upload.')

    args = parser.parse_args()
    upload_tsv_to_workspace(args.tsv, args.project, args.workspace)
