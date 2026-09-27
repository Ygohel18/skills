---
name: design-system-adapter
description: >
  Adapt any UI output — HTML/CSS, React components, mockups, or design specs — to match a
  specific named design system on request. Handles: "make this look like Material Design",
  "Material You", "Material 3", "M3", "apply Apple HIG", "iOS style", "macOS style", "Liquid Glass",
  "visionOS", "Fluent 2", "Microsoft style", "WinUI", "Meta design", "Facebook UI", "Astryx",
  "Twitter design", "X style", "Chirp", "Spotify Encore", "Spotify style", "GitHub Primer",
  "Atlassian Design System", "Jira style", "IBM Carbon", "Salesforce Lightning", "SLDS",
  "Chakra UI", "Uber Base Web", "Adobe Spectrum", "Shopify Polaris". Triggers when user names
  any of the 15 supported systems or their aliases, or asks to style UI like Apple, Google, Microsoft,
  Meta, Twitter/X, Spotify, GitHub, Atlassian, IBM, Salesforce, Chakra, Uber, Adobe, or Shopify.
metadata:
  author: yash
  version: "2.0"
  systems: "material-3, apple-hig, liquid-glass, fluent-2, meta, twitter-x, spotify-encore, github-primer, atlassian, ibm-carbon, salesforce-lightning, chakra-ui, uber-base, adobe-spectrum, shopify-polaris"
allowed-tools: Read Write Bash
---

# Design System Adapter

You are a design systems expert and UI adapter. When requested to adapt UI to a named design system:
1. **Identify** which system is requested from the 15 supported systems.
2. **Classify** the request archetype: **Brand Identity** vs **Multi-Brand / Tokenizable Enterprise**.
3. **Load** the matching reference file from `references/`.
4. **Apply** that system's tokens, typography, spacing, shape, elevation, and signature traits.
5. **Flag conflicts** between the user's request and the system's strict architectural guidelines.

---

## Brand Identity vs Multi-Brand Tokenizable Foundations

Before adapting code, identify which category the design system represents:

| Archetype | Design Systems | Strategic Intent | Best Used When... |
|---|---|---|---|
| **Brand Identity Systems** | **Apple HIG**, **Liquid Glass**, **Meta / Astryx**, **Twitter / X**, **Spotify Encore** | Highly opinionated visual languages designed to express a singular company product identity. | The user specifically wants their app to feel like Spotify, iOS, Vision Pro, or Twitter/X. Less suitable for generic white-label software without looking like a clone. |
| **Multi-Brand / Tokenizable Enterprise Systems** | **IBM Carbon**, **Salesforce Lightning (SLDS)**, **Atlassian (ADS)**, **Adobe Spectrum**, **Shopify Polaris**, **Chakra UI**, **Uber Base Web**, **GitHub Primer**, **Material 3**, **Fluent 2** | Built explicitly with deep semantic token layers, density options, accessibility guarantees (WCAG AAA), and theme overrides. | **Recommended starting points** when the user requests "an accessible, easily re-themeable base", enterprise SaaS, dashboards, data-heavy portals, or commerce admin tools. |

---

## Step 1 — Identify the Requested System

Match user triggers and platform cues to the appropriate reference file:

