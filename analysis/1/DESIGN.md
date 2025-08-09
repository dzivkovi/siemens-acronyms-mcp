# Siemens Glossary of Acronyms - Demo MCP Integration for Internal APIs

## Problem
Large enterprises grow through acquisitions, creating a maze of evolving terminology. At Siemens Digital Industries Software alone: EDA now means something different post-Mentor Graphics acquisition, TeamCenter became Teamcenter, and DISW emerged as the new division name. 

This confusion isn't just internal—clients, partners, and suppliers struggle with our terminology too. Everyone wastes time decoding acronyms that change meaning across divisions and eras. LLMs can't help—they don't know our language or recent rebrandings. Senior engineers become walking glossaries for both colleagues and customers.

This demo shows how to MCP-enable glossaries for everyone. By using open licenses (MIT for code, CC BY 4.0 for data), we create a shared vocabulary that benefits internal teams, external partners, and even AI assistants—making institutional knowledge accessible where people actually work.

## Goal
Create a demonstration MCP server that exposes Siemens acronyms data through both REST and MCP endpoints, proving that internal APIs can be MCP-enabled without external package deployment. Success = working demo that responds to "What does DISW mean?" via VS Code/Claude.

## Scope (M/S/W)
- [M] Single search endpoint serving both REST and MCP
- [M] API key authentication for MCP only
- [M] Fuzzy matching for typos using RapidFuzz
- [M] External JSON data file for easy updates
- [M] Health check with hostname and uptime
- [M] Swagger UI for REST API
- [M] File watching for auto-reload
- [S] VS Code configuration example
- [S] Test suite with pytest
- [W] Database storage
- [W] User management
- [W] Write operations

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 | REST endpoint at /api/v1/search | User queries "?q=EDA" without auth | Returns EDA definition with 200 status |
| 2 | MCP endpoint at /mcp | User sends MCP request without API key | Returns 401 Unauthorized |
| 3 | MCP endpoint with valid API key | User queries "DISW" via MCP | Returns Digital Industries Software info |
| 4 | User types "Temcenter" (typo) | Search is performed | Returns "Teamcenter" as top result |
| 5 | Acronyms JSON file is modified | Next search request arrives | Updated data is returned without restart |
| 6 | Health endpoint at /health | GET request is made | Returns status, hostname, uptime, version |
| 7 | Multiple API keys in env | Request with sk-team-A | Authentication succeeds |
| 8 | Search for "Sim" | Partial match requested | Returns Simcenter and related products |

## Technical Design

### Architecture
```
FastAPI Application
├── REST API (/api/v1/search) - Public
├── MCP Server (/mcp) - Protected
├── Health Check (/health) - Public
└── Swagger UI (/docs) - Public

Data Layer
├── siemens_acronyms.json - External file
├── AcronymsService - File watching + caching
└── RapidFuzz - Fuzzy matching engine
```

### Key Components
1. **FastMCP Integration**: Use `@mcp.tool` decorator to expose search function
2. **Authentication**: Environment variable `GLOSSARY_API_KEYS` with comma-separated keys
3. **Search Algorithm**: Exact match (100) → Fuzzy match (>80) → Partial match (>60)
4. **File Watching**: Check file mtime on each request, reload if changed

### Data Schema (Structured Loose)
```json
{
  "term": "required",
  "description": "required", 
  "category": "Product|Acronym|Technology|Process|Standard",
  "full_name": "optional",
  "url": "optional",
  "division": "optional",
  "related": ["optional"],
  "products": ["optional"],
  "formerly": "optional",
  "acquired": "optional",
  "metadata": { "flexible": "key-value" }
}
```

## Implementation Steps
1. **Project Setup**
   - Create project directory `siemens_acronyms_server`
   - Initialize with `requirements.txt`: fastapi, fastmcp, rapidfuzz, python-dotenv, uvicorn, pytest
   - Create `.env` file with `GLOSSARY_API_KEYS=sk-team-A,sk-team-B,sk-Daniel`

2. **Test Suite First (test_acronyms_server.py)**
   - Write all acceptance criteria as pytest tests
   - Include: exact match, fuzzy match, auth tests, health check tests
   - Run tests (all should fail initially)

3. **Data Model (siemens_acronyms.json)**
   - Create JSON file with sample Siemens terms
   - Include: EDA, DISW, Teamcenter, NX, Simcenter, Opcenter, Digital Twin

4. **Core Service (acronyms_service.py)**
   - Implement AcronymsService class with file watching
   - Add search method with RapidFuzz scoring
   - Handle file reload on mtime change

5. **FastAPI Application (main.py)**
   - Create FastAPI app with CORS and logging
   - Add health endpoint returning required fields
   - Add public REST endpoint at `/api/v1/search`

6. **MCP Integration**
   - Create FastMCP instance
   - Add `@mcp.tool` decorated search function
   - Mount MCP app at `/mcp` with auth middleware

7. **Authentication Middleware**
   - Read API keys from environment
   - Validate on MCP routes only
   - Return 401 for invalid keys

8. **VS Code Configuration**
   - Create `.vscode/mcp.json` with HTTP transport config
   - Document environment variable setup

## Testing Strategy
1. **Unit Tests**: AcronymsService search logic, API key validation
2. **Integration Tests**: REST endpoint, MCP endpoint with/without auth
3. **File Watch Tests**: Modify JSON, verify reload
4. **Fuzzy Match Tests**: Common typos (Temcenter, Simmcenter)
5. **Performance Tests**: 1000+ term acronyms, <100ms response

Run with: `pytest -v --cov=.`

## Risks & Considerations
- **File I/O Performance**: Each request checks file mtime (minimal overhead)
- **Memory Usage**: Entire acronyms loaded in memory (OK for <10k terms)
- **Security**: API keys in plain text (acceptable for demo)
- **Fuzzy Matching**: May return unexpected results with very short queries
- **JSON Validation**: Malformed JSON could crash service (add try/catch)
- **Concurrent Access**: File reload not thread-safe (use lock if needed)
