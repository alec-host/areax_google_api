import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from store.redis_client import retrieve_token_from_redis,store_token_in_redis

# Scopes for reading emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_api():
    """Authenticate to the Gmail API and return the service object."""
    try:
        creds = None
        token_data = retrieve_token_from_redis()
        if token_data:
            creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Store the updated credentials in Redis
                store_token_in_redis(creds.to_json())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8001)
                # Store the new credentials in Redis
                store_token_in_redis(creds.to_json())
        return build('gmail', 'v1', credentials=creds)
    except BaseException as e:
        print("ERROR: ", e)