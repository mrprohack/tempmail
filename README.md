# Temp Mail Services

Python utilities for working with temporary email services. Supports multiple providers with a unified interface.

## Supported Services

| Service | Domain | Status |
|---------|--------|--------|
| TempMailo | tempmailo.com | ✅ Working |
| Mail.tm | mail.tm | ✅ Working |
| Temp-Mail.io | temp-mail.io | ✅ Working |
| TempMail.so | tempmail.so | ✅ Working |
| TempMail.plus | tempmail.plus | ✅ Working |
| MCP Server | tempmail-mcp | ✅ Fast |

## Quick Start with uv (Recommended)

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run any service
uv run python tempmailo.com/main.py
uv run python mail.tm/main.py
uv run python tempmail.plus/main.py
```

## MCP Server (Model Context Protocol)

Fast MCP server for AI assistants to use temp email services.

### Install & Run

```bash
cd mcp
uv sync                    # Install dependencies
uv run python server.py    # Start MCP server (stdio)
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `get_temp_email` | Create temp email (tempmailo, mailtm, tempmailplus) |
| `check_inbox` | Check inbox for email |
| `read_message` | Read message by ID |
| `extract_urls` | Extract URLs from email content |

### Example MCP Usage

```json
{
  "tool": "get_temp_email",
  "arguments": {"provider": "tempmailo"}
}
// Returns: {"email": "test123@tempmailo.com"}
```

## Installation (pip)

```bash
pip install -r tempmailo.com/requirements.txt
```

Required packages:
- `requests`
- `browsercookie`
- `beautifulsoup4`

## Usage

```bash
python tempmailo.com/main.py
python mail.tm/main.py
python temp-mail.io/main.py
python tempmail.so/main.py
python tempmail.plus/main.py
```

### Example Output

```python
# tempmailo.com
Email: {'email': 'test123@tempmailo.com'}
Messages: []

# mail.tm  
Email: abc123@mail.tm
Inbox: {'hydra:member': [...]}

# tempmail.plus
Email: test123@merepost.com
Inbox: {'result': True, 'mail_list': [...]}
```

## Running Tests

```bash
# Main services
cd tempmailo.com && python -m pytest cookie_test/ -v

# MCP server
cd mcp && uv run pytest test_server.py -v
```

**Test Results:** 13/13 passing (main) + 12/12 (MCP)

## Project Structure

```
tempmail/
├── README.md              # This file
├── AGENTS.md              # Guidelines for AI agents
├── .gitignore             # Git ignore rules
├── tempmailo.com/
│   ├── main.py           # TempMailo service
│   ├── requirements.txt  # Dependencies
│   └── cookie_test/
│       └── tests.py      # Unit tests
├── mail.tm/
│   └── main.py           # Mail.tm service
├── temp-mail.io/
│   └── main.py           # Temp-Mail.io service
├── tempmail.so/
│   └── main.py           # TempMail.so service
├── tempmail.plus/
│   └── main.py           # TempMail.plus service
└── mcp/
    ├── pyproject.toml    # uv project config
    ├── server.py         # MCP server
    └── test_server.py    # MCP tests
```

## Features

- Generate random temporary email addresses
- Check inbox for received emails
- Extract URLs from email content
- Simple CLI interface (no user input required)
- MCP server for AI assistant integration
- Fast with shared HTTP session and caching
- Consistent API across all providers

## License

MIT
