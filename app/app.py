from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.model import EmailSearch,UserInformation
from gmail_auth import authenticate_gmail_api
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

@app.post('/authorize')
async def authorize(user_information: UserInformation):
    if(len(user_information.email) == 0):
        return {"successs":False,"error":True,"message":"Email must be provided."}
    elif(len(user_information.reference_number) == 0):
        return {"successs":False,"error":True,"message":"Reference_number must be provided."}
    else:
        if(is_valid_email(user_information.email)):
            service = authenticate_gmail_api()
            if(service is not None):
                return {"successs":True,"error":False,"message":"Authorization was successful."}
            else:
                return {"successs":False,"error":True,"message":"Authorization has failed."}
        else:
            return {"successs":False,"error":True,"message":"Invalid email."}
    
@app.post('/fetch_emails')
async def fetch_emails(email_search: EmailSearch):
    service = authenticate_gmail_api()
    if(service is not None):
        messages = await search_emails(service, email_search.search_words, "")
        emails = [ await get_email_body(service, message['id']) for message in messages]
        if(len(emails) == 0):
            return []
        else:
            return (emails)
    else:
        return {"successs":True,"error":False,"message":"No credentials provided."}
      
@app.get('/callback')
async def callback():
    return {"successs":True,"error":False,"message":"Success"}

if __name__ == '__main__':
    try:
        import uvicorn
        print('server is running')
        uvicorn.run("app:app", host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt exception caught. Program terminated.\n")