import requests

url = 'https://tempmail.so/us/api/inbox?requestTime=1749970572331&lang=us'
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    'cookie': 'tm_session=JiG4Bn%2BJEpf3rPSLQwtLPODHdtXEX1vGmipcz%2F%2Fpd%2BeCofzrWmni8uhBZ0NAKycaI%2F%2FAiNz5vg5iu0%2FQz0J02zTewSc%2BGagp5F0EosBeHAbMGfRatTgclq7gbyITECAJFCTcm2CI6C8iw0Kg%2BVBnqVXYZ13FFOPERAKpOpT2DypAKUdslmX5dTWcWE0asQEPIpoQRyXdnnc68fGsE4Uzw01bM%2BitjIo31IuhP4ONhrOCnwugirwVB6KFy%2FAAAIKilCPiNKaS00jotAd3ryN0chMuwQfKt7HF9xn%2F1QxVPxUNYNfO2LcqhxhzYSX4uLN%2BF8XW3wJ%2F9EStCniIoba%2BPoZbtLKjX0%2FPLWrb41fSskKxa%2Bp7KXBpaEQu4tks1J3t6uHuPcga05HtnKSKsMcJvJ0gcU5rY7Fo6feYi1l9QxPEvNPL%2BE5f9Ox18T4wajDS6QRwL2ReQMVMkB4nUyOJQ1DVuaGg5eMdmK2vkjDc3h%2Bv0ysnctjiIHC%2FNFbE9t%2BQ',
    'priority': 'u=1, i',
    'referer': 'https://tempmail.so/',
    'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-inbox-lifespan': '600'
}

response = requests.get(url, headers=headers)

# Print the response (or handle it as needed)
print(response.json())
