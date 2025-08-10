Check the current state of interrupted /work and continue from where we left off.

## First: Load Work Context

Always read the `/work` command to understand the full workflow and what each step involves:
```bash
cat .claude/commands/work.md
```

## State Detection

```bash
# 1. Current branch and issue
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"

# Extract issue number from branch name (e.g., feat/4-description -> 4)
ISSUE_NUM=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
if [ -n "$ISSUE_NUM" ]; then
  echo "Working on issue: #$ISSUE_NUM"
  gh issue view $ISSUE_NUM --comments | head -20
else
  echo "No issue detected. Specify issue number or use /work to start new work."
fi

# 2. Git status
echo -e "\n=== Git Status ==="
if [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes found:"
  git status -s
else
  echo "✓ No uncommitted changes"
fi

# 3. Test status
echo -e "\n=== Test Status ==="
if pytest -v --last-failed --tb=no 2>/dev/null | grep -q "failed"; then
  echo "❌ Some tests are failing - need to fix"
  pytest -v --last-failed --tb=short
else
  echo "✓ All tests passing"
fi

# 4. Open PRs
echo -e "\n=== Open PRs ==="
OPEN_PRS=$(gh pr list --state open --author @me --json number,title --jq length)
if [ "$OPEN_PRS" -gt 0 ]; then
  echo "You have open PRs:"
  gh pr list --state open --author @me
else
  echo "No open PRs"
fi
```

## Resume Decision

Based on the above status, continue at the appropriate step from `/work` workflow:

1. **If uncommitted changes exist**:
   - Tests failing → Continue at **Step 4: TEST** or **Step 5: CODE**
   - Tests passing → Continue at **Step 6: VALIDATE**

2. **If all clean (no uncommitted changes)**:
   - No PR exists → Continue at **Step 8: PR**
   - PR exists → Continue at **Step 9: COMPLETE**

3. **If on main branch**: 
   - Check for issue to work on → Start at **Step 1: ANALYZE**

4. **If DESIGN.md exists in analysis/0000/**:
   - Move it to numbered folder → Execute **Step 7: ORGANIZE**

Reference the specific step details from `/work.md` that you loaded above.