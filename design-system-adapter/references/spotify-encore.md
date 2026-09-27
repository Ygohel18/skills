# Spotify Encore Design System

> Source: https://spotify.design/ | https://engineering.atspotify.com/
> Encore is Spotify's internal tiered design system — not open-sourced.
> These specs are derived from official Spotify engineering blog posts, design talks (Figma Config,
> Design Systems Day), and reverse-engineered production values.
> Typeface note: Spotify Mix (2024) replaced Spotify Circular as the primary typeface.

## Core Principles (2–3 sentences)
Encore is a **tiered design system** built to serve 45+ platforms and 2,000+ device types — from car dashboards to smartwatches to desktop. It separates **Encore Foundation** (primitive tokens: colour, spacing, type) from **platform-specific layers** (iOS, Android, Web) that consume the foundation. The design language is bold, dark-first, and music-centric: high-contrast, generous whitespace in content areas, and Spotify Green as the single unapologetic accent against deep black.

---

## Color System

Encore Foundation defines primitive colour tokens consumed by all platforms.

### Core Palette
| Token | Value | Usage |
|---|---|---|
| `$black` | `#000000` | Root background (default dark) |
| `$base` | `#121212` | Main app background |
| `$elevated-base` | `#1E1E1E` | Cards, side panels |
| `$highlight` | `#282828` | Hovered rows, selected items |
| `$press` | `#333333` | Pressed state |
| `$subdued` | `#A7A7A7` | Secondary text, inactive icons |
| `$white` | `#FFFFFF` | Primary text (on dark) |
| `$green` | `#1ED760` | Primary action (desktop green) |
| `$green-press` | `#169C46` | Button press/active |
| `$green-subdued` | `#1DB954` | Alternative green (older brand) |
| `$error` | `#E91429` | Error states |
| `$warning` | `#E8AA12` | Warnings |
| `$info` | `#2D46B9` | Informational |
| `$announcement` | `#0D72EA` | Announcements, new features |

### Light Mode (Encore Web — light variant)
| Token | Value |
|---|---|
| `$background` | `#FFFFFF` |
| `$surface` | `#F7F7F7` |
| `$text-primary` | `#000000` |
| `$text-secondary` | `#6A6A6A` |
| `$accent` | `#1DB954` |

### Dark Mode First
Spotify is **dark-first** — the dark palette is the primary design. Light mode is an adaptation, not the default. When adapting to Spotify Encore, default to dark mode unless explicitly requested otherwise.

---

## Typography Scale

**Font:** Spotify Mix (2024, designed with Dinamo) — proprietary. Blends geometric, grotesque, and humanist styles for motion and static use.
**Fallback:** `Circular, 'Helvetica Neue', Helvetica, Arial, sans-serif` → `system-ui, sans-serif`

| Role | Size (desktop) | Weight | Line Height | Usage |
|---|---|---|---|---|
| Display | 96px | 900 Black | 96px | Hero, album art |
| Title 1 | 56px | 700 Bold | 64px | Page titles |
| Title 2 | 40px | 700 Bold | 48px | Section titles |
| Title 3 | 32px | 700 Bold | 40px | Feature headers |
| Title 4 | 24px | 700 Bold | 32px | Card titles |
| Title 5 | 20px | 700 Bold | 28px | List headers |
| Title 6 | 18px | 700 Bold | 24px | — |
| Body | 16px | 400 Regular | 24px | General text |
| Body Small | 14px | 400 Regular | 20px | Secondary text |
| Fine Print | 12px | 400 Regular | 16px | Labels, metadata |
| Micro | 10px | 400 Regular | 12px | Smallest labels |

**Weight convention:** Headings are always Bold (700) or Black (900). Body is Regular (400). Never use Light or Thin.

---

## Spacing & Layout Grid

- **Base unit:** 4px (Encore uses a 4px grid, tighter than M3's 8dp)
- Spacing scale: `4, 8, 12, 16, 24, 32, 40, 48, 56, 64`
- **Content max-width:** `~1280px` (desktop app); no right rail by default
- **Left nav width:** `~72px` (icon-only collapsed) or `~232px` (expanded)
- **Grid:** Content area flexible; cards in grid at 4-column (desktop, ~232px min card width)
- **Card gap:** `24px` between cards in a grid row

---

## Elevation Model

Spotify uses minimal elevation — the primary depth cue is **background colour delta** between layers.

| Layer | Background | Elevation signal |
|---|---|---|
| Root | `#121212` | None |
| Sidebar / nav | `#000000` | Slightly darker |
| Content cards | `#181818` | Slightly lighter |
| Hovered row | `#282828` | Tinted highlight |
| Modal/dialog | `#282828` | + overlay backdrop `rgba(0,0,0,0.7)` |
| Context menu | `#282828` | + `box-shadow: 0 4px 12px rgba(0,0,0,0.5)` |

There are **no coloured shadows** — elevation is purely through background tone values. Drop shadows are used only for floating menus/tooltips.

---

## Corner Radius Conventions

| Element | Radius |
|---|---|
| Buttons (primary, CTA) | 9999px (pill) |
| Buttons (secondary text) | 9999px (pill) |
| Cards (album, playlist) | 4–8px (square-ish) |
| Input fields | 4px |
| Progress bar | 9999px |
| Notification pill | 9999px |
| Avatar / profile | 50% |
| Toast | 8px |

Spotify signature: **pill-shaped buttons** (always `border-radius: 9999px`) paired with **near-square cards** (4–8px radius). This contrast is intentional.

---

## Motion Principles

- **Easing:** `cubic-bezier(0.3, 0, 0, 1)` — fast out, slow settle. Never linear.
- **Duration standard:** `250ms` for most transitions
- **Fast transitions:** `100ms` — hover, focus ring, icon state
- **Slow transitions:** `400ms` — page load, feature animation
- **Playback controls:** No animation delay — zero-latency feel is critical for music controls
- **Progress bar:** Smooth linear interpolation, never jumpy
- **Card hover:** Subtle `translateY(-4px)` + shadow intensify — `250ms ease`
- No heavy page transitions — navigation is instant; only content area crossfades

---

## Iconography

- **Library:** Spotify uses a **proprietary custom icon set** — not publicly available
- **Web approximation:** Use [Phosphor Icons](https://phosphoricons.com/) (Regular/Bold) as the closest style match
- Icon weight: medium-weight outline style (not thin, not filled by default)
- Selected/active state: filled version of the icon
- Size: 16px (compact), 24px (standard player controls), 32px (feature icons)
- Never mix icon libraries within a single view

---

## 5 Signature "Tells" — Unmistakably Spotify Encore

1. **`#1ED760` Spotify Green** on `#000000` black — this exact high-contrast pairing is the brand's most recognisable signature
2. **Pill-shaped buttons everywhere** — primary, secondary, follow, and play buttons are all fully rounded `border-radius: 9999px`
3. **Bold/Black weight headings at large scale** — 56–96px headlines at 700–900 weight for album/artist hero sections
4. **Dense dark grid of square-ish cards** — album art at 4px radius in tight 4–5 column grids on `#121212` background
5. **Zero elevation shadows in the content layer** — depth is conveyed only through `#000000`/`#121212`/`#181818`/`#282828` tone stepping
