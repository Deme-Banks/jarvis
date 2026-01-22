# PowerShell script to push JARVIS to GitHub
# Run this script from the jarvis-voice-system directory

Write-Host "=== JARVIS GitHub Push Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "jarvis_pi.py")) {
    Write-Host "ERROR: Not in jarvis-voice-system directory" -ForegroundColor Red
    Write-Host "Please run this script from the jarvis-voice-system folder" -ForegroundColor Yellow
    exit 1
}

Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init

Write-Host "Adding remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Deme-Banks/jarvis.git

Write-Host "Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: JARVIS Voice Assistant with cybersecurity module

Features:
- Voice-first multi-agent AI assistant
- Raspberry Pi optimized with local LLM support
- Cybersecurity testing module for VSOC
- Natural language processing
- VSOC integration and reporting
- Advanced DDoS and malware testing tools"

Write-Host ""
Write-Host "Ready to push!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Ensure you're authenticated with GitHub" -ForegroundColor White
Write-Host "2. Run: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "If you need to authenticate:" -ForegroundColor Yellow
Write-Host "  - Use Personal Access Token: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "  - Or use: gh auth login (if GitHub CLI is installed)" -ForegroundColor White
Write-Host ""

$push = Read-Host "Push to GitHub now? (y/n)"
if ($push -eq "y" -or $push -eq "Y") {
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    git branch -M main
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "Repository: https://github.com/Deme-Banks/jarvis" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "Push failed. Check authentication or run manually:" -ForegroundColor Red
        Write-Host "  git push -u origin main" -ForegroundColor Yellow
    }
} else {
    Write-Host "Skipped push. Run 'git push -u origin main' when ready." -ForegroundColor Yellow
}
