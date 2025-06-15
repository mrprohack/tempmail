import requests
import random

headers={
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.7',
    'if-none-match': '"bb1c002561b8f012167b2e1a2bbf1e45"',
    'origin': 'https://mail.tm',
    'priority': 'u=1, i',
    'referer': 'https://mail.tm/',
    'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

def get_domain():
    response = requests.get('https://api.mail.tm/domains', headers=headers)

    if response.status_code == 200:
        data = response.json()
        domain = data['hydra:member'][0]['domain']
        return domain
    else:
        print("Failed to retrieve data:", response.status_code)

def create_random_account():
    domain = get_domain()
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    email_address = f'{random_string}@{domain}'
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    return email_address, password


def get_account(email_address, password):
    response = requests.post('https://api.mail.tm/accounts', headers={
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://mail.tm',
        'priority': 'u=1, i',
        'referer': 'https://mail.tm/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }, json={
        'address': email_address,
        'password': password
    })

    if response.status_code == 201:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)

def get_token(email_address, password):

    response = requests.post('https://api.mail.tm/token', headers={
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://mail.tm',
        'priority': 'u=1, i',
        'referer': 'https://mail.tm/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }, json={
        'address': email_address,
        'password': password
    })

    if response.status_code == 200:
        data = response.json()
        return data['token']
    else:
        print("Failed to retrieve data:", response.status_code)

def get_inbox(token):
    response = requests.get('https://api.mail.tm/messages', headers={
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'authorization': f'Bearer {token}',
        'if-none-match': '"0a4f448ec35e5f2e298782d9de55c215"',
        'origin': 'https://mail.tm',
        'priority': 'u=1, i',
        'referer': 'https://mail.tm/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)

def get_message(token, message_id):
    response = requests.get(f'https://api.mail.tm/messages/{message_id}', headers={
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'authorization': f'Bearer {token}',
        'if-none-match': '"0a4f448ec35e5f2e298782d9de55c215"',
        'origin': 'https://mail.tm',
        'priority': 'u=1, i',
        'referer': 'https://mail.tm/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    })
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)

if __name__ == "__main__":
    email_address, password = create_random_account()
    print(email_address, password)
    account = get_account(email_address, password)
    print(account['id'])
    token = get_token(email_address, password)
    print(token)
    input("Press Enter to continue...")
    inbox = get_inbox(token)
    print(inbox)
    input("Press Enter to continue...")
    message = get_message(token, inbox['hydra:member'][0]['id'])
    print(message)
    input("Press Enter to continue...")
    print(message['html'])