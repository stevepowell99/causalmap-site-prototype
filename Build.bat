@echo off
cd /d "%~dp0"

REM Install required Python packages if needed.
py -c "import yaml, markdown" 1>nul 2>nul
if errorlevel 1 (
    py -m pip install pyyaml markdown
)

REM One-off build into dist/.
py build.py

pause
