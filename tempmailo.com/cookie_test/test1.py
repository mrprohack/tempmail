import requests

url = 'https://example.com'

# Send a GET request
response = requests.get(url)

# Get cookies
cookies = response.cookies

# Print cookies
for cookie in cookies:
    print(f"{cookie.name} = {cookie.value}")
