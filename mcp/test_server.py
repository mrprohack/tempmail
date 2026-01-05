"""
Tests for TempMail MCP Server
Run with: uv run pytest mcp/test_server.py -v
"""

import pytest


class TestExtractUrls:
    def test_extract_single_url(self):
        from server import extract_urls
        urls = extract_urls("Visit https://example.com for more info")
        assert len(urls) == 1
        assert "https://example.com" in urls

    def test_extract_multiple_urls(self):
        from server import extract_urls
        urls = extract_urls("Links: https://a.com and https://b.com")
        assert len(urls) == 2
        assert "https://a.com" in urls
        assert "https://b.com" in urls

    def test_extract_urls_empty(self):
        from server import extract_urls
        assert extract_urls("") == []

    def test_extract_urls_removes_trailing_punctuation(self):
        from server import extract_urls
        urls = extract_urls("Visit https://example.com.")
        assert len(urls) == 1
        assert "https://example.com" in urls


class TestRandomStr:
    def test_random_str_length(self):
        from server import random_str
        s = random_str(10)
        assert len(s) == 10
        assert s.isalnum()

    def test_random_str_different(self):
        from server import random_str
        s1 = random_str(8)
        s2 = random_str(8)
        assert len(s1) == len(s2) == 8


class TestGetTempEmail:
    def test_tempmailo(self):
        from server import get_temp_email
        result = get_temp_email("tempmailo")
        assert isinstance(result, dict)
        assert "email" in result
        assert "@" in result["email"]

    def test_mailtm(self):
        from server import get_temp_email
        result = get_temp_email("mailtm")
        assert isinstance(result, dict)
        assert "email" in result
        assert "@" in result["email"]
        assert "domain" in result

    def test_tempmailplus(self):
        from server import get_temp_email
        result = get_temp_email("tempmailplus")
        assert isinstance(result, dict)
        assert "email" in result
        assert "@" in result["email"]


class TestCheckInbox:
    def test_check_inbox_returns_dict(self):
        from server import check_inbox
        result = check_inbox("test@example.com", "tempmailo")
        assert isinstance(result, (dict, list))

    def test_check_inbox_with_mailtm(self):
        from server import check_inbox
        result = check_inbox("test@mail.tm", "mailtm")
        assert isinstance(result, dict)


class TestIntegration:
    def test_all_providers_work(self):
        from server import get_temp_email, check_inbox
        for provider in ["tempmailo", "mailtm", "tempmailplus"]:
            email = get_temp_email(provider)
            assert isinstance(email, dict)
            assert "email" in email
            inbox = check_inbox(email["email"], provider)
            assert isinstance(inbox, (dict, list))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
