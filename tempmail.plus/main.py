import requests
import random
import re

def creat_random_email():
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    domains = ['mailto.plus','fexpost.com','fexbox.org','mailbox.in.ua','rover.info','chitthi.in','fextemp.com','any.pink','merepost.com']
    email = f'{random_string}@{random.choice(domains)}'
    return email

def get_inbox(email):
    url = 'https://tempmail.plus/api/mails'
    params = {
        'email': email,
        'limit': 20,
        'epin': ''
    }
    headers = {
        'sec-ch-ua-platform': 'Linux',
        'Referer': 'https://tempmail.plus/en/',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # print(response.json())
        email_id = response.json()['first_id']
        return email_id
    else:
        print(f"Error: {response.status_code}")

def read_email(email_id, email):
    url = f'https://tempmail.plus/api/mails/{email_id}'
    params = {
        'email': email,
        'epin': ''
    }
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'email={email}',
        'priority': 'u=1, i',
        'referer': 'https://tempmail.plus/en/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Linux',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def return_url(data):
    urls = set()  # Use a set to avoid duplicate URLs

    # Extract URLs from the 'html' field
    html_content = data.get('html', '')
    urls.update(re.findall(r'https?://[^\s]+', html_content))

    # Extract URLs from the 'text' field
    text_content = data.get('text', '')
    urls.update(re.findall(r'https?://[^\s]+', text_content))

    # Print the extracted URLs
    for url in urls:
        print(url)

if __name__ == "__main__":
    check = input("Do you want to create a new email? (y/n): ")
    if check == "y":
        email = creat_random_email()
        print(email)
        input("Press Enter to read the inbox")
        email_id = get_inbox(email)
        data = read_email(email_id, email)
        if data:
            return_url(data)
    else:
        email = input("Enter your email: ")
        email_id = get_inbox(email)
        data = read_email(email_id, email)
        if data:
            return_url(data)
