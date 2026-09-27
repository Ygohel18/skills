# Stack Reference: Plain HTML + Tailwind CDN

## File Structure

```
project/
├── index.html              ← /
├── about.html              ← /about
├── contact.html            ← /contact
├── faq.html                ← /faq
├── blog.html               ← /blog
├── blog-post.html          ← /blog/:slug (template)
├── login.html              ← /login
├── register.html           ← /register
├── forgot-password.html    ← /forgot-password
├── reset-password.html     ← /reset-password
├── otp.html                ← /otp
├── legal.html              ← /legal
├── legal-privacy.html      ← /legal/privacy
├── legal-terms.html        ← /legal/terms
├── legal-refund.html       ← /legal/refund
├── css/
│   └── tokens.css          ← All CSS variables from DESIGN.md
└── js/
    └── main.js             ← Mobile menu + interactions
```

## HTML Base Template

Every HTML file must start with this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title | Site Name</title>

  <!-- Fonts (from DESIGN.md section 3.1) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=HEADING_FONT:wght@400;600;700;800&family=BODY_FONT:wght@300;400;500;600&display=swap" rel="stylesheet" />

  <!-- Tailwind CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Tailwind Config (inline, extends with custom tokens) -->
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: {
              DEFAULT: 'var(--color-primary)',
              hover: 'var(--color-primary-hover)',
              light: 'var(--color-primary-light)',
            },
            secondary: {
              DEFAULT: 'var(--color-secondary)',
            },
            bg: {
              DEFAULT: 'var(--color-bg)',
              alt: 'var(--color-bg-alt)',
              card: 'var(--color-bg-card)',
              input: 'var(--color-bg-input)',
            },
            text: {
              DEFAULT: 'var(--color-text)',
              muted: 'var(--color-text-muted)',
              faint: 'var(--color-text-faint)',
              inverse: 'var(--color-text-inverse)',
            },
            heading: 'var(--color-heading)',
            border: {
              DEFAULT: 'var(--color-border)',
              strong: 'var(--color-border-strong)',
            },
          },
          fontFamily: {
            display: ['HEADING_FONT', 'system-ui', 'sans-serif'],
            body: ['BODY_FONT', 'system-ui', 'sans-serif'],
          },
          borderRadius: {
            sm: 'var(--radius-sm)',
            DEFAULT: 'var(--radius-md)',
            md: 'var(--radius-md)',
            lg: 'var(--radius-lg)',
            xl: 'var(--radius-xl)',
            full: '9999px',
          },
          boxShadow: {
            card: 'var(--shadow-card)',
            elevated: 'var(--shadow-elevated)',
          },
        },
      },
    }
  </script>

  <!-- CSS Variables (paste all from DESIGN.md section 2.1) -->
  <style>
    :root {
      --color-primary:        #XXXXXX;
      --color-primary-hover:  #XXXXXX;
      --color-primary-light:  #XXXXXX;
      --color-bg:             #XXXXXX;
      --color-bg-alt:         #XXXXXX;
      --color-bg-card:        #XXXXXX;
      --color-bg-input:       #XXXXXX;
      --color-text:           #XXXXXX;
      --color-text-muted:     #XXXXXX;
      --color-text-faint:     #XXXXXX;
      --color-text-inverse:   #XXXXXX;
      --color-heading:        #XXXXXX;
      --color-border:         #XXXXXX;
      --color-border-strong:  #XXXXXX;
      --radius-sm:            4px;
      --radius-md:            8px;
      --radius-lg:            12px;
      --radius-xl:            16px;
      --shadow-card:          0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
      --shadow-elevated:      0 10px 25px -5px rgba(0,0,0,0.1);
    }

    body {
      font-family: 'BODY_FONT', system-ui, sans-serif;
      background-color: var(--color-bg);
      color: var(--color-text);
    }

    h1, h2, h3, h4, h5, h6 {
      font-family: 'HEADING_FONT', system-ui, sans-serif;
      color: var(--color-heading);
    }
  </style>
