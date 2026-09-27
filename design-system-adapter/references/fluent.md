# Microsoft Fluent 2

> Source: https://fluent2.microsoft.design/ | https://react.fluentui.dev/
> GitHub: https://github.com/microsoft/fluentui

## Core Principles (2–3 sentences)
Fluent 2 is Microsoft's cross-platform design system for Windows, web, iOS, and Android, built around **two-tier semantic tokens** (global primitives → alias semantics) and the philosophy that UI should feel **purposeful and efficient** without being cold. It combines a carefully calibrated shadow system for depth, Segoe UI Variable as its signature typeface, and a restrained-yet-warm colour palette anchored in Microsoft's `#0078D4` blue brand. Accessibility is first-class: every token automatically produces a high-contrast mode variant.

---

## Color System

### Two-Tier Token Architecture
- **Global tokens** — raw values: `colorPaletteBlueBorder2: #0078D4`
- **Alias tokens** — semantic names: `colorBrandBackground`, `colorNeutralBackground1`

Always use alias tokens in components — never global tokens directly.

### Key Alias Tokens
| Token | Light | Dark | Usage |
|---|---|---|---|
| `colorBrandBackground` | `#0078D4` | `#115EA3` | Primary action button fill |
| `colorBrandForeground1` | `#0078D4` | `#479EF5` | Links, active text |
| `colorNeutralBackground1` | `#FFFFFF` | `#1F1F1F` | Page background |
| `colorNeutralBackground2` | `#F5F5F5` | `#292929` | Secondary background |
| `colorNeutralBackground3` | `#F0F0F0` | `#333333` | Tertiary background |
| `colorNeutralForeground1` | `#242424` | `#FFFFFF` | Primary text |
| `colorNeutralForeground2` | `#424242` | `#D6D6D6` | Secondary text |
| `colorNeutralStroke1` | `#D1D1D1` | `#444444` | Default border |
| `colorStatusSuccessForeground1` | `#107C10` | `#54B054` | Success text |
| `colorStatusDangerForeground1` | `#A80000` | `#F1707B` | Error text |

### High Contrast Mode
Every alias token has an automatic high-contrast variant. Never override `color` with inline styles when using Fluent components — tokens cascade correctly.

### Brand Colours (standard palette)
Microsoft's brand blue ramp: `#0F3058` (darkest) → `#0078D4` (brand) → `#28A8E0` → `#C7E0F4` (lightest)

---

## Typography Scale

Font: **Segoe UI Variable** (Windows 11 system font). Web fallback: `'Segoe UI', system-ui, -apple-system, sans-serif`.

| Token | Size | Weight | Line Height |
|---|---|---|---|
| `fontSizeBase100` | 10px | 400 | 14px | Tiny labels |
| `fontSizeBase200` | 12px | 400 | 16px | Caption |
| `fontSizeBase300` | 14px | 400 | 20px | Body (default) |
| `fontSizeBase400` | 16px | 400 | 22px | Body large |
| `fontSizeBase500` | 20px | 600 | 28px | Subtitle |
| `fontSizeBase600` | 24px | 600 | 32px | Title 3 |
| `fontSizeHero700` | 28px | 700 | 36px | Title 2 |
| `fontSizeHero800` | 32px | 700 | 40px | Title 1 |
| `fontSizeHero900` | 40px | 700 | 52px | Large title |
| `fontSizeHero1000` | 68px | 700 | 92px | Display |

Weight tokens: `fontWeightRegular: 400`, `fontWeightMedium: 500`, `fontWeightSemibold: 600`, `fontWeightBold: 700`

CSS import (Google Fonts fallback): `@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap');`

---

## Spacing & Layout Grid

