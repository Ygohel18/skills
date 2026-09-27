# Uber Base Web Design System

> Source: https://baseweb.design/ | https://baseweb.design/guides/theming/
> GitHub: https://github.com/uber/baseweb
> Confidence: **Fully documented spec** (Uber publishes complete theme tokens, overrides architecture, and component libraries for web and mobile).

## Core Principles (2–3 sentences)
Uber Base Web is an enterprise-grade, accessible foundation created for high-reliability mobility, delivery, and internal operational dashboards. It is characterized by **bold monochrome contrast (stark black and white), clean geometric typography, sharp square or 0–4px radii, and minimal ornamentation**. Designed for re-theming, it uses a centralized token system that easily accommodates sub-brands (Uber Rider, Uber Driver, Uber Eats, Uber Freight).

---

## Color System

Base Web is anchored in high-contrast monochromes, using color almost exclusively for actionable states or semantic alerts.

### Core Theme Tokens
| Token Name | Light Theme | Dark Theme | Usage |
|---|---|---|---|
| `backgroundPrimary` | `#FFFFFF` | `#000000` | Canvas background |
| `backgroundSecondary` | `#F6F6F6` | `#141414` | Secondary containers, inputs, sidebars |
| `backgroundTertiary` | `#EEEEEE` | `#1F1F1F` | Hover states on secondary surfaces |
| `backgroundInversePrimary` | `#000000` | `#FFFFFF` | Primary button fill |
| `contentPrimary` | `#000000` | `#FFFFFF` | Primary text and headings |
| `contentSecondary` | `#545454` | `#AFAFAF` | Supporting text, descriptions |
| `contentTertiary` | `#757575` | `#6B6B6B` | Inactive icons, subtle captions |
| `borderOpaque` | `#E2E2E2` | `#292929` | Container outlines, card borders |
| `borderSelected` | `#000000` | `#FFFFFF` | Active selection border |
| `accent` | `#276EF1` | `#276EF1` | Uber interactive blue (links, active tabs) |
| `negative` | `#E11900` | `#E11900` | Destructive errors, cancellations |
| `positive` | `#0E8345` | `#0E8345` | Success indicators, trip confirmed |
| `warning` | `#FFE1A5` | `#FFE1A5` | Warning alerts |

---

## Typography Scale

Font: **Uber Move Text** (Body) and **Uber Move** (Display/Headlines). Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.

| Token | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `font1450` | 96px | 112px | 700 | Hero landing displays |
| `font1050` | 40px | 52px | 700 | Primary page titles |
| `font850` | 32px | 40px | 700 | Modal titles, section headers |
| `font650` | 24px | 32px | 600 | Card titles, group headers |
| `font450` | 16px | 22px | 600 | Emphasized subheaders, button labels |
| `font350` | 16px | 24px | 400 | Primary paragraph text |
| `font250` | 14px | 20px | 400 | Standard UI, table cells, form labels |
| `font150` | 12px | 16px | 400 | Helper captions, vehicle license plate meta |

---

## Spacing & Layout Grid

- **Base unit:** 4px (with 8px multiples)
- **Token Scale:**
  - `scale100`: 4px
  - `scale200`: 8px
  - `scale300`: 12px
  - `scale400`: 16px
  - `scale500`: 20px
  - `scale600`: 24px
  - `scale800`: 32px
  - `scale1200`: 48px
- **Grid:** 12-column responsive fluid grid with 24px gutters.

---

## Elevation & Materiality Model

Base Web is intentionally **ultra-flat and graphic**. Surfaces do not float with heavy shadows; they rely on crisp `1px solid var(--borderOpaque)` lines or stark contrasting fills:
- `lighting400`: `0 1px 4px 0 rgba(0, 0, 0, 0.12)` (Standard floating menu)
- `lighting600`: `0 4px 16px 0 rgba(0, 0, 0, 0.16)` (Modal dialogs)
- `lighting1000`: `0 12px 32px 0 rgba(0, 0, 0, 0.24)` (Drawer overlays)

---

## Corner Radius Conventions

Base Web adheres to very tight corner radii:
- `radius100`: 2px (Small tags)
- `radius200`: 4px (Standard buttons, cards, text inputs)
- `radius300`: 8px (Large card modules, floating modals)
- `radiusFull`: 9999px (Circular avatar, pill-shaped tags)

---

## Motion & Animation Principles

- Animation is brief, utilitarian, and decisive:
  - Timing: 100ms–200ms.
  - Easing: `cubic-bezier(0.2, 0, 0, 1)` (instant acceleration, gentle deceleration).
  - Used for drawer slide-outs and vehicle marker position interpolations.

---

## Iconography Style

- **System:** Base Web Icons (monochrome SVGs on a 16px / 24px grid).
- **Style:** Minimalist 2px stroke, geometric terminations, zero rounded caps.

---

## Accessibility Notes
- Meets WCAG 2.1 AA and Section 508.
- Stark monochrome design provides 15:1 to 21:1 contrast ratios between primary text and backgrounds.
- High-contrast 3px solid focus ring: `outline: 3px solid #000000` (light mode) or `#FFFFFF` (dark mode).

---

## Signature Visual "Tells"

1. **High-contrast black CTA buttons:** Primary buttons are solid pitch black (`#000000`) with crisp white text and 4px radius (or stark white buttons in dark mode).
2. **Graphic monochrome typography:** High-contrast headlines with tight line spacing in Uber Move.
3. **Pill-shaped status chips:** Minimalist status badges with muted gray background and dark text.
4. **Clean location waypoint inputs:** Pickup/destination input fields styled with square/circle bullet icons connected by a vertical dotted line.
5. **Architectural 1px dividers:** Flat card surfaces divided strictly with `#E2E2E2` hairline borders.
