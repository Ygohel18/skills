# Django, FastAPI & Flask Security Audit Guide

A comprehensive security engineering manual covering vulnerability paths, dangerous sinks, and defensive patterns across Python web applications (Django, FastAPI, and Flask).

---

## 1. Django Security Architecture & Dangerous Sinks

### 1.1 `DEBUG = True` in Production
- **Risk:** Displays interactive traceback with local variables, configuration keys, database connection strings, and internal file paths.
- **Remediation:**
  ```python
  # settings.py
  import os
  DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1')
  ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'example.com,api.example.com').split(',')
  ```

### 1.2 `ALLOWED_HOSTS = ['*']` Wildcard Exposure
- **Risk:** Permits HTTP Host Header Injection, leading to password reset link poisoning (attacker receives password reset email generated with attacker's domain) and cache poisoning.
- **Remediation:** Explicitly list domain names in `ALLOWED_HOSTS`. Never use `['*']` in production.

### 1.3 SQL Injection in Raw Queries & Extra Clauses
Django ORM automatically parameterizes `filter()`, `get()`, and `exclude()`. However, raw SQL methods do **not** escape inputs if passed as formatted strings.

```python
# ❌ VULNERABLE: Python f-string in raw() or extra()
users = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{request.GET['username']}'")
queryset = Post.objects.extra(where=[f"title = '{title}'"])

# ❌ VULNERABLE: Direct cursor string formatting
with connection.cursor() as cursor:
    cursor.execute(f"SELECT * FROM orders WHERE user_id = '{user_id}'")

# ✅ SECURE: Parameterized query bindings (tuple/list)
users = User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [request.GET['username']])

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
```

### 1.4 Cross-Site Scripting via `mark_safe()` and `|safe`
Django templates auto-escape all variables by default. Invoking `mark_safe()` or applying the `|safe` filter instructs the template engine to render raw HTML.

```python
from django.utils.safestring import mark_safe

# ❌ VULNERABLE: Marking untrusted user input as safe
def user_bio(request):
    bio_html = mark_safe(f"<div class='bio'>{request.user.bio}</div>")
    return render(request, "bio.html", {"bio": bio_html})

# ✅ SECURE: Sanitize using bleach before mark_safe, or let templates auto-escape
import bleach

def user_bio(request):
    clean_bio = bleach.clean(
        request.user.bio,
        tags=['b', 'i', 'u', 'em', 'strong', 'p', 'a'],
        attributes={'a': ['href', 'title']}
    )
    return render(request, "bio.html", {"bio": mark_safe(clean_bio)})
```

### 1.5 Insecure Deserialization (`pickle`)
```python
import pickle

# ❌ VULNERABLE: Deserializing untrusted session or cookie data
user_session = pickle.loads(request.COOKIES['session_data'])

# ✅ SECURE: JSON or signed cryptographic tokens (django.core.signing)
from django.core import signing

data = signing.loads(request.COOKIES['signed_session'])
```

### 1.6 ModelForm Mass Assignment via `fields = '__all__'`
```python
# ❌ VULNERABLE: '__all__' exposes administrative attributes like is_staff, is_superuser
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

# ✅ SECURE: Explicit field allowlist
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
```

---

## 2. FastAPI & Pydantic Security Architecture

### 2.1 SQL Injection in SQLAlchemy (`text()`)
```python
from sqlalchemy import text
from sqlalchemy.orm import Session

# ❌ VULNERABLE: f-string concatenation in text()
def get_user_by_email(db: Session, email: str):
    return db.execute(text(f"SELECT * FROM users WHERE email = '{email}'")).fetchall()

# ✅ SECURE: Parameterized bound parameters (:param)
def get_user_by_email(db: Session, email: str):
    return db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": email}
    ).fetchall()
```

### 2.2 Insecure CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

# ❌ VULNERABLE: Wildcard origins with credentials allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # Security risk: browsers allow credentialed cross-origin read
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SECURE: Strict domain allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "https://admin.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 2.3 SSRF via HTTP Client (`httpx` / `requests`)
```python
import httpx
import ipaddress
import socket
from urllib.parse import urlparse

# ❌ VULNERABLE: Direct request to user-supplied webhook
@app.post("/webhook/test")
async def test_webhook(url: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url) # Attacker targets: http://169.254.169.254/latest/meta-data/
        return resp.text

# ✅ SECURE: Validate IP is not private/loopback
def validate_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid protocol")
    ip_str = socket.gethostbyname(parsed.hostname)
    ip = ipaddress.ip_address(ip_str)
    if ip.is_private or ip.is_loopback or ip.is_link_local:
        raise ValueError("Private IP destinations are forbidden")
```

---

## 3. Flask Security Architecture

### 3.1 Server-Side Template Injection (SSTI) in Jinja2
```python
from flask import render_template_string, request

# ❌ VULNERABLE: Concatenating user input into template string
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # Attacker passes: {{ config.items() }} or {{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)

# ✅ SECURE: Pass user input as template context variable
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    template = "<h1>Hello, {{ name }}!</h1>"
    return render_template_string(template, name=name)
```
