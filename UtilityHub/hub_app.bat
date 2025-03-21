@echo off
setlocal

echo Utility Hub Launcher
echo -----------------------

REM Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.6 or higher.
    pause
    exit /b 1
)

REM Check if running from the correct directory
if not exist "hub_app.py" (
    echo Error: hub_app.py not found in the current directory.
    echo Please run this batch file from the same directory as hub_app.py.
    pause
    exit /b 1
)

echo Starting Utility Hub...
echo.

REM Launch the application
python hub_app.py

REM Check if the application exited with an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Utility Hub exited with an error. Error code: %ERRORLEVEL%
    pause
)

endlocal