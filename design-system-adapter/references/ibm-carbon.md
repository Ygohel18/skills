# IBM Carbon Design System (Carbon v11)

> Source: https://carbondesignsystem.com/ | https://carbondesignsystem.com/guidelines/color/overview/
> NPM: `@carbon/styles`, `@carbon/react`
> Confidence: **Fully documented spec** (Carbon is an open-source, enterprise-grade, rigorously documented token system).

## Core Principles (2–3 sentences)
IBM Carbon is built upon the IBM Design Language, emphasizing **rationality, scientific precision, architectural balance, and ruthless accessibility**. It uses a strict 2x Grid system, deliberate high-contrast monochrome palettes with electric blue accents, and purposeful square or near-square geometry. Carbon is built specifically for complex enterprise platforms, data analytics, cloud consoles, and multi-tenant systems.

---

## Color System

Carbon defines four official themes:
- **Light themes:** `white` (pure white canvas) and `g10` (Gray 10, soft light gray).
- **Dark themes:** `g90` (Gray 90, deep charcoal) and `g100` (Gray 100, near black `#161616`).

### Core Semantic Tokens
| Token | White Theme | g100 Theme | Usage |
|---|---|---|---|
| `$background` | `#FFFFFF` | `#161616` | Main page canvas |
| `$layer-01` | `#F4F4F4` | `#262626` | First container/card layer |
| `$layer-02` | `#FFFFFF` | `#393939` | Secondary nested container layer |
| `$layer-03` | `#F4F4F4` | `#525252` | Tertiary elevated layer |
| `$text-primary` | `#161616` | `#F4F4F4` | Primary body, headlines |
| `$text-secondary` | `#525252` | `#C6C6C6` | Supporting labels, timestamps |
| `$text-placeholder` | `#A8A8A8` | `#6F6F6F` | Placeholder field text |
| `$text-on-color` | `#FFFFFF` | `#FFFFFF` | Text on primary brand buttons |
| `$interactive` | `#0F62FE` | `#0F62FE` | Carbon Interactive Blue (buttons, links) |
| `$border-subtle` | `#E0E0E0` | `#393939` | Container outlines, dividers |
| `$border-strong` | `#8D8D8D` | `#8D8D8D` | Input field borders, active tabs |
| `$focus` | `#0F62FE` | `#FFFFFF` | High-visibility focus ring |
| `$support-error` | `#DA1E28` | `#FA4D56` | Form validation error |
| `$support-success` | `#24A148` | `#42BE65` | Success indicators |

---

## Typography Scale

Font: **IBM Plex Sans** (UI), **IBM Plex Mono** (Code & Data Tables), **IBM Plex Serif** (Editorial).
Google Fonts: `@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');`

| Token | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `$heading-05` | 32px | 40px | 400 / 600 | Page titles, dashboard headlines |
| `$heading-04` | 28px | 36px | 400 / 600 | Modal titles, major section headers |
| `$heading-03` | 20px | 26px | 400 / 600 | Card titles, drawer headers |
| `$heading-02` | 16px | 22px | 600 | Subheadings, table column groups |
| `$heading-01` | 14px | 18px | 600 | Fieldset headers, section subheaders |
| `$body-long-02` | 16px | 24px | 400 | Editorial text, documentation |
| `$body-short-02` | 16px | 22px | 400 | Table rows, notifications |
| `$body-short-01` | 14px | 18px | 400 | Standard UI controls, inputs, buttons |
| `$label-01` | 12px | 16px | 400 | Form labels, helper captions |
| `$code-01` | 12px | 16px | 400 (Mono) | Inline code snippets, hashes |

---

## Spacing & 2x Grid System

- **Base unit:** 8px base rhythm (mini-unit: 4px).
- **Spacing tokens:**
  - `$spacing-01`: 2px
  - `$spacing-02`: 4px
  - `$spacing-03`: 8px
  - `$spacing-04`: 12px
  - `$spacing-05`: 16px
  - `$spacing-06`: 24px
  - `$spacing-07`: 32px
  - `$spacing-08`: 40px
  - `$spacing-09`: 48px
- **Density Options:**
  - Carbon defines explicit height scales for controls (Buttons, Inputs, Table Rows):
    - `xs`: 24px
    - `sm`: 32px (Compact enterprise mode)
    - `md`: 40px (Comfortable standard)
    - `lg`: 48px (Spacious)
    - `xl`: 64px

---

## Elevation & Materiality Model

Carbon is resolutely **flat and architectural**. It replaces arbitrary floating drop shadows with a **layering model**:
- Physical elevation is expressed by shifting background tokens from `$background` $\rightarrow$ `$layer-01` $\rightarrow$ `$layer-02` $\rightarrow$ `$layer-03`.
- In light mode, layers shift darker (`#FFFFFF` $\rightarrow$ `#F4F4F4` $\rightarrow$ `#E0E0E0`).
- In dark mode, layers shift lighter (`#161616` $\rightarrow$ `#262626` $\rightarrow$ `#393939`).
- Modals and transient popovers use crisp, tight geometric box shadows:
  - Dropdown / Menu: `0 2px 6px 0 rgba(0, 0, 0, 0.2)`
  - Modal: `0 12px 24px 0 rgba(0, 0, 0, 0.1)`

> **Conflict note:** Heavy organic drop shadows, rounded pill buttons, or whimsical gradients violate Carbon core guidelines.

---

## Corner Radius Conventions

- Carbon components have **0px corner radius** (strictly square corners) by default across all inputs, cards, dialogs, and primary buttons!
- Badges and tags: `border-radius: 9999px` or `0px`.
- Toggle switches: `border-radius: 9999px`.
- Everything else: `0px` sharp geometric corners.

---

## Motion & Animation Principles

Carbon motion is mechanical, precise, and purposeful.
- **Productive Motion:** 90ms–150ms for operational tasks (dropdowns, accordions, button clicks).
- **Expressive Motion:** 240ms–400ms for system expansions, page transitions.
- **Easings:**
  - Entrance: `cubic-bezier(0, 0, 0.38, 0.9)`
  - Exit: `cubic-bezier(0.2, 0, 1, 0.9)`
  - Standard / Move: `cubic-bezier(0.4, 0.14, 0.3, 1)`

---

## Iconography Style

- **System:** **IBM Carbon Icons** (16px, 20px, 24px, 32px).
- **Attributes:** Strict 2px stroke, sharp corners, non-rounded terminations, mechanical angular geometry.

---

## Accessibility Notes
- First-class WCAG 2.1 AAA contrast targets for interactive text.
- Focus indicator: 2px solid `$focus` (`#0F62FE` or `#FFFFFF`) with 0px offset or inset.
- Form inputs have persistent labels, helper text, and inline validation icons.

---

## Signature Visual "Tells"

1. **Sharp 0px corner radii:** Buttons, cards, and modal dialogs are completely square-cornered.
2. **IBM Blue #0F62FE:** Unmistakable vivid electric blue used for primary actions and focus indicators.
3. **IBM Plex Sans typography:** Clean, slightly technical grotesque sans-serif with distinct letterforms.
4. **Data table toolbar:** High-density table header with integrated search input, batch action bar, and icon action overflow buttons.
5. **Layered surface stepping:** Subtle shift in container background gray instead of drop shadows.
