# Design Template Workspace

Place your `DESIGN.md` file here when starting new work. This serves as the staging area for issue creation.

## Template Structure

Copy this template into `DESIGN.md` in this folder:

```markdown
# <CLEAR DESCRIPTIVE TITLE>

## Problem / Metric
<Describe the problem being solved and measurable impact>

## Goal
<Clear statement of what success looks like>

## Scope (M/S/W)
- [M] Must have - Critical functionality that makes this feature viable
- [S] Should have - Nice to have but not essential
- [W] Won't have - Explicitly out of scope for this iteration

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 | <initial state> | <action taken> | <expected outcome> |
| 2 | ... | ... | ... |

## Technical Design
<Implementation approach, architecture decisions, key components>

## Implementation Steps
1. <Concrete step with file/component to modify>
2. <Next step...>

## Testing Strategy
<How to verify the implementation works>

## Risks & Considerations
<Potential issues, dependencies, or concerns>
```

## Workflow

1. **Check Documentation**: Always check latest documentation first before designing
2. **Draft**: Create or update `analysis/0000/DESIGN.md` with your design using the template above
3. **Issue**: Run `/issue "Your issue title"` - this links the design file
4. **Move**: After GitHub assigns issue #NN, run `mkdir -p analysis/NN && mv analysis/0000/DESIGN.md analysis/NN/`
5. **Commit**: Add and commit the organizational changes to main branch
6. **Work**: Run `/work NN` to create feature branch and implement the issue
7. **PR**: Create pull request - this triggers automated code reviews

## Important Notes

- **Clean Workspace**: Always ensure this folder contains only `README.md` after moving work to numbered folders
- **Documentation First**: Check relevant documentation and existing patterns before designing
- **Specificity**: Be specific about implementation details and include concrete acceptance criteria
