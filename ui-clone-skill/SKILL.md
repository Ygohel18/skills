---
name: ui-clone
description: >
  Use this skill whenever the user provides a screenshot, image, or visual reference of any website,
  app, dashboard, or UI and wants to: analyze the design, clone it, recreate it, build it pixel-perfectly,
  generate components from it, produce a design system from it, or convert a screenshot to a reusable prompt.
  Triggers: uploading any UI screenshot, saying "clone this", "recreate this", "build this website",
  "make this look the same", "pixel perfect copy", "match this design", "analyze this UI",
  "screenshot to prompt", "describe this UI as a prompt", "generate a prompt from this design",
  "what prompt would recreate this", "generate components from this", or attaching any image of a
  website/app/dashboard/landing page. ALWAYS use this skill when an image of a UI is provided alongside
  any build/clone/recreate/analyze/prompt-generation intent.
metadata:
  author: yash
  version: "2.1"
  stacks: "html, bootstrap, vite-react, nextjs, shadcn, astro, laravel-blade, android-compose, android-xml, flutter, react-native"
allowed-tools: Bash(python3:*) Bash(pip:*) Bash(bash:*) Read Write
---

# UI Clone Skill

You are a senior UI engineer and design systems architect. When given a screenshot of a website, app, or UI, your job depends on what the user wants:

- **Screenshot → Prompt**: Analyze the screenshot and produce a detailed natural-language prompt describing the UI (Phase 0)
- **Screenshot → Code**: Analyze, document the design system, and generate pixel-perfect code (Phases 1–3)
- **Screenshot → Both**: Produce the prompt AND the code

Determine the mode from the user's intent. Default to **both prompt + code** if they say "clone this" or "build this".

Always complete all relevant phases **in order**. Never skip the analysis phase.

---

## Platform Context — Web vs App

Before writing any code, determine whether this is a **web project** or a **mobile app project**.

> **Read `references/web-vs-app-context.md` to understand what features apply to each platform.**

| Platform | Includes |
|---|---|
| **Web** (HTML, React, Next.js, Astro, Laravel) | Back-to-top button, SEO meta, footer, cookie banner, keyboard nav, responsive CSS breakpoints |
| **Mobile App** (Android, Flutter, React Native) | Bottom nav bar, safe area, splash screen, local fonts, platform theme, touch targets, hardware back nav |
| **Both** | Auth flows, legal pages, error/empty/loading states, brand tokens, accessibility, form validation |

**Web projects MUST include a Back-to-top button on every scrollable page.** See `references/web-vs-app-context.md` for implementation.

---

## Phase 0 — Screenshot to Prompt (Optional Mode)

> **Read `references/screenshot-to-prompt.md` for the full implementation guide.**

Activate this phase when the user asks to **describe the UI as a prompt** instead of (or before) building it.

**Trigger phrases:** "screenshot to prompt", "describe this as a prompt", "what prompt would recreate this?", "give me a prompt for this", "convert this to a prompt", "make a reusable prompt"

**What to produce:** A fully-structured `PROMPT.md` (or inline block) with:

```
## UI Rebuild Prompt: [Page Name]

### Overview      — 1–2 sentences: type of UI + aesthetic mood
### Layout        — spatial structure, zones, columns, max-width
### Color Palette — every color with its role + approximate hex
### Typography    — font, size, weight, color per element type
### Components    — every visible component with variant/state/details
### Spacing       — key measurements (padding, gap, heights, max-widths)
### Visual Effects— shadows, radius, gradients, animations, blur
### Content       — all visible text, labels, placeholder values
### Interactions  — hover/focus/active states, dropdown/modal behavior
### Responsive    — inferred mobile vs desktop behavior
```

After producing the prompt, ask:
```
Here’s your UI prompt. Would you like me to:
A) Use this to generate the full code now (pick a stack)
B) Save it as PROMPT.md
C) Both — save the prompt AND generate code
D) Just the prompt for now
```

See `references/screenshot-to-prompt.md` for full section-by-section instructions and complete output examples.

---

## Phase 1 — Deep Visual Analysis

Before writing a single line of code, analyze the screenshot exhaustively. Think through each layer:

### 1.1 Layout & Structure
- Overall page layout: full-width, boxed, asymmetric, grid-based?
- Number of columns, sidebar presence, sticky elements
- Header structure: height, content alignment, logo position, nav links, CTAs
- Hero/above-fold: full-viewport? split layout? image/video background?
- Section rhythm: padding between sections (estimate px values)
- Footer structure: columns, link groups, copyright bar

