import pickle
import os

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import pymsgbox


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    HOST = 'localhost'
    PORT = 8080
    cred = None
    displayMessage = False


    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    else:
        displayMessage = True

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        # pymsgbox.alert('Report Successfully Exported to Google Drive', 'Google Drive Export', timeout=2000)
        print(API_SERVICE_NAME, 'service created successfully')
        return (service, displayMessage)
    except Exception as e:
        print('Unable to connect.')
        print(e)
        pymsgbox.alert('Report Failed to Export to Google Drive', 'Google Drive Export', timeout=2000)
        return (None, displayMessage)
