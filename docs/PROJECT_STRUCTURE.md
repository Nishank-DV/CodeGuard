# CodeGuard Project Structure

```
CodeGuard/
│
├── 📄 README.md                          # Main project documentation [UPDATED Phase 2]
├── 📄 quick-start.sh                     # Quick start for Linux/macOS [NEW]
├── 📄 quick-start.bat                    # Quick start for Windows [NEW]
├── 📄 CONTRIBUTING.md                    # Contribution guidelines
├── 📄 LICENSE                            # MIT License
├── 📄 .gitignore                         # Git ignore rules
│
├── apps/
│   ├── web/                              # React Frontend (Vite)
│   │   ├── src/
│   │   │   ├── components/               # 11 Reusable UI components
│   │   │   │   ├── Navbar.tsx            # Navigation bar
│   │   │   │   ├── Footer.tsx            # Footer with links
│   │   │   │   ├── Button.tsx            # Primary/secondary buttons
│   │   │   │   ├── Card.tsx              # Card container with glow
│   │   │   │   ├── SeverityBadge.tsx    # Vulnerability severity badges
│   │   │   │   ├── Input.tsx             # Form input field
│   │   │   │   ├── HeroSection.tsx       # Hero banner
│   │   │   │   ├── FeatureCard.tsx       # Feature showcase cards
│   │   │   │   ├── CTASection.tsx        # Call-to-action section
│   │   │   │   ├── PageLayout.tsx        # Page wrapper
│   │   │   │   └── WorkflowSection.tsx   # Process flow visualization
│   │   │   │
│   │   │   ├── pages/                    # Route pages
│   │   │   │   ├── HomePage.tsx          # Landing page
│   │   │   │   ├── FeaturesPage.tsx      # Features overview
│   │   │   │   ├── AboutPage.tsx         # About & mission
│   │   │   │   └── AnalyzePage.tsx       # Code analyzer [UPDATED Phase 2]
│   │   │   │
│   │   │   ├── styles/
│   │   │   │   └── globals.css           # Global Tailwind styles
│   │   │   │
│   │   │   ├── utils/
│   │   │   │   └── api.ts                # API client utilities
│   │   │   │
│   │   │   ├── App.tsx                   # Router setup
│   │   │   ├── main.tsx                  # Entry point
│   │   │   └── vite-env.d.ts             # Vite types
│   │   │
│   │   ├── public/                       # Static assets
│   │   │   ├── logo.svg                  # CodeGuard logo
│   │   │   └── favicon.ico               # Favicon
│   │   │
│   │   ├── package.json                  # Dependencies
│   │   ├── tsconfig.json                 # TypeScript config
│   │   ├── vite.config.ts                # Vite config
│   │   ├── tailwind.config.js            # Tailwind CSS config
│   │   ├── postcss.config.js             # PostCSS config
│   │   ├── index.html                    # HTML template
│   │   ├── .env.example                  # Environment template
│   │   └── .env                          # Environment (local)
│   │
│   └── api/                              # FastAPI Backend (Python)
│       ├── analyzers/                    # Language-specific analyzers [NEW Phase 2]
│       │   ├── base_analyzer.py          # Abstract base class
│       │   ├── python_analyzer.py        # Python vulnerability detector (8 rules)
│       │   ├── javascript_analyzer.py    # JavaScript detector (7 rules)
│       │   ├── __init__.py               # Package exports
│       │   └── # Future: java_analyzer.py, go_analyzer.py, etc.
│       │
│       ├── routes/                       # API endpoints
│       │   ├── __init__.py               # Package init
│       │   ├── health.py                 # Health check endpoint
│       │   └── analysis.py               # Analysis endpoints
│       │
│       ├── services/                     # Business logic
│       │   ├── __init__.py               # Package init
│       │   ├── analysis_service.py       # Analyzer dispatcher [UPDATED Phase 2]
│       │   └── risk_scoring.py           # Risk calculation [NEW Phase 2]
│       │
│       ├── schemas/                      # Pydantic models
│       │   ├── __init__.py               # Package init
│       │   └── analysis.py               # Analysis models [UPDATED Phase 2]
│       │
│       ├── tests/                        # Unit tests [NEW Phase 2]
│       │   ├── __init__.py               # Package init
│       │   ├── test_python_analyzer.py   # Python analyzer tests
│       │   ├── test_javascript_analyzer.py # JavaScript analyzer tests
│       │   └── test_risk_scoring.py      # Risk scoring tests
│       │
│       ├── main.py                       # FastAPI app & routes
│       ├── config.py                     # Configuration & settings
│       ├── pyproject.toml                # Poetry dependencies
│       ├── poetry.lock                   # Locked versions
│       ├── .env.example                  # Environment template
│       ├── .env                          # Environment (local)
│       └── requirements.txt              # Pip requirements (fallback)
│
├── packages/                             # Shared packages (Future expansion)
│   ├── ui/                               # Shared UI components
│   └── types/                            # Shared TypeScript types
│
├── configs/                              # Shared configuration
│   ├── eslintrc.json                     # ESLint rules
│   ├── prettier.json                     # Prettier formatting
│   └── tsconfig.base.json                # Shared TypeScript config
│
└── docs/                                 # Documentation
    ├── ARCHITECTURE.md                   # System architecture deep dive
    ├── API.md                            # API endpoint reference
    ├── DETECTION_RULES.md                # All 15 vulnerability rules [NEW Phase 2]
    ├── PHASE2_SUMMARY.md                 # Implementation summary [NEW Phase 2]
    ├── DEPLOYMENT.md                     # Deployment guide
    ├── CONTRIBUTING.md                   # Developer guidelines
    └── # Future: PERFORMANCE.md, SECURITY.md, etc.
```

