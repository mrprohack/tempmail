import requests
import time
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.internal.temp-mail.io"
HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://temp-mail.io',
    'referer': 'https://temp-mail.io/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_new_email():
    try:
        resp = requests.post(f"{BASE_URL}/api/v3/email/new", headers=HEADERS, json={
            "min_name_length": 10, "max_name_length": 10
        }, timeout=10)
        if resp.status_code == 200:
            return resp.json()['email']
    except Exception as e:
        logger.error(f"Failed to get email: {e}")
    return None

def get_messages(email_id):
    try:
        resp = requests.get(f"{BASE_URL}/api/v3/email/{email_id}/messages", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get messages: {e}")
    return []

def extract_url(email_id):
    messages = get_messages(email_id)
    for msg in messages:
        body = msg.get('body_text', '')
        match = re.search(r'https://[^\s<>"]+', body)
        if match:
            return match.group(0)
    return None

def main():
    email = get_new_email()
    print(f"Email: {email}")
    if email:
        url = extract_url(email)
        print(f"URL found: {url}")

if __name__ == "__main__":
    main()
