# -*- coding: utf-8 -*-
"""Upload a local tsv to a Terra workspace data model when it is too large to import from Terra UI."""
from common import *
import tempfile


def main():
    setup()

    # # The main argument parser
    # parser = DefaultArgsParser(description="Imports a TSV file when it is too large to import from FireCloud.")

    # # Core application arguments
    # parser.add_argument('-p', '--namespace', dest='ws_namespace', action='store', required=True, help='Workspace namespace')
    # parser.add_argument('-n', '--name', dest='ws_name', action='store', required=True, help='Workspace name')
    # parser.add_argument('-f', '--tsv_file', dest='tsv_file', action='store', required=True, help='TSV file to import.')

    # args = parser.parse_args()

    tsv_strings = []
    with open(args.tsv_file, "r") as tsvfile:
        headers = tsvfile.readline()

        tsv_data = headers
        for i, line in enumerate(tsvfile):
            tsv_data += line

            if i > 0 and i % 200 == 0:
                tsv_strings.append(tsv_data)
                tsv_data = headers

        # catch the last lines from the tsv file that aren't caught by the % above
        tsv_strings.append(tsv_data)

        # TODO: REPLACE PROGRESSBAR WITH TQDM
        pb = ProgressBar(0, len(tsv_strings), "Split TSV files uploaded")
        pb.print_bar()

        # Upload the individual TSV files via API call to Terra Workspace
        for tsv_string in tsv_strings:
            request = firecloud_api.upload_entities(args.ws_namespace, args.ws_name, tsv_string)
            if request.status_code != 200:
                fail(request.text)
            pb.increment()
            pb.print_bar()

if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description="Imports/upload a TSV file to Terra when it is too large to upload via the UI.")
    # application arguments
    parser.add_argument(
        '-p', '--project',
        type=str,
        dest='ws_project',
        action='store',
        required=True,
        help='Terra namespace/project of workspace.')
    parser.add_argument(
        '-n', '--workspace',
        type=str,
        dest='ws_name',
        action='store',
        required=True,
        help='Name of Terra workspace.')
    parser.add_argument(
        '-f', '--tsv_file',
        type=str,
        dest='tsv_file',
        action='store',
        required=True,
        help='Path to local tsv file to upload.')

    args = parser.parse_args()
    upload_tsv_to_workspace(args.tsv, args.project, args.workspace)