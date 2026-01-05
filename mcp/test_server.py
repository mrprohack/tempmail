"""
Tests for TempMail MCP Server
Run with: python -m pytest mcp/test_server.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import (
    extract_urls_from_content,
    TempMailoProvider,
    MailTMProvider,
    TempMailPlusProvider,
)


class TestExtractUrls:
    def test_extract_single_url(self):
        content = "Visit https://example.com for more info"
        urls = extract_urls_from_content(content)
        assert len(urls) == 1
        assert "https://example.com" in urls

    def test_extract_multiple_urls(self):
        content = "Links: https://a.com and https://b.com"
        urls = extract_urls_from_content(content)
        assert len(urls) == 2
        assert "https://a.com" in urls
        assert "https://b.com" in urls

    def test_extract_urls_empty(self):
        assert extract_urls_from_content("") == []
        assert extract_urls_from_content(None) == []

    def test_extract_urls_removes_trailing_punctuation(self):
        content = "Visit https://example.com."
        urls = extract_urls_from_content(content)
        assert len(urls) == 1
        assert "https://example.com" in urls

    def test_extract_urls_http_only(self):
        content = "Visit https://example.com and ftp://files.com"
        urls = extract_urls_from_content(content)
        assert len(urls) == 1
        assert "https://example.com" in urls


class TestTempMailoProvider:
    def test_get_new_email_returns_dict(self):
        provider = TempMailoProvider()
        result = provider.get_new_email()
        assert isinstance(result, dict)
        assert "email" in result

    def test_get_new_email_format(self):
        provider = TempMailoProvider()
        result = provider.get_new_email()
        email = result["email"]
        assert "@" in email

    def test_check_inbox_returns_dict(self):
        provider = TempMailoProvider()
        result = provider.check_inbox("test@example.com")
        assert isinstance(result, (dict, list))

    def test_read_message_returns_dict(self):
        provider = TempMailoProvider()
        result = provider.read_message("test@example.com", "123")
        assert isinstance(result, dict)


class TestMailTMProvider:
    def test_get_new_email_returns_dict(self):
        provider = MailTMProvider()
        result = provider.get_new_email()
        assert isinstance(result, dict)
        assert "email" in result

    def test_get_new_email_format(self):
        provider = MailTMProvider()
        result = provider.get_new_email()
        email = result["email"]
        assert "@" in email
        assert "." in email

    def test_check_inbox_returns_dict(self):
        provider = MailTMProvider()
        result = provider.check_inbox("test@mail.tm")
        assert isinstance(result, dict)
        assert "hydra:member" in result

    def test_random_str_length(self):
        provider = MailTMProvider()
        s = provider._random_str(10)
        assert len(s) == 10


class TestTempMailPlusProvider:
    def test_get_new_email_returns_dict(self):
        provider = TempMailPlusProvider()
        result = provider.get_new_email()
        assert isinstance(result, dict)
        assert "email" in result

    def test_get_new_email_format(self):
        provider = TempMailPlusProvider()
        result = provider.get_new_email()
        email = result["email"]
        assert "@" in email

    def test_validate_email_valid(self):
        provider = TempMailPlusProvider()
        assert provider._validate_email("test@example.com") is True
        assert provider._validate_email("user.name@domain.co.uk") is True

    def test_validate_email_invalid(self):
        provider = TempMailPlusProvider()
        assert provider._validate_email("invalid") is False
        assert provider._validate_email("no@domain") is False

    def test_check_inbox_returns_dict(self):
        provider = TempMailPlusProvider()
        result = provider.check_inbox("test@ merepost.com")
        assert isinstance(result, dict)


class TestIntegration:
    def test_providers_dict_not_empty(self):
        from server import PROVIDERS
        assert len(PROVIDERS) == 3
        assert "tempmailo" in PROVIDERS
        assert "mailtm" in PROVIDERS
        assert "tempmailplus" in PROVIDERS

    def test_all_providers_have_required_methods(self):
        from server import PROVIDERS
        for name, provider in PROVIDERS.items():
            assert hasattr(provider, 'get_new_email')
            assert hasattr(provider, 'check_inbox')
            assert hasattr(provider, 'read_message')
            result = provider.get_new_email()
            assert isinstance(result, dict)
            assert "email" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
