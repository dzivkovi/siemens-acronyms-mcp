# Design Command

**Model Preference**: Use the latest Claude 4 Opus model

You are creating a design document for a new feature or improvement. Your task is to generate a comprehensive DESIGN.md file that will guide implementation.

First, you will be given a feature description:

<feature_description>
$ARGUMENTS
</feature_description>

Follow these steps carefully:

1. **Check for existing designs**:
   - Check for DESIGN.md, DESIGN_b.md, DESIGN_c.md, etc. in analysis/0000/
   - Use alphabetic suffixes to avoid confusion with numbered issue folders
   - If DESIGN.md exists, create DESIGN_b.md; if both exist, create DESIGN_c.md, etc.
   - These represent uncommitted work that hasn't been turned into issues yet

2. **Analyze the request**:
   - Understand the problem being solved
   - Consider how it fits with existing architecture
   - Check relevant documentation and existing patterns
   - ALWAYS check latest documentation first

3. **Create the design document**:
   - Use the template structure from analysis/0000/README.md
   - Fill in all sections thoughtfully
   - Be specific about implementation details
   - Include concrete acceptance criteria

4. **Save the design**:
   - Write to `analysis/0000/DESIGN.md` (or DESIGN_b.md, DESIGN_c.md if others exist)
   - Include clear title and comprehensive details
   - Make it ready for `/issue` command to reference

## Design Document Structure

Your output should follow this template exactly:

```markdown
# <CLEAR DESCRIPTIVE TITLE>

## Problem / Metric
<Describe the problem being solved and measurable impact>

## Goal
<Clear statement of what success looks like>

## Scope (M/S/W)
- [M] Must have items...
- [S] Should have items...
- [W] Won't do items...

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

Remember:

- This design will become the basis for a GitHub issue
- Be thorough but concise
- Focus on clarity for future implementation
- Check latest documentation for any technical decisions