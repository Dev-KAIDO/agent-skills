---
name: security-comprehensive
description: Comprehensive security skill — vulnerability scanning, threat modeling, OWASP prevention, auth patterns, API security, mobile security, penetration testing, compliance (GDPR/HIPAA/SOC2), secrets management, incident response, and remediation. Use when reviewing, building, or securing any application (web, mobile, API, infrastructure).
---

# Security Comprehensive — Complete Skill

## Overview

**Single skill for all security work.** Covers prevention, detection, response, and compliance across all platforms. Merges `application-security`, `security-gate`, `security-threat-model`, `security-remediator`, `security-best-practices`, `security-ownership-map`, `engineering-security-engineer`, `project-rbac-audit-policy`, and `cityofaiagents-security-hardening`.

---

## 1. Threat Modeling (نمذجة التهديدات)

### 1.1 STRIDE Methodology
| Category | Threat | Example |
|----------|--------|---------|
| **S**poofing | Impersonation | Forging JWT tokens |
| **T**ampering | Data modification | SQL injection |
| **R**epudiation | Denial of actions | Missing audit logs |
| **I**nformation Disclosure | Data exposure | Unencrypted PII |
| **D**enial of Service | Availability attack | DDoS, resource exhaustion |
| **E**levation of Privilege | Unauthorized access | IDOR, privilege escalation |

### 1.2 Trust Boundaries
```
[Internet] → [CDN/WAF] → [Load Balancer] → [API Gateway] → [Application] → [Database]
                 ↑              ↑                  ↑              ↑            ↑
            Trust boundary  Trust boundary   Trust boundary  Trust boundary  Trust boundary
```

### 1.3 Threat Model Process
1. **Identify assets:** data, credentials, APIs, infrastructure
2. **Map data flow:** where does sensitive data go?
3. **Identify trust boundaries:** where does context change?
4. **Enumerate threats:** STRIDE at each boundary
5. **Assess risk:** likelihood × impact
6. **Define mitigations:** controls for each threat
7. **Document:** threat model document with evidence

### 1.4 Risk Assessment Matrix
| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Low | Low | Medium |

---

## 2. OWASP Top 10 (2025) — Prevention

### 2.1 A01: Broken Access Control
```python
# ❌ BAD: Client-side only check
if user.role == "admin":  # Client can modify this

# ✅ GOOD: Server-side authorization on every request
def require_permission(permission):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                raise PermissionDenied()
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```
**Rules:**
- Deny by default (default deny, explicit allow)
- Verify server-side on every request (client checks are UX only)
- Use IDOR-safe object references (UUIDs, ownership checks)
- Log access control failures
- Disable directory listing

### 2.2 A02: Cryptographic Failures
```python
# ❌ BAD: MD5, SHA1 for passwords
password_hash = hashlib.md5(password).hexdigest()

# ✅ GOOD: bcrypt/argon2 for passwords
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ GOOD: AES-256-GCM for data at rest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
aesgcm = AESGCM(key)
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
```
**Rules:**
- Encrypt data in transit (TLS 1.3) and at rest (AES-256)
- Use strong algorithms: bcrypt/argon2 (passwords), AES-GCM (data), Ed25519 (signing)
- Rotate keys regularly
- Never hardcode keys/secrets
- Use environment variables or secret managers

### 2.3 A03: Injection
```python
# ❌ BAD: String concatenation
query = "SELECT * FROM users WHERE id = " + user_input

# ✅ GOOD: Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))

# ❌ BAD: Direct HTML
html = f"<p>{user_input}</p>"

# ✅ GOOD: Template escaping
html = template.render(text=escape(user_input))
```
**Rules:**
- Use parameterized queries / ORMs (never string concatenation)
- Input validation: allowlist (not denylist)
- Output encoding: HTML, JS, URL, SQL specific
- Use CSP headers for XSS prevention
- Escape at point of use

### 2.4 A04: Insecure Design
- Threat model during design phase
- Separate tenants/data at design level
- Rate limiting by design
- Secure by default: minimal permissions
- Limit resource consumption

### 2.5 A05: Security Misconfiguration
```nginx
# ✅ Secure headers
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```
**Rules:**
- Remove default accounts and configurations
- Enable security headers
- Disable verbose error messages in production
- Update and patch regularly
- Use infrastructure as code (IaC) for reproducible config

### 2.6 A06: Vulnerable Components
- Inventory all dependencies (SBOM)
- Monitor CVE databases
- Automate dependency scanning (Dependabot, Snyk, npm audit)
- Update regularly
- Remove unused dependencies

### 2.7 A07: Authentication Failures
```python
# ✅ Secure authentication
- Multi-factor authentication (MFA) available
- Password policy: 12+ chars, complexity, breach check (HaveIBeenPwned)
- Account lockout: 5-10 failed attempts → lock + notify
- Session management: secure, HttpOnly, SameSite cookies
- Session timeout: 15-30 min inactivity
- Password reset: time-limited, single-use tokens
```

