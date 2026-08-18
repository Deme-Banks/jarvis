# JARVIS Voice System - Startup Script
# Ensures everything is installed and optionally starts JARVIS

param(
    [switch]$SkipSetup,      # Skip environment setup
    [switch]$SkipInstall,    # Skip package installation
    [switch]$SkipEnvCheck,   # Skip .env file check
    [switch]$AutoStart,      # Automatically start JARVIS after setup
    [string]$Mode = "ui",    # Mode: ui (window), text, voice
    [switch]$Help            # Show help
)

# Colors
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $InfoColor
    Write-Host $Text -ForegroundColor $InfoColor
    Write-Host "========================================" -ForegroundColor $InfoColor
    Write-Host ""
}

function Write-Step {
    param([string]$Text)
    Write-Host "→ $Text" -ForegroundColor $InfoColor
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor $SuccessColor
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor $WarningColor
}

function Write-Error {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor $ErrorColor
}

function Exit-WithPause {
    param([int]$ExitCode = 1)
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor $InfoColor
    try {
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } catch {
        # If ReadKey fails, use Read-Host as fallback
        Read-Host "Press Enter to exit"
    }
    exit $ExitCode
}

function Show-Help {
    Write-Header "JARVIS Startup Script - Help"
    Write-Host "Usage: .\start_jarvis.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -SkipSetup      Skip virtual environment setup"
    Write-Host "  -SkipInstall    Skip package installation"
    Write-Host "  -SkipEnvCheck   Skip .env file validation"
    Write-Host "  -AutoStart      Automatically start JARVIS after setup"
    Write-Host '  -Mode [mode]    text (Ollama REPL, default), pi (voice), learning'
    Write-Host "  -Help           Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\start_jarvis.ps1                    # Full setup and manual start"
    Write-Host "  .\start_jarvis.ps1 -AutoStart         # Setup and auto-start"
    Write-Host "  .\start_jarvis.ps1 -AutoStart -Mode text  # Ollama text REPL (no microphone)"
    Write-Host "  .\start_jarvis.ps1 -SkipSetup         # Skip setup, just start"
    Write-Host "  .\start_jarvis.ps1 -Mode learning     # Start in learning mode"
    Write-Host ""
}

if ($Help) {
    Show-Help
    exit 0
}

# Change to script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Ollama CLI is often installed but missing from PATH until a new login
$ollamaBin = Join-Path $env:LOCALAPPDATA "Programs\Ollama"
if (Test-Path (Join-Path $ollamaBin "ollama.exe")) {
    if ($env:Path -notlike "*Ollama*") {
        $env:Path = "$ollamaBin;$env:Path"
    }
}

Write-Header "JARVIS Voice System - Startup"

# ============================================================================
# Step 1: Check Python (always needed)
# ============================================================================
Write-Step "Checking Python installation..."

$pythonExe = $null

# Try py first (Python launcher, more reliable on Windows)
$testOutput = & py --version 2>&1
if ($LASTEXITCODE -eq 0 -and $testOutput -match "Python") {
    $pythonExe = "py"
} else {
    # Try python command
    $testOutput = & python --version 2>&1
    if ($LASTEXITCODE -eq 0 -and $testOutput -match "Python") {
        $pythonExe = "python"
    }
}

if (-not $pythonExe) {
    Write-Error "Python not found!"
    Write-Host "Please install Python 3.13+ from: https://www.python.org/downloads/" -ForegroundColor $WarningColor
    Write-Host "Or use the Python launcher (py) from Microsoft Store." -ForegroundColor $WarningColor
    Exit-WithPause 1
}

# Get Python version
$versionOutput = & $pythonExe --version 2>&1
if ($versionOutput -match "Python") {
    Write-Success "Found: $versionOutput"
} else {
    Write-Error "Python version check failed! Output: $versionOutput"
    Exit-WithPause 1
}

# Verify version is 3.13+
$versionMatch = $versionOutput -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 13)) {
        Write-Warning "Python 3.13+ recommended. Current: $versionOutput"
    }
}

