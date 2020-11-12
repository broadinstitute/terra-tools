##!/usr/bin/env python

import argparse
import requests

from oauth2client.service_account import ServiceAccountCredentials
from firecloud import api as fapi


def main(args):
    # set up scopes and credentials
    scopes = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(args.json_credentials, scopes=scopes)
    headers = {"Authorization": "bearer " + credentials.get_access_token().access_token}
    headers["User-Agent"] = fapi.FISS_USER_AGENT

    uri = args.fc_url + "/register/profile"

    profile_json = {
        "firstName": "None",
        "lastName": "None",
        "title": "None",
        "contactEmail": args.owner_email,
        "institute": "None",
        "institutionalProgram": "None",
        "programLocationCity": "None",
        "programLocationState": "None",
        "programLocationCountry": "None",
        "pi": "None",
        "nonProfitStatus": "false"
    }
    request = requests.post(uri, headers=headers, json=profile_json)

    if request.status_code == 200:
        print(f"The service account {credentials._service_account_email} is now registered with Terra. You can share workspaces with this address, or use it to call APIs.")
    else:
        print(f"Unable to register service account: {request.text}")


if __name__ == "__main__":
    # The main argument parser
    parser = argparse.ArgumentParser(description="Register a service account for use in Terra.")

    # Core application arguments
    parser.add_argument('-j', '--json_credentials', dest='json_credentials', action='store', required=True, help='Path to the json credentials file for this service account.')
    parser.add_argument('-e', '--owner_email', dest='owner_email', action='store', required=True, help='Email address of the person who owns this service account')
    parser.add_argument('-u', '--url', dest='fc_url', action='store', default="https://api.firecloud.org", required=False, help='Base url of FireCloud server to contact (default https://api.firecloud.org)')

    args = parser.parse_args()

    main(args)
