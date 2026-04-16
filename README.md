# CodeGuard 🛡️

**AI-Assisted Static Code Analysis Platform** for real-time security vulnerability detection.

![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)
![Status](https://img.shields.io/badge/status-Phase%205-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

---

## 🚀 Overview

CodeGuard is a next-generation **shift-left security platform** that detects and helps remediate security vulnerabilities in source code in real-time. Built with AI-powered static analysis and advanced Abstract Syntax Tree (AST) parsing, CodeGuard helps development teams catch vulnerabilities **before they reach production**.

### Why CodeGuard?

- **🧠 AI-Powered**: Machine learning models understand code semantics and context
- **⚡ Real-Time**: Instant vulnerability detection integrated into your workflow
- **🎯 Accurate**: OWASP-aligned severity classification with minimal false positives
- **🔧 Actionable**: Secure fix recommendations for every vulnerability
- **📊 Developer-First**: Premium UX designed for modern development teams

---

## 📋 Table of Contents

- [Vision & Problem Statement](#vision--problem-statement)
- [Implementation Progress](#implementation-progress-phases-1-5)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [UI/UX Highlights](#uiux-highlights)
- [Current Capability Snapshot](#current-capability-snapshot-phase-5)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

---

## 🎯 Vision & Problem Statement

### The Problem

Traditional security practices focus on **detection after deployment** (shift-right), but by then, vulnerabilities are already affecting real users. Modern development teams need solutions that catch issues **during development** (shift-left).

Existing static analysis tools have critical limitations:
- **Excessive false positives** → Alert fatigue
- **Poor context awareness** → Missed vulnerabilities
- **Slow scanning** → Workflow disruption
- **No fix guidance** → Manual remediation overhead

### CodeGuard's Solution

Combine three powerful analysis techniques:

1. **Abstract Syntax Tree (AST) Parsing** - Deep structural code analysis
2. **Data Flow Analysis** - Track sensitive data through codebases
3. **AI/ML Threat Detection** - Semantic understanding of vulnerability patterns

Result: **Accurate, actionable, real-time vulnerability detection** that developers actually trust.

---

## 🏗️ Implementation Progress (Phases 1-5)

### Phase 1: MVP Foundation ✅

✅ **Enterprise-grade architecture** - Production-ready monorepo structure  
✅ **Premium frontend** - Stunning React UI with Framer Motion animations  
✅ **Design system** - 11 reusable components with accessibility features  
✅ **Multi-page experience** - Home, Features, About, Analyze pages  
✅ **Backend scaffold** - FastAPI service with modular architecture  
✅ **Environment support** - .env configuration for all environments  

### Phase 2: Real Analysis Engine ✅

✅ **Python analyzer** - AST-based with 8 detection rules  
✅ **JavaScript analyzer** - Pattern-based with 7 detection rules  
✅ **Risk scoring system** - Severity-weighted, confidence-adjusted, 0-100 scale  
✅ **Frontend integration** - Real API calls and result rendering  
✅ **Full vulnerability data model** - CWE IDs, OWASP categories, secure fixes  
✅ **Test suite** - Unit tests for analyzers and scoring  

### Phase 3: Intelligent Enrichment ✅

✅ **Post-processing pipeline** - deduplication, confidence adjustment, filtering  
✅ **Metadata enrichment** - CWE/OWASP mapping and exploitability context  
✅ **Remediation intelligence** - richer fix guidance and business impact details  

### Phase 4: Product Workflow ✅

✅ **Persistent scan history** - SQLite-backed scan artifacts and findings  
✅ **Dashboard & history pages** - trend and remediation workflow views  
✅ **Report generation** - downloadable JSON/Markdown reports  

### Phase 4.1: Endpoint Auth + RBAC ✅

✅ **API key auth** with role-based permissions (`viewer`, `analyst`, `admin`)  
✅ **Protected scan/report/remediation operations**  

### Phase 5: Finalization ✅

✅ **Deployment hardening** - startup auth config validation and request-size controls  
✅ **Batch file scanning** - partial-failure tolerant multi-file scanning endpoint  
✅ **Analytics enrichment** - top finding titles and language distribution  
✅ **Frontend auth workflow** - login page, protected routes, centralized API utility  
✅ **Report hardening** - safer filenames and secure response headers  

---

## 🏛️ Architecture

```
codeguard/
│
├── apps/
│   ├── web/                  # React Frontend (Vite)
│   │   ├── src/
│   │   │   ├── components/   # 11 reusable UI components
│   │   │   ├── pages/        # Route pages (Home, Features, About, Analyze)
│   │   │   ├── styles/       # Global Tailwind CSS
│   │   │   ├── utils/        # Utilities & helpers
│   │   │   ├── App.tsx       # Router setup
│   │   │   └── main.tsx      # Entry point
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.js
│   │   └── index.html
│   │
│   └── api/                  # FastAPI Backend (Python 3.10+)
│       ├── analyzers/        # Language-specific vulnerability detectors
│       │   ├── base_analyzer.py      # Abstract base class
│       │   ├── python_analyzer.py    # Python AST-based scanner
│       │   └── javascript_analyzer.py # JavaScript pattern-based scanner
│       ├── routes/           # API endpoints
│       ├── services/         # Business logic
│       │   ├── analysis_service.py   # Analyzer dispatcher
│       │   └── risk_scoring.py       # Risk calculation engine
│       ├── schemas/          # Pydantic models + validation
│       ├── tests/            # Unit tests for analyzers
│       ├── main.py           # FastAPI app & routes
│       ├── config.py         # Configuration & environment
│       ├── pyproject.toml    # Dependencies (Poetry)
│       └── .env.example      # Environment template
│
├── packages/
│   ├── ui/                   # Shared UI components (Future: monorepo expansion)
│   └── types/                # Shared TypeScript types (Future)
│
├── configs/                  # Shared configuration
├── docs/                     # Additional documentation
└── README.md                 # This file
```

### Key Architectural Principles

- **Modular**: Clear separation of concerns (analyzers, services, routes)
- **Language-Agnostic**: Analyzer base class allows easy addition of new languages
- **Scalable**: Service-based backend, component-based frontend
- **Testable**: Unit tests for all analysis logic
- **Production-Ready**: Environment config, error handling, logging
- **Type-Safe**: TypeScript frontend, Pydantic backend validation

---

## ⚙️ Tech Stack

### Frontend

| Technology | Purpose |
|-----------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool (5x faster than CRA) |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Premium animations |
| **lucide-react** | Icon library |
| **React Router** | Client-side routing |

### Backend

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Language |
| **FastAPI** | Web framework |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Poetry** | Dependency management |

### Design System

- **Dark cyber-security theme** with neon accents
- **Glassmorphism** panels with backdrop blur
- **Gradient text** and animated backgrounds
- **Responsive** across all devices
- **Accessibility-conscious** color contrasts

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.10+
- **Git**

### Installation

#### 1. Clone Repository

```bash
git clone <repo-url>
cd CodeGuard
```

#### 2. Setup Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at **http://localhost:5173**

#### 3. Setup Backend

```bash
cd apps/api

# Install dependencies (using Poetry)
pip install poetry
poetry install

# Create .env file
cp .env.example .env

# Run development server
poetry run uvicorn main:app --reload
```

API will be available at **http://localhost:8000**

API documentation:
- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### Verify Installation

1. **Frontend**: Visit http://localhost:5173 - should see CodeGuard homepage
2. **Backend**: Visit http://localhost:8000/health - should see health status
3. **Integration**: Try the Analyze page - API should respond with sample vulnerabilities

---

## 🔌 API Documentation

### Health Endpoint

```http
GET /health
```

Response:
```json
{
  "status": "healthy",
   "version": "0.5.0",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Analysis Endpoint

```http
POST /analyze
Content-Type: application/json

{
  "code": "function test() { ... }",
  "language": "javascript",
  "filename": "app.js"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "language": "javascript",
    "total_issues": 3,
    "critical_count": 0,
    "high_count": 1,
    "medium_count": 1,
    "low_count": 1,
    "risk_score": 42.5,
    "vulnerabilities": [
      {
        "id": "uuid",
        "title": "SQL Injection",
        "severity": "high",
        "cwe_id": "CWE-89",
        "line_number": 5,
        "fix_suggestion": "Use parameterized queries",
        "confidence": 0.87
      },
      ...
    ],
    "scanned_at": "2024-01-15T10:30:00.000Z"
  },
  "message": "Analysis complete. Found 3 vulnerabilities."
}
```

### Supported Languages

- Python
- JavaScript / TypeScript

---

## 🎨 UI/UX Highlights

### Design System

**Reusable Components:**
- `Button` - Primary, secondary, ghost variants
- `Card` - With glow effects and hover animations
- `SeverityBadge` - Color-coded vulnerability levels
- `Input` - Form input with error states
- `Navbar` - Sticky, responsive navigation
- `Footer` - Rich footer with links
- `HeroSection` - Animated hero with CTA
- `FeatureCard` - Scrollable feature showcase
- `PageLayout` - Consistent page wrapper
- `WorkflowSection` - Process flow visualization
- `CTASection` - Call-to-action section

### Visual Identity

```css
/* Color Palette */
Backgrounds:   #0a0e27 (cyber-bg), #1a1f3a (cyber-surface)
Accent:        #00d9ff (neon cyan), #7c3aed (purple)
Text:          #e0e0e0 (light gray)
Borders:       #2a2f4a (semi-transparent)

/* Effects */
Glassmorphism:  backdrop-blur-md with border opacity
Gradients:      Cyan → Purple combinations
Animations:     Smooth 300ms transitions with Framer Motion
```

### Pages

| Page | Purpose |
|------|---------|
| **Home** | Hero section, features, workflow, CTA |
| **Features** | Detailed feature explanations |
| **About** | Mission, vision, problem/solution storytelling |
| **Analyze** | Live code editor with persisted analysis, remediation workflow, and batch scan |
| **Dashboard** | Aggregate analytics, severity/remediation breakdown, language distribution |
| **History** | Persisted scans, drill-down findings, report download, status updates |
| **Login** | Demo role/key selection for protected workflows |

---

## � Vulnerability Detection Examples

### Python: SQL Injection Detection

**Vulnerable Code:**
```python
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ SQL Injection!
result = cursor.execute(query)
```

**Detection:**
- Rule: `sql_injection`
- Severity: HIGH
- CWE: CWE-89
- Confidence: 0.95

**Secure Fix:**
```python
user_id = request.args.get('id')
query = "SELECT * FROM users WHERE id = ?"  # ✅ Parameterized!
result = cursor.execute(query, (user_id,))
```

### JavaScript: XSS Vulnerability Detection

**Vulnerable Code:**
```javascript
const userInput = request.query.content;
document.getElementById('output').innerHTML = userInput;  // ❌ XSS!
```

**Detection:**
- Rule: `innerhtml`
- Severity: HIGH
- CWE: CWE-79
- Confidence: 0.98

**Secure Fix:**
```javascript
const userInput = request.query.content;
document.getElementById('output').textContent = userInput;  // ✅ Safe!
```

### Python: Hardcoded Secrets Detection

**Vulnerable Code:**
```python
API_KEY = "sk-1234567890abcdef"  # ❌ Hardcoded!
password = "admin123"  # ❌ Hardcoded!
```

**Detection:**
- Rule: `hardcoded_secrets`
- Severity: HIGH
- CWE: CWE-798
- Confidence: 0.87

**Secure Fix:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')  # ✅ From environment!
password = os.getenv('PASSWORD')  # ✅ From environment!
```

---

## 📦 Available Scripts

### Frontend

```bash
cd apps/web

npm run dev      # Start dev server (http://localhost:5173)
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Run ESLint
npm run format   # Format with Prettier
```

### Backend

```bash
cd apps/api

# Development
poetry run uvicorn main:app --reload

# Testing
poetry run pytest tests/                 # Run all tests
poetry run pytest tests/test_python_analyzer.py -v  # Run specific test
poetry run pytest --cov=analyzers tests/  # Coverage report

# Code quality
poetry run black .                       # Format code
poetry run mypy .                        # Type checking
poetry run isort .                       # Sort imports
```

### Both Services (Quick Start)

```bash
# Terminal 1: Backend
cd apps/api
poetry run uvicorn main:app --reload

# Terminal 2: Frontend
cd apps/web
npm run dev
```

Then visit: **http://localhost:5173**

---

## 🎯 Current Capability Snapshot (Phase 5)

### ✅ Completed

**Core Detection + Product Workflow**
- ✅ AST-based Python analyzer with 8 detection rules
- ✅ Pattern-based JavaScript analyzer with 7 detection rules
- ✅ Risk scoring system (severity-weighted, confidence-multiplied, 0-100 scale)
- ✅ Frontend-backend integration with persisted scan artifacts
- ✅ Role-based protected workflows for scan/report/remediation actions
- ✅ Batch file scanning with partial-failure handling
- ✅ Dashboard/history analytics and secure report downloads

### 📊 Vulnerability Detection Rules

**Python Analyzer (8 Rules)**

| Rule | Type | Severity | Description |
|------|------|----------|-------------|
| `eval_exec` | Code Execution | CRITICAL | Direct eval() or exec() usage |
| `hardcoded_secrets` | Secrets | HIGH | Hardcoded passwords, API keys, tokens |
| `sql_injection` | Injection | HIGH | SQL queries via string concatenation/format |
| `command_injection` | Injection | HIGH/CRITICAL | os.system(), shell=True usage |
| `unsafe_deserialization` | Deserialization | HIGH | pickle.loads() or similar unsafe operations |
| `weak_hashing` | Cryptography | HIGH/MEDIUM | MD5, SHA1, or crypt for security purposes |
| `debug_mode` | Configuration | MEDIUM | DEBUG=True, print() statements in production |
| `xxe_parsing` | XML Processing | MEDIUM | Unsafe XML/Entity parsing |

**JavaScript Analyzer (7 Rules)**

| Rule | Type | Severity | Description |
|------|------|----------|-------------|
| `eval` | Code Execution | CRITICAL | eval() calls in JavaScript |
| `innerhtml` | XSS | HIGH | innerHTML assignment with untrusted data |
| `document_write` | DOM | HIGH | document.write() usage |
| `hardcoded_secrets` | Secrets | HIGH | API keys, tokens, passwords in code |
| `sql_concatenation` | Injection | HIGH | SQL queries built with string operators |
| `weak_crypto` | Cryptography | MEDIUM | createCipher, MD5, SHA1 in crypto operations |
| `dangerous_calls` | Code Execution | HIGH | setTimeout with eval, Function constructor |

### 🧮 Risk Scoring Algorithm

```
Risk Score = (Total Weighted Severity / Max Possible) × 100

Where:
  Severity Weights = {critical: 10, high: 7, medium: 4, low: 1, info: 0.25}
  Confidence Multiplier = 1.0 if ≥85%, else 0.7 if ≥70%, else 0.5
  Max Possible = (Count × Critical Weight) = 10 per vulnerability
  
Result Range: 0-100
  0-10:   Green (minimal risk)
  10-40:  Yellow (moderate risk)
  40-70:  Orange (high risk)
  70-100: Red (critical risk)
```

### 🔬 Analysis Mode

**Python**: AST traversal with regex fallback for syntax errors
- Uses `ast.walk()` for structural analysis
- Falls back to regex patterns when syntax invalid
- Contextual line extraction with surrounding code

**JavaScript**: Pattern/regex-based with future tree-sitter support
- Regex patterns with comment filtering
- Structured for future migration to tree-sitter
- Does not support full control flow analysis in MVP

### 📝 Example Output

```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "language": "python",
    "total_issues": 3,
    "critical_count": 1,
    "high_count": 2,
    "medium_count": 0,
    "risk_score": 78.5,
    "vulnerabilities": [
      {
        "id": "1",
        "title": "Eval Usage",
        "severity": "critical",
        "cwe_id": "CWE-95",
        "owasp_category": "A03:2021 – Injection",
        "line_number": 42,
        "code_snippet": "result = eval(user_input)",
        "fix_suggestion": "Use json.loads() for JSON, ast.literal_eval() for safe evaluation",
        "secure_fix_code": "import json\nresult = json.loads(user_input)",
        "confidence": 0.99,
        "rule_id": "PYTHON-EVAL-01"
      },
      ...
    ]
  }
}
```

### 🧪 Running Tests

```bash
cd apps/api

# Install test dependencies
poetry add --group dev pytest pytest-cov

# Run all tests
poetry run pytest tests/

# Run specific test file
poetry run pytest tests/test_python_analyzer.py

# With coverage
poetry run pytest --cov=analyzers tests/
```

### 🚀 Roadmap

**1. Extended Language Support**
- Java (with full AST support)
- C++ (Clang-based analysis)
- Go (go/ast parser)
- Rust (rustc AST)
- PHP (PHP-Parser)

**2. CI/CD Integrations**
- GitHub Actions pull request checks
- GitLab CI/CD pipelines
- Bitbucket Pipelines
- Jenkins plugins

**3. AI/ML Integration**
- LLM-based false positive filtering
- Semantic code understanding
- Secure code generation
- Learning from organization patterns

**4. Database & Persistence**
- PostgreSQL backend
- Historical analysis tracking
- Trend analytics & reporting
- Scan comparison

**5. IDE Plugins**
- VS Code extension with inline warnings
- JetBrains plugins (IntelliJ, PyCharm, WebStorm)
- Real-time scanning as you type

**6. Team Features**
- Multi-user collaboration
- Issue assignment & tracking
- Team dashboards
- Compliance reporting (HIPAA, SOC2, ISO27001)

---

## 🔐 Security Best Practices

- ✅ No hardcoded secrets (use `.env`)
- ✅ CORS properly configured
- ✅ Input validation on all endpoints
- ✅ Type safety with TypeScript + Pydantic
- ✅ Environment-based configuration
- ✅ API-key auth with role-based endpoint controls
- ✅ Request-size limiting and strict upload validation
- ✅ Hardened report downloads with no-store and nosniff headers

---

## 📝 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=/api
```

### Backend (.env)
```env
DEBUG=true
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

See [apps/web/.env.example](apps/web/.env.example) and [apps/api/.env.example](apps/api/.env.example) for all options.

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push branch: `git push origin feature/amazing-feature`
4. Open Pull Request

### Code Style

**Frontend:**
- TypeScript strict mode
- ESLint rules enforced
- Prettier formatting

**Backend:**
- Black code formatter
- Type hints required
- MyPy type checking

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## ⚠️ Known Limitations

- **JavaScript uses regex patterns** (not full AST) → Some false positives/negatives possible
- **SQLite persistence by default** → Not suitable for high-concurrency multi-node deployments
- **No CI/CD plugins yet** → Planned roadmap item
- **Pattern-based analysis only** → Control flow analysis not yet implemented
- **Single language per scan** → Cannot analyze polyglot files

### Roadmap to Address Limitations

| Limitation | Target | Solution |
|-----------|--------|----------|
| JavaScript regex → AST | Next major | Integrate tree-sitter parser |
| SQLite scaling limits | Next major | PostgreSQL + migration layer |
| No CI/CD integration | Near-term | GitHub Actions and GitLab CI integration |
| Limited control-flow depth | Mid-term | Deeper data-flow analysis engine |
| Polyglot support | Mid-term | Multi-language detection per file |

---

## 🚀 Getting Production-Ready

To deploy to production:

1. **Security**
   - Set `DEBUG=false` in backend `.env`
   - Add authentication & authorization (OAuth2, JWT)
   - Enable HTTPS/TLS
   - Set rate limiting & DDoS protection

2. **Infrastructure**
   - Use environment-specific configuration
   - Add database persistence layer (PostgreSQL)
   - Implement proper logging & monitoring (ELK Stack, DataDog)
   - Set up CI/CD pipelines (GitHub Actions, GitLab CI)
   - Configure production CORS origins only

3. **Scaling**
   - Containerize with Docker
   - Deploy with Kubernetes or similar orchestration
   - Add caching layer (Redis)
   - Set up metrics collection (Prometheus)

4. **Compliance**
   - GDPR compliance for code analysis
   - SOC2 audit trail
   - Data retention policies
   - HIPAA considerations for sensitive data

---

## ✅ Phase 5 Finalization Addendum

Phase 5 completed with deployment-hardening controls, protected workflows, and report/analytics polish while preserving existing architecture.

### Backend

- API auth and startup validation: fail-fast validation for auth config and role-aware access controls.
- Request hardening: request-size guard middleware and strict upload validation/sanitized filenames.
- Batch scanning: new `POST /analyze/batch-files` endpoint with per-file success/failure results and aggregate metrics.
- Analytics enrichment: scan summaries now include `top_finding_titles` and `language_distribution`.
- Report hardening: sanitized download filenames, `no-store` cache policy, and `nosniff` header.

### Frontend

- Shared API/auth utilities: centralized `apiFetch` and auth-aware report URL generation.
- Protected navigation: login page and route guard for analyze/dashboard/history flows.
- Analyze UX upgrade: single-file and multi-file batch scanning in one page with summarized batch outcomes.
- Dashboard/History updates: consume enriched analytics fields and use centralized API utility paths.

### Verification Completed

Commands executed successfully:

```bash
# Frontend
cd apps/web
npm run build

# Backend (targeted)
cd apps/api
PYTHONPATH=. pytest -q tests/test_phase41_auth_rbac.py tests/test_phase5_batch_and_analytics.py
```

Result:
- Frontend build passed.
- Targeted auth + Phase 5 backend tests passed (`9 passed`).

Note:
- The broad legacy Phase 3 integration suite currently has pre-existing failures unrelated to Phase 5 changes.

---

## 📚 Documentation Files

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Detailed system design
- [API.md](docs/API.md) - Full API reference
- [DETECTION_RULES.md](docs/DETECTION_RULES.md) - All 15+ detection rules with examples
- [CONTRIBUTING.md](CONTRIBUTING.md) - Developer guidelines

---

## 🤓 For Security Professionals

### Analysis Methodology

1. **Syntax Analysis** - Parse code into AST (Python) or patterns (JavaScript)
2. **Semantic Analysis** - Understand data flow and variable usage
3. **Rule Matching** - Apply 15+ detection rules across languages
4. **Risk Scoring** - Weighted severity × confidence confidence → 0-100 scale
5. **Remediation** - Provide actionable secure code snippets

### False Positive Reduction

- Confidence scoring (0.5-1.0) on all detections
- Context-aware rule triggering
- Whitelist common safe patterns
- User feedback integration (Phase 3)

### What's NOT in Scope (MVP)

- ❌ Dependency vulnerability scanning (SBOM/supply chain)
- ❌ Data classification & DLP
- ❌ Advanced control flow analysis
- ❌ Taint tracking across files
- ❌ Symbolic execution
- ❌ Custom query languages

---

## 💬 Contact & Support

For questions, suggestions, or bug reports:
- 📧 Email: support@codeguard.dev
- 🐛 Issues: [GitHub Issues](https://github.com/yourorg/CodeGuard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourorg/CodeGuard/discussions)
- 📖 Wiki: [Project Wiki](https://github.com/yourorg/CodeGuard/wiki)

---

## 🎓 About the Team

CodeGuard is built by security and software engineering professionals passionate about shifting security left and empowering developers with actionable insights.

**Team Expertise:**
- Application Security (AppSec)
- Software Engineering
- DevSecOps practices
- Vulnerability Research
- Secure Code Development

---

**Built with ❤️ for secure software development.**

*CodeGuard Phase 5 - Production-hardened secure code analysis workflow platform.* 🛡️

---

## Phase 4 Completion: Security Platform Upgrade

Phase 4 upgrades CodeGuard from one-time intelligent scanning to a usable security product workflow with persistence, analytics, reporting, and remediation tracking.

### Implemented in Phase 4

1. Persistent scan history (SQLite)
   - Every analysis is stored with metadata, findings, severity counts, risk score, summary, and duration.
   - Findings are persisted with remediation workflow state.

2. Scan history and summary APIs
   - `GET /scans` with pagination, sorting, and filtering.
   - `GET /scans/{id}` for full scan detail and findings.
   - `DELETE /scans/{id}` for history cleanup.
   - `GET /scans/summary` for analytics metrics.

3. Report generation
   - `GET /scans/{id}/report?format=json|md` for downloadable JSON and Markdown reports.
   - Reports include metadata, severity summary, prioritized findings, and remediation details.

4. Remediation workflow
   - Finding status lifecycle: `open`, `reviewing`, `resolved`, `ignored`.
   - Remediation notes support per finding.
   - `PATCH /scans/{scan_id}/findings/{finding_id}` updates status and notes.

5. File-based scanning support
   - New endpoint: `POST /analyze/file`.
   - Extension allowlist and size limits enforced.
   - UTF-8 text-only handling. Uploaded files are never executed.

6. Dashboard and history UX
   - New pages:
     - `/dashboard` for analytics summary and severity/remediation insights.
     - `/history` for recent scans, detail drilldown, report download, delete, and finding status updates.
   - Analyze page enhanced with:
     - File scan action
     - Report download buttons
     - Finding status + notes controls

7. Stronger health and diagnostics
   - `GET /health/ready` now checks database readiness.
   - `GET /health/diagnostics` provides operational status without leaking secrets.

### Backend Structure Added (Phase 4)

- `apps/api/database/session.py`
- `apps/api/models/scan.py`
- `apps/api/repositories/scan_repository.py`
- `apps/api/routes/scans.py`
- `apps/api/schemas/scans.py`
- `apps/api/services/persistence/scan_store.py`
- `apps/api/services/analytics/scan_analytics.py`
- `apps/api/services/reports/report_generator.py`
- `apps/api/services/remediation/status_manager.py`

### Frontend Structure Added (Phase 4)

- `apps/web/src/pages/DashboardPage.tsx`
- `apps/web/src/pages/ScanHistoryPage.tsx`

### Security Hardening Applied to CodeGuard Itself

Findings fixed in this phase:

1. Overly permissive API behavior
   - Added stricter language normalization and allowlist handling in analysis route.

2. Input-size and upload hardening gaps
   - Added max code length enforcement.
   - Added max upload size and extension allowlist.
   - Added UTF-8 decode validation and safe text-only processing.

3. Error leakage risk
   - Replaced raw exception exposure with sanitized error response in analysis route.
   - Added global exception handler in FastAPI app.

4. CORS defaults too broad
   - Switched wildcard methods/headers to explicit allowlists in settings.

5. Readiness gap
   - Added DB-backed readiness check and diagnostics endpoint.

Deferred intentionally:

- Authentication/authorization for history/report/status endpoints.
- Rate limiting and abuse protection.
- Full JavaScript AST parser migration.
- PostgreSQL migration and multi-tenant data model.

### Verification Performed (Phase 4)

Backend verification completed:

1. Syntax compilation checks:
   - `python -m py_compile` on analyzers, routes, main, and analysis service.

2. Unit tests:
   - `pytest tests/test_phase4_repository.py tests/test_phase4_reports.py`
   - Result: all passing.

3. API integration smoke tests (TestClient):
   - `/health`, `/health/ready`, `/health/diagnostics`
   - `/analyze` persisted to DB
   - `/scans`, `/scans/{id}`, `/scans/summary`
   - `/scans/{id}/report`
   - `/analyze/file`
   - finding status patch persistence
   - Result: successful responses.

Frontend verification completed:

1. Dependency install
   - `npm install` in `apps/web`

2. Build verification
   - `npm run build` in `apps/web`
   - Result: successful Vite production build.

### How to Run (Phase 4)

Backend:

```bash
cd apps/api
python -m uvicorn main:app --reload
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

Phase 4 key routes:

- `/analyze`
- `/dashboard`
- `/history`

### Known Limitations After Phase 4

- No authn/authz yet on management endpoints.
- SQLite is single-node local persistence only.
- Reports currently JSON/Markdown (PDF deferred).
- Trend analytics are summary-based, not full time-series visualization.

### Phase 5 Delivery Against Phase 4 Plan

Delivered in Phase 5:

1. Auth + role-based access control for scan artifacts.
2. Analytics enrichment for findings and language breakdown.
3. Frontend protected workflows and centralized API/auth utilities.
4. Security hardening for upload handling, request sizing, and report downloads.

Still on roadmap:

1. PostgreSQL + migration layer.
2. CI/CD integrations (GitHub Actions first).
3. Team workflows (assignment, SLA tracking, notifications).
4. Deeper analytics (time-series trends and recurrence modeling).

## Phase 4.1 Addendum: Endpoint Auth and Role-Based Controls

A focused Phase 4.1 hardening layer is now active for API endpoints with minimal architecture changes.

### Auth Model

- Header-based API key auth using `X-API-Key`
- Role mapping from environment configuration
- Roles:
  - `viewer`: read-only scan access
  - `analyst`: can analyze and update remediation status
  - `admin`: full access, including destructive delete

### Role Permissions

- `GET /auth/whoami`: any authenticated role
- `POST /analyze`, `POST /analyze/file`: `analyst`, `admin`
- `GET /scans`, `GET /scans/{id}`, `GET /scans/summary`, `GET /scans/{id}/report`: `viewer`, `analyst`, `admin`
- `PATCH /scans/{scan_id}/findings/{finding_id}`: `analyst`, `admin`
- `DELETE /scans/{id}`: `admin`

### Configuration

Backend (`apps/api/.env`):

```env
AUTH_ENABLED=true
AUTH_HEADER_NAME=X-API-Key
AUTH_API_KEYS=admin:dev-admin-key,analyst:dev-analyst-key,viewer:dev-viewer-key
```

Frontend (`apps/web/.env`):

```env
VITE_API_URL=/api
VITE_API_KEY=dev-analyst-key
```

### Notes

- Current keys are development defaults. Rotate before non-dev usage.
- Client-side keys are for local MVP flow; production should use token-based auth and server-side session management.
- Health endpoints remain intentionally public for ops checks.

## Local Run and Troubleshooting (Windows)

Use two terminals from project root.

Terminal 1 (Backend):

```powershell
Set-Location apps/api
poetry install
poetry run uvicorn main:app --reload
```

Terminal 2 (Frontend):

```powershell
Set-Location apps/web
npm install
npm run dev
```

Expected URLs:

- Frontend: `http://localhost:5173`
- Backend health: `http://127.0.0.1:8000/health`
- Dashboard API through proxy: `http://localhost:5173/api/scans/summary`

If backend exits with code 1:

1. Check if port 8000 is already in use:

```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

2. If a stale process is holding the port, stop it:

```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
```

3. Confirm Python environment and dependencies:

```powershell
Set-Location apps/api
poetry env info
poetry install
```

4. Start backend again:

```powershell
poetry run uvicorn main:app --reload
```

If frontend exits with code 1:

1. Reinstall frontend dependencies:

```powershell
Set-Location apps/web
npm install
```

2. Ensure frontend environment file contains:

```env
VITE_API_URL=/api
VITE_API_KEY=dev-analyst-key
```

3. Start frontend again:

```powershell
npm run dev
```