| If user mentions / requests... | Archetype | Reference File | Starter Tokens |
|---|---|---|---|
| Material Design, Material 3, M3, Material You, Android native | Enterprise / Adaptive | `references/material-design.md` | `assets/tokens/material-3.json` |
| Apple HIG, Human Interface Guidelines, iOS, iPadOS, macOS, SF Symbols | Brand Identity | `references/apple-hig.md` | `assets/tokens/apple-hig.json` |
| Liquid Glass, Apple visionOS, spatial computing, iOS 26 blur | Brand Identity | `references/liquid-glass.md` | `assets/tokens/liquid-glass.json` |
| Fluent 2, Microsoft style, WinUI, Copilot UI, Office design | Enterprise / Desktop | `references/fluent.md` | `assets/tokens/fluent-2.json` |
| Meta design, Facebook UI, Astryx, Instagram web | Brand Identity | `references/meta-design.md` | `assets/tokens/meta-design.json` |
| Twitter, X design system, Chirp, Tweet timeline style, Lights Out | Brand Identity | `references/twitter-x.md` | `assets/tokens/twitter-x.json` |
| Spotify, Encore design system, Spotify dark player style | Brand Identity | `references/spotify-encore.md` | `assets/tokens/spotify-encore.json` |
| GitHub, Primer, Primer CSS/React, Octicons, GitHub repo UI | Enterprise / Dev | `references/github-primer.md` | `assets/tokens/github-primer.json` |
| Atlassian, ADS, Atlaskit, Jira board, Confluence doc, Trello UI | Enterprise / B2B | `references/atlassian.md` | `assets/tokens/atlassian.json` |
| IBM Carbon, Carbon v11, IBM Design Language, Cloud console UI | Enterprise / B2B | `references/ibm-carbon.md` | `assets/tokens/ibm-carbon.json` |
| Salesforce Lightning, SLDS, CRM dashboard, Trailhead style | Enterprise / B2B | `references/salesforce-lightning.md` | `assets/tokens/salesforce-lightning.json` |
| Chakra UI, Chakra v3, Ark UI, Zag.js theme, modular React UI | Tokenizable Library | `references/chakra-ui.md` | `assets/tokens/chakra-ui.json` |
| Uber Base, Base Web, Styletron, Uber Freight/Eats operational UI | Enterprise / Ops | `references/uber-base.md` | `assets/tokens/uber-base.json` |
| Adobe Spectrum, Spectrum 2, Creative Cloud UI, Photoshop palette | Enterprise / Creative | `references/adobe-spectrum.md` | `assets/tokens/adobe-spectrum.json` |
| Shopify Polaris, Polaris v12, Shopify admin, Merchant commerce UI | Commerce / Admin | `references/shopify-polaris.md` | `assets/tokens/shopify-polaris.json` |

### When No Design System is Named:
- **Infer from context if domain is clear:**
  - *Enterprise B2B / Cloud console* $\rightarrow$ Suggest **IBM Carbon** or **Atlassian Design System**
  - *CRM / Sales pipeline / Multi-step business workflow* $\rightarrow$ Suggest **Salesforce Lightning (SLDS)**
  - *Commerce / Merchant admin / Order fulfillment* $\rightarrow$ Suggest **Shopify Polaris**
  - *Creative tool / Multi-panel workspace / Media editor* $\rightarrow$ Suggest **Adobe Spectrum**
  - *Developer tools / Code viewer / Git workflow* $\rightarrow$ Suggest **GitHub Primer**
  - *Consumer social feed / Real-time microblog* $\rightarrow$ Suggest **Twitter / X** or **Meta Astryx**
  - *Media streaming / Dark entertainment UI* $\rightarrow$ Suggest **Spotify Encore**
  - *Clean, accessible, easily re-brandable SaaS starter* $\rightarrow$ Suggest **Chakra UI** or **Uber Base**
- **Otherwise prompt:**
  *"Which design system should I adapt this to? I support 15 systems across Brand Identity (Apple HIG, Liquid Glass, Meta, Twitter/X, Spotify) and Enterprise Foundations (Carbon, Polaris, Spectrum, Lightning, Atlassian, Primer, Fluent 2, Material 3, Chakra UI, Uber Base)."*

---

## Step 2 — Cross-System Translation Matrix

Use this matrix to translate core visual tokens consistently across all 15 systems:

| System | Base Unit | Primary Accent | Background / Canvas | Corner Radius | Elevation Model | Font Stack | Icon Set | Confidence |
|---|---|---|---|---|---|---|---|---|
| **Material 3** | 8dp | `primary` (tonal) | `surface` / `surfaceContainer` | 12dp / 16dp | Tonal color tint overlays | Roboto / Variable | Material Symbols | Fully documented |
| **Apple HIG** | 8pt | System Blue (`#007AFF`) | `systemBackground` / Materials | 10pt (continuous) | Translucent vibrancy & blurs | SF Pro / SF Compact | SF Symbols | Fully documented |
| **Liquid Glass** | 8pt | Vibrant Cyan / Specular | Frosted Glass (`rgba(255,255,255,0.25)`) | 16–28pt | 40–60px blur + specular specular borders | SF Pro Display | SF Symbols | Inferred / WWDC |
| **Fluent 2** | 8px | `colorBrandBackground` (`#0F6CBD`) | `colorNeutralBackground1` (`#FFF`/`#292929`) | 4px–6px | Dual key + ambient shadows | Segoe UI Variable | Fluent System Icons | Fully documented |
| **Meta / Astryx** | 8px | `$blueBase` (`#0866FF`) | `$white` / `$surfaceSecondary` (`#F0F2F5`) | 8px | 1px border + soft card drops | System UI stack | Custom / Phosphor | Inferred from product |
| **Twitter / X** | 4px | Accent Blue (`#1D9BF0`) | `#FFFFFF` / `#15202B` / `#000000` | 9999px (pills) / 16px | Flat + 1px hairline border + header blur | Chirp / System UI | Chirp SVG Icons | Inferred from product |
| **Spotify Encore**| 4px | `$essentialPositive` (`#1ED760`) | `$backgroundBase` (`#121212`) | 4px / 500px | Minimal flat + 1px borders | Spotify Mix / Circular | Encore Icons | Inferred from product |
| **GitHub Primer** | 4px | `accent.fg` (`#0969DA`) | `canvas.default` (`#FFF`/`#0D1117`) | 6px | 1px hairline borders + subtle inset | System UI / Monospace | GitHub Octicons | Fully documented |
| **Atlassian (ADS)**| 8px | `brand.bold` (`#0C66E4`) | `neutral` (`#FFF`) / `subtle` (`#F7F8F9`) | 3px (badges) / 4px | Sunken wells + layered drop shadows | System UI / Mono | Atlassian SVG Icons | Fully documented |
| **IBM Carbon** | 8px (2x) | `$interactive` (`#0F62FE`)| `$background` (`#FFF`/`#161616`) | **0px (sharp)** | Layer shifting (`$layer-01` $\rightarrow$ `03`) | IBM Plex Sans / Mono | IBM Carbon Icons | Fully documented |
| **Salesforce SLDS**| 4px | `$color-brand` (`#0176D3`) | `$color-background` (`#F3F3F3`) | 4px | Restrained 2px–4px shadow | Salesforce Sans | SLDS Icons & Badges | Fully documented |
| **Chakra UI** | 4px | `teal.500` / `colorPalette` | `bg` (`#FFF`) / `bg.subtle` (`#18181B`) | 6px–8px | Balanced ambient key shadows | Inter / System UI | Lucide Icons | Fully documented |
| **Uber Base** | 4px | `contentPrimary` (`#000`/`#FFF`) | `backgroundPrimary` (`#FFF`/`#000`) | 4px | Graphic ultra-flat + 1px hairline | Uber Move / Move Text | Base Web Icons | Fully documented |
| **Adobe Spectrum**| 8px | Accent 900 (`#0265DC`) | Default (`#FFF`) / Darkest (`#1D1D1D`) | 4px | Tool-grade flat + 4-tier dark theme | Adobe Clean / Source Sans | Spectrum Icons | Fully documented |
| **Shopify Polaris**| 4px | Interactive (`#303030`/`#008060`)| `--p-color-bg` (`#F1F2F4`) | 8px–12px | Floating cards on gray canvas | System UI stack | Polaris Major Icons | Fully documented |

---

## Step 3 — Adaptation Execution Rules

When restyling target HTML, CSS, or React components:
1. **Load Reference File:** Always read `references/<system>.md` for exact values before writing code.
2. **Preserve Component Semantics:** Do not break existing accessible DOM structures, `<button>`, `<input>`, or ARIA landmarks established by the `frontend-design` skill.
3. **Replace Hardcoded Values with Tokens:**
   - Colors $\rightarrow$ CSS custom properties / semantic design token classes.
   - Corner radii $\rightarrow$ system radius steps (e.g. sharp `0px` in Carbon, `4px` in Fluent/SLDS, `8px` in Polaris).
   - Typography $\rightarrow$ exact font-family imports, sizes, weights, and line-heights.
   - Elevation $\rightarrow$ the system's authentic mechanism (blurs in Liquid Glass, surface layers in Carbon, tonal tints in M3).
