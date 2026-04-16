# CodeGuard Detection Rules - Phase 2

## Python Analyzer (8 Rules)

### 1. Eval/Exec Execution (CRITICAL)

**Rule ID:** `PYTHON-EVAL-01`  
**Severity:** CRITICAL  
**CWE:** CWE-95 (Improper Neutralization of Directives in Dynamically Evaluated Code)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.99

**Description:**
Direct usage of `eval()` or `exec()` functions allows arbitrary code execution. These functions should never be used with untrusted input.

**Vulnerable Pattern:**
```python
# ❌ CRITICAL - Direct eval usage
result = eval(user_input)

# ❌ CRITICAL - Direct exec usage
exec(user_code)

# ❌ CRITICAL - eval in try/except (still dangerous)
try:
    result = eval(user_input)
except:
    pass
```

**Secure Alternative:**
```python
# ✅ Use json.loads for JSON parsing
import json
result = json.loads(user_input)

# ✅ Use ast.literal_eval for safe Python literals
import ast
result = ast.literal_eval(user_input)

# ✅ Use restricted evaluation libraries
import numexpr
result = numexpr.evaluate(user_expr)
```

**Detection Method:** AST traversal looking for `Call` nodes with `func.id == 'eval'` or `'exec'`

---

### 2. Hardcoded Secrets (HIGH)

**Rule ID:** `PYTHON-SECRETS-02`  
**Severity:** HIGH  
**CWE:** CWE-798 (Use of Hard-Coded Credentials)  
**OWASP:** A02:2021 – Cryptographic Failures  
**Confidence:** 0.87

**Description:**
Hardcoded credentials expose sensitive information in source code. Secrets should be stored in environment variables or secure vaults.

**Vulnerable Pattern:**
```python
# ❌ HIGH - Hardcoded password
password = "admin123"

# ❌ HIGH - Hardcoded API key
api_key = "sk-1234567890abcdef"

# ❌ HIGH - Hardcoded token
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# ❌ HIGH - Hardcoded database credentials
db_password = "postgres_secret_123"

# ❌ HIGH - In configuration
config = {
    "api_key": "sk-secret",
    "db_password": "secret123"
}
```

**Secure Alternative:**
```python
# ✅ Use environment variables
import os
password = os.getenv('DB_PASSWORD')
api_key = os.getenv('API_KEY')

# ✅ Use .env files
from dotenv import load_dotenv
load_dotenv()
auth_token = os.getenv('AUTH_TOKEN')

# ✅ Use secure vaults (HashiCorp Vault, AWS Secrets Manager)
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='db_password')
```

**Detection Method:** Regex patterns matching `password=`, `api_key=`, `token=`, `secret=` assignments with string literals

---

### 3. SQL Injection (HIGH)

**Rule ID:** `PYTHON-SQL-03`  
**Severity:** HIGH  
**CWE:** CWE-89 (Improper Neutralization of Special Elements used in an SQL Command)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.92

**Description:**
SQL queries built via string concatenation or formatting are vulnerable to injection attacks when user input is not properly sanitized.

**Vulnerable Pattern:**
```python
# ❌ HIGH - String concatenation
user_id = request.args.get('id')
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)

# ❌ HIGH - f-string formatting
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ❌ HIGH - .format() method
query = "SELECT * FROM users WHERE email = {}".format(user_email)
cursor.execute(query)

# ❌ HIGH - String formatting with %
query = "DELETE FROM users WHERE id = %s" % (user_id,)
cursor.execute(query)
```

**Secure Alternative:**
```python
# ✅ Use parameterized queries
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# ✅ Use ORM (SQLAlchemy)
from sqlalchemy import select
stmt = select(User).where(User.id == user_id)

# ✅ Use prepared statements
conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✅ Use query builders
query = Query('users').where('id', '=', user_id)
```

**Detection Method:** AST traversal detecting SQL strings (checking for "SELECT", "INSERT", "UPDATE", "DELETE") combined with BinOp or JoinedStr nodes

---