### 1.2 Color System
- **Background colors**: primary body bg, section alternates, card backgrounds
- **Brand/accent colors**: primary CTA color, secondary accent, hover states
- **Text colors**: headings, body, muted/secondary, links, placeholders
- **Border colors**: dividers, card borders, input borders
- **State colors**: success, error, warning, info, badge colors
- Identify exact or closest hex values for all observed colors

### 1.3 Typography
- Font families: heading font (serif/sans/display), body font, monospace if present
- Font sizes per element: h1, h2, h3, h4, body, small, caption, label, badge
- Font weights per element: identify 300/400/500/600/700/800/900 usage
- Line heights and letter spacing (estimate from visual)
- Text transforms: uppercase labels, title case headings?
- Font pairings: identify if Google Fonts, system fonts, or custom

### 1.4 Spacing & Sizing
- Base spacing unit (4px or 8px grid)
- Section vertical padding (estimate: sm/md/lg/xl)
- Card internal padding
- Button padding and height
- Input height and padding
- Gap between grid items
- Container max-width

### 1.5 Component Inventory
Identify every UI component visible:
- Navigation: type (topnav, sidebar, hamburger), items, dropdowns
- Buttons: sizes (sm/md/lg), variants (primary/secondary/ghost/outline/link), icon buttons
- Cards: shadow, border-radius, hover effect, image ratio
- Forms: input style, label position, validation indicators
- Badges/tags/chips: shape, color variants
- Icons: library style (outline/solid/duotone), approximate size
- Tables: striped? bordered? compact?
- Modals/dialogs: if visible
- Alerts/toasts: if visible
- Tabs/accordions: if visible
- Breadcrumbs/pagination: if visible
- Progress bars/steppers: if visible

### 1.6 Visual Style & Effects
- Border radius: none / subtle (2-4px) / medium (6-8px) / large (12-16px) / pill (9999px)
- Box shadows: none / subtle / card / elevated / dramatic — estimate spread/blur/color
- Glassmorphism: backdrop-blur, semi-transparent backgrounds?
- Gradients: linear/radial, directions, color stops
- Images: aspect ratios, object-fit style, overlay treatment
- Animations/transitions: hover lifts, fade-ins, skeleton loading indicators

### 1.7 Dark/Light Mode
- Is this a dark-mode or light-mode design?
- Are there mode-switching elements visible?

---

## Phase 2 — Generate DESIGN.md

After analysis, produce a complete `DESIGN.md` file. This is the single source of truth for the entire project.

See `references/DESIGN_MD_TEMPLATE.md` for the exact format to follow.

Key rules:
- Every color must have a CSS variable name AND hex value
- Every spacing value must map to a Tailwind class
- Every font must be specified with its Google Fonts import URL or fallback stack
- Document every component variant with its classes

**Optional: Use the bundled Python script to scaffold DESIGN.md faster** (see Scripts section below).

---

## Bundled Scripts

This skill includes executable scripts in `scripts/`. Run them with Python 3 or Bash — no external agent tool required beyond what's in `allowed-tools`.

### 1. `scripts/extract_colors.py` — Extract dominant colors from a screenshot

Run this **during Phase 1** when you have a saved image file. It uses pixel analysis to extract the most dominant colors and outputs a ready-to-paste color palette.

```bash
# Install dependency (one-time)
pip install Pillow colorthief

# Run
python3 scripts/extract_colors.py path/to/screenshot.png

# Options
python3 scripts/extract_colors.py screenshot.png --top 10 --format hsl
#   --top N       How many colors to extract (default: 8)
#   --format      hex | hsl | rgb  (default: hex)
```

Output: CSS variable block + color table ready to paste into DESIGN.md.

> **When to use:** When the user provides an actual image file path. Skip if the image is only visible in the conversation (analyse visually instead).

---

### 2. `scripts/generate_design_md.py` — Scaffold DESIGN.md from collected tokens

Run this **at the end of Phase 1 / start of Phase 2** once you've identified the key design tokens. It generates a complete pre-filled `DESIGN.md` with all sections, tables, CSS variables, and Tailwind config.

