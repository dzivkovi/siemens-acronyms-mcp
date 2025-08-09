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
from fastapi.responses import JSONResponse
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


@app.get("/.well-known/oauth-protected-resource")
async def oauth_protected_resource():
    """OAuth discovery endpoint - tells clients we use API key auth, not OAuth."""
    # Return empty to indicate we don't use OAuth
    # Claude Code will fall back to using the header authentication
    return JSONResponse({
        "resource_server": "http://localhost:8000",
        "authorization_servers": [],  # Empty = no OAuth, use headers instead
        "bearer_token_required": False
    })


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
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    # Handle MCP protocol methods
    if method == "initialize":
        # MCP initialization handshake
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "0.1.0",
                    "capabilities": {
                        "tools": {},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "siemens-acronyms",
                        "version": APP_VERSION
                    }
                },
                "id": request_id,
            }
        )
    
    elif method == "initialized":
        # Client notification that initialization is complete
        return JSONResponse({"jsonrpc": "2.0", "result": {}, "id": request_id})
    
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
                        }
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

    elif method == "ping":
        # Health check for MCP
        return JSONResponse({"jsonrpc": "2.0", "result": {}, "id": request_id})

    # Method not found
    return JSONResponse(
        {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Method not found: {method}"}, "id": request_id}
    )
