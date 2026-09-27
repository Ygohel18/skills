# GitHub Primer Design System

> Source: https://primer.style/ | https://primer.style/design/ | https://primer.style/tokens/
> GitHub: https://github.com/primer/primitives | https://github.com/primer/react

## Core Principles (2–3 sentences)
Primer is GitHub's design system designed to support complex, density-heavy developer workflows with maximum clarity and speed. It prioritizes semantic consistency, rock-solid accessibility (WCAG AA/AAA compliance), and high contrast through functional tokens. Rather than dramatic ornamentation, Primer emphasizes crisp hairline borders, purposeful typography hierarchies, and predictable component affordances.

---

## Color System

Primer uses a functional, role-based token architecture built on top of base scales (50–900). Tokens are split into foreground (`fg`), background (`canvas`), border (`border`), and interactive/feedback states.

### Key Functional Tokens
| Token | Light Default | Dark Default | Semantic Role |
|---|---|---|---|
| `fg.default` | `#1F2328` | `#F0F6FC` | Primary text and icons |
| `fg.muted` | `#656D76` | `#9198A1` | Secondary/helper text, timestamps |
| `fg.subtle` | `#6E7781` | `#7D8590` | Placeholder text, disabled glyphs |
| `canvas.default` | `#FFFFFF` | `#0D1117` | Primary page canvas / background |
| `canvas.subtle` | `#F6F8FA` | `#161B22` | Secondary background, code blocks, headers |
| `canvas.inset` | `#F6F8FA` | `#010409` | Inset backgrounds, text areas |
| `border.default` | `#D0D7DE` | `#30363D` | Standard container and card borders |
| `border.muted` | `#D8DEE4` | `#21262D` | Divider lines, subtle row separators |
| `accent.fg` | `#0969DA` | `#4493F8` | Primary links, active navigation items |
| `accent.emphasis` | `#0969DA` | `#1F6FEB` | Primary button backgrounds, active badges |
| `success.fg` | `#1A7F37` | `#3FB950` | Open PR / commit success, status badges |
| `success.emphasis` | `#1F883D` | `#238636` | Primary action button ("Merge", "Commit") |
| `attention.fg` | `#9A6700` | `#D29922` | Warnings, WIP states, draft PRs |
| `danger.fg` | `#D1242F` | `#F85149` | Destructive actions, closed issues/PRs |
| `done.fg` | `#8250DF` | `#A371F7` | Merged PRs, completed milestones |

### Dark Mode Architecture
Primer features 4 distinct dark and dimmed themes:
- `dark_default` (canvas `#0D1117`, border `#30363D`)
- `dark_dimmed` (canvas `#22272E`, border `#444C56`)
- `dark_high_contrast` (pure black `#0A0C10`, stark white text)
- `dark_colorblind` (adapted categorical hues)

Theme switching is handled entirely via CSS custom properties mapped onto `data-color-mode="dark"` or `data-dark-theme="dark"`. Hardcoding hex colors without CSS variable references is strictly avoided.

---

## Typography Scale

Font Stack:
- **UI / Body:** `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"`
- **Monospace / Code:** `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace`

### Named Typography Steps
| Token | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `text-display` | 40px–48px | 1.25 | 500 / 600 | Marketing heroes, top-level headings |
| `text-title-large` | 32px | 1.25 | 600 | Repository / org titles |
| `text-title-medium` | 20px | 1.4 | 600 | Card titles, section headers |
| `text-title-small` | 16px | 1.5 | 600 | Subsections, item titles |
| `text-body-large` | 16px | 1.5 | 400 | Longform documentation, readme body |
| `text-body-medium` | 14px | 1.4285 | 400 / 600 | Standard UI text, list rows, button labels |
| `text-body-small` | 12px | 1.3333 | 400 | Meta text, commit SHAs, file stats, timestamps |
| `text-code-inline` | 12px / 14px | 1.45 | 400 | Inline code, git hashes, branch names |

---

## Spacing & Layout Grid

- **Base unit:** 4px (with 8px rhythm for major containers)
- **Spacing tokens:**
  - `space-1` = 4px
  - `space-2` = 8px
  - `space-3` = 16px
  - `space-4` = 24px
  - `space-5` = 32px
  - `space-6` = 40px
  - `space-7` = 48px
  - `space-8` = 64px
- **Layout Max Width:** 1280px standard container (`container-xl`)
- **Breakpoints:**
  - `sm`: 544px
  - `md`: 768px
  - `lg`: 1012px
  - `xl`: 1280px
  - `xxl`: 1400px

---

## Elevation & Materiality Model

Primer deliberately avoids heavy drop shadows or skeumorphic depth. Spatial separation is achieved almost entirely via **hairline borders (1px solid)** and subtle contrast between `canvas.default` and `canvas.subtle`.

### Shadow Tokens
| Token | Box Shadow | Usage |
|---|---|---|
| `shadow-resting-xsmall` | `0 1px 0 rgba(31, 35, 40, 0.04)` | Standard buttons resting state |
| `shadow-resting-small` | `0 1px 0 rgba(31, 35, 40, 0.04), inset 0 1px 0 rgba(255, 255, 255, 0.25)` | Primary callout buttons |
| `shadow-resting-medium` | `0 3px 6px rgba(140, 149, 159, 0.15)` | Dropdowns, autocomplete popovers |
| `shadow-floating-large` | `0 8px 24px rgba(140, 149, 159, 0.2)` | Modals, dialogs, branch switchers |
| `shadow-inset` | `inset 0 1px 0 rgba(208, 215, 222, 0.2)` | Input fields, search bars |

---

## Corner Radius Conventions

Primer keeps radii compact and disciplined to preserve density:
- **Small (`border-radius-small`):** `3px` — Badges, count labels, status pills, inline tags
- **Medium (`border-radius-medium`):** `6px` — Standard buttons, input fields, cards, popover menus
- **Large (`border-radius-large`):** `12px` — Floating modals, banner callouts
- **Full (`border-radius-full`):** `9999px` — User avatars (circular), pill badges

---

## Motion & Animation Principles

Animations in Primer are fast, subtle, and utilitarian:
- **Duration:** 100ms–200ms for hover and popover transitions; maximum 300ms for drawer slides.
- **Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (snappy ease-out).
- **Reduced Motion:** Always respected with `@media (prefers-reduced-motion: reduce) { transition: none; animation: none; }`.

---

## Iconography Style

- **System:** **GitHub Octicons** (SVG icons with 16px and 24px native grids).
- **Key attributes:** Monoline, 1.5px/2px stroke feel, pixel-snapped to 16x16 boundaries.
- **Common icons:** Repo (`repo`), Git PR (`git-pull-request`), Git Branch (`git-branch`), Issue (`issue-opened`), Star (`star`), Check (`check`), Alert (`alert`).

---

## Signature Visual "Tells"

1. **Crisp 1px borders everywhere:** Cards, sidebars, headers, and code diffs use `1px solid var(--borderColor-default)` with 6px rounded corners.
2. **Pill counter badges:** Numeric indicators (e.g. `(42)`) in tabs and buttons are styled with 3px/9999px radii and subtle gray background `#AFB8C133`.
3. **Dual-font code / UI pairing:** Strict distinction between monospace code/hashes and system UI sans-serif for controls.
4. **Distinct status semantics:** Specific green (`#1F883D`), purple (`#8250DF`), red (`#CF222E`), and yellow/amber (`#9A6700`) associated with git states (open, merged, closed, draft).
5. **Segmented / Underline Tab navigation:** Horizontal nav with subtle bottom indicator bar and active bolding.
