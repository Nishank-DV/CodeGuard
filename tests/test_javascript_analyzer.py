"""Tests for JavaScript analyzer."""

import pytest
from analyzers.javascript_analyzer import JavaScriptAnalyzer


def test_detect_eval():
    """Test detection of eval() usage."""
    code = """
eval(userCode);
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("eval" in v.title.lower() for v in vulns)
    assert any(v.severity == "critical" for v in vulns)


def test_detect_innerhtml():
    """Test detection of innerHTML assignment."""
    code = """
element.innerHTML = userInput;
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("innerHTML" in v.title for v in vulns)
    assert any(v.severity in ["high", "critical"] for v in vulns)


def test_detect_document_write():
    """Test detection of document.write()."""
    code = """
document.write(userData);
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("document.write" in v.title for v in vulns)


def test_detect_hardcoded_api_key():
    """Test detection of hardcoded API keys."""
    code = """
const API_KEY = "sk-1234567890abcde";
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9";
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert len(vulns) >= 2
    assert any("api" in v.title.lower() for v in vulns)
    assert any("token" in v.title.lower() for v in vulns)


def test_no_vulns_in_safe_code():
    """Test that safe code produces no vulnerabilities."""
    code = """
function displayUser(name) {
    const element = document.getElementById('user');
    element.textContent = name;
    return element;
}

const API_KEY = process.env.REACT_APP_API_KEY;
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    # Safe code should have no critical vulns
    critical_vulns = [v for v in vulns if v.severity == "critical"]
    assert len(critical_vulns) == 0


def test_detect_sql_concatenation():
    """Test detection of SQL query concatenation."""
    code = """
const query = 'SELECT * FROM users WHERE id = ' + userId;
connection.query(query);
"""
    analyzer = JavaScriptAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("SQL" in v.title or "concatenation" in v.description for v in vulns)
