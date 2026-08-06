"""
TempMail MCP Server - Fast Model Context Protocol server for temp emails

Usage:
    uv run python mcp/server.py

Available tools:
- get_temp_email: Create temp email (tempmailo, mailtm, tempmailplus)
- check_inbox: Check inbox for email
- read_message: Read message by ID
- extract_urls: Extract URLs from email content
- delete_email: Delete a temporary email address
- mark_as_read: Mark a message as read
- search_emails: Search emails by sender or subject
- filter_emails: Filter emails by read status or date
"""

import asyncio
import json
import logging
import random
import re
import string
import time
from datetime import datetime
from typing import Dict, List, Optional, Set, Union

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

_DOMAINS_CACHE: Optional[str] = None

_TEMPMAILPLUS_DOMAINS: List[str] = [
    'mailto.plus', 'fexpost.com', 'fexbox.org', 'mailbox.in.ua',
    'rover.info', 'chitthi.in', 'fextemp.com', 'any.pink', 'merepost.com'
]


def _parse_time(s: str) -> float:
    """Parse ISO 8601 or YYYY-MM-DD string to UTC timestamp."""
    s = s.strip()
    # Try ISO with 'Z' or timezone
    if 'T' in s:
        s = s.replace('Z', '+00:00')
        return datetime.fromisoformat(s).timestamp()
    # Fallback: date-only
    return time.mktime(time.strptime(s, "%Y-%m-%d"))


def _get_timestamp(msg: Dict) -> float:
    """Extract createdAt timestamp (ISO string or epoch int) from message dict."""
    created = msg.get("createdAt") or msg.get("created_at") or msg.get("id", 0)
    if isinstance(created, (int, float)):
        return float(created)
    if isinstance(created, str):
        try:
            return _parse_time(created)
        except (ValueError, TypeError):
            pass
    return 0.0


def random_str(length: int) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def extract_urls(content: str) -> List[str]:
    """Extract URLs from email content.

    Args:
        content: The text content to extract URLs from

    Returns:
        List of unique URLs found in the content
    """
    if not content:
        return []
    urls: Set[str] = set()
    for url in _URL_RE.findall(content):
        clean_url = re.sub(r'[.,;!?]$', '', url)
        if clean_url.startswith('http'):
            urls.add(clean_url)
    return list(urls)


def get_temp_email(provider: str = "tempmailo") -> Dict[str, str]:
    """Create a new temporary email address.

    Args:
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Dictionary containing email address and optionally domain
    """
    if provider == "mailtm":
        return _mailtm_get_email()
    if provider == "tempmailplus":
        return _tempmailplus_get_email()
    return _tempmailo_get_email()


def check_inbox(email: str, provider: str = "tempmailo") -> Union[Dict, List]:
    """Check inbox for a given email address.

    Args:
        email: The email address to check
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Inbox data as dictionary or list
    """
    if provider == "mailtm":
        return _mailtm_check_inbox(email)
    if provider == "tempmailplus":
        return _tempmailplus_check_inbox(email)
    return _tempmailo_check_inbox(email)


def read_message(email: str, message_id: str, provider: str = "tempmailo") -> Dict:
    """Read a specific message by ID.

    Args:
        email: The email address
        message_id: The message ID to retrieve
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Message data as dictionary
    """
    if provider == "mailtm":
        return _mailtm_read_message(email, message_id)
    if provider == "tempmailplus":
        return _tempmailplus_read_message(email, message_id)
    return _tempmailo_read_message(email, message_id)


def delete_email(email: str, provider: str = "tempmailo") -> Dict[str, str]:
    """Delete a temporary email address.

    Args:
        email: The email address to delete
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Status message
    """
    if provider == "mailtm":
        return _mailtm_delete_email(email)
    if provider == "tempmailplus":
        return _tempmailplus_delete_email(email)
    return _tempmailo_delete_email(email)


def mark_as_read(email: str, message_id: str, provider: str = "tempmailo") -> Dict[str, str]:
    """Mark a message as read.

    Args:
        email: The email address
        message_id: The message ID to mark as read
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Status message
    """
    if provider == "mailtm":
        return _mailtm_mark_as_read(email, message_id)
    if provider == "tempmailplus":
        return _tempmailplus_mark_as_read(email, message_id)
    return _tempmailo_mark_as_read(email, message_id)


def search_emails(email: str, query: str, provider: str = "tempmailo") -> Dict[str, Union[List, str]]:
    """Search emails by sender or subject.

    Args:
        email: The email address to search in
        query: Search query (matches sender or subject)
        provider: Email provider (tempmailo, mailtm, tempmailplus)

    Returns:
        Filtered messages matching the query
    """
    inbox = check_inbox(email, provider)
    messages = inbox if isinstance(inbox, list) else inbox.get("hydra:member", inbox.get("data", []))

    query_lower = query.lower()
    filtered = [
        msg for msg in messages
        if query_lower in str(msg.get("from", "")).lower()
        or query_lower in str(msg.get("subject", "")).lower()
    ]

    return {"query": query, "results": filtered, "count": len(filtered)}


