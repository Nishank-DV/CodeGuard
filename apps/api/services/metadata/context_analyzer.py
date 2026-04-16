"""
Contextual reasoning to determine if suspicious code is actually exploitable.
"""

import re
from typing import Tuple


class ContextAnalyzer:
    """Analyzes code context to determine exploitability and risk factors."""
    
    @staticmethod
    def analyze_exploit_likelihood(code: str, finding_line: int, rule_type: str) -> Tuple[str, float]:
        """Analyze if a finding is actually exploitable based on context.
        
        Args:
            code: Full source code
            finding_line: Line number of the finding (1-indexed)
            rule_type: Type of rule (e.g., "eval", "sql_injection", "command_injection")
            
        Returns:
            (exploitability_level, confidence_adjustment)
        """
        lines = code.split('\n')
        
        # Get context around the finding
        context_start = max(0, finding_line - 1 - 5)
        context_end = min(len(lines), finding_line + 5)
        context = '\n'.join(lines[context_start:context_end])
        
        if rule_type in ("eval", "exec", "command_injection"):
            return ContextAnalyzer._analyze_code_execution(context, finding_line, lines)
        elif rule_type == "sql_injection":
            return ContextAnalyzer._analyze_sql_likelihood(context, finding_line, lines)
        elif rule_type == "hardcoded_secrets":
            return ContextAnalyzer._analyze_secret_likelihood(context)
        else:
            return "medium", 0.0
    
    @staticmethod
    def _analyze_code_execution(context: str, finding_line: int, lines: list) -> Tuple[str, float]:
        """Analyze if code execution is actually exploitable."""
        # Check if user input is actually passed to eval/exec
        if ContextAnalyzer._has_user_input_flow(context, lines, finding_line):
            return "high", +0.20
        
        # Check if the input is hard-coded
        if ContextAnalyzer._has_hardcoded_input(context):
            return "low", -0.30
        
        return "medium", 0.0
    
    @staticmethod
    def _analyze_sql_likelihood(context: str, finding_line: int, lines: list) -> Tuple[str, float]:
        """Analyze if SQL injection is actually likely."""
        # Check for parameterized query frameworks used elsewhere
        full_code = '\n'.join(lines)
        
        if ContextAnalyzer._uses_parameterized_elsewhere(full_code):
            # This violation stands out - likely oversight or forgotten case
            return "high", +0.15
        
        # Check if string concat happens with obvious hardcoded values
        if ContextAnalyzer._has_hardcoded_values(context):
            return "low", -0.25
        
        return "medium", 0.0
    
    @staticmethod
    def _analyze_secret_likelihood(context: str) -> Tuple[str, float]:
        """Analyze if hardcoded value is an actual production secret."""
        # Demo/test indicators
        demo_patterns = [
            r"(?i)(demo|test|example|placeholder|fake|mock|xxx|todo)",
            r"(?i)(admin123|password123|qwerty|1234)",
        ]
        
        for pattern in demo_patterns:
            if re.search(pattern, context):
                return "low", -0.25
        
        # Look like real values
        if ContextAnalyzer._looks_like_real_credential(context):
            return "high", +0.20
        
        return "medium", 0.0
    
    @staticmethod
    def _has_user_input_flow(context: str, lines: list, finding_line: int) -> bool:
        """Check if user input flows to the suspicious function."""
        # Look for assignment from user-input sources nearby
        patterns = [
            r"request\.(args|form|json|GET|POST)",
            r"input\s*\(",
            r"sys\.argv",
            r"getenv\(",
        ]
        
        for pattern in patterns:
            if re.search(pattern, context):
                return True
        
        return False
    
    @staticmethod
    def _has_hardcoded_input(context: str) -> bool:
        """Check if the suspicious call uses obviously hardcoded input."""
        # String literals directly passed
        return bool(re.search(r'eval\s*\(\s*["\']|exec\s*\(\s*["\']', context))
    
    @staticmethod
    def _uses_parameterized_elsewhere(code: str) -> bool:
        """Check if code uses parameterized queries elsewhere."""
        patterns = [
            r"execute\s*\(\s*['\"].*?['\"].*?,\s*\(",
            r"query\s*\(\s*['\"].*?\?",
        ]
        
        for pattern in patterns:
            if re.search(pattern, code):
                return True
        return False
    
    @staticmethod
    def _has_hardcoded_values(context: str) -> bool:
        """Check if the SQL uses only hardcoded values."""
        return not bool(re.search(r"(user_|request\.|param\(|getenv)", context))
    
    @staticmethod
    def _looks_like_real_credential(context: str) -> bool:
        """Check if the value looks like a real credential."""
        # Real looking patterns: long base64, UUIDs, API key patterns, etc.
        patterns = [
            r"(?i)sk_[a-z0-9]{20,}",  # Stripe-like key
            r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}",  # UUID
            r"[A-Za-z0-9+/]{40,}={0,2}",  # Base64-like
        ]
        
        for pattern in patterns:
            if re.search(pattern, context):
                return True
        
        return False