### 4. Command Injection (HIGH/CRITICAL)

**Rule ID:** `PYTHON-CMD-04`  
**Severity:** HIGH (CRITICAL if shell=True)  
**CWE:** CWE-78 (Improper Neutralization of Special Elements used in an OS Command)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.98

**Description:**
Direct execution of OS commands with user input via `os.system()` or `shell=True` allows command injection.

**Vulnerable Pattern:**
```python
# ❌ CRITICAL - os.system with user input
import os
filename = request.args.get('file')
os.system("ls " + filename)

# ❌ CRITICAL - subprocess with shell=True
import subprocess
subprocess.run("echo " + user_input, shell=True)

# ❌ CRITICAL - os.popen
os.popen("cat " + filepath)

# ❌ HIGH - command as string with user data
cmd = f"wget {user_url} -O file.txt"
os.system(cmd)
```

**Secure Alternative:**
```python
# ✅ Use subprocess without shell
import subprocess
subprocess.run(["ls", filename])

# ✅ Use subprocess.run with list of args
subprocess.run(["echo", user_input])

# ✅ Use pathlib for file operations
from pathlib import Path
content = Path(filename).read_text()

# ✅ Use dedicated libraries
import requests
response = requests.get(user_url)
```

**Detection Method:** AST traversal detecting `os.system()`, `subprocess.call()`, `os.popen()` calls; checking for `shell=True` keyword argument

---

### 5. Unsafe Deserialization (HIGH)

**Rule ID:** `PYTHON-DESER-05`  
**Severity:** HIGH  
**CWE:** CWE-502 (Deserialization of Untrusted Data)  
**OWASP:** A08:2021 – Software and Data Integrity Failures  
**Confidence:** 0.99

**Description:**
Using `pickle.loads()` or similar unsafe deserialization functions with untrusted data can lead to arbitrary code execution.

**Vulnerable Pattern:**
```python
# ❌ HIGH - pickle.loads with untrusted data
import pickle
user_data = request.data
obj = pickle.loads(user_data)

# ❌ HIGH - pickle.load from file
with open('cache.pkl', 'rb') as f:
    data = pickle.load(f)

# ❌ HIGH - dill.loads (like pickle)
import dill
obj = dill.loads(untrusted_bytes)
```

**Secure Alternative:**
```python
# ✅ Use JSON for serialization
import json
obj = json.loads(user_data)

# ✅ Use MessagePack
import msgpack
obj = msgpack.unpackb(user_data)

# ✅ Use cloudy pickles with restrictions (if pickle needed)
import pickletools
pickletools.dis(pickle_data)  # Inspect first

# ✅ Use dataclass serialization
import dataclasses
obj = dataclasses.asdict(data)
```

**Detection Method:** AST traversal detecting `pickle.loads()` and `pickle.load()` calls

---

### 6. Weak Hashing (HIGH/MEDIUM)

**Rule ID:** `PYTHON-HASH-06`  
**Severity:** HIGH (for passwords), MEDIUM (for other uses)  
**CWE:** CWE-327 (Use of a Broken or Risky Cryptographic Algorithm)  
**OWASP:** A02:2021 – Cryptographic Failures  
**Confidence:** 0.95

**Description:**
MD5, SHA1, and `crypt` module are cryptographically broken. Use strong hashing algorithms like bcrypt, scrypt, or Argon2.

**Vulnerable Pattern:**
```python
# ❌ HIGH - MD5 for password
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()

# ❌ HIGH - SHA1 for password
hashed = hashlib.sha1(password.encode()).hexdigest()

# ❌ MEDIUM - MD5 for cache keys (less critical)
cache_key = hashlib.md5(data).hexdigest()

# ❌ HIGH - crypt module (deprecated)
import crypt
hashed = crypt.crypt(password, salt)
```

**Secure Alternative:**
```python
# ✅ Use bcrypt for passwords
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ Use scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
kdf = Scrypt(...)
key = kdf.derive(password.encode())

# ✅ Use Argon2
import argon2
ph = argon2.PasswordHasher()
hashed = ph.hash(password)

# ✅ Use PBKDF2 if bcrypt not available
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
```