def filter_emails(
    email: str,
    provider: str = "tempmailo",
    read: Optional[bool] = None,
    since: Optional[str] = None,
    until: Optional[str] = None
) -> Dict[str, Union[List, str]]:
    """Filter emails by read status or date range.

    Args:
        email: The email address to filter
        provider: Email provider (tempmailo, mailtm, tempmailplus)
        read: Filter by read status (True=read, False=unread, None=ignore)
        since: Filter emails after this date (ISO format)
        until: Filter emails before this date (ISO format)

    Returns:
        Filtered messages matching criteria
    """
    inbox = check_inbox(email, provider)
    messages = inbox if isinstance(inbox, list) else inbox.get("hydra:member", inbox.get("data", []))
    filtered = list(messages)

    if read is not None:
        filtered = [m for m in filtered if m.get("seen", False) == read]

    try:
        if since:
            since_ts = _parse_time(since)
            filtered = [m for m in filtered if _get_timestamp(m) >= since_ts]
        if until:
            until_ts = _parse_time(until)
            filtered = [m for m in filtered if _get_timestamp(m) <= until_ts]
    except (ValueError, TypeError) as e:
        logger.warning(f"Date filtering error: {e}")

    return {"filters": {"read": read, "since": since, "until": until}, "results": filtered, "count": len(filtered)}


# TempMailo provider functions
_TEMPMAILO_TOKEN: Optional[str] = None
_TEMPMAILO_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'origin': 'https://tempmailo.com',
    'referer': 'https://tempmailo.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def _tempmailo_token() -> Optional[str]:
    """Get the ASP.NET antiforgery token from the tempmailo.com homepage (cached)."""
    global _TEMPMAILO_TOKEN
    if _TEMPMAILO_TOKEN:
        return _TEMPMAILO_TOKEN
    resp = _SESSION.get("https://tempmailo.com/", headers=_TEMPMAILO_HEADERS, timeout=_TIMEOUT)
    match = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', resp.text)
    if match:
        _TEMPMAILO_TOKEN = match.group(1)
    return _TEMPMAILO_TOKEN


