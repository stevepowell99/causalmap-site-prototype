@echo off
cd /d "%~dp0"

REM Ensure Python 3 is available before installing packages.
call "%~dp0Ensure Python.bat"
if errorlevel 1 (
    pause
    exit /b 1
)

REM Install the pinned generator (sitegen) and its dependencies from requirements.txt.
"%PYTHON_EXE%" %PYTHON_ARGS% -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo Could not install requirements.txt; building with whatever sitegen is already installed.
)

REM One-off build into dist/.
"%PYTHON_EXE%" %PYTHON_ARGS% build.py

pause
