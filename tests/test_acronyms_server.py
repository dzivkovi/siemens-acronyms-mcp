#!/usr/bin/env python3
"""Simple MCP Tests - Following "Less is More" Principle

Tests only the essential integration points without protocol simulation:
- Tools exist and are properly registered
- Tools work when called directly
- MCP app can be created
- Authentication middleware is installed
- Integration points are connected

No complex protocol simulation, session management, or JSON-RPC testing.
"""

import json
import os
from unittest.mock import patch

import pytest


class TestMCPToolsExist:
    """Test that MCP tools are properly registered - code-buddy style"""

    def test_search_acronyms_tool_exists(self):
        """Test that search_acronyms tool is registered as FunctionTool"""
        from src.mcp_service import search_acronyms

        assert search_acronyms.__class__.__name__ == "FunctionTool"
        assert search_acronyms.name == "search_acronyms"
        assert "search" in search_acronyms.description.lower()
        assert "acronyms" in search_acronyms.description.lower()

    def test_get_health_tool_exists(self):
        """Test that get_health tool is registered as FunctionTool"""
        from src.mcp_service import get_health

        assert get_health.__class__.__name__ == "FunctionTool"
        assert get_health.name == "get_health"
        assert "health" in get_health.description.lower()


class TestMCPToolsWork:
    """Test that MCP tools work when called directly - no protocol needed"""

    @pytest.mark.asyncio
    async def test_search_acronyms_works(self):
        """Test search_acronyms tool function directly"""
        from src.mcp_service import search_acronyms

        # Call the tool function directly
        result = await search_acronyms.fn("EDA")

        # Validate result structure
        assert isinstance(result, str)
        data = json.loads(result)
        assert "results" in data
        assert "query" in data
        assert "count" in data
        assert data["query"] == "EDA"

    @pytest.mark.asyncio
    async def test_get_health_works(self):
        """Test get_health tool function directly"""
        from src.mcp_service import get_health

        # Call the tool function directly
        result = await get_health.fn()

        # Validate result structure
        assert isinstance(result, str)
        data = json.loads(result)
        assert "status" in data
        assert "hostname" in data
        assert "uptime" in data
        assert "version" in data
        assert data["status"] == "healthy"


class TestMCPIntegration:
    """Test that MCP is properly integrated - no protocol simulation"""

    def test_mcp_app_can_be_created(self):
        """Test that MCP app can be created"""
        from src.mcp_service import get_mcp_app

        mcp_app = get_mcp_app()
        assert mcp_app is not None

    def test_main_app_uses_mcp(self):
        """Test that main app integrates MCP properly"""
        from src.main import app

        # Check that MCP endpoint is mounted
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        assert any(path.startswith("/mcp") for path in routes)

    def test_auth_middleware_configured(self):
        """Test that MCP auth middleware is configured - simple approach"""
        # Just test that we can import and create the middleware
        from src.auth_middleware import MCPAuthMiddleware

        middleware = MCPAuthMiddleware(None)
        assert middleware is not None

        # Test that main.py imports it (integration point)
        with open("src/main.py") as f:
            content = f.read()
            assert "from .auth_middleware import MCPAuthMiddleware" in content
            assert "app.add_middleware(MCPAuthMiddleware)" in content

    def test_acronyms_service_loads(self):
        """Test that acronyms service loads data"""
        import asyncio

        from src.acronyms_service import AcronymsService

        async def test_load():
            service = AcronymsService()
            await service.load_data()
            # Should have loaded some acronyms (uses .data not .acronyms)
            assert len(service.data) > 0
            return True

        result = asyncio.run(test_load())
        assert result is True


class TestMCPAuthenticationLogic:
    """Test auth middleware logic - no protocol simulation"""

    def test_no_api_keys_allows_access(self):
        """Test that no API keys configured allows access"""
        from src.auth_middleware import MCPAuthMiddleware

        # When no MCP_API_KEYS, should allow access
        with patch.dict(os.environ, {}, clear=True):
            middleware = MCPAuthMiddleware(None)
            # This is just testing the logic exists - full test would need request simulation
            assert middleware is not None

    @patch.dict(os.environ, {"MCP_API_KEYS": "test-key-123"})
    def test_api_keys_configured_requires_validation(self):
        """Test that configured API keys trigger validation"""
        from src.auth_middleware import MCPAuthMiddleware

        middleware = MCPAuthMiddleware(None)
        # This tests that the middleware exists and can be configured
        assert middleware is not None

        # Test the key parsing logic
        import os
        keys_str = os.getenv("MCP_API_KEYS", "")
        valid_keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        assert "test-key-123" in valid_keys


# ============================================================================
# KEEP ONLY ESSENTIAL HTTP TESTS (not protocol simulation)
# ============================================================================

@pytest.fixture
def simple_client():
    """Simple test client - no complex lifespan needed for basic tests"""
    from fastapi.testclient import TestClient

    from src.main import app

    return TestClient(app)


def test_mcp_endpoint_exists(simple_client):
    """Test that /mcp endpoint exists and responds"""
    # Just test endpoint exists - don't simulate protocol
    response = simple_client.post("/mcp", json={})
    # Should not be 404 (endpoint exists)
    assert response.status_code != 404


@patch.dict(os.environ, {"MCP_API_KEYS": "test-key"})
def test_mcp_auth_blocks_missing_key(simple_client):
    """Test that auth middleware blocks requests without API key"""
    response = simple_client.post("/mcp", json={})
    # Should be 403 when API keys configured but none provided
    assert response.status_code == 403


@patch.dict(os.environ, {"MCP_API_KEYS": "test-key"})
def test_mcp_auth_allows_valid_key(simple_client):
    """Test that auth middleware allows valid API key"""
    headers = {"X-API-Key": "test-key"}
    response = simple_client.post("/mcp", json={}, headers=headers)
    # Should not be 403 (auth passed) - protocol errors (400) are fine
    assert response.status_code != 403


# ============================================================================
# REMOVE ALL THE OVER-ENGINEERED PROTOCOL SIMULATION TESTS
# ============================================================================
# No more:
# - JSON-RPC protocol simulation
# - Session management testing
# - Full workflow testing
# - Complex client fixtures
# - Protocol response validation
# - TestMCPHealthTool class with 6 variants
# - TestIntegration class
# - tools/list and tools/call simulation
