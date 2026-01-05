import requests
import random
import string
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://tempmail.plus/api/mails"
DOMAINS = ['mailto.plus', 'fexpost.com', 'fexbox.org', 'mailbox.in.ua', 'rover.info', 'chitthi.in', 'fextemp.com', 'any.pink', 'merepost.com']
HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def random_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(DOMAINS)}"

def validate_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def get_inbox(email):
    if not validate_email(email):
        return None
    params = {"email": email, "limit": 20, "epin": ""}
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get inbox: {e}")
    return None

def read_email(email_id, email):
    if not email_id:
        return None
    url = f"{BASE_URL}/{email_id}"
    params = {"email": email, "epin": ""}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to read email: {e}")
    return None

def extract_urls(data):
    if not data:
        return []
    urls = set()
    for key in ['html', 'text']:
        content = data.get(key, '')
        found = re.findall(r'https://[^\s<>"]+', content)
        for url in found:
            url = re.sub(r'[.,;!?]$', '', url)
            if url.startswith('http'):
                urls.add(url)
    return list(urls)

def main():
    email = random_email()
    print(f"Email: {email}")
    inbox = get_inbox(email)
    print(f"Inbox: {inbox}")
    if inbox and inbox.get('first_id'):
        msg = read_email(inbox['first_id'], email)
        urls = extract_urls(msg)
        print(f"URLs: {urls}")

if __name__ == "__main__":
    main()
