# Setup Git and Push to GitHub

## Step 1: Install Git

### Windows (PowerShell as Administrator)
```powershell
# Option 1: Using winget
winget install Git.Git

# Option 2: Using Chocolatey
choco install git

# Option 3: Download installer
# Visit: https://git-scm.com/download/win
```

After installation, **restart your terminal/PowerShell**.

### Verify Installation
```powershell
git --version
```

## Step 2: Find Your Project Directory

The `jarvis-voice-system` folder should contain:
- `jarvis_pi.py`
- `config_pi.py`
- `requirements_pi.txt`
- `README.md`
- `cybersecurity/` folder
- etc.

Navigate to it:
```powershell
cd path\to\jarvis-voice-system
```

## Step 3: Configure Git (First Time Only)

```powershell
git config --global user.name "Deme-Banks"
git config --global user.email "your-email@example.com"
```

## Step 4: Initialize and Push

```powershell
# Initialize Git
git init

# Add remote repository
git remote add origin https://github.com/Deme-Banks/jarvis.git

# Add all files
git add .

# Create commit
git commit -m "Initial commit: JARVIS Voice Assistant with cybersecurity module"

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 5: Authentication

When prompted:
- **Username**: `Deme-Banks`
- **Password**: Use a **Personal Access Token** (NOT your GitHub password)

### Create Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "JARVIS Push"
4. Select scope: `repo` (full control)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)
7. Paste it as the password when pushing

## Alternative: Use GitHub Desktop

If you prefer a GUI:
1. Download: https://desktop.github.com/
2. Sign in with your GitHub account
3. Add repository: File → Add Local Repository
4. Select your `jarvis-voice-system` folder
5. Publish to GitHub

## Troubleshooting

### "Git not recognized"
- Install Git (see Step 1)
- Restart terminal after installation
- Check PATH: `$env:PATH -split ';' | Select-String git`

### "Authentication failed"
- Use Personal Access Token, not password
- Ensure token has `repo` scope
- Token may have expired - generate new one

### "Repository not found"
- Verify repository exists: https://github.com/Deme-Banks/jarvis
- Check repository name is correct
- Ensure you have push access

### "Remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/Deme-Banks/jarvis.git
```

---

**Once pushed, your repository will be live at:**
https://github.com/Deme-Banks/jarvis
