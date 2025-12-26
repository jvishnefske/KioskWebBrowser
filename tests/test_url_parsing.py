"""Tests for URL parsing logic used in the kiosk browsers."""

import pathlib
from urllib.parse import urlparse


def normalize_url(url, base_path=None):
    """
    Normalize a URL string to a proper URL format.

    This mirrors the logic used in qtwebwindow.py and window.py.

    Args:
        url: The URL string to normalize
        base_path: Optional base path for resolving relative file paths

    Returns:
        Normalized URL string with proper scheme
    """
    if not url:
        return None

    parsed = urlparse(url)
    if parsed.scheme:
        return url

    # Check if it's a file path
    if base_path:
        path = base_path / url
    else:
        path = pathlib.Path(url)

    if path.is_file():
        return f"file://{path.absolute()}"

    # Default to http scheme
    return f"http://{url}"


class TestUrlNormalization:
    """Test URL normalization logic."""

    def test_url_with_http_scheme_unchanged(self):
        """URLs with http scheme should be returned unchanged."""
        url = "http://example.com"
        result = normalize_url(url)
        assert result == url

    def test_url_with_https_scheme_unchanged(self):
        """URLs with https scheme should be returned unchanged."""
        url = "https://example.com"
        result = normalize_url(url)
        assert result == url

    def test_url_without_scheme_gets_http_prefix(self):
        """URLs without scheme should get http:// prepended."""
        url = "example.com"
        result = normalize_url(url)
        assert result == "http://example.com"

    def test_none_url_returns_none(self):
        """None URL should return None."""
        result = normalize_url(None)
        assert result is None

    def test_empty_url_returns_none(self):
        """Empty URL should return None."""
        result = normalize_url("")
        assert result is None

    def test_file_scheme_unchanged(self):
        """URLs with file scheme should be returned unchanged."""
        url = "file:///path/to/file.html"
        result = normalize_url(url)
        assert result == url

    def test_local_file_gets_file_scheme(self, tmp_path):
        """Existing local files should get file:// scheme."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<html></html>")

        result = normalize_url(str(test_file))
        assert result.startswith("file://")
        assert str(test_file.absolute()) in result


class TestUrlParsing:
    """Test URL parsing behavior from standard library."""

    def test_parse_http_url(self):
        """HTTP URLs should parse correctly."""
        parsed = urlparse("http://example.com/path")
        assert parsed.scheme == "http"
        assert parsed.netloc == "example.com"
        assert parsed.path == "/path"

    def test_parse_file_url(self):
        """File URLs should parse correctly."""
        parsed = urlparse("file:///home/user/file.html")
        assert parsed.scheme == "file"
        assert parsed.path == "/home/user/file.html"

    def test_parse_url_without_scheme(self):
        """URLs without scheme should have empty scheme."""
        parsed = urlparse("example.com")
        assert parsed.scheme == ""
