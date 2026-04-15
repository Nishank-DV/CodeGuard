"""
Advanced confidence adjustment based on context, exploitability, and risk factors.
"""

import re
from typing import List, Tuple
from schemas.analysis import Vulnerability


class ConfidenceAdjuster:
    """Adjusts confidence scores based on contextual analysis."""
    
    @staticmethod
    def adjust_findings(vulns: List[Vulnerability], code: str) -> List[Vulnerability]:
        """Adjust confidence scores based on code context.
        
        Args:
            vulns: List of vulnerabilities to adjust
            code: Original source code
            
        Returns:
            Updated vulnerabilities with refined confidence
        """
        lines = code.split('\n')
        
        for vuln in vulns:
            # Get context around the finding
            context = ConfidenceAdjuster._get_context(lines, vuln.line_number)
            
            # Determine confidence reason based on analysis
            reason = ConfidenceAdjuster._analyze_confidence(vuln, context, code)
            vuln.confidence_reason = reason[0]
            
            # Adjust confidence based on context
            adjustment = reason[1]
            vuln.confidence = max(0.0, min(1.0, vuln.confidence + adjustment))
            
            # Calculate priority score from confidence and severity
            vuln.priority_score = ConfidenceAdjuster._calculate_priority(vuln)
        
        return vulns
    
    @staticmethod
    def _get_context(lines: List[str], line_number: int, radius: int = 3) -> str:
        """Get surrounding code context.
        
        Args:
            lines: All code lines
            line_number: Target line (1-indexed)
            radius: Lines of context on each side
            
        Returns:
            Context string
        """
        start = max(0, line_number - 1 - radius)
        end = min(len(lines), line_number + radius)
        return '\n'.join(lines[start:end])
    
    @staticmethod
    def _analyze_confidence(vuln: Vulnerability, context: str, full_code: str) -> Tuple[str, float]:
        """Analyze and return confidence reason and adjustment.
        
        Args:
            vuln: Vulnerability to analyze
            context: Code context around finding
            full_code: Full source code
            
        Returns:
            (reason_label, confidence_adjustment_delta)
        """
        reason = "unresolved"
        adjustment = 0.0
        
        # Check for explicit user input indicators
        if ConfidenceAdjuster._has_user_input_indicator(context):
            reason = "user_input_confirmed"
            adjustment = +0.15
        
        # Check for obvious non-production context
        if ConfidenceAdjuster._is_test_context(context):
            reason = "test_code_detected"
            adjustment = -0.30
        
        # Check for commented code
        if ConfidenceAdjuster._is_commented(context, vuln.line_number):
            reason = "commented_code"
            adjustment = -0.25
        
        # Check for exception/error handling context
        if ConfidenceAdjuster._in_exception_handler(context):
            reason = "in_exception_handler"
            adjustment = -0.10
        
        # Check for obvious placeholder values
        if ConfidenceAdjuster._has_placeholder_value(vuln.code_snippet or ""):
            reason = "placeholder_detected"
            adjustment = -0.20
        
        # Direct exact match gets highest confidence
        if not reason or reason == "unresolved":
            reason = "exact_match"
            adjustment = 0.0
        
        return reason, adjustment
    
    @staticmethod
    def _has_user_input_indicator(context: str) -> bool:
        """Check if code suggests user input is actually involved."""
        patterns = [
            r"request\.(args|form|json|GET|POST)",
            r"sys\.argv",
            r"input\s*\(",
            r"raw_input\s*\(",
            r"getenv\(",
        ]
        for pattern in patterns:
            if re.search(pattern, context):
                return True
        return False
    
    @staticmethod
    def _is_test_context(context: str) -> bool:
        """Check if code is clearly in a test/demo."""
        patterns = [
            r"(?i)(test_|def test|if __name__|@pytest|@test|describe\(|it\()",
            r"(?i)(FIXME|TODO|XXX|HACK|DEBUG)",
        ]
        for pattern in patterns:
            if re.search(pattern, context):
                return True
        return False
    
    @staticmethod
    def _is_commented(context: str, line_number: int) -> bool:
        """Check if the specific line is commented out."""
        lines = context.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('#') or line.strip().startswith('//'):
                return True
        return False
    
    @staticmethod
    def _in_exception_handler(context: str) -> bool:
        """Check if code is in an exception handler."""
        return bool(re.search(r"except\s*:|catch\s*\(", context))
    
    @staticmethod
    def _has_placeholder_value(code_snippet: str) -> bool:
        """Check if the code contains obvious placeholder values."""
        patterns = [
            r"(?i)(XXX|TODO|FIXME|your_|demo|example|test|placeholder)",
            r"(?i)(dummy|fake|mock|stub)",
        ]
        for pattern in patterns:
            if re.search(pattern, code_snippet):
                return True
        return False
    
    @staticmethod
    def _calculate_priority(vuln: Vulnerability) -> int:
        """Calculate 0-100 priority score from severity and confidence.
        
        Args:
            vuln: Vulnerability with severity and confidence
            
        Returns:
            Priority score 0-100
        """
        severity_scores = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25,
            "info": 10,
        }
        
        severity_base = severity_scores.get(vuln.severity, 50)
        
        # Apply confidence multiplier
        priority = int(severity_base * vuln.confidence)
        
        return max(0, min(100, priority))