```bash
# No extra dependencies — stdlib only
python3 scripts/generate_design_md.py \
  --project "ProjectName" \
  --output DESIGN.md \
  --colors "primary=#6366F1,surface=#1E293B,text=#F8FAFC,muted=#94A3B8,border=#334155" \
  --font-heading "Inter" \
  --font-body "Inter" \
  --radius 12 \
  --mode dark
```

Output: a complete `DESIGN.md` written to the specified path.

> **When to use:** Always — this replaces manually writing DESIGN.md from scratch. Review and adjust the generated file against your Phase 1 analysis.

---

### 3. `scripts/validate_skill.sh` — Validate skill structure

For use by skill maintainers. Checks SKILL.md frontmatter, line count, and that all referenced files exist.

```bash
bash scripts/validate_skill.sh
# or from outside the skill directory:
bash /path/to/ui-clone-skill/scripts/validate_skill.sh /path/to/ui-clone-skill
```

> **When to use:** After making structural changes to this skill. Not used during normal UI-clone tasks.

---

## Phase 3 — Code Generation

### Step 3.1 — Confirm Stack

Ask the user which stack they want **if not already specified**:

**Web Stacks**
```
A)  Plain HTML + Tailwind CDN           (zero setup, fastest start)
B)  Plain HTML + Bootstrap 5            (zero setup, Bootstrap class system)
C)  Vite + React + Tailwind             (modern SPA)
D)  Next.js + Tailwind + shadcn/ui      (full-stack ready, recommended default)
E)  Astro + Vite + React + Tailwind     (content-focused MPA, minimal JS)
F)  Laravel Blade + Tailwind            (PHP full-stack, server-rendered)
```

**Mobile / Cross-Platform Stacks**
```
G)  Android — Jetpack Compose           (Kotlin, modern declarative UI)
H)  Android — Classic XML Views         (Kotlin/Java, traditional View system)
I)  Flutter                             (Dart, cross-platform iOS + Android + Web)
J)  React Native                        (TypeScript/JS, cross-platform iOS + Android)
```

Default to **D (Next.js + shadcn/ui)** if they say "best practice" or don't specify a stack.
Default to **E (Astro)** if they mention content sites, blogs, or minimal JavaScript.
Default to **G (Jetpack Compose)** for new Android-only projects.
Default to **I (Flutter)** for new cross-platform mobile projects.

### Step 3.2 — Project Scaffolding

Read the relevant stack reference before generating:
- Plain HTML + Tailwind  → `references/stack-html.md`
- Plain HTML + Bootstrap → `references/stack-html-bootstrap.md`
- Vite + React           → `references/stack-vite.md`
- Next.js + shadcn       → `references/stack-shadcn.md`
- Astro + Vite + React   → `references/stack-astro.md`
- Laravel Blade          → `references/stack-laravel-blade.md`
- Android Compose        → `references/stack-android-compose.md`
- Android XML            → `references/stack-android-xml.md`
- Flutter                → `references/stack-flutter.md`
- React Native           → `references/stack-react-native.md`

### Step 3.3 — Always-Required Pages & Routes

**Every project must include ALL of these routes**, regardless of what the screenshot shows. These are non-negotiable defaults:

```
/                       → Home page (cloned from screenshot)
/about                  → About page
/contact                → Contact page
/faq                    → FAQ page
/blog                   → Blog listing page
/blog/[slug]            → Blog detail page

/login                  → Login page
/register               → Register / Sign up page
/forgot-password        → Forgot password page
/reset-password         → Reset password page (with token param)
/otp                    → OTP / 2FA verification page

/legal                  → Legal hub page (links to all legal pages)
/legal/privacy          → Privacy policy page
/legal/terms            → Terms of service page
/legal/refund           → Refund / cancellation policy page
```

**For Next.js / shadcn**: Create `app/` directory with all routes as folders + `page.tsx`
**For Vite/React**: Create `src/pages/` and configure React Router with all routes
**For Astro**: Create `src/pages/` with file-based routing (`.astro` files); use `[slug].astro` for dynamic blog routes
**For HTML (Tailwind or Bootstrap)**: Create individual `.html` files for every route
**For Laravel Blade**: Define all routes in `routes/web.php`; create views in `resources/views/`
**For Android (Compose or XML)**: Create a screen/Fragment per route; configure Navigation Component with all destinations
**For Flutter**: Configure `GoRouter` with all routes; create a screen file per route under `lib/features/`
**For React Native**: Configure Stack + Tab navigators with all screen components

### Step 3.4 — Component Architecture

Organize components by type:

