# MCP Integration Guide: Add AI Assistant Access to Your REST API

## Quick Start: One-Shot Design Document

For a comprehensive, single-pass implementation guide, see [docs/MCP_DESIGN.md](docs/MCP_DESIGN.md). This document provides everything needed to add MCP to any FastAPI application in one go.

### Using with GitHub Issues Workflow

If you're following our "GitHub Issues + /issue + /work cloud commands" development workflow:

1. **Copy the design to your analysis folder:**
   ```bash
   mkdir -p analysis/0000
   cp docs/MCP_DESIGN.md analysis/0000/DESIGN.md
   ```

2. **Create the GitHub issue:**
   ```
   /issue "Add MCP Server (HTTP transport) to existing FastAPI application"
   ```

3. **Start implementation:**
   ```
   /work 1  # or the issue number created
   ```

The design document will guide you through:
- Adding MCP endpoint at `/mcp`
- Implementing HTTP transport within the same application
- Setting up API key authentication
- Auto-discovering `/health` and business routes
- Complete testing and client configuration

## What We Built

We added MCP (Model Context Protocol) support to an existing FastAPI REST API, enabling it to work with AI assistants like Claude Code and VS Code Copilot. This guide shows the exact patterns we used from our implementation.

## The Architecture Pattern

```
Your Service (single deployment)
├── /api/v1/search     → Public REST endpoint (no auth)
├── /health            → Health check endpoint  
└── /mcp               → MCP protocol endpoint (API key auth)
    ├── tools/list     → Discovery: what tools are available
    └── tools/call     → Execution: run the tools
```

## Core Implementation Pattern

### 1. The MCP Endpoint Handler

We added one endpoint that handles all MCP protocol methods (`src/main.py:206-307`):

```python
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Handle MCP protocol requests."""
    # Handle body reading if middleware already consumed it
    if hasattr(request, '_body'):
        body = json.loads(request._body)
    else:
        body = await request.json()
    
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")
    
    # Protocol handshake
    if method == "initialize":
        requested_version = params.get("protocolVersion", "2025-06-18")
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": requested_version,  # Echo client's version
                "capabilities": {"tools": {}, "resources": {}},
                "serverInfo": {
                    "name": "siemens-acronyms",
                    "version": APP_VERSION
                }
            },
            "id": request_id
        })
    
    # Handle notifications (may not have ID)
    elif method == "initialized":
        if request_id is not None:
            return JSONResponse({"jsonrpc": "2.0", "result": {}, "id": request_id})
        else:
            return JSONResponse({})
    
    # Tool discovery
    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {"tools": [...]},  # Your tools here
            "id": request_id
        })
    
    # Tool execution
    elif method == "tools/call":
        tool_name = params.get("name")
        # Route to appropriate tool handler
```

### 2. Authentication Pattern: Protected MCP, Public REST

We protect only the MCP endpoint while keeping REST public (`src/main.py:172-202`):

```python
@app.middleware("http")
async def mcp_auth_middleware(request: Request, call_next):
    """Add authentication to MCP endpoints only."""
    if request.url.path.startswith("/mcp"):
        # Special case: get_health tool bypasses auth
        try:
            body = await request.body()
            request._body = body  # Store for later use
            body_json = json.loads(body) if body else {}
            method = body_json.get("method")
            
            if method == "tools/call":
                tool_name = body_json.get("params", {}).get("name")
                if tool_name == "get_health":
                    # Skip auth for public tools
                    response = await call_next(request)
                    return response
        except Exception:
            pass
        
        # Check API key for other requests
        api_key = request.headers.get("X-API-Key")
        allowed_keys = os.getenv("GLOSSARY_API_KEYS", "").split(",")
        allowed_keys = [key.strip() for key in allowed_keys if key.strip()]
        
        if api_key not in allowed_keys:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid or missing API key"}
            )
    
    return await call_next(request)
```

### 3. Tool Definition Pattern

We define tools with FastMCP decorators and expose them via tools/list (`src/main.py:72-101`):

```python
# Tool with parameters (requires auth)
@mcp.tool()
async def search_acronyms(query: str) -> str:
    """Search for Siemens acronyms and terminology."""
    results = await acronyms_service.search(query)
    return json.dumps({"results": results, "query": query, "count": len(results)})

# Tool without parameters (public access)
@mcp.tool()
async def get_health() -> str:
    """Get server health status including uptime and hostname."""
    health_data = {
        "status": "healthy",
        "hostname": socket.gethostname(),
        "uptime": time.time() - APP_START_TIME,
        "version": APP_VERSION
    }
    return json.dumps(health_data)
```

