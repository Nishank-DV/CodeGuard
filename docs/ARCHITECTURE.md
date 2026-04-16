# CodeGuard Architecture Document

## System Overview

CodeGuard is built as a **monorepo SaaS platform** with clear separation between frontend and backend.

```
┌─────────────────────────────────────────────────────────┐
│                     CodeGuard                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐          ┌──────────────────┐    │
│  │   React Frontend │          │  FastAPI Backend │    │
│  │   (Vite)         │          │  (Python)        │    │
│  │                  │          │                  │    │
│  │  • Pages         │◄────────►│  • Health        │    │
│  │  • Components    │  HTTP    │  • Analysis      │    │
│  │  • Routing       │  /API    │  • Future routes │    │
│  │                  │          │                  │    │
│  └──────────────────┘          └──────────────────┘    │
│         │                                │              │
│         │                                │              │
│         └────────────────┬───────────────┘              │
│                          │                             │
│                          ▼                             │
│                    [Phase 2: Database]                │
│                    [Phase 2: AI/ML]                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Frontend Architecture (React + Vite)

### Directory Structure

```
apps/web/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── SeverityBadge.tsx
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── HeroSection.tsx
│   │   ├── FeatureCard.tsx
│   │   ├── PageLayout.tsx
│   │   ├── WorkflowSection.tsx
│   │   ├── CTASection.tsx
│   │   └── index.ts         # Export all components
│   │
│   ├── pages/               # Route pages
│   │   ├── HomePage.tsx
│   │   ├── FeaturesPage.tsx
│   │   ├── AboutPage.tsx
│   │   ├── AnalyzePage.tsx
│   │   └── index.ts
│   │
│   ├── styles/
│   │   └── global.css       # Global Tailwind styles
│   │
│   ├── utils/               # Utilities (future)
│   │
│   ├── App.tsx              # Router configuration
│   └── main.tsx             # Entry point
│
├── index.html               # HTML template
├── package.json
├── vite.config.ts           # Build configuration
├── tsconfig.json
├── tailwind.config.js       # Tailwind customization
└── postcss.config.js        # PostCSS config
```

### Component Pattern

All components follow this pattern:

```typescript
import React from 'react';
import { motion } from 'framer-motion';

interface ComponentProps {
  /* props */
}

export const Component: React.FC<ComponentProps> = ({ /* props */ }) => {
  return (
    <motion.div>
      {/* content */}
    </motion.div>
  );
};
```

### State Management

Phase 1 uses React's built-in state. Future phases may introduce:
- Context API for global state
- Redux/Zustand for complex state
- TanStack Query for server state

### Styling

- **Tailwind CSS** for utility classes
- **Custom Tailwind config** with cyber theme colors
- **CSS variables** for dynamic theming (future)
- **Framer Motion** for animations

## Backend Architecture (FastAPI + Python)

### Directory Structure

```
apps/api/
├── main.py                  # FastAPI app factory
├── config.py                # Configuration management
│
├── routes/                  # API endpoints
│   ├── __init__.py
│   ├── health.py           # Health checks
│   └── analysis.py         # Analysis endpoints
│
├── services/                # Business logic
│   ├── __init__.py
│   └── analysis_service.py # Analysis service
│
├── schemas/                 # Pydantic models
│   ├── __init__.py
│   └── analysis.py        # Analysis schemas
│
├── pyproject.toml           # Dependencies (Poetry)
├── .env.example
└── .gitignore
```

### Service Layer Pattern

```python
class AnalysisService:
    """Handles analysis business logic."""
    
    @staticmethod
    def analyze_code(code: str, language: str) -> AnalysisResult:
        """Phase 1: Returns mock data. Phase 2: Implements real logic."""
        pass
```

### API Endpoint Pattern

```python
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """API endpoint with validation and error handling."""
    # Validate
    # Call service
    # Return response
```

## Data Models

### Vulnerability

```python
{
  "id": "uuid",
  "title": "SQL Injection",
  "severity": "high",           # critical, high, medium, low, info
  "cwe_id": "CWE-89",
  "line_number": 5,
  "fix_suggestion": "Use parameterized queries",
  "confidence": 0.87            # 0.0 - 1.0
}
```

### AnalysisResult

```python
{
  "id": "uuid",
  "language": "javascript",
  "vulnerabilities": [...],
  "total_issues": 3,
  "critical_count": 0,
  "high_count": 1,
  "medium_count": 1,
  "low_count": 1,
  "risk_score": 42.5            # 0 - 100
  "scanned_at": "2024-01-15T..."
}
```

## Integration Points (Phase 2)

### Database Integration

```python
# Phase 2: Add SQLAlchemy models
from sqlalchemy import Column, String

class ScanResult(Base):
    __tablename__ = "scan_results"
    id = Column(String, primary_key=True)
    # fields...
```

### AI/ML Integration

```python
# Phase 2: LLM-based threat reasoning
from langchain import OpenAI

async def generate_fix(vulnerability: Vulnerability) -> str:
    """Use LLM to generate secure fix."""
    pass
```

### CI/CD Integration

```python
# Phase 2: GitHub/GitLab webhooks
@router.post("/webhooks/github")
async def handle_github_webhook(payload: GithubPushPayload):
    """Trigger scan on code push."""
    pass
```

## Security Architecture

### Phase 1 (Current)

- ✅ CORS configured per environment
- ✅ Input validation with Pydantic
- ✅ Type safety (TypeScript + Python)
- ✅ No hardcoded secrets (.env files)
- ✅ Async operations for non-blocking I/O

### Phase 2 (Planned)

- 🔲 Authentication (JWT)
- 🔲 Authorization (RBAC)
- 🔲 Rate limiting
- 🔲 Encrypted database
- 🔲 Audit logging
- 🔲 API key management

## Performance Considerations

### Frontend

- Lazy loading routes
- Code splitting with dynamic imports
- Image optimization with next-gen formats
- Reduced motion for accessibility

### Backend

- Async/await throughout
- Non-blocking I/O
- Connection pooling (when database added)
- Caching strategies (Phase 2)
- Request timeout handling

## Error Handling

### Frontend

```typescript
try {
  // API call
} catch (error) {
  // Show user-friendly error
  // Log to monitoring
}
```

### Backend

```python
try:
    result = analyze_code(code, language)
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=str(e)
    )
```

## Testing Strategy

### Frontend (Phase 2)

- Unit tests with Vitest
- Component tests with React Testing Library
- E2E tests with Playwright/Cypress

### Backend (Phase 2)

- Unit tests with pytest
- Integration tests
- Load testing with locust

## Deployment Architecture

### Development

```
Frontend: http://localhost:5173
Backend: http://localhost:8000
```

### Production (Phase 2)

```
Frontend: Vercel / Netlify / S3 + CloudFront
Backend: AWS ECS / Render / Railway
Database: PostgreSQL on AWS RDS
```

## Monitoring & Observability

### Phase 1

- Health check endpoints
- Basic error logging

### Phase 2 (Planned)

- Sentry for error tracking
- CloudWatch / Datadog for monitoring
- OpenTelemetry for tracing
- Log aggregation (ELK stack)

---

This architecture is designed to scale from MVP to enterprise-grade SaaS platform.

