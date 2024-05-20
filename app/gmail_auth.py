import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from store.redis_client import retrieve_token_from_redis,store_token_in_redis
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

# Scopes for reading emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

REDIRECT_URI= os.getenv("REDIRECT_URI")

def _authenticate_gmail_api(email):
    """Authenticate to the Gmail API and return the service object."""
    try:
        creds = None
        token_data = retrieve_token_from_redis(email)
        if token_data:
            creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Store the updated credentials in Redis
                store_token_in_redis(creds.to_json(),email)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=5001)
                # Store the new credentials in Redis
                store_token_in_redis(creds.to_json(),email)
        return build('gmail', 'v1', credentials=creds)
    except BaseException as e:
        print("ERROR: ", e)

def get_authorization_url(email: str):
    flow = Flow.from_client_secrets_file('credentials.json', scopes=SCOPES, redirect_uri=REDIRECT_URI)
    state = json.dumps({'email': email})
    auth_url, _ = flow.authorization_url(prompt='consent',state=quote(state))

    return auth_url

def authenticate_gmail_api(auth_code: str,email: str):
    """Authenticate to the Gmail API using the authorization code and return the service object."""
    try:
        flow = Flow.from_client_secrets_file('credentials.json', scopes=SCOPES, redirect_uri=REDIRECT_URI)
        flow.fetch_token(code=auth_code)

        creds = flow.credentials
        store_token_in_redis(creds.to_json(),email)
        return build('gmail', 'v1', credentials=creds)
    except BaseException as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {e}")
    
def load_credentials(email: str):
    """Load credentials from Redis and return the service object."""
    token_data = retrieve_token_from_redis(email)
    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
        if creds and creds.valid:
            return build('gmail', 'v1', credentials=creds)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            store_token_in_redis(creds.to_json(),email)
            return build('gmail', 'v1', credentials=creds)
    raise HTTPException(status_code=401, detail="Credentials are not valid")