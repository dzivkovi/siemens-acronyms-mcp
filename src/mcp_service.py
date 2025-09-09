#!/usr/bin/env python3
"""
MCP Service - Minimal implementation using FastMCP 2.11.2 capabilities.
HTTP 403 authentication for VS Code compatibility.
"""

import json
import socket
import time
import logging
from fastmcp import FastMCP

from .acronyms_service import AcronymsService

logger = logging.getLogger(__name__)
APP_START_TIME = time.time()
APP_VERSION = "1.0.0"

# Create FastMCP instance - authentication handled by middleware
mcp = FastMCP(name="siemens-glossary")

# Initialize the acronyms service
acronyms_service = AcronymsService()


@mcp.tool()
async def search_acronyms(query: str) -> str:
    """
    Search for Siemens acronyms and terminology with fuzzy matching.

    Args:
        query: The term or acronym to search for

    Returns:
        JSON string with search results including similarity scores
    """
    try:
        results = await acronyms_service.search(query)
        response = {
            "results": results,
            "query": query,
            "count": len(results)
        }
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Search error in MCP tool: {e}")
        error_response = {
            "error": f"Search failed: {str(e)}",
            "query": query,
            "results": [],
            "count": 0
        }
        return json.dumps(error_response)


@mcp.tool()
async def get_health() -> str:
    """
    Get server health status including uptime, hostname, and version.

    Returns:
        JSON string with health status data
    """
    health_data = {
        "status": "healthy",
        "hostname": socket.gethostname(),
        "uptime": time.time() - APP_START_TIME,
        "version": APP_VERSION,
        "service": "siemens-acronyms-mcp"
    }
    return json.dumps(health_data)


def get_mcp_app():
    """
    Get FastMCP ASGI app using HTTP transport - actual code-buddy pattern.
    
    This uses the proven working HTTP transport from code-buddy, not SSE.
    FastMCP handles all HTTP JSON-RPC protocol details automatically.
    """
    return mcp.http_app(path="/")


async def initialize_mcp_service():
    """
    Initialize the MCP service by loading acronyms data.
    Call this during application startup.
    """
    logger.info("Initializing MCP service...")
    await acronyms_service.load_data()
    logger.info("MCP service initialized successfully")