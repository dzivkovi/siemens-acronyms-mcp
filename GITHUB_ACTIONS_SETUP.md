# GitHub Actions for Code Reviews

## Overview
This guide helps you integrate Claude automated code reviews into your GitHub repository. 

## Method 1: Official Automatic Setup (Try This First!)

The simplest way is to use the official automatic installation:

### Official Documentation
**Start here:** https://docs.anthropic.com/en/docs/claude-code/github-actions

### Quick Steps
1. In Claude Code, run: `/install-github-app`
2. Follow the prompts to authenticate and select your repository
3. Add your API key when prompted

**If this works, you're done!** 🎉

## Method 2: Manual Setup (Fallback)

If the automatic setup fails (common error: 404 "GitHub App not found"), use this proven manual approach.

### Why Manual Setup?
The `/install-github-app` command may fail due to:
- GitHub App installation issues
- Authentication token limitations
- Repository permission conflicts

This manual method works reliably by directly copying the official workflow files.

## Prerequisites for Manual Setup
1. GitHub repository with admin access
2. Anthropic API key
3. GitHub CLI (`gh`) installed and authenticated

## Manual Setup Steps

### Step 1: Get the Workflow Files
Copy the workflow files directly from the official repository - DO NOT modify them initially:

```bash
# Clone the official claude-code-action repository
git clone https://github.com/anthropics/claude-code-action.git /tmp/claude-code-action

# Create workflows directory in your project
mkdir -p .github/workflows

# Copy the essential workflow files
cp /tmp/claude-code-action/.github/workflows/claude.yml .github/workflows/
cp /tmp/claude-code-action/examples/claude-auto-review.yml .github/workflows/
```

### Step 2: Adjust for Your Language/Framework
The default workflows use `bun` (JavaScript/TypeScript). For Python projects, update the `allowed_tools` and `custom_instructions`:

**In `.github/workflows/claude.yml`**, replace:
```yaml
allowed_tools: "Bash(bun install),Bash(bun test:*),Bash(bun run format),Bash(bun typecheck)"
custom_instructions: "You have also been granted tools for editing files and running bun commands..."
```

With Python-specific tools:
```yaml
allowed_tools: "Bash(pytest:*),Bash(python:*),Bash(python3:*),Bash(pip:*),Bash(pip3:*),Bash(pip install:*),Bash(ruff:*),Bash(ruff format:*),Bash(ruff check:*),Bash(uvicorn:*),Bash(source:*),Bash(cat:*),Bash(ls:*),Bash(pwd:*),Bash(echo:*)"
custom_instructions: "You are working on a Python project. You have access to Python development tools including pip for package management, pytest for testing, and ruff for formatting/linting."
```

### Step 3: Add Repository Secret
1. Go to your repository settings: `https://github.com/[YOUR_USERNAME]/[YOUR_REPO]/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Anthropic API key
5. Click "Add secret"

### Step 4: Commit and Push
```bash
git add .github/workflows/
git commit -m "feat: Add GitHub Actions for Claude code reviews"
git push origin your-branch-name
```

## What You Get

### 1. claude.yml - Interactive Assistant
- **Triggers on**: Comments containing `@claude` in issues and PRs
- **Use case**: Ask Claude questions about code, request changes, get explanations
- **Example**: Comment "@claude can you check if the error handling is correct?"

### 2. claude-auto-review.yml - Automatic PR Reviews
- **Triggers on**: New PRs and updates to PRs
- **Use case**: Automatic code review on every PR
- **What it reviews**: Code quality, bugs, performance, security, test coverage

## Testing Your Setup

### Test 1: Create an Issue
1. Create a new issue on GitHub
2. In the issue body or comment, write: `@claude explain what this repository does`
3. Wait ~30-60 seconds for Claude to respond

### Test 2: Create a Pull Request
1. Push a branch with changes
2. Create a PR from that branch
3. Claude will automatically review it within 1-2 minutes

### Test 3: Check Action Logs
1. Go to Actions tab in your repository
2. Look for "Claude Code" or "Claude Auto Review" workflows
3. Click on a run to see detailed logs

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Action doesn't trigger | Check if workflows are on the default branch or in the PR's base branch |
| "Bad credentials" error | Verify ANTHROPIC_API_KEY secret is set correctly |
| No response from Claude | Check Actions tab for workflow runs and error logs |
| Permission denied | Ensure workflows have correct permissions (see workflow files) |

### Required Workflow Permissions
The workflows need these permissions (already configured in the files):
- `contents: read` - Read repository code
- `pull-requests: read` - Read PR information  
- `issues: read` - Read issue information
- `id-token: write` - Required for authentication

## Important Notes

1. **No GitHub App Required**: Despite documentation mentioning app installation, these workflows use GitHub Actions directly - no app installation needed.

2. **Model Version**: The workflows use the latest Claude Opus model (`claude-opus-4-1-20250805`). This can be changed in the workflow files if needed.

3. **WSL2/Windows Users**: The setup works identically on WSL2. GitHub Actions run on GitHub's servers, not locally.

4. **Costs**: 
   - GitHub Actions minutes (free tier includes 2000 minutes/month)
   - Anthropic API usage (check your plan's limits)

## File Structure
After setup, you should have:
```
.github/
└── workflows/
    ├── claude.yml           # Responds to @claude mentions
    └── claude-auto-review.yml  # Automatic PR reviews
```

## Security Best Practices
1. Never commit API keys directly - always use GitHub Secrets
2. Review Claude's suggestions before merging
3. Consider limiting auto-review to certain file types or directories
4. Set appropriate timeout limits in workflows (default: 60 minutes)

## Additional Resources
- [Official claude-code-action repository](https://github.com/anthropics/claude-code-action)
- [Example workflows](https://github.com/anthropics/claude-code-action/tree/main/examples)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Anthropic API documentation](https://docs.anthropic.com/)

## Why Manual Setup?
The `/install-github-app` command mentioned in official docs often fails with 404 errors. This manual approach:
- Gives you full control over the configuration
- Works reliably without app installation
- Allows customization for your specific language/framework
- Provides transparency into what's being set up

---
*Last tested: 2025-08-09 with claude-code-action@beta*