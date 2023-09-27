import requests
import time
import re

headers = {
    'authority': 'api.internal.temp-mail.io',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'application-name': 'web',
    'application-version': '2.2.29',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://temp-mail.io',
    'referer': 'https://temp-mail.io/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}


def get_new_email():
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'

    data = {
        "min_name_length": 10,
        "max_name_length": 10
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:  # If the request is successful
        response_data = response.json()
        return response_data['email']


def get_email(email_id):
    url = f'https://api.internal.temp-mail.io/api/v3/email/{email_id}/messages'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Response JSON:", response.json())
        email_body_text = response.json()[0]['body_text']
        url_pattern = r'https://[^ ]+'
        url_match = re.search(url_pattern, email_body_text)
        if url_match:
            url = url_match.group()
            return url
        else:
            print("No URL found in the email body text.")


if __name__ == '__main__':
    email = get_new_email()
    time.sleep(30)
    url = get_email(email)
