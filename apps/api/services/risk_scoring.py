"""
Risk scoring and severity classification system.
"""

from typing import List, Dict
from schemas.analysis import Vulnerability


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
    
    # Confidence multiplier (high confidence = 1.0, medium = 0.7, low = 0.5)
    CONFIDENCE_THRESHOLD = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.5,
    }
    
    @staticmethod
    def calculate_risk_score(vulnerabilities: List[Vulnerability]) -> float:
        """Calculate overall risk score (0-100).
        
        Uses weighted severity scoring:
        - Critical: 10 points per issue
        - High: 7 points per issue
        - Medium: 4 points per issue
        - Low: 1 point per issue
        - Info: 0.25 points per issue
        
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
        # Maximum score would be all vulns being critical with high confidence
        max_possible = len(vulnerabilities) * 10  # All critical
        normalized_score = (total_score / max_possible) * 100
        
        # Cap at 100
        return min(100.0, normalized_score)
    
    @staticmethod
    def _confidence_to_multiplier(confidence: float) -> float:
        """Convert confidence (0-1) to multiplier for scoring.
        
        Args:
            confidence: Confidence value (0.0 to 1.0)
            
        Returns:
            Multiplier for scoring (0.5 to 1.0)
        """
        if confidence >= 0.85:
            return 1.0
        elif confidence >= 0.70:
            return 0.7
        else:
            return 0.5
    
    @staticmethod
    def severity_distribution(vulnerabilities: List[Vulnerability]) -> Dict[str, int]:
        """Get count of vulnerabilities by severity.
        
        Args:
            vulnerabilities: List of detected vulnerabilities
            
        Returns:
            Dictionary with severity counts
        """
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


class SeverityClassifier:
    """Maps CWE/vulnerability patterns to OWASP and severity classifications."""
    
    # CWE to severity mapping
    CWE_SEVERITY_MAP = {
        "CWE-95": "critical",   # Improper Neutralization of Directives in Dynamically Evaluated Code
        "CWE-78": "critical",   # Improper Neutralization of Special Elements used in an OS Command
        "CWE-89": "high",       # SQL Injection
        "CWE-79": "high",       # Improper Neutralization of Input During Web Page Generation
        "CWE-327": "high",      # Use of a Broken or Risky Cryptographic Algorithm
        "CWE-798": "high",      # Use of Hard-coded Credentials
        "CWE-502": "high",      # Deserialization of Untrusted Data
        "CWE-489": "medium",    # Active Debug Code
        "CWE-352": "medium",    # Cross-Site Request Forgery (CSRF)
        "CWE-754": "medium",    # Improper Exception Handling
        "CWE-295": "medium",    # Improper Certificate Validation
        "CWE-22": "high",       # Improper Limitation of a Pathname to a Restricted Directory
    }
    
    # OWASP Top 10 2021 categories
    OWASP_CATEGORIES = {
        "A01": "A01:2021 - Broken Access Control",
        "A02": "A02:2021 - Cryptographic Failures",
        "A03": "A03:2021 - Injection",
        "A04": "A04:2021 - Insecure Design",
        "A05": "A05:2021 - Security Misconfiguration",
        "A06": "A06:2021 - Vulnerable and Outdated Components",
        "A07": "A07:2021 - Authentication and Session Management Failures",
        "A08": "A08:2021 - Software and Data Integrity Failures",
        "A09": "A09:2021 - Logging and Monitoring Failures",
        "A10": "A10:2021 - Server-Side Request Forgery (SSRF)",
    }
