## Register a service account for use in Terra
This script will register a service account so that it can be used in Terra.  This means that the service account can be used to call any of the Terra APIs, and that a given workspace/method can be shared with the service account.

In order to run this script you will need to download the credentials JSON file for your service account.  See https://cloud.google.com/storage/docs/authentication#generating-a-private-key for information on creating a service account credentials JSON file.

Usage (from the main directory):

```python3 scripts/register_service_account/register_service_account.py -j <path to your service account credentials json file> -e <email address for owner of this service account, it's where notifications will go>```

Usage (using Docker):

```docker run --rm -it -v "$HOME"/.config:/.config -v <path to your service account credentials json file>:/svc.json broadinstitute/firecloud-tools python /scripts/register_service_account/register_service_account.py -j /svc.json -e <email address for owner of this service account, it's where notifications will go>```

You can verify that the registration worked by running the following curl command, after authorizing as the service account:
1. Authorize as the SA: `gcloud auth activate-service-account --key-file=PATH_TO_JSON_KEY_FILE`
2. Run: `curl -X GET "https://api.firecloud.org/me?userDetailsOnly=false" -H "accept: application/json" -H "Authorization: Bearer $(gcloud auth --account=SERVICE_ACCOUNT_NAME print-access-token)"`
