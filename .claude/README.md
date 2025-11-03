# Claude Code Custom Commands

This directory contains custom slash commands for Claude Code. Each `.md` file in the `commands/` subdirectory defines a reusable command.

## Available Commands

### From Anthropic Official Cookbooks

These commands are from [Anthropic's Claude Cookbooks](https://github.com/anthropics/claude-cookbooks/tree/main/.claude/commands):

- `/link-review` - Review links in changed files for quality and security issues
- `/model-check` - Validate Claude model usage against current public models
- `/notebook-review` - Comprehensive review of Jupyter notebooks and Python scripts

### Custom Commands

Remaining commands are custom for this project (based on [ai-strategy-consulting](https://github.com/dzivkovi/ai-strategy-consulting/tree/main/.claude)):

**Quick Saves:**
- `/save` - **FAST** smart save (Haiku-powered, saves to `work/`, auto-naming)
- `/note` - *Deprecated* (use `/save` instead - faster, cleaner, better organized)

**Workflow:**
- `/explore` - Chat about possible approaches
- `/issue` - Create GitHub issues (my take on [Compound Engineering](https://every.to/c/compounding-engineering))
- `/work` - Implement GitHub issue using TDD
- `/resume` - Continue interrupted work
- `/kanban` - Retroactive documentation for completed work
- `/reflection` - Improvement analysis (inspired by [https://reddit.com/r/ClaudeAI/comments/1laby6h/](https://reddit.com/r/ClaudeAI/comments/1laby6h/))

## Usage

Type any command in a Claude Code session. For example:
- `/save` - Save last response with smart filename
- `/save "your answer about git attributes"` - Save specific content
- `/notebook-review` - Review Jupyter notebooks (Anthropic command)
- `/explore how to add caching` - Explore implementation approaches
- `/issue 'Add rate limiting to API'` - Create GitHub issue
- `/work 42` - Implement issue #42
