@echo off
cd /d "%~dp0"

REM Install the pinned generator (sitegen), its dependencies and livereload.
py -m pip install -q -r requirements.txt livereload
if errorlevel 1 (
    echo Could not install requirements.txt; previewing with whatever sitegen is already installed.
)

REM Start the live preview server.
echo Press Ctrl+C to stop the preview server, or close this window.
py preview.py

pause
