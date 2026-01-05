# TODO.md - TempMail Project Improvements

## Overview

This file tracks improvements and enhancements for the TempMail project. All improvements are prioritized in phases.

---

## Code Quality

### Type Hints
- [ ] Add type hints to all functions in `mcp/server.py`
- [ ] Add type hints to `tempmailo.com/main.py`
- [ ] Add type hints to `mail.tm/main.py`
- [ ] Add type hints to `temp-mail.io/main.py`
- [ ] Add type hints to `tempmail.plus/main.py`

### Warnings & Cleanup
- [ ] Fix Pydantic v1/v2 compatibility warnings (Python 3.14)
- [ ] Remove unused `BeautifulSoup` import from `mcp/server.py`
- [ ] Refactor `_mailtm_get_domain()` to handle edge cases better
- [ ] Add unit tests for error handling paths

### Testing
- [ ] Add integration tests with mocks for offline testing
- [ ] Add tests for all new MCP tools
- [ ] Add error handling test cases

---

## New MCP Tools

### delete_email
**Description:** Delete/revoke a temporary email address

**Implementation:**
```python
@mcp.tool()
def delete_email(email: str, provider: str = "tempmailo") -> dict:
    """Delete a temporary email address"""
    # Implementation for each provider
```

**Providers:**
- [ ] tempmailo
- [ ] mailtm
- [ ] tempmailplus

### mark_as_read
**Description:** Mark a message as read

**Implementation:**
```python
@mcp.tool()
def mark_as_read(email: str, message_id: str, provider: str = "tempmailo") -> dict:
    """Mark a message as read"""
    # Implementation for each provider
```

**Providers:**
- [ ] tempmailo
- [ ] mailtm
- [ ] tempmailplus

### search_emails
**Description:** Search emails by sender or subject

**Implementation:**
```python
@mcp.tool()
def search_emails(email: str, query: str, provider: str = "tempmailo") -> dict:
    """Search emails by sender or subject"""
    # Filter inbox results by query
```

**Providers:**
- [ ] tempmailo
- [ ] mailtm
- [ ] tempmailplus

### filter_emails
**Description:** Filter emails by criteria (date, read status)

**Implementation:**
```python
@mcp.tool()
def filter_emails(
    email: str,
    read: Optional[bool] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    provider: str = "tempmailo"
) -> dict:
    """Filter emails by read status or date range"""
    # Filter inbox by criteria
```

**Providers:**
- [ ] tempmailo
- [ ] mailtm
- [ ] tempmailplus

---

## Performance

### Connection Pooling
- [ ] Add HTTP connection pooling with `requests.Session()`
- [ ] Configure connection pool size
- [ ] Add keep-alive settings

### Request Optimization
- [ ] Add request batching for multiple emails
- [ ] Implement exponential backoff for retries
- [ ] Add request deduplication

### Caching
- [ ] Expand domain caching (already exists for mailtm)
- [ ] Add token caching
- [ ] Add response caching for read-only operations

---

## Documentation

### API Reference
- [ ] Document all MCP tools with parameters and return types
- [ ] Add usage examples for each tool
- [ ] Document provider-specific behaviors

### Contributing Guide
- [ ] Create `CONTRIBUTING.md`
- [ ] Add coding standards
- [ ] Add testing requirements
- [ ] Add commit message conventions

### README Updates
- [ ] Add all new MCP tools to README
- [ ] Add architecture diagram
- [ ] Add performance benchmarks
- [ ] Add troubleshooting section

---

## Priority Phases

### Phase 1: Code Quality (Completed) ✅
```
[x] Add type hints to mcp/server.py
[x] Fix Pydantic compatibility warnings  
[x] Add docstrings to public functions
[x] Remove unused imports
[x] Add error handling tests
```

### Phase 2: New MCP Tools (Completed) ✅
```
[x] delete_email - Delete/revoke a temporary email
[x] mark_as_read - Mark message as read
[x] search_emails - Search emails by sender or subject
[x] filter_emails - Filter emails by read status or date range
```

### Phase 3: Performance (Optimization)
```
Priority 10: Add connection pooling
Priority 11: Implement request optimization
Priority 12: Expand caching
```

### Phase 4: Documentation (Polish)
```
Priority 13: Create API reference
Priority 14: Create CONTRIBUTING.md
Priority 15: Update README with all features
```

---

## Progress Tracking

| Category | Total | Completed | In Progress | Pending |
|----------|-------|-----------|-------------|---------|
| Code Quality | 13 | 5 | 0 | 8 |
| New MCP Tools | 12 | 4 | 0 | 8 |
| Performance | 6 | 0 | 0 | 6 |
| Documentation | 6 | 0 | 0 | 6 |
| **Total** | **37** | **9** | **0** | **28** |

### ✅ Completed (Phase 1)
- [x] Add type hints to `mcp/server.py`
- [x] Fix Pydantic compatibility warnings (Python 3.14)
- [x] Remove unused `BeautifulSoup` import
- [x] Add docstrings to all public functions
- [x] Add `delete_email` tool
- [x] Add `mark_as_read` tool
- [x] Add `search_emails` tool
- [x] Add `filter_emails` tool
- [x] Add/update tests for all new tools (24 tests total)

---

## Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/improvement-name`
3. Make changes following code style guidelines in `AGENTS.md`
4. Add tests for new functionality
5. Run tests: `cd mcp && uv run pytest test_server.py -v`
6. Commit: `git commit -m "feat: add new tool or fix"`
7. Push: `git push origin feature/improvement-name`
8. Create PR

---

## Notes

- All new tools must have type hints
- All public functions must have docstrings
- Tests must pass before merging
- Follow naming conventions from `AGENTS.md`
- Use environment variables for API keys (see `.env.example`)
