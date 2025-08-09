# Siemens Acronyms MCP Server

A demonstration of how to add Model Context Protocol (MCP) capabilities to existing internal APIs without external package deployment.

## Overview

This server exposes Siemens-specific terminology through:
- **REST API** - Public access at `/api/v1/search`
- **MCP Endpoint** - Protected access at `/mcp` (requires API key)
- **Health Check** - System status at `/health`

## Features

- 🔍 **Fuzzy Search** - Handles typos using RapidFuzz
- 🔄 **Hot Reload** - Updates acronyms without restart
- 🔒 **Secure MCP** - API key authentication for MCP endpoint
- 📖 **Swagger UI** - Interactive API documentation at `/docs`
- 🧪 **Test-Driven** - Comprehensive test suite with pytest

## Quick Start

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd <project-name>
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run tests**
   ```bash
   pytest -v
   ```

4. **Start server**
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Test endpoints**
   - REST: http://localhost:8000/api/v1/search?q=EDA
   - Swagger: http://localhost:8000/docs
   - Health: http://localhost:8000/health

## MCP Client Configuration

### Claude
```bash
claude mcp add siemens-acronyms \
  --transport http \
  --env GLOSSARY_API_KEY=sk-team-A \
  http://localhost:8000/mcp
```

### VS Code
See `.vscode/mcp.json` for configuration.

## Development

This project follows Test-Driven Development (TDD):
1. Write failing tests in `tests/`
2. Implement features in `src/`
3. Refactor as needed
4. Commit with clear messages

## API Examples

### Search for acronym
```bash
curl "http://localhost:8000/api/v1/search?q=DISW"
```

### Handle typos
```bash
curl "http://localhost:8000/api/v1/search?q=Temcenter"
# Returns: Teamcenter
```

## Contributing

1. Check existing issues or create new ones
2. Follow TDD approach
3. Update tests for new features
4. Update `siemens_acronyms.json` for new terms

## License

- **Code**: MIT License
- **Glossary Data**: Creative Commons Attribution 4.0 International (CC BY 4.0)

This allows both internal and external users to benefit from and contribute to the glossary.