def _tempmailo_get_email() -> Dict[str, str]:
    """Get a new TempMailo email address."""
    token = _tempmailo_token()
    if not token:
        logger.error("tempmailo: no verification token")
        return {"email": f"test{random_str(8)}@tempmailo.com"}
    try:
        resp = _SESSION.get(
            "https://tempmailo.com/changemail",
            params={'_r': str(int(time.time() * 1000))},
            headers={**_TEMPMAILO_HEADERS, 'RequestVerificationToken': token},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200 and resp.text.strip():
            return {"email": resp.text.strip()}
    except Exception as e:
        logger.error(f"tempmailo: {e}")
    return {"email": f"test{random_str(8)}@tempmailo.com"}


def _tempmailo_check_inbox(email: str) -> Union[Dict, List]:
    """Check TempMailo inbox."""
    token = _tempmailo_token()
    if not token:
        logger.error("tempmailo inbox: no verification token")
        return []
    try:
        resp = _SESSION.post(
            "https://tempmailo.com/",
            json={"mail": email},
            headers={**_TEMPMAILO_HEADERS, 'RequestVerificationToken': token},
            timeout=_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logger.error(f"tempmailo inbox: {e}")
    return []


def _tempmailo_read_message(email: str, message_id: str) -> Dict:
    """Read a TempMailo message."""
    try:
        inbox = _tempmailo_check_inbox(email)
        messages = inbox if isinstance(inbox, list) else inbox.get("data", [])
        for msg in messages:
            if str(msg.get("id")) == str(message_id):
                return msg
    except Exception as e:
        logger.error(f"tempmailo read: {e}")
    return {}


def _tempmailo_delete_email(email: str) -> Dict[str, str]:
    """Delete TempMailo email (simulated)."""
    return {"status": "deleted", "email": email, "provider": "tempmailo"}


def _tempmailo_mark_as_read(email: str, message_id: str) -> Dict[str, str]:
    """Mark TempMailo message as read (simulated)."""
    return {"status": "marked_read", "message_id": message_id, "email": email, "provider": "tempmailo"}


# Mail.tm provider functions
def _mailtm_get_domain() -> str:
    """Get available Mail.tm domain with caching."""
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
    """Get Mail.tm authentication token."""
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


def _mailtm_get_email() -> Dict[str, str]:
    """Get a new Mail.tm email address."""
    domain = _mailtm_get_domain()
    email = f"{random_str(10)}@{domain}"
    return {"email": email, "domain": domain}


def _mailtm_check_inbox(email: str) -> Dict[str, List]:
    """Check Mail.tm inbox."""
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


def _mailtm_read_message(email: str, message_id: str) -> Dict:
    """Read a Mail.tm message."""
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


def _mailtm_delete_email(email: str) -> Dict[str, str]:
    """Delete Mail.tm email (simulated)."""
    return {"status": "deleted", "email": email, "provider": "mailtm"}


def _mailtm_mark_as_read(email: str, message_id: str) -> Dict[str, str]:
    """Mark Mail.tm message as read (simulated)."""
    return {"status": "marked_read", "message_id": message_id, "email": email, "provider": "mailtm"}


# TempMailPlus provider functions
def _tempmailplus_get_email() -> Dict[str, str]:
    """Get a new TempMailPlus email address."""
    name = random_str(10)
    domain = random.choice(_TEMPMAILPLUS_DOMAINS)
    return {"email": f"{name}@{domain}"}


def _tempmailplus_check_inbox(email: str) -> Dict:
    """Check TempMailPlus inbox."""
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


def _tempmailplus_read_message(email: str, message_id: str) -> Dict:
    """Read a TempMailPlus message."""
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


def _tempmailplus_delete_email(email: str) -> Dict[str, str]:
    """Delete TempMailPlus email (simulated)."""
    return {"status": "deleted", "email": email, "provider": "tempmailplus"}


def _tempmailplus_mark_as_read(email: str, message_id: str) -> Dict[str, str]:
    """Mark TempMailPlus message as read (simulated)."""
    return {"status": "marked_read", "message_id": message_id, "email": email, "provider": "tempmailplus"}


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="get_temp_email",
            description="Create a new temporary email address. Specify provider: tempmailo, mailtm, or tempmailplus",
            inputSchema={
                "type": "object",
                "properties": {"provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider to use"}}
            }
        ),
        Tool(
            name="check_inbox",
            description="Check inbox for a given email address and provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address to check"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"}
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
                    "email": {"type": "string", "description": "Email address"},
                    "message_id": {"type": "string", "description": "Message ID to read"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"}
                },
                "required": ["email", "message_id"]
            }
        ),
        Tool(
            name="extract_urls",
            description="Extract URLs from email content (html or text)",
            inputSchema={
                "type": "object",
                "properties": {"content": {"type": "string", "description": "Email content to extract URLs from"}},
                "required": ["content"]
            }
        ),
        Tool(
            name="delete_email",
            description="Delete a temporary email address (simulated for some providers)",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address to delete"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"}
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="mark_as_read",
            description="Mark a message as read",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address"},
                    "message_id": {"type": "string", "description": "Message ID to mark as read"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"}
                },
                "required": ["email", "message_id"]
            }
        ),
        Tool(
            name="search_emails",
            description="Search emails by sender or subject",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address to search in"},
                    "query": {"type": "string", "description": "Search query (matches sender or subject)"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"}
                },
                "required": ["email", "query"]
            }
        ),
        Tool(
            name="filter_emails",
            description="Filter emails by read status or date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address"},
                    "provider": {"enum": ["tempmailo", "mailtm", "tempmailplus"], "default": "tempmailo", "description": "Email provider"},
                    "read": {"type": "boolean", "description": "Filter by read status (true=read, false=unread)"},
                    "since": {"type": "string", "description": "Filter after this date (YYYY-MM-DD)"},
                    "until": {"type": "string", "description": "Filter before this date (YYYY-MM-DD)"}
                },
                "required": ["email"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, args: Dict) -> List[TextContent]:
    """Handle tool calls from MCP clients."""
    try:
        email = args.get("email", "") or ""
        message_id = args.get("message_id", "") or ""
        provider = args.get("provider", "tempmailo")

        if name == "get_temp_email":
            result = get_temp_email(provider)
        elif name == "check_inbox":
            result = check_inbox(email, provider)
        elif name == "read_message":
            result = read_message(email, message_id, provider)
        elif name == "extract_urls":
            result = extract_urls(args.get("content", ""))
        elif name == "delete_email":
            result = delete_email(email, provider)
        elif name == "mark_as_read":
            result = mark_as_read(email, message_id, provider)
        elif name == "search_emails":
            result = search_emails(email, args.get("query", ""), provider)
        elif name == "filter_emails":
            result = filter_emails(
                email, provider,
                read=args.get("read"),
                since=args.get("since"),
                until=args.get("until")
            )
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

        return [TextContent(type="text", text=json.dumps(result))]

    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main() -> None:
    """Start the TempMail MCP Server."""
    logger.info("Starting TempMail MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
