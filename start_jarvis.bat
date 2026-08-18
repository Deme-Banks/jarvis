@echo off
REM Quick launcher for JARVIS (Windows Batch)
REM This calls the PowerShell script

powershell.exe -ExecutionPolicy Bypass -File "%~dp0start_jarvis.ps1" %*

REM If script exits with error, pause so user can see the message
if errorlevel 1 (
    echo.
    echo Script exited with an error. Check the messages above.
    pause
)
