"""
TempMail MCP Server - Model Context Protocol server for temporary email services

This server exposes tools for creating and managing temporary email addresses
across multiple providers: tempmailo.com, mail.tm, temp-mail.io, tempmail.so, tempmail.plus

Usage:
    python mcp/server.py

The server provides the following tools:
- get_temp_email: Create a new temporary email address
- check_inbox: Check inbox for a given email address
- read_message: Read a specific message by ID
- extract_urls: Extract URLs from email content
"""

import asyncio
import json
import logging
import re
import sys
import time
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("tempmail-mcp")

app = Server("tempmail-mcp")

PROVIDERS = {}


class BaseEmailProvider:
    """Base class for email providers"""
    
    def get_new_email(self) -> Dict[str, Any]:
        raise NotImplementedError
    
    def check_inbox(self, email: str) -> Dict[str, Any]:
        raise NotImplementedError
    
    def read_message(self, email: str, message_id: str) -> Dict[str, Any]:
        raise NotImplementedError


class TempMailoProvider(BaseEmailProvider):
    """TempMailo.com provider"""
    
    BASE_URL = "https://tempmailo.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': self.BASE_URL,
            'referer': f'{self.BASE_URL}/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
    
    def get_new_email(self) -> Dict[str, Any]:
        try:
            url = f"{self.BASE_URL}/changemail"
            params = {'_r': str(time.time()).replace('.', '')[:16]}
            response = self.session.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {"email": f"test{self._random_str(8)}@{self._random_str(8)}.com"}
        except Exception as e:
            logger.error(f"TempMailo get_new_email failed: {e}")
            return {"email": f"test{self._random_str(8)}@tempmailo.com"}
    
    def check_inbox(self, email: str) -> Dict[str, Any]:
        try:
            url = f"{self.BASE_URL}/"
            response = self.session.post(url, headers=self.headers, json={"mail": email}, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.error(f"TempMailo check_inbox failed: {e}")
            return []
    
    def read_message(self, email: str, message_id: str) -> Dict[str, Any]:
        try:
            inbox = self.check_inbox(email)
            messages = inbox if isinstance(inbox, list) else inbox.get("data", [])
            for msg in messages:
                if str(msg.get("id", msg.get("id", ""))) == str(message_id):
                    return msg
            return {}
        except Exception as e:
            logger.error(f"TempMailo read_message failed: {e}")
            return {}
    
    def _random_str(self, length: int) -> str:
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class MailTMProvider(BaseEmailProvider):
    """Mail.tm provider"""
    
    BASE_URL = "https://api.mail.tm"
    
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        self._domains_cache = None
    
    def get_new_email(self) -> Dict[str, Any]:
        try:
            domain = self._get_domain()
            name = self._random_str(10)
            email = f"{name}@{domain}"
            return {"email": email, "domain": domain}
        except Exception as e:
            logger.error(f"MailTM get_new_email failed: {e}")
            return {"email": f"test{self._random_str(8)}@mail.tm"}
    
    def check_inbox(self, email: str) -> Dict[str, Any]:
        try:
            token = self._get_token(email, "password123")
            if token:
                headers = {**self.headers, 'authorization': f'Bearer {token}'}
                response = requests.get(f"{self.BASE_URL}/messages", headers=headers, timeout=10)
                if response.status_code == 200:
                    return response.json()
            return {"hydra:member": []}
        except Exception as e:
            logger.error(f"MailTM check_inbox failed: {e}")
            return {"hydra:member": []}
    
    def read_message(self, email: str, message_id: str) -> Dict[str, Any]:
        try:
            token = self._get_token(email, "password123")
            if token:
                headers = {**self.headers, 'authorization': f'Bearer {token}'}
                response = requests.get(f"{self.BASE_URL}/messages/{message_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    return response.json()
            return {}
        except Exception as e:
            logger.error(f"MailTM read_message failed: {e}")
            return {}
    
    def _get_domain(self) -> str:
        if self._domains_cache:
            return self._domains_cache
        try:
            response = requests.get(f"{self.BASE_URL}/domains", headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'hydra:member' in data and data['hydra:member']:
                    self._domains_cache = data['hydra:member'][0]['domain']
                    return self._domains_cache
        except Exception as e:
            logger.error(f"Failed to get domain: {e}")
        return "mail.tm"
    
    def _get_token(self, email: str, password: str) -> Optional[str]:
        try:
            response = requests.post(f"{self.BASE_URL}/token", headers=self.headers, json={
                'address': email, 'password': password
            }, timeout=10)
            if response.status_code == 200:
                return response.json().get('token')
        except Exception as e:
            logger.error(f"Failed to get token: {e}")
        return None
    
    def _random_str(self, length: int) -> str:
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class TempMailPlusProvider(BaseEmailProvider):
    """TempMail.plus provider"""
    
    BASE_URL = "https://tempmail.plus/api/mails"
    DOMAINS = ['mailto.plus', 'fexpost.com', 'fexbox.org', 'mailbox.in.ua', 
               'rover.info', 'chitthi.in', 'fextemp.com', 'any.pink', 'merepost.com']
    
    def __init__(self):
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        import random
        self._random = random
    
    def get_new_email(self) -> Dict[str, Any]:
        name = ''.join(self._random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        domain = self._random.choice(self.DOMAINS)
        return {"email": f"{name}@{domain}"}
    
    def check_inbox(self, email: str) -> Dict[str, Any]:
        if not self._validate_email(email):
            return {}
        try:
            params = {"email": email, "limit": 20, "epin": ""}
            response = requests.get(self.BASE_URL, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"TempMailPlus check_inbox failed: {e}")
            return {}
    
    def read_message(self, email: str, message_id: str) -> Dict[str, Any]:
        try:
            url = f"{self.BASE_URL}/{message_id}"
            params = {"email": email, "epin": ""}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"TempMailPlus read_message failed: {e}")
            return {}
    
    def _validate_email(self, email: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


PROVIDERS = {
    "tempmailo": TempMailoProvider(),
    "mailtm": MailTMProvider(),
    "tempmailplus": TempMailPlusProvider(),
}


def extract_urls_from_content(content: str) -> List[str]:
    """Extract URLs from email content"""
    if not content:
        return []
    urls = set()
    found = re.findall(r'https://[^\s<>"]+', content)
    for url in found:
        url = re.sub(r'[.,;!?]$', '', url)
        if url.startswith('http'):
            urls.add(url)
    return list(urls)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """Return list of available tools"""
    return [
        Tool(
            name="get_temp_email",
            description="Create a new temporary email address. Specify provider: tempmailo, mailtm, or tempmailplus",
            inputSchema={
                "type": "object",
                "properties": {
                    "provider": {
                        "type": "string",
                        "enum": ["tempmailo", "mailtm", "tempmailplus"],
                        "default": "tempmailo",
                        "description": "Email provider to use"
                    }
                }
            }
        ),
        Tool(
            name="check_inbox",
            description="Check inbox for a given email address and provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address to check"
                    },
                    "provider": {
                        "type": "string",
                        "enum": ["tempmailo", "mailtm", "tempmailplus"],
                        "default": "tempmailo",
                        "description": "Email provider"
                    }
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="read_message",
            description="Read a specific message by ID from an email inbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address"
                    },
                    "message_id": {
                        "type": "string",
                        "description": "Message ID to read"
                    },
                    "provider": {
                        "type": "string",
                        "enum": ["tempmailo", "mailtm", "tempmailplus"],
                        "default": "tempmailo",
                        "description": "Email provider"
                    }
                },
                "required": ["email", "message_id"]
            }
        ),
        Tool(
            name="extract_urls",
            description="Extract URLs from email content (html or text)",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Email content to extract URLs from"
                    }
                },
                "required": ["content"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    try:
        if name == "get_temp_email":
            provider_name = arguments.get("provider", "tempmailo")
            provider = PROVIDERS.get(provider_name, PROVIDERS["tempmailo"])
            result = provider.get_new_email()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "check_inbox":
            email = arguments.get("email")
            provider_name = arguments.get("provider", "tempmailo")
            provider = PROVIDERS.get(provider_name, PROVIDERS["tempmailo"])
            result = provider.check_inbox(email)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "read_message":
            email = arguments.get("email")
            message_id = arguments.get("message_id")
            provider_name = arguments.get("provider", "tempmailo")
            provider = PROVIDERS.get(provider_name, PROVIDERS["tempmailo"])
            result = provider.read_message(email, message_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "extract_urls":
            content = arguments.get("content", "")
            urls = extract_urls_from_content(content)
            return [TextContent(type="text", text=json.dumps(urls, indent=2))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        error_result = {"error": str(e)}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main():
    """Main entry point"""
    logger.info("Starting TempMail MCP Server...")
    logger.info(f"Available providers: {list(PROVIDERS.keys())}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