### 2.8 A08: Data Integrity Failures
- Verify data integrity (HMAC, digital signatures)
- Use CI/CD with signed commits
- Validate serialized data (avoid unsafe deserialization)
- Use SRI for external scripts

### 2.9 A09: Logging & Monitoring Failures
```python
# ✅ Security logging
logger.info("User login", extra={
    "user_id": user.id,
    "ip": request.ip,
    "user_agent": request.headers["User-Agent"],
    "result": "success"
})

logger.warning("Failed login", extra={
    "user_id": user.id,
    "ip": request.ip,
    "attempt": attempt_count
})
```
**Log:** authentication events, access control failures, input validation failures, high-value transactions, errors (without sensitive data)

### 2.10 A10: SSRF (Server-Side Request Forgery)
- Validate and sanitize all URLs
- Use allowlist for outbound requests
- Disable HTTP redirects
- Segment network (don't expose internal services)
- Use metadata service protection (cloud)

---

## 3. API Security (أمن الواجهات البرمجية)

### 3.1 OWASP API Security Top 10
1. **Broken object level authorization (BOLA):** verify ownership on every object access
2. **Broken user authentication:** strong tokens, expiry, revocation
3. **Excessive data exposure:** return only needed fields
4. **Lack of resources & rate limiting:** paginate, rate limit
5. **Broken function level authorization:** verify permissions per endpoint
6. **Mass assignment:** whitelist allowed fields
7. **Security misconfiguration:** CORS, headers, error handling
8. **Injection:** input validation, parameterized queries
9. **Improper asset management:** API versioning, documentation
10. **Insufficient logging:** log all API access and errors

### 3.2 Rate Limiting
```python
# Token bucket algorithm
RATE_LIMIT = 100  # requests per minute
BURST = 20        # burst capacity

@app.before_request
def rate_limit():
    key = f"rate:{request.remote_addr}"
    tokens = redis.get(key) or RATE_LIMIT
    if int(tokens) <= 0:
        abort(429, "Rate limit exceeded")
    redis.decr(key)
```

### 3.3 API Authentication
```python
# JWT with proper claims
{
    "sub": "user-123",
    "iss": "auth.example.com",
    "aud": "api.example.com",
    "exp": 1735689600,
    "iat": 1735686000,
    "jti": "unique-token-id",    # for revocation
    "scope": "read write"
}

# Verification
- Verify signature (RS256/EdDSA)
- Check expiry (exp)
- Check audience (aud)
- Check issuer (iss)
- Check revocation (jti blacklist)
```

### 3.4 Input Validation
```python
# Use schema validation
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    age: int
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower().strip()
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v
```

---

## 4. Mobile Security (أمن التطبيقات المحمولة)

### 4.1 Checklist
- [ ] Certificate pinning (prevent MITM)
- [ ] Secure token storage (Keychain/Keystore, not SharedPreferences)
- [ ] Jailbreak/root detection (optional, with graceful degradation)
- [ ] Code obfuscation (ProGuard/R8 for Android)
- [ ] No sensitive data in logs
- [ ] Screenshot prevention for sensitive screens (optional)
- [ ] Biometric authentication available
- [ ] Deep link validation (prevent unauthorized navigation)
- [ ] Network security config (Android) / ATS (iOS)
- [ ] Secure local database (SQLCipher or encrypted)

### 4.2 Token Storage
```kotlin
// Android - Keystore
val keyStore = KeyStore.getInstance("AndroidKeyStore")
keyStore.load(null)
val secretKey = SecretKeySpec(keyBytes, "AES")

// iOS - Keychain
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth_token",
    kSecValueData as String: tokenData
]
SecItemAdd(query as CFDictionary, nil)
```

---

## 5. RBAC & Authorization (الصلاحيات)

### 5.1 Principles
- **Deny by default:** no access unless explicitly granted
- **Least privilege:** minimum permissions needed
- **Separation of duties:** different users for critical operations
- **Defense in depth:** multiple authorization layers

### 5.2 RBAC Implementation
```python
# Role definitions
ROLES = {
    "admin": ["read", "write", "delete", "manage_users"],
    "editor": ["read", "write"],
    "viewer": ["read"],
}

# Permission check middleware
def require_permission(permission):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user_permissions = ROLES.get(request.user.role, [])
            if permission not in user_permissions:
                raise PermissionDenied(f"Requires: {permission}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.route("/users", methods=["POST"])
@require_permission("manage_users")
def create_user(request):
    ...
```

### 5.3 Negative Permission Tests
```python
def test_viewer_cannot_delete():
    """Viewer should NOT be able to delete"""
    response = client.delete("/resource/1", headers=viewer_token)
    assert response.status_code == 403

def test_unauthenticated_blocked():
    """No token should be blocked"""
    response = client.get("/resource")
    assert response.status_code == 401
```

---

## 6. Secrets Management (إدارة الأسرار)

### 6.1 Rules
| ❌ Never | ✅ Always |
|----------|----------|
| Hardcode in source | Environment variables |
| Commit to git | Secret manager (Vault, AWS SSM) |
| Share in chat | Rotate regularly |
| Log secrets | Redact in logs |
| Use weak keys | Use strong random keys |

### 6.2 Environment Variables
```bash
# .env (NEVER commit to git)
DATABASE_URL=postgresql://user:pass@localhost/db
JWT_SECRET=super-secret-key-change-me
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# .gitignore
.env
.env.local
.env.production
```

### 6.3 Secret Rotation
- API keys: rotate every 90 days
- JWT signing keys: rotate monthly or on compromise
- Database passwords: rotate quarterly
- TLS certificates: auto-renew before expiry

---

## 7. Compliance (الامتثال)

### 7.1 GDPR (بيانات شخصية)
- [ ] Lawful basis for processing
- [ ] Data minimization (collect only what's needed)
- [ ] Right to access (data export)
- [ ] Right to deletion (right to be forgotten)
- [ ] Data portability (export in standard format)
- [ ] Privacy by design
- [ ] Data Protection Impact Assessment (DPIA)
- [ ] Breach notification (72 hours)
- [ ] Data Processing Agreement (DPA) with processors

### 7.2 HIPAA (بيانات صحية)
- [ ] PHI encryption (at rest and in transit)
- [ ] Access controls and audit logging
- [ ] Business Associate Agreements (BAAs)
- [ ] Risk assessment
- [ ] Employee training
- [ ] Incident response plan
- [ ] Minimum necessary standard

### 7.3 SOC 2
- [ ] Security controls documented
- [ ] Access controls reviewed quarterly
- [ ] Change management process
- [ ] Incident response plan tested
- [ ] Vendor risk assessment
- [ ] Employee offboarding process
- [ ] Audit trail (6+ months retention)

### 7.4 PCI-DSS (بيانات بطاقات)
- [ ] Never store CVV
- [ ] Tokenize card numbers
- [ ] Encrypt cardholder data
- [ ] Regular vulnerability scans
- [ ] Network segmentation
- [ ] Access restriction (need-to-know)

---

## 8. Incident Response (الاستجابة للحوادث)

### 8.1 Process
```
1. Detect     → monitoring, alerts, user reports
2. Triage     → severity classification (P0-P3)
3. Contain    → isolate affected systems
4. Investigate→ root cause analysis
5. Remediate  → fix vulnerability
6. Recover    → restore normal operation
7. Post-mortem → lessons learned, prevention
```

### 8.2 Severity Classification
| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 - Critical | Active breach, data exposed | Immediate |
| P1 - High | Vulnerability with exploit | 1 hour |
| P2 - Medium | Vulnerability without exploit | 24 hours |
| P3 - Low | Best practice violation | 1 week |

### 8.3 Post-Mortem Template
- What happened (timeline)
- Impact (data, users, systems)
- Root cause
- What went well
- What went poorly
- Action items (with owners and deadlines)
- Prevention measures

---

## 9. Security Scanning (المسح الأمني)

### 9.1 Types
| Scan | Tool | Frequency |
|------|------|-----------|
| SAST (static) | Semgrep, SonarQube | Every commit |
| DAST (dynamic) | OWASP ZAP, Burp Suite | Staging |
| Dependency | npm audit, Snyk, Dependabot | Daily |
| Secrets | git-secrets, truffleHog | Every commit |
| Container | Trivy, Snyk Container | Every build |
| Infrastructure | Checkov, tfsec | Every IaC change |

### 9.2 Scan Results Triage
```
Critical → Fix immediately (block release)
High     → Fix within sprint
Medium   → Fix within month
Low      → Fix when convenient
False positive → Document and suppress with justification
```

---

## 10. Security Ownership Map (خريطة ملكية الأمان)

### 10.1 Purpose
Analyze git history to build a **people↔file security ownership topology** — who actually touches security-sensitive code.

### 10.2 What It Computes
| Metric | Meaning | Use |
|--------|---------|-----|
| **Bus factor** | # of owners whose loss stops work | Identify single points of failure |
| **Sensitive ownership** | Who owns auth/crypto/secrets code | Ensure qualified reviewers |
| **Hotspot files** | High-churn + security-sensitive | Mandatory review gates |
| **Co-change clusters** | Files that change together (Jaccard) | Discover implicit module boundaries |
| **Ownership clusters** | Community detection over file↔author graph | Team topology insights |

### 10.3 Workflow
```bash
# 1. Build ownership graph (people ↔ files bipartite graph)
python scripts/run_ownership_map.py --repo . --output ownership.json

# 2. Query results
python scripts/query_ownership.py --file src/auth/middleware.py

# 3. Maintainers from community detection (networkx)
python scripts/community_maintainers.py --repo .
```

### 10.4 Rules
- ✅ Exclude Dependabot/automation authors (false owners)
- ✅ Export to Neo4j (Cypher in `references/neo4j-import.md`) or Gephi for visualization
- ✅ Weight by recency (recent commits matter more than 5-year-old ones)
- ✅ Use for: assigning security reviewers, finding orphaned sensitive code, bus-factor risk
- ❌ Never use commit count alone as ownership (renames, bulk edits distort it)

---

## 11. Secure Storage Migration (ترحيل التخزين الآمن)

### 11.1 Storage-Surface Scanning
Before migrating, classify every place secrets live:
| Surface | Risk | Typical Location |
|---------|------|------------------|
| SQLite / DB tables | High (plaintext) | `*.db`, migrations |
| JSON / YAML config | High | `config.json`, `settings.yaml` |
| Environment files | Medium | `.env`, `.env.local` |
| Cookies / localStorage | Medium | Web app code |
| Logs | High (often missed) | `*.log`, log statements |
| SharedPreferences (Android) | High | `SharedPreferences` |
| UserDefaults (iOS) | Medium | `UserDefaults` |

Use `scripts/scan_secret_storage.py` to enumerate surfaces; see `references/storage_options.md` for backend capabilities.

### 11.2 Platform-Secure Backends
| Platform | Backend |
|----------|---------|
| Windows | Credential Manager + DPAPI (encrypt before store) |
| macOS / iOS | Keychain |
| Android | Keystore (hardware-backed when available) |
| Linux | `keyring` library (Secret Service / KWallet) |
| Cross-platform Python | `keyring` package |
| Web | httpOnly Secure cookies (never localStorage for tokens) |

### 11.3 Migration Plan Rules
- ✅ **Plan only** — produce the plan; do not implement without approval
- ✅ Backward compatibility: old data readable during transition (dual-read then cut over)
- ✅ Tests must prove **no plaintext secrets remain** after migration
- ✅ One surface at a time, verify each before the next
- ❌ Never log secret values during migration
- ❌ Never weaken encryption for migration convenience

---

## 12. Security Gate & Governance (بوابة الأمان والحوكمة)

### 12.1 Gate Outcomes
```
PASS   → no blocking findings → proceed
WARN   → findings with no blocking severity → proceed + record
FAIL   → blocking findings exist → stop until remediated
```
Emit a gate artifact with status, findings, and evidence — never gate silently.

### 12.2 Baseline-Surface Triggers (always gate)
- Licensing / license-check code
- Device fingerprinting
- Data transfer / export packages
- Auth, payments, PII paths
- New or changed dependencies

### 12.3 Threat-Model Evidence Discipline
- ✅ Every claim backed by **repo evidence** (file:line)
- ✅ Enumerate attacker **non-capabilities** (what the attacker cannot do)
- ✅ Abuse paths written as concrete sequences
- ❌ Never assert a threat without showing where it applies in code

### 12.4 Remediation Prioritization
```
1. KEV / actively exploited   → immediate
2. Critical + reachable       → this sprint
3. High                      → this month
4. Medium/Low                → backlog
```
- **Reject remediation plans without a confirmed finding** (no speculative fixes)
- Live secrets found in transit → rotate, do not just relocate
- Map fixes to ASVS/GHSA/NVD where applicable

---

## 13. Verification Checklist (قائمة التحقق)

### Pre-Release Security Checklist
- [ ] All dependencies updated, no known CVEs
- [ ] No hardcoded secrets in source code
- [ ] Authentication on all protected endpoints
- [ ] Authorization checks server-side
- [ ] Input validation on all user inputs
- [ ] Output encoding for all user-generated content
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] TLS 1.3 for all connections
- [ ] Rate limiting on sensitive endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Logging captures security events
- [ ] Secrets in environment/secret manager only
- [ ] Database queries parameterized
- [ ] CORS properly configured
- [ ] File upload validation (type, size, content)
- [ ] Session management secure (HttpOnly, SameSite, expiry)
- [ ] Password hashing (bcrypt/argon2)
- [ ] MFA available for admin accounts
- [ ] Backup encryption verified
- [ ] Incident response plan documented

---

## Related Skills

- `$design-web` / `$design-mobile` / `$design-desktop` — for UI design
- `$testing-web` / `$testing-desktop` — for security testing
- `$backend-comprehensive` — for API security implementation
- `$repair-stability` — for fixing security vulnerabilities
- `$code-engineering` — for code review with security focus
