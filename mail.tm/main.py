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
            # API historically returned {"hydra:member": [...]} or {"data": [...]},
            # but now returns a bare JSON list. Handle all three shapes.
            if isinstance(data, list):
                members = data
            elif isinstance(data, dict):
                members = data.get('hydra:member') or data.get('data') or []
            else:
                members = []
            for entry in members:
                if isinstance(entry, dict) and entry.get('domain'):
                    _DOMAINS_CACHE = entry['domain']
                    return _DOMAINS_CACHE
    except Exception as e:
        logger.error(f"Failed to get domain: {e}")
    # Do NOT fall back to "mail.tm" - it is not a valid registration domain.
    # Signal failure so the caller can react instead of proceeding with garbage.
    raise RuntimeError("Could not resolve a valid mail.tm domain from the API")

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
    try:
        email, password = random_email()
    except RuntimeError as e:
        logger.error(f"Cannot start: {e}")
        raise SystemExit(1)
    print(f"Email: {email}")

    if not create_account(email, password):
        logger.error("Account creation failed")
        raise SystemExit(1)
    print("Account created")

    token = get_token(email, password)
    if not token:
        logger.error("Token fetch failed")
        raise SystemExit(1)
    print(f"Token: {token[:50]}...")

    inbox = get_inbox(token)
    print(f"Inbox: {inbox}")
    members = inbox.get("hydra:member") if isinstance(inbox, dict) else inbox
    if members:
        msg = get_message(token, members[0]["id"])
        print(f"Message: {msg}")

if __name__ == "__main__":
    main()
