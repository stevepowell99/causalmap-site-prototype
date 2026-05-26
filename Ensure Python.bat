@echo off

REM Find Python 3, installing it for the current user with winget if needed.
set "PYTHON_EXE="
set "PYTHON_ARGS="

where py 1>nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys" 1>nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=py"
        set "PYTHON_ARGS=-3"
    )
)

if not defined PYTHON_EXE if exist "%LocalAppData%\Programs\Python\Launcher\py.exe" (
    "%LocalAppData%\Programs\Python\Launcher\py.exe" -3 -c "import sys" 1>nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=%LocalAppData%\Programs\Python\Launcher\py.exe"
        set "PYTHON_ARGS=-3"
    )
)

if not defined PYTHON_EXE if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    "%LocalAppData%\Programs\Python\Python313\python.exe" -c "import sys" 1>nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe"
)

if not defined PYTHON_EXE (
    where python 1>nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if sys.version_info[0] == 3 else 1)" 1>nul 2>nul
        if not errorlevel 1 set "PYTHON_EXE=python"
    )
)

if defined PYTHON_EXE exit /b 0

where winget 1>nul 2>nul
if errorlevel 1 (
    echo Python 3 is required, and winget is not available to install it automatically.
    exit /b 1
)

echo Python 3 was not found. Installing it with winget...
winget install --id Python.Python.3.13 --exact --source winget --scope user --silent --accept-package-agreements --accept-source-agreements --disable-interactivity
if errorlevel 1 (
    echo Automatic Python install failed.
    exit /b 1
)

if exist "%LocalAppData%\Programs\Python\Launcher\py.exe" (
    "%LocalAppData%\Programs\Python\Launcher\py.exe" -3 -c "import sys" 1>nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=%LocalAppData%\Programs\Python\Launcher\py.exe"
        set "PYTHON_ARGS=-3"
    )
)

if not defined PYTHON_EXE if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    "%LocalAppData%\Programs\Python\Python313\python.exe" -c "import sys" 1>nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe"
)

if not defined PYTHON_EXE (
    where py 1>nul 2>nul
    if not errorlevel 1 (
        py -3 -c "import sys" 1>nul 2>nul
        if not errorlevel 1 (
            set "PYTHON_EXE=py"
            set "PYTHON_ARGS=-3"
        )
    )
)

if not defined PYTHON_EXE (
    echo Python was installed, but this command window cannot find it yet. Close this window and try again.
    exit /b 1
)

exit /b 0
