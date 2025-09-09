#!/usr/bin/env python3
"""Proven MCP authentication middleware from code-buddy project.
Returns HTTP 403 (not 401) to avoid VS Code OAuth popups.
"""

import logging
import os

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MCPAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate API keys for MCP endpoints.
    Returns 403 Forbidden (not 401) to avoid triggering VS Code OAuth popups.

    IMPORTANT: This is a deliberate architectural decision, not a mistake.
    VS Code's MCP client interprets HTTP 401 as requiring OAuth2/OpenID Connect,
    which triggers unwanted authentication popups. By returning 403 instead,
    we properly deny access without triggering VS Code's OAuth discovery.
    """

    async def dispatch(self, request: Request, call_next):
        # Only check MCP routes
        if request.url.path.startswith("/mcp"):
            # Get valid API keys from environment
            valid_keys_str = os.getenv("MCP_API_KEYS", "")

            # If no keys configured, allow access (backward compatibility)
            if not valid_keys_str:
                logger.debug("No MCP_API_KEYS configured - allowing MCP access")
                return await call_next(request)

            # Parse valid keys
            valid_keys = [k.strip() for k in valid_keys_str.split(",") if k.strip()]

            # Get API key from header
            api_key = request.headers.get("X-API-Key") or request.headers.get("x-api-key")

            # Check if key is valid
            if not api_key:
                logger.warning(f"MCP request to {request.url.path} missing API key")
                # CRITICAL: Return 403 (not 401) to avoid VS Code OAuth popup
                return JSONResponse(
                    status_code=403,  # <-- Intentionally NOT 401
                    content={"error": "API key required for MCP access"},
                )

            if api_key not in valid_keys:
                logger.warning(f"Invalid MCP API key attempted: {api_key[:6]}...")
                # CRITICAL: Return 403 (not 401) - see comment above
                return JSONResponse(
                    status_code=403,  # <-- Intentionally NOT 401
                    content={"error": "Invalid API key"},
                )

            # Valid key - allow request
            logger.debug(f"Valid MCP API key accepted: {api_key[:6]}...")

        return await call_next(request)