```
components/
├── layout/
│   ├── Header.tsx         ← nav, logo, CTA button, mobile menu
│   ├── Footer.tsx         ← links, copyright, socials
│   └── PageWrapper.tsx    ← consistent page padding/max-width
├── ui/
│   ├── Button.tsx         ← all variants from DESIGN.md
│   ├── Badge.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   └── ...
├── sections/
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── Testimonials.tsx
│   ├── Pricing.tsx
│   ├── CTA.tsx
│   └── ...
└── forms/
    ├── LoginForm.tsx
    ├── RegisterForm.tsx
    ├── ContactForm.tsx
    └── ...
```

### Step 3.5 — Pixel-Perfection Rules

When writing component code:

1. **Colors**: Use ONLY the CSS variables defined in DESIGN.md — never hardcode hex values
2. **Spacing**: Match the visual rhythm exactly — if sections have 80px padding, use `py-20`
3. **Typography**: Load the exact fonts from DESIGN.md, apply exact size/weight/tracking
4. **Borders**: Match border-radius exactly using custom Tailwind config values
5. **Shadows**: Match shadow depth exactly — use custom shadow tokens if needed
6. **Hover states**: Always implement hover/focus/active states as observed
7. **Responsive**: Always include mobile-first breakpoints (sm/md/lg/xl)
8. **Icons**: Use Lucide React (for Next.js/Vite/Astro islands) or inline SVGs (for HTML and static Astro components)

### Step 3.6 — Web-Specific Requirements (Web Stacks Only)

> Only applies to stacks A–F (HTML, Bootstrap, Vite, Next.js, Astro, Laravel). Skip for mobile stacks G–J.

**Back-to-Top button** — MANDATORY on every web page with scrollable content:
- Add to the root layout / template so it appears on every page automatically
- Appears only after scrolling ≥ 400px (fade-in animation)
- Fixed position: bottom-right (`bottom-6 right-6`)
- Smooth-scrolls to top on click
- Accessible: `aria-label="Back to top"`, keyboard-activatable
- See full implementation in `references/web-vs-app-context.md`

**SEO** — Every page must have `<title>`, `<meta name="description">`, Open Graph tags.

**Cookie banner** — Simple dismissible banner stored in `localStorage`.

**Skip-to-main-content** — First focusable element on every page for screen reader users.

### Step 3.7 — Custom UI Component Library (React-Based Web Stacks)

> Applies to stacks C (Vite), D (Next.js), E (Astro) when a custom component system already exists.

**Read `references/custom-ui-components.md` before implementing any UI component.**

Critical rules:
- **Do NOT install shadcn/ui**
- **Do NOT copy shadcn source code**
- All components must be re-implemented inside the project's own `components/ui/` directory
- Inspect existing components first — match their exact TypeScript patterns, `cn()` usage, `forwardRef`, variants, and export style
- Every component must: support controlled + uncontrolled mode, use `forwardRef`, set `displayName`, implement keyboard navigation, include correct ARIA attributes

Required component barrel (update `components/ui/index.ts`):
```
alert, alert-dialog, aspect-ratio, breadcrumb, calendar, checkbox,
collapsible, combobox, command, context-menu, drawer, form, hover-card,
input-otp, menubar, navigation-menu, pagination, progress, radio-group,
resizable, select, slider, table, toast, toggle, toggle-group
```
(Plus all existing: accordion, avatar, badge, button, card, dialog, dropdown-menu, input, label, popover, scroll-area, separator, sheet, skeleton, switch, tabs, textarea, tooltip)

### Step 3.8 — Auth Pages Standard

All auth pages (/login, /register, /forgot-password, /reset-password, /otp) must follow this pattern:
- Centered card layout on desktop, full-width on mobile
- Brand logo at top
- Clean form with validation states
- Link to related auth pages (login ↔ register, forgot-password link on login)
- Consistent with the site's color/typography system

### Step 3.9 — Legal Pages Standard

All legal pages must:
- Use the site's typography and color system
- Include consistent `<LastUpdated>` component
- Have a sidebar TOC on desktop (anchor links to sections)
- Have a legal hub `/legal` page with cards linking to each policy

### Step 3.10 — Blog System Standard

- `/blog` must show a grid of post cards (title, excerpt, date, category, author avatar)
- `/blog/[slug]` must show full article layout with:
  - Hero image
  - Author meta bar
  - Rich prose typography (matching site fonts, with `prose` class or equivalent)
  - Related posts section
  - CTA block at bottom

