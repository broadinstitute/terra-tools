# -*- coding: utf-8 -*-
"""Upload a local tsv to a Terra workspace data model when it is too large to import from Terra UI."""
import argparse
from firecloud import api as fapi
from tqdm import tqdm


def upload_tsv_to_workspace(tsv, project, workspace):
    """Split large TSV file and upload individual smaller TSV files to Terra workspace."""
    # initiate list that will contain n items where each n = header + 5000 rows of input tsv data
    tsv_strings = []

    # open input tsv, save header, split large tsv into 5000 row chunks, upload each 5000 chunk to Terra via API
    with open(tsv, "r") as tsvfile:
        # save header from input tsv (entity:table-name_id, col1, col2, col3, ...)
        header = tsvfile.readline()
        # initiate tsv_subset variable with header - 5000 rows of data to be added to tsv_subset
        tsv_subset = header

        # loop through input tsv, check for 5000 rows, add to tsv_subset (already contains header)
        for i, line in enumerate(tsvfile):
            # add row by row to tsv_subset
            tsv_subset += line

            # add until rows = 5000
            if i > 0 and i % 5000 == 0:
                # for each tsv_subset (header + 5000 rows) append to tsv_strings
                tsv_strings.append(tsv_subset)
                # reset tsv_subset to be only header
                tsv_subset = header

        # catch the last lines from the tsv file that aren't caught by the % above
        tsv_strings.append(tsv_subset)

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
