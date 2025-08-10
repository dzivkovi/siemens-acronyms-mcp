Check the current state of interrupted /work and continue from where we left off.

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

Based on the above status:

1. **If uncommitted changes**: Continue with implementation or testing
2. **If tests failing**: Fix the failing tests
3. **If all tests pass + no PR**: Ready to create PR (go to step 8 of /work)
4. **If PR exists**: Check if it needs project assignment or review

Continue with the appropriate step from the `/work` command workflow.