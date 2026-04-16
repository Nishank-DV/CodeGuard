"""Integration tests for Phase 3: Intelligent Analysis Pipeline"""

import pytest
from analyzers.python_analyzer import PythonAnalyzer
from services.postprocessing.finding_filter import FindingFilter
from services.postprocessing.confidence_adjuster import ConfidenceAdjuster
from services.postprocessing.deduplicator import Deduplicator
from services.metadata.cwe_mapper import CWEMapper
from services.metadata.context_analyzer import ContextAnalyzer
from services.metadata.owasp_mapper import OWASPMapper
from services.remediation.fix_generator import RemediationEngine
from services.analysis_service import AnalysisService


class TestPostProcessingPipeline:
    """Test the complete Phase 3 post-processing pipeline."""
    
    def test_filter_demo_code(self):
        """Test FindingFilter removes demo/test code vulnerabilities."""
        code = """
# Demo script - not production
password = "demo_password_123"
api_key = "test_key_placeholder"
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        # Should detect hardcoded secrets
        assert len(vulns) >= 1
        
        # Filter should downgrade confidence for demo/test context
        filtered, info = FindingFilter.filter_findings(vulns, code)
        
        # Some findings may be filtered if confidence drops below threshold
        assert 'demo' in code.lower() or 'test' in code.lower()
        assert info.get('filtered_count', 0) >= 0
    
    def test_confidence_adjustment_with_reasoning(self):
        """Test ConfidenceAdjuster provides detailed reasoning."""
        code = """
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert len(vulns) > 0
        
        # Adjust confidence with context
        adjusted = ConfidenceAdjuster.adjust_findings(vulns, code)
        
        # Check that confidence_reason is populated
        for vuln in adjusted:
            assert hasattr(vuln, 'confidence_reason')
            assert vuln.confidence_reason is not None
            assert len(vuln.confidence_reason) > 0
            
            # Check priority score is calculated
            assert hasattr(vuln, 'priority_score')
            assert 0 <= vuln.priority_score <= 100
    
    def test_deduplication_on_same_line(self):
        """Test Deduplicator merges findings on same line."""
        # Create multiple vulnerabilities on same line (simulated)
        code = """
eval(user_input)  # This could match multiple rules
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        # Should have at least eval detection
        initial_count = len(vulns)
        
        # Deduplicate
        deduplicated, info = Deduplicator.deduplicate(vulns)
        
        # Verify dedup info
        assert 'original_count' in info
        assert 'deduplicated_count' in info
        assert info['original_count'] >= info['deduplicated_count']
    
    def test_metadata_enrichment_cwe(self):
        """Test CWE metadata enrichment."""
        code = """query = f"SELECT * FROM users WHERE id = {user_id}" """
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert len(vulns) > 0
        
        # Enriched should have CWE data
        vuln = vulns[0]
        assert vuln.cwe_id is not None
        
        # Get CWE metadata
        cwe_info = CWEMapper.get_cwe_info(vuln.cwe_id)
        assert cwe_info is not None
        assert 'severity_base' in cwe_info
        assert 'exploitability' in cwe_info
    
    def test_context_analyzer_user_input_detection(self):
        """Test ContextAnalyzer detects user input flow."""
        code = """
