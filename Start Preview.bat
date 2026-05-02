@echo off
cd /d "%~dp0"

REM Install required Python packages if needed.
py -c "import yaml, markdown, livereload" 1>nul 2>nul
if errorlevel 1 (
    py -m pip install pyyaml markdown livereload
)

REM Start the live preview server.
echo Press Ctrl+C to stop the preview server, or close this window.
py preview.py

pause
