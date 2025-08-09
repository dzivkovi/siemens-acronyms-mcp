#!/bin/bash
# Useful aliases for Python development with virtual environments
# Source this file in your shell: source scripts/aliases.sh

# Virtual environment management
alias mkv='python -m venv venv'
alias va='source venv/bin/activate'
alias vd='deactivate'
alias vp='python -m pip install --upgrade pip'

# Quick setup sequence (run these in order):
# 1. mkv  - Create virtual environment
# 2. va   - Activate virtual environment  
# 3. vp   - Upgrade pip (IMPORTANT: do this before installing requirements)
# 4. pip install -r requirements.txt

# Lazy typing shortcut
alias l='ls -alrt'

# System monitoring (if available)
alias gpu='nvidia-smi'
alias gpuinfo='nvidia-smi -L'
alias meminfo='free -h'

echo "Aliases loaded! Quick setup:"
echo "  1. mkv  - Create virtual environment"
echo "  2. va   - Activate virtual environment"
echo "  3. vp   - Upgrade pip (important!)"
echo "  4. pip install -r requirements.txt"