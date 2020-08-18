# Author - Alap Raval | Northwestern University
# Reference - https://github.com/nrccua/file_export_sample
# Using python 3.7.2
# pip install -r requirements.txt
# Store your credentials in config.py file
# USERNAME = ""
# PASSWORD = ""
# ORGANIZATION_UID = ""
# API_KEY = ""
# FTP_USERNAME = ""
# FTP_PASSWORD = ""

# Run python ACT_download_script.py command in terminal/command prompt or use it in your scheduler

import requests
import json
import os
import re
from urllib.parse import urlparse, unquote
from pathlib import Path
import pysftp
from datetime import date 
import config

# SET THE API URL
URL = "https://api.datalab.nrccua.org/v1"
DOWNLOAD_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = Path(DOWNLOAD_DIR)

# Encoura Service Account credentials
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
ORGANIZATION_UID = config.ORGANIZATION_UID
API_KEY = config.API_KEY

# Your Technolutions FTP login credentials
FTP_USERNAME = config.FTP_USERNAME
FTP_PASSWORD = config.FTP_PASSWORD

TODAY = date.today()
TODAY = TODAY.strftime("%B %d, %Y")

def get_valid_filename(s):
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)

def copy_to_slate(file):
    print(f"Copying file to Slate ftp server.\n")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection('ft.technolutions.net', username=FTP_USERNAME, password=FTP_PASSWORD, cnopts=cnopts) as sftp:
        with sftp.cd('/incoming/test_scores'):           # temporarily chdir to test_scores directory
            sftp.put(file)  	# upload file to test_scores on ftp server
            print(f"File has been copied.\n")


# payload to login and get session token.
payload = {"userName": USERNAME, "password": PASSWORD, "acceptedTerms": True}

session = requests.Session()

# set the api key for the rest of the session
session.headers.update({"x-api-key": API_KEY})

# login
response_json = session.post(f"{URL}/login", data=json.dumps(payload)).json()

if "sessionToken" not in response_json:
    print(f"Couldn't find sessionToken in response json:\n {response_json}\n")

# set the authorization header for the rest of the session
session.headers.update({"Authorization": f"JWT {response_json['sessionToken']}"})

print(f"{TODAY} \n Downloading ACT score files since last download.\n")

# payload to return list of files
get_exports_payload = {"status": "NotDelivered", "productKey": "score-reporter"}
response_json = session.get(
    f"{URL}/datacenter/exports", params=get_exports_payload, headers={"Organization": ORGANIZATION_UID},
).json()

# loop through results
files_to_download = []
for export in response_json:
    if "uid" in export:
        export_uid = export["uid"]
        # api route for download
        file_export_url = f"{URL}/datacenter/exports/{export_uid}/download"
        export_response_json = session.get(file_export_url, headers={"Organization": ORGANIZATION_UID}).json()
        if "downloadUrl" in export_response_json:
            files_to_download.append(export_response_json["downloadUrl"])

if len(files_to_download) > 0:
    print(f"File Listings received. There are {len(files_to_download)} file(s) available.\n")
    for file in files_to_download:
        parsed_url = urlparse(file)
        # get the file name from the url, unescape it, and then replace whitespace with underscore
        escaped_filename = get_valid_filename(unquote(os.path.basename(parsed_url.path)))
        download_path = DOWNLOAD_DIR / escaped_filename
        # print(f"Downloading file from url {file}")
        # don't use the session here
        download_file_response = requests.get(file, allow_redirects=True, stream=True)
        if download_file_response.ok:
            print(f"Downloading file to {download_path}.\n")
            with open(download_path, "wb") as f:
                # we are going to chunk the download because we don't know how large the files are
                for chunk in download_file_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            copy_to_slate(download_path)
        else:
            print(f"There was an error retrieving {file} with status code {download_file_response.status_code}.")
            print(f"{download_file_response.content}\n")
else:
    print(f"No file is available to download.\n")