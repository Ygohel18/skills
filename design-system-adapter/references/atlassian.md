# Atlassian Design System (ADS)

> Source: https://atlassian.design/ | https://atlassian.design/tokens/ | https://atlassian.design/components
> NPM: `@atlaskit/tokens`, `@atlaskit/css`
> Confidence: **Fully documented spec** (Atlassian publishes complete public tokens, component APIs, accessibility guidance, and theme definitions).

## Core Principles (2–3 sentences)
The Atlassian Design System powers Jira, Confluence, Trello, and Bitbucket with an emphasis on **team productivity, operational clarity, and high-density information management**. It balances clean enterprise structure with approachable personality through distinct color coding, purposeful badges, and crisp typography. The system is multi-brand and re-themeable, powered by an explicit semantic design token architecture.

---

## Color System

ADS uses a tiered token architecture: **Global Base** (hues 50–900) $\rightarrow$ **Semantic Design Tokens** (`color.background.*`, `color.text.*`, `color.border.*`).

### Core Semantic Tokens
| Token Name | Light Mode | Dark Mode | Usage |
|---|---|---|---|
| `color.background.neutral` | `#FFFFFF` | `#1D2125` | Default card/page surface |
| `color.background.neutral.subtle` | `#F7F8F9` | `#22272B` | Page canvas, side navigation bars |
| `color.background.brand.bold` | `#0C66E4` | `#579DFF` | Primary button fill, key highlights |
| `color.background.brand.bold.hovered` | `#0055CC` | `#85B8FF` | Primary button hover |
| `color.background.success.bold` | `#1F845A` | `#22A06B` | Done status, completed sprints |
| `color.background.warning.bold` | `#E2B203` | `#E2B203` | In-progress, alerts |
| `color.background.danger.bold` | `#CA3521` | `#E34935` | Blocker bugs, errors, delete actions |
| `color.text` | `#172B4D` | `#C7D1DB` | Primary text |
| `color.text.subtle` | `#626F86` | `#8C9BAB` | Metadata, timestamps, helper text |
| `color.text.inverse` | `#FFFFFF` | `#1D2125` | Text on bold backgrounds |
| `color.text.brand` | `#0C66E4` | `#579DFF` | Links, active state labels |
| `color.border` | `#DCDFE4` | `#44546F` | Standard container and input borders |
| `color.border.focused` | `#388BFF` | `#85B8FF` | Focus state ring |

### Dark Mode
Atlassian supports full light and dark mode toggling via the `data-color-mode="dark"` HTML attribute. Tokens automatically remap contrast ratios without altering functional hue meanings.

---

## Typography Scale

Font Stack:
- **UI:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Noto Sans', 'Ubuntu', 'Fira Sans', 'Helvetica Neue', sans-serif`
- **Code:** `'SFMono-Medium', 'SF Mono', 'Segoe UI Mono', 'Roboto Mono', 'Ubuntu Mono', Menlo, Consolas, monospace`

| Step | Font Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `font.heading.xxlarge` | 35px | 40px | 600 | Top-level marketing/product headers |
| `font.heading.xlarge` | 29px | 32px | 600 | Page titles (Jira board name, Confluence doc) |
| `font.heading.large` | 24px | 28px | 600 | Modal titles, major section headers |
| `font.heading.medium` | 20px | 24px | 600 | Section headers, card group titles |
| `font.heading.small` | 14px | 16px | 700 | Subsection headers, table headers |
| `font.heading.xsmall` | 11px | 16px | 700 (Uppercase) | Jira issue sidebar attribute labels |
| `font.body.large` | 16px | 24px | 400 | Longform document reading text |
| `font.body` | 14px | 20px | 400 | Standard UI, table cells, form inputs |
| `font.body.small` | 12px | 16px | 400 | Metadata, helper text, breadcrumbs |

---

## Spacing & Layout Grid

- **Base unit:** 8px (with 4px half-step for micro-spacing)
- **Token Scale:**
  - `space.025`: 2px
  - `space.050`: 4px
  - `space.100`: 8px
  - `space.150`: 12px
  - `space.200`: 16px
  - `space.300`: 24px
  - `space.400`: 32px
  - `space.500`: 40px
- **Layout Densities:**
  - **Compact:** 4px padding in table rows, issue lists, and breadcrumbs.
  - **Comfortable:** 8px–12px padding in standard views and settings.

---

## Elevation & Materiality Model

Atlassian uses layered drop shadows to indicate stacking context and surface hierarchy:
- `elevation.surface.sunken`: Inset background for canvas/board wells (`#F7F8F9`).
- `elevation.surface.raised`: Standard floating card: `box-shadow: 0px 1px 1px #091E4240, 0px 0px 1px #091E424F`.
- `elevation.surface.overlay`: Dropdowns, popovers: `box-shadow: 0px 4px 8px -2px #091E4240, 0px 0px 1px #091E424F`.
- `elevation.surface.modal`: Dialogs and lightboxes: `box-shadow: 0px 8px 12px -4px #091E424F, 0px 0px 1px #091E424F`.

---

## Corner Radius Conventions

- `border.radius.050`: 2px (checkboxes, progress bars)
- `border.radius.100`: 3px (standard badges, tags, Lozenge components)
- `border.radius.200`: 4px (buttons, input fields, cards)
- `border.radius.300`: 8px (modals, dropdown menus)
- `border.radius.circle`: 9999px (avatars, circular icon buttons)

---

## Motion & Animation Principles

- **Durations:** Fast: 100ms; Medium: 200ms; Slow: 350ms.
- **Easing:** `cubic-bezier(0.2, 0, 0, 1)` for entrances; `cubic-bezier(0.2, 0, 0.8, 1)` for exits.
- Respects `prefers-reduced-motion` across all Atlaskit components.

---

## Iconography Style

- **System:** Atlassian Icons (Atlassian SVG library).
- **Style:** Clean 16px/24px grid icons with 1.5px consistent stroke or solid geometric fills.
- Distinct Jira issue type icons (Story = Green Bookmark, Task = Blue Checkmark, Bug = Red Circle Dot, Epic = Purple Lightning/Star).

---

## Accessibility Notes
- Strict WCAG 2.1 AA compliance across all components.
- Focus visible state is mandatory: `outline: 2px solid var(--color-border-focused)` with 2px offset (`outline-offset: 2px`).
- Text contrast ratios exceed 4.5:1 for standard body text and 3:1 for large headings across both light and dark themes.

---

## Signature Visual "Tells"

1. **The "Lozenge" status badge:** Capsule/pill badges with bold background fills (`#EAE6FF`, `#E3FCEF`, `#FFEBE6`) and uppercase text (e.g. `IN PROGRESS`, `DONE`, `BLOCKER`).
2. **Issue Key + Avatar pairings:** Prominent monospace issue keys (e.g. `PROJ-1024`) next to 24px circular avatars.
3. **Left navigation sidebar:** Collapsible sidebar with Atlassian product logo, project dropdown, and clean text/icon vertical list.
4. **Subtle card wells:** Kanban/Scrum board columns with sunken neutral backgrounds (`#F7F8F9`) containing white floating cards with 4px border radius.
5. **Charcoal & Atlassian Blue:** Primary brand blue (`#0C66E4`) paired with rich navy-charcoal text (`#172B4D`).
