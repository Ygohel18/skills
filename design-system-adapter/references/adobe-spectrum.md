# Adobe Spectrum (Spectrum 2 / Spectrum Web Components)

> Source: https://spectrum.adobe.com/ | https://opensource.adobe.com/spectrum-web-components/
> GitHub: https://github.com/adobe/spectrum-tokens
> Confidence: **Fully documented spec** (Adobe Spectrum is an industry benchmark for cross-platform tokens, color mathematics, scale dimensions, and WCAG accessibility compliance).

## Core Principles (2–3 sentences)
Adobe Spectrum is the unified design system powering Creative Cloud, Document Cloud, and Experience Cloud applications (Photoshop, Illustrator, Acrobat, Premiere, Firefly). It emphasizes **tool-grade precision, creative flow, visual quietness, and multi-scale responsiveness** (adaptive between mouse desktop and touch tablet/mobile). The interface avoids visual noise so user-created content remains the primary focal point.

---

## Color System

Spectrum features 4 official color themes: **Lightest**, **Light**, **Dark**, and **Darkest** (standard creative tool canvas like Photoshop).

### Core Semantic Tokens
| Token Name | Light Theme | Darkest Theme | Usage |
|---|---|---|---|
| `--spectrum-alias-background-color-default` | `#FFFFFF` | `#1D1D1D` | Canvas / document background |
| `--spectrum-alias-background-color-secondary` | `#F8F8F8` | `#252525` | Tool panels, sidebars |
| `--spectrum-alias-background-color-tertiary` | `#EAEAEA` | `#323232` | Well backgrounds, sub-panels |
| `--spectrum-alias-text-color-default` | `#222222` | `#E1E1E1` | Primary text and tool labels |
| `--spectrum-alias-text-color-secondary` | `#6E6E6E` | `#909090` | Helper text, keyboard shortcut labels |
| `--spectrum-alias-border-color-default` | `#D5D5D5` | `#3E3E3E` | Panel borders, input borders |
| `--spectrum-accent-color-900` | `#0265DC` | `#2680EB` | Primary CTA, active tool highlight |
| `--spectrum-semantic-positive-color-default` | `#2D9D78` | `#27AB83` | Success states |
| `--spectrum-semantic-negative-color-default` | `#E34850` | `#EC5B62` | Errors, warnings, destructive |

### Color Science
All colors in Spectrum are scientifically tuned using perceptual color algorithms to maintain mathematically consistent contrast ratios across all four themes.

---

## Typography Scale

Font: **Adobe Clean** (Proprietary). Open alternative: **Inter** or **Source Sans 3**.
Import: `@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap');`

| Step | Font Size (Medium Scale) | Line Height | Weight |
|---|---|---|---|
| Heading XXL | 36px | 45px | 700 |
| Heading XL | 28px | 35px | 700 |
| Heading L | 22px | 28px | 700 |
| Heading M | 18px | 24px | 700 |
| Heading S | 16px | 20px | 700 |
| Body L | 16px | 24px | 400 |
| Body M | 14px | 20px | 400 (Standard UI text) |
| Body S | 12px | 16px | 400 (Panel labels, shortcuts) |
| Body XS | 11px | 14px | 400 (Metadata, tooltips) |

---

## Spacing & Layout Scales

Spectrum introduces a dual-scale layout model: **Medium (Desktop / Mouse)** and **Large (Touch / Mobile)**.
- **Base Grid:** 8px base rhythm (with 4px and 2px micro steps).
- **Scale tokens (Medium Scale):**
  - `--spectrum-global-dimension-size-50`: 4px
  - `--spectrum-global-dimension-size-100`: 8px
  - `--spectrum-global-dimension-size-200`: 16px
  - `--spectrum-global-dimension-size-300`: 24px
  - `--spectrum-global-dimension-size-400`: 32px
- **Component Heights (Medium Scale):**
  - Buttons / Inputs: 32px (`--spectrum-global-dimension-size-400` in Medium)
  - Touch Button / Inputs: 40px (in Large touch mode)

---

## Elevation & Materiality Model

- Panels and workspace toolbars are **flat** with thin hairlines (`1px solid var(--spectrum-alias-border-color-default)`).
- Floating flyouts, color pickers, and tool popovers use soft omni-directional drops:
  - Dropdown: `0 1px 4px 0 rgba(0, 0, 0, 0.15)`
  - Tooltip: `0 2px 8px 0 rgba(0, 0, 0, 0.2)`
  - Modal: `0 10px 30px 0 rgba(0, 0, 0, 0.25)`

---

## Corner Radius Conventions

- Small controls (badges, tags): `2px`–`3px`
- Standard inputs and buttons: `4px`
- Large cards and dialogs: `8px`–`10px`
- Circular action buttons / avatars: `9999px`

---

## Motion & Animation Principles

- Animation is subtle, calm, and functional, never distracting creative attention:
  - Duration: 130ms (Fast / Tooltips), 160ms (Short / Buttons), 250ms (Regular / Menus).
  - Easing: `cubic-bezier(0, 0, 0.4, 1)` (Deceleration / Entrances).

---

## Iconography Style

- **System:** **Spectrum Workflow Icons** (18px, 24px).
- **Attributes:** Precision line-drawn vectors, 1.5px consistent stroke, perfectly aligned to pixel grid boundaries.

---

## Accessibility Notes
- Rigorous WCAG 2.1 AA/AAA compliance across all four themes.
- High-visibility keyboard focus indicator: 2px solid `--spectrum-accent-color-900` with 2px offset (`outline-offset: 2px`).
- Explicit support for screen readers, high contrast Windows modes, and keyboard navigation.

---

## Signature Visual "Tells"

1. **Four-tier theme switcher:** Darkest (`#1D1D1D`), Dark (`#252525`), Light (`#F8F8F8`), Lightest (`#FFFFFF`).
2. **Tool panel density:** Compact tool palettes featuring 32px square tool icon buttons, divider lines, and integrated scrubber sliders.
3. **Spectrum Action Buttons:** Subtle borderless or quiet ghost buttons with 18px tool icons that reveal a tinted gray background on hover.
4. **Slider scrubbers:** Precision range slider with central numeric readout badge and blue fill track.
5. **Keyboard shortcut badges:** Right-aligned monospaced key combinations (e.g. `⌘V`, `⇧Z`) rendered in muted text beside menu items.
