"""
OWASP Top 10 mapping and categorization.
"""

from typing import Dict, Optional


class OWASPMapper:
    """Maps vulnerabilities to OWASP Top 10 categories."""
    
    OWASP_CATEGORIES = {
        "A01:2021 – Broken Access Control": {
            "id": "A01",
            "description": "Failure to properly restrict user access to resources.",
            "prevalence": "high",
            "related_cwes": ["CWE-639", "CWE-284"],
        },
        "A02:2021 – Cryptographic Failures": {
            "id": "A02",
            "description": "Failure to protect sensitive data through encryption.",
            "prevalence": "high",
            "related_cwes": ["CWE-327", "CWE-326", "CWE-330"],
        },
        "A03:2021 – Injection": {
            "id": "A03",
            "description": "Injection of untrusted data into dynamic queries or commands.",
            "prevalence": "high",
            "related_cwes": ["CWE-94", "CWE-95", "CWE-78", "CWE-89"],
        },
        "A04:2021 – Insecure Design": {
            "id": "A04",
            "description": "Lack of secure design patterns and threat modeling.",
            "prevalence": "high",
            "related_cwes": ["CWE-697"],
        },
        "A05:2021 – Security Misconfiguration": {
            "id": "A05",
            "description": "Insecure default configurations or incomplete setup.",
            "prevalence": "high",
            "related_cwes": ["CWE-16", "CWE-489"],
        },
        "A06:2021 – Vulnerable and Outdated Components": {
            "id": "A06",
            "description": "Use of libraries with known vulnerabilities.",
            "prevalence": "high",
            "related_cwes": ["CWE-1035"],
        },
        "A07:2021 – Authentication Failures": {
            "id": "A07",
            "description": "Broken authentication mechanisms.",
            "prevalence": "high",
            "related_cwes": ["CWE-306", "CWE-307"],
        },
        "A08:2021 – Software and Data Integrity Failures": {
            "id": "A08",
            "description": "Insufficient integrity verification of code or data.",
            "prevalence": "medium",
            "related_cwes": ["CWE-353", "CWE-502"],
        },
        "A09:2021 – Logging and Monitoring Failures": {
            "id": "A09",
            "description": "Insufficient detection of security incidents.",
            "prevalence": "medium",
            "related_cwes": ["CWE-778"],
        },
        "A10:2021 – Server-Side Request Forgery": {
            "id": "A10",
            "description": "SSRF vulnerabilities allowing unauthorized requests.",
            "prevalence": "medium",
            "related_cwes": ["CWE-918"],
        },
    }
    
    @staticmethod
    def get_category(cwe_id: str) -> str:
        """Get OWASP category for a CWE.
        
        Args:
            cwe_id: CWE identifier (e.g., "CWE-95")
            
        Returns:
            OWASP category string
        """
        cwe_map = {
            "CWE-95": "A03:2021 – Injection",
            "CWE-78": "A03:2021 – Injection",
            "CWE-89": "A03:2021 – Injection",
            "CWE-79": "A03:2021 – Injection",
            "CWE-327": "A02:2021 – Cryptographic Failures",
            "CWE-798": "A02:2021 – Cryptographic Failures",
            "CWE-502":  "A08:2021 – Software and Data Integrity Failures",
            "CWE-611": "A03:2021 – Injection",
            "CWE-489": "A05:2021 – Security Misconfiguration",
        }
        return cwe_map.get(cwe_id, "A01:2021 – Broken Access Control")
    
    @staticmethod
    def get_category_info(owasp_category: str) -> Dict:
        """Get information about an OWASP category.
        
        Args:
            owasp_category: OWASP category string
            
        Returns:
            Dictionary with category metadata
        """
        return OWASPMapper.OWASP_CATEGORIES.get(owasp_category, {})
