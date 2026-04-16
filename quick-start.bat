@echo off
REM CodeGuard Phase 2 - Quick Start for Windows

echo.
echo 🛡️  CodeGuard Phase 2 - Quick Start
echo ===================================
echo.

REM Check Node.js
echo 📋 Checking dependencies...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found. Please install Node.js 18+
    exit /b 1
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i

echo ✅ Node.js %NODE_VER%
echo ✅ Python %PY_VER%
echo.

REM Setup backend
echo 🔧 Setting up backend...
cd apps\api

if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✅ Created .env file
    )
)

echo Installing Python dependencies...
pip install poetry >nul 2>&1
poetry install >nul 2>&1

cd ..\..

REM Setup frontend
echo.
echo 🎨 Setting up frontend...
cd apps\web

echo Installing Node dependencies...
call npm install >nul 2>&1

if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✅ Created .env file
    )
)

cd ..\..

REM Run tests
echo.
echo 🧪 Running tests...
cd apps\api
poetry run pytest tests\ -q 2>nul
cd ..\..

REM Summary
echo.
echo ✅ Setup complete!
echo.
echo 📖 To get started:
echo.
echo    1. Open PowerShell or Command Prompt (Terminal 1)
echo       cd apps\api
echo       poetry run uvicorn main:app --reload
echo.
echo    2. Open another PowerShell or Command Prompt (Terminal 2)
echo       cd apps\web
echo       npm run dev
echo.
echo    3. Visit the app
echo       http://localhost:5173
echo.
echo 📚 Documentation:
echo    - README.md - Full project overview
echo    - docs/DETECTION_RULES.md - All 15 vulnerability rules
echo    - docs/API.md - API endpoint reference
echo.
echo 🚀 Happy analyzing! 🛡️
echo.
pause
