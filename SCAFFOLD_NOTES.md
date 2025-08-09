# Python Project Scaffold with Compound Engineering

This repository serves as a reusable scaffold for Python projects using the Compound Engineering workflow with Claude Code.

## Inspiration & Philosophy

This scaffold implements the "Compound Engineering" approach, inspired by:
- **Article**: [How I Use Claude Code to Ship Like a Team of Five](https://every.to/source-code/how-i-use-claude-code-to-ship-like-a-team-of-five) by Kieran (Every Inc)
- **Video**: [Claude Code: How Two Engineers Ship Like a Team of 15](https://www.youtube.com/watch?v=Lh_X32t9_po)

The core philosophy: Stop thinking in terms of files and functions. Start thinking about outcomes and delegation.

## What This Scaffold Provides

### Claude Code Integration
- 6 custom slash commands in `.claude/commands/`
- CLAUDE.md with project-specific AI instructions
- Emphasis on parallel task execution via subagents

### Development Workflow
- TDD-first approach enforced in documentation
- Ruff for formatting/linting (120 char line length)
- GitHub issue templates (epic, story, infra)
- Structured analysis folder for note-taking

### Python Project Structure
- FastAPI application skeleton
- pyproject.toml with modern tooling
- Type hints and async/await patterns
- Comprehensive test structure with pytest

### Bonus: MCP Integration Example
This specific instance demonstrates adding MCP (Model Context Protocol) on top of a REST API, but MCP is optional for your project.

## How to Reuse This Scaffold

### Step 1: Clone and Rename
```bash
git clone <this-repo> your-project-name
cd your-project-name
rm -rf .git
git init
```

### Step 2: Quick Domain Replacement

Run these commands to find and replace domain-specific terms:
```bash
# Find all Siemens/acronym references
grep -r "siemens\|Siemens\|acronym\|Acronym\|glossary\|Glossary" --exclude-dir=.git --exclude-dir=venv

# Common replacements needed:
# - "Siemens" → Your company/domain
# - "acronym/Acronym" → Your data type
# - "glossary/Glossary" → Your service type
# - "siemens-acronyms-mcp" → your-project-name
```

### Step 3: Key Files to Update

| File | Current Purpose | Customize For Your Project |
|------|----------------|---------------------------|
| `README.md` | Describes acronym/glossary service | Your project's purpose |
| `CLAUDE.md` | AI instructions for acronym service | Your project's architecture |
| `pyproject.toml` | name = "siemens-acronyms-mcp" | name = "your-project" |
| `siemens_acronyms.json` | Sample data file | Your data (or delete) |
| `src/acronyms_service.py` | Service logic | Rename to match your domain |
| `tests/test_acronyms_server.py` | Test suite | Rename to match your domain |
| `.env.example` | GLOSSARY_API_KEY | Your env variables |

### Step 4: MCP Configuration (Optional)
If NOT using MCP:
- Delete `.mcp.json` and `.vscode/mcp.json`
- Remove MCP sections from CLAUDE.md
- Remove `fastmcp` from requirements.txt

If keeping MCP:
- Update MCP endpoint paths in CLAUDE.md
- Modify authentication approach as needed

### Step 5: Initialize Your Project
```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install --upgrade pip  # CRITICAL: Upgrade pip first!
pip install -r requirements.txt

# Optional: Use the provided aliases for quicker setup
source scripts/aliases.sh
# Then: mkv, va, vp, pip install -r requirements.txt

# Run initial tests to ensure scaffold works
pytest -v

# Format and lint
ruff format .
ruff check . --fix

# Create initial commit
git commit -m "feat: Initialize project from Compound Engineering scaffold"
```

## What Makes This Scaffold Special

1. **Compound Engineering Ready**: Optimized for AI-assisted development with Claude Code
2. **Complete Workflow**: From design (`/design`) to implementation (`/work`) to reflection
3. **Quality Built-in**: TDD, linting, and formatting pre-configured
4. **Documentation-First**: CLAUDE.md ensures consistent AI assistance across sessions
5. **Real Example**: Based on actual production code, not theoretical templates

## Key Principles to Maintain

1. **TDD Always**: Write tests first, implementation second
2. **Parallel Execution**: Leverage Claude's Task tool for independent operations
3. **Clear Documentation**: Keep CLAUDE.md updated with project-specific patterns
4. **Structured Notes**: Use analysis/ folder for design docs and decisions
5. **Definition of Done**: Every issue/PR has clear completion criteria

## Why This Structure Works

- **Cognitive Offload**: CLAUDE.md ensures every new Claude instance understands your project
- **Workflow Automation**: Slash commands reduce repetitive tasks
- **Quality Gates**: TDD + ruff + pytest ensure code quality
- **Context Preservation**: Analysis folder maintains project history

## Current Example Domain

This scaffold currently contains a working example of a glossary/terminology service with:
- REST API for public access
- MCP endpoint for AI tool integration
- Hot-reloading data file
- Fuzzy search capabilities

This is just ONE possible use case - adapt it to your needs!

---

**Note**: After customization, you can delete this SCAFFOLD_NOTES.md file, or move it to `analysis/0000/` for reference.