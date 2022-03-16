## import_large_tsv.py
Import (upload) a large tsv file to a Terra workspace.
This script uploads large tsv files in chunks, for use when the number of individual entities is too large to upload via the Terra UI. The input tsv file should be formatted in the Terra required format for a single entity data table load file.

To execute:
```python3 scripts/import_large_tsv/import_large_tsv.py --project <workspace-project> --workspace <workspace_name> --tsv <path_to_tsv_to_upload>```

To get full details on input parameters run the following command (from the main directory):
```python3 scripts/import_large_tsv/import_large_tsv.py -h```

## bulk_import_large_tsvs.py
Import (upload) multiple large tsv files to a Terra workspace.
This script uploads multiple large tsv files when the tsv files are too large to upload via the Terra UI. The input tsv file should be a newline delimited file where each line is a path to the local single data table (entity) tsv file to upload to a Terra workspace.

To execute:
```python3 scripts/import_large_tsv/bulk_import_large_tsvs.py --project <workspace-project> --workspace <workspace_name> --tsv <path_to_newline_delimited_tsv>```