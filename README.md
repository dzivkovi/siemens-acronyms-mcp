# Siemens Acronyms MCP Server

A glossary service exposing Siemens-specific terminology via REST API and MCP (Model Context Protocol) endpoints. This demonstrates how to add MCP capabilities to existing internal APIs, making institutional knowledge accessible to AI assistants and development tools.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd siemens-acronyms-mcp
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   # Comma-separated list of API keys for MCP endpoint authentication
   GLOSSARY_API_KEYS=sk-team-A,sk-team-B,sk-Daniel
   
   # Optional: Custom path to acronyms file
   # GLOSSARY_FILE_PATH=siemens_acronyms.json
   
   # Optional: Log level (DEBUG, INFO, WARNING, ERROR)
   LOG_LEVEL=INFO
   ```

4. **Run the server**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   The server will be available at http://localhost:8000

## 📡 API Endpoints

### 1. REST API (Public Access)

**Search Endpoint:** `GET /api/v1/search?q={query}`

No authentication required. Returns acronym definitions with fuzzy matching.

```bash
# Search for an exact acronym
curl "http://localhost:8000/api/v1/search?q=EDA"

# Fuzzy search handles typos
curl "http://localhost:8000/api/v1/search?q=Temcenter"
# Returns: Teamcenter (with similarity score)

# Partial matches
curl "http://localhost:8000/api/v1/search?q=Sim"
# Returns: Simcenter and related terms
```

**Response format:**
```json
{
  "results": [
    {
      "term": "EDA",
      "full_name": "Electronic Design Automation",
      "description": "IC design, PCB design, and electronic systems design tools",
      "score": 100.0
    }
  ],
  "query": "EDA",
  "count": 1
}
```

### 2. MCP Endpoint (Protected)

**Endpoint:** `POST /mcp`

Requires `X-API-Key` header with valid API key from `GLOSSARY_API_KEYS`.

```bash
# List available tools
curl -X POST http://localhost:8000/mcp \
  -H "X-API-Key: sk-team-A" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

# Search using MCP protocol
curl -X POST http://localhost:8000/mcp \
  -H "X-API-Key: sk-team-A" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_acronyms",
      "arguments": {"query": "DISW"}
    },
    "id": 2
  }'
```

### 3. Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8000/health
```

Returns:
```json
{
  "status": "healthy",
  "hostname": "your-hostname",
  "uptime": 123.45,
  "version": "1.0.0"
}
```

### 4. API Documentation

Interactive Swagger UI available at: http://localhost:8000/docs

## 🤖 Connecting AI Assistants via MCP

### Claude Code Integration

After starting the server, you can connect Claude Code to use the acronyms service:

1. **Add the MCP Server**
   ```bash
   # Add the MCP server with HTTP transport and API key
   claude mcp add --transport http siemens-acronyms http://localhost:8000/mcp \
     --header "X-API-Key: sk-team-A"
   
   # Verify connection status (should show ✓ Connected)
   claude mcp list
   ```

2. **Option 2: Manual Configuration in `.mcp.json`**
   
   Create or edit `.mcp.json` in your project directory (for local scope) or use `claude mcp add --scope project` for team sharing:
   ```json
   {
     "mcpServers": {
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
   
   Or with environment variable expansion:
   ```json
   {
     "mcpServers": {
       "siemens-acronyms": {
         "type": "http",
         "url": "http://localhost:8000/mcp",
         "headers": {
           "X-API-Key": "${GLOSSARY_API_KEY:-sk-team-A}"
         }
       }
     }
   }
   ```

3. **Verify Configuration**
   ```bash
   # List configured MCP servers
   claude mcp list
   
   # Get details of the siemens-acronyms server
   claude mcp get siemens-acronyms
   ```

4. **Interactive Usage in Claude Code**
   
   After configuration, in Claude Code you can ask:
   - "What does DISW mean in Siemens context?"
   - "Search for EDA in the Siemens glossary"
   - "Find information about Teamcenter"
   - "Use the siemens-acronyms MCP server to search for TeamCenter"

5. **Non-Interactive Usage (Command Line)**
   
   Use the `-p` flag for non-interactive queries, perfect for scripts and automation:
   
   ```bash
   # Basic search
   claude -p "Using the siemens-acronyms MCP server, what does DISW mean?"
   
   # Test fuzzy matching (handles typos)
   claude -p "Using the siemens-acronyms MCP server, search for 'Temcenter'"
   # Returns: Teamcenter with 94.74% match score
   
   # Search by partial terms
   claude -p "Using the siemens-acronyms MCP server, search for 'software'"
   # Returns: DISW and other software-related acronyms
   
   # With permission bypass for automation
   claude -p --dangerously-skip-permissions \
     "Using the siemens-acronyms MCP server, what does EDA stand for?"
   ```
   
   **Note**: Claude Code will request permission to use MCP tools on first use. Either:
   - Grant permission interactively when prompted
   - Use `--dangerously-skip-permissions` flag for scripts (use cautiously)
   - Configure allowed tools in `.claude/settings.json`

### VS Code MCP Extension

If using VS Code with MCP extension, create `.vscode/mcp.json`:

```json
{
  "servers": {
    "siemens-acronyms": {
      "transport": "http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "X-API-Key": "sk-team-A"
      }
    }
  }
}
```

### Testing MCP Connection

You can test the MCP connection directly:

```python
# test_mcp_connection.py
import httpx
import asyncio
import json

