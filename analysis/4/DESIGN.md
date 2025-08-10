# Expose Health Check as MCP Tool for Service Discovery and Monitoring

## Problem / Metric
Currently, the health check endpoint (`/health`) is only accessible via REST API, not through the MCP protocol. This means AI assistants and MCP clients cannot programmatically check the server's status, hostname, or uptime without making direct HTTP calls outside the MCP protocol. This limits service discovery and monitoring capabilities for MCP-native clients.

**Metric**: Enable 100% of MCP clients to query server health status through the standard MCP tools interface without requiring additional HTTP client configuration.

## Goal
Expose the existing health check functionality as an MCP tool that can be discovered via `tools/list` and invoked via `tools/call`, providing the same information as the REST endpoint (status, hostname, uptime, version) but through the MCP protocol. The tool should be public (no authentication required) for both developers and LLMs to monitor service health.

## Scope (M/S/W)
- [M] Create new MCP tool `get_health` that returns health status
- [M] Tool returns: status, hostname, uptime, version (same as REST endpoint)
- [M] No authentication required for this tool (public access)
- [M] Tool appears in `tools/list` discovery
- [M] Tool callable via `tools/call` with no parameters
- [S] Add unit tests for the new MCP tool
- [S] Update documentation to reflect new tool availability
- [W] Remove or deprecate existing REST health endpoint
- [W] Add additional monitoring metrics beyond current fields
- [W] Implement health history or trend tracking

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 | MCP server is running | Client calls `tools/list` | Response includes `get_health` tool with proper schema |
| 2 | MCP client without API key | Calls `get_health` tool via MCP | Returns health data with 200 status (no auth required) |
| 3 | MCP client with valid API key | Calls `get_health` tool | Returns same health data (auth not checked for this tool) |
| 4 | Server has been running 5 minutes | `get_health` tool is called | Returns uptime ≈ 300 seconds |
| 5 | Server is on host "prod-server-01" | `get_health` tool is called | Returns hostname: "prod-server-01" |
| 6 | MCP tool call with extra params | `get_health` called with unexpected args | Ignores extra params, returns health data |
| 7 | Claude Code or VS Code | Uses MCP to check server health | Successfully receives health status via MCP protocol |

## Technical Design

### Architecture Changes
```
Current State:
- REST: GET /health → HealthResponse
- MCP: Only search_acronyms tool available

Proposed State:
- REST: GET /health → HealthResponse (unchanged)
- MCP: Two tools available:
  1. search_acronyms (existing)
  2. get_health (new, public)
```

### Implementation Approach
1. **Add new MCP tool decorator** in `main.py`:
   ```python
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

2. **Update tools/list response** to include the new tool with no required parameters

3. **Modify authentication middleware** to explicitly allow `get_health` tool calls without API key validation:
   ```python
   # In tools/call handler
   if tool_name == "get_health":
       # No auth check - public tool
       result = await get_health()
   elif tool_name == "search_acronyms":
       # Existing auth flow for protected tools
       ...
   ```

### Tool Schema
```json
{
  "name": "get_health",
  "description": "Get server health status including uptime and hostname",
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

## Implementation Steps
1. **Add MCP tool function** (`src/main.py:72-85`)
   - Add `@mcp.tool()` decorated `get_health()` function after `search_acronyms`
   - Return JSON string with health data matching REST endpoint format

2. **Update tools/list handler** (`src/main.py:210-231`)
   - Add `get_health` tool definition to the tools array
   - Include empty inputSchema (no parameters required)

3. **Update tools/call handler** (`src/main.py:233-251`)
   - Add conditional branch for `tool_name == "get_health"`
   - Call `get_health()` function without auth check
   - Return result in standard MCP format

4. **Bypass authentication for health tool** (`src/main.py:156-168`)
   - Modify middleware to skip auth for `get_health` tool calls
   - Or handle within tools/call to avoid auth before tool execution

5. **Add tests** (`tests/test_acronyms_server.py`)
   - Test `get_health` appears in tools/list
   - Test calling without API key succeeds
   - Test response contains all required fields
   - Test uptime increases between calls

6. **Update documentation**
   - Add `get_health` tool to README.md MCP tools section
   - Update INTEGRATION_GUIDE.md with health check example

## Testing Strategy
1. **Unit Tests**:
   - `test_mcp_health_tool_in_list()` - Verify tool appears in discovery
   - `test_mcp_health_without_auth()` - Confirm no API key required
   - `test_mcp_health_response_fields()` - Validate all fields present
   - `test_mcp_health_uptime_increases()` - Check uptime calculation

2. **Integration Tests**:
   - Test with Claude Code CLI: `claude -p "Using siemens-acronyms MCP, check the server health"`
   - Test with VS Code MCP client
   - Verify tool works alongside existing `search_acronyms` tool

3. **Manual Testing**:
   ```bash
   # Direct MCP protocol test
   curl -X POST http://localhost:8000/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/call",
       "params": {"name": "get_health", "arguments": {}},
       "id": 1
     }'
   ```

## Risks & Considerations
- **Security**: Making health endpoint public via MCP could expose server details (hostname). This is acceptable for internal services but should be documented.
- **Backwards Compatibility**: Existing REST endpoint remains unchanged, no breaking changes.
- **Performance**: Health check is lightweight, no performance concerns.
- **Caching**: Consider if health data should be cached (probably not - want real-time data).
- **Error Handling**: If server is unhealthy, should tool return error or unhealthy status? (Return unhealthy status for monitoring tools to parse).
- **Tool Naming**: Using `get_health` to match REST endpoint pattern, could use `check_health` or `health_status` instead.
- **Authentication Bypass**: Need to ensure ONLY the health tool bypasses auth, not all tools.