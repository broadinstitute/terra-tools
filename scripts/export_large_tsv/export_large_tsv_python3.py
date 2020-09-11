# -*- coding: utf-8 -*-
"""Download a remote tsv from a Terra workspace data model when it is too large to export from Terra UI."""
import argparse
from firecloud import api as fapi
# from tqdm import tqdm


def download_tsv_from_workspace(project, workspace, entity, tsv_name):
    """Download large TSV file from Terra workspace."""
    # get list of entity types in workspace using API call
    request = fapi.list_entity_types(project, workspace)
    if request.status_code != 200:
        print(request.text)

    entity_types_json = request.json()
    entity_count = entity_types_json[args.entity_type]["count"]
    print(f'{entity_count} {entity}(s) to gather...')
    attribute_names = entity_types_json[args.entity_type]["attributeNames"]

    exit(1)
    with open(args.output_file, "w") as tsvfile:
        tsvfile.write("\t".join(attribute_names)+"\n")

        entity_data = []
        row_num = 0
        page_size = 1000
        num_pages = int(math.ceil(float(entity_count) / page_size))

        pool = mp.Pool(processes=2)
        entity_requests = []

        for i in range(1, num_pages + 1):
            entity_requests.append(pool.apply_async(get_entity_by_page,
                                                    args=(args.ws_namespace, args.ws_name, args.entity_type, i, page_size)))

        pb = ProgressBar(0, entity_count, "Entities gathered")

        for request in entity_requests:
            for entity_json in request.get(timeout=100)["results"]:
                attributes = entity_json["attributes"]
                values = []
                for attribute_name in attribute_names:
                    value = ""

                    if attribute_name in attributes:
                        value = attributes[attribute_name]
                    if attribute_name == "participant" or attribute_name == "sample":
                        value = value["entityName"]

                    values.append(value)

                tsvfile.write("\t".join(values)+"\n")
                row_num += 1
                pb.increment()
                pb.print_bar()


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
