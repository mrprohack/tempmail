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

## Installation

```bash
pip install -r tempmailo.com/requirements.txt
```

Required packages:
- `requests`
- `browsercookie`
- `beautifulsoup4`

## Usage

Run any service directly:

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
Token: eyJ0eXAiOiJKV1Qi...
Inbox: {'hydra:member': [...]}

# tempmail.plus
Email: test123@merepost.com
Inbox: {'result': True, 'mail_list': [...]}
```

## Running Tests

```bash
cd tempmailo.com
python -m pytest cookie_test/              # All tests
python -m pytest cookie_test/test1.py      # Specific file
python -m pytest cookie_test/test1.py::TestRandomStr  # Test class
python -m pytest cookie_test/test1.py::TestRandomStr::test_random_str_length  # Single test
```

**Test Results:** 13/13 passing

## Project Structure

```
tempmail/
├── AGENTS.md              # Guidelines for AI agents
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── tempmailo.com/
│   ├── main.py           # TempMailo service
│   ├── requirements.txt  # Dependencies
│   └── cookie_test/
│       ├── test1.py      # Email validation tests
│       └── test2.py      # API tests
├── mail.tm/
│   └── main.py           # Mail.tm service
├── temp-mail.io/
│   └── main.py           # Temp-Mail.io service
├── tempmail.so/
│   └── main.py           # TempMail.so service
└── tempmail.plus/
    └── main.py           # TempMail.plus service
```

## Features

- Generate random temporary email addresses
- Check inbox for received emails
- Extract URLs from email content
- Simple CLI interface (no user input required)
- Consistent API across all providers

## License

MIT
