import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://tempmailo.com"
HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'origin': BASE_URL,
    'referer': f'{BASE_URL}/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def get_new_email(session=None):
    session = session or requests.Session()
    try:
        url = f"{BASE_URL}/changemail"
        params = {'_r': str(time.time()).replace('.', '')[:16]}
        response = session.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"email": f"test{random_str(8)}@tempmailo.com"}
    except Exception as e:
        logger.error(f"Failed to get email: {e}")
        return {"email": f"test{random_str(8)}@tempmailo.com"}

def read_email(email_address, session=None):
    session = session or requests.Session()
    try:
        url = f"{BASE_URL}/"
        response = session.post(url, headers=HEADERS, json={"mail": email_address}, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Failed to read email: {e}")
        return []

def random_str(length):
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def main():
    session = requests.Session()
    email = get_new_email(session)
    print(f"Email: {email}")
    time.sleep(2)
    messages = read_email(email.get("email"), session)
    print(f"Messages: {messages}")

if __name__ == "__main__":
    main()
