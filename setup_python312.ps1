# Setup Python 3.12 Virtual Environment for JARVIS
# Run this AFTER installing Python 3.12

Write-Host "JARVIS Python 3.12 Setup" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

# Check if Python 3.12 is available
$python312 = Get-Command py -ErrorAction SilentlyContinue
if (-not $python312) {
    Write-Host "ERROR: 'py' launcher not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.12 from: https://www.python.org/downloads/release/python-31211/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    exit 1
}

# Check Python 3.12 version
Write-Host "Checking Python 3.12..." -ForegroundColor Cyan
$version = & py -3.12 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.12 not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.12 from: https://www.python.org/downloads/release/python-31211/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    exit 1
}

Write-Host "Found: $version" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv312") {
    Write-Host "Virtual environment 'venv312' already exists." -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Remove-Item -Recurse -Force venv312
        & py -3.12 -m venv venv312
        Write-Host "Virtual environment created!" -ForegroundColor Green
    }
} else {
    & py -3.12 -m venv venv312
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

Write-Host ""

# Activate and install packages
Write-Host "Activating virtual environment and installing packages..." -ForegroundColor Cyan
Write-Host ""

& venv312\Scripts\activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "Installing requirements from requirements.txt..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
Write-Host ""

python -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use this environment:" -ForegroundColor Cyan
    Write-Host "  venv312\Scripts\activate" -ForegroundColor White
    Write-Host ""
    Write-Host "To verify PyAudio:" -ForegroundColor Cyan
    Write-Host "  python -c 'import pyaudio; print(\"✓ PyAudio installed!\")'" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Some packages failed to install." -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    exit 1
}
