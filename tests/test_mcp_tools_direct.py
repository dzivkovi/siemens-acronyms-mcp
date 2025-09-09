#!/usr/bin/env python3
"""
Unit tests for MCP tools direct function calls.

Tests the 2 MCP tools that wrap the API endpoints:
- search_acronyms tool (wraps /api/v1/search)
- get_health tool (wraps /health)
"""
import pytest
import os
import json


class TestMCPToolsDirect:
    """Test MCP tools directly without HTTP protocol complexity"""

    def setup_method(self):
        """Set up test environment"""
        os.environ["MCP_API_KEYS"] = "test-direct"

    @pytest.mark.asyncio
    async def test_search_acronyms_tool(self):
        """Test search_acronyms MCP tool directly"""
        from src.mcp_service import search_acronyms
        
        # Test with valid query - access the function from the FunctionTool
        result = await search_acronyms.fn("EDA")
        
        # Validate result is JSON string
        assert isinstance(result, str)
        data = json.loads(result)
        
        # Validate structure
        assert "results" in data
        assert "query" in data
        assert "count" in data
        assert data["query"] == "EDA"
        assert isinstance(data["results"], list)
        assert isinstance(data["count"], int)

    @pytest.mark.asyncio
    async def test_search_acronyms_empty_query(self):
        """Test search_acronyms with empty query"""
        from src.mcp_service import search_acronyms
        
        result = await search_acronyms.fn("")
        data = json.loads(result)
        
        assert data["query"] == ""
        assert data["count"] == 0
        assert data["results"] == []

    @pytest.mark.asyncio
    async def test_get_health_tool(self):
        """Test get_health MCP tool directly"""
        from src.mcp_service import get_health
        
        result = await get_health.fn()
        
        # Validate result is JSON string
        assert isinstance(result, str)
        data = json.loads(result)
        
        # Validate health structure
        assert "status" in data
        assert "hostname" in data
        assert "uptime" in data
        assert "version" in data
        assert "service" in data
        
        assert data["status"] == "healthy"
        assert isinstance(data["uptime"], (int, float))
        assert data["service"] == "siemens-acronyms-mcp"

    @pytest.mark.asyncio
    async def test_search_acronyms_error_handling(self):
        """Test search_acronyms error handling"""
        from src.mcp_service import search_acronyms
        
        # Should not raise exceptions, should return error in JSON
        result = await search_acronyms.fn("test-query")
        data = json.loads(result)
        
        # Should always have these fields even on error
        assert "query" in data
        assert "count" in data
        assert "results" in data