</head>

<body class="antialiased">
  <!-- HEADER (same across all pages) -->
  <header class="sticky top-0 z-50 border-b border-[color:var(--color-border)] bg-[color:var(--color-bg)] bg-opacity-95 backdrop-blur-sm">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
      <!-- Logo -->
      <a href="/" class="font-display text-xl font-bold text-[color:var(--color-heading)]">Logo</a>

      <!-- Desktop Nav -->
      <nav class="hidden items-center gap-1 md:flex">
        <a href="/" class="px-3 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Home</a>
        <a href="/about.html" class="px-3 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">About</a>
        <a href="/blog.html" class="px-3 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Blog</a>
        <a href="/faq.html" class="px-3 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">FAQ</a>
        <a href="/contact.html" class="px-3 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Contact</a>
      </nav>

      <!-- CTA -->
      <div class="hidden items-center gap-3 md:flex">
        <a href="/login.html" class="px-4 py-2 text-sm font-medium text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Log in</a>
        <a href="/register.html" class="rounded-md bg-[color:var(--color-primary)] px-4 py-2 text-sm font-medium text-[color:var(--color-text-inverse)] transition-colors hover:bg-[color:var(--color-primary-hover)]">Get started</a>
      </div>

      <!-- Mobile Toggle -->
      <button id="mobile-menu-toggle" class="md:hidden" aria-label="Toggle menu">
        <svg id="icon-menu" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
        <svg id="icon-close" xmlns="http://www.w3.org/2000/svg" class="hidden h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div id="mobile-menu" class="hidden border-t border-[color:var(--color-border)] px-6 py-4 md:hidden">
      <nav class="flex flex-col gap-1">
        <a href="/" class="rounded-md px-3 py-2.5 text-sm font-medium text-[color:var(--color-text-muted)] hover:bg-[color:var(--color-bg-alt)]">Home</a>
        <a href="/about.html" class="rounded-md px-3 py-2.5 text-sm font-medium text-[color:var(--color-text-muted)] hover:bg-[color:var(--color-bg-alt)]">About</a>
        <a href="/blog.html" class="rounded-md px-3 py-2.5 text-sm font-medium text-[color:var(--color-text-muted)] hover:bg-[color:var(--color-bg-alt)]">Blog</a>
        <a href="/faq.html" class="rounded-md px-3 py-2.5 text-sm font-medium text-[color:var(--color-text-muted)] hover:bg-[color:var(--color-bg-alt)]">FAQ</a>
        <a href="/contact.html" class="rounded-md px-3 py-2.5 text-sm font-medium text-[color:var(--color-text-muted)] hover:bg-[color:var(--color-bg-alt)]">Contact</a>
      </nav>
      <div class="mt-4 flex gap-2 border-t border-[color:var(--color-border)] pt-4">
        <a href="/login.html" class="flex-1 rounded-md border border-[color:var(--color-border)] px-4 py-2 text-center text-sm font-medium">Log in</a>
        <a href="/register.html" class="flex-1 rounded-md bg-[color:var(--color-primary)] px-4 py-2 text-center text-sm font-medium text-[color:var(--color-text-inverse)]">Sign up</a>
      </div>
    </div>
  </header>

  <!-- PAGE CONTENT -->
  <main>
    <!-- Insert page-specific content here -->
  </main>

  <!-- FOOTER -->
  <footer class="border-t border-[color:var(--color-border)] bg-[color:var(--color-bg-alt)]">
    <div class="mx-auto max-w-7xl px-6 py-12">
      <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <a href="/" class="font-display text-lg font-bold text-[color:var(--color-heading)]">Logo</a>
          <p class="mt-3 text-sm text-[color:var(--color-text-muted)]">Company tagline here.</p>
        </div>
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-wider text-[color:var(--color-text-muted)]">Product</h4>
          <ul class="mt-3 space-y-2">
            <li><a href="#" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Features</a></li>
            <li><a href="#" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Pricing</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-wider text-[color:var(--color-text-muted)]">Company</h4>
          <ul class="mt-3 space-y-2">
            <li><a href="/about.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">About</a></li>
            <li><a href="/blog.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Blog</a></li>
            <li><a href="/contact.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-wider text-[color:var(--color-text-muted)]">Legal</h4>
          <ul class="mt-3 space-y-2">
            <li><a href="/legal-privacy.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Privacy</a></li>
            <li><a href="/legal-terms.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Terms</a></li>
            <li><a href="/legal-refund.html" class="text-sm text-[color:var(--color-text-muted)] hover:text-[color:var(--color-text)]">Refund Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="mt-8 border-t border-[color:var(--color-border)] pt-8 text-center text-xs text-[color:var(--color-text-faint)]">
        &copy; 2025 Company Name. All rights reserved.
      </div>
    </div>
  </footer>

  <!-- Mobile menu script -->
  <script>
    const toggle = document.getElementById('mobile-menu-toggle')
    const menu = document.getElementById('mobile-menu')
    const iconMenu = document.getElementById('icon-menu')
    const iconClose = document.getElementById('icon-close')

    toggle.addEventListener('click', () => {
      const isOpen = !menu.classList.contains('hidden')
      menu.classList.toggle('hidden', isOpen)
      iconMenu.classList.toggle('hidden', !isOpen)
      iconClose.classList.toggle('hidden', isOpen)
    })
  </script>
