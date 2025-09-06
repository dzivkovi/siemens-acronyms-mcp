Please save content as a markdown file with a specific naming convention and structure. Follow these instructions carefully:

## CRITICAL: Check for user instructions FIRST!

If the user provided specific instructions about what to save:
<user_instructions>
$ARGUMENTS
</user_instructions>

- If user instructions exist above, follow them to determine WHAT content to save
- If no instructions provided (empty), default to saving your last response

Examples:
- `/note` → Save your last response
- `/note (AI extraction conversation)` → Save content about AI extraction conversation
- `/note (summary of GraphRAG implementation)` → Save summary of GraphRAG work

### CRITICAL: I'll run commands to find your next file number:
The /note command will automatically:
1. Create today's analysis directory
2. Check what numbered files already exist  
3. Show you the template path with NN to replace

Just use `/note` and I'll handle the directory checking for you.

This command will:
1. Create the correct date folder (e.g., analysis/2025-07-21)
2. Show you what numbered files already exist
3. Tell you to pick the next number (NN) and replace meaningful-name

### IMPORTANT: Copy the exact path shown in the output and use it for the Write command!

## 1. File Naming and Location

Save the file in the following format: `analysis/$CURRENT_DATE/NN-meaningful-file-name.md` where:

### IMPORTANT NOTES:

1. Use bash `date` command for dates

- Always use a bash variable to store and reuse the current date:
```bash
CURRENT_DATE=$(date +%Y-%m-%d)
mkdir -p analysis/$CURRENT_DATE
```

- DO NOT manually type the date - always use the $CURRENT_DATE variable to avoid month transcription errors.

2. NN is a two-digit number (01, 02, etc.) indicating the order of the file for that day

3. Meaningful-file-name is a brief description of the content. If this is the first note of the day, start with 01. Otherwise, increment this number sequentially.

## 2. Content Structure

Each entry should include:

- Date and timestamp (use bash command: `date +"%Y-%m-%d at %H:%M:%S %Z"`)

### WARNING - COMMON BUG:
The date July 21 is `2025-07-21` NOT `2025-01-21`!
- 07 = July (NOT 01 which is January)
- If today is July 21, the folder MUST be `analysis/2025-07-21/`
- Context of the conversation
- The question/query from the user
- Your analysis and findings as seen in the chat
