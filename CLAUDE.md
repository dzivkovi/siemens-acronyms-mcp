# Siemens Acronyms MCP Server

This project provides a glossary service for Siemens-specific terminology, accessible via REST and MCP.

## Common Commands
- `pytest -v` - Run all tests
- `pytest -v --cov=src` - Run tests with coverage
- `uvicorn src.main:app --reload` - Start development server
- `./scripts/validate_acronyms.py` - Validate acronyms JSON structure

## Project Structure
- `src/main.py` - FastAPI application with REST and MCP endpoints
- `src/acronyms_service.py` - Core search logic with file watching
- `siemens_acronyms.json` - Glossary data (external, reloadable)
- `tests/` - Pytest test suite (TDD approach)

## Code Style
- Use type hints for all function parameters and returns
- Follow PEP 8 with 88-character line limit (Black formatter)
- Docstrings for all public functions
- Async/await for I/O operations

## Testing Guidelines
- Write tests FIRST (TDD)
- Each test should test ONE thing
- Use descriptive test names: test_<what>_<when>_<expected>
- Mock external dependencies (file I/O for unit tests)

## API Design
- REST endpoint is PUBLIC (no auth)
- MCP endpoint requires API key via environment variable
- All responses use same format for consistency
- Fuzzy matching with RapidFuzz for typo tolerance

## Important Files
- `design.md` - Complete technical design document
- `.env` - Local environment variables (not in git)
- `.vscode/mcp.json` - VS Code MCP configuration

## Workflow
1. Write failing tests first
2. Implement minimal code to pass tests
3. Refactor if needed
4. Commit with descriptive messages
5. Update this file with new patterns/commands
