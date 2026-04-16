# Project Setup Guide

## Quick Start

### Option 1: Manual Setup

#### Frontend
```bash
cd apps/web
npm install
npm run dev
```

#### Backend
```bash
cd apps/api
pip install poetry
poetry install
poetry run uvicorn main:app --reload
```

### Option 2: Using Scripts (Coming Soon)

We'll provide shell scripts for one-command setup.

## Development Workflow

### Working on Features

1. **Start both servers in separate terminals**

Terminal 1 - Frontend:
```bash
cd apps/web
npm run dev
```

Terminal 2 - Backend:
```bash
cd apps/api
poetry run uvicorn main:app --reload
```

2. **Open browser**: http://localhost:5173

3. **API docs**: http://localhost:8000/docs

### Adding New Pages

1. Create new component in `apps/web/src/pages/`
2. Add route to `apps/web/src/App.tsx`
3. Add link in `Navbar.tsx`

### Adding New API Endpoints

1. Create schema in `apps/api/schemas/`
2. Create service in `apps/api/services/`
3. Create route in `apps/api/routes/`
4. Include router in `apps/api/main.py`

### Component Development

Design components following the pattern in `apps/web/src/components/`:

```typescript
import React from 'react';
import { motion } from 'framer-motion';

interface MyComponentProps {
  title: string;
  onClick?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ title, onClick }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      onClick={onClick}
    >
      {title}
    </motion.div>
  );
};
```

## Troubleshooting

### Frontend Port Already in Use

```bash
# Kill process on port 5173
lsof -ti :5173 | xargs kill -9
```

### Backend Module Not Found

```bash
cd apps/api
poetry install
```

### CORS Errors

Check `CORS_ORIGINS` in `.env` matches your frontend URL.

### Path Alias Not Working

Ensure `vite.config.ts` has the correct path:
```typescript
alias: {
  '@': path.resolve(__dirname, './src'),
}
```

## IDE Setup

### VS Code

Install extensions:
- ESLint
- Prettier
- Python
- Pylance
- Thunder Client (for API testing)

## Building for Production

### Frontend

```bash
cd apps/web
npm run build
# Output: dist/
```

### Backend

```bash
cd apps/api
poetry export -f requirements.txt > requirements.txt
# Use requirements.txt for Docker/conventional deployment
```

