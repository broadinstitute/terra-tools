# -*- coding: utf-8 -*-
"""Common GCS and FISS tools."""

import sys
import logging
import tenacity as tn

from firecloud import errors as ferrors
from google.cloud import storage

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)


def my_before_sleep(retry_state):
    if retry_state.attempt_number < 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    logger.log(
        loglevel, 'Retrying %s with %s in %s seconds; attempt #%s ended with: %s',
        retry_state.fn, retry_state.args, str(int(retry_state.next_action.sleep)), retry_state.attempt_number, retry_state.outcome)


@tn.retry(wait=tn.wait_chain(*[tn.wait_fixed(5)]
                             + [tn.wait_fixed(10)]
                             + [tn.wait_fixed(30)]
                             + [tn.wait_fixed(60)]),
          stop=tn.stop_after_attempt(5),
          before_sleep=my_before_sleep)
def call_fiss(fapifunc, okcode, *args, specialcodes=None, **kwargs):
    ''' call FISS (firecloud api), check for errors, return json response

    function inputs:
        fapifunc : fiss api function to call, e.g. `fapi.get_workspace`
        okcode : fiss api response code indicating a successful run
        *args : args to input to api call
        specialcodes : optional - LIST of response code(s) for which you don't want to retry
        **kwargs : kwargs to input to api call

    function returns:
        response.json() : json response of the api call if successful
        OR
        response : non-parsed API response if you submitted specialcodes

    example use:
        output = call_fiss(fapi.get_workspace, 200, 'help-gatk', 'Sequence-Format-Conversion')
    '''
    # call the api
    response = fapifunc(*args, **kwargs)

    # check for errors; this is copied from _check_response_code in fiss
    if type(okcode) == int:
        # codes = [okcode]
        if specialcodes is None:
            codes = [okcode]
        else:
            codes = [okcode] + specialcodes
    if response.status_code not in codes:
        print(response.content)
        raise ferrors.FireCloudServerError(response.status_code, response.content)
    elif specialcodes is not None:
        return response

    # return the json response if all goes well
    return response.json()


def write_file_to_bucket(local_file_path, file_name, bucket_name):
    """Write a string to a file in a bucket."""
    # set up cloud storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)

    blob.upload_from_string(local_file_path)

    uri = f"gs://{bucket_name}/{file_name}"
    print(f"Saved file to {uri}")

    return uri
