# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Siemens Acronyms MCP Server - A glossary service exposing Siemens-specific terminology via REST API and MCP endpoint. Demonstrates adding MCP capabilities to existing internal APIs without external package deployment.

## Commands

### Development
- `pytest -v` - Run all tests
- `pytest -v --cov=src` - Run tests with coverage report
- `pytest -v tests/test_acronyms_server.py::test_specific` - Run specific test
- `uvicorn src.main:app --reload` - Start development server (port 8000)
- `uvicorn src.main:app --reload --port 8001` - Start on alternate port

### Code Quality
- `ruff format .` - Format code (120 char line length)
- `ruff check . --fix` - Fix linting issues automatically
- `ruff check .` - Check for linting issues without fixing

### Environment Setup
- `python -m venv venv && source venv/bin/activate` - Create/activate virtual environment
- `pip install -r requirements.txt` - Install dependencies
- `cp .env.example .env` - Create environment file (edit with API keys)

## Architecture

### Service Architecture
The application follows a layered architecture with clear separation of concerns:

1. **FastAPI Application** (`src/main.py`)
   - Dual endpoint strategy: Public REST API + Protected MCP endpoint
   - REST: `/api/v1/search` - No authentication required
   - MCP: `/mcp` - Requires API key via `X-API-Key` header
   - Health check: `/health` - System status monitoring

2. **Acronyms Service** (`src/acronyms_service.py`)
   - Core search logic with fuzzy matching (RapidFuzz library)
   - File watcher for hot-reloading `siemens_acronyms.json`
   - Singleton pattern for service instance
   - Async/await for I/O operations

3. **Data Layer**
   - `siemens_acronyms.json` - External glossary file (hot-reloadable)
   - Format: Array of objects with `acronym`, `expansion`, `description` fields
   - Licensed under CC BY 4.0 for open contribution

### MCP Integration Pattern
- Uses `fastmcp` library for MCP protocol implementation
- Authentication via environment variable `GLOSSARY_API_KEY`
- Same search functionality exposed through both REST and MCP
- Response format consistency across both endpoints

## Development Workflow

### Parallel Task Execution
IMPORTANT: Always use parallel execution via the Task tool when possible. Examples of parallelizable tasks:
- Searching for patterns across multiple directories simultaneously
- Running independent test suites concurrently
- Analyzing different code modules in parallel
- Fetching data from multiple sources at once
- Generating documentation for multiple components

This improves performance significantly and should be the default approach for independent operations.

### TDD Approach (MANDATORY)
1. Write failing test in `tests/test_acronyms_server.py`
2. Implement minimal code to pass test
3. Refactor if needed (maintain all tests passing)
4. Commit with descriptive message

### Test Naming Convention
- Pattern: `test_<what>_<when>_<expected>`
- Example: `test_search_with_typo_returns_fuzzy_match`
- Mock file I/O for unit tests, use fixtures for integration tests

## Code Standards

### Python Style
- Type hints for ALL function parameters and returns
- PEP 8 with 120-character line limit (configured in ruff)
- Docstrings for public functions (Google style)
- Async/await for I/O operations

### API Response Format
```python
{
    "results": [...],  # Always array, even for single result
    "query": "...",    # Echo back the search query
    "count": N         # Number of results
}
```

## Important Context

### Environment Variables
- `GLOSSARY_API_KEY` - Required for MCP endpoint authentication
- `GLOSSARY_FILE_PATH` - Optional, defaults to `siemens_acronyms.json`
- `LOG_LEVEL` - Optional, defaults to `INFO`

### File Watching
The service automatically reloads acronyms when `siemens_acronyms.json` changes. No restart required for data updates.

### Fuzzy Matching
Uses RapidFuzz with configurable threshold (default 80% similarity) to handle typos and partial matches.

## Current State Notes

- Core implementation files (`src/main.py`, `src/acronyms_service.py`) are currently empty scaffolds
- Test file has placeholder - implement real tests following TDD
- Design document (`design.md`) needs to be populated with complete specification
- `./scripts/validate_acronyms.py` referenced in old CLAUDE.md does not exist yet