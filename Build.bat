@echo off
cd /d "%~dp0"

REM Ensure Python 3 is available before installing packages.
call "%~dp0Ensure Python.bat"
if errorlevel 1 (
    pause
    exit /b 1
)

REM Install required Python packages if needed.
"%PYTHON_EXE%" %PYTHON_ARGS% -c "import yaml, markdown" 1>nul 2>nul
if errorlevel 1 (
    "%PYTHON_EXE%" %PYTHON_ARGS% -m pip install pyyaml markdown
)

REM One-off build into dist/.
"%PYTHON_EXE%" %PYTHON_ARGS% build.py

pause
