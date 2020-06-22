# Tools for use with Terra

To run a giving script using Docker:

  * `docker run --rm -v "$HOME"/.config:/.config broadinstitute/terra-tools:latest python3 /scripts/<script name.py> <arguments>`


For example, to run the `upload_tsv` script:
`docker run --rm -v "$HOME"/.config:/.config broadinstitute/terra-tools:latest python3 /scripts/upload_tsv.py --tsv <tsv_path> --project <terra_project> --workspace <terra_workspace>`

## Prerequisites
* Install the Google Cloud SDK from https://cloud.google.com/sdk/downloads
* Set the Application Default Credentials (run `gcloud auth application-default login`)
* Python 3.7

When running without the docker, check the packages in `requirements.txt`.