"""
Finding filter for reducing false positives from obviously placeholder/demo values.
"""

import re
from typing import List
from schemas.analysis import Vulnerability


class FindingFilter:
    """Filters out obvious false positives and downgrades low-confidence findings."""
    
    # Obvious placeholder/demo patterns
    DEMO_PATTERNS = [
        r"(?i)(demo|test|example|sample|placeholder|your_|mock|fake|xxx|todo)",
        r"(?i)(admin123|password123|test123|qwerty|123456|12345)",
        r"(?i)API_KEY=.*$|password=.*$|secret=.*$",
        r"(?i)(demo|test)_",
    ]
    
    # Patterns that suggest the code is not production
    NON_PRODUCTION_INDICATORS = [
        r"(?i)(test|demo|example|sandbox|debug)",
        r"if\s*__name__\s*==\s*['\"]__main__['\"]",  # Python main guard
        r"(?i)(jest\.|describe\(|it\(|test\()",  # Jest/test framework calls
    ]
    
    @staticmethod
    def is_demo_value(value_str: str) -> bool:
        """Check if a string looks like demo/placeholder text.
        
        Args:
            value_str: String to check
            
        Returns:
            True if appears to be demo/placeholder
        """
        if not value_str:
            return False
        
        for pattern in FindingFilter.DEMO_PATTERNS:
            if re.search(pattern, value_str):
                return True
        return False
    
    @staticmethod
    def is_production_code(code: str, line_number: int) -> bool:
        """Check if code context suggests production use.
        
        Args:
            code: Full source code
            line_number: Line number of finding
            
        Returns:
            True if likely production code
        """
        lines = code.split('\n')
        
        # Get context around the finding (±5 lines)
        start = max(0, line_number - 6)
        end = min(len(lines), line_number + 5)
        context = '\n'.join(lines[start:end])
        
        # Check for test/demo indicators in context
        for pattern in FindingFilter.NON_PRODUCTION_INDICATORS:
            if re.search(pattern, context):
                return False
        
        return True
    
    @staticmethod
    def filter_findings(vulns: List[Vulnerability], code: str) -> List[Vulnerability]:
        """Filter out obvious false positives.
        
        Args:
            vulns: List of vulnerabilities to filter
            code: Original source code for context
            
        Returns:
            Filtered list of vulnerabilities
        """
        filtered = []
        
        for vuln in vulns:
            # Check for obvious demo values in code snippet
            if vuln.code_snippet and FindingFilter.is_demo_value(vuln.code_snippet):
                # Downgrade confidence for demo code
                vuln.confidence *= 0.6
                vuln.priority_score = max(0, vuln.priority_score - 25)
            
            # Check if parent code is test/demo
            if not FindingFilter.is_production_code(code, vuln.line_number):
                # Significant downgrade for non-production context
                vuln.confidence *= 0.4
                vuln.priority_score = max(0, vuln.priority_score - 40)
            
            # Only skip findings with extremely low confidence after adjustment
            if vuln.confidence >= 0.3:
                filtered.append(vuln)
        
        return filtered
