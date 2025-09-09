"""FastAPI application with dual REST/MCP endpoints for Siemens acronyms.

This implementation demonstrates modern MCP best practices:
- Actually uses @mcp.tool() decorators (vs defining and ignoring them)
- HTTP 403 authentication for VS Code compatibility (no OAuth popups)
- Clean FastMCP integration without manual JSON-RPC handling
- API key management suitable for small teams without Azure AD overhead
"""

import logging
import os
import socket
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from .acronyms_service import AcronymsService
from .auth_middleware import MCPAuthMiddleware
from .mcp_service import get_mcp_app

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


# Initialize the acronyms service for REST API
acronyms_service = AcronymsService()

# Get MCP app
mcp_app = get_mcp_app()


@asynccontextmanager
async def combined_lifespan(app) -> AsyncGenerator[None, None]:
    """Combined lifespan for FastAPI and MCP"""
    # Start MCP lifespan
    async with mcp_app.lifespan(app):
        # Initialize acronyms service
        await acronyms_service.load_data()
        logger.info("Siemens Acronyms Server started")
        yield


# Create FastAPI app with combined lifespan
app = FastAPI(
    title="Siemens Glossary of Acronyms API",
    description="REST and MCP endpoints for searching Siemens terminology",
    version=APP_VERSION,
    lifespan=combined_lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add proven MCP authentication middleware (HTTP 403 for VS Code compatibility)
app.add_middleware(MCPAuthMiddleware)

# Mount MCP server
app.mount("/mcp", mcp_app)


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
    """Search for acronyms with fuzzy matching.

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


# MCP authentication is now handled natively by FastMCP's StaticTokenVerifier


# MCP endpoint is now handled by the mounted FastMCP app at /mcp
# All JSON-RPC protocol details are handled automatically by FastMCP
