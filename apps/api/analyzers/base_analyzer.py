"""
Base analyzer class defining the interface for language-specific analyzers.
"""

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
    
    def find_line_numbers(self, pattern: str) -> List[int]:
        """Find all line numbers matching a pattern.
        
        Args:
            pattern: Pattern to search for (exact match)
            
        Returns:
            List of line numbers (1-indexed)
        """
        line_numbers = []
        for i, line in enumerate(self.lines, 1):
            if pattern in line:
                line_numbers.append(i)
        return line_numbers
