# Git Setup Instructions

## Prerequisites

1. **Install Git** (if not already installed):
   - Windows: Download from https://git-scm.com/download/win
   - Or use: `winget install Git.Git`

2. **Verify Git installation**:
   ```bash
   git --version
   ```

## Setup and Push to GitHub

### Step 1: Navigate to Project Directory
```bash
cd jarvis-voice-system
```

### Step 2: Initialize Git Repository
```bash
git init
```

### Step 3: Add Remote Repository
```bash
git remote add origin https://github.com/Deme-Banks/jarvis.git
```

### Step 4: Configure Git (if first time)
```bash
git config user.name "Deme-Banks"
git config user.email "your-email@example.com"
```

### Step 5: Add All Files
```bash
git add .
```

### Step 6: Create Initial Commit
```bash
git commit -m "Initial commit: JARVIS Voice Assistant with cybersecurity module"
```

### Step 7: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for GitHub credentials. Use:
- Personal Access Token (recommended) - Create at: https://github.com/settings/tokens
- Or GitHub username/password

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
gh repo create Deme-Banks/jarvis --public --source=. --remote=origin --push
```

## Troubleshooting

### If push is rejected:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### If authentication fails:
1. Generate Personal Access Token: https://github.com/settings/tokens
2. Use token as password when prompted
3. Or use SSH: `git remote set-url origin git@github.com:Deme-Banks/jarvis.git`

### Check remote:
```bash
git remote -v
```
