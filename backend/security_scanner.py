"""
Day 16 - Security Scanner

Regex/pattern based scanner that works across every supported
language (security anti-patterns tend to look similar regardless of
syntax). Detects:
    * SQL injection risk (string concatenation/formatting into SQL)
    * Hardcoded passwords / API keys / secrets
    * Unsafe eval()/exec() usage
    * Weak hashing algorithms (MD5, SHA1)
    * Command injection risk (os.system, shell=True, Runtime.exec, etc.)
"""

import re

SEVERITY_HIGH = "High"
SEVERITY_MEDIUM = "Medium"
SEVERITY_LOW = "Low"


CHECKS = [
    {
        "name": "SQL Injection",
        "severity": SEVERITY_HIGH,
        "pattern": re.compile(
            r"""(SELECT|INSERT|UPDATE|DELETE)\b.{0,80}?(["'`]\s*\+|\+\s*["'`]|%s|f["'].*\{|\.format\()""",
            re.IGNORECASE,
        ),
        "message": "Possible SQL injection — query built with string concatenation/formatting instead of parameterized queries",
    },
    {
        "name": "Hardcoded Secret",
        "severity": SEVERITY_HIGH,
        "pattern": re.compile(
            r"""(password|passwd|pwd|api[_-]?key|secret|token)\s*[:=]\s*["'][^"'\n]{3,}["']""",
            re.IGNORECASE,
        ),
        "message": "Hardcoded credential/secret found — move to environment variables or a secrets manager",
    },
    {
        "name": "Unsafe eval/exec",
        "severity": SEVERITY_HIGH,
        "pattern": re.compile(r"\b(eval|exec)\s*\("),
        "message": "Use of eval()/exec() — can execute arbitrary code if input is not fully trusted",
    },
    {
        "name": "Weak Hashing Algorithm",
        "severity": SEVERITY_MEDIUM,
        "pattern": re.compile(r"\b(md5|sha1)\s*\(", re.IGNORECASE),
        "message": "Weak hashing algorithm (MD5/SHA1) — use SHA-256 or a dedicated password hash (bcrypt/argon2)",
    },
    {
        "name": "Command Injection",
        "severity": SEVERITY_HIGH,
        "pattern": re.compile(
            r"(os\.system\s*\(|subprocess\.\w+\([^)]*shell\s*=\s*True|Runtime\.getRuntime\(\)\.exec|popen\s*\()",
        ),
        "message": "Possible command injection — shell command built from potentially untrusted input",
    },
    {
        "name": "Insecure Deserialization",
        "severity": SEVERITY_MEDIUM,
        "pattern": re.compile(r"\bpickle\.loads?\s*\(|\byaml\.load\s*\((?!.*Loader)"),
        "message": "Insecure deserialization — pickle/yaml.load on untrusted data can execute arbitrary code",
    },
]


class SecurityScanner:

    def __init__(self, filepath):
        self.filepath = filepath

    def scan(self):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        issues = []

        for lineno, line in enumerate(lines, start=1):
            for check in CHECKS:
                if check["pattern"].search(line):
                    issues.append({
                        "line": lineno,
                        "type": check["name"],
                        "severity": check["severity"],
                        "message": check["message"],
                        "code": line.strip()[:120],
                    })

        return issues

    @staticmethod
    def summarize(issues):
        summary = {SEVERITY_HIGH: 0, SEVERITY_MEDIUM: 0, SEVERITY_LOW: 0}
        for issue in issues:
            summary[issue["severity"]] = summary.get(issue["severity"], 0) + 1
        return summary
