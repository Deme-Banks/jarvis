# Setup Python 3.12 for JARVIS (Windows)
# This script helps install Python 3.12 or compile PyAudio for Python 3.14

Write-Host "JARVIS Python 3.12 Setup" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

# Check current Python
$currentPython = & py --version 2>&1
Write-Host "Current Python: $currentPython" -ForegroundColor Cyan
Write-Host ""

# Option 1: Download Python 3.12 Windows installer
Write-Host "Option 1: Download Python 3.12 Windows Installer" -ForegroundColor Yellow
Write-Host "  This is the easiest option - gets you a working Python 3.12 with PyAudio support" -ForegroundColor White
Write-Host ""
Write-Host "  Would you like to download Python 3.12.11 Windows installer? (Y/N)" -ForegroundColor Cyan
$download = Read-Host

if ($download -eq "Y" -or $download -eq "y") {
    Write-Host ""
    Write-Host "Downloading Python 3.12.11 Windows 64-bit installer..." -ForegroundColor Cyan
    
    $python312Url = "https://www.python.org/ftp/python/3.12.11/python-3.12.11-amd64.exe"
    $installerPath = "$env:USERPROFILE\Downloads\python-3.12.11-amd64.exe"
    
    try {
        Invoke-WebRequest -Uri $python312Url -OutFile $installerPath
        Write-Host ""
        Write-Host "SUCCESS: Download complete!" -ForegroundColor Green
        Write-Host "  Installer saved to: $installerPath" -ForegroundColor White
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Run the installer: $installerPath" -ForegroundColor White
        Write-Host "  2. IMPORTANT: Check 'Add Python 3.12 to PATH' during installation" -ForegroundColor White
        Write-Host "  3. After installation, run: .\start_jarvis.ps1" -ForegroundColor White
        Write-Host ""
        Write-Host "Would you like to run the installer now? (Y/N)" -ForegroundColor Cyan
        $runInstaller = Read-Host
        if ($runInstaller -eq "Y" -or $runInstaller -eq "y") {
            Start-Process $installerPath
        }
    } catch {
        Write-Host ""
        Write-Host "ERROR: Download failed: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manual download:" -ForegroundColor Yellow
        Write-Host "  Go to: https://www.python.org/downloads/release/python-31211/" -ForegroundColor White
        Write-Host "  Download: Windows installer (64-bit)" -ForegroundColor White
    }
    exit 0
}

# Option 2: Compile PyAudio from source (if C++ tools available)
Write-Host ""
Write-Host "Option 2: Compile PyAudio from source using C++ tools" -ForegroundColor Yellow
Write-Host "  This will compile PyAudio for your current Python 3.14" -ForegroundColor White
Write-Host ""

# Check for C++ compiler
$hasCl = Get-Command cl -ErrorAction SilentlyContinue
$hasGcc = Get-Command gcc -ErrorAction SilentlyContinue

if (-not $hasCl -and -not $hasGcc) {
    Write-Host "WARNING: C++ compiler not found in PATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To use this option, you need:" -ForegroundColor Cyan
    Write-Host "  1. Visual Studio Build Tools installed" -ForegroundColor White
    Write-Host "  2. Run from 'Developer Command Prompt for VS' or" -ForegroundColor White
    Write-Host "  3. Run: vcvars64.bat to set up the environment" -ForegroundColor White
    Write-Host ""
    Write-Host "Would you like to try compiling anyway? (Y/N)" -ForegroundColor Cyan
    $tryCompile = Read-Host
    if ($tryCompile -ne "Y" -and $tryCompile -ne "y") {
        exit 0
    }
}

Write-Host "Attempting to compile PyAudio from source..." -ForegroundColor Cyan
Write-Host ""

# First, we need to fix the venv pip issue
Write-Host "Step 1: Fixing virtual environment..." -ForegroundColor Cyan
Write-Host "  Recreating venv without pip issues..." -ForegroundColor White

if (Test-Path "venv313") {
    Remove-Item -Recurse -Force venv313 -ErrorAction SilentlyContinue
}

# Create venv without pip first
py -m venv venv313 --without-pip 2>&1 | Out-Null

# Install pip using get-pip.py
Write-Host "  Installing pip..." -ForegroundColor White
$getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
$getPipPath = "$env:TEMP\get-pip-jarvis.py"

try {
    # Try downloading get-pip.py
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($getPipUrl, $getPipPath)
    
    & .\venv313\Scripts\python.exe $getPipPath 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ pip installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ pip installation had issues" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Could not download get-pip.py" -ForegroundColor Red
    Write-Host "  Manual step: Download get-pip.py and run it in the venv" -ForegroundColor Yellow
}

# Now try to install PyAudio
Write-Host ""
Write-Host "Step 2: Installing build dependencies..." -ForegroundColor Cyan
& .\venv313\Scripts\python.exe -m pip install --upgrade pip setuptools wheel 2>&1 | Out-Null

Write-Host ""
Write-Host "Step 3: Installing PyAudio (this will compile from source)..." -ForegroundColor Cyan
Write-Host "  This may take 5-10 minutes..." -ForegroundColor Yellow

& .\venv313\Scripts\python.exe -m pip install pyaudio 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: PyAudio installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run: .\start_jarvis.ps1 -AutoStart" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "PyAudio compilation failed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Missing C++ compiler: Install Visual Studio Build Tools" -ForegroundColor White
    Write-Host "  - Missing PortAudio: PyAudio requires PortAudio library" -ForegroundColor White
    Write-Host ""
    Write-Host "Recommendation: Use Option 1 (Python 3.12 installer) for easier setup" -ForegroundColor Cyan
}
