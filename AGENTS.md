# AGENTS.md - Guidelines for Agentic Coding

## Build, Lint, and Test Commands

### Installing Dependencies
```bash
pip install -r tempmailo.com/requirements.txt
```

### Running the Application
```bash
python tempmailo.com/main.py
python mail.tm/main.py
python temp-mail.io/main.py
python tempmail.so/main.py
python tempmail.plus/main.py
```

### Running Tests
```bash
cd tempmailo.com && python -m pytest cookie_test/              # Run all tests
cd tempmailo.com && python -m pytest cookie_test/test1.py      # Run specific test file
cd tempmailo.com && python -m pytest cookie_test/test1.py::TestRandomStr  # Run test class
cd tempmailo.com && python -m pytest cookie_test/test1.py::TestRandomStr::test_random_str_length  # Run single test
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
import json
import logging
import re
import time

import browsercookie
import requests
from bs4 import BeautifulSoup

from .utils import helper_function
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
def get_new_email(self) -> Optional[Dict[str, Any]]:
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
- Return `None` or empty dict/list on failure, don't raise for expected cases
- Use `response.raise_for_status()` for HTTP requests
```python
try:
    response = self.session.get(url, headers=self.headers)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to get email: {e}")
    return None
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
- Use `requests.Session()` for persistent connections
- Define headers as class or module constants when reused
- Use `json=` parameter for JSON bodies, `data=` for form data
- Always check `response.status_code` or use `raise_for_status()`

### Security
- Never commit API keys, tokens, or cookies to version control
- Use environment variables for sensitive data
- Validate all inputs before use

### Documentation
- Write docstrings for public classes and methods
- Use triple quotes for docstrings
- Keep docstrings concise but informative
```python
def get_new_email(self) -> Optional[str]:
    """Get a new temporary email address from the service."""
```

### Project Structure
- Each temp mail service gets its own directory
- Shared utilities go in a `utils/` directory
- Tests go in `cookie_test/` subdirectory
- `requirements.txt` per service or root-level for shared dependencies
