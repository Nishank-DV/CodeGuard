# CodeGuard: Academic Code Snippets for Project Report

This document contains representative code snippets from the CodeGuard platform suitable for academic project reports. The snippets showcase key architectural patterns, security implementations, and design decisions.

---

## 1. Core Architecture: Abstract Base Analyzer Pattern

**File:** `apps/api/analyzers/base_analyzer.py`

```python
from abc import ABC, abstractmethod
from typing import List
from schemas.analysis import Vulnerability


class BaseAnalyzer(ABC):
    """Abstract base class for language-specific code analyzers."""
    
    def __init__(self, code: str):
        """Initialize analyzer with source code.
        
        Args:
            code: Source code to analyze
        """
        self.code = code
        self.lines = code.split('\n')
    
    @abstractmethod
    def analyze(self) -> List[Vulnerability]:
        """Analyze code and return list of vulnerabilities.
        
        Returns:
            List of detected vulnerabilities
        """
        pass
    
    def get_line_snippet(self, line_number: int, context_lines: int = 0) -> str:
        """Get code snippet around a specific line.
        
        Args:
            line_number: Line number (1-indexed)
            context_lines: Number of lines of context to include
            
        Returns:
            Code snippet
        """
        start = max(0, line_number - 1 - context_lines)
        end = min(len(self.lines), line_number + context_lines)
        snippet_lines = self.lines[start:end]
        return '\n'.join(snippet_lines)
```

**Why this matters:** Demonstrates the Abstract Factory/Strategy pattern for supporting multiple programming languages with extensible, type-safe architecture.

---

## 2. Security Analysis: Python Vulnerability Detection

**File:** `apps/api/analyzers/python_analyzer.py` (excerpt)

```python
class PythonAnalyzer(BaseAnalyzer):
    """Analyzer for Python code using AST-based detection."""

    def analyze(self) -> List[Vulnerability]:
        """Analyze Python code for vulnerabilities."""
        self.vulnerabilities = []
        
        self._detect_eval_exec()
        self._detect_hardcoded_secrets()
        self._detect_sql_injection()
        self._detect_command_injection()
        self._detect_unsafe_deserialization()
        self._detect_weak_hashing()
        
        return self.vulnerabilities

    def _detect_eval_exec(self) -> None:
        """Detect eval() and exec() usage."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func_name = node.func.id if isinstance(node.func, ast.Name) else None
                if func_name == "eval":
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Use of eval()",
                            description="eval() executes arbitrary Python code, creating critical security risks.",
                            severity="critical",
                            cwe_id="CWE-95",
                            owasp_category="A03:2021 - Injection",
                            line_number=node.lineno,
                            recommendation="Use ast.literal_eval() or json.loads().",
                            secure_fix="import ast\nvalue = ast.literal_eval(user_input)",
                        )
                    )
```

**Academic Value:** Shows real-world CWE/OWASP mapping and remediation guidance generation.

---

## 3. Risk Scoring Algorithm

**File:** `apps/api/services/risk_scoring.py`

```python
class RiskScorer:
    """Calculates risk scores based on vulnerability findings."""
    
    # Severity weights for risk calculation
    SEVERITY_WEIGHTS = {
        "critical": 10,
        "high": 7,
        "medium": 4,
        "low": 1,
        "info": 0.25,
    }
    
    @staticmethod
    def calculate_risk_score(vulnerabilities: List[Vulnerability]) -> float:
        """Calculate overall risk score (0-100).
        
        Formula: (total_weighted_score / max_possible_score) * 100
        
        Args:
            vulnerabilities: List of detected vulnerabilities
            
        Returns:
            Risk score from 0 to 100
        """
        if not vulnerabilities:
            return 0.0
        
        total_score = 0.0
        
        for vuln in vulnerabilities:
            severity_weight = RiskScorer.SEVERITY_WEIGHTS.get(vuln.severity, 0)
            confidence_multiplier = RiskScorer._confidence_to_multiplier(vuln.confidence)
            total_score += severity_weight * confidence_multiplier
        
        # Normalize to 0-100 scale
        max_possible = len(vulnerabilities) * 10  # All critical
        normalized_score = (total_score / max_possible) * 100
        
        return min(100.0, normalized_score)
    
    @staticmethod
    def severity_distribution(vulnerabilities: List[Vulnerability]) -> Dict[str, int]:
        """Get count of vulnerabilities by severity."""
        distribution = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
        }
        
        for vuln in vulnerabilities:
            distribution[vuln.severity] += 1
        
        return distribution
```

