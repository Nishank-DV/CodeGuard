#!/bin/bash
# CodeGuard Phase 2 Quick Start Script

echo "🛡️  CodeGuard Phase 2 - Quick Start"
echo "=================================="
echo ""

# Check dependencies
echo "📋 Checking dependencies..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.10+"
    exit 1
fi

echo "✅ Node.js v$(node --version)"
echo "✅ Python v$(python --version)"
echo ""

# Setup backend
echo "🔧 Setting up backend..."
cd apps/api

if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    echo "Installing Poetry..."
    pip install poetry > /dev/null 2>&1
fi

echo "Installing Python dependencies..."
poetry install > /dev/null 2>&1

# Copy .env if needed
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "No .env.example file"
fi

cd ../..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd apps/web

echo "Installing Node dependencies..."
npm install > /dev/null 2>&1

# Copy .env if needed
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "No .env.example file"
fi

cd ../..

# Run tests
echo ""
echo "🧪 Running tests..."
cd apps/api

if command -v pytest &> /dev/null; then
    echo "Running Python tests..."
    poetry run pytest tests/ -q
else
    echo "⚠️  pytest not found, skipping tests"
fi

cd ../..

# Summary
echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 To get started:"
echo ""
echo "   # Terminal 1: Start backend API"
echo "   cd apps/api"
echo "   poetry run uvicorn main:app --reload"
echo ""
echo "   # Terminal 2: Start frontend"
echo "   cd apps/web"
echo "   npm run dev"
echo ""
echo "   # Visit the app"
echo "   http://localhost:5173"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Full project overview"
echo "   - docs/DETECTION_RULES.md - All 15 vulnerability rules"
echo "   - docs/API.md - API endpoint reference"
echo ""
echo "🚀 Happy analyzing! 🛡️"
