import json
import urllib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from model.model import EmailSearch,UserInformation
from gmail_auth import authenticate_gmail_api,get_authorization_url,load_credentials
from gmail_api import search_emails,get_email_body
from middleware.config import origins,allow_headers,allow_methods
from utils.mail_validate import is_valid_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

@app.get('/callback')
async def callback():
    return JSONResponse(status_code=200,content={"successs":True,"error":False,"message":"Success"})

@app.post('/authorize')
async def authorize(user_information: UserInformation):
    if(len(user_information.email) == 0):
        return JSONResponse(status_code=400,content={"successs":False,"error":True,"message":"Email must be provided."})
    elif(len(user_information.reference_number) == 0):
        return JSONResponse(status_code=400,content={"successs":False,"error":True,"message":"Reference_number must be provided."})
    else:
        if(is_valid_email(user_information.email)):
            auth_url = get_authorization_url(user_information.email)
            if(auth_url is not None):
                return JSONResponse(status_code=200,content={"successs":True,"error":False,"message":auth_url})
            else:
                return JSONResponse(status_code=401,content={"successs":False,"error":True,"message":"Authorization has failed."})
        else:
            return JSONResponse(status_code=400,content={"successs":False,"error":True,"message":"Invalid email."})

@app.get('/oauth2callback')
async def oauth2callback(request: Request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    if not code:
        return JSONResponse(status_code=400,content={"success":False,"error":True,"message": "Authorization code not provided"})
    else:
        if(state):
            decoded_state = urllib.parse.unquote(state)
            data = json.loads(decoded_state)

            authenticate_gmail_api(code,data.get("email"))
            return JSONResponse(status_code=200,content={"success":True,"error":False,"message": "Authentication successful"})
        else:
            return JSONResponse(status_code=400,content={"success":False,"error":True,"message": "Email not provided"})
    
@app.post('/fetch_emails')
async def fetch_emails(email_search: EmailSearch):
    if(is_valid_email(email_search.email)):
        if(len(email_search.search_words) > 0):
            try:
                service = load_credentials(email_search.email)
                if(service is not None):
                    messages = await search_emails(service, email_search.search_words, "")
                    searched_emails = [ await get_email_body(service, message['id']) for message in messages]
                    if(len(searched_emails) == 0):
                        return JSONResponse(status_code=404,content={"successs":True,"error":False,"message":[]})
                    else:
                        return JSONResponse(status_code=200,content={"successs":True,"error":False,"message":searched_emails})
                else:
                    return JSONResponse(status_code=400,content={"successs":True,"error":False,"message":"No credentials provided."})
            except Exception as e:
                return JSONResponse(status_code=e.status_code,content={"successs":False,"error":True,"message": e.detail})
        else:
            return JSONResponse(status_code=400,content={"successs":False,"error":True,"message":"Search keyword has to be provided."})
    else:
        return JSONResponse(status_code=400,content={"successs":False,"error":True,"message":"Invalid email."})

if __name__ == '__main__':
    try:
        import uvicorn
        print('server is running')
        uvicorn.run("app:app", host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt exception caught. Program terminated.\n")