**Detection Method:** AST traversal detecting `hashlib.md5()`, `hashlib.sha1()`, `crypt.crypt()` calls

---

### 7. Debug Mode (MEDIUM)

**Rule ID:** `PYTHON-DEBUG-07`  
**Severity:** MEDIUM  
**CWE:** CWE-489 (Active Debug Code)  
**OWASP:** A05:2021 – Security Misconfiguration  
**Confidence:** 0.85

**Description:**
Debug mode in production exposes sensitive information and enables attackers to execute arbitrary code or inspect the application state.

**Vulnerable Pattern:**
```python
# ❌ MEDIUM - DEBUG=True in production
DEBUG = True

# ❌ MEDIUM - Flask debug mode
app.run(debug=True)

# ❌ MEDIUM - Django debug in settings
DEBUG = True

# ❌ MEDIUM - print statements in production code
def process_payment(card_number):
    print(f"Processing card: {card_number}")  # Logs sensitive data!
    # ...
```

**Secure Alternative:**
```python
# ✅ Use environment-specific settings
import os
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ✅ Production-safe logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Processing card: XXXX")  # Mask sensitive data

# ✅ Flask production mode
app.run(debug=False)

# ✅ Use proper logging instead of print
logger.info("Transaction processed")
```

**Detection Method:** Regex patterns detecting `DEBUG=True`, `debug=True`, `app.run(debug=True)` assignment and calls

---

### 8. XXE/XML External Entity (MEDIUM)

**Rule ID:** `PYTHON-XXE-08`  
**Severity:** MEDIUM  
**CWE:** CWE-611 (Improper Restriction of XML External Entity Reference)  
**OWASP:** A05:2021 – Security Misconfiguration  
**Confidence:** 0.82

**Description:**
Parsing untrusted XML with default settings can allow XXE attacks leading to information disclosure or DoS.

**Vulnerable Pattern:**
```python
# ❌ MEDIUM - Unsafe XML parsing with ElementTree
import xml.etree.ElementTree as ET
tree = ET.parse(untrusted_file)

# ❌ MEDIUM - lxml with external entities enabled
from lxml import etree
tree = etree.parse(untrusted_file)

# ❌ MEDIUM - defusedxml without restrictions
from defusedxml import ElementTree
tree = ElementTree.parse(untrusted_file)
```

**Secure Alternative:**
```python
# ✅ Use defusedxml (hardens XML parsing)
from defusedxml.ElementTree import parse
tree = parse(untrusted_file)

# ✅ Disable external entities explicitly
import xml.etree.ElementTree as ET
for event, elem in ET.iterparse(file, events=['start']):
    if 'DOCTYPE' in elem.tag:
        raise ValueError("XXE detected")

# ✅ Use JSON instead of XML
import json
data = json.load(file)
```

**Detection Method:** AST traversal detecting XML parsing calls without defusedxml namespace

---

## JavaScript Analyzer (7 Rules)

### 1. Eval Usage (CRITICAL)

**Rule ID:** `JS-EVAL-01`  
**Severity:** CRITICAL  
**CWE:** CWE-95 (Improper Neutralization of Directives in Dynamically Evaluated Code)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.98

**Description:**
`eval()` executes arbitrary JavaScript code and should never be used, especially with user input.

**Vulnerable Pattern:**
```javascript
// ❌ CRITICAL - Direct eval
eval(userCode);

// ❌ CRITICAL - eval in callback
setTimeout(`eval(${userInput})`, 1000);

// ❌ CRITICAL - eval of deserialized data
const data = JSON.parse(jsonStr);
eval(data.code);

// ❌ CRITICAL - new Function() equivalent
const fn = new Function(userInput);
fn();
```