### Step 3.11 — UX Language & Copy Rules

> **Read `references/ux-language-rules.md` before writing any user-facing text.**

Assume every user of every screen is a **normal, non-technical person** — not a developer, not a designer.

- **Zero technical jargon** anywhere on screen (no "authentication error", no "500", no "null", no "token expired")
- **Error messages** must say what went wrong AND what to do next, in plain words
- **Button labels** describe the specific action, not generic verbs ("Save changes" not "Submit")
- **Empty states** are friendly and include an action when possible
- **Admin dashboards**: plain labels, no module names, no system terminology, no developer metrics
- **Status badges**: human words only ("Active", "Pending", "Cancelled") — never codes or flags
- **Loading states**: include context ("Loading your messages…" not just "Loading…")
- **Confirmation dialogs**: descriptive action buttons ("Yes, delete post" / "Keep post")

---

## Output Checklist

Before declaring done, verify:

**Design System**
- [ ] DESIGN.md generated with all tokens
- [ ] Stack-specific config extended with all DESIGN.md custom tokens
- [ ] Fonts imported correctly (CDN for web, bundled locally for apps)

**Routing & Pages**
- [ ] All required routes created (see Step 3.3 list)
- [ ] All routes work with no broken links

**Layout Components**
- [ ] Header component with working mobile nav
- [ ] Footer component with all link groups (web only)
- [ ] Back-to-top button in root layout (web only — Step 3.6)
- [ ] Bottom navigation bar (mobile apps only)

**Pages**
- [ ] Home page sections cloned from screenshot
- [ ] Auth pages complete with form validation
- [ ] Legal pages with content placeholders
- [ ] Blog listing + detail pages (web) or equivalent screens (app)

**Custom UI Components (React web stacks)**
- [ ] All 25 new components implemented in `components/ui/` (Step 3.7)
- [ ] Barrel export updated with all components
- [ ] No shadcn/ui installed or imported
- [ ] All components inspected against existing project patterns

**UX Language (every project)**
- [ ] Zero technical jargon visible to users
- [ ] All error messages are plain-language with next steps
- [ ] All empty states are friendly with actions where applicable
- [ ] All button labels describe the specific action
- [ ] Admin labels use plain nouns (if admin dashboard)
- [ ] Loading states include context text

**Quality**
- [ ] CSS variables declared in globals.css (web)
- [ ] All components responsive down to 375px (web) / adaptive layouts (app)
- [ ] Keyboard navigation works on all interactive elements (web)
- [ ] Touch targets ≥ 48×48dp (mobile apps)

---

## Reference Files

### Core References (Read on Every Project)
- `references/DESIGN_MD_TEMPLATE.md` — Exact format for the DESIGN.md output
- `references/web-vs-app-context.md` — **What applies to web vs mobile app** (Back-to-top, SEO, safe area, etc.)
- `references/ux-language-rules.md` — **Human-friendly copy rules** (no jargon, error messages, button labels, admin UI)
- `references/component-patterns.md` — Reusable patterns for common components

### Screenshot-to-Prompt Reference
- `references/screenshot-to-prompt.md` — **Full guide** for converting any screenshot into a structured UI rebuild prompt (section-by-section instructions + complete output example)

### Custom UI Component Library (React Web Stacks)
- `references/custom-ui-components.md` — **Full custom component implementations** (no shadcn — all 25 new components + barrel export)

### Web Stack References
- `references/stack-html.md` — Plain HTML + Tailwind CDN setup guide
- `references/stack-html-bootstrap.md` — Plain HTML + Bootstrap 5 setup guide
- `references/stack-vite.md` — Vite + React + Tailwind setup guide
- `references/stack-shadcn.md` — Next.js + shadcn/ui + Tailwind setup guide
- `references/stack-astro.md` — Astro + Vite + React + Tailwind setup guide
- `references/stack-laravel-blade.md` — Laravel Blade + Tailwind CSS setup guide

### Mobile / Cross-Platform Stack References
- `references/stack-android-compose.md` — Android Jetpack Compose (Kotlin + Material 3)
- `references/stack-android-xml.md` — Android Classic XML Views (Kotlin + Material Components)
- `references/stack-flutter.md` — Flutter (Dart + GoRouter + Riverpod + Material 3)
- `references/stack-react-native.md` — React Native (TypeScript + React Navigation + NativeWind)
