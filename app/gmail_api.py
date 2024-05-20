import base64
from datetime import datetime, timedelta
from utils.html_tags import remove_html_tags

async def search_emails(service, subject_keyword, body_keyword):
    """Search for specific emails by keywords in the subject and body."""
    # Calculate the date one month ago from today
    date_today = datetime.now().strftime('%Y/%m/%d')
    date_one_month_ago = (datetime.now() - timedelta(days=90)).strftime('%Y/%m/%d')
    
    # Construct the query with subject and body keywords
    query = f'subject:({subject_keyword}) after:{date_one_month_ago} AND before:{date_today}'
    if body_keyword:
        body_query = " OR ".join(f'"{keyword}"' for keyword in body_keyword)
        query += f" ({body_query})"

    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])

    return messages

async def get_email_body(service, message_id):
    """Get the body of the email."""
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    body = ''

    if 'parts' in message['payload']:
        parts = message['payload']['parts']
        for part in parts:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                data = part['body']['data']
                body = remove_html_tags(base64.urlsafe_b64decode(data).decode('utf-8'))
                break
            elif 'parts' in part:
                for sub_part in part['parts']:
                    if sub_part['mimeType'] == 'text/plain' and 'data' in sub_part['body']:
                        data = sub_part['body']['data']
                        body = remove_html_tags(base64.urlsafe_b64decode(data).decode('utf-8'))
                        break
    elif 'data' in message['payload']['body']:
        data = message['payload']['body']['data']
        body = remove_html_tags(base64.urlsafe_b64decode(data).decode('utf-8'))
    
    return body