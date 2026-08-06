import requests
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://tempmail.so/us/api/inbox"
HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

# IMPORTANT: This cookie expires quickly (hours). You must obtain a fresh
# tm_session cookie from a browser session at https://tempmail.so and
# paste it below. The hard-coded value below is a placeholder and WILL FAIL.
COOKIE = "tm_session=REPLACE_WITH_FRESH_COOKIE_FROM_BROWSER"


def get_inbox():
    params = {"requestTime": str(int(time.time() * 1000)), "lang": "us"}
    headers = {**HEADERS, 'cookie': COOKIE}
    try:
        resp = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        # Surface the actual HTTP error instead of returning {} silently
        logger.error(f"HTTP {resp.status_code}: {resp.text}")
        raise RuntimeError(f"Inbox request failed with status {resp.status_code}")
    except requests.RequestException as e:
        logger.error(f"Network error getting inbox: {e}")
        raise


def main():
    try:
        inbox = get_inbox()
    except RuntimeError as e:
        logger.error(f"Cannot fetch inbox: {e}")
        sys.exit(1)
    print(f"Inbox: {inbox}")


if __name__ == "__main__":
    main()
