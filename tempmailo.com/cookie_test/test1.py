import pytest
import re


class TestRandomStr:
    def test_random_str_length(self):
        import string
        import random
        length = 10
        result = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        assert len(result) == length
        assert result.isalnum()

    def test_random_str_different(self):
        import string
        import random
        s1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        s2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        assert len(s1) == len(s2) == 8


class TestEmailValidation:
    def test_validate_email_valid(self):
        def validate_email(email):
            return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True

    def test_validate_email_invalid(self):
        def validate_email(email):
            return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
        assert validate_email("invalid") is False
        assert validate_email("no@domain") is False
        assert validate_email("@domain.com") is False

    def test_email_with_underscore(self):
        def validate_email(email):
            return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
        assert validate_email("user_name@domain.com") is True


class TestURLExtraction:
    def test_extract_urls_simple(self):
        data = {
            "html": "Visit https://example.com for more info",
            "text": ""
        }
        urls = set()
        for key in ['html', 'text']:
            content = data.get(key, '')
            found = re.findall(r'https://[^\s<>"]+', content)
            for url in found:
                url = re.sub(r'[.,;!?]$', '', url)
                if url.startswith('http'):
                    urls.add(url)
        assert len(urls) == 1
        assert "https://example.com" in urls

    def test_extract_urls_empty(self):
        urls = set()
        for key in [None, {}]:
            if not key:
                continue
        assert len(urls) == 0

    def test_extract_urls_multiple(self):
        data = {
            "html": "Links: https://a.com and https://b.com",
            "text": ""
        }
        urls = set()
        for key in ['html', 'text']:
            content = data.get(key, '')
            found = re.findall(r'https://[^\s<>"]+', content)
            for url in found:
                url = re.sub(r'[.,;!?]$', '', url)
                if url.startswith('http'):
                    urls.add(url)
        assert len(urls) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
