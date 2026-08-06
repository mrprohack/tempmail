import browsercookie
import requests
import sys


def get_cookies():
    # Load cookies from Chrome (can also use .firefox())
    cj = browsercookie.chrome()

    url = 'https://tempmailo.com/'

    # Send request with browser cookies
    response = requests.get(url, cookies=cj)

    # Print response cookies
    for cookie in response.cookies:
        return f"{cookie.name} = {cookie.value}"


def get_email(cookies_str=None):
    url = 'https://tempmailo.com/changemail'
    params = {'_r': '0.2495460142978132'}

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://tempmailo.com/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    # Parse cookie string into a dictionary
    cookies = {}
    if cookies_str:
        try:
            # Extract cookie name and value
            parts = cookies_str.split(' = ', 1)
            if len(parts) == 2:
                name, value = parts
                cookies[name] = value
                print(f"Using parsed cookie: {name}={value}")
        except Exception as e:
            print(f"Error parsing cookie: {e}")

    # If no valid cookies parsed, use default cookies
    # NOTE: These hard-coded cookies EXPIRE QUICKLY (hours/days).
    # They are EXAMPLES ONLY and will fail with HTTP 400/403.
    # You MUST obtain fresh cookies from a browser session at tempmailo.com.
    if not cookies:
        cookies = {
            'cf_clearance': '8FFHgpWq1WwnZ5ySJdwBYYk3UMVcbkgfYk2zEOk8h.U-1749562939-1.2.1.1-b4n7Y5VDHTYOcilcEs5vWfoR7p6o.AuNjpgOv5GPTNUxPuDS0LQVkY_gBsBkrUlndCmByKYyMTkS3ULN_SjJmG6sOPnCMJJjwi8xmj_I74U2FrzN8ysIhhjpte3.Md_s3u4AET7C4jZNmLgXilpS8bYgtu5CjzmhIRWF2I9VPgVl.LPHgP8igGrAQcZnqL41cTSd0xgj2iBEwb1ALZFeKIAHZRe5Fpfd5ULfC30rybUyeOLBC5F0HDMDLzcu2lonNt8IhgohDvVEGT7Fvl0noxcMkhafSXeFjd0PBbhHMOYF1t6HRWh580vf.w7TV7To5zRSHLLLhF._LwS_FIl6gz_gI5U01ynOpohOW98VuW8',
            '.AspNetCore.Antiforgery.dXyz_uFU2og': 'CfDJ8ME6aLb6vcpBt4PDUkX5Re69vVcwde1KliavPP7aBRXuHEC_e0VWlu0KtebYzqjClbS_zYXrzxR9KgGNpbpvUVwEV65F-cHBk5LxX0H266NnERw1_RoPMJ5aUhgIIMdkRcKq4ahHzky0lxihRttKkA4'
        }
        print("Using default cookies (will likely fail - see NOTE above)")

    response = requests.get(url, params=params, headers=headers, cookies=cookies)

    # Print response info for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:200]}")

    # Check if response is successful and contains JSON
    if response.status_code == 200 and response.text.strip():
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Failed to parse JSON", "content": response.text}
    else:
        raise RuntimeError(f"Request failed with status code {response.status_code}: {response.text[:200]}")


if __name__ == "__main__":
    cookies = get_cookies()
    print(f"Cookies from browser: {cookies}")
    try:
        print(get_email(cookies))
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
