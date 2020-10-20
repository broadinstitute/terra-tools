##!/usr/bin/env python

import argparse
import os
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials


def get_access_token(json_credentials, new_scopes=None):
    """Takes a path to a service account's json credentials file and return an access token with scopes."""
    scopes = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

    if new_scopes is not None:
        if isinstance(new_scopes, list):
            scopes = scopes + new_scopes
        else:
            print("Could not parse scopes. If you want to add additional scopes, add them as a list.")
            print("For example: "
                  "\n\tpython get_access_token.py <credentials/default> \"['https://www.googleapis.com/auth/cloud-platform']\"")
            exit(1)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_credentials, scopes=scopes)

    return credentials.get_access_token().access_token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get an access token for a service account for use in Terra.")

    parser.add_argument('-j', '--json_credentials', help='Path to the json credentials file for this service account.')
    parser.add_argument('-d', '--default', action='store_true', help='Print application default credentials access token.')
    parser.add_argument('--new_scopes', type=list, help='Additional scopes to add, in the form of a list')

    args = parser.parse_args()

    if args.default:
        print(GoogleCredentials.get_application_default().get_access_token().access_token)
        exit(1)
    if args.json_credentials is None or not os.path.isfile(args.json_credentials):
        print("This script will print out an access token for either the application default credentials or for a service account.  "
              "\nOnly the token is printed so this can be combined with other commands such as curl calls.")
        print("Usage: "
              "\n\tpython3 get_access_token.py -d (to get access token for the application default credentials)"
              "\n\tpython3 get_access_token.py -j <path to service account json file> (to get access token for a service account)")
        exit(1)

    print(get_access_token(args.json_credentials, args.new_scopes))
