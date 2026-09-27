# Twitter / X Design System (Chirp)

> Source: Product reverse-engineering (web app `abs.twimg.com`), Chirp font announcements, and public web client CSS inspection.
> Confidence: **Inferred from product** (Twitter/X does not publish an official standalone open-source design token repository; values verified against live Web / PWA stylesheet bundles).

## Core Principles (2–3 sentences)
The Twitter/X design system is built around high-density, real-time social information consumption with instant responsiveness. Following the rebrand to X, it embraces high-contrast monochrome foundations (pure black `#000000`, stark white, neutral grays) punctuated by customizable user accent colors. The interface relies on crisp hairline dividers, circular media frames, and a content-forward timeline rhythm.

---

## Color System

X uses a 3-tier theme model: **Default Light**, **Dim (Navy/Dark Blue)**, and **Lights Out (Pure OLED Black)**.

### Semantic Color Roles
| Token / Variable | Light Mode | Dim Mode | Lights Out (Black) | Usage |
|---|---|---|---|---|
| `--color-background` | `#FFFFFF` | `#15202B` | `#000000` | Canvas background |
| `--color-surface` | `#F7F9F9` | `#1E2732` | `#16181C` | Cards, search bars, side containers |
| `--color-border` | `#EFF3F4` | `#38444D` | `#2F3336` | Hairline timeline dividers, card outlines |
| `--color-text-primary` | `#0F1419` | `#F7F9F9` | `#E7E9EA` | Tweet body text, usernames, titles |
| `--color-text-secondary` | `#536471` | `#8B98A5` | `#71767B` | Handles (`@username`), timestamps, metadata |
| `--color-accent-default` | `#1D9BF0` | `#1D9BF0` | `#1D9BF0` | Default signature X/Twitter blue |
| `--color-accent-options` | `#FFD400` (Yellow), `#F91880` (Pink), `#7856FF` (Purple), `#FF7A00` (Orange), `#00BA7C` (Green) | Customizable user accents |
| `--color-danger` | `#F4212E` | `#F4212E` | `#F4212E` | Unfollow, delete tweet, block actions |

---

## Typography Scale

Font Stack:
- **Primary:** `Chirp, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`
- Note: Chirp is X's custom variable sans-serif font (commissioned from Bētype). On fallback systems, system sans-serif is used with tight character spacing.

| Role | Font Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| Header / Hero | 20px | 24px | 700 / 800 | Timeline headers, profile display names |
| Tweet Body (Standard) | 15px | 20px | 400 | Primary tweet/post text |
| Tweet Body (Large/Focus) | 17px–20px | 24px | 400 | Expanded single-tweet permalink view |
| Metadata / Secondary | 13px | 16px | 400 | Handles, timestamps, view counts, reply labels |
| Micro / Pills | 11px–12px | 14px | 700 | Notification counts, badge text |

---

## Spacing & Layout Grid

- **Base unit:** 4px (with 12px and 16px timeline padding)
- **Timeline Column Width:** Exactly `600px` max-width for the primary feed column (`--column-feed-width: 600px`).
- **Sidebar Widths:**
  - Navigation Sidebar (Left): `88px` (compact) to `275px` (expanded desktop).
  - Search / Trends Sidebar (Right): `290px` to `350px`.
- **Feed Row Padding:** `12px 16px` vertical/horizontal padding per post item.

---

## Elevation & Materiality Model

- Twitter/X is almost entirely **flat with hairline borders** (`1px solid var(--color-border)`).
- **Sticky Headers:** Glassmorphic blur overlay with `backdrop-filter: blur(12px)` and 85% opacity (`rgba(255, 255, 255, 0.85)` in light, `rgba(0, 0, 0, 0.65)` in Lights Out).
- **Dropdowns & Modals:** Minimal high-contrast shadows:
  - Floating menus: `box-shadow: rgba(101, 119, 134, 0.2) 0px 0px 15px, rgba(101, 119, 134, 0.15) 0px 0px 3px 1px`.
  - Lights out menus: `box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 15px, rgba(255, 255, 255, 0.15) 0px 0px 3px 1px`.

---

## Corner Radius Conventions

- **Avatars:** Strictly circular (`border-radius: 9999px` / `50%`) for standard users; square with rounded corners (`border-radius: 4px`) for verified organizations.
- **Pills & Action Buttons:** Fully rounded pill shapes (`border-radius: 9999px`) for "Post", "Follow", and tab filters.
- **Media Containers (Images, Video cards):** `border-radius: 16px` with overflow hidden.
- **Search inputs & Quoted Tweets:** `border-radius: 16px` to `9999px`.

---

## Motion & Animation Principles

- **Micro-interactions:** Snappy 150ms–200ms ease transitions on hover and heart like animations.
- **Like Animation:** Multi-stage SVG heart bounce with particle burst (`scale(0) -> scale(1.3) -> scale(1.0)` over 400ms).
- **Page transitions:** Instantaneous feed updates via virtualized DOM, zero artificial motion delay.

---

## Iconography Style

- **Monoline Outline Icons:** 20px–22.5px SVG icons with uniform 1.75px–2px stroke weight.
- **Active State:** Fills the icon glyph (e.g. hollow bookmark becomes solid filled bookmark; heart outline becomes filled red `#F91880`).
- **Standard Action Bar:** 4-action row below posts (Reply, Repost, Like, Bookmark/Share) with expansive touch targets and subtle circular hover rings (`rgba(29, 155, 240, 0.1)`).

---

## Accessibility Notes
- Contrast in Lights Out mode is extreme (pure `#000000` vs `#E7E9EA`), achieving WCAG AAA.
- In Dim mode (`#15202B`), secondary text (`#8B98A5`) satisfies 4.5:1 WCAG AA contrast against dark blue backgrounds.
- Focus outlines use high-contrast cyan/accent rings: `outline: 2px solid var(--color-accent)`.

---

## Signature Visual "Tells"

1. **Pill-shaped action buttons:** "Follow" (high contrast inverted black/white) and "Post" buttons are always fully rounded capsules (`border-radius: 9999px`).
2. **Hairline timeline dividers:** Clean `1px solid` horizontal dividers separating feed items with no drop shadows between cards.
3. **Circular user avatars:** 40px (timeline) or 134px (profile header) circular profile pictures.
4. **Frosted sticky top bar:** Blurry sticky header displaying "For You" / "Following" tabs with a centered sliding blue bottom indicator.
5. **Interactive hover halos:** Soft circular background highlights (`40px x 40px`, `border-radius: 50%`) appearing behind action icons on hover.
