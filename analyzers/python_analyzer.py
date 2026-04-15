"""
Python code analyzer using AST (Abstract Syntax Tree) for security vulnerability detection.
"""

import ast
import re
from typing import List, Optional
from uuid import uuid4

from analyzers.base_analyzer import BaseAnalyzer
from schemas.analysis import Vulnerability


class PythonAnalyzer(BaseAnalyzer):
    """Analyzer for Python code using AST-based detection."""

    def __init__(self, code: str):
        super().__init__(code)
        self.tree: Optional[ast.AST] = None
        self.vulnerabilities: List[Vulnerability] = []

        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            # If code has syntax errors, we still try pattern-based detection.
            pass

    def analyze(self) -> List[Vulnerability]:
        """Analyze Python code for vulnerabilities."""
        self.vulnerabilities = []

        self._detect_eval_exec()
        self._detect_hardcoded_secrets()
        self._detect_sql_injection()
        self._detect_command_injection()
        self._detect_unsafe_deserialization()
        self._detect_weak_hashing()
        self._detect_debug_mode()
        self._detect_yaml_unsafe_load()
        self._detect_tempfile_misuse()
        self._detect_assert_for_security()
        self._detect_insecure_random()
        self._detect_requests_insecure_ssl()

        return self.vulnerabilities

    def _detect_eval_exec(self) -> None:
        """Detect eval() and exec() usage."""
        if self.tree is None:
            for i, line in enumerate(self.lines, 1):
                if re.search(r"\beval\s*\(", line) and not line.strip().startswith("#"):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Use of eval()",
                            description="eval() executes arbitrary Python code, creating critical security risks.",
                            severity="critical",
                            cwe_id="CWE-95",
                            owasp_category="A03:2021 - Injection",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Avoid eval(). Use ast.literal_eval() for safe parsing, or json.loads() for JSON.",
                            secure_fix="import ast\nvalue = ast.literal_eval(user_input)",
                        )
                    )

                if re.search(r"\bexec\s*\(", line) and not line.strip().startswith("#"):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Use of exec()",
                            description="exec() executes arbitrary Python code dynamically.",
                            severity="critical",
                            cwe_id="CWE-95",
                            owasp_category="A03:2021 - Injection",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Replace exec() with safer alternatives like importlib or explicit branching.",
                            secure_fix="# Avoid dynamic code execution with exec",
                        )
                    )
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func_name = node.func.id if isinstance(node.func, ast.Name) else None
                if func_name == "eval":
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Use of eval()",
                            description="eval() executes arbitrary Python code, creating critical security risks.",
                            severity="critical",
                            cwe_id="CWE-95",
                            owasp_category="A03:2021 - Injection",
                            line_number=node.lineno,
                            code_snippet=self.get_line_snippet(node.lineno),
                            recommendation="Avoid eval(). Use ast.literal_eval() or json.loads().",
                            secure_fix="import ast\nvalue = ast.literal_eval(user_input)",
                        )
                    )
                elif func_name == "exec":
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Use of exec()",
                            description="exec() executes arbitrary Python code dynamically.",
                            severity="critical",
                            cwe_id="CWE-95",
                            owasp_category="A03:2021 - Injection",
                            line_number=node.lineno,
                            code_snippet=self.get_line_snippet(node.lineno),
                            recommendation="Replace exec() with safer alternatives.",
                            secure_fix="# Avoid dynamic code execution with exec",
                        )
                    )

    def _detect_hardcoded_secrets(self) -> None:
        secret_patterns = {
            "password": (r"password\s*=\s*['\"]([^'\"]*)['\"]", "Password"),
            "api_key": (r"api_key\s*=\s*['\"]([^'\"]*)['\"]", "API Key"),
            "secret": (r"secret\s*=\s*['\"]([^'\"]*)['\"]", "Secret"),
            "token": (r"token\s*=\s*['\"]([^'\"]*)['\"]", "Token"),
            "private_key": (r"private_key\s*=\s*['\"]([^'\"]*)['\"]", "Private Key"),
            "access_key": (r"access_key\s*=\s*['\"]([^'\"]*)['\"]", "Access Key"),
        }

        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            for key_type, (pattern, label) in secret_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if "TODO" in line or "FIXME" in line:
                        continue
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=f"Hardcoded {label}",
                            description=f"Hardcoded {label.lower()} found in source code.",
                            severity="high",
                            cwe_id="CWE-798",
                            owasp_category="A02:2021 - Cryptographic Failures",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation=f"Use environment variables or secret vaults for {label.lower()}.",
                            secure_fix=f"import os\n{key_type} = os.getenv('{key_type.upper()}')",
                        )
                    )

    def _detect_sql_injection(self) -> None:
        sql_concat_patterns = [
            r"['\"].*%\s*\(",
            r"f['\"].*\{",
            r"\.format\s*\(",
            r"\+\s*str\(",
        ]

        for i, line in enumerate(self.lines, 1):
            if re.search(r"(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)\s", line, re.IGNORECASE):
                if any(re.search(pattern, line) for pattern in sql_concat_patterns):
                    if not line.strip().startswith("#"):
                        self.vulnerabilities.append(
                            self._create_vulnerability(
                                title="Potential SQL Injection",
                                description="SQL query appears to be constructed with string formatting/concatenation.",
                                severity="high",
                                cwe_id="CWE-89",
                                owasp_category="A03:2021 - Injection",
                                line_number=i,
                                code_snippet=line.strip(),
                                recommendation="Use parameterized queries to prevent SQL injection.",
                                secure_fix="cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                            )
                        )

    def _detect_command_injection(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if "os.system" in line and not line.strip().startswith("#"):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Command Injection via os.system()",
                        description="os.system() with unsanitized input allows arbitrary command execution.",
                        severity="critical",
                        cwe_id="CWE-78",
                        owasp_category="A03:2021 - Injection",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use subprocess.run() with shell=False and list args.",
                        secure_fix="import subprocess\nsubprocess.run(['command', 'arg1'], shell=False)",
                    )
                )

            if "shell=True" in line and not line.strip().startswith("#"):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Command Injection via subprocess with shell=True",
                        description="subprocess with shell=True allows shell injection attacks.",
                        severity="high",
                        cwe_id="CWE-78",
                        owasp_category="A03:2021 - Injection",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use subprocess.run() with shell=False.",
                        secure_fix="subprocess.run(['ls', '-la'], shell=False)",
                    )
                )

    def _detect_unsafe_deserialization(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if "pickle.loads" in line and not line.strip().startswith("#"):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Unsafe Deserialization with pickle.loads()",
                        description="pickle.loads() can execute arbitrary code during deserialization.",
                        severity="high",
                        cwe_id="CWE-502",
                        owasp_category="A08:2021 - Software and Data Integrity Failures",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use json.loads() for untrusted data.",
                        secure_fix="import json\ndata = json.loads(untrusted_data)",
                    )
                )

    def _detect_weak_hashing(self) -> None:
        weak_hash_patterns = [
            (r"hashlib\.(md5|sha1)", "MD5/SHA1"),
            (r"crypt\.crypt", "crypt module"),
        ]

        for i, line in enumerate(self.lines, 1):
            for pattern, algo_name in weak_hash_patterns:
                if re.search(pattern, line, re.IGNORECASE) and not line.strip().startswith("#"):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=f"Weak Hashing Algorithm ({algo_name})",
                            description=f"{algo_name} is cryptographically weak and unsuitable for password hashing.",
                            severity="high",
                            cwe_id="CWE-327",
                            owasp_category="A02:2021 - Cryptographic Failures",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use bcrypt, scrypt, or argon2.",
                            secure_fix="import bcrypt\nhashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())",
                        )
                    )

    def _detect_debug_mode(self) -> None:
        debug_patterns = [
            (r"debug\s*=\s*True", "Flask/Django Debug Mode"),
            (r"DEBUG\s*=\s*True", "Production Debug Flag"),
        ]

        for i, line in enumerate(self.lines, 1):
            for pattern, mode_name in debug_patterns:
                if re.search(pattern, line) and not line.strip().startswith("#"):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title=f"Debug Mode Enabled ({mode_name})",
                            description="Debug mode enabled in production exposes sensitive information.",
                            severity="medium",
                            cwe_id="CWE-489",
                            owasp_category="A05:2021 - Security Misconfiguration",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Disable debug mode in production.",
                            secure_fix="import os\ndebug = os.getenv('DEBUG', 'False') == 'True'",
                        )
                    )

    def _detect_yaml_unsafe_load(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            if re.search(r"yaml\.load\s*\(", line) and "SafeLoader" not in line and "safe_load" not in line:
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Unsafe YAML Deserialization",
                        description="yaml.load() without SafeLoader can deserialize arbitrary Python objects.",
                        severity="high",
                        cwe_id="CWE-502",
                        owasp_category="A08:2021 - Software and Data Integrity Failures",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use yaml.safe_load() or yaml.load(..., Loader=yaml.SafeLoader).",
                        secure_fix="import yaml\ndata = yaml.safe_load(untrusted_yaml)",
                    )
                )

    def _detect_tempfile_misuse(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            if re.search(r"tempfile\.mktemp\s*\(", line):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Insecure tempfile.mktemp() Usage",
                        description="tempfile.mktemp() is insecure due to race conditions.",
                        severity="high",
                        cwe_id="CWE-377",
                        owasp_category="A05:2021 - Security Misconfiguration",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use tempfile.mkstemp() or NamedTemporaryFile.",
                        secure_fix="import tempfile\nfd, path = tempfile.mkstemp()",
                    )
                )
            if re.search(r"['\"]/(tmp|var/tmp)['\"]", line) and ("open" in line or "write" in line):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="Hardcoded Insecure Temp Path",
                        description="Hardcoded temp paths are susceptible to symlink attacks.",
                        severity="medium",
                        cwe_id="CWE-377",
                        owasp_category="A05:2021 - Security Misconfiguration",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Use tempfile module for secure temporary files.",
                        secure_fix="import tempfile\nwith tempfile.NamedTemporaryFile() as tmp:\n    tmp.write(data)",
                    )
                )

    def _detect_assert_for_security(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            if re.search(r"\bassert\s+", line):
                if any(k in line.lower() for k in ["auth", "permission", "trusted", "valid", "access", "user"]):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Assert Used for Security Check",
                            description="assert statements can be removed with Python -O and should not enforce security.",
                            severity="medium",
                            cwe_id="CWE-670",
                            owasp_category="A04:2021 - Insecure Design",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use explicit condition checks with raise/return.",
                            secure_fix="if not user_trusted:\n    raise PermissionError('User not trusted')",
                        )
                    )

    def _detect_insecure_random(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            if re.search(r"random\.(randint|choice|shuffle|random)\s*\(", line):
                if any(k in line.lower() for k in ["token", "secret", "password", "key", "nonce", "salt"]):
                    self.vulnerabilities.append(
                        self._create_vulnerability(
                            title="Insecure Random for Cryptographic Use",
                            description="random module is not cryptographically secure.",
                            severity="high",
                            cwe_id="CWE-330",
                            owasp_category="A02:2021 - Cryptographic Failures",
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use secrets module for token/key generation.",
                            secure_fix="import secrets\ntoken = secrets.token_hex(32)",
                        )
                    )

    def _detect_requests_insecure_ssl(self) -> None:
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("#"):
                continue
            if re.search(r"requests\.(get|post|put|delete|patch|request)\s*\(", line) and (
                "verify=False" in line or "verify = False" in line
            ):
                self.vulnerabilities.append(
                    self._create_vulnerability(
                        title="SSL Certificate Verification Disabled",
                        description="verify=False disables TLS certificate validation and enables MITM attacks.",
                        severity="high",
                        cwe_id="CWE-295",
                        owasp_category="A02:2021 - Cryptographic Failures",
                        line_number=i,
                        code_snippet=line.strip(),
                        recommendation="Keep TLS verification enabled and use trusted CA certs.",
                        secure_fix="response = requests.get(url)  # verify=True by default",
                    )
                )

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
            confidence=0.9,
            rule_id=f"PY-{cwe_id.split('-')[1]}",
        )