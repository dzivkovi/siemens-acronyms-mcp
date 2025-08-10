You are an AI assistant implementing GitHub issues using Test-Driven Development. Your goal is to take a GitHub issue number and implement it following established engineering best practices.

**Model Preference**: Use the latest Claude 4 Sonnet model

**Issue to implement:**
$ARGUMENTS

## Workflow

**Note:** If work was interrupted, use `/resume` command to check state and continue.

### Step 1: ANALYZE - Understand the Issue
```bash
# If ARGUMENTS is issue number: gh issue view $ARGUMENTS
# If ARGUMENTS is description: search for related issue first
gh issue view $ARGUMENTS --comments
```
- Understand the problem and requirements
- Read all comments for important updates/corrections

### Step 2: BRANCH - Create Feature Branch
```bash
# Determine work type based on issue (feat|fix|docs|chore)
# Use issue number and brief description for branch name
git checkout -b <TYPE>/$ARGUMENTS-brief-description

# Examples:
# git checkout -b feat/19-python-formatting-cleanup
# git checkout -b fix/23-database-connection-error
# git checkout -b docs/15-api-documentation-update
# git checkout -b chore/8-dependency-updates
```
- Follow project convention: `<TYPE>/$ISSUE_NUMBER-description`
- Keep description brief but descriptive
- Branch created before any implementation work begins

### Step 3: RESEARCH - Understand Codebase
- Read CLAUDE.md for project context and commands
- **Check for design document**: Read `analysis/$ARGUMENTS/DESIGN.md` if it exists
- Search for relevant files using available tools
- Understand existing patterns and conventions
- Use Context7 MCP to get the most recent documentation

### Step 4: TEST - Write Failing Tests First
**Critical:** Tests define success. Implementation serves tests.
- Write tests that demonstrate the required capability
- Ensure tests fail initially (proves they're testing the right thing)
- Include edge cases and performance requirements
- For AI features: Plan to run tests 5+ times to catch nondeterminism

### Step 5: CODE - Implement Minimal Solution
- Follow existing code patterns and conventions
- Use project libraries and tools (ruff for linting, pytest for testing)
- Implement only what's needed to pass the tests

### Step 6: VALIDATE - Run Quality Checks
```bash
# Run tests multiple times (catch AI nondeterminism)
pytest -v

# Code quality (120 char line length configured)
ruff format .
ruff check . --fix
```

### Step 7: ORGANIZE - Move Design Document
```bash
mkdir -p analysis/$ARGUMENTS && mv analysis/0000/DESIGN.md analysis/$ARGUMENTS/DESIGN.md
```

### Step 8: PR - Create Pull Request
8.1 Show the proposed commit message
8.2 ⚠️ STOP: Ask user for review before committing
8.3 Wait for explicit approval: "Ready to commit and create PR?"

```bash
# Use appropriate work type prefix: feat|fix|docs|chore
# Descriptive commit following project patterns
git add -A
git commit -m "<TYPE>: implement [brief description]

- Key changes made
- Evaluation tests now passing
- All quality gates passing

Closes #$ISSUE_NUMBER"

git push -u origin <TYPE>/$ISSUE_NUMBER-description

# Create PR and capture the URL
PR_URL=$(gh pr create --title "<TYPE>: [Issue title]" --body-file .github/PULL_REQUEST_TEMPLATE.md)
echo "PR created: $PR_URL"

# Try to add to project (auto-detect owner and project)
# Note: This is optional - if it fails, just add via GitHub UI
REPO_OWNER=$(gh repo view --json owner --jq '.owner.login')
# Get the first open project number (no hardcoding!)
PROJECT_NUM=$(gh project list --owner $REPO_OWNER --format json | jq -r '.projects[] | select(.closed == false) | .number' | head -1)

gh project item-add $PROJECT_NUM --owner $REPO_OWNER --url "$PR_URL" 2>/dev/null && \
  echo "✓ Added to project #$PROJECT_NUM" || \
  echo "→ Add to project manually: Open PR → Right sidebar → Projects → Select project"
```

### Step 9: COMPLETE - Monitor and Finish
The PR is created and should be added to the project. 
- If project addition failed, open the PR and add it via the right sidebar
- Monitor CI checks and review feedback

## Key Principles for This Project

- **Evaluation-First:** Write tests before implementation, run 5+ times
- **Tests are Immutable:** Never modify tests to make implementation easier
- **Less is More:** Simplest solution that passes tests wins
- **Quality Gates:** All automated validation must pass before completion
- **Defensive Programming:** MANDATORY validation after every code change (see CLAUDE.md)

## Project-Specific Notes

- Line length: 120 characters (configured in pyproject.toml)
- Testing: Focus on evaluation tests that verify business requirements
- Performance: Query responses should be <1s for evaluation criteria