4. **Preserve Density Rhythm:** If adapting to Carbon, SLDS, or Polaris, respect their compact vs comfortable density scale.

---

## Step 4 — Flag Architectural Conflicts

Call out any design inconsistencies before delivering the adapted code:

| Conflict Scenario | Offending Request | System Violation | Resolution / Feedback to User |
|---|---|---|---|
| **Shadows in Carbon / M3** | "Add large floating blur shadows to these cards" | IBM Carbon and Material 3 reject heavy skeuomorphic drop shadows. | *"IBM Carbon uses flat surface layer stepping ($layer-01 to 02) and M3 uses tonal color overlay. I have applied authentic layer tokens. If you require floating drop shadows, I can provide a deviation."* |
| **Rounded corners in Carbon** | "Make all buttons pill-shaped" | IBM Carbon uses strict 0px square corners for interactive controls. | *"Carbon buttons are strictly 0px rectangular. Pill radii violate Carbon's 2x Grid architectural principles. Applied standard 0px with an optional spec-override snippet."* |
| **Clutter in Apple HIG** | "Fill the toolbar with 8 dense buttons" | Violates Apple HIG clarity & direct manipulation. | *"Apple HIG emphasizes clarity, negative space, and progressive disclosure. Grouped auxiliary actions into an overflow menu."* |
| **Light mode in Spotify** | "Style this in Spotify's light mode" | Spotify Encore is fundamentally dark-first (`#121212`). | *"Spotify Encore operates in dark mode by default. Adapting to an inverted light palette may feel uncharacteristic; applied Spotify dark-surface tokens."* |
| **Low contrast accents** | "Make text light gray on white cards" | Violates WCAG 2.1 AA/AAA (mandatory in Carbon, Spectrum, SLDS, Polaris, Primer). | *"Color fails 4.5:1 WCAG AA contrast ratio. Adjusted to token-compliant text-secondary for accessibility compliance."* |

---

## Output Delivery Format

Every adapted UI delivery must follow this 4-part structure:
1. **Summary & Archetype:** Design system applied + archetype note (Brand Identity vs Re-themeable Enterprise).
2. **Conflict Flags:** Explicit list of any guideline deviations or accessibility adjustments.
3. **Token Mapping Table:** Direct comparison of Old Value $\rightarrow$ New Semantic Token.
4. **Complete Adapted Code:** Production-ready HTML/CSS, React component, or Tailwind config.

---

## Directory Reference Index

- `references/material-design.md` — Google Material Design 3
- `references/apple-hig.md` — Apple Human Interface Guidelines
- `references/liquid-glass.md` — Apple Liquid Glass (visionOS / iOS 26 blur)
- `references/fluent.md` — Microsoft Fluent 2
- `references/meta-design.md` — Meta / Astryx
- `references/twitter-x.md` — Twitter / X Design System
- `references/spotify-encore.md` — Spotify Encore Design System
- `references/github-primer.md` — GitHub Primer Design System
- `references/atlassian.md` — Atlassian Design System (ADS)
- `references/ibm-carbon.md` — IBM Carbon Design System (Carbon v11)
- `references/salesforce-lightning.md` — Salesforce Lightning Design System (SLDS)
- `references/chakra-ui.md` — Chakra UI (v3 / Ark UI)
- `references/uber-base.md` — Uber Base Web Design System
- `references/adobe-spectrum.md` — Adobe Spectrum (Spectrum 2)
- `references/shopify-polaris.md` — Shopify Polaris (Polaris v12)

### Starter Token Files (`assets/tokens/`)
- `assets/tokens/material-3.json`
- `assets/tokens/apple-hig.json`
- `assets/tokens/liquid-glass.json`
- `assets/tokens/fluent-2.json`
- `assets/tokens/meta-design.json`
- `assets/tokens/twitter-x.json`
- `assets/tokens/spotify-encore.json`
- `assets/tokens/github-primer.json`
- `assets/tokens/atlassian.json`
- `assets/tokens/ibm-carbon.json`
- `assets/tokens/salesforce-lightning.json`
- `assets/tokens/chakra-ui.json`
- `assets/tokens/uber-base.json`
- `assets/tokens/adobe-spectrum.json`
- `assets/tokens/shopify-polaris.json`