# ============================================================================
# Step 2: Setup Virtual Environment
# ============================================================================
if (-not $SkipSetup) {
    Write-Step "Setting up virtual environment..."
    
    # Use 'venv' instead of 'venv' to avoid conflicts with locked old venv
    $venvPath = "venv"
    $venvPython = "$venvPath\Scripts\python.exe"
    
    if (Test-Path $venvPath) {
        if (Test-Path $venvPython) {
            # Test if the venv Python actually works
            $testVenv = & $venvPython --version 2>&1
            if ($testVenv -match "Python") {
                Write-Success "Virtual environment already exists and is valid"
            } else {
                Write-Warning "Virtual environment exists but appears corrupted, recreating..."
                Remove-Item -Recurse -Force $venvPath -ErrorAction SilentlyContinue
                & $pythonExe -m venv $venvPath 2>&1 | Out-Null
                if (Test-Path $venvPython) {
                    Write-Success "Virtual environment recreated"
                } else {
                    Write-Warning "Virtual environment creation had warnings, but continuing..."
                }
            }
        } else {
            Write-Warning "Virtual environment incomplete, recreating..."
            Remove-Item -Recurse -Force $venvPath -ErrorAction SilentlyContinue
            & $pythonExe -m venv $venvPath --prompt JARVIS 2>&1 | Out-Null
            if (Test-Path $venvPython) {
                # Ensure pip is available
                & $venvPython -m ensurepip --upgrade 2>&1 | Out-Null
                Write-Success "Virtual environment recreated"
            } else {
                Write-Error "Failed to create virtual environment"
                Exit-WithPause 1
            }
        }
    } else {
        & $pythonExe -m venv $venvPath --prompt JARVIS 2>&1 | Out-Null
        if (Test-Path $venvPython) {
            # Ensure pip is available
            & $venvPython -m ensurepip --upgrade 2>&1 | Out-Null
            Write-Success "Virtual environment created"
            } else {
                Write-Error "Failed to create virtual environment"
                Exit-WithPause 1
            }
    }
    
    # Verify venv Python exists
    if (-not (Test-Path $venvPython)) {
        Write-Error "Virtual environment Python not found at: $venvPython"
        Write-Host "Attempting to create virtual environment..." -ForegroundColor $WarningColor
        & $pythonExe -m venv $venvPath --prompt JARVIS 2>&1 | Out-Null
        if (Test-Path $venvPython) {
            & $venvPython -m ensurepip --upgrade 2>&1 | Out-Null
            Write-Success "Virtual environment created"
        } else {
            Exit-WithPause 1
        }
    }
}

