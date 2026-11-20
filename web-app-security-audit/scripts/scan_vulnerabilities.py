#!/usr/bin/env python3
"""
Web Application Vulnerability Static Scanner

Performs static analysis on PHP, JavaScript, and TypeScript codebases to detect
dangerous security sinks, injection paths, mass assignment risks, and misconfigurations.

Usage:
    python3 scan_vulnerabilities.py <file-or-directory> [--json]
"""

import os
import re
import sys
import json
import argparse
from typing import List, Dict, Any

VULN_PATTERNS = [
    # --- PHP / Laravel ---
    {
        "id": "LARAVEL-01",
        "category": "Configuration",
        "severity": "CRITICAL",
        "name": "Debug Mode Enabled in Production",
        "regex": r'^\s*APP_DEBUG\s*=\s*true',
        "extensions": [".env", ".env.production", ".env.example"],
        "description": "APP_DEBUG=true leaks secrets and stack traces, and historical Ignition versions allow RCE (CVE-2021-3129).",
        "remediation": "Set APP_DEBUG=false in production environments."
    },
    {
        "id": "PHP-01",
        "category": "Insecure Deserialization",
        "severity": "CRITICAL",
        "name": "Native PHP unserialize() on Untrusted Data",
        "regex": r'\bunserialize\s*\(\s*(?:\$_|\$[a-zA-Z0-9_]+->input|\$request)',
        "extensions": [".php"],
        "description": "Calling unserialize() on user-controlled data can trigger POP gadget chains leading to RCE.",
        "remediation": "Use json_decode() or signed cryptographic payloads instead."
    },
    {
        "id": "LARAVEL-02",
        "category": "SQL Injection",
        "severity": "HIGH",
        "name": "Raw SQL with String Concatenation / Interpolation",
        "regex": r'(?:DB::raw|whereRaw|selectRaw|havingRaw|orderByRaw)\s*\(\s*(?:["\'].*\$|\$|["\'].*\.\s*\$)',
        "extensions": [".php"],
        "description": "Raw SQL clauses with string concatenation or variable interpolation bypass query parameterization.",
        "remediation": "Use parameterized query bindings: whereRaw('status = ?', [$status])."
    },
    {
        "id": "LARAVEL-03",
        "category": "Cross-Site Scripting (XSS)",
        "severity": "MEDIUM",
        "name": "Unescaped Blade Directive",
        "regex": r'\{!!\s*\$(?:[a-zA-Z0-9_]+->|\$_|\$request|\$[a-zA-Z0-9_]+)\s*!!\}',
        "extensions": [".blade.php", ".php"],
        "description": "{!! $var !!} renders raw unescaped HTML, opening stored or reflected XSS vulnerabilities.",
        "remediation": "Use auto-escaped {{ $var }} or sanitize user HTML via HTMLPurifier before rendering."
    },
    {
        "id": "LARAVEL-04",
        "category": "Mass Assignment",
        "severity": "HIGH",
        "name": "Disabled Model Guarding ($guarded = [])",
        "regex": r'protected\s+\$guarded\s*=\s*\[\s*\]\s*;',
        "extensions": [".php"],
        "description": "Empty $guarded allows mass assignment of administrative or sensitive model attributes.",
        "remediation": "Define explicit $fillable attributes or validate via FormRequest before model creation."
    },

    # --- Node.js & JavaScript ---
    {
        "id": "NODE-01",
        "category": "Command Injection",
        "severity": "CRITICAL",
        "name": "OS Command Execution with User Input",
        "regex": r'(?:child_process\s*\.\s*(?:exec|execSync)|exec\s*\(|execSync\s*\()\s*(?:`|["\'].*\+|[a-zA-Z0-9_]+\s*\+)',
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".mjs"],
        "description": "Passing concatenated strings to child_process.exec invokes a system shell, allowing command injection.",
        "remediation": "Use child_process.execFile() or spawn() with an arguments array, without shell=true."
    },
    {
        "id": "NODE-02",
        "category": "Code Injection",
        "severity": "CRITICAL",
        "name": "Dynamic Code Evaluation (eval / Function / vm)",
        "regex": r'\b(?:eval|new\s+Function|vm\.runIn(?:ThisContext|NewContext))\s*\(',
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".mjs"],
        "description": "Dynamically compiling user-provided strings executes arbitrary code in the V8 process.",
        "remediation": "Eliminate eval() and new Function(); use static parsers or safe AST evaluation."
    },
    {
        "id": "NODE-03",
        "category": "Prototype Pollution",
        "severity": "HIGH",
        "name": "Dangerous Object Prototype Property Assignment",
        "regex": r'\[\s*["\'](?:__proto__|constructor|prototype)["\']\s*\]|Object\.assign\s*\(\s*\{\}\s*,\s*(?:req\.body|payload)',
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".mjs"],
        "description": "Modifying __proto__ or unvalidated recursive object assignment can pollute Object.prototype.",
        "remediation": "Block __proto__ / constructor keys, or use Object.create(null) / Map."
    },

    # --- Next.js ---
    {
        "id": "NEXT-01",
        "category": "Secret Exposure",
        "severity": "CRITICAL",
        "name": "Exposing Secret Key via NEXT_PUBLIC_ Prefix",
        "regex": r'NEXT_PUBLIC_[A-Z0-9_]*(?:SECRET|PRIVATE|TOKEN|KEY|PASS|AUTH)[A-Z0-9_]*\s*=',
        "extensions": [".env", ".env.local", ".env.production", ".js", ".ts"],
        "description": "NEXT_PUBLIC_ variables are baked into browser client JavaScript bundles at build time.",
        "remediation": "Remove NEXT_PUBLIC_ prefix so the secret remains isolated to the server runtime."
    },
    {
        "id": "NEXT-02",
        "category": "Cross-Site Scripting (XSS)",
        "severity": "HIGH",
        "name": "dangerouslySetInnerHTML with User Input",
        "regex": r'dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html\s*:\s*(?!sanitize|DOMPurify)[a-zA-Z0-9_.]+',
        "extensions": [".jsx", ".tsx", ".js", ".ts"],
        "description": "Rendering unsanitized HTML in React components bypasses virtual DOM XSS protections.",
        "remediation": "Sanitize markup using DOMPurify.sanitize() before setting __html."
    },

    # --- NestJS ---
    {
        "id": "NEST-01",
        "category": "Mass Assignment",
        "severity": "HIGH",
        "name": "ValidationPipe without whitelist: true",
        "regex": r'new\s+ValidationPipe\s*\(\s*(?:\{\s*(?!.*whitelist\s*:\s*true)[^}]*\}|\s*\))',
        "extensions": [".ts", ".js"],
        "description": "NestJS ValidationPipe without whitelist: true permits stripped/non-whitelisted properties in DTOs.",
        "remediation": "Instantiate ValidationPipe({ whitelist: true, forbidNonWhitelisted: true })."
    },

    # --- Python: Django, FastAPI & Flask ---
    {
        "id": "DJANGO-01",
        "category": "Configuration",
        "severity": "CRITICAL",
        "name": "Django DEBUG = True in Production",
        "regex": r'^\s*DEBUG\s*=\s*True',
        "extensions": [".py"],
        "description": "DEBUG = True leaks interactive stack traces, configuration settings, and secrets upon unhandled exceptions.",
        "remediation": "Set DEBUG = False in production settings or load from environment variables."
    },
    {
        "id": "DJANGO-02",
        "category": "Cross-Site Scripting (XSS)",
        "severity": "HIGH",
        "name": "Unsafe mark_safe() Invocation",
        "regex": r'\bmark_safe\s*\(\s*(?:f["\']|["\'].*\+|[a-zA-Z0-9_.]+\s*\+)',
        "extensions": [".py"],
        "description": "Bypassing Django template auto-escaping with mark_safe() on concatenated input enables XSS.",
        "remediation": "Sanitize user HTML using bleach.clean() before invoking mark_safe()."
    },
    {
        "id": "PY-01",
        "category": "SQL Injection",
        "severity": "HIGH",
        "name": "Raw SQL with String Formatting (Django / SQLAlchemy)",
        "regex": r'(?:\.raw|\.extra|cursor\.execute|text)\s*\(\s*(?:f["\']|["\'].*%\s*[a-zA-Z0-9_]|["\'].*\+\s*[a-zA-Z0-9_])',
        "extensions": [".py"],
        "description": "String formatting or f-strings inside raw SQL queries bypass parameterization.",
        "remediation": "Use query parameters list or dictionary: cursor.execute('SELECT * FROM t WHERE id = %s', [user_id])."
    },
    {
        "id": "PY-02",
        "category": "Insecure Deserialization",
        "severity": "CRITICAL",
        "name": "Untrusted pickle.loads() Deserialization",
        "regex": r'\bpickle\s*\.\s*(?:loads|load)\s*\(',
        "extensions": [".py"],
        "description": "Deserializing untrusted data with pickle allows arbitrary code execution via __reduce__.",
        "remediation": "Use json or django.core.signing for serialization of untrusted payloads."
    },
    {
        "id": "FLASK-01",
        "category": "Template Injection (SSTI)",
        "severity": "CRITICAL",
        "name": "Jinja2 Server-Side Template Injection via render_template_string",
        "regex": r'\brender_template_string\s*\(\s*(?:f["\']|["\'].*\+|[a-zA-Z0-9_.]+\s*\+)',
        "extensions": [".py"],
        "description": "Passing user input into render_template_string enables SSTI leading to sandbox escape and RCE.",
        "remediation": "Pass untrusted variables as keyword arguments into static template strings: render_template_string('Hello {{ name }}', name=user_input)."
    },
    {
        "id": "PY-03",
        "category": "Command Injection",
        "severity": "CRITICAL",
        "name": "OS Command Execution (os.system / subprocess shell=True)",
        "regex": r'\bos\.system\s*\(|subprocess\.(?:Popen|call|run|check_output)\s*\([^)]*shell\s*=\s*True',
        "extensions": [".py"],
        "description": "Invoking a shell via os.system or shell=True with user-supplied arguments enables command injection.",
        "remediation": "Pass arguments as a list to subprocess.run(..., shell=False)."
    },

    # --- CodeIgniter & Generic PHP ---
    {
        "id": "CI-01",
        "category": "SQL Injection",
        "severity": "HIGH",
        "name": "CodeIgniter Raw Query Concatenation",
        "regex": r'\$this\s*->\s*db\s*->\s*query\s*\(\s*["\'].*\.\s*\$',
        "extensions": [".php"],
        "description": "Concatenating user input into $this->db->query() bypasses CodeIgniter's query parameterization.",
        "remediation": "Use query bindings: $this->db->query('SELECT * FROM t WHERE col = ?', [$val])."
    },
    {
        "id": "CI-02",
        "category": "Configuration",
        "severity": "HIGH",
        "name": "CodeIgniter CSRF Protection Disabled",
        "regex": r'\$config\[[\'"]csrf_protection[\'"]\]\s*=\s*FALSE\s*;',
        "extensions": [".php"],
        "description": "Disabling CSRF protection allows cross-site request forgery attacks on authenticated endpoints.",
        "remediation": "Set $config['csrf_protection'] = TRUE; in application/config/config.php."
    },

    # --- Express.js & Fastify ---
    {
        "id": "EXP-01",
        "category": "Open Redirect",
        "severity": "MEDIUM",
        "name": "Unvalidated res.redirect() from User Query",
        "regex": r'res\.redirect\s*\(\s*req\.(?:query|params|body)',
        "extensions": [".js", ".ts"],
        "description": "Redirecting users directly to unvalidated user-controlled parameters enables phishing attacks.",
        "remediation": "Verify that target URLs are relative and start with a single slash (url.startsWith('/') && !url.startsWith('//'))."
    },
    {
        "id": "EXP-02",
        "category": "Path Traversal",
        "severity": "HIGH",
        "name": "res.sendFile() with User Input",
        "regex": r'res\.sendFile\s*\(\s*req\.(?:query|params|body)',
        "extensions": [".js", ".ts"],
        "description": "Serving files directly from request parameters without an explicit root directory allows directory traversal.",
        "remediation": "Pass path.basename(file) with an explicit { root: safeDir, dotfiles: 'deny' } option."
    }
]

