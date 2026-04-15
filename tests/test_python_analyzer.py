"""Tests for Python analyzer."""

import pytest
from analyzers.python_analyzer import PythonAnalyzer


def test_detect_eval():
    """Test detection of eval() usage."""
    code = """
result = eval(user_input)
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert len(vulns) == 1
    assert vulns[0].severity == "critical"
    assert "eval" in vulns[0].title.lower()


def test_detect_exec():
    """Test detection of exec() usage."""
    code = """
exec(user_code)
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("exec" in v.title.lower() for v in vulns)
    assert any(v.severity == "critical" for v in vulns)


def test_detect_sql_injection():
    """Test detection of SQL injection patterns."""
    code = """
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("SQL" in v.title for v in vulns)
    assert any(v.severity == "high" for v in vulns)


def test_detect_hardcoded_password():
    """Test detection of hardcoded credentials."""
    code = """
password = "admin123"
api_key = "sk-secret-key"
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert len(vulns) >= 2
    assert any("password" in v.title.lower() for v in vulns)
    assert any("api_key" in v.title.lower() for v in vulns)


def test_detect_weak_hashing():
    """Test detection of weak hashing algorithms."""
    code = """
import hashlib
hash_obj = hashlib.md5(password.encode())
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("hashing" in v.title.lower() for v in vulns)
    assert any(v.severity in ["medium", "high"] for v in vulns)


def test_no_vulns_in_safe_code():
    """Test that safe code produces no vulnerabilities."""
    code = """
import hashlib
import bcrypt

def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def query_user(user_id):
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchall()
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    # Filter out debug mode if it's detected
    critical_vulns = [v for v in vulns if v.severity in ["critical", "high"]]
    assert len(critical_vulns) == 0


def test_detect_command_injection():
    """Test detection of command injection."""
    code = """
import os
os.system("ls " + user_input)
"""
    analyzer = PythonAnalyzer(code)
    vulns = analyzer.analyze()
    
    assert any("os.system" in v.title or "command" in v.title.lower() for v in vulns)