### 4. Tool Discovery Response

In tools/list handler (`src/main.py:227-257`):

```python
"tools": [
    {
        "name": "search_acronyms",
        "description": "Search for Siemens acronyms and terminology",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The term or acronym to search for"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_health",
        "description": "Get server health status including uptime and hostname",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []  # No parameters required
        }
    }
]
```

### 5. Tool Execution Pattern

In tools/call handler (`src/main.py:259-299`):

```python
elif method == "tools/call":
    tool_name = params.get("name")
    
    if tool_name == "search_acronyms":
        query = params.get("arguments", {}).get("query", "")
        results = await acronyms_service.search(query)
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {
                "content": [{
                    "type": "text",
                    "text": json.dumps({"results": results, "query": query, "count": len(results)})
                }]
            },
            "id": request_id
        })
    
    elif tool_name == "get_health":
        health_data = {
            "status": "healthy",
            "hostname": socket.gethostname(),
            "uptime": time.time() - APP_START_TIME,
            "version": APP_VERSION
        }
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {
                "content": [{
                    "type": "text",
                    "text": json.dumps(health_data)
                }]
            },
            "id": request_id
        })
```

## Key Implementation Lessons

### 1. Protocol Version Negotiation
**Issue**: Clients send different protocol versions.
**Solution**: Always echo back the client's requested version, don't hardcode.

### 2. Request Body Consumption
**Issue**: Middleware reading request body prevents endpoint from reading it.
**Solution**: Store body in request object after reading in middleware.

### 3. Mixed Authentication
**Issue**: Some tools should be public, others protected.
**Solution**: Check tool name in middleware and selectively bypass auth.

### 4. Notification Handling
**Issue**: MCP sends notifications that may not have request IDs.
**Solution**: Check if ID exists before including in response.

## Testing Patterns We Used

### Test Structure (`tests/test_acronyms_server.py`)

```python
class TestMCPHealthTool:
    """Tests for MCP health check tool"""
    
    def test_mcp_health_without_auth(self):
        """Test that get_health tool works without API key"""
        client = TestClient(app)
        response = client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "get_health", "arguments": {}},
                "id": 1
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
    @patch.dict(os.environ, {"GLOSSARY_API_KEYS": "sk-test-123"})
    def test_mcp_health_tool_in_list(self):
        """Test that get_health tool appears in tools/list"""
        # Test with authentication for protected endpoints
```

### Test Coverage Areas
- Tool discovery (tools appear in list)
- Authentication bypass for public tools
- Authentication required for protected tools
- Response format validation
- Uptime tracking accuracy
- Handling of extra parameters

## Client Configuration

### Claude Code CLI
```bash
# Add the server
claude mcp add siemens-acronyms http://localhost:8000/mcp \
  --header "X-API-Key: sk-team-A"

# Test it works
claude -p "Using siemens-acronyms MCP, check the server health"
```

### VS Code GitHub Copilot
Create `.vscode/mcp.json`:
```json
{
  "servers": {
    "siemens-acronyms": {
      "type": "http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "X-API-Key": "sk-team-A"
      }
    }
  }
}
```

### Claude Code Permissions
Add to `.claude/settings.json`:
```json
"permissions": {
  "allow": [
    "mcp__siemens-acronyms__search_acronyms",
    "mcp__siemens-acronyms__get_health"
  ]
}
```

## Environment Variables

```env
# API keys for MCP authentication (comma-separated)
GLOSSARY_API_KEYS=sk-team-A,sk-team-B,sk-team-C

# Optional configuration
LOG_LEVEL=INFO
GLOSSARY_FILE_PATH=siemens_acronyms.json
```

## What This Pattern Gives You

1. **Single deployment**: REST and MCP in one service
2. **Backward compatibility**: Existing REST clients continue working
3. **Selective authentication**: Mix public and protected tools
4. **Hot reload**: Data changes apply to both protocols
5. **AI assistant access**: Works with Claude, Copilot, and other MCP clients

## Files to Reference

- `src/main.py` - Complete implementation (lines 172-307 for MCP)
- `tests/test_acronyms_server.py` - Test patterns (lines 340-505)
- `.env.example` - Environment variable template
- `.vscode/mcp.json` - VS Code configuration
- `.claude/settings.json` - Claude permissions

## Tested With

✅ Claude Code CLI  
✅ VS Code GitHub Copilot  
✅ 37 passing tests  
✅ Both public and protected tools  
✅ Fuzzy search functionality  

This implementation adds ~130 lines to expose your REST API to AI assistants via MCP, maintaining full backward compatibility.