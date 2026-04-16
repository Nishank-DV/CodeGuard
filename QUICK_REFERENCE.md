# 🚀 CodeGuard - Quick Reference Card

## Start Development

### Terminal 1 - Frontend
```bash
cd apps/web
npm install
npm run dev
```
→ **http://localhost:5173**

### Terminal 2 - Backend
```bash
cd apps/api
poetry install
poetry run uvicorn main:app --reload
```
→ **http://localhost:8000**  
→ **API Docs: http://localhost:8000/docs**

---

## Project Structure Quick Guide

```
CodeGuard/
├── apps/web/          Frontend (React + Vite + TypeScript)
├── apps/api/          Backend (FastAPI + Python)
├── docs/              Documentation
├── README.md          Main documentation
└── DELIVERY_SUMMARY.md Current delivery details
```

---

## Frontend Commands

```bash
npm run dev       # Start dev server
npm run build     # Production build
npm run preview   # Preview build
npm run lint      # Run ESLint
```

## Backend Commands

```bash
poetry run uvicorn main:app --reload  # Dev server
poetry run pytest                      # Run tests
poetry run black .                     # Format
poetry run mypy .                      # Type check
```

---

## Key Features Built

✅ **4 Pages**: Home, Features, About, Analyze  
✅ **11 Components**: Reusable UI system  
✅ **Dark Theme**: Cybersecurity aesthetic  
✅ **Animations**: Framer Motion  
✅ **API**: FastAPI with endpoints  
✅ **TypeScript**: Full type safety  
✅ **Responsive**: Mobile-friendly  

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root info |
| `/health` | GET | Health check |
| `/health/ready` | GET | Readiness check |
| `/analyze` | POST | Analyze code |
| `/analyze/{id}` | GET | Get previous result (Phase 2) |

---

## Environment Variables

### Frontend `.env`
```env
VITE_API_URL=http://localhost:8000/api
```

### Backend `.env`
```env
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## Pages Overview

| Page | Route | Features |
|------|-------|----------|
| Home | `/` | Hero, features, workflow, CTA |
| Features | `/features` | Detailed capabilities |
| About | `/about` | Vision, mission, roadmap |
| Analyze | `/analyze` | Code editor, mock results |

---

## Component Examples

### Button
```tsx
<Button variant="primary" size="lg">
  Click Me
</Button>
```

### Card
```tsx
<Card glow onClick={() => setActive(true)}>
  Content here
</Card>
```

### Badge
```tsx
<SeverityBadge severity="high">
  HIGH RISK
</SeverityBadge>
```

---

## Styling with Tailwind

### Custom Colors
```
cyber-bg       #0a0e27
cyber-surface  #1a1f3a
cyber-accent   #00d9ff
cyber-border   #2a2f4a
```

### Usage
```tsx
<div className="bg-cyber-bg text-cyber-accent border border-cyber-border">
  Content
</div>
```

---

## Debugging

### Frontend Issues
1. Check console: DevTools → Console
2. Verify API URL in `.env`
3. Check CORS errors in Network tab
4. Restart dev server: Ctrl+C, npm run dev

### Backend Issues
1. Check API response: http://localhost:8000/health
2. Verify dependencies: `poetry install`
3. Check port: `lsof -ti :8000`
4. Review logs in terminal

---

## Next Steps

### Phase 2 Priorities
1. Implement AST analysis engine
2. Integrate AI/ML models
3. Add database persistence
4. Create CI/CD integrations
5. Build team collaboration features

### Quick Wins
- [ ] Add authentication
- [ ] Connect to database
- [ ] Deploy to Vercel (frontend)
- [ ] Deploy to Render/Railway (backend)
- [ ] Add monitoring (Sentry)

---

## Resources

📚 **Documentation**
- README.md - Full overview
- docs/SETUP.md - Detailed setup
- docs/ARCHITECTURE.md - System design
- docs/DEPENDENCIES.md - All packages

🔗 **External**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## Support

❓ **Quick Troubleshooting**
- Port conflicts: Kill process on port
- Module errors: Reinstall dependencies
- CORS issues: Check .env CORS_ORIGINS
- Type errors: Check component props

---

**CodeGuard Phase 1** - Ready for demo and production deployment ✨

