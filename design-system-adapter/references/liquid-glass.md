# Apple Liquid Glass

> Source: WWDC 2025 — "Meet Liquid Glass" session | https://developer.apple.com/design/human-interface-guidelines/
> Introduced: iOS 26, visionOS 26, macOS Tahoe, watchOS 11 (2025)

## Core Principles (2–3 sentences)
Liquid Glass is Apple's most significant interface evolution since iOS 7, treating every UI surface as a **physically-plausible optical material** that refracts, reflects, and adapts to the light conditions and content behind it. It is NOT a simple blur — it is a **multi-pass rendering system** combining chromatic refraction, dynamic tinting, saturation boosting, and adaptive vibrancy to keep text legible against any background. The design goal is a hierarchy where **functional chrome** (bars, controls) appears as a continuous glassy layer floating above the **content layer**, which remains visually clean.

---

## Color System

Liquid Glass is **content-adaptive** — it derives its colour from whatever is behind it.

### Material Variants
| Variant | Use | Character |
|---|---|---|
| **Regular** | Default nav bars, sidebars, tab bars | High contrast, strong separation |
| **Clear** | Subtle overlays, secondary controls | More transparent, softer |
| **Tinted** | System-tinted overlays (Music, Maps) | App-brand colour blended into glass |

### Adaptive Legibility
The material automatically applies:
- **Saturation boost** when background is highly chromatic (prevents muddy blur)
- **Dynamic tinting** to slightly pull the glass colour toward background hues
- **Vibrancy** for all text and SF Symbols placed inside glass (`UIVibrancyEffectStyle`)

### CSS Approximation (web — imperfect)
```css
/* Liquid Glass — Regular, light appearance */
.liquid-glass {
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(200%) brightness(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(200%) brightness(1.05);
  border: 1px solid rgba(255, 255, 255, 0.55);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.7),   /* top specular highlight */
    inset 0 -1px 0 rgba(0,0,0,0.08),        /* bottom shadow edge */
    0 4px 24px rgba(0,0,0,0.12);
}

/* Dark appearance */
.liquid-glass-dark {
  background: rgba(30, 30, 35, 0.55);
  backdrop-filter: blur(24px) saturate(180%) brightness(0.95);
  -webkit-backdrop-filter: blur(24px) saturate(180%) brightness(0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.12),
    0 4px 24px rgba(0,0,0,0.35);
}
```

**Note:** True Liquid Glass uses Metal-level chromatic refraction — CSS can approximate the aesthetic but not the physics.

---

## Typography

Same as Apple HIG (SF Pro / SF Compact), with these Liquid Glass-specific considerations:
- Text placed **inside** glass must use **vibrancy** to remain legible — never plain white or black text on glass
- Labels in glass: use `UIVibrancyEffectStyle.label` (native) or `mix-blend-mode: luminosity` + `filter: drop-shadow` (web approximation)
- **Navigation bar titles** inherit the glass material automatically — always render as a single line
- **Tab bar labels** at 10pt minimum, always Semibold inside glass

---

## Spacing & Layout

- Inherits Apple HIG spacing (8pt grid, 16pt margins)
- **Glass layer floats above content** — content scrolls behind glass, not under opaque bars
- Navigation bar and tab bar extend to screen edges with no background gap
- **Safe area** still applies — content must not enter the glass zone unless intentional (hero images extending behind nav bar)
- `contentInsets` are automatically adjusted to account for glass overlapping content

---

## Elevation / Materiality Model

Liquid Glass replaces traditional elevation numbers with a **two-layer architecture**:

| Layer | Contents | Material |
|---|---|---|
| **Content layer** | Scrollable content, cards, text | Clean, solid or near-solid backgrounds |
| **Chrome layer** | Navigation, tab bar, toolbars, sidebar | Liquid Glass material |
| **Floating controls** | FABs, action buttons over content | Glass with stronger blur + border ring |

**Do NOT** apply Liquid Glass to:
- Content cards (creates visual noise)
- Background/root views
- Every element (reserve for functional chrome only)

Shadow for glass floating controls: `box-shadow: 0 2px 8px rgba(0,0,0,0.18), 0 8px 32px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.6)`

---

## Corner Radius Conventions

Liquid Glass extends Apple HIG radii with additional "continuous" (superellipse) curves:

| Element | Radius | Note |
|---|---|---|
| Tab bar pills | ~24pt (pill) | New pill-shaped tab style in iOS 26 |
| Nav bar glass | Full width, 0 radius at edges | Extends to screen corners |
| Floating action buttons | 20pt | Glass border ring required |
| Sheets over glass | 14–20pt (top corners) | Continuity with glass material |
| Controls inside glass | 10pt | Matches button standard |

iOS 26 introduces **pill-shaped tab bars** — this is one of Liquid Glass's most visible changes.

---

## Motion Principles

Liquid Glass introduces physics-informed **material transitions**:
- **Glass appears:** Fade + slight scale up (0.95→1.0) + blur grows in — `duration: 0.4s, spring`
- **Glass dismisses:** Fade + slight scale down + blur fades — `duration: 0.25s, ease-in`
- **Content scrolls behind glass:** Parallax-like depth as content moves under the glass layer
- **Tab switch:** Crossfade of content + glass pill slides/morphs to new position
- **Interaction response:** Glass brightens/highlights briefly on tap (specular flash effect)

CSS approximation:
```css
@keyframes glassEnter {
  from { opacity: 0; transform: scale(0.96); backdrop-filter: blur(0px); }
  to   { opacity: 1; transform: scale(1);    backdrop-filter: blur(24px); }
}
.glass-enter { animation: glassEnter 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
```

---

## Iconography

Same as Apple HIG — SF Symbols are required. Liquid Glass-specific:
- Icons inside glass must use **Hierarchical rendering mode** with vibrancy
- Icon colour adapts to glass material automatically in native; web must approximate with `color: inherit` + vibrancy mixin
- New **Icon Composer** tool (Xcode 16+) allows custom icons to adapt to Liquid Glass materials

---

## 5 Signature "Tells" — Unmistakably Liquid Glass

1. **Pill-shaped tab bar** — the tab bar becomes a floating pill at the bottom rather than a solid bar edge-to-edge
2. **Chromatic refraction fringe** — a thin rainbow-ish edge glow where glass meets vivid backgrounds (subtle, 1–2px)
3. **Specular highlight edge** — top edge of glass elements has a bright white 1px inset highlight
4. **Content visibly scrolls behind chrome** — there is no solid white background stopping the scroll; you see content through glass
5. **No flat-colour backgrounds on chrome** — every nav bar, tab bar, and sidebar is transparent glass, never solid

---

## Conflict & Compatibility Notes

- **Liquid Glass requires backdrop-filter** — not supported in Firefox without a flag. Provide solid-colour fallback.
- **Never use dark text directly on Liquid Glass** — use vibrancy or ensure high contrast ratio is validated at runtime
- **Do not combine with Material Design elevation** — tonal overlays conflict with glass aesthetics
- **visionOS vs iOS:** On visionOS, glass materials add depth parallax and 3D positioning — CSS cannot replicate this