**Academic Value:** Demonstrates algorithmic approach to security scoring with weighted metrics and normalization.

---

## 4. Authentication & RBAC Implementation

**File:** `apps/api/security/auth.py`

```python
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

@dataclass
class AuthPrincipal:
    role: str
    api_key: str


ALLOWED_ROLES = {"admin", "analyst", "viewer"}


@lru_cache(maxsize=1)
def _parse_auth_map() -> dict[str, str]:
    """Parse and cache API key to role mapping."""
    entries = [e.strip() for e in settings.auth_api_keys.split(",") if e.strip()]
    parsed: dict[str, str] = {}
    for entry in entries:
        if ":" not in entry:
            continue
        role, key = entry.split(":", 1)
        role = role.strip().lower()
        key = key.strip()
        if role in ALLOWED_ROLES and key:
            parsed[key] = role
    return parsed


async def get_current_principal(
    api_key_header_value: str | None = Depends(api_key_header),
    api_key_query_value: str | None = Query(default=None, alias="api_key"),
) -> AuthPrincipal:
    """Dependency injection for FastAPI RBAC."""
    if not settings.auth_enabled:
        return AuthPrincipal(role="admin", api_key="auth-disabled")

    api_key = api_key_header_value or api_key_query_value

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    role = _resolve_role_from_key(api_key)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    return AuthPrincipal(role=role, api_key=api_key)
```

**Academic Value:** Shows secure API authentication with role-based access control (RBAC) using dependency injection.

---

## 5. Post-Processing Pipeline: Deduplication

**File:** `apps/api/services/postprocessing/deduplicator.py`

```python
class Deduplicator:
    """Merges duplicate or highly similar findings into cleaner results."""
    
    @staticmethod
    def deduplicate(vulns: List[Vulnerability]) -> tuple[List[Vulnerability], Dict]:
        """Deduplicate similar vulnerabilities.
        
        Merges findings that:
        - Occur on the same line
        - Have same CWE
        - Match same rule patterns
        
        Args:
            vulns: List of vulnerabilities
            
        Returns:
            (deduplicated list, deduplication info dict)
        """
        if not vulns:
            return [], {"total_merged": 0}
        
        # Group by (line_number, rule_id, cwe_id)
        groups: Dict[tuple, List[Vulnerability]] = {}
        
        for vuln in vulns:
            key = (vuln.line_number, vuln.rule_id or "unknown", vuln.cwe_id)
            if key not in groups:
                groups[key] = []
            groups[key].append(vuln)
        
        # Merge groups with highest confidence
        deduplicated = []
        total_merged = 0
        
        for key, group in groups.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                merged = Deduplicator._merge_vulns(group)
                deduplicated.append(merged)
                total_merged += len(group) - 1
        
        dedup_info = {
            "total_merged": total_merged,
            "original_count": len(vulns),
            "deduplicated_count": len(deduplicated),
        }
        
        return deduplicated, dedup_info
```

**Academic Value:** Demonstrates post-processing techniques to reduce false positives and improve result quality.

---

## 6. Analysis Service: Complete Pipeline Orchestration

**File:** `apps/api/services/analysis_service.py` (excerpt)

