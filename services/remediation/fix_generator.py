"""
Fix recommendation generator with detailed remediation guidance.
"""

from typing import Tuple
from schemas.analysis import Vulnerability


class RemediationEngine:
    """Generates remediation guidance for each vulnerability type."""
    
    REMEDIATION_TEMPLATES = {
        "CWE-95": {
            "short_rec": "Avoid eval() and exec(). Use safer alternatives like ast.literal_eval() or json.loads().",
            "detailed": """
The eval() and exec() functions execute arbitrary Python code, creating critical security risks:
1. **Never** use them with untrusted input
2. **Never** pass user-supplied strings to these functions
3. **Risk**: Complete system compromise, data breach, arbitrary code execution

**Safer alternatives:**
- For JSON: Use `json.loads()` instead of `eval()`
- For Python literals: Use `ast.literal_eval()` for safe evaluation
- For dynamic code: Consider restricted execution environments or sandboxing
- For most cases: Redesign to avoid dynamic code execution entirely
            """,
            "priority": "critical",
        },
        "CWE-78": {
            "short_rec": "Never use os.system() with user input. Use subprocess with list arguments.",
            "detailed": """
OS command injection allows attackers to execute arbitrary system commands:
1. **Never** use `os.system()` with user-controlled data
2. **Never** use `shell=True` with user input
3. **Risk**: Complete system compromise, data theft, service disruption

**Safer alternatives:**
- Use `subprocess.run()` with `shell=False` (default) and list of arguments
- Use dedicated libraries: `pathlib` for file ops, `requests` for HTTP, etc.
- If shell needed: Use `shlex.quote()` to escape dangerous characters

**Example:**
```python
# ❌ VULNERABLE
os.system(f"ls {user_dir}")

# ✅ SAFE
subprocess.run(["ls", user_dir])
```
            """,
            "priority": "critical",
        },
        "CWE-89": {
            "short_rec": "Use parameterized queries instead of string concatenation for SQL.",
            "detailed": """
SQL injection allows attackers to manipulate database queries:
1. **Never** concatenate user input into SQL strings
2. **Always** use parameterized queries or ORMs
3. **Risk**: Data breach, modification, deletion, unauthorized access

**Safer alternatives:**
- Use parameterized queries with `?` or `:param` placeholders
- Use ORM frameworks: SQLAlchemy, Django ORM, etc.
- Use prepared statements in your database library

**Example:**
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ SAFE - Parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ✅ SAFE - ORM
user = User.query.filter_by(id=user_id).first()
```
            """,
            "priority": "critical",
        },
        "CWE-79": {
            "short_rec": "Use textContent instead of innerHTML, or sanitize HTML properly.",
            "detailed": """
Cross-site scripting (XSS) allows attackers to inject malicious scripts:
1. **Never** assign untrusted HTML to `innerHTML`
2. **Always** use `textContent` for plain text
3. **Risk**: Session hijacking, credential theft, malware infection

**Safer alternatives:**
- Use `textContent` for plain text (no HTML parsing)
- Use template literals with innerHTML only for trusted content
- Use HTML sanitization libraries like DOMPurify
- Use framework innerHTML escaping (React, Vue, Angular)

**Example:**
```javascript
// ❌ VULNERABLE
element.innerHTML = userData;

// ✅ SAFE - Plain text
element.textContent = userData;

// ✅ SAFE - Sanitized HTML
element.innerHTML = DOMPurify.sanitize(userData);
```
            """,
            "priority": "critical",
        },
        "CWE-798": {
            "short_rec": "Move hardcoded credentials to environment variables or secure vaults.",
            "detailed": """
Hardcoded credentials in source code expose secrets to anyone with code access:
1. **Never** commit credentials to version control
2. **Always** use environment variables or secure vaults
3. **Risk**: Unauthorized access, account takeover, data breach

**Safer alternatives:**
- Use environment variables: `os.getenv('API_KEY')`
- Use .env files (with .gitignore, NOT committed)
- Use cloud vaults: AWS Secrets Manager, HashiCorp Vault, etc.
- Use CI/CD secrets management

**Example:**
```python
# ❌ VULNERABLE
API_KEY = "sk_live_51234567890"

# ✅ SAFE
import os
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```
            """,
            "priority": "high",
        },
        "CWE-327": {
            "short_rec": "Use strong cryptographic algorithms like bcrypt, Argon2, or SHA-256.",
            "detailed": """
Weak cryptographic algorithms can be broken by attackers:
1. **Never** use MD5, SHA1, or single rounds of hashing
2. **Always** use strong, modern algorithms
3. **Risk**: Credential compromise, data encryption bypass

**Safer alternatives for passwords:**
- Use bcrypt, scrypt, or Argon2 with proper parameters
- Never use MD5 or SHA1 for security purposes

**Safer alternatives for general hashing:**
- Use SHA-256 or newer for non-password hashing
- Use PBKDF2 with many iterations if bcrypt unavailable

**Example:**
```python
# ❌ VULNERABLE
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()

# ✅ SAFE
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
```
            """,
            "priority": "high",
        },
    }
    
    @staticmethod
    def generate_remediation(vuln: Vulnerability, code: str) -> None:
        """Generate detailed remediation guidance for a vulnerability.
        
        Updates the vulnerability object with detailed remediation info.
        
        Args:
            vuln: Vulnerability object to update
            code: Original source code for context
        """
        cwe_id = vuln.cwe_id
        template = RemediationEngine.REMEDIATION_TEMPLATES.get(cwe_id)
        
        if template:
            vuln.fix_suggestion = template["short_rec"]
            vuln.detailed_remediation = template["detailed"].strip()
            vuln.remediation_priority = template["priority"]
        
        # Set business impact based on vulnerability type
        vuln.business_impact = RemediationEngine._determine_business_impact(cwe_id)
    
    @staticmethod
    def _determine_business_impact(cwe_id: str) -> str:
        """Determine business impact of a vulnerability type.
        
        Args:
            cwe_id: CWE identifier
            
        Returns:
            Business impact description
        """
        mapping = {
            "CWE-95": "arbitrary_code_execution - complete system compromise",
            "CWE-78": "command_injection - system compromise",
            "CWE-89": "data_breach - unauthorized database access",
            "CWE-79": "user_compromise - session hijacking, credential theft",
            "CWE-798": "unauthorized_access - account takeover",
            "CWE-327": "encryption_bypass - cryptographic failure",
            "CWE-502": "arbitrary_code_execution - deserialization attack",
            "CWE-611": "information_disclosure - XXE data exfiltration",
        }
        
        return mapping.get(cwe_id, "security_violation - potential compromise")
