#!/bin/bash

# CodeGuard Quick Start Script
# This script sets up the entire CodeGuard development environment

set -e

echo "🛡️  CodeGuard - Setting up development environment..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Frontend Setup
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎨 Setting up Frontend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd apps/web

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
fi

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ node_modules already exists${NC}"
fi

cd ../..

# Backend Setup
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔧 Setting up Backend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd apps/api

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
fi

if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    pip install poetry
fi

if [ ! -d ".venv" ]; then
    echo "Installing dependencies with Poetry..."
    poetry install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

cd ../..

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "📝 Next Steps:"
echo ""
echo "1. Start the frontend (Terminal 1):"
echo -e "   ${YELLOW}cd apps/web && npm run dev${NC}"
echo ""
echo "2. Start the backend (Terminal 2):"
echo -e "   ${YELLOW}cd apps/api && poetry run uvicorn main:app --reload${NC}"
echo ""
echo "3. Open in browser:"
echo -e "   Frontend: ${YELLOW}http://localhost:5173${NC}"
echo -e "   Backend:  ${YELLOW}http://localhost:8000${NC}"
echo -e "   API Docs: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Project overview"
echo "   • docs/SETUP.md - Detailed setup guide"
echo "   • docs/ARCHITECTURE.md - System architecture"
echo "   • docs/DEPENDENCIES.md - All dependencies"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