```python
class AnalysisService:
    """Code analysis with intelligent post-processing pipeline."""
    
    @staticmethod
    def analyze_code(code: str, language: str) -> AnalysisResult:
        """Analyze source code with intelligent post-processing pipeline.
        
        Complete analysis pipeline:
        1. Detect vulnerabilities with language-specific analyzer
        2. Filter obvious false positives and demo code
        3. Adjust confidence based on code context
        4. Deduplicate similar findings on same line
        5. Enrich with metadata (CWE, exploitability, OWASP)
        6. Analyze contextual exploitability
        7. Generate detailed remediation guidance
        8. Calculate final prioritization scores
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript)
            
        Returns:
            AnalysisResult with intelligent, de-duped, prioritized vulnerabilities
        """
        language_lower = language.lower()
        
        # 1. Dispatch to appropriate analyzer
        if language_lower == 'python':
            analyzer = PythonAnalyzer(code)
        elif language_lower in ['javascript', 'typescript', 'js', 'ts']:
            analyzer = JavaScriptAnalyzer(code)
        else:
            raise ValueError(f"Language '{language}' not supported")
        
        # Run detection
        vulnerabilities = analyzer.analyze()
        
        # 2. Filter obvious false positives
        vulnerabilities = FindingFilter.filter_findings(vulnerabilities, code)
        
        # 3. Adjust confidence based on context
        vulnerabilities = ConfidenceAdjuster.adjust_findings(vulnerabilities, code)
        
        # 4. Deduplicate identical findings on same line
        vulnerabilities, dedup_info = Deduplicator.deduplicate(vulnerabilities)
        
        # 5-7. Enrich with metadata, remediation guidance, and calculate scores
        # ... (continues with enrichment pipeline)
```

**Academic Value:** Shows systematic multi-stage data processing pipeline with separation of concerns.

---

## 7. API Route Implementation

**File:** `apps/api/routes/analysis.py` (excerpt)

```python
@router.post("", response_model=AnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze source code for security vulnerabilities.
    
    Args:
        request: CodeAnalysisRequest containing code and language
        
    Returns:
        AnalysisResponse with vulnerability findings
    """
    try:
        if not request.code or not request.code.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code cannot be empty"
            )

        if len(request.code) > settings.max_code_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Code exceeds max allowed length ({settings.max_code_length} characters)"
            )

        normalized_language = _normalize_language(request.language)
        if normalized_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported language: {request.language}"
            )

        safe_filename = sanitize_filename(request.filename) if request.filename else None
        result, _ = await _analyze_and_store_single(request.code, normalized_language, safe_filename)
        
        return AnalysisResponse(
            success=True,
            data=result,
            message=f"Analysis complete. Found {result.total_issues} vulnerabilities."
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Analysis failed for language=%s", request.language)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed due to an internal error"
        )
```

**Academic Value:** Demonstrates RESTful API design with comprehensive validation and error handling.

---

## 8. Data Models (Schema)

**File:** `apps/api/schemas/analysis.py` (excerpt)

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal


class Vulnerability(BaseModel):
    """Represents a detected vulnerability with Phase 3 enhancements."""
    id: str
    title: str
    description: str
    severity: Literal["critical", "high", "medium", "low", "info"]
    cwe_id: str
    owasp_category: str
    line_number: int
    column_number: Optional[int] = None
    code_snippet: Optional[str] = None
    fix_suggestion: Optional[str] = None
    secure_fix_code: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    
    # Phase 3 enhancements
    confidence_reason: Optional[str] = None
    priority_score: int = Field(ge=0, le=100, default=50)
    exploitability: Literal["low", "medium", "high"] = Field(default="medium")
    remediation_priority: Literal["critical", "high", "medium", "low"] = Field(default="medium")
    business_impact: Optional[str] = None
    detailed_remediation: Optional[str] = None
    
    # Phase 4 remediation workflow
    status: Literal["open", "reviewing", "resolved", "ignored"] = Field(default="open")
    remediation_notes: Optional[str] = Field(default=None, max_length=2000)


class AnalysisResult(BaseModel):
    """Result of code analysis with Phase 3 metadata."""
    id: str
    language: str
    vulnerabilities: list[Vulnerability]
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: float = Field(ge=0.0, le=100.0)
    scanned_at: datetime
    deduplication_info: Optional[dict] = None
```

**Academic Value:** Shows structured data design with rich metadata and domain-specific validation.

---

## 9. FastAPI Application Setup

**File:** `apps/api/main.py` (excerpt)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    init_db()
    validate_auth_configuration()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    @app.middleware("http")
    async def request_size_guard(request: Request, call_next):
        """Guard against oversized requests."""
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit():
            if int(content_length) > settings.max_request_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"success": False, "error": "Request too large"},
                )
        return await call_next(request)
    
    # Include routers
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(analysis_router)
    app.include_router(scans_router)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Global exception handler."""
        logger.exception("Unhandled API exception")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"},
        )
    
    return app
```

