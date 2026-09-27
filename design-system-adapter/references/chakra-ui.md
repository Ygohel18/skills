# Chakra UI Design System (v3 / Zag / Ark UI)

> Source: https://chakra-ui.com/ | https://v3.chakra-ui.com/docs/theming/tokens
> GitHub: https://github.com/chakra-ui/chakra-ui
> Confidence: **Fully documented spec** (Chakra UI provides complete programmatic design token definitions, semantic tokens, component recipes, and WAI-ARIA compliant headless primitives).

## Core Principles (2–3 sentences)
Chakra UI is a developer-centric, modular, and accessible component library designed around **frictionless composability, design-token ergonomics, and seamless light/dark theming**. It treats tokens as first-class CSS custom properties and component recipes, empowering teams to build accessible SaaS interfaces with minimal boilerplate. It is explicitly multi-brand and built from the ground up to be customized and re-themed.

---

## Color System

Chakra v3 structures colors into hue scales (50–950) mapped directly to **semantic tokens** that auto-resolve between light and dark modes via CSS variables.

### Key Semantic Color Tokens
| Semantic Token | Light Mode | Dark Mode | Usage |
|---|---|---|---|
| `bg` | `#FFFFFF` | `#111111` | Root canvas background |
| `bg.subtle` | `#F4F4F5` (gray.100) | `#18181B` (gray.900) | Secondary backgrounds, sidebars |
| `bg.muted` | `#E4E4E7` (gray.200) | `#27272A` (gray.800) | Hover backgrounds, input fills |
| `fg` | `#09090B` (gray.950) | `#FAFAFA` (gray.50) | Primary text |
| `fg.muted` | `#71717A` (gray.500) | `#A1A1AA` (gray.400) | Secondary text, captions |
| `border` | `#E4E4E7` (gray.200) | `#27272A` (gray.800) | Container and control borders |
| `colorPalette.solid` | `teal.600` (`#0D9488`) | `teal.500` (`#14B8A6`) | Primary action background fill (default palette) |
| `colorPalette.subtle` | `teal.50` (`#F0FDFA`) | `teal.950` (`#042F2E`) | Selected chip background, soft badges |
| `colorPalette.fg` | `teal.700` (`#0F766E`) | `teal.300` (`#5EEAD4`) | Accent text, active tab indicators |

### Dynamic Color Palette Concept
Chakra components accept a `colorPalette` prop (e.g. `colorPalette="teal"`, `colorPalette="blue"`, `colorPalette="purple"`). The component automatically resolves `solid`, `subtle`, `contrast`, and `fg` tokens within that hue family.

---

## Typography Scale

Font Stack:
- **Heading / Body:** `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`
- **Mono:** `SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace`

| Step | Font Size | Line Height | Letter Spacing |
|---|---|---|---|
| `2xs` | 10px (0.625rem) | 14px | +0.05em |
| `xs` | 12px (0.75rem) | 16px | 0 |
| `sm` | 14px (0.875rem) | 20px | 0 |
| `md` | 16px (1rem) | 24px | 0 |
| `lg` | 18px (1.125rem) | 28px | -0.01em |
| `xl` | 20px (1.25rem) | 28px | -0.01em |
| `2xl` | 24px (1.5rem) | 32px | -0.02em |
| `3xl` | 30px (1.875rem) | 36px | -0.02em |
| `4xl` | 36px (2.25rem) | 40px | -0.03em |

---

## Spacing & Layout Grid

- **Base unit:** 4px
- **Spacing tokens:**
  - `1`: 4px, `2`: 8px, `3`: 12px, `4`: 16px, `5`: 20px, `6`: 24px, `8`: 32px, `10`: 40px, `12`: 48px, `16`: 64px
- **Container sizes:** `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px)

---

## Elevation & Materiality Model

Chakra UI uses smooth, subtle ambient shadows with balanced key lights:
- `shadow.xs`: `0 1px 2px 0 rgba(0, 0, 0, 0.05)` (Buttons, form fields)
- `shadow.sm`: `0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)` (Cards)
- `shadow.md`: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)` (Dropdowns)
- `shadow.lg`: `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)` (Drawers)
- `shadow.xl`: `0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)` (Modal dialogs)

---

## Corner Radius Conventions

- `radii.xs`: 2px
- `radii.sm`: 4px (Checkboxes, small tags)
- `radii.md`: 6px (Standard buttons, inputs)
- `radii.lg`: 8px (Cards, alerts)
- `radii.xl`: 12px (Modals)
- `radii.full`: 9999px (Pills, badges, circular avatars)

---

## Motion & Animation Principles

- Uses CSS keyframes and cubic beziers:
  - Fast: 150ms `ease-out`
  - Normal: 200ms `cubic-bezier(0.4, 0, 0.2, 1)`
  - Slow: 300ms `ease-in-out`
- Dialogs scale in slightly (`scale(0.95) -> scale(1)`) with simultaneous opacity fade.

---

## Iconography Style

- **Recommended System:** Lucide Icons or React Icons (`@chakra-ui/react` pairs seamlessly with Lucide).
- **Style:** 18px–20px outline SVG icons with 2px consistent stroke.

---

## Accessibility Notes
- Built directly upon **Ark UI / Zag.js** state machines following WAI-ARIA Authoring Practices.
- Focus visible indicator: `outline: 2px solid var(--chakra-colors-colorPalette-focusRing, #0D9488)` with 2px offset.
- Full keyboard trap and focus restoration in Dialog and Popover components.

---

## Signature Visual "Tells"

1. **Subtle colored tag badges:** Badges using soft background tint (`bg: colorPalette.subtle`, `color: colorPalette.fg`) with 4px or pill radius.
2. **Teal default brand identity:** Iconic Chakra default accent (`teal.500` / `teal.600`) for buttons, active switches, and checkboxes.
3. **Smooth 6px–8px rounded cards:** Crisp white or dark gray cards with 1px border and soft `shadow.sm`.
4. **Toast notification stack:** Floating pill/box alerts anchored to top-right or bottom-right with colored left accent strip or solid status icon.
5. **Fluid form controls:** Input fields with soft background fill or 1px border that animate to a distinct colored focus ring on active typing.
