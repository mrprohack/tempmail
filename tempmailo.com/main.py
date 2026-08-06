import re
import time

import requests

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

_session = requests.Session()
_token_cache = None


def _get_verification_token():
    """Fetch the ASP.NET antiforgery token from the homepage (cached)."""
    global _token_cache
    if _token_cache:
        return _token_cache
    html = _session.get(BASE_URL + '/', headers=HEADERS, timeout=10).text
    match = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', html)
    if not match:
        raise RuntimeError("Could not extract RequestVerificationToken from tempmailo.com")
    _token_cache = match.group(1)
    return _token_cache


def get_new_email():
    """Get a fresh temp email address from tempmailo.com."""
    headers = {**HEADERS, 'RequestVerificationToken': _get_verification_token()}
    params = {'_r': str(time.time()).replace('.', '')[:16]}
    response = _session.get(f"{BASE_URL}/changemail", headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return {"email": response.text.strip()}


def read_email(email_address):
    """Check the inbox for a tempmailo.com address."""
    headers = {**HEADERS, 'RequestVerificationToken': _get_verification_token()}
    response = _session.post(BASE_URL + '/', headers=headers, json={"mail": email_address}, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    email = get_new_email()
    print(f"Email: {email}")
    time.sleep(2)
    messages = read_email(email.get("email"))
    print(f"Messages: {messages}")
