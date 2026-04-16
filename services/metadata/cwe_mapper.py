"""
CWE (Common Weakness Enumeration) mapping and metadata.
"""

from typing import Dict, Optional


class CWEMapper:
    """Provides CWE IDs and detailed information for vulnerabilities."""
    
    CWE_METADATA = {
        "CWE-95": {
            "title": "Improper Neutralization of Directives in Dynamically Evaluated Code",
            "description": "Evaluation of code with externally-influenced instructions.",
            "severity_base": "high",
            "exploitability": "high",
            "impact": "Arbitrary code execution",
        },
        "CWE-78": {
            "title": "Improper Neutralization of Special Elements used in an OS Command",
            "description": "OS command injection vulnerability.",
            "severity_base": "high",
            "exploitability": "high",
            "impact": "System compromise",
        },
        "CWE-89": {
            "title": "Improper Neutralization of Special Elements used in an SQL Command",
            "description": "SQL injection vulnerability.",
            "severity_base": "high",
            "exploitability": "high",
            "impact": "Data breach or modification",
        },
        "CWE-79": {
            "title": "Improper Neutralization of Input During Web Page Generation",
            "description": "Cross-site scripting (XSS) vulnerability.",
            "severity_base": "high",
            "exploitability": "medium",
            "impact": "Session hijacking, credential theft",
        },
        "CWE-327": {
            "title": "Use of a Broken or Risky Cryptographic Algorithm",
            "description": "Weak or deprecated cryptographic algorithm usage.",
            "severity_base": "high",
            "exploitability": "medium",
            "impact": "Cryptographic bypass",
        },
        "CWE-798": {
            "title": "Use of Hard-Coded Credentials",
            "description": "Embedded secrets in source code.",
            "severity_base": "high",
            "exploitability": "high",
            "impact": "Unauthorized access",
        },
        "CWE-502": {
            "title": "Deserialization of Untrusted Data",
            "description": "Unsafe deserialization of untrusted input.",
            "severity_base": "high",
            "exploitability": "high",
            "impact": "Arbitrary code execution",
        },
        "CWE-611": {
            "title": "Improper Restriction of XML External Entity Reference",
            "description": "XXE vulnerability allowing data exfiltration.",
            "severity_base": "high",
            "exploitability": "medium",
            "impact": "Information disclosure or DoS",
        },
        "CWE-489": {
            "title": "Active Debug Code",
            "description": "Debug mode or debug code enabled in production.",
            "severity_base": "medium",
            "exploitability": "medium",
            "impact": "Information disclosure",
        },
        "CWE-352": {
            "title": "Cross-Site Request Forgery (CSRF)",
            "description": "CSRF vulnerability allowing unauthorized actions.",
            "severity_base": "high",
            "exploitability": "medium",
            "impact": "Unauthorized state change",
        },
    }
    
    @staticmethod
    def get_cwe_info(cwe_id: str) -> Dict:
        """Get detailed information for a CWE.
        
        Args:
            cwe_id: CWE identifier (e.g., "CWE-95")
            
        Returns:
            Dictionary with CWE metadata
        """
        return CWEMapper.CWE_METADATA.get(cwe_id, {
            "title": cwe_id,
            "description": "Unknown CWE",
            "severity_base": "medium",
            "exploitability": "medium",
        })
    
    @staticmethod
    def get_exploitability(cwe_id: str) -> str:
        """Get exploitability level for a CWE.
        
        Args:
            cwe_id: CWE identifier
            
        Returns:
            Exploitability level: "low", "medium", or "high"
        """
        info = CWEMapper.get_cwe_info(cwe_id)
        return info.get("exploitability", "medium")