**Secure Alternative:**
```javascript
// ✅ Use JSON.parse for JSON
const data = JSON.parse(jsonStr);

// ✅ Use Web Workers for isolated execution
const worker = new Worker('worker.js');
worker.postMessage(userCode);

// ✅ Use sandboxed iframes
const iframe = document.createElement('iframe');
iframe.sandbox.add('allow-scripts');

// ✅ Use expression parsers for math
import { evaluate } from 'mathjs';
const result = evaluate(expression);
```

**Detection Method:** Regex pattern matching `eval\s*\(` not in comments

---

### 2. innerHTML Assignment (HIGH)

**Rule ID:** `JS-XSS-02`  
**Severity:** HIGH  
**CWE:** CWE-79 (Improper Neutralization of Input During Web Page Generation)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.96

**Description:**
Assigning untrusted content to `innerHTML` creates XSS vulnerabilities. Use `textContent` or sanitization instead.

**Vulnerable Pattern:**
```javascript
// ❌ HIGH - innerHTML with user input
const userContent = getQueryParam('content');
document.getElementById('output').innerHTML = userContent;

// ❌ HIGH - innerHTML in event handlers
element.onclick = () => {
    div.innerHTML = userData.description;
};

// ❌ HIGH - innerHTML with API response
fetch('/api/content')
    .then(r => r.json())
    .then(data => {
        el.innerHTML = data.html;  // ❌ Assume untrusted
    });

// ❌ HIGH - innerHTML concatenation
el.innerHTML = '<p>' + userInput + '</p>';
```

**Secure Alternative:**
```javascript
// ✅ Use textContent for text only
element.textContent = userContent;

// ✅ Use textContent with createElement
const p = document.createElement('p');
p.textContent = userContent;
element.appendChild(p);

// ✅ Use innerHTML with pre-sanitized content
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userContent);

// ✅ Use template literals with escaping
const template = `<p>${escapeHtml(userInput)}</p>`;
element.innerHTML = template;
```

**Detection Method:** Regex pattern matching `.innerHTML\s*=` with subsequent assignment

---

### 3. document.write() Usage (HIGH)

**Rule ID:** `JS-DOM-03`  
**Severity:** HIGH  
**CWE:** CWE-79 (XSS)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.94

**Description:**
`document.write()` executes synchronously and can be hijacked. Prefer DOM manipulation methods.

**Vulnerable Pattern:**
```javascript
// ❌ HIGH - document.write with untrusted data
const userData = request.query.data;
document.write(userData);

// ❌ HIGH - document.write in scripts
document.write('<script src="' + srcUrl + '"></script>');

// ❌ HIGH - document.write in event handlers
element.onclick = () => {
    document.write(userInput);  // Overwrites entire page!
};
```

**Secure Alternative:**
```javascript
// ✅ Use DOM methods
const div = document.createElement('div');
div.textContent = userData;
document.body.appendChild(div);

// ✅ Use innerHTML with sanitization
element.innerHTML = DOMPurify.sanitize(userData);

// ✅ Use insertAdjacentHTML
element.insertAdjacentHTML('beforeend', sanitized);
```

**Detection Method:** Regex pattern matching `document\.write\s*\(`

---

### 4. Hardcoded Secrets (HIGH)

**Rule ID:** `JS-SECRETS-04`  
**Severity:** HIGH  
**CWE:** CWE-798 (Use of Hard-Coded Credentials)  
**OWASP:** A02:2021 – Cryptographic Failures  
**Confidence:** 0.88

**Description:**
API keys and secrets hardcoded in client-side JavaScript are exposed to all users and can be found via browser dev tools.

**Vulnerable Pattern:**
```javascript
// ❌ HIGH - Hardcoded API key
const API_KEY = 'sk-1234567890abcdef';

// ❌ HIGH - Hardcoded auth token
const AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

// ❌ HIGH - API key in config object
const config = {
    apiKey: 'sk-secret123',
    baseUrl: 'https://api.example.com'
};

// ❌ HIGH - Bearer token
const headers = {
    Authorization: 'Bearer secret-token-12345'
};
```

