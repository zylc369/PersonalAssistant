@echo off
REM setup.bat - TTS CLI Setup Script for Windows
REM This script sets up the TTS CLI tool by checking Python, creating virtual environment, and installing dependencies

setlocal enabledelayedexpansion

echo ===================================
echo TTS CLI Setup Script
echo ===================================
echo.

REM Check if we're in the right directory
if not exist "tts_cli.py" (
    echo [ERROR] tts_cli.py not found in current directory
    echo [ERROR] Please run this script from the TTS tool directory
    pause
    exit /b 1
)

REM Check Python 3
echo [INFO] Checking Python 3 installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Found Python version: %PYTHON_VERSION%

REM Parse version to check if it's 3.8+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Check if Python 3.8 or higher
if %MAJOR% lss 3 (
    echo [ERROR] Python 3.8 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %MAJOR% equ 3 (
    if %MINOR% lss 8 (
        echo [ERROR] Python 3.8 or higher is required
        echo Current version: %PYTHON_VERSION%
        pause
        exit /b 1
    )
)

echo [SUCCESS] Python version check passed

REM Check if pip is available
python -c "import pip" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available for Python 3
    echo pip should be included with Python installation
    pause
    exit /b 1
)

REM Check for development dependencies
set INSTALL_DEV=false
if "%1"=="--dev" set INSTALL_DEV=true
if "%1"=="-d" set INSTALL_DEV=true

if "%INSTALL_DEV%"=="true" (
    echo [INFO] Will install development dependencies
)

REM Virtual environment path
set VENV_PATH=tts_venv

REM Create virtual environment
echo [INFO] Creating virtual environment at %VENV_PATH%...

if exist "%VENV_PATH%" (
    echo [WARNING] Virtual environment already exists. Recreating...
    rmdir /s /q "%VENV_PATH%"
)

python -m venv %VENV_PATH%
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment created successfully

REM Activate virtual environment and install dependencies
echo [INFO] Installing dependencies...

REM Activate virtual environment
call %VENV_PATH%\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
if exist "requirements.txt" (
    echo [INFO] Installing core dependencies from requirements.txt...
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo [ERROR] Failed to install core dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Core dependencies installed successfully
) else (
    echo [ERROR] requirements.txt not found
    pause
    exit /b 1
)

REM Install development dependencies if requested
if "%INSTALL_DEV%"=="true" (
    if exist "requirements-dev.txt" (
        echo [INFO] Installing development dependencies from requirements-dev.txt...
        pip install -r requirements-dev.txt
        
        if errorlevel 1 (
            echo [WARNING] Failed to install development dependencies (optional)
        ) else (
            echo [SUCCESS] Development dependencies installed successfully
        )
    )
)

REM Windows-specific checks
echo [INFO] Windows detected. Checking for additional dependencies...

REM Test the installation
echo [INFO] Testing TTS CLI installation...

python -c "
try:
    from TTS.api import TTS
    print('✓ TTS import successful')
except ImportError as e:
    print('✗ TTS import failed:', e)
    exit(1)

try:
    import torch
    print('✓ PyTorch import successful')
    print('✓ CUDA available:', torch.cuda.is_available())
except ImportError as e:
    print('✗ PyTorch import failed:', e)
    exit(1)
"

if errorlevel 1 (
    echo [ERROR] TTS CLI test failed
    pause
    exit /b 1
)

echo [SUCCESS] TTS CLI test passed

REM Create launcher script
echo [INFO] Creating launcher script...

REM Create Windows batch launcher
(
echo @echo off
echo REM TTS CLI Launcher for Windows
echo REM This script activates the virtual environment and runs tts_cli.py
echo.
echo REM Activate virtual environment
echo call %VENV_PATH%\Scripts\activate.bat
echo.
echo REM Run tts_cli.py with all arguments
echo python tts_cli.py %%*
) > tts.bat

if errorlevel 1 (
    echo [ERROR] Failed to create launcher script
    pause
    exit /b 1
)

echo [SUCCESS] Launcher script created successfully

REM Create PowerShell launcher
(
echo # TTS CLI Launcher for PowerShell
echo # This script activates the virtual environment and runs tts_cli.ps1
echo.
echo $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
echo $VenvPath = Join-Path $ScriptDir "%VENV_PATH%"
echo.
echo if ^(Test-Path $VenvPath^) {
echo     ^& "$VenvPath\Scripts\Activate.ps1"
echo     python (Join-Path $ScriptDir "tts_cli.py") $args
echo } else {
echo     Write-Error "Virtual environment not found at $VenvPath"
echo     Write-Error "Please run setup.bat first"
echo     exit 1
echo }
) > tts.ps1

echo.
echo [SUCCESS] Setup completed successfully!
echo.
echo === Usage Instructions ===
echo.
echo 1. Using the batch script ^(recommended^):
echo    tts.bat "Hello world"
echo.
echo 2. Using PowerShell:
echo    powershell -ExecutionPolicy Bypass -File tts.ps1 "Hello world"
echo.
echo 3. Manual usage:
echo    %VENV_PATH%\Scripts\activate.bat
echo    python tts_cli.py "Hello world"
echo.
echo 4. To see all options:
echo    tts.bat --help
echo.
echo 5. First time usage:
echo    tts.bat "Hello world"  REM This will download the TTS model
echo.
echo 6. To check model information:
echo    tts.bat --info
echo.
echo Notes:
echo - Models are downloaded automatically on first use
echo - Model location is displayed on each run
echo - For update checking, use: tts.bat "Hello world" --check-updates
echo.
pause