"""
FastAPI application with dual REST/MCP endpoints for Siemens acronyms.
"""

import json
import logging
import os
import socket
import time
from contextlib import asynccontextmanager
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .acronyms_service import AcronymsService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Track application start time
APP_START_TIME = time.time()
APP_VERSION = "1.0.0"


class SearchResponse(BaseModel):
    """Response model for search endpoint."""

    results: list[dict[str, Any]] = Field(default_factory=list)
    query: str
    count: int


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    hostname: str
    uptime: float
    version: str


# Initialize service
acronyms_service = AcronymsService()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("Starting Siemens Acronyms Server...")
    await acronyms_service.load_data()
    yield
    # Shutdown
    logger.info("Shutting down Siemens Acronyms Server...")


# Create FastMCP instance for MCP integration
mcp = FastMCP(
    name="siemens-glossary",
)


@mcp.tool()
async def search_acronyms(query: str) -> str:
    """
    Search for Siemens acronyms and terminology.

    Args:
        query: The term or acronym to search for

    Returns:
        JSON string with search results
    """
    results = await acronyms_service.search(query)
    return json.dumps({"results": results, "query": query, "count": len(results)})


@mcp.tool()
async def get_health() -> str:
    """
    Get server health status including uptime and hostname.

    Returns:
        JSON string with health status data
    """
    health_data = {
        "status": "healthy",
        "hostname": socket.gethostname(),
        "uptime": time.time() - APP_START_TIME,
        "version": APP_VERSION,
    }
    return json.dumps(health_data)


# Create FastAPI app
app = FastAPI(
    title="Siemens Glossary of Acronyms API",
    description="REST and MCP endpoints for searching Siemens terminology",
    version=APP_VERSION,
    lifespan=app_lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# OAuth discovery endpoints removed - not needed for VS Code or Claude Code
# Both work fine with just the X-API-Key header authentication


@app.get("/")
async def redirect_to_docs(request: Request) -> RedirectResponse:
    """Redirect root URL to Swagger documentation."""
    # Preserve query parameters if present
    query_string = request.url.query
    redirect_url = "/docs"
    if query_string:
        redirect_url = f"/docs?{query_string}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        hostname=socket.gethostname(),
        uptime=time.time() - APP_START_TIME,
        version=APP_VERSION,
    )


@app.get("/api/v1/search", response_model=SearchResponse)
async def rest_search_acronyms(q: str = Query(..., min_length=1, description="Search query")) -> SearchResponse:
    """
    Search for acronyms with fuzzy matching.

    This is the public REST endpoint - no authentication required.
    """
    try:
        results = await acronyms_service.search(q)
        return SearchResponse(results=results, query=q, count=len(results))
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during search",
        ) from e


# API key validation middleware for MCP endpoint
async def validate_api_key(request: Request) -> Optional[str]:
    """Validate API key from X-API-Key header."""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return None

    # Get allowed keys from environment
    allowed_keys = os.getenv("GLOSSARY_API_KEYS", "").split(",")
    allowed_keys = [key.strip() for key in allowed_keys if key.strip()]

    if api_key in allowed_keys:
        return api_key
    return None


# Custom MCP middleware for authentication
@app.middleware("http")
async def mcp_auth_middleware(request: Request, call_next):
    """Add authentication to MCP endpoints only."""
    # Only apply auth to /mcp endpoints
    if request.url.path.startswith("/mcp"):
        # Check if this is a get_health tool call - if so, skip auth
        try:
            body = await request.body()
            request._body = body  # Store body for later use
            body_json = json.loads(body) if body else {}
            method = body_json.get("method")

            # Allow get_health tool calls without authentication
            if method == "tools/call":
                tool_name = body_json.get("params", {}).get("name")
                if tool_name == "get_health":
                    # Skip auth check for get_health
                    response = await call_next(request)
                    return response
        except Exception:
            pass  # If we can't parse the body, continue with normal auth

        api_key = await validate_api_key(request)
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid or missing API key"},
                headers={"WWW-Authenticate": "X-API-Key"},
            )
    response = await call_next(request)
    return response


# MCP endpoint handling
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Handle MCP protocol requests."""
    # Check if body was already read by middleware
    if hasattr(request, "_body"):
        body = json.loads(request._body)
    else:
        body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    # Handle MCP protocol methods
    if method == "initialize":
        # MCP initialization handshake
        # Use the protocol version requested by the client if supported
        requested_version = params.get("protocolVersion", "2025-06-18")
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": requested_version,  # Echo back the client's version
                    "capabilities": {"tools": {}, "resources": {}},
                    "serverInfo": {"name": "siemens-acronyms", "version": APP_VERSION},
                },
                "id": request_id,
            }
        )

    elif method == "initialized" or method == "notifications/initialized":
        # Client notification that initialization is complete
        # Notifications don't have IDs and don't require a response
        if request_id is not None:
            return JSONResponse({"jsonrpc": "2.0", "result": {}, "id": request_id})
        else:
            # For notifications, return empty response
            return JSONResponse({})

    elif method == "tools/list":
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "result": {
                    "tools": [
                        {
                            "name": "search_acronyms",
                            "description": "Search for Siemens acronyms and terminology",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "The term or acronym to search for"}
                                },
                                "required": ["query"],
                            },
                        },
                        {
                            "name": "get_health",
                            "description": "Get server health status including uptime and hostname",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": [],
                            },
                        },
                    ]
                },
                "id": request_id,
            }
        )

    elif method == "tools/call":
        tool_name = params.get("name")
        if tool_name == "search_acronyms":
            query = params.get("arguments", {}).get("query", "")
            results = await acronyms_service.search(query)
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({"results": results, "query": query, "count": len(results)}),
                            }
                        ]
                    },
                    "id": request_id,
                }
            )
        elif tool_name == "get_health":
            # get_health doesn't need any arguments
            health_data = {
                "status": "healthy",
                "hostname": socket.gethostname(),
                "uptime": time.time() - APP_START_TIME,
                "version": APP_VERSION,
            }
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(health_data),
                            }
                        ]
                    },
                    "id": request_id,
                }
            )

    elif method == "ping":
        # Health check for MCP
        return JSONResponse({"jsonrpc": "2.0", "result": {}, "id": request_id})

    # Method not found
    return JSONResponse(
        {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Method not found: {method}"}, "id": request_id}
    )
