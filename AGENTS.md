# AGENTS.md - Guidelines for Agentic Coding

## Build, Lint, and Test Commands

### Installing Dependencies
```bash
# Main services
pip install -r tempmailo.com/requirements.txt

# MCP server (uses uv)
cd mcp && uv sync

# Groq integration
cd mcp && cp .env.example .env
# Then edit .env and add GROQ_API_KEY
```

### Running the Application
```bash
# Main services
python tempmailo.com/main.py
python mail.tm/main.py
python temp-mail.io/main.py
python tempmail.plus/main.py

# MCP server (stdio transport)
cd mcp && uv run python server.py
```

### Running Tests
```bash
# Main services tests
cd tempmailo.com && python -m pytest cookie_test/              # All tests
cd tempmailo.com && python -m pytest cookie_test/test1.py      # Specific file
cd tempmailo.com && python -m pytest cookie_test/test1.py::TestRandomStr  # Test class
cd tempmailo.com && python -m pytest cookie_test/test1.py::TestRandomStr::test_random_str_length  # Single test

# MCP server tests
cd mcp && uv run pytest test_server.py -v                      # All MCP tests
cd mcp && uv run pytest test_server.py::TestExtractUrls -v     # Specific class

# Groq + MCP integration tests
cd mcp && export GROQ_API_KEY=your_key && uv run python test_groq_mcp.py

# Run single Groq test function
cd mcp && uv run python -c "
import asyncio
from test_groq_mcp import test_groq_api
asyncio.run(test_groq_api())
"
```

### Linting
```bash
flake8 . --max-line-length=100 --extend-ignore=E203
pylint tempmailo.com/main.py
black --check .  # Check formatting without modifying
black .          # Auto-format files
```

---

## Code Style Guidelines

### Imports
- Group imports in this order: standard library, third-party, local modules
- Use absolute imports
- Keep imports sorted alphabetically within each group
```python
import asyncio
import json
import logging
import re
import time
from typing import Any, Dict, List, Optional

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
```

### Formatting
- Line length: 100 characters maximum
- Use 4 spaces for indentation (no tabs)
- Use spaces around operators: `x = 1 + 2`
- No spaces inside parentheses: `func(arg1, arg2)`
- Use trailing commas for multi-line collections

### Types
- Use type hints for function signatures
- Prefer explicit types over `Any`
```python
def get_new_email(self) -> Dict[str, Any]:
    ...

def validate_email(email: str) -> bool:
    ...
```
- Use `Optional[X]` instead of `Union[X, None]`

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `TempMailo`, `EmailClient`)
- **Functions/Variables**: `snake_case` (e.g., `get_new_email`, `email_address`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BASE_URL`, `DEFAULT_TIMEOUT`)
- **Private methods**: prefix with underscore (e.g., `_get_cookies`)
- **Module-level private variables**: prefix with underscore (e.g., `_session`)

### Error Handling
- Use `try/except` blocks with specific exception types
- Always log errors with appropriate level
- Return `None`, `{}`, or `[]` on failure, don't raise for expected cases
- Use `response.raise_for_status()` for HTTP requests
```python
try:
    response = self.session.get(url, headers=self.headers)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to get email: {e}")
    return {}
```

### Class Structure
- Use `__init__` for initialization only
- Group methods logically (API methods together, helpers together)
- Use properties for computed attributes
- Keep methods focused and under 50 lines when possible

### Logging
- Use module-level logger: `logger = logging.getLogger(__name__)`
- Configure logging at module entry: `logging.basicConfig(level=logging.INFO)`
- Use appropriate log levels: `DEBUG` for dev, `INFO` for runtime, `WARNING`/`ERROR` for issues

### HTTP Requests
- Use `requests.Session()` for persistent connections across requests
- Define headers as module constants when reused
- Use `json=` parameter for JSON bodies, `data=` for form data
- Always check `response.status_code` or use `raise_for_status()`
- Set reasonable timeouts (5-10 seconds)

### Security
- Never commit API keys, tokens, or cookies to version control
- Use environment variables for sensitive data
- Validate all inputs before use
- Create `.env.example` template for required env vars

### Documentation
- Write docstrings for public classes and methods
- Use triple quotes for docstrings
- Keep docstrings concise but informative
```python
def get_new_email(self) -> Dict[str, Any]:
    """Get a new temporary email address from the service."""
```

### Project Structure
```
tempmail/
├── README.md              # Project documentation
├── AGENTS.md              # This file
├── .gitignore             # Git ignore rules
├── tempmailo.com/         # TempMailo service
│   ├── main.py
│   ├── requirements.txt
│   └── cookie_test/       # Unit tests
├── mail.tm/               # Mail.tm service
│   └── main.py
├── temp-mail.io/          # Temp-Mail.io service
│   └── main.py
├── tempmail.plus/         # TempMail.plus service
│   └── main.py
└── mcp/                   # MCP Server
    ├── pyproject.toml     # uv project config
    ├── server.py          # MCP server (stdio transport)
    ├── test_server.py     # MCP unit tests
    ├── test_groq_mcp.py   # Groq + LangChain integration tests
    ├── .env.example       # Environment template
    └── .venv/             # Virtual environment
```

### MCP Server Guidelines
- MCP server uses `mcp.server.Server` from official SDK
- Tools registered with `@app.list_tools()` decorator
- Tool handlers registered with `@app.call_tool()` decorator
- Use `stdio_server()` for local subprocess communication
- Return `List[TextContent]` from tool handlers
- Log at INFO level for requests, ERROR for failures