</body>
</html>
```

## Auth Page Pattern (HTML)

For login.html, register.html, etc. — replace `<main>` content:

```html
<main class="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
  <div class="w-full max-w-sm rounded-xl border border-[color:var(--color-border)] bg-[color:var(--color-bg-card)] p-8 shadow-[var(--shadow-elevated)]">
    <!-- Logo -->
    <div class="mb-6 text-center">
      <span class="font-display text-2xl font-bold text-[color:var(--color-heading)]">Logo</span>
    </div>

    <h1 class="mb-1 text-center font-display text-2xl font-bold text-[color:var(--color-heading)]">Welcome back</h1>
    <p class="mb-6 text-center text-sm text-[color:var(--color-text-muted)]">Sign in to your account</p>

    <form class="space-y-4">
      <div>
        <label for="email" class="mb-1.5 block text-sm font-medium text-[color:var(--color-text)]">Email</label>
        <input type="email" id="email" placeholder="you@example.com"
          class="w-full rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-bg-input)] px-3 py-2 text-sm text-[color:var(--color-text)] placeholder-[color:var(--color-text-faint)] outline-none transition focus:border-[color:var(--color-border-strong)] focus:ring-2 focus:ring-[color:var(--color-primary)] focus:ring-opacity-20" />
      </div>

      <div>
        <div class="mb-1.5 flex items-center justify-between">
          <label for="password" class="text-sm font-medium text-[color:var(--color-text)]">Password</label>
          <a href="/forgot-password.html" class="text-xs text-[color:var(--color-primary)] hover:underline">Forgot password?</a>
        </div>
        <input type="password" id="password" placeholder="••••••••"
          class="w-full rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-bg-input)] px-3 py-2 text-sm text-[color:var(--color-text)] placeholder-[color:var(--color-text-faint)] outline-none transition focus:border-[color:var(--color-border-strong)] focus:ring-2 focus:ring-[color:var(--color-primary)] focus:ring-opacity-20" />
      </div>

      <button type="submit"
        class="w-full rounded-md bg-[color:var(--color-primary)] px-4 py-2.5 text-sm font-semibold text-[color:var(--color-text-inverse)] transition hover:bg-[color:var(--color-primary-hover)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-primary)] focus:ring-offset-2">
        Sign in
      </button>
    </form>

    <p class="mt-4 text-center text-sm text-[color:var(--color-text-muted)]">
      Don't have an account?
      <a href="/register.html" class="font-medium text-[color:var(--color-primary)] hover:underline">Sign up</a>
    </p>
  </div>
</main>
```