- **Base unit:** 4px (Fluent uses a 4px grid, unlike M3's 8dp)
- Standard spacing tokens: `spacingHorizontalXS: 4px`, `spacingHorizontalS: 8px`, `spacingHorizontalM: 12px`, `spacingHorizontalL: 16px`, `spacingHorizontalXL: 20px`, `spacingHorizontalXXL: 24px`, `spacingHorizontal3XL: 32px`
- **Component padding:** Inputs and buttons use `spacingHorizontalL` (16px) horizontal, `spacingVerticalS` (8px) vertical
- Layout grid: 12 columns, 24px gutters, 24px margin

---

## Elevation Model

Fluent 2 uses **dual-layer shadows** (key shadow + ambient shadow) to simulate realistic depth.

| Token | Box Shadow | Z-position |
|---|---|---|
| `shadow2` | `0 1px 2px rgba(0,0,0,0.14), 0 0 2px rgba(0,0,0,0.12)` | Resting cards |
| `shadow4` | `0 2px 4px rgba(0,0,0,0.14), 0 0 2px rgba(0,0,0,0.12)` | Hover cards |
| `shadow8` | `0 4px 8px rgba(0,0,0,0.14), 0 0 2px rgba(0,0,0,0.12)` | Focused/active cards |
| `shadow16` | `0 8px 16px rgba(0,0,0,0.14), 0 0 2px rgba(0,0,0,0.12)` | Dropdowns, menus |
| `shadow28` | `0 14px 28px rgba(0,0,0,0.24), 0 0 8px rgba(0,0,0,0.2)` | Dialogs, panels |
| `shadow64` | `0 32px 64px rgba(0,0,0,0.24), 0 0 8px rgba(0,0,0,0.2)` | Modals, drawers |

Dark mode shadow: opacity values are reduced by ~30% (darker backgrounds need less shadow contrast).

---

## Corner Radius Conventions

| Token | Value | Component examples |
|---|---|---|
| `borderRadiusNone` | 0px | Tables, data grids |
| `borderRadiusSmall` | 2px | Tags, compact chips |
| `borderRadiusMedium` | 4px | Buttons, input fields |
| `borderRadiusLarge` | 6px | Cards, dialogs |
| `borderRadiusXLarge` | 8px | Panels, feature cards |
| `borderRadiusCircular` | 10000px | Avatars, badges, pills |

Fluent 2 uses **notably smaller radii** than M3 — 4px buttons are a signature Fluent tell.

---

## Motion Principles

Fluent 2 uses **fast, purposeful** animations. Never slow or decorative.

| Type | Duration | Easing | Usage |
|---|---|---|---|
| Ultra-fast | 50ms | `cubic-bezier(0,0,1,1)` | State toggles (checkbox check) |
| Fast | 100ms | `cubic-bezier(0.1,0.9,0.2,1)` | Icon changes, badge updates |
| Normal | 200ms | `cubic-bezier(0.1,0.9,0.2,1)` | Collapse/expand, tooltip show |
| Slow | 300ms | `cubic-bezier(0.1,0.9,0.2,1)` | Panel slide in/out |
| Extra Slow | 500ms | `cubic-bezier(0.1,0.9,0.2,1)` | Page-level transitions |

Fluent easing `cubic-bezier(0.1,0.9,0.2,1)` = aggressive deceleration (snappy arrive, smooth settle). Never use linear easing for UI motion.

---

## Iconography

- **Library:** [Fluent System Icons](https://github.com/microsoft/fluentui-system-icons) — open-source, 2500+ icons
- **Styles:** Regular (outline) and Filled — use Regular by default, Filled for selected/active state
- **Sizes:** 12, 16, 20, 24, 28, 32, 48px — always use the matching size icon (don't scale)
- **Colour:** Icon should use `colorNeutralForeground1` or `colorBrandForeground1` for active
- **NPM:** `@fluentui/react-icons`

---

## 5 Signature "Tells" — Unmistakably Fluent 2

1. **Small, precise corner radii** — 4px buttons and inputs feel tighter and more precise than M3's pill shapes
2. **Dual-layer shadows** — cards have a key shadow + ambient shadow pair, creating a more "lifted paper" feel
3. **Segoe UI Variable** — the slightly condensed, crisp Microsoft system font is immediately recognisable
4. **`#0078D4` Microsoft Blue** as primary brand, never warm or purple-tinted
5. **Compact density by default** — Fluent 2 packs more content into less space than Material or Apple — it's a productivity-first system
