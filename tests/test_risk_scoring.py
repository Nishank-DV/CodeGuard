"""Tests for risk scoring module."""

import pytest
from schemas.analysis import Vulnerability
from services.risk_scoring import RiskScorer


def test_risk_score_no_vulns():
    """Test risk score for clean code."""
    vulns = []
    score = RiskScorer.calculate_risk_score(vulns)
    assert score == 0.0


def test_risk_score_single_critical():
    """Test risk score for single critical vulnerability."""
    vuln = Vulnerability(
        id="1",
        title="Test",
        description="Test",
        severity="critical",
        cwe_id="CWE-95",
        owasp_category="A03",
        line_number=1,
        code_snippet="test",
        fix_suggestion="fix",
        secure_fix_code="fixed",
        confidence=1.0,
        rule_id="TEST-1"
    )
    score = RiskScorer.calculate_risk_score([vuln])
    assert score == 100.0  # Single critical = 100%


def test_risk_score_multiple_issues():
    """Test risk score calculation with multiple issues."""
    vulns = [
        Vulnerability(
            id="1",
            title="Test",
            description="Test",
            severity="critical",
            cwe_id="CWE-95",
            owasp_category="A03",
            line_number=1,
            code_snippet="test",
            fix_suggestion="fix",
            secure_fix_code="fixed",
            confidence=1.0,
            rule_id="TEST-1"
        ),
        Vulnerability(
            id="2",
            title="Test",
            description="Test",
            severity="high",
            cwe_id="CWE-89",
            owasp_category="A03",
            line_number=2,
            code_snippet="test",
            fix_suggestion="fix",
            secure_fix_code="fixed",
            confidence=0.8,
            rule_id="TEST-2"
        ),
    ]
    score = RiskScorer.calculate_risk_score(vulns)
    assert 50 < score <= 100


def test_severity_distribution():
    """Test severity distribution calculation."""
    vulns = [
        Vulnerability(
            id="1",
            title="Test",
            description="Test",
            severity="critical",
            cwe_id="CWE-95",
            owasp_category="A03",
            line_number=1,
            code_snippet="test",
            fix_suggestion="fix",
            secure_fix_code="fixed",
            confidence=1.0,
            rule_id="TEST-1"
        ),
        Vulnerability(
            id="2",
            title="Test",
            description="Test",
            severity="high",
            cwe_id="CWE-89",
            owasp_category="A03",
            line_number=2,
            code_snippet="test",
            fix_suggestion="fix",
            secure_fix_code="fixed",
            confidence=1.0,
            rule_id="TEST-2"
        ),
        Vulnerability(
            id="3",
            title="Test",
            description="Test",
            severity="medium",
            cwe_id="CWE-352",
            owasp_category="A01",
            line_number=3,
            code_snippet="test",
            fix_suggestion="fix",
            secure_fix_code="fixed",
            confidence=1.0,
            rule_id="TEST-3"
        ),
    ]
    
    dist = RiskScorer.severity_distribution(vulns)
    
    assert dist["critical"] == 1
    assert dist["high"] == 1
    assert dist["medium"] == 1
    assert dist["low"] == 0
    assert dist["info"] == 0
