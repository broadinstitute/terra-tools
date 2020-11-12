## Import (upload) a tsv file for a given entity type in a workspace
This script uploads large tsv files in chunks, for use when the number of individual entities is too large to upload via the UI.

To execute the script, run the following command (from the main directory):
```python3 scripts/import_large_tsv/import_large_tsv.py --project <workspace-project> --workspace <workspace_name> --tsv <path_to_tsv_to_upload>```

To get full details on input parameters run the following command (from the main directory):
```python3 scripts/import_large_tsv/import_large_tsv.py -h```
