import browsercookie
import requests

# Load cookies from Chrome (can also use .firefox())
cj = browsercookie.chrome()

# url = 'https://tempmailo.com/'
url = "https://incognitomail.co/"

# Send request with browser cookies
response = requests.get(url, cookies=cj)
print(response.text)

# Print response cookies
for cookie in response.cookies:
    print(f"{cookie.name} = {cookie.value}")
