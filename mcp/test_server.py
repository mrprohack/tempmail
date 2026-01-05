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


class TestDeleteEmail:
    def test_delete_email_tempmailo(self):
        from server import delete_email
        result = delete_email("test@example.com", "tempmailo")
        assert isinstance(result, dict)
        assert result.get("status") == "deleted"
        assert result.get("email") == "test@example.com"

    def test_delete_email_mailtm(self):
        from server import delete_email
        result = delete_email("test@mail.tm", "mailtm")
        assert isinstance(result, dict)
        assert result.get("status") == "deleted"

    def test_delete_email_tempmailplus(self):
        from server import delete_email
        result = delete_email("test@merepost.com", "tempmailplus")
        assert isinstance(result, dict)
        assert result.get("status") == "deleted"


class TestMarkAsRead:
    def test_mark_as_read_tempmailo(self):
        from server import mark_as_read
        result = mark_as_read("test@example.com", "123", "tempmailo")
        assert isinstance(result, dict)
        assert result.get("status") == "marked_read"
        assert result.get("message_id") == "123"

    def test_mark_as_read_mailtm(self):
        from server import mark_as_read
        result = mark_as_read("test@mail.tm", "456", "mailtm")
        assert isinstance(result, dict)
        assert result.get("status") == "marked_read"

    def test_mark_as_read_tempmailplus(self):
        from server import mark_as_read
        result = mark_as_read("test@merepost.com", "789", "tempmailplus")
        assert isinstance(result, dict)
        assert result.get("status") == "marked_read"


class TestSearchEmails:
    def test_search_emails_returns_dict(self):
        from server import search_emails
        result = search_emails("test@example.com", "example", "tempmailo")
        assert isinstance(result, dict)
        assert "query" in result
        assert "results" in result
        assert "count" in result

    def test_search_emails_with_results(self):
        from server import search_emails
        # Mock inbox data would be tested here
        result = search_emails("test@example.com", "test", "tempmailo")
        assert isinstance(result, dict)
        assert result["count"] >= 0
        assert isinstance(result["results"], list)


class TestFilterEmails:
    def test_filter_emails_returns_dict(self):
        from server import filter_emails
        result = filter_emails("test@example.com", "tempmailo")
        assert isinstance(result, dict)
        assert "filters" in result
        assert "results" in result
        assert "count" in result

    def test_filter_emails_with_read_filter(self):
        from server import filter_emails
        result = filter_emails("test@example.com", "tempmailo", read=False)
        assert isinstance(result, dict)
        assert result["filters"]["read"] is False

    def test_filter_emails_with_date_filters(self):
        from server import filter_emails
        result = filter_emails("test@example.com", "tempmailo", since="2024-01-01", until="2024-12-31")
        assert isinstance(result, dict)
        assert result["filters"]["since"] == "2024-01-01"
        assert result["filters"]["until"] == "2024-12-31"


class TestIntegration:
    def test_all_providers_work(self):
        from server import get_temp_email, check_inbox
        for provider in ["tempmailo", "mailtm", "tempmailplus"]:
            email = get_temp_email(provider)
            assert isinstance(email, dict)
            assert "email" in email
            inbox = check_inbox(email["email"], provider)
            assert isinstance(inbox, (dict, list))

    def test_new_tools_available(self):
        from server import (
            delete_email, mark_as_read, search_emails, filter_emails
        )
        # Test all new tools exist and return expected types
        assert callable(delete_email)
        assert callable(mark_as_read)
        assert callable(search_emails)
        assert callable(filter_emails)

        # Test return types
        assert isinstance(delete_email("test@example.com"), dict)
        assert isinstance(mark_as_read("test@example.com", "123"), dict)
        assert isinstance(search_emails("test@example.com", "test"), dict)
        assert isinstance(filter_emails("test@example.com"), dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