# ============================================================================
# Step 3: Install/Update Packages
# ============================================================================
if (-not $SkipInstall) {
    Write-Step "Installing/updating packages..."
    
    $venvPython = "venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Warning "Virtual environment not found. Creating it now..."
        if (-not $SkipSetup) {
            # Try to create venv
            & $pythonExe -m venv venv --prompt JARVIS 2>&1 | Out-Null
            if (Test-Path $venvPython) {
                & $venvPython -m ensurepip --upgrade 2>&1 | Out-Null
                Write-Success "Virtual environment created"
            } else {
                Write-Error "Failed to create virtual environment. Please run: .\start_jarvis.ps1 (without -SkipSetup)"
                Exit-WithPause 1
            }
        } else {
            Write-Error "Virtual environment not found. Run without -SkipSetup first."
            Exit-WithPause 1
        }
    }
    
    # Ensure pip is installed first
    Write-Host "  Ensuring pip is installed..." -ForegroundColor $InfoColor
    $pipTest = & $venvPython -m pip --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "pip not found in venv, installing via get-pip.py..."
        
        # Download and install pip using get-pip.py (most reliable method)
        $getPipPath = "$env:TEMP\get-pip-jarvis-$(Get-Random).py"
        try {
            $ProgressPreference = 'SilentlyContinue'
            Write-Host "    Downloading get-pip.py..." -ForegroundColor $InfoColor
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile("https://bootstrap.pypa.io/get-pip.py", $getPipPath)
            
            Write-Host "    Installing pip (this may take a moment)..." -ForegroundColor $InfoColor
            $pipInstallOutput = & $venvPython $getPipPath 2>&1
            $pipInstallSuccess = $LASTEXITCODE -eq 0
            
            # Clean up
            Remove-Item $getPipPath -ErrorAction SilentlyContinue
            
            # Verify pip is now installed
            if ($pipInstallSuccess) {
                $pipTest2 = & $venvPython -m pip --version 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "pip installed successfully"
                } else {
                    Write-Warning "pip installation completed but verification failed"
                }
            } else {
                Write-Warning "pip installation had errors, but continuing..."
                Write-Host "    Output: $($pipInstallOutput -join ' ')" -ForegroundColor Gray
            }
        } catch {
            Write-Warning "Could not install pip automatically: $_"
            Write-Host "    The virtual environment may need to be recreated." -ForegroundColor $WarningColor
            Write-Host "    Try: Remove-Item -Recurse -Force venv; .\start_jarvis.ps1" -ForegroundColor White
            Write-Host "    Or run: .\fix_pyaudio.ps1 and choose option 2" -ForegroundColor White
        }
    } else {
        Write-Success "pip is available"
    }
    
    # Fix pip configuration (remove no-index and proxy issues)
    # Run fix_network.ps1 if it exists to handle network issues
    if (Test-Path "fix_network.ps1") {
        & .\fix_network.ps1 | Out-Null
    }
    
    # PIP_NO_INDEX prevents pip from accessing PyPI - must be removed
    [Environment]::SetEnvironmentVariable("PIP_NO_INDEX", $null, "Process")
    Remove-Item Env:\PIP_NO_INDEX -ErrorAction SilentlyContinue
    Remove-Item Env:\PIP_INDEX_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\PIP_DISABLE_PIP_VERSION_CHECK -ErrorAction SilentlyContinue
    # Disable proxy completely - clear all proxy variables
    Remove-Item Env:\HTTP_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\HTTPS_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\http_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:\https_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:\ALL_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\all_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:\NO_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\no_proxy -ErrorAction SilentlyContinue
    # Clear git proxy settings that might interfere
    Remove-Item Env:\GIT_HTTP_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\GIT_HTTPS_PROXY -ErrorAction SilentlyContinue
    
    # Upgrade pip
    Write-Host "  Upgrading pip..." -ForegroundColor $InfoColor
    & $venvPython -m pip install --upgrade pip --quiet 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "pip ready"
    } else {
        Write-Warning "pip upgrade had issues, continuing..."
    }
    
    # Check if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host "  Installing requirements..." -ForegroundColor $InfoColor
        Write-Host "    This may take several minutes, especially for PyAudio..." -ForegroundColor $WarningColor
        
        # Try installing PyAudio separately first (it's often problematic on Windows)
        Write-Host "    Installing PyAudio (may require C++ build tools)..." -ForegroundColor $InfoColor
        & $venvPython -m pip install pyaudio 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "PyAudio installation failed. Trying alternative method..."
            Write-Host "    Attempting to install PyAudio from pre-built wheel..." -ForegroundColor $InfoColor
            # Try installing from a wheel or alternative source
            & $venvPython -m pip install pipwin 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                & $venvPython -m pipwin install pyaudio 2>&1 | Out-Null
            }
        }
        
        # Install all other requirements
        Write-Host "  Installing packages from requirements.txt..." -ForegroundColor $InfoColor
        # Ensure pip can access PyPI (fix no-index and proxy configuration)
        [Environment]::SetEnvironmentVariable("PIP_NO_INDEX", $null, "Process")
        Remove-Item Env:\PIP_NO_INDEX -ErrorAction SilentlyContinue
        Remove-Item Env:\PIP_INDEX_URL -ErrorAction SilentlyContinue
        # Clear all proxy variables
        Remove-Item Env:\HTTP_PROXY -ErrorAction SilentlyContinue
        Remove-Item Env:\HTTPS_PROXY -ErrorAction SilentlyContinue
        Remove-Item Env:\http_proxy -ErrorAction SilentlyContinue
        Remove-Item Env:\https_proxy -ErrorAction SilentlyContinue
        Remove-Item Env:\ALL_PROXY -ErrorAction SilentlyContinue
        Remove-Item Env:\all_proxy -ErrorAction SilentlyContinue
        Remove-Item Env:\GIT_HTTP_PROXY -ErrorAction SilentlyContinue
        Remove-Item Env:\GIT_HTTPS_PROXY -ErrorAction SilentlyContinue
        
        # Try installing with proxy disabled and direct connection
        Write-Host "  Attempting package installation (this may take a few minutes)..." -ForegroundColor $InfoColor
        Write-Host "  Note: If this fails, check FIX_PIP_PROXY.md for network/proxy issues" -ForegroundColor $WarningColor
        
        # Try multiple methods to bypass proxy issues
        # Method 1: Disable proxy completely and use pip.ini config
        $pipOutput = & $venvPython -m pip install --proxy="" --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 2>&1
        $pipExitCode = $LASTEXITCODE
        
        # If permission error, try with different temp directory
        if ($pipOutput -match "Permission denied|OSError.*13") {
            Write-Host "  Permission issue detected, trying with different temp directory..." -ForegroundColor $InfoColor
            $oldTemp = $env:TEMP
            $env:TEMP = "$env:USERPROFILE\AppData\Local\Temp\pip-install"
            New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
            $pipOutput = & $venvPython -m pip install --proxy="" --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 2>&1
            $pipExitCode = $LASTEXITCODE
            $env:TEMP = $oldTemp
        }
        
        # Method 2: Try with index URL explicitly set
        if ($pipExitCode -ne 0) {
            Write-Host "  Retrying with explicit PyPI index..." -ForegroundColor $InfoColor
            $pipOutput = & $venvPython -m pip install --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 2>&1
            $pipExitCode = $LASTEXITCODE
        }
        
        # Method 3: Try without proxy flag
        if ($pipExitCode -ne 0) {
            Write-Host "  Retrying with default settings..." -ForegroundColor $InfoColor
            $pipOutput = & $venvPython -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 2>&1
            $pipExitCode = $LASTEXITCODE
        }
        
        # If still failing, show detailed error and offer fix script
        if ($pipExitCode -ne 0) {
            $errorMsg = $pipOutput -join "`n"
            if ($errorMsg -match "ProxyError|proxy") {
                Write-Host "  Proxy configuration issue detected!" -ForegroundColor $ErrorColor
                Write-Host ""
                Write-Host "  Quick fix: Run .\fix_network.ps1" -ForegroundColor $InfoColor
                Write-Host "  Or see NETWORK_ISSUE_SUMMARY.md for detailed solutions" -ForegroundColor $WarningColor
                Write-Host ""
                Write-Host "  The issue is: Proxy is configured but not working" -ForegroundColor $WarningColor
                Write-Host "  You may need to:" -ForegroundColor $InfoColor
                Write-Host "    1. Run PowerShell as Administrator" -ForegroundColor White
                Write-Host "    2. Run: netsh winhttp reset proxy" -ForegroundColor White
                Write-Host "    3. Or disable proxy in Windows Settings > Network & Internet > Proxy" -ForegroundColor White
            } elseif ($errorMsg -match "PIP_NO_INDEX|no-index") {
                Write-Host "  PIP_NO_INDEX is still set!" -ForegroundColor $ErrorColor
                Write-Host "  Run: .\fix_network.ps1 to fix this" -ForegroundColor $InfoColor
            } else {
                Write-Host "  Package installation failed. See errors above." -ForegroundColor $WarningColor
                Write-Host "  Try running: .\fix_network.ps1" -ForegroundColor $InfoColor
            }
        }
        
        if ($pipExitCode -eq 0) {
            Write-Success "All packages installed"
        } else {
            # Check if it's a network/PyPI issue
            $pipError = $pipOutput -join " "
            if ($pipError -match "Could not find a version" -or $pipError -match "No matching distribution") {
                Write-Warning "Package installation failed - possible network/PyPI issue"
                Write-Host "  Error: Could not find packages on PyPI" -ForegroundColor $WarningColor
                Write-Host "  This might be a network issue or Python 3.14 compatibility problem" -ForegroundColor $WarningColor
                Write-Host "  Try:" -ForegroundColor $InfoColor
                Write-Host "    1. Check your internet connection" -ForegroundColor White
                Write-Host "    2. Try: .\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel" -ForegroundColor White
                Write-Host "    3. Or install Python 3.12 for better package support" -ForegroundColor White
            } else {
                Write-Warning "Some packages may have failed to install"
                Write-Host "  Check errors above. You may need to install PyAudio manually:" -ForegroundColor $WarningColor
                Write-Host "    Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor White
                Write-Host "    Or install Visual C++ Build Tools from Microsoft" -ForegroundColor White
            }
        }
    } else {
        Write-Warning "requirements.txt not found, skipping package installation"
    }
}

