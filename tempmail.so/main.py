import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://tempmail.so/us/api/inbox"
HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

COOKIE = "tm_session=JiG4Bn%2BJEpf3rPSLQwtLPODHdtXEX1vGmipcz%2F%2Fpd%2BeCofzrWmni8uhBZ0NAKycaI%2F%2FAiNz5vg5iu0%2FQz0J02zTewSc%2BGagp5F0EosBeHAbMGfRatTgclq7gbyITECAJFCTcm2CI6C8iw0Kg%2BVBnqVXYZ13FFOPERAKpOpT2DypAKUdslmX5dTWcWE0asQEPIpoQRyXdnnc68fGsE4Uzw01bM%2BitjIo31IuhP4ONhrOCnwugirwVB6KFy%2FAAAIKilCPiNKaS00jotAd3ryN0chMuwQfKt7HF9xn%2F1QxVPxUNYNfO2LcqhxhzYSX4uLN%2BF8XW3wJ%2F9EStCniIoba%2BPoZbtLKjX0%2FPLWrb41fSskKxa%2Bp7KXBpaEQu4tks1J3t6uHuPcga05HtnKSKsMcJvJ0gcU5rY7Fo6feYi1l9QxPEvNPL%2BE5f9Ox18T4wajDS6QRwL2ReQMVMkB4nUyOJQ1DVuaGg5eMdmK2vkjDc3h%2Bv0ysnctjiIHC%2FNFbE9t%2BQ"

def get_inbox():
    params = {"requestTime": str(int(time.time() * 1000)), "lang": "us"}
    headers = {**HEADERS, 'cookie': COOKIE}
    try:
        resp = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get inbox: {e}")
    return {}

def main():
    inbox = get_inbox()
    print(f"Inbox: {inbox}")

if __name__ == "__main__":
    main()
