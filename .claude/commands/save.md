---
model: haiku
---

FAST and SMART save. Speed with intelligence.

## User Instructions:
$ARGUMENTS

## What to save:

If $ARGUMENTS is provided:
- Use it as INSTRUCTIONS for what content to save
- Examples:
  - "2 answers before this one" → Save the 2 previous responses
  - "the Python installation discussion" → Save content about Python installation
  - "code snippets only" → Extract just the code from recent messages
  - Empty/none → Save last assistant response

## Execution:

1. **Run bash ONCE** to get date, number, timestamp:
```bash
bash -c 'D=$(date +%Y-%m-%d); mkdir -p work/$D; N=$(printf "%02d" $(($(ls -1 work/$D/ 2>/dev/null | grep -E "^[0-9]{2}-" | tail -1 | cut -d- -f1 | sed "s/^0*//" || echo 0) + 1))); T=$(date +"%Y-%m-%d at %H:%M:%S %Z"); echo "$D|$N|$T"'
```

2. **Determine content** (following user instructions from $ARGUMENTS)

3. **Generate smart filename** from content summary (3-5 words, kebab-case):
   - Analyze what's being saved
   - Create descriptive name: `python-version-switching`, `save-command-optimization`, etc.
   - Keep it SHORT but MEANINGFUL

4. **Write file** to: `work/DATE/NUMBER-smart-filename.md`

## Content Structure:

```markdown
Date: TIMESTAMP

[Content based on user instructions]
```

**Balance speed with intelligence:**
- Smart filename generation (worth the extra 0.5-1s)
- Follow user instructions carefully
- Clean, readable content
- Target: 2-3 seconds total execution

Execute NOW!
