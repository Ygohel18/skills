# Stack: Plain HTML + Bootstrap 5

## Overview
Zero-build setup using Bootstrap 5 via CDN. Best for rapid prototyping, CMS integrations, or teams already familiar with Bootstrap's class system.

---

## CDN Setup (index.html boilerplate)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Project Name</title>

  <!-- Bootstrap 5 CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" />
  <!-- Bootstrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" />
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <style>
    :root {
      --bs-primary:    #YOUR_PRIMARY;
      --color-surface: #YOUR_SURFACE;
      --color-text:    #YOUR_TEXT;
      --font-heading:  'Inter', sans-serif;
      --font-body:     'Inter', sans-serif;
    }
    body { font-family: var(--font-body); color: var(--color-text); }
    h1,h2,h3,h4,h5,h6 { font-family: var(--font-heading); }
  </style>
</head>
<body>
  <!-- PAGE CONTENT -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## File Structure

```
project/
├── index.html
├── about.html
├── contact.html
├── faq.html
├── blog.html
├── blog-detail.html
├── login.html
├── register.html
├── forgot-password.html
├── reset-password.html
├── otp.html
├── legal.html
├── legal-privacy.html
├── legal-terms.html
├── legal-refund.html
├── css/
│   └── custom.css
├── js/
│   └── main.js
└── assets/images/
```

---

## Key Patterns

### Navbar
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary sticky-top">
  <div class="container">
    <a class="navbar-brand fw-bold fs-4" href="/">Brand</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0 gap-lg-1 align-items-lg-center">
        <li class="nav-item"><a class="nav-link" href="/about.html">About</a></li>
        <li class="nav-item"><a class="nav-link" href="/blog.html">Blog</a></li>
        <li class="nav-item">
          <a class="btn btn-primary ms-lg-2 px-4" href="/register.html">Get Started</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### Hero Section
```html
<section class="py-5 py-lg-6 text-center bg-dark text-white">
  <div class="container py-5">
    <h1 class="display-3 fw-bold mb-4">Your Headline Here</h1>
    <p class="lead text-white-50 mb-5 mx-auto" style="max-width:600px;">Supporting description.</p>
    <div class="d-flex flex-wrap gap-3 justify-content-center">
      <a href="/register.html" class="btn btn-primary btn-lg px-5">Get Started</a>
      <a href="/about.html" class="btn btn-outline-light btn-lg px-5">Learn More</a>
    </div>
  </div>
</section>
```

### Card Grid
```html
<section class="py-5">
  <div class="container">
    <div class="row g-4">
      <div class="col-sm-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body p-4">
            <div class="fs-1 mb-3">🚀</div>
            <h5 class="card-title fw-semibold">Feature Title</h5>
            <p class="card-text text-muted">Feature description.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Auth Page (Login)
```html
<main class="min-vh-100 d-flex align-items-center justify-content-center bg-light py-5">
  <div class="card shadow-sm border-0 w-100" style="max-width:420px;">
    <div class="card-body p-4 p-md-5">
      <div class="text-center mb-4">
        <a href="/" class="text-decoration-none fw-bold fs-3 text-primary">BrandLogo</a>
        <h1 class="h4 fw-bold mt-3 mb-1">Sign in to your account</h1>
      </div>
      <form>
        <div class="mb-3">
          <label for="email" class="form-label fw-medium">Email</label>
          <input type="email" id="email" class="form-control form-control-lg" placeholder="you@example.com" />
        </div>
        <div class="mb-4">
          <label for="password" class="form-label fw-medium">Password</label>
          <input type="password" id="password" class="form-control form-control-lg" placeholder="••••••••" />
        </div>
        <button type="submit" class="btn btn-primary w-100 btn-lg">Sign In</button>
      </form>
      <p class="text-center text-muted small mt-4 mb-0">
        No account? <a href="register.html" class="text-primary text-decoration-none fw-medium">Sign up</a>
      </p>
    </div>
  </div>
</main>
```

### Footer
```html
<footer class="bg-dark text-white py-5">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-4">
        <h5 class="fw-bold mb-3">BrandName</h5>
        <p class="text-white-50 small">Short company tagline.</p>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="fw-semibold mb-3">Legal</h6>
        <ul class="list-unstyled small text-white-50">
          <li class="mb-2"><a href="legal-privacy.html" class="text-white-50 text-decoration-none">Privacy</a></li>
          <li class="mb-2"><a href="legal-terms.html" class="text-white-50 text-decoration-none">Terms</a></li>
        </ul>
      </div>
    </div>
    <hr class="border-white border-opacity-25 mt-4"/>
    <p class="text-white-50 small text-center mb-0">&copy; 2024 BrandName. All rights reserved.</p>
  </div>
</footer>
```

---

## Custom CSS Overrides (css/custom.css)

```css
:root {
  --bs-border-radius:    0.5rem;
  --bs-border-radius-lg: 0.75rem;
}
.btn {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,.15);
}
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,.12) !important;
}
```

---

## Dark Mode

```html
<html lang="en" data-bs-theme="dark">
```

```js
// theme toggle (main.js)
const toggle = document.getElementById('theme-toggle');
toggle?.addEventListener('click', () => {
  const html = document.documentElement;
  html.dataset.bsTheme = html.dataset.bsTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', html.dataset.bsTheme);
});
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.dataset.bsTheme = saved;
```

---

## Bootstrap → DESIGN.md Token Mapping

| DESIGN.md Token   | Bootstrap Equivalent                       |
|-------------------|--------------------------------------------|
| `--color-primary` | `--bs-primary` + `--bs-primary-rgb`        |
| `--radius-card`   | `--bs-border-radius` override              |
| `--shadow-card`   | `.shadow-sm` override in custom.css        |
| `--font-heading`  | `h1-h6 { font-family }` in custom.css     |
| Spacing scale     | Bootstrap 4px base (`0.25rem`)             |

---

## Checklist

- [ ] Bootstrap 5 CSS + JS CDN on every page
- [ ] Bootstrap Icons CDN added
- [ ] Google Fonts imported (from DESIGN.md)
- [ ] CSS variables declared in custom.css
- [ ] Navbar responsive with collapse
- [ ] All required pages created as `.html` files
- [ ] Dark mode toggle implemented
- [ ] Forms use `form-control-lg` + proper labels
- [ ] Footer has all link groups
