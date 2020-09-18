## Export (download) a tsv file for a given entity in a workspace
This script generates a local tsv file for a given entity type ("participant", "sample", "pair", etc.) when the number of individual entities is too large to download from the GUI.

To execute the script, run the following command (from the main directory):
```python3 scripts/export_large_tsv/export_large_tsv.py --project <workspace-project> --workspace <workspace_name> --entity <entity_name> --tsv_filename <output_tsv_filename>```

To get full details on input parameters run the following command (from the main directory):
```python3 scripts/export_large_tsv/export_large_tsv.py -h```