# ============================================================================
# Step 4: Check Environment Variables
# ============================================================================
if (-not $SkipEnvCheck) {
    Write-Step "Checking environment configuration..."
    
    if (Test-Path ".env") {
        Write-Success ".env file exists"
        
        # Check for critical variables (optional check)
        $envContent = Get-Content ".env" -Raw
        $hasOpenAI = $envContent -match "OPENAI_API_KEY=(?!your_|$)"
        $hasGemini = $envContent -match "GEMINI_API_KEY=(?!your_|$)"
        
        if (-not $hasOpenAI -and -not $hasGemini) {
            Write-Warning "No API keys configured in .env"
            Write-Host "  JARVIS can work with local LLM (Ollama) without API keys" -ForegroundColor $InfoColor
            Write-Host "  For cloud LLM features, configure API keys in .env" -ForegroundColor $InfoColor
        } else {
            Write-Success "API keys configured"
        }
    } else {
        Write-Warning ".env file not found"
        if (Test-Path ".env.example") {
            Write-Host "  Copy .env.example to .env and configure your settings" -ForegroundColor $InfoColor
            Write-Host "  JARVIS can work with local LLM (Ollama) without .env" -ForegroundColor $InfoColor
        }
    }
}

# ============================================================================
# Step 5: Verify Installation
# ============================================================================
Write-Step "Verifying installation..."

