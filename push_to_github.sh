#!/bin/bash
# Bash script to push JARVIS to GitHub
# Run this script from the jarvis-voice-system directory

echo "=== JARVIS GitHub Push Script ==="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    echo "Install Git: sudo apt-get install git"
    exit 1
fi

echo "Git found: $(git --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "jarvis_pi.py" ]; then
    echo "ERROR: Not in jarvis-voice-system directory"
    echo "Please run this script from the jarvis-voice-system folder"
    exit 1
fi

echo "Initializing Git repository..."
git init

echo "Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Deme-Banks/jarvis.git

echo "Adding all files..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit: JARVIS Voice Assistant with cybersecurity module

Features:
- Voice-first multi-agent AI assistant
- Raspberry Pi optimized with local LLM support
- Cybersecurity testing module for VSOC
- Natural language processing
- VSOC integration and reporting
- Advanced DDoS and malware testing tools"

echo ""
echo "Ready to push!"
echo ""
echo "Next steps:"
echo "1. Ensure you're authenticated with GitHub"
echo "2. Run: git push -u origin main"
echo ""
echo "If you need to authenticate:"
echo "  - Use Personal Access Token: https://github.com/settings/tokens"
echo "  - Or use: gh auth login (if GitHub CLI is installed)"
echo ""

read -p "Push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "Successfully pushed to GitHub!"
        echo "Repository: https://github.com/Deme-Banks/jarvis"
    else
        echo ""
        echo "Push failed. Check authentication or run manually:"
        echo "  git push -u origin main"
    fi
else
    echo "Skipped push. Run 'git push -u origin main' when ready."
fi
