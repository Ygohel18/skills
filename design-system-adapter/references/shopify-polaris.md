# Shopify Polaris (Polaris v12)

> Source: https://polaris.shopify.com/ | https://polaris.shopify.com/tokens/color
> NPM: `@shopify/polaris`, `@shopify/polaris-tokens`
> Confidence: **Fully documented spec** (Polaris publishes comprehensive open-source tokens, React component libraries, content guidelines, and accessibility benchmarks).

## Core Principles (2–3 sentences)
Shopify Polaris is purpose-built to help millions of independent merchants successfully manage and grow their businesses. It emphasizes **actionable clarity, merchant empowerment, trustworthy resilience, and effortless workflow efficiency**. The visual language is warm, clean, and restrained, using purposeful color coding to highlight critical inventory, order statuses, and revenue milestones.

---

## Color System

Polaris uses a semantic token architecture based on CSS variables: `--p-color-*`.

### Core Semantic Tokens
| Token Name | Light Value | Dark Value | Usage |
|---|---|---|---|
| `--p-color-bg` | `#F1F2F4` | `#1A1A1A` | Canvas background for merchant admin |
| `--p-color-bg-surface` | `#FFFFFF` | `#202123` | Primary cards, table bodies, banners |
| `--p-color-bg-surface-secondary` | `#F7F7F8` | `#2A2B2D` | Table headers, secondary card panels |
| `--p-color-text` | `#303030` | `#E3E3E3` | Primary body text |
| `--p-color-text-secondary` | `#616161` | `#999999` | Helper descriptions, timestamps |
| `--p-color-border` | `#D4D4D4` | `#404040` | Card borders, table dividers |
| `--p-color-border-subtle` | `#E3E3E3` | `#333333` | Hairline list item separators |
| `--p-color-bg-interactive` | `#303030` | `#E3E3E3` | High-contrast standard button |
| `--p-color-bg-fill-brand` | `#008060` (Classic) / `#000000` (Modern) | Accent fill |
| `--p-color-bg-fill-success` | `#AEE9D1` | `#1A3B32` | Success banner background |
| `--p-color-text-success` | `#005E46` | `#2DC28D` | Order fulfilled status |
| `--p-color-bg-fill-attention` | `#FFEA8A` | `#4F3C00` | Payment pending status badge |
| `--p-color-bg-fill-critical` | `#FED3D1` | `#4A1B1D` | Failed checkout, low stock alert |

---

## Typography Scale

Font Stack:
- **Primary:** `-apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif`

| Token | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `--p-font-size-800` | 32px | 40px | 700 | Store overview headline, revenue total |
| `--p-font-size-600` | 24px | 32px | 700 | Page titles (e.g. "Products", "Orders") |
| `--p-font-size-500` | 20px | 28px | 600 | Card titles, modal headers |
| `--p-font-size-400` | 16px | 24px | 600 | Emphasized body text, section headers |
| `--p-font-size-350` | 14px | 20px | 400 | Standard UI text, table rows, form inputs |
| `--p-font-size-300` | 12px | 16px | 400 | Metadata, inventory SKUs, helper text |

---

## Spacing & Layout Scale

- **Base unit:** 4px (with 8px multiples)
- **Token Scale:**
  - `--p-space-050`: 2px
  - `--p-space-100`: 4px
  - `--p-space-150`: 6px
  - `--p-space-200`: 8px
  - `--p-space-300`: 12px
  - `--p-space-400`: 16px
  - `--p-space-500`: 20px
  - `--p-space-600`: 24px
  - `--p-space-800`: 32px
- **Layout Densities:**
  - **Comfortable:** Default card padding (16px–20px).
  - **Condensed / Compact:** Table rows and fulfillment pick lists (8px padding).

---

## Elevation & Materiality Model

Polaris surfaces are resting cards with subtle drop shadows on a soft gray `#F1F2F4` backdrop:
- `--p-shadow-050`: `0px 1px 0px rgba(0, 0, 0, 0.05)` (Subtle card border reinforcement)
- `--p-shadow-100`: `0px 2px 4px rgba(0, 0, 0, 0.05)` (Standard resting cards)
- `--p-shadow-200`: `0px 4px 8px rgba(0, 0, 0, 0.08)` (Dropdown popovers, date range pickers)
- `--p-shadow-400`: `0px 12px 24px rgba(0, 0, 0, 0.12)` (Modal dialogs)

---

## Corner Radius Conventions

- `--p-border-radius-050`: 2px
- `--p-border-radius-100`: 4px (Small tags, status badges)
- `--p-border-radius-200`: 8px (Buttons, text inputs, search fields)
- `--p-border-radius-300`: 12px (Cards, banners, panels)
- `--p-border-radius-full`: 9999px (Pills, user avatars)

---

## Motion & Animation Principles

- Animation is snappy, predictable, and reassuring:
  - Duration: 100ms–200ms.
  - Easing: `cubic-bezier(0.25, 0.1, 0.25, 1)` (smooth ease).
  - Used for banner expansions, checkout progress, and modal backdrops.

---

## Iconography Style

- **System:** **Shopify Polaris Major Icons** (20px SVG format).
- **Attributes:** Solid and outline glyphs, rounded corner vertices, 20px $\times$ 20px viewbox.

---

## Accessibility Notes
- Rigorous compliance with WCAG 2.1 AA.
- Form inputs always feature associated `<Label>` elements with optional `helpText`.
- High-contrast focus state: `outline: 2px solid #005BD3` with 2px offset.
- Screen-reader announcement polite regions for live stock/price updates.

---

## Signature Visual "Tells"

1. **Polaris Callout Banners:** Rounded notification cards with thick colored background fills (e.g. green for order success, amber for action required, red for urgent error) with bold icon and dismiss 'X'.
2. **Soft gray backdrop canvas:** The entire merchant interface sits on `#F1F2F4` with floating white `#FFFFFF` cards featuring 8px–12px radius.
3. **Pill-shaped order status badges:** Compact status indicators (e.g. "Paid" in green, "Unfulfilled" in yellow/amber, "Archived" in gray).
4. **Index table / Data grid:** Multi-row tables with bulk-selection checkboxes, sticky column headers, and action bars.
5. **Two-column layout:** Standard admin page layout with 2/3 width main card column and 1/3 width right summary sidebar ("Summary", "Sales Channels", "Customer").