$venvPython = "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Warning "Virtual environment not found at: $venvPython"
    Write-Host "Please run: .\start_jarvis.ps1 (without -SkipSetup)" -ForegroundColor $WarningColor
    Exit-WithPause 1
}

if (Test-Path $venvPython) {
    # Test critical imports
    $testImports = @("sys", "os")
    $allGood = $true
    
    foreach ($module in $testImports) {
        & $venvPython -c "import $module" 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed to import $module"
            $allGood = $false
        }
    }
    
    if ($allGood) {
        Write-Success "Python environment verified"
    }
} else {
    Write-Warning "Cannot verify - virtual environment not found"
}

# ============================================================================
# Step 6: Ensure Virtual Environment Exists (if starting)
# ============================================================================
$venvPython = "venv\Scripts\python.exe"

# If auto-starting, make sure venv exists
if ($AutoStart) {
    if (-not (Test-Path $venvPython)) {
        Write-Warning "Virtual environment not found. Creating it now..."
        if (-not $SkipSetup) {
            & $pythonExe -m venv venv --prompt JARVIS 2>&1 | Out-Null
            if (Test-Path $venvPython) {
                & $venvPython -m ensurepip --upgrade 2>&1 | Out-Null
                Write-Success "Virtual environment created"
            } else {
                Write-Error "Failed to create virtual environment"
                Exit-WithPause 1
            }
        } else {
            Write-Error "Virtual environment not found and -SkipSetup is enabled"
            Write-Host "Run: .\start_jarvis.ps1 (without -SkipSetup) to create the environment" -ForegroundColor $WarningColor
            Exit-WithPause 1
        }
    }
}

# Check Critical Dependencies (if starting)
$pyaudioOk = $false
$wantVoice = $AutoStart -and ($Mode.ToLower() -eq "pi")
if ($wantVoice -and (Test-Path $venvPython)) {
    Write-Step "Checking critical dependencies..."
    
    $missingDeps = @()
    
    # Check pyaudio (most common issue for voice mode)
    $pyaudioCheck = & $venvPython -c "import pyaudio" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingDeps += "pyaudio"
    } else {
        $pyaudioOk = $true
    }
    
    if ($missingDeps.Count -gt 0) {
        Write-Warning "Missing critical dependencies: $($missingDeps -join ', ')"
        Write-Host ""
        
        if ($missingDeps -contains "pyaudio") {
            Write-Host "Attempting to install PyAudio..." -ForegroundColor $InfoColor
            if (Test-Path "install_pyaudio.ps1") {
                & .\install_pyaudio.ps1
            } else {
                # Try direct installation
                Write-Host "  Trying pipwin method..." -ForegroundColor $InfoColor
                & $venvPython -m pip install pipwin 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    & $venvPython -m pipwin install pyaudio 2>&1
                }
                
                # If that failed, try direct install
                if ($LASTEXITCODE -ne 0) {
                    & $venvPython -m pip install pyaudio 2>&1
                }
            }
            
            # Check again
            $pyaudioCheck2 = & $venvPython -c "import pyaudio" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "PyAudio installed successfully!"
                $pyaudioOk = $true
            } else {
                Write-Host ""
                Write-Warning "PyAudio is not available. Voice mode needs a microphone stack."
                Write-Host "  Falling back to text mode (Ollama REPL). See OLLAMA.md" -ForegroundColor $InfoColor
                Write-Host "  Manual install later: .\install_pyaudio.ps1" -ForegroundColor White
                if ($Mode.ToLower() -eq "pi") {
                    $Mode = "text"
                }
            }
        }
        
        Write-Success "Critical dependencies available"
    } else {
        Write-Success "Critical dependencies available"
    }
}

