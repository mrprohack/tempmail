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

### Claude Desktop Integration

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tempmail": {
      "command": "uv",
      "args": ["--directory", "/path/to/tempmail", "run", "python", "mcp/server.py"]
    }
  }
}
```

## Groq + LangChain Integration

Test MCP tools with Groq LLM using LangChain adapters.

### Setup

```bash
cd mcp
cp .env.example .env
# Edit .env and add your Groq API key
export $(cat .env | xargs)  # or: export GROQ_API_KEY=your_key
```

### Run Groq + MCP Tests

```bash
source ../.venv/bin/activate
python test_groq_mcp.py
```

### Test Results: 4/4 PASSED ✅

```
============================================================
1. Testing Groq API
============================================================
✅ Groq Response: Groq API working!

============================================================
2. Testing MCP Tools Directly
============================================================
✅ Found 4 tools: get_temp_email, check_inbox, read_message, extract_urls
✅ Email: testjekpnklb@tempmailo.com
✅ URLs: ['https://google.com', 'https://example.com']

============================================================
3. Testing Groq + MCP Combined
============================================================
✅ Got email: testbpvmv29o@tempmailo.com
✅ Recommendation from Groq LLM

============================================================
4. Testing All MCP Providers
============================================================
✅ tempmailo: test7ty55e8u@tempmailo.com
✅ mailtm: am0ug3nday@mail.tm
✅ tempmailplus: nmn7h1r5n7@any.pink
```

### Groq + MCP Combined Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Groq LLM      │────▶│  MCP Server     │────▶│  Temp Email     │
│  (Llama 3.3)    │     │  (4 tools)      │     │  Providers      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
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

# Groq + LangChain + MCP integration tests
cd mcp && source ../.venv/bin/activate && python test_groq_mcp.py
```

**Test Results:**
- Main services: 13/13 passing
- MCP server: 12/12 passing
- Groq + MCP: 4/4 passing

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
    ├── server.py         # MCP server (320 lines, optimized)
    ├── test_server.py    # MCP unit tests (12 tests)
    ├── test_groq_mcp.py  # Groq + LangChain integration tests
    └── .env.example      # Environment template for API keys
```

## Features

- Generate random temporary email addresses
- Check inbox for received emails
- Extract URLs from email content
- Simple CLI interface (no user input required)
- MCP server for AI assistant integration
- Fast with shared HTTP session and caching
- Consistent API across all providers
- Groq LLM integration for intelligent workflows
- LangChain MCP adapters for seamless tool loading

## License

MIT
