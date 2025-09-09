#!/usr/bin/env python3
"""Unit tests for HTTP 403 VS Code compatibility.

This validates the key architectural innovation: returning HTTP 403 (not 401)
to prevent VS Code OAuth discovery and popup dialogs.
"""
import os
from unittest.mock import patch

from fastapi.testclient import TestClient


class TestHTTP403Compatibility:
    """Test HTTP 403 behavior for VS Code compatibility"""

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key-123"})
    def test_mcp_returns_403_not_401(self):
        """Critical test: MCP endpoints return HTTP 403, not 401"""
        from src.main import app
        client = TestClient(app)

        # Test MCP endpoint without auth
        response = client.post("/mcp/messages", json={"method": "test"})

        # CRITICAL: Must be 403, not 401
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        assert response.status_code != 401, "401 triggers VS Code OAuth popups!"

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key-123"})
    def test_mcp_error_message_quality(self):
        """Test that 403 error messages are professional"""
        from src.main import app
        client = TestClient(app)

        response = client.post("/mcp/messages", json={"method": "test"})
        assert response.status_code == 403

        error_data = response.json()
        error_msg = error_data.get("error", "")

        # Should have clear error message for developers
        assert "api key" in error_msg.lower()

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key-123"})
    def test_no_oauth_discovery_headers(self):
        """Test that we don't return headers that trigger OAuth discovery"""
        from src.main import app
        client = TestClient(app)

        response = client.post("/mcp/messages", json={"method": "test"})

        # These headers would trigger OAuth discovery - make sure they're not present
        oauth_headers = ["WWW-Authenticate", "www-authenticate"]
        for header in oauth_headers:
            assert header not in response.headers, f"Found '{header}' header (triggers OAuth)"

    @patch.dict(os.environ, {"MCP_API_KEYS": "valid-key,another-key"})
    def test_valid_api_key_bypasses_403(self):
        """Test that valid API keys bypass the 403 response"""
        from src.main import app
        client = TestClient(app)

        headers = {"X-API-Key": "valid-key"}
        response = client.post("/mcp/messages", json={"method": "test"}, headers=headers)

        # Should not be 403 (auth passed)
        assert response.status_code != 403

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key"})
    def test_multiple_api_key_header_formats(self):
        """Test both X-API-Key and x-api-key header formats work"""
        from src.main import app
        client = TestClient(app)

        # Test uppercase header
        headers1 = {"X-API-Key": "test-key"}
        response1 = client.post("/mcp/messages", json={"method": "test"}, headers=headers1)

        # Test lowercase header
        headers2 = {"x-api-key": "test-key"}
        response2 = client.post("/mcp/messages", json={"method": "test"}, headers=headers2)

        # Both should bypass 403 auth
        assert response1.status_code != 403
        assert response2.status_code != 403

    def test_no_auth_configured_allows_access(self):
        """Test that when no MCP_API_KEYS are configured, access is allowed"""
        # Clear any existing keys
        with patch.dict(os.environ, {"MCP_API_KEYS": ""}, clear=True):
            from src.main import app
            client = TestClient(app)

            response = client.post("/mcp/messages", json={"method": "test"})

            # Should not be 403 when no auth is configured
            assert response.status_code != 403

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key"})
    def test_rest_endpoints_unaffected(self):
        """Test that REST endpoints are not affected by MCP authentication"""
        from src.main import app
        client = TestClient(app)

        # REST endpoints should work without auth
        response = client.get("/api/v1/search?q=test")
        assert response.status_code == 200

        response = client.get("/health")
        assert response.status_code == 200
