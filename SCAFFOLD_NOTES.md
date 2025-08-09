# Python Project Scaffold with Compound Engineering

*"Here to learn from fellow builders making the leap" - and now, sharing back what we've learned.*

## The Story Behind This Scaffold

I'm Daniel from [Serverless Toronto](http://serverlesstoronto.org/). I've been using LLMs since late 2022, but it wasn't until I saw Kieran Klaassen's video that everything clicked:

- **Video**: [Claude Code: How Two Engineers Ship Like a Team of 15](https://www.youtube.com/watch?v=Lh_X32t9_po)

This was my AHA moment. I adopted his "/issue + /work commands + Kanban" setup and found myself shipping at the velocity of a small team—thinking less like a lone developer and more like an Engineering Manager orchestrating parallel work streams.

Later, Kieran documented his workflow in detail, and Every Media, Inc. published their prompt templates:
- **Article**: [How I Use Claude Code to Ship Like a Team of Five](https://every.to/source-code/how-i-use-claude-code-to-ship-like-a-team-of-five)
- **Prompts**: [Claude Commands Repository](https://github.com/EveryInc/claude_commands)

## The Real Discovery: It's Not About Coding

Here's what most people miss about Compound Engineering: **it's not about coding faster—it's about specification and clarity**.

This approach has given me a renewed appreciation for the work of Business Analysts. Why? Because it emphasizes the old saying: *"If you don't know where you're going, you'll end up somewhere else."*

When you shift from coding to orchestrating AI agents, you suddenly have time to:
- Create thorough designs
- Think through edge cases
- Write clear specifications
- **Understand your users deeply**—what they actually need, not what's fun to build
- **Polish the rough edges**—make software people love, not just tolerate
- **Validate business value**—ensure every feature serves a real purpose
- Act as a true Engineering Manager who thinks about outcomes, not outputs

Technology doesn't exist in isolation—it's a function of business needs and human desires. The extra bandwidth from AI assistance means we can finally build software that's both powerful AND delightful to use.

The paradox? By stepping back from the keyboard, you ship more and better code that actually matters.

## Why This Scaffold Exists

YouTube is flooded with "me too" Agentic videos promising 10x productivity. There's some good info there, but choose your mentors carefully—you'll spend more time reading than doing. Stay close to the source: [Anthropic's Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices).

This scaffold is my interpretation of Compound Engineering, battle-tested and ready for reuse. I'm thoroughly enjoying this moment in software development history, and I want to share this excitement with the rest of you.

### The Core Philosophy

"Stop thinking in terms of files and functions. Start thinking about outcomes and delegation." 

This shifts your mental model from coding to engineering management—orchestrating multiple AI agents instead of being a single thread of execution, while keeping humans at the center of everything you build.

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

### Step 5: Set Up GitHub Project Board (Required for /issue and /work commands)

**See Working Example**: [Compound Engineering in Action](https://github.com/users/dzivkovi/projects/3)

**Create Your Kanban Board:**
1. Go to: https://github.com/YOUR_USERNAME?tab=projects
2. Click "New project" → Select "Board" template
3. Name it (e.g., "PROJECT_NAME Development" or "Compound Engineering in Action")
4. You'll get 3 default columns: Todo, In Progress, Done

**Optional: Add More Columns**
1. Click the "+" button (far right, after Done column)
2. Click "New Column" 
3. Name it (e.g., "In Review" or "Awaiting feedback")
4. Drag to reorder columns if needed
5. Click "..." on any column to edit details or add descriptions

**Verify Project-Repository Link**
1. Check if already linked: In your project, look for repository name in the header
2. If not linked: Go to project Settings → "Manage access" → Link repositories
3. Make sure "Projects" is enabled in your repo Settings → Features

**Optional: Make Project Public**
- By default, projects are private
- To make public: Project Settings → Scroll to "Danger zone" → Change visibility
- Public projects allow community contributors to see your workflow

**Optional: Add Project Description & README**
- In project Settings, add a short description (what you're building)
- Add a README to explain your workflow (markdown supported)
- Or via CLI: `gh api graphql` to update both programmatically
- This helps visitors understand your Compound Engineering approach

**Enable Automation:**
1. In the project, click "..." (top right menu) → Workflows
2. Enable "Item added to project" → Default to "Todo"
3. Enable "Item closed" → Move to "Done"

**Test It:**
Create an issue in your repo - it should automatically appear in the Todo column!

This Kanban board is essential for the Claude Code workflow—the `/issue` and `/work` commands interact with it.

### Step 6: Initialize Your Project
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