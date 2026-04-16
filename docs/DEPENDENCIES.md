# Dependencies & Deployment Guide

## Frontend Dependencies

### Core
- `react@18.2.0` - UI framework
- `react-dom@18.2.0` - DOM renderer
- `react-router-dom@6.20.0` - Client-side routing

### Styling & Animations
- `tailwindcss@3.4.0` - Utility-first CSS
- `framer-motion@10.16.0` - Animation library
- `lucide-react@0.301.0` - Icon library

### Dev Dependencies
- `vite@5.0.0` - Build tool
- `typescript@5.3.0` - Type safety
- `autoprefixer@10.4.16` - CSS processor
- `postcss@8.4.32` - CSS transformations
- `@vitejs/plugin-react@4.2.0` - Vite React plugin

## Backend Dependencies

### Core
- `fastapi@0.104.1` - Web framework
- `uvicorn@0.24.0` - ASGI server with WebSocket support
- `pydantic@2.5.0` - Data validation
- `pydantic-settings@2.1.0` - Settings management
- `python-multipart@0.0.6` - Form parsing
- `aiofiles@23.2.1` - Async file handling

### Dev Dependencies
- `pytest@7.4.3` - Testing framework
- `black@23.12.0` - Code formatter
- `isort@5.13.2` - Import sorter
- `flake8@6.1.0` - Linter
- `mypy@1.7.1` - Type checker

## Installation

### Frontend
```bash
cd apps/web
npm install
# or
yarn install
```

### Backend
```bash
cd apps/api
pip install poetry
poetry install
```

## Deployment Checklist

### Before Deploying to Production

**Frontend:**
- [ ] Update API endpoint URL in `.env`
- [ ] Run `npm run build` and verify output
- [ ] Check bundle size
- [ ] Test all routes
- [ ] Verify CORS configuration

**Backend:**
- [ ] Set `DEBUG=false`
- [ ] Set appropriate `CORS_ORIGINS`
- [ ] Configure database connection string
- [ ] Set up logging
- [ ] Add authentication/authorization
- [ ] Run test suite: `poetry run pytest`
- [ ] Enable HTTPS

### Docker Deployment (Future)

```dockerfile
# Frontend
FROM node:18-alpine
WORKDIR /app
COPY apps/web .
RUN npm install && npm run build
EXPOSE 3000

# Backend
FROM python:3.10-slim
WORKDIR /app
COPY apps/api .
RUN pip install poetry && poetry install
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

## Performance Optimization

### Frontend
- Lazy load routes with React.lazy()
- Code splitting with dynamic imports
- Image optimization
- Bundle analysis with `vite build --analyse-chunk-size`

### Backend
- Async/await for I/O operations
- Connection pooling (when database added)
- Response caching with headers
- Rate limiting middleware

## Monitoring & Logging

### Frontend
- Browser DevTools
- Sentry for error tracking
- Google Analytics for usage

### Backend
- Application logs to stdout
- Structured logging with JSON
- Health checks at `/health` and `/health/ready`
- Performance monitoring with middleware