# ============================================================================
# Step 7: Determine JARVIS Entry Point
# ============================================================================
$jarvisScript = "run.py"
$jarvisArgs = switch ($Mode.ToLower()) {
    "voice" { "voice" }
    "pi" { "voice" }
    "text" { "text" }
    default { "ui" }
}

if (-not (Test-Path $jarvisScript)) {
    Write-Error "JARVIS script not found: $jarvisScript"
    Write-Host "Available scripts:" -ForegroundColor $InfoColor
    Get-ChildItem -Filter "jarvis*.py" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor $InfoColor }
    Exit-WithPause 1
}

# ============================================================================
# Step 8: Start JARVIS (if requested)
# ============================================================================
Write-Header "Setup Complete!"

Write-Host "Virtual Environment:" -ForegroundColor $InfoColor
Write-Host "  Location: venv" -ForegroundColor White
Write-Host "  Activate: venv\Scripts\activate" -ForegroundColor White
Write-Host ""

Write-Host "JARVIS Script:" -ForegroundColor $InfoColor
Write-Host "  Mode: $Mode" -ForegroundColor White
    Write-Host "  Script: $jarvisScript $jarvisArgs" -ForegroundColor White
Write-Host ""

if ($AutoStart) {
    # Final check before starting
    if (-not (Test-Path $venvPython)) {
        Write-Error "Virtual environment Python not found: $venvPython"
        Write-Host "Please run: .\start_jarvis.ps1 (without -SkipSetup) to create the environment" -ForegroundColor $WarningColor
        Exit-WithPause 1
    }
    
    Write-Step "Starting JARVIS..."
    Write-Host "Press Ctrl+C to stop" -ForegroundColor $WarningColor
    Write-Host ""
    
    # Run JARVIS and capture output/errors
    try {
        & $venvPython $jarvisScript $jarvisArgs 2>&1
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -ne 0) {
            Write-Host ""
            Write-Error "JARVIS exited with error code: $exitCode"
            Write-Host "Check the error messages above for details." -ForegroundColor $WarningColor
            Write-Host ""
            Write-Host "Press any key to exit..." -ForegroundColor $InfoColor
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    } catch {
        Write-Host ""
        Write-Error "Failed to start JARVIS: $_"
        Write-Host ""
        Write-Host "Common issues:" -ForegroundColor $WarningColor
        Write-Host "  - Missing dependencies: Run .\start_jarvis.ps1 (without -SkipInstall)" -ForegroundColor White
        Write-Host "  - Configuration error: Check config_pi.py and .env files" -ForegroundColor White
        Write-Host "  - Audio device issues: Check microphone/audio settings" -ForegroundColor White
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor $InfoColor
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
} else {
    Write-Host "To start JARVIS in text mode (Ollama, no microphone):" -ForegroundColor $InfoColor
    Write-Host "  venv\Scripts\python.exe run.py text" -ForegroundColor White
    Write-Host ""
    Write-Host "Voice mode:" -ForegroundColor $InfoColor
    Write-Host "  venv\Scripts\python.exe run.py voice" -ForegroundColor White
    Write-Host ""
    Write-Host "Or: .\start_jarvis.ps1 -AutoStart -Mode text" -ForegroundColor $InfoColor
    Write-Host "Offline LLM setup: see docs\OLLAMA.md" -ForegroundColor $InfoColor
}
