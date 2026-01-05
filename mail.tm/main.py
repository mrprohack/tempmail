import requests
import random
import string
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.mail.tm"
HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

_DOMAINS_CACHE = None

def get_domain():
    global _DOMAINS_CACHE
    if _DOMAINS_CACHE:
        return _DOMAINS_CACHE
    try:
        resp = requests.get(f"{BASE_URL}/domains", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if 'hydra:member' in data and data['hydra:member']:
                _DOMAINS_CACHE = data['hydra:member'][0]['domain']
                return _DOMAINS_CACHE
            elif 'data' in data and data['data']:
                _DOMAINS_CACHE = data['data'][0]['domain']
                return _DOMAINS_CACHE
    except Exception as e:
        logger.error(f"Failed to get domain: {e}")
    return "mail.tm"

def random_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = get_domain()
    return f"{name}@{domain}", "password123"

def create_account(email, password):
    try:
        resp = requests.post(f"{BASE_URL}/accounts", headers=HEADERS, json={
            'address': email, 'password': password
        }, timeout=10)
        return resp.status_code == 201
    except Exception as e:
        logger.error(f"Failed to create account: {e}")
        return False

def get_token(email, password):
    try:
        resp = requests.post(f"{BASE_URL}/token", headers=HEADERS, json={
            'address': email, 'password': password
        }, timeout=10)
        if resp.status_code == 200:
            return resp.json()['token']
    except Exception as e:
        logger.error(f"Failed to get token: {e}")
    return None

def get_inbox(token):
    try:
        headers = {**HEADERS, 'authorization': f'Bearer {token}'}
        resp = requests.get(f"{BASE_URL}/messages", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get inbox: {e}")
    return {"hydra:member": []}

def get_message(token, message_id):
    try:
        headers = {**HEADERS, 'authorization': f'Bearer {token}'}
        resp = requests.get(f"{BASE_URL}/messages/{message_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get message: {e}")
    return {}

def main():
    email, password = random_email()
    print(f"Email: {email}")
    
    if create_account(email, password):
        print("Account created")
    
    token = get_token(email, password)
    if token:
        print(f"Token: {token[:50]}...")
        inbox = get_inbox(token)
        print(f"Inbox: {inbox}")
        if inbox.get("hydra:member"):
            msg = get_message(token, inbox["hydra:member"][0]["id"])
            print(f"Message: {msg}")

if __name__ == "__main__":
    main()