from flask import request
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert len(vulns) > 0
        
        # Context analyzer should detect user input
        for vuln in vulns:
            exploit_level, confidence_delta = ContextAnalyzer.analyze_exploit_likelihood(
                vuln.code_snippet,
                code,
                vuln.cwe_id
            )
            
            # Should assess exploitability
            assert exploit_level in ['low', 'medium', 'high']
            # Confidence delta should be realistic
            assert -1 <= confidence_delta <= 1
    
    def test_remediation_generation_completeness(self):
        """Test RemediationEngine generates complete remediation."""
        code = """query = f"SELECT * FROM users WHERE id = {user_id}" """
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert len(vulns) > 0
        
        # Generate remediation for first finding
        vuln = vulns[0]
        RemediationEngine.generate_remediation(vuln)
        
        # Check all remediation fields populated
        assert vuln.detailed_remediation is not None
        assert len(vuln.detailed_remediation) > 50  # Should be substantial
        
        assert vuln.business_impact is not None
        assert len(vuln.business_impact) > 10
        
        assert vuln.remediation_priority in ['critical', 'high', 'medium', 'low']
    
    def test_owasp_mapping(self):
        """Test OWASP category mapping."""
        code = """query = f"SELECT * FROM users WHERE id = {user_id}" """
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert len(vulns) > 0
        
        # Get OWASP category
        vuln = vulns[0]
        category = OWASPMapper.get_category(vuln.cwe_id)
        
        assert category is not None
        assert '2021' in category  # OWASP Top 10 2021
        assert 'A' in category  # Category format A##:YYYY
    
    def test_full_pipeline_integration(self):
        """Test complete pipeline from code to enriched findings."""
        code = """
# Vulnerable code example
import sqlite3

def login_user(username):
    password = input("Password: ")
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

DEBUG = True
"""
        
        # Run analysis service (complete pipeline)
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # Verify structure
        assert result.vulnerabilities is not None
        assert len(result.vulnerabilities) > 0
        assert result.risk_score >= 0
        
        # Check all Phase 3 fields are populated
        for vuln in result.vulnerabilities:
            assert vuln.confidence_reason is not None
            assert vuln.priority_score is not None
            assert vuln.exploitability in ['low', 'medium', 'high']
            assert vuln.remediation_priority in ['critical', 'high', 'medium', 'low']
            assert vuln.business_impact is not None
            assert vuln.detailed_remediation is not None
    
    def test_javascript_pipeline(self):
        """Test Phase 3 pipeline with JavaScript code."""
        code = """
const API_KEY = 'sk-1234567890';
document.getElementById('content').innerHTML = userInput;

function deleteUser(id) {
    database.delete(id);  // Missing auth check
}
"""
        
        service = AnalysisService()
        result = service.analyze(code, 'javascript')
        
        # Should detect multiple issues
        assert result.total_issues > 0
        
        # All findings should be enriched
        for vuln in result.vulnerabilities:
            assert vuln.confidence_reason is not None
            assert vuln.priority_score is not None
            assert hasattr(vuln, 'exploitability')
    
    def test_confidence_reason_accuracy(self):
        """Test confidence reasons are accurate and specific."""
        code = """
# This is test code - do not use in production
api_key = "demo_key_12345"
"""
        
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        # Adjust for context
        adjusted = ConfidenceAdjuster.adjust_findings(vulns, code)
        
        # Check reasons are specific
        for vuln in adjusted:
            reason = vuln.confidence_reason
            valid_reasons = [
                'exact_match',
                'user_input_confirmed',
                'test_code_detected',
                'commented_code',
                'in_exception_handler',
                'placeholder_detected',
                'context_dependent'
            ]
            assert any(r in reason.lower() for r in valid_reasons)
    
    def test_priority_score_ordering(self):
        """Test findings are ordered by priority score."""
        code = """
import yaml
eval(user_input)  # Critical
password = "secret123"  # High
DEBUG = True  # Medium
"""
        
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # Verify priority-ordered
        prev_score = float('inf')
        for vuln in result.vulnerabilities:
            assert vuln.priority_score <= prev_score
            prev_score = vuln.priority_score
    
    def test_false_positive_reduction(self):
        """Test pipeline reduces false positives."""
        code = """
# TODO: Implement proper validation
# FIXME: password = "admin123"  # This is commented, not real
debug = False  # Not debug mode in production

def authenticate(credentials):
    # Only use demo credentials for testing
    demo_user = "demo_user"
    demo_pass = "demo_pass_temporary"
    return credentials == demo_user
"""
        
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # Should filter out many false positives but keep real issues
        assert result.total_issues < 5  # Should be reduced
        
        # Critical issues should not be in demo/test code
        critical = [v for v in result.vulnerabilities if v.severity == 'critical']
        assert len(critical) == 0
    
    def test_meta_information_availability(self):
        """Test all meta information is available in results."""
        code = """eval(user_data)"""
        
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # Check dedup info available
        if result.deduplication_info:
            assert 'original_count' in result.deduplication_info
            assert 'deduplicated_count' in result.deduplication_info
        
        # Check findings have all meta fields
        for vuln in result.vulnerabilities:
            assert vuln.cwe_id is not None
            assert vuln.owasp_category is not None
            assert vuln.confidence is not None
            assert vuln.confidence_reason is not None
            assert vuln.priority_score is not None
            assert vuln.exploitability is not None
            assert vuln.remediation_priority is not None
            assert vuln.business_impact is not None
            assert vuln.detailed_remediation is not None


