"""
Deduplication layer to merge similar findings and avoid redundant reports.
"""

from typing import List, Dict
from schemas.analysis import Vulnerability


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
        
        # Merge groups
        deduplicated = []
        total_merged = 0
        
        for key, group in groups.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                # Merge multiple findings into one with highest confidence
                merged = Deduplicator._merge_vulns(group)
                deduplicated.append(merged)
                total_merged += len(group) - 1
        
        dedup_info = {
            "total_merged": total_merged,
            "original_count": len(vulns),
            "deduplicated_count": len(deduplicated),
        }
        
        return deduplicated, dedup_info
    
    @staticmethod
    def _merge_vulns(vulns: List[Vulnerability]) -> Vulnerability:
        """Merge multiple identical vulnerabilities into one.
        
        Takes the finding with highest confidence and keeps all details.
        
        Args:
            vulns: List of similar vulnerabilities to merge
            
        Returns:
            Single merged vulnerability
        """
        # Sort by confidence descending
        sorted_vulns = sorted(vulns, key=lambda v: v.confidence, reverse=True)
        best = sorted_vulns[0]
        
        # Use highest confidence from any finding
        best.confidence = sorted_vulns[0].confidence
        
        return best