**Secure Alternative:**
```javascript
// ✅ Use environment variables (build-time injection)
const API_KEY = process.env.REACT_APP_API_KEY;

// ✅ Fetch from backend endpoint
async function getApiKey() {
    const response = await fetch('/api/config');
    const config = await response.json();
    return config.apiKey;
}

// ✅ Use OAuth flow
import { useAuth0 } from "@auth0/auth0-react";
const { getAccessTokenSilently } = useAuth0();
const token = await getAccessTokenSilently();

// ✅ Use session-based auth
const token = sessionStorage.getItem('auth_token');
```

**Detection Method:** Regex patterns matching API key prefixes (`sk-`, `pk-`, Bearer patterns) in string assignments

---

### 5. SQL Concatenation (HIGH)

**Rule ID:** `JS-SQL-05`  
**Severity:** HIGH  
**CWE:** CWE-89 (SQL Injection)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.90

**Description:**
Building SQL queries via string concatenation in client-side code... (though SQL shouldn't be in JavaScript)

**Vulnerable Pattern:**
```javascript
// ❌ HIGH - SQL concatenation (client-side shouldn't have SQL!)
const userId = request.query.id;
const query = 'SELECT * FROM users WHERE id = ' + userId;

// ❌ HIGH - SQL injection in API call
const query = `SELECT * FROM products WHERE name = '${productName}'`;
fetch('/api/query', { method: 'POST', body: JSON.stringify({ query }) });

// ❌ HIGH - Template literal SQL
const userId = getUserId();
const sql = `DELETE FROM users WHERE id = ${userId}`;
```

**Secure Alternative:**
```javascript
// ✅ Use parameterized API endpoints
fetch(`/api/users/${userId}`)
    .then(r => r.json());

// ✅ Use POST with separate parameters
fetch('/api/users/search', {
    method: 'POST',
    body: JSON.stringify({ id: userId })
});

// ✅ Let backend handle SQL with prepared statements
const response = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
);

// ✅ Use ORM query builders (if client-side SQL needed)
import { sql } from 'drizzle-orm';
const users = await db.query.users.findMany({
    where: eq(users.id, userId)
});
```

**Detection Method:** Regex pattern matching SQL keywords (SELECT, INSERT, UPDATE, DELETE, DROP) + concatenation operators

---

### 6. Weak Cryptography (MEDIUM)

**Rule ID:** `JS-CRYPTO-06`  
**Severity:** MEDIUM  
**CWE:** CWE-327 (Use of Broken/Risky Cryptographic Algorithm)  
**OWASP:** A02:2021 – Cryptographic Failures  
**Confidence:** 0.91

**Description:**
Using deprecated or weak cryptographic algorithms like MD5, SHA1, or `createCipher`.

**Vulnerable Pattern:**
```javascript
// ❌ MEDIUM - crypto.createCipher (deprecated)
const crypto = require('crypto');
const cipher = crypto.createCipher('aes-256-cbc', password);

// ❌ MEDIUM - MD5 hashing
const md5Hash = require('md5');
const hash = md5Hash(data);

// ❌ MEDIUM - SHA1 hashing
const sha1 = require('sha1');
const hash = sha1(data);

// ❌ MEDIUM - TweetNaCl weak key
const key = nacl.utils.random(16);  // Should be 32 bytes
```

**Secure Alternative:**
```javascript
// ✅ Use createCipheriv with proper key/IV
const crypto = require('crypto');
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);
const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);

// ✅ Use bcrypt for passwords
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);

// ✅ Use SHA-256 for hashing
const hash = crypto.createHash('sha256').update(data).digest('hex');

// ✅ Use proper PBKDF2
const derivedKey = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512');
```

**Detection Method:** Regex patterns matching `createCipher`, `require('md5')`, `require('sha1')` calls

---

### 7. Dangerous Method Calls (HIGH)

**Rule ID:** `JS-DANGER-07`  
**Severity:** HIGH  
**CWE:** CWE-95 (Code Execution)  
**OWASP:** A03:2021 – Injection  
**Confidence:** 0.93

**Description:**
Methods like `Function()` constructor, `setTimeout/setInterval` with strings, or `setImmediate` allow code execution.

**Vulnerable Pattern:**
```javascript
// ❌ HIGH - Function constructor with user input
const userCode = request.query.code;
const fn = new Function(userCode);
fn();

// ❌ HIGH - setTimeout with code string
setTimeout('alert(' + userMessage + ')', 1000);

// ❌ HIGH - setInterval with string
setInterval(`updateUI('${data}')`, 5000);

// ❌ HIGH - setImmediate with code
setImmediate(() => eval(userInput));

// ❌ HIGH - requestAnimationFrame with code
requestAnimationFrame(eval);
```

**Secure Alternative:**
```javascript
// ✅ Use setTimeout with function reference
const handler = () => alert(userMessage);
setTimeout(handler, 1000);

// ✅ Use setInterval with bound function
const updateFn = updateUI.bind(null, data);
setInterval(updateFn, 5000);

// ✅ Use Web Workers for code execution
const worker = new Worker('worker.js');
worker.postMessage({ userCode });

// ✅ Use arrow functions for callbacks
setTimeout(() => {
    alert(userMessage);
}, 1000);
```

**Detection Method:** Regex patterns matching `new Function`, `setTimeout\s*\(\s*['"\`]`, `setInterval\s*\(\s*['"\`]`

---

## Risk Scoring Algorithm

### Calculation Formula

```
Risk Score = (Total Weighted Severity / Max Possible) × 100

Where:
  Severity Weights:
    - CRITICAL: 10
    - HIGH: 7
    - MEDIUM: 4
    - LOW: 1
    - INFO: 0.25

  Confidence Multiplier:
    - ≥ 0.85: 1.0 (apply full weight)
    - 0.70-0.84: 0.7 (reduce weight by 30%)
    - < 0.70: 0.5 (reduce weight by 50%)

  Max Possible = 10 (single CRITICAL vuln at confidence 1.0)

Result Range: 0-100
  0-10:   🟢 Green (minimal risk)
  10-40:  🟡 Yellow (moderate risk)
  40-70:  🟠 Orange (high risk)
  70-100: 🔴 Red (critical risk)
```

### Example Calculations

**Example 1: Single Critical Vulnerability**
```
1 × CRITICAL (10) × 1.0 confidence = 10 points
Risk Score = (10 / 10) × 100 = 100
```

**Example 2: Mixed Severities**
```
1 CRITICAL (10) @ 0.99 confidence = 9.9
2 HIGH (7×2) @ 0.80 confidence = 11.2
1 MEDIUM (4) @ 0.70 confidence = 2.8

Total = 9.9 + 11.2 + 2.8 = 24 points
Risk Score = (24 / 10) × 100 = 100 (capped)
```

**Example 3: Low Confidence Findings**
```
1 HIGH (7) @ 0.65 confidence = 3.5
1 MEDIUM (4) @ 0.55 confidence = 1.1

Total = 3.5 + 1.1 = 4.6 points
Risk Score = (4.6 / 10) × 100 = 46
```

---

## Detection Confidence Factors

| Factor | Impact | Notes |
|--------|--------|-------|
| AST match (Python) | +0.15 | High confidence for structural code patterns |
| Exact regex match | +0.10 | Pattern directly matches vulnerable code |
| Context awareness | +0.05 | Rule considers surrounding code context |
| False positive history | -0.05 | Known false positive patterns |
| User feedback | ±0.10 | Adjustments from real-world testing |

---

## Future Enhancements

- **Control Flow Analysis**: Track data flow through code
- **Type Inference**: Understand data types and transformations
- **Taint Tracking**: Follow suspicious data across files
- **ML-based**: Machine learning model for semantic analysis
- **Custom Rules**: User-defined vulnerability patterns
- **Integration Frameworks**: Detect framework-specific vulnerabilities

---

*Last Updated: Phase 2 - January 2024*  
*Total Rules: 15 (8 Python + 7 JavaScript)*  
*Coverage: OWASP Top 10 2021, CWE Top 25*
