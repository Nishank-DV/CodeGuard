"""
Code analysis service with Phase 3 intelligence enhancements.
Pipeline: detection → filtering → confidence adjustment → deduplication →
          metadata enrichment → remediation guidance → prioritization
"""

from uuid import uuid4
from datetime import datetime
from schemas.analysis import AnalysisResult
from analyzers.python_analyzer import PythonAnalyzer
from analyzers.javascript_analyzer import JavaScriptAnalyzer
from services.risk_scoring import RiskScorer
from services.postprocessing.finding_filter import FindingFilter
from services.postprocessing.confidence_adjuster import ConfidenceAdjuster
from services.postprocessing.deduplicator import Deduplicator
from services.metadata.cwe_mapper import CWEMapper
from services.metadata.context_analyzer import ContextAnalyzer
from services.remediation.fix_generator import RemediationEngine


class AnalysisService:
    """Code analysis with Phase 3 intelligence enhancements."""
    
    @staticmethod
    def analyze_code(code: str, language: str) -> AnalysisResult:
        """Analyze source code with intelligent post-processing pipeline.
        
        Complete analysis pipeline:
        1. Detect vulnerabilities with language-specific analyzer
        2. Filter obvious false positives and demo code
        3. Adjust confidence based on code context
        4. Deduplicate similar findings on same line
        5. Enrich with metadata (CWE, exploitability, OWASP)
        6. Analyze contextual exploitability
        7. Generate detailed remediation guidance
        8. Calculate final prioritization scores
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript)
            
        Returns:
            AnalysisResult with intelligent, de-duped, prioritized vulnerabilities
            
        Raises:
            ValueError: If language is not supported
        """
        language_lower = language.lower()
        
        # 1. Dispatch to appropriate analyzer
        if language_lower == 'python':
            analyzer = PythonAnalyzer(code)
        elif language_lower in ['javascript', 'typescript', 'js', 'ts']:
            analyzer = JavaScriptAnalyzer(code)
        else:
            raise ValueError(f"Language '{language}' not supported. Try: python, javascript")
        
        # Run detection
        vulnerabilities = analyzer.analyze()
        
        # 2. Filter obvious false positives
        vulnerabilities = FindingFilter.filter_findings(vulnerabilities, code)
        
        # 3. Adjust confidence based on context
        vulnerabilities = ConfidenceAdjuster.adjust_findings(vulnerabilities, code)
        
        # 4. Deduplicate identical findings on same line
        vulnerabilities, dedup_info = Deduplicator.deduplicate(vulnerabilities)
        
        # 5-7. Enrich and prioritize each finding
        for vuln in vulnerabilities:
            # Get exploitability from CWE
            vuln.exploitability = CWEMapper.get_exploitability(vuln.cwe_id)
            
            # Analyze contextual exploitability
            rule_type = (vuln.rule_id or "").split("-")[0].lower() if vuln.rule_id else ""
            exploit_level, confidence_adj = ContextAnalyzer.analyze_exploit_likelihood(
                code, vuln.line_number, rule_type
            )
            
            # Apply contextual confidence adjustment
            vuln.exploitability = exploit_level
            vuln.confidence = max(0.0, min(1.0, vuln.confidence + confidence_adj))
            
            # Generate detailed remediation
            RemediationEngine.generate_remediation(vuln, code)
            
            # Recalculate priority after all adjustments
            vuln.priority_score = ConfidenceAdjuster._calculate_priority(vuln)
        
        # Sort by priority (highest first)
        vulnerabilities.sort(key=lambda v: v.priority_score, reverse=True)
        
        # Recalculate risk metrics
        severity_dist = RiskScorer.severity_distribution(vulnerabilities)
        risk_score = RiskScorer.calculate_risk_score(vulnerabilities)
        
        # Build final result
        return AnalysisResult(
            id=str(uuid4()),
            language=language_lower,
            vulnerabilities=vulnerabilities,
            total_issues=len(vulnerabilities),
            critical_count=severity_dist["critical"],
            high_count=severity_dist["high"],
            medium_count=severity_dist["medium"],
            low_count=severity_dist["low"],
            info_count=severity_dist["info"],
            risk_score=risk_score,
            deduplication_info=dedup_info,
            scanned_at=datetime.utcnow(),
        )
