from argparse import ArgumentParser
import os
import sys
import requests
import csv
import json

from oauth2client.client import GoogleCredentials


def create_table_order_json(headers):
    return None    

# function to get authorization bearer token for requests
def get_access_token():
    """Get access token."""

    scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
    credentials = GoogleCredentials.get_application_default()
    credentials = credentials.create_scoped(scopes)

    return credentials.get_access_token().access_token

if __name__ == "__main__":
    # The main argument parser
    parser = ArgumentParser(description="Add path, file size, and md5 information for all files in a given directory.")

    # Core application arguments
    parser.add_argument('-p', '--project', dest='project', action='store', required=True, help='Project for workspace to update.')
    parser.add_argument('-w', '--workspace_name', dest='workspace_name', action='store', required=True, help='Name of workspace to update.')
    parser.add_argument('-t', '--tsv', dest='tsvs', nargs='+', action='store', required=True, help='Path to tsv(s) to use for updating column ordering.  Order from the TSV file will be used to set the Terra column order.')

    args = parser.parse_args()

    project = args.project
    workspace_name = args.workspace_name

    # Library/publishLibraryWorkspace
    uri = f"https://api.firecloud.org/api/workspaces/{project}/{workspace_name}/updateAttributes"

    # Get access token and and add to headers for requests.
    # -H  "accept: application/json" -H  "Authorization: Bearer [token]"
    headers = {"Authorization": "Bearer " + get_access_token(), "accept": "application/json"}

    column_data = {}
    for tsv in args.tsvs:
        with open(tsv) as tsv_file:
            tsv_reader = csv.reader(tsv_file, delimiter = '\t')
            # loop to iterate through the rows of csv
            for row in tsv_reader:
                
                filtered_rows = [column.replace("entity:", "") for column in row]
                #TODO: get column names without entity:, create json for each, add that to the update json
                column_data[filtered_rows[0].replace("_id", "")] = {"shown":filtered_rows}
                
 
                # breaking the loop after the
                # first iteration itself
                break
   

    update_json = [{"op":"AddUpdateAttribute","attributeName":"workspace-column-defaults","addUpdateAttribute": json.dumps(column_data)}]


    # capture API response and status_code
    response = requests.patch(uri, headers=headers, json=update_json)
    status_code = response.status_code

    # publishing fail
    if status_code not in [200]:
        print(f"WARNING: Failed to update workspace.")
        print("Please see full response for error:")
        print(response.text)
    else:
        print("Successfully updated column ordering.")
    
