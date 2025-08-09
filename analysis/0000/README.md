# Design Template Workspace

Place your `DESIGN.md` file here when starting new work. This serves as the staging area for issue creation.

## Template Structure

Copy this template into `DESIGN.md` in this folder:

```markdown
# <WORKING TITLE>

## Problem / Metric
_TBD_

## Goal
_TBD_

## Scope (M/S/W)
- [M] …
- [S] …
- [W] …

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 |       |      |      |

---
*(generated automatically – refine or replace before work starts)*
```

## Workflow

1. **Draft**: Create or update `analysis/0000/DESIGN.md` with your design
2. **Issue**: Run `/issue "Your issue title"` - this links the design file
3. **Move**: After GitHub assigns issue #NN, run `mkdir -p analysis/NN && mv analysis/0000/DESIGN.md analysis/NN/`
4. **Commit**: Add and commit the organizational changes to main branch
5. **Work**: Run `/work NN` to create feature branch and implement the issue
6. **PR**: Create pull request - this triggers automated code reviews

**Important**: Always ensure this folder contains only `README.md` (this file) after moving work to its numbered folder. This keeps the workspace clean for the next task.
