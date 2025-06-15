import requests
import json
import time
import browsercookie
import logging
import re
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TempMailo:
    def __init__(self):
        self.base_url = "https://tempmailo.com"
        self.session = requests.Session()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://tempmailo.com',
            'referer': 'https://tempmailo.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.get_browser_cookies()

    def get_browser_cookies(self):
        """Get cookies from Chrome browser"""
        logger.info("Getting cookies from Chrome browser...")
        try:
            # Load cookies from Chrome
            chrome_cookies = browsercookie.chrome()
            
            # Create a session to maintain cookies
            self.session = requests.Session()
            self.session.cookies = chrome_cookies
            
            # Make initial request to get all cookies and HTML content
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            # Parse HTML to get the request verification token
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # First try to find meta tag with requestverificationtoken
            token_meta = soup.find('meta', {'name': 'requestverificationtoken'})
            if token_meta and token_meta.get('content'):
                self.headers['requestverificationtoken'] = token_meta.get('content')
                logger.info(f"Found token in meta tag: {token_meta.get('content')[:10]}...")
            else:
                # Try to find form input with __RequestVerificationToken
                token_input = soup.find('input', {'name': '__RequestVerificationToken'})
                if token_input and token_input.get('value'):
                    self.headers['requestverificationtoken'] = token_input.get('value')
                    logger.info(f"Found token in form input: {token_input.get('value')[:10]}...")
                else:
                    # Try to extract token from script tags using regex
                    scripts = soup.find_all('script')
                    for script in scripts:
                        if script.string:
                            token_match = re.search(r'antiforgeryToken[\s]*:[\s]*[\'"]([^\'"]+)[\'"]', script.string)
                            if token_match:
                                self.headers['requestverificationtoken'] = token_match.group(1)
                                logger.info(f"Found token in script: {token_match.group(1)[:10]}...")
                                break
            
            # Add X-XSRF-TOKEN if present in cookies
            if 'XSRF-TOKEN' in self.session.cookies:
                self.headers['X-XSRF-TOKEN'] = self.session.cookies['XSRF-TOKEN']
            
            logger.info("Successfully got cookies from browser")
            # Debug info
            logger.info(f"Cookie count: {len(self.session.cookies)}")
            for cookie in self.session.cookies:
                if 'cf_clearance' in cookie.name:
                    logger.info(f"Found Cloudflare cookie: {cookie.name}")
                if 'AspNetCore' in cookie.name:
                    logger.info(f"Found ASP.NET cookie: {cookie.name}")
            
            if 'requestverificationtoken' not in self.headers:
                logger.warning("Could not find request verification token in page")
                
        except Exception as e:
            logger.error(f"Error getting browser cookies: {e}")
            raise

    def get_new_email_direct(self):
        """Get a new email using direct curl headers and cookies"""
        logger.info("Trying direct curl method to get email...")
        
        # Direct curl headers from user's command
        direct_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': 'https://tempmailo.com/',
            'requestverificationtoken': 'CfDJ8ME6aLb6vcpBt4PDUkX5Re5fziWhsT1QgXdo2xk7YRVANkiEhlkbgGiuhncQt6e-m86KGyQbylmLQUoyuIha772UEVgbX9Rdy-7QBAsGzQDbMq7_vDMIa_3NuCdGuKDUaT5QTK7SHWqdikpk3YWMtqw',
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
        
        # Direct curl cookies from user's command
        direct_cookies = {
            'cf_clearance': '8FFHgpWq1WwnZ5ySJdwBYYk3UMVcbkgfYk2zEOk8h.U-1749562939-1.2.1.1-b4n7Y5VDHTYOcilcEs5vWfoR7p6o.AuNjpgOv5GPTNUxPuDS0LQVkY_gBsBkrUlndCmByKYyMTkS3ULN_SjJmG6sOPnCMJJjwi8xmj_I74U2FrzN8ysIhhjpte3.Md_s3u4AET7C4jZNmLgXilpS8bYgtu5CjzmhIRWF2I9VPgVl.LPHgP8igGrAQcZnqL41cTSd0xgj2iBEwb1ALZFeKIAHZRe5Fpfd5ULfC30rybUyeOLBC5F0HDMDLzcu2lonNt8IhgohDvVEGT7Fvl0noxcMkhafSXeFjd0PBbhHMOYF1t6HRWh580vf.w7TV7To5zRSHLLLhF._LwS_FIl6gz_gI5U01ynOpohOW98VuW8',
            '.AspNetCore.Antiforgery.dXyz_uFU2og': 'CfDJ8ME6aLb6vcpBt4PDUkX5Re7GVXg6GAkCBZGtVnpf2LIv8kb4TgKgVj5wnzeHDRzwkTi31Qt_8o-gPT7SrJCWIQgFo8BMTeLYtRwO2s3jZIUn9epSwVb_PxGoo8Jq5ougXftvMGEWs-Vzv3mwuF8Uvic'
        }
        
        url = f"{self.base_url}/changemail"
        params = {'_r': '0.2495460142978132'}
        
        try:
            response = requests.get(
                url,
                headers=direct_headers,
                cookies=direct_cookies,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Direct curl method failed: {e}")
            return None

    def get_new_email(self):
        """Get a new temporary email address"""
        try:
            # First make sure we're authenticated by visiting the main page
            main_response = self.session.get(self.base_url, headers=self.headers)
            main_response.raise_for_status()
            
            # Try two different API endpoints for getting a new email
            # Method 1: Using /changemail endpoint
            url1 = f"{self.base_url}/changemail"
            params1 = {'_r': str(time.time())}
            
            try:
                response1 = self.session.get(url1, headers=self.headers, params=params1)
                if response1.status_code == 200:
                    return response1.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Method 1 failed: {e}")
            
            # Method 2: Using /api/emails/random endpoint
            url2 = f"{self.base_url}/api/emails/random"
            
            try:
                response2 = self.session.get(url2, headers=self.headers)
                if response2.status_code == 200:
                    return response2.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Method 2 failed: {e}")
            
            # Method 3: Try the direct curl method
            direct_result = self.get_new_email_direct()
            if direct_result:
                return direct_result
            
            # Method 4: If all API methods fail, extract email from HTML
            soup = BeautifulSoup(main_response.text, 'html.parser')
            email_element = soup.select_one('input#email-address')
            if email_element and email_element.get('value'):
                email = email_element.get('value')
                logger.info(f"Extracted email from HTML: {email}")
                return {"email": email}
            
            # If all methods fail, retry with refreshed cookies
            logger.error("All methods failed to get new email, refreshing cookies...")
            self.get_browser_cookies()
            response = self.session.get(url1, headers=self.headers, params=params1)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting new email: {e}")
            return None

    def read_email(self, email_address):
        """Read emails for the given email address"""
        try:
            # Try different API endpoints
            # Method 1: Using POST to main URL
            url1 = f"{self.base_url}/"
            data = {"mail": email_address}
            
            try:
                response1 = self.session.post(
                    url1,
                    headers=self.headers,
                    json=data
                )
                if response1.status_code == 200:
                    return response1.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Method 1 failed: {e}")
            
            # Method 2: Using GET to /api/emails endpoint
            url2 = f"{self.base_url}/api/emails"
            params = {"email": email_address}
            
            try:
                response2 = self.session.get(
                    url2,
                    headers=self.headers,
                    params=params
                )
                if response2.status_code == 200:
                    return response2.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Method 2 failed: {e}")
            
            # If both methods fail, retry with refreshed cookies
            logger.error("All methods failed to read emails, refreshing cookies...")
            self.get_browser_cookies()
            response = self.session.post(
                url1,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reading emails: {e}")
            return None

def main():
    # Create an instance of TempMailo
    temp_mail = TempMailo()
    
    # Get a new email address
    logger.info("Getting new email address...")
    email_result = temp_mail.get_new_email()
    if email_result:
        email_address = email_result.get('email')
        logger.info(f"New email address: {email_address}")
        
        # Wait a few seconds and then check for emails
        logger.info("Waiting for emails...")
        time.sleep(5)
        
        # Read emails
        emails = temp_mail.read_email(email_address)
        if emails:
            logger.info("\nReceived emails:")
            print(json.dumps(emails, indent=2))
        else:
            logger.info("No emails found or error occurred while reading emails")
    else:
        logger.error("Failed to get new email address")

if __name__ == "__main__":
    main()