## Directory Details

### Frontend (`apps/web/`)

**Purpose:** React-based user interface for CodeGuard  
**Tech Stack:** React 18, Vite, TypeScript, Tailwind CSS, Framer Motion  
**Key Features:**
- 4 main pages (Home, Features, About, Analyze)
- 11 reusable components
- Dark theme with neon accents
- Responsive design

**Key Files:**
- `AnalyzePage.tsx` - Real code analysis interface with API integration
- `App.tsx` - React Router setup
- `components/` - Reusable UI library

### Backend (`apps/api/`)

**Purpose:** FastAPI service for vulnerability analysis  
**Tech Stack:** Python 3.10+, FastAPI, Pydantic, AST module  
**Key Features:**
- 15 vulnerability detection rules (8 Python + 7 JavaScript)
- Real-time analysis via `/analyze` endpoint
- Risk scoring system (0-100 normalized scale)
- Comprehensive error handling

**Key Files:**
- `analyzers/` - Language-specific detection engines
- `services/analysis_service.py` - Dispatcher routing to analyzers
- `services/risk_scoring.py` - Risk calculation engine
- `main.py` - FastAPI app setup
- `routes/` - API endpoints

### Tests (`apps/api/tests/`)

**Purpose:** Unit test coverage for analysis logic  
**Framework:** pytest  
**Coverage:**
- Python analyzer: 7 tests covering all 8 rules
- JavaScript analyzer: 6 tests covering all 7 rules
- Risk scoring: 4 tests for calculation & distribution

### Documentation (`docs/`)

**Files:**
1. **ARCHITECTURE.md** - System design & component interactions
2. **API.md** - Endpoint reference with examples
3. **DETECTION_RULES.md** - All 15 rules with vulnerable/secure code
4. **PHASE2_SUMMARY.md** - Implementation status & stats
5. **DEPLOYMENT.md** - Production setup guide
6. **CONTRIBUTING.md** - Developer guidelines

---

## Key Implementation Details

### Vulnerability Detection Flow

```
┌─────────────────────────────────────┐
│  Frontend: AnalyzePage.tsx          │
│  - Paste code                       │
│  - Select language                  │
│  - Click Analyze                    │
└────────────┬────────────────────────┘
             │ POST /analyze
             ▼
┌─────────────────────────────────────┐
│  Backend: AnalysisService           │
│  - Receive code + language          │
│  - Route to appropriate analyzer    │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
Python          JavaScript
Analyzer        Analyzer
(8 rules)       (7 rules)
    │                 │
    └────────┬───────┘
             ▼
┌─────────────────────────────────────┐
│  RiskScorer                         │
│  - Calculate weighted scores        │
│  - Aggregate severity counts        │
│  - Return 0-100 risk score         │
└────────────┬────────────────────────┘
             │ AnalysisResult
             ▼
┌─────────────────────────────────────┐
│  Frontend: Results Display          │
│  - Show vulnerabilities             │
│  - Display risk score               │
│  - Expandable cards with fixes      │
└─────────────────────────────────────┘
```

### Risk Scoring Algorithm

```
Risk Score = (Weighted Severity Sum / Max Possible) × 100

Severity Weights:
  CRITICAL: 10 (full weight)
  HIGH:      7 (70% of critical)
  MEDIUM:    4 (40% of critical)
  LOW:       1 (10% of critical)
  INFO:     0.25 (2.5% of critical)

Confidence Multipliers:
  ≥ 0.85: 1.0 (trust the finding)
  0.70-0.84: 0.7 (reduce by 30%)
  < 0.70: 0.5 (reduce by 50%)

Result Scale:
  0-10:   🟢 Green (minimal)
  10-40:  🟡 Yellow (moderate)
  40-70:  🟠 Orange (high)
  70-100: 🔴 Red (critical)
```

---

## Getting Started Quick Reference

### Prerequisites
- Node.js 18+
- Python 3.10+
- Git

### Quick Setup
```bash
# Windows
cd CodeGuard
quick-start.bat

# Linux/macOS  
cd CodeGuard
bash quick-start.sh
```

### Manual Setup
```bash
# Backend
cd apps/api
poetry install
poetry run uvicorn main:app --reload

# Frontend (new terminal)
cd apps/web
npm install
npm run dev
```

### Running Tests
```bash
cd apps/api
poetry run pytest tests/ -v
```

---

## File Count Summary

| Component | Files | Type |
|-----------|-------|------|
| Frontend Components | 11 | TypeScript/React |
| Frontend Pages | 4 | TypeScript/React |
| Backend Analyzers | 3 | Python |
| Backend Services | 2 | Python |
| Backend Tests | 3 | Python |
| Backend Routes | 2 | Python |
| Documentation | 7 | Markdown |
| Config Files | 8+ | Various |
| **Total** | **~40** | Mixed |

---

## Phase 2 Additions [NEW]

```
✅ New Files:
  - apps/api/analyzers/*.py (3 files)
  - apps/api/services/risk_scoring.py
  - apps/api/tests/* (3 files)
  - docs/DETECTION_RULES.md
  - docs/PHASE2_SUMMARY.md
  - quick-start.bat, quick-start.sh

✅ Modified Files:
  - apps/api/schemas/analysis.py
  - apps/api/services/analysis_service.py
  - apps/web/src/pages/AnalyzePage.tsx
  - README.md

Total Lines Added: ~2,660
```

---

*Last Updated: January 2024 - Phase 2 Complete*  
*Status: Production-ready with real vulnerability detection* 🛡️