async def test_mcp():
    async with httpx.AsyncClient() as client:
        # Test tools/list
        response = await client.post(
            "http://localhost:8000/mcp",
            headers={"X-API-Key": "sk-team-A"},
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1
            }
        )
        print("Tools available:", response.json())
        
        # Test search
        response = await client.post(
            "http://localhost:8000/mcp",
            headers={"X-API-Key": "sk-team-A"},
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "search_acronyms",
                    "arguments": {"query": "EDA"}
                },
                "id": 2
            }
        )
        result = response.json()
        if "result" in result:
            content = json.loads(result["result"]["content"][0]["text"])
            print("Search results:", content)

asyncio.run(test_mcp())
```

## 🔍 Real-World Usage Examples

Based on practical testing with Claude Code, here are actual results:

### Fuzzy Matching in Action
```bash
# Typo in "Teamcenter" → Still finds the right result
$ claude -p --dangerously-skip-permissions \
    "Using siemens-acronyms MCP, search for 'Temcenter'"
> Found "Teamcenter" with 94.74% confidence score

# Partial word matching
$ claude -p --dangerously-skip-permissions \
    "Using siemens-acronyms MCP, search for 'software'"
> Found DISW (Digital Industries Software) with 84% match
```

### Understanding MCP Communication
Each Claude Code query triggers multiple MCP calls:
1. `initialize` - Protocol handshake
2. `tools/list` - Discover available tools
3. `tools/call` - Execute the search
4. Server logs show all requests with 200 OK status

### Performance Observations
- Response time: <50ms for typical queries
- Connection overhead: ~100ms for initial handshake
- Fuzzy matching adds negligible latency (<10ms)

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest -v --cov=src

# Run specific test categories
pytest -v tests/test_acronyms_server.py::TestRESTEndpoint
pytest -v tests/test_acronyms_server.py::TestMCPEndpoint
```

Current test coverage: **83%** with 31 tests passing.

## 🔧 Development

### Project Structure
```
siemens-acronyms-mcp/
├── src/
│   ├── main.py              # FastAPI application
│   └── acronyms_service.py  # Core search service
├── tests/
│   └── test_acronyms_server.py  # Test suite
├── siemens_acronyms.json    # Glossary data (hot-reloadable)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md              # This file
```

### Adding New Acronyms

Edit `siemens_acronyms.json`:

```json
{
  "acronyms": [
    {
      "term": "NEW_TERM",
      "full_name": "Full Name of Term",
      "category": "Acronym",
      "description": "Description of what this term means",
      "division": "DISW",
      "url": "https://optional-url.com",
      "related": ["RELATED1", "RELATED2"]
    }
  ]
}
```

The service automatically reloads the file without restart.

### Code Quality

Before committing:

```bash
# Format code
ruff format .

# Check linting
ruff check . --fix

# Run tests
pytest -v
```

## 🚦 Deployment

### Production Deployment

1. **Using Uvicorn directly**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Using Gunicorn with Uvicorn workers**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Docker deployment**
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GLOSSARY_API_KEYS` | Comma-separated API keys for MCP auth | - | Yes (for MCP) |
| `GLOSSARY_FILE_PATH` | Path to acronyms JSON file | `siemens_acronyms.json` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

## 📊 Performance

- **Search response time**: <100ms for 1000+ terms
- **Concurrent requests**: Handles 50+ simultaneous connections
- **Memory usage**: ~50MB with 1000 terms loaded
- **Hot reload**: File changes detected within 1 second

## 🤝 Contributing

1. Check existing issues or create new ones
2. Follow TDD approach - write tests first
3. Ensure all tests pass and code is formatted
4. Update `siemens_acronyms.json` for new terms
5. Create pull request with clear description

## 📄 License

- **Code**: MIT License - Use freely in your projects
- **Glossary Data** (`siemens_acronyms.json`): CC BY 4.0 - Share and adapt with attribution

This dual licensing allows both internal Siemens use and external contributions.

## 🆘 Troubleshooting

### Server won't start
- Check Python version: `python --version` (needs 3.10+)
- Verify all dependencies: `pip install -r requirements.txt`
- Check port availability: `lsof -i :8000`

### MCP endpoint returns 401
- Verify API key in `.env` file
- Check `X-API-Key` header in request
- Ensure no spaces in `GLOSSARY_API_KEYS` value

### Search returns no results
- Check `siemens_acronyms.json` file exists and is valid JSON
- Verify file permissions allow reading
- Check logs for file loading errors

### Claude Code can't connect
- Ensure server is running: `curl http://localhost:8000/health`
- Verify API key matches between server and client config
- Check firewall/network settings allow localhost connections
- Protocol version issue: Claude Code uses `"2025-06-18"` protocol version
  - The server automatically echoes back the client's requested version
  - If you see connection success but tools don't work, restart Claude Code

## 📞 Support

For issues or questions:
1. Check the [Issues](https://github.com/your-repo/issues) page
2. Review test files for usage examples
3. Consult `CLAUDE.md` for AI assistant guidance

---

**Note**: This is a demonstration project showing how to MCP-enable internal glossaries and APIs. The patterns shown here can be applied to other internal services to make them accessible to AI assistants while maintaining security through API key authentication.