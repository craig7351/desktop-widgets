@echo off
echo Starting Desktop Widget...
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call .\venv\Scripts\activate
    echo Installing dependencies...
    pip install PyQt6 requests
) else (
    call .\venv\Scripts\activate
)

start "" /b pythonw main.py
echo Widget is running in the background.
exit
