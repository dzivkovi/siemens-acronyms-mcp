# Contributing to Siemens Acronyms MCP Server

## Development Setup

1. **Clone and activate environment**
   ```bash
   git clone <repository-url>
   cd siemens-acronyms-mcp
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m pip install --upgrade pip  # Important: upgrade pip first!
   pip install -r requirements.txt
   
   # Optional: Load useful aliases
   source scripts/aliases.sh
   ```

2. **Configure environment**
   ```bash
   cp env.example .env
   # Add your MCP_API_KEYS to .env
   ```

## Development Workflow

### Test-Driven Development (Required)

1. **Write failing test first** in `tests/test_acronyms_server.py`
   ```python
   def test_search_acronym_returns_exact_match():
       # Test MUST fail initially
       result = search_acronym("EDA")
       assert result["results"][0]["acronym"] == "EDA"
   ```

2. **Implement minimal code** to pass the test
3. **Refactor** while keeping tests green

### Before Committing

```bash
# Run tests multiple times (catch AI nondeterminism)
pytest -v

# Code quality (120 char line length configured)
ruff format .
ruff check . --fix
```

## Pull Request Process

1. **Branch naming**: `feat|fix|docs|chore/<description>`
   ```bash
   git checkout -b feat/add-fuzzy-search
   ```

2. **Commit messages**: Use conventional commits
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation only
   - `chore:` Maintenance

3. **PR checklist**:
   - [ ] Tests pass (`pytest -v`)
   - [ ] Code formatted (`ruff format .`)
   - [ ] Linting clean (`ruff check .`)
   - [ ] New tests for new features
   - [ ] Updated `siemens_acronyms.json` if adding terms

## Adding Acronyms

Edit `siemens_acronyms.json`:
```json
{
  "acronym": "NEW",
  "expansion": "New Engineering Widget",
  "description": "Brief description"
}
```

Run server to verify hot-reload works:
```bash
uvicorn src.main:app --reload
```

## Code Standards

- Type hints for all functions
- Docstrings for public functions
- Async/await for I/O operations
- 120-character line limit (configured in pyproject.toml)