def scan_file(file_path: str) -> List[Dict[str, Any]]:
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return violations

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()

    for idx, line in enumerate(lines):
        line_num = idx + 1
        for rule in VULN_PATTERNS:
            # Check file extension
            matches_ext = any(file_path.endswith(e) for e in rule["extensions"])
            if not matches_ext:
                continue

            if re.search(rule["regex"], line):
                violations.append({
                    "id": rule["id"],
                    "name": rule["name"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "file": file_path,
                    "line": line_num,
                    "snippet": line.strip()[:120],
                    "description": rule["description"],
                    "remediation": rule["remediation"]
                })
    return violations

def collect_files(target: str) -> List[str]:
    valid_exts = {".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".env", ".env.example", ".env.local", ".env.production"}
    if os.path.isfile(target):
        return [target]

    matched_files = []
    for root, dirs, files in os.walk(target):
        # Exclude common large/vendor directories
        dirs[:] = [d for d in dirs if d not in {"node_modules", "vendor", ".git", "dist", "build", ".next"}]
        for f in files:
            full_path = os.path.join(root, f)
            if any(f.endswith(ext) or f.startswith(".env") for ext in valid_exts):
                matched_files.append(full_path)
    return matched_files

def main():
    parser = argparse.ArgumentParser(description="Web Application Vulnerability Static Scanner")
    parser.add_argument("target", help="File or directory path to audit")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    files = collect_files(args.target)
    all_violations = []

    for f in files:
        all_violations.extend(scan_file(f))

    # Calculate severity counts
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for v in all_violations:
        sev = v["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    if args.json:
        output = {
            "target": args.target,
            "files_scanned": len(files),
            "total_violations": len(all_violations),
            "severity_summary": severity_counts,
            "violations": all_violations
        }
        print(json.dumps(output, indent=2))
        sys.exit(1 if all_violations else 0)

    # CLI Human-Readable Output
    print("=" * 80)
    print("WEB APPLICATION SECURITY AUDIT REPORT")
    print("=" * 80)
    print(f"Target Scanned:    {args.target}")
    print(f"Files Inspected:   {len(files)}")
    print(f"Total Violations:  {len(all_violations)}")
    print(f"Severity Breakdown: CRITICAL: {severity_counts['CRITICAL']} | HIGH: {severity_counts['HIGH']} | MEDIUM: {severity_counts['MEDIUM']}")
    print("-" * 80)

    if not all_violations:
        print("✅ No critical web application vulnerability sinks detected.")
        print("=" * 80)
        sys.exit(0)

    for v in all_violations:
        color_tag = f"[{v['severity']}]"
        print(f"\n{color_tag} {v['name']} ({v['id']})")
        print(f"  Category:    {v['category']}")
        print(f"  Location:    {v['file']}:{v['line']}")
        print(f"  Code:        {v['snippet']}")
        print(f"  Risk:        {v['description']}")
        print(f"  Remediation: {v['remediation']}")

    print("\n" + "=" * 80)
    print("AUDIT COMPLETE: Review flagged sinks and implement remediations immediately.")
    print("=" * 80)
    sys.exit(1)

if __name__ == "__main__":
    main()
