"""
JavaScript code analyzer using pattern-based detection for security vulnerabilities.
"""

import re
from typing import List
from uuid import uuid4

from analyzers.base_analyzer import BaseAnalyzer
from schemas.analysis import Vulnerability


class JavaScriptAnalyzer(BaseAnalyzer):
    """Analyzer for JavaScript/TypeScript code using pattern-based detection."""

    def analyze(self) -> List[Vulnerability]:
        self.vulnerabilities = []

        self._detect_eval()
        self._detect_innerHTML()
        self._detect_document_write()
        self._detect_hardcoded_secrets()
        self._detect_sql_concatenation()
        self._detect_weak_crypto()
        self._detect_dangerous_method_calls()
        self._detect_storage_secrets()
        self._detect_child_process()
        self._detect_postmessage_sensitive()
        self._detect_missing_auth()

        return self.vulnerabilities

    def _detect_eval(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if re.search(r"\beval\s*\(", line) and not self._is_comment(line):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Use of eval()",
                        description="eval() executes arbitrary JavaScript code, creating critical security risks.",
                        severity="critical",
                        cwe_id="CWE-95",
                        owasp_category="A03:2021 - Injection",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Avoid eval(). Use JSON.parse() or safer parsing logic.",
                        secure_fix="// Replace eval() with safer parser functions",
                    )
                )

    def _detect_innerHTML(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if re.search(r"\.innerHTML\s*=", line) and not self._is_comment(line):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Unsafe innerHTML Assignment",
                        description="innerHTML assignment with untrusted data can lead to XSS.",
                        severity="high",
                        cwe_id="CWE-79",
                        owasp_category="A03:2021 - Injection",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use textContent for text or sanitize HTML content.",
                        secure_fix="element.textContent = userInput;",
                    )
                )

    def _detect_document_write(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if re.search(r"document\.write\s*\(", line) and not self._is_comment(line):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Use of document.write()",
                        description="document.write() can introduce XSS vulnerabilities.",
                        severity="high",
                        cwe_id="CWE-79",
                        owasp_category="A03:2021 - Injection",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use DOM APIs such as createElement/appendChild.",
                        secure_fix="document.body.appendChild(element);",
                    )
                )

    def _detect_hardcoded_secrets(self) -> None:
        secret_patterns = {
            "api_key": r"api_key\s*[:=]\s*['\"]([a-zA-Z0-9_-]+)['\"]",
            "token": r"token\s*[:=]\s*['\"]([a-zA-Z0-9_-]+)['\"]",
            "password": r"password\s*[:=]\s*['\"]([^'\"]*)['\"]",
            "secret": r"secret\s*[:=]\s*['\"]([a-zA-Z0-9_-]+)['\"]",
            "access_key": r"access_key\s*[:=]\s*['\"]([a-zA-Z0-9_-]+)['\"]",
        }

        for i, line in enumerate(self.lines, 1):
            if self._is_comment(line):
                continue
            for secret_type, pattern in secret_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=f"Hardcoded {secret_type.capitalize()}",
                            description=f"Hardcoded {secret_type} found in source code.",
                            severity="high",
                            cwe_id="CWE-798",
                            owasp_category="A02:2021 - Cryptographic Failures",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use environment variables or secure secret storage.",
                            secure_fix=f"const {secret_type} = process.env.{secret_type.upper()};",
                        )
                    )

    def _detect_sql_concatenation(self) -> None:
        sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE"]
        for i, line in enumerate(self.lines, 1):
            if any(keyword in line.upper() for keyword in sql_keywords):
                if any(op in line for op in ["+", "`", "concat", "format"]) and not self._is_comment(line):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="SQL Query String Concatenation",
                            description="SQL query appears to use string concatenation with user input.",
                            severity="high",
                            cwe_id="CWE-89",
                            owasp_category="A03:2021 - Injection",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use parameterized queries or prepared statements.",
                            secure_fix="connection.query('SELECT * FROM users WHERE id = ?', [userId]);",
                        )
                    )

    def _detect_weak_crypto(self) -> None:
        weak_patterns = [
            (r"crypto\.createCipher\s*\(", "createCipher (deprecated)", "CWE-327"),
            (r"require\s*\(\s*['\"]md5['\"]\s*\)", "MD5 hashing", "CWE-327"),
            (r"require\s*\(\s*['\"]sha1['\"]\s*\)", "SHA1 hashing", "CWE-327"),
        ]

        for i, line in enumerate(self.lines, 1):
            for pattern, description, cwe in weak_patterns:
                if re.search(pattern, line, re.IGNORECASE) and not self._is_comment(line):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=f"Weak Cryptography: {description}",
                            description=f"{description} is cryptographically weak.",
                            severity="medium",
                            cwe_id=cwe,
                            owasp_category="A02:2021 - Cryptographic Failures",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use modern cryptography such as bcrypt/scrypt for passwords.",
                            secure_fix="const hash = await bcrypt.hash(password, 10);",
                        )
                    )

    def _detect_dangerous_method_calls(self) -> None:
        dangerous_patterns = [
            (r"setTimeout\s*\(\s*['\"]", "eval in setTimeout", "CWE-95", "high"),
            (r"setInterval\s*\(\s*['\"]", "eval in setInterval", "CWE-95", "high"),
            (r"Function\s*\(\s*['\"][^'\"]*['\"]\s*\)", "Dynamic Function constructor", "CWE-95", "high"),
        ]

        for i, line in enumerate(self.lines, 1):
            for pattern, desc, cwe, severity in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE) and not self._is_comment(line):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=desc,
                            description=f"Using {desc} with string code execution is dangerous.",
                            severity=severity,
                            cwe_id=cwe,
                            owasp_category="A03:2021 - Injection",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use regular functions instead of dynamic code execution.",
                            secure_fix="// Use named functions instead of dynamic execution",
                        )
                    )

    def _detect_storage_secrets(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if self._is_comment(line):
                continue
            if re.search(r"(localStorage|sessionStorage)\.setItem\s*\(", line):
                if any(k in line.lower() for k in ["token", "secret", "password", "key", "api", "credential"]):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Sensitive Data in Browser Storage",
                            description="Storing secrets in localStorage/sessionStorage exposes them to XSS.",
                            severity="high",
                            cwe_id="CWE-922",
                            owasp_category="A01:2021 - Broken Access Control",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use secure httpOnly cookies for sensitive session data.",
                            secure_fix="// Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict",
                        )
                    )

    def _detect_child_process(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if self._is_comment(line):
                continue
            if re.search(r"(child_process\.exec|spawn|execFile)\s*\(", line):
                if "shell" in line or "+" in line or "`" in line:
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Command Injection via child_process",
                            description="child_process execution with shell/string concatenation allows injection.",
                            severity="critical",
                            cwe_id="CWE-78",
                            owasp_category="A03:2021 - Injection",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use execFile with explicit argument array and no shell.",
                            secure_fix="execFile('command', [arg], callback);",
                        )
                    )

    def _detect_postmessage_sensitive(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if self._is_comment(line):
                continue
            if re.search(r"\.postMessage\s*\(", line):
                if any(k in line.lower() for k in ["token", "secret", "password", "key", "credential", "session"]):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Sensitive Data via postMessage",
                            description="postMessage can leak sensitive data across origins if misused.",
                            severity="medium",
                            cwe_id="CWE-201",
                            owasp_category="A01:2021 - Broken Access Control",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Avoid sending secrets over postMessage and always validate origin.",
                            secure_fix="window.parent.postMessage({ event: 'ok' }, 'https://trusted.example');",
                        )
                    )

    def _detect_missing_auth(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if self._is_comment(line):
                continue
            if re.search(r"(delete|remove|drop|update)\s*\(\s*(id|req\.params\.id)", line, re.IGNORECASE):
                if "auth" not in line.lower() and "permission" not in line.lower() and "if" not in line:
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Missing Authorization Check",
                            description="Sensitive operation detected without obvious authorization check.",
                            severity="high",
                            cwe_id="CWE-639",
                            owasp_category="A01:2021 - Broken Access Control",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Verify requester authorization before sensitive operations.",
                            secure_fix="if (!isAuthorized(user, resource)) throw new Error('Unauthorized');",
                        )
                    )

    def _is_comment(self, line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("//") or stripped.startswith("/*")

    def _create_vulnerability(
        self,
        title: str,
        description: str,
        severity: str,
        cwe_id: str,
        owasp_category: str,
        line_number: int,
        code_snippet: str,
        recommendation: str,
        secure_fix: str,
    ) -> Vulnerability:
        return Vulnerability(
            id=str(uuid4()),
            title=title,
            description=description,
            severity=severity,
            cwe_id=cwe_id,
            owasp_category=owasp_category,
            line_number=line_number,
            column_number=None,
            code_snippet=code_snippet,
            fix_suggestion=recommendation,
            secure_fix_code=secure_fix,
            confidence=0.85,
            rule_id=f"JS-{cwe_id.split('-')[1]}",
        )