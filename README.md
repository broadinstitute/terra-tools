# Tools for use with Terra

To run a giving script using Docker:

  * `docker run --rm -it -v "$HOME"/.config:/.config broadinstitute/firecloud-tools python3 /scripts/<script name.py> <arguments>`

## Prerequisites
* Install the Google Cloud SDK from https://cloud.google.com/sdk/downloads
* Set the Application Default Credentials (run `gcloud auth application-default login`)
* Python 3.7

When running without the docker, check the packages in `requirements.txt`.