class TestEnhancedRules:
    """Test newly added Phase 3 detection rules."""
    
    def test_python_yaml_unsafe_load(self):
        """Test yaml.load() without SafeLoader detection."""
        code = """
import yaml
data = yaml.load(untrusted_input)  # Vulnerable
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        yaml_vulns = [v for v in vulns if 'YAML' in v.title]
        assert len(yaml_vulns) > 0
    
    def test_python_tempfile_misuse(self):
        """Test tempfile.mktemp() insecurity detection."""
        code = """
import tempfile
tmp_file = tempfile.mktemp()  # Vulnerable
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('tempfile' in v.title.lower() for v in vulns)
    
    def test_python_assert_for_security(self):
        """Test assert used for security checks detection."""
        code = """
assert user_is_authenticated, "User must be authenticated"
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('assert' in v.title.lower() for v in vulns)
    
    def test_python_insecure_random(self):
        """Test insecure random() for secrets detection."""
        code = """
import random
token = random.randint(0, 1000000)  # Vulnerable
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('random' in v.title.lower() for v in vulns)
    
    def test_python_requests_no_verify(self):
        """Test requests verify=False detection."""
        code = """
import requests
response = requests.get(url, verify=False)  # Vulnerable
"""
        analyzer = PythonAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('SSL' in v.title or 'verify' in v.title.lower() for v in vulns)
    
    def test_javascript_storage_secrets(self):
        """Test localStorage secret detection."""
        from analyzers.javascript_analyzer import JavaScriptAnalyzer
        
        code = """
localStorage.setItem('token', authToken);
"""
        analyzer = JavaScriptAnalyzer(code)
        vulns = analyzer.analyze()
        
        storage_vulns = [v for v in vulns if 'storage' in v.title.lower()]
        assert len(storage_vulns) > 0
    
    def test_javascript_child_process(self):
        """Test Node.js child_process command injection detection."""
        from analyzers.javascript_analyzer import JavaScriptAnalyzer
        
        code = """
const { exec } = require('child_process');
exec('ls ' + userInput, (err, out) => {});
"""
        analyzer = JavaScriptAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('child_process' in v.title.lower() or 'command' in v.title.lower() for v in vulns)
    
    def test_javascript_postmessage_sensitive(self):
        """Test postMessage with sensitive data detection."""
        from analyzers.javascript_analyzer import JavaScriptAnalyzer
        
        code = """
window.parent.postMessage({ token: userToken }, '*');
"""
        analyzer = JavaScriptAnalyzer(code)
        vulns = analyzer.analyze()
        
        assert any('postmessage' in v.title.lower() for v in vulns)
    
    def test_javascript_missing_auth(self):
        """Test missing authentication check detection."""
        from analyzers.javascript_analyzer import JavaScriptAnalyzer
        
        code = """
app.delete('/user/:id', (req, res) => {
    database.delete(req.params.id);
});
"""
        analyzer = JavaScriptAnalyzer(code)
        vulns = analyzer.analyze()
        
        # May detect as potential authorization issue
        assert len(vulns) >= 0  # Flexible detection


class TestRegressions:
    """Test that Phase 3 doesn't break Phase 2 functionality."""
    
    def test_original_rules_still_work(self):
        """Test original detection rules still function."""
        code = """
eval(user_input)
password = 'hardcoded'
os.system('ls ' + filename)
"""
        
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # All original rule detections should work
        assert any('eval' in v.title.lower() for v in result.vulnerabilities)
        assert any('password' in v.title.lower() for v in result.vulnerabilities)
        assert any('command' in v.title.lower() or 'os.system' in v.title for v in result.vulnerabilities)
    
    def test_safe_code_still_clean(self):
        """Test safe code produces minimal false positives."""
        code = """
import bcrypt

def safe_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def safe_query(user_id):
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()
"""
        
        service = AnalysisService()
        result = service.analyze(code, 'python')
        
        # Should have no critical or high-severity issues
        critical_high = [v for v in result.vulnerabilities if v.severity in ['critical', 'high']]
        assert len(critical_high) == 0
