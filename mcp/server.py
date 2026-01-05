"""
TempMail MCP Server - Fast Model Context Protocol server for temp emails

Usage:
    uv run python mcp/server.py

Available tools:
- get_temp_email: Create temp email (tempmailo, mailtm, tempmailplus)
- check_inbox: Check inbox for email
- read_message: Read message by ID
- extract_urls: Extract URLs from email content
"""

import asyncio
import json
import logging
import random
import re
import string
from typing import Any

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("tempmail-mcp")

app = Server("tempmail-mcp")

_URL_RE = re.compile(r'https://[^\s<>"]+')
_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

_SESSION = requests.Session()
_TIMEOUT = 5

_DOMAINS_CACHE = None


def random_str(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def extract_urls(content: str) -> list:
    if not content:
        return []
    urls = set()
    for url in _URL_RE.findall(content):
        url = re.sub(r'[.,;!?]$', '', url)
        if url.startswith('http'):
            urls.add(url)
    return list(urls)


def get_temp_email(provider: str = "tempmailo") -> dict:
    if provider == "mailtm":
        return _mailtm_get_email()
    if provider == "tempmailplus":
        return _tempmailplus_get_email()
    return _tempmailo_get_email()


def check_inbox(email: str, provider: str = "tempmailo") -> dict:
    if provider == "mailtm":
        return _mailtm_check_inbox(email)
    if provider == "tempmailplus":
        return _tempmailplus_check_inbox(email)
    return _tempmailo_check_inbox(email)


def read_message(email: str, message_id: str, provider: str = "tempmailo") -> dict:
    if provider == "mailtm":
        return _mailtm_read_message(email, message_id)
    if provider == "tempmailplus":
        return _tempmailplus_read_message(email, message_id)
    return _tempmailo_read_message(email, message_id)


# TempMailo provider
def _tempmailo_get_email() -> dict:
    try:
        resp = _SESSION.get(
            "https://tempmailo.com/changemail",
            params={'_r': str(int(__import__('time').time() * 1000))},
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://tempmailo.com',
                'referer': 'https://tempmailo.com/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            },
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"tempmailo: {e}")
    return {"email": f"test{random_str(8)}@tempmailo.com"}


def _tempmailo_check_inbox(email: str) -> dict:
    try:
        resp = _SESSION.post(
            "https://tempmailo.com/",
            json={"mail": email},
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0',
            },
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"tempmailo inbox: {e}")
    return []


def _tempmailo_read_message(email: str, message_id: str) -> dict:
    try:
        inbox = _tempmailo_check_inbox(email)
        messages = inbox if isinstance(inbox, list) else inbox.get("data", [])
        for msg in messages:
            if str(msg.get("id")) == str(message_id):
                return msg
    except Exception as e:
        logger.error(f"tempmailo read: {e}")
    return {}


# Mail.tm provider
def _mailtm_get_domain() -> str:
    global _DOMAINS_CACHE
    if _DOMAINS_CACHE:
        return _DOMAINS_CACHE
    try:
        resp = _SESSION.get(
            "https://api.mail.tm/domains",
            headers={'accept': 'application/json'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            data = resp.json()
            # Handle both dict with 'hydra:member' and direct list responses
            if isinstance(data, dict) and data.get('hydra:member'):
                members = data['hydra:member']
            elif isinstance(data, list):
                members = data
            else:
                members = []
            
            if members and isinstance(members, list):
                _DOMAINS_CACHE = members[0]['domain']
                return _DOMAINS_CACHE
    except Exception as e:
        logger.error(f"mailtm domain: {e}")
    return "mail.tm"


def _mailtm_get_token(email: str) -> str:
    try:
        resp = _SESSION.post(
            "https://api.mail.tm/token",
            json={"address": email, "password": "password123"},
            headers={'accept': 'application/json', 'content-type': 'application/json'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json().get('token', '')
    except Exception as e:
        logger.error(f"mailtm token: {e}")
    return ''


def _mailtm_get_email() -> dict:
    domain = _mailtm_get_domain()
    email = f"{random_str(10)}@{domain}"
    return {"email": email, "domain": domain}


def _mailtm_check_inbox(email: str) -> dict:
    token = _mailtm_get_token(email)
    if not token:
        return {"hydra:member": []}
    try:
        resp = _SESSION.get(
            "https://api.mail.tm/messages",
            headers={'accept': 'application/json', 'authorization': f'Bearer {token}'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"mailtm inbox: {e}")
    return {"hydra:member": []}


def _mailtm_read_message(email: str, message_id: str) -> dict:
    token = _mailtm_get_token(email)
    if not token:
        return {}
    try:
        resp = _SESSION.get(
            f"https://api.mail.tm/messages/{message_id}",
            headers={'accept': 'application/json', 'authorization': f'Bearer {token}'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"mailtm read: {e}")
    return {}


# TempMailPlus provider
_TEMPMAILPLUS_DOMAINS = [
    'mailto.plus', 'fexpost.com', 'fexbox.org', 'mailbox.in.ua',
    'rover.info', 'chitthi.in', 'fextemp.com', 'any.pink', 'merepost.com'
]


def _tempmailplus_get_email() -> dict:
    name = random_str(10)
    domain = random.choice(_TEMPMAILPLUS_DOMAINS)
    return {"email": f"{name}@{domain}"}


def _tempmailplus_check_inbox(email: str) -> dict:
    if not _EMAIL_RE.match(email):
        return {}
    try:
        resp = _SESSION.get(
            "https://tempmail.plus/api/mails",
            params={"email": email, "limit": 20},
            headers={'accept': 'application/json', 'user-agent': 'Mozilla/5.0'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"tempmailplus inbox: {e}")
    return {}


def _tempmailplus_read_message(email: str, message_id: str) -> dict:
    try:
        resp = _SESSION.get(
            f"https://tempmail.plus/api/mails/{message_id}",
            params={"email": email},
            headers={'accept': 'application/json', 'user-agent': 'Mozilla/5.0'},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"tempmailplus read: {e}")
    return {}


@app.list_tools()
async def list_tools() -> list:
    return [
        Tool(
            name="get_temp_email",
            description="Create temp email (tempmailo, mailtm, tempmailplus)",
            inputSchema={
                "type": "object",
                "properties": {"provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo"}}
            }
        ),
        Tool(
            name="check_inbox",
            description="Check inbox for email",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo"}
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="read_message",
            description="Read message by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "message_id": {"type": "string"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo"}
                },
                "required": ["email", "message_id"]
            }
        ),
        Tool(
            name="extract_urls",
            description="Extract URLs from email content",
            inputSchema={
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, args: dict) -> list:
    try:
        email = args.get("email", "") or ""
        message_id = args.get("message_id", "") or ""
        
        if name == "get_temp_email":
            result = get_temp_email(args.get("provider", "tempmailo"))
        elif name == "check_inbox":
            result = check_inbox(email, args.get("provider", "tempmailo"))
        elif name == "read_message":
            result = read_message(email, message_id, args.get("provider", "tempmailo"))
        elif name == "extract_urls":
            result = extract_urls(args.get("content", ""))
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown: {name}"}))]
        return [TextContent(type="text", text=json.dumps(result))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    logger.info("Starting TempMail MCP Server...")
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
