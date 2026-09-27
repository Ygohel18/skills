# Apple Human Interface Guidelines (HIG)

> Source: https://developer.apple.com/design/human-interface-guidelines/

## Core Principles (2–3 sentences)
Apple HIG is built on three pillars: **Clarity** (typography, whitespace, and colour purposefully direct attention), **Deference** (the UI recedes to let content lead), and **Depth** (layering, translucency, and animation establish spatial relationships without gimmickry). Typography, colour, and icons come from the Apple system to provide familiarity and automatic accessibility adaptations. Always use Dynamic Type and system semantic colours — never hardcode point sizes or hex values.

---

## Color System

### System Colours (iOS / macOS)
Apple provides semantic adaptive colours that automatically shift between light and dark:

| Semantic name | Light (approx) | Dark (approx) | Usage |
|---|---|---|---|
| `systemBlue` | `#007AFF` | `#0A84FF` | Default tint, links, primary CTA |
| `systemGreen` | `#34C759` | `#30D158` | Success, go states |
| `systemRed` | `#FF3B30` | `#FF453A` | Destructive, error |
| `systemOrange` | `#FF9500` | `#FF9F0A` | Warnings |
| `systemPurple` | `#AF52DE` | `#BF5AF2` | Secondary accent |
| `systemYellow` | `#FFCC00` | `#FFD60A` | Caution |
| `label` | `#000000` | `#FFFFFF` | Primary text |
| `secondaryLabel` | `rgba(60,60,67,0.6)` | `rgba(235,235,245,0.6)` | Secondary text |
| `systemBackground` | `#FFFFFF` | `#000000` | App root background |
| `secondarySystemBackground` | `#F2F2F7` | `#1C1C1E` | Grouped table background |
| `tertiarySystemBackground` | `#FFFFFF` | `#2C2C2E` | Cards on grouped bg |
| `separator` | `rgba(60,60,67,0.36)` | `rgba(84,84,88,0.65)` | Dividers |

### Vibrancy
Use vibrancy for text/icons over blurred materials — never composite on pure colours.
CSS equivalent: `backdrop-filter: blur(20px) saturate(180%); background: rgba(255,255,255,0.72);` (light).

### Accent colour
One app-wide accent (user-configurable on macOS). Avoid multiple competing accent colours.

---

## Typography Scale

Font: **SF Pro** (iOS/macOS), **SF Compact** (watchOS). Fallback: `-apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial`.

| Style | Size (default) | Weight | Usage |
|---|---|---|---|
| Large Title | 34pt | Bold (700) | Navigation large title |
| Title 1 | 28pt | Bold | Primary page title |
| Title 2 | 22pt | Bold | Section headers |
| Title 3 | 20pt | Semibold (600) | Sub-section headers |
| Headline | 17pt | Semibold | List section headers |
| Body | 17pt | Regular (400) | Primary reading text |
| Callout | 16pt | Regular | Secondary reading, sidebars |
| Subheadline | 15pt | Regular | Secondary info |
| Footnote | 13pt | Regular | Footnotes, captions |
| Caption 1 | 12pt | Regular | Labels, smallest readable |
| Caption 2 | 11pt | Regular | Absolute minimum |

**Dynamic Type:** Always use named styles, not fixed sizes. Users may set their preferred size up to XXX-Large (to 53pt body).
**Never** use font weights below Regular at body size or below.

---

## Spacing & Layout

- **Base unit:** 8pt grid (multiples of 4pt acceptable)
- **Screen margins:** 16pt (standard), 20pt (large screen)
- **Content insets:** Minimum 16pt horizontal padding from screen edge
- **Cell heights:** Standard 44pt (minimum touch target), 60pt (subtitle cell), 76pt (image cell)
- **Navigation bar height:** 44pt (compact), 52pt (regular, with large title)
- **Tab bar height:** 49pt (standard), 83pt (home indicator devices)
- **Status bar clearance:** Always use `safeAreaInsets` — never hardcode offsets

---

## Elevation / Depth Model

HIG uses **layered materials** rather than numeric elevation:

| Material | Usage | CSS approximation |
|---|---|---|
| **Regular** (default) | Sheets, popovers | `backdrop-filter: blur(20px); background: rgba(255,255,255,0.8)` |
| **Thin** | Transient backgrounds | `backdrop-filter: blur(8px); background: rgba(255,255,255,0.6)` |
| **Thick** | Modal sheets | `backdrop-filter: blur(30px); background: rgba(255,255,255,0.9)` |
| **Chrome** | Sidebars, toolbars | `backdrop-filter: blur(40px) saturate(200%); background: rgba(246,246,246,0.8)` |

Shadows are used sparingly (popovers, menus): `box-shadow: 0 4px 24px rgba(0,0,0,0.12), 0 1px 4px rgba(0,0,0,0.08)`.

---

## Corner Radius Conventions

| Context | iOS radius | macOS radius |
|---|---|---|
| Full-screen views | 0 (extends to edges) | N/A |
| Cards / grouped cells | 10pt | 8pt |
| Action sheets, drawers | 12pt (top only) | — |
| Buttons (standard) | 10pt | 6pt |
| Buttons (pill) | 9999pt | — |
| Icons (app icon) | 22.5% of size (superellipse) | Same |
| Alerts | 14pt | 10pt |
| Popovers | 14pt | 10pt |

---

## Motion Principles

- **Prefer spring animations** over linear/cubic easing — physics feel natural and alive
- Standard spring: `damping: 0.8, stiffness: 300` (SwiftUI default)
- Duration: Never set explicitly when using springs — let physics determine
- CSS approximation for spring feel: `transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)`
- Transitions must be purposeful — only animate when it conveys information about spatial relationships
- Avoid decorative animations; every motion should have semantic intent
- Parallax on 3D Touch / hover: subtle tilt effect on icons (2–4deg max)

---

## Iconography

- **Library:** [SF Symbols](https://developer.apple.com/sf-symbols/) — 6,000+ icons with variable weight, scale, and rendering modes
- **Not available as open SVG** — requires macOS SF Symbols app or SwiftUI `Image(systemName:)`
- **Web alternative:** Use SF Symbols `.svg` exports (via the macOS app) or licensed alternatives
- **Weight:** Always match symbol weight to surrounding text weight
- **Scale:** Three scales — Small, Medium (default), Large — always use Medium unless explicitly aligning with compact text
- **Rendering modes:** Monochrome, Hierarchical, Palette, Multicolor — pick one mode per context

---

## 5 Signature "Tells" — Unmistakably Apple HIG

1. **SF Pro font** — `-apple-system` stack, large title boldly scaled at 34pt, thin body at 17pt Regular
2. **Translucent materials** — sidebar, sheet, and navigation backgrounds use `backdrop-filter` blur, not solid fills
3. **Single accent colour** — one app tint (default `systemBlue`) applied consistently; no multi-colour accent scheme
4. **Large navigation titles** that collapse on scroll (`UINavigationController` large title behaviour)
5. **44×44pt minimum touch targets** everywhere — even icon buttons have invisible tappable area
