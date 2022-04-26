import pickle
import os

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    HOST = 'localhost'
    PORT = 8080
    cred = None
    displayMessage = False


    # pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    # if os.path.exists(pickle_file):
    #     with open(pickle_file, 'rb') as token:
    #         cred = pickle.load(token)

    # if not cred or not cred.valid:
    #     if cred and cred.expired and cred.refresh_token:
    #         cred.refresh(Request())
    #     else:


    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = 'https://flpinventory.com/report/'
    authorization_url, state = flow.authorization_url(access_type='offline', prompt='select_account', include_granted_scopes='true')
    # Set redirect URI
    # Generate Auth URL
    # Redirect Auth URL


    # with open(pickle_file, 'wb') as token:
    #     pickle.dump(cred, token)
    # else:
    #     displayMessage = True
