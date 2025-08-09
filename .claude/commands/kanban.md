**Model Preference**: Use the latest Claude 4 Opus model

You are helping document and package already-completed work into proper GitHub issues and PRs for project management visibility. This is for situations where significant work has been done but needs retroactive documentation for stakeholder communication.

**Context**: The user has completed significant work (uncommitted changes) but realized it should be properly tracked as an issue/PR for project management and client visibility.

## Command Usage
```
/kanban "what you did"     # Simplest - I'll ask 3 questions and handle the rest
/kanban                    # Same as above, I'll ask what you did first
/kanban feat "what you did" # Skip the type question
```

## SIMPLE MODE (Default Approach)

When user runs `/kanban "what you did"`, ask these 3 questions:
1. **Type?** "Is this a feat (new feature), fix (bug fix), docs, or chore?"
2. **Why does it matter?** "What problem did this solve for users/business?"
3. **What should I verify still works?** "Any specific tests I should highlight?"

Then handle everything else automatically.

## CRITICAL CHECKLIST (for all models):
```
[ ] git status - See what changed (RECORD: note any untracked files)
[ ] Create issue - Get issue number
[ ] git stash push -m "..." --include-untracked - Save ALL work
[ ] VERIFY: git stash list - Confirm stash created
[ ] Create branch - feat/XX-description
[ ] git stash pop - Restore work to branch
[ ] VERIFY: git status - Confirm all changes restored
[ ] git add -A - Stage changes
[ ] git commit - Link to issue
[ ] git push - Push branch
[ ] Create PR - Link everything
```

**SAFETY GUARANTEE**: If process fails at any step, run `git stash list` and `git stash pop` to recover all work.

## Workflow: Retroactive Issue Creation

### 1. Assess Current State
```bash
# Check what's been done but not committed
git status
git diff --stat

# Understand the scope of changes
ls -la scripts/ | grep -E "new|modified"
```

### 2. Document the Work as an Issue

Think deeply about:
- **What problem was solved?** (not just what code changed)
- **Why does it matter to the business/client?**
- **What are the measurable improvements?**
- **What testing was done?**

Create a comprehensive issue that tells the story:
```bash
gh issue create --title "feat: [Descriptive title of what was accomplished]" \
  --body "[Comprehensive description including:
  - Problem statement
  - Solution approach
  - Business benefits
  - Technical improvements
  - Testing results
  - Metrics/statistics
  ]" \
  --label enhancement
```

### 3. Preserve Current Work
```bash
# Stash with descriptive message
git stash push -m "[Brief description of improvements]" --include-untracked
```

### 4. Create Proper Branch
```bash
# Use the issue number from step 2
git checkout -b feat/[ISSUE_NUMBER]-[brief-description]
```

### 5. Restore Work to Branch
```bash
# Pop the stashed changes
git stash pop
```

### 6. Stage and Review
```bash
# Stage all changes
git add -A

# Review what will be committed
git status
```

### 7. Create Meaningful Commit
```bash
git commit -m "feat: [Match issue title]

[Bullet points of key changes]
[Business impact]
[Technical achievements]

Closes #[ISSUE_NUMBER]"
```

### 8. Push and Create PR
```bash
# Push branch
git push -u origin [branch-name]

# Create PR with comprehensive body
gh pr create --title "feat: [Issue title]" \
  --body "[Include:
  - Link to issue
  - Before/after comparison
  - Validation results
  - Key metrics
  ]"
```

## Key Principles

1. **Tell the Story**: Focus on WHY the work matters, not just WHAT changed
2. **Quantify Impact**: Include metrics, performance improvements, coverage stats
3. **Business Language**: Write for stakeholders, not just developers
4. **Complete Documentation**: The issue should stand alone as a project artifact
5. **Proper Attribution**: Give credit to the deep work that was done

## Example Messages

**Bad**: "Updated scripts and fixed stuff"

**Good**: "Made surveillance system portable across datasets, achieving 100% content coverage (146,335 nodes) and standardizing backup procedures"

## Issue Template (REQUIRED SECTIONS ONLY)

```markdown
## Summary
[Answer to "What did you do?" and "Why does it matter?"]

## What We Accomplished
[Bulleted list from git diff analysis]

## Validation & Testing
[Answer to "What should I verify still works?"]

## Files Changed
[From git status]
```

## Optional Sections (add if relevant):
- **Metrics**: [If performance improvements]
- **Technical Details**: [If complex changes]
- **Next Steps**: [If this enables future work]

## Auto-Detection Rules

**Type Detection**:
- New files = feat
- Only fixes = fix  
- Only docs/ = docs
- Scripts/config = chore

**Stash Message**: Use same as issue title

**Branch Name**: `{type}/{issue-number}-{kebab-case-description}`

**Commit Message**:
```
{type}: {issue title}

{3-5 bullet points from issue}

Closes #{issue-number}
```

## Quick Reference
```
INPUT:  /kanban "made scripts portable"
OUTPUT: 
  1. Ask: feat/fix/docs/chore?
  2. Ask: Why does it matter?
  3. Ask: What tests to highlight?
  4. Execute checklist automatically
```

**FOR ANY MODEL**: Stick to the 9-step checklist. Don't overthink. If stuck, just ask the user.