**Academic Value:** Demonstrates enterprise-grade application setup with middleware, CORS, and centralized error handling.

---

## 10. Frontend Button Component (React Pattern)

**File:** `apps/web/src/components/Button.tsx`

```typescript
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', ...props }, ref) => {
    const baseStyles = 'font-medium rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed';
    
    const variants = {
      primary: 'bg-cyan-500 hover:bg-cyan-600 text-black focus:ring-cyan-400',
      secondary: 'bg-purple-600 hover:bg-purple-700 text-white focus:ring-purple-500',
      ghost: 'bg-transparent hover:bg-cyber-surface text-cyan-400 border border-cyber-border focus:ring-cyan-400',
    };

    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-6 py-2.5 text-base',
      lg: 'px-8 py-3 text-lg',
    };

    return (
      <button
        ref={ref}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';
```

**Academic Value:** Shows reusable component pattern with composition over inheritance, accessibility support, and TypeScript best practices.

---

## 11. Frontend Routing & RBAC

**File:** `apps/web/src/App.tsx`

```typescript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from '@/components';
import { HomePage, FeaturesPage, AboutPage, AnalyzePage, DashboardPage, ScanHistoryPage } from '@/pages';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/features" element={<FeaturesPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route
          path="/analyze"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst"]}>
              <AnalyzePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst", "viewer"]}>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst", "viewer"]}>
              <ScanHistoryPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
```

**Academic Value:** Demonstrates client-side routing with role-based route protection.

---

## 12. Data Persistence Models

**File:** `apps/api/models/scan.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ScanRecord:
    id: str
    code_hash: str
    filename: Optional[str]
    language: str
    scanned_at: datetime
    duration_ms: int
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: float
    finding_summary: str
    findings_json: str


@dataclass
class ScanSummaryRecord:
    total_scans: int
    total_vulnerabilities: int
    average_risk_score: float
    most_common_language: Optional[str]
    highest_risk_scan_id: Optional[str]
    highest_risk_score: float
    top_cwe_ids: list[str]
    severity_distribution: dict[str, int]
    avg_findings_per_scan: float
    scans_last_7_days: int
    open_findings: int
    resolved_findings: int
    ignored_findings: int
    generated_at: datetime
```

**Academic Value:** Shows data model design for scan artifacts with aggregate statistics for analytics.

---

## Key Architectural Patterns Demonstrated

1. **Abstract Factory Pattern** - BaseAnalyzer for multi-language support
2. **Strategy Pattern** - Different analyzers for different languages
3. **Dependency Injection** - FastAPI Depends() for RBAC
4. **Pipeline Pattern** - Sequential data processing stages (filter → adjust → deduplicate → enrich)
5. **Repository Pattern** - ScanStore for data persistence
6. **Composite Components** - React reusable components with variants
7. **Pydantic Models** - Schema validation and serialization

---

## Academic Discussion Points

- **Analysis Accuracy:** How deduplication and confidence adjustment reduce false positives
- **Scalability:** Stateless API design for horizontal scaling
- **Security:** RBAC implementation with role-based endpoint access
- **UX/DX:** How structured metadata (CWE, OWASP) improves developer experience
- **Testing Approach:** Unit tests for analyzers, integration tests for pipeline
- **Performance:** Risk scoring algorithm complexity, deduplication efficiency

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React + TypeScript + Tailwind | Responsive UI with component library |
| **Backend** | FastAPI + Python | High-performance async API |
| **Analysis** | AST parsing + Regex patterns | Code structure analysis |
| **Database** | SQLite | Scan history and findings persistence |
| **Security** | API keys + RBAC | Authentication and authorization |
| **Validation** | Pydantic | Schema validation and serialization |

---

This document provides ready-to-use code snippets that demonstrate core concepts suitable for academic presentations, project documentation, and educational purposes.
