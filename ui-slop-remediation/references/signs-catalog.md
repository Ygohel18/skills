# Encyclopedia of AI Slop Signs & Craft Remedies

An exhaustive catalog of over 50 specific visual, typographic, copywriting, and architectural failure modes common to AI-generated interfaces ("vibecoding"), paired with their production-grade engineering remedies.

---

## 1. Surfaces, Effects & Color Palettes

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Purple/Violet Gradient Washes** | `bg-gradient-to-r from-purple-600 to-indigo-600` on primary buttons, nav bars, or hero sections. | Replace with a solid neutral surface from your product's chosen World ramp (e.g. Graphite, Slate, Stone). Reserve the accent for the single primary call-to-action. |
| **Neon & Colored Drop Glows** | `shadow-[0_0_30px_rgba(139,92,246,0.6)]` or `drop-shadow(0 0 12px #8b5cf6)`. | Remove entirely. Establish depth on dark themes using discrete surface elevations (`#141416` $\to$ `#1c1c20`) and subtle hairline highlights (`border-white/[0.08]`). |
| **Gradient Text Clipping** | `bg-clip-text text-transparent bg-gradient-to-r` on page titles, card numbers, or logo marks. | Use solid high-contrast primary text (`text-foreground` or `#ededef`). Never clip gradients across text baselines. |
| **Radial Color Blobs & Fog** | Giant blurred colorful `div`s with `blur-3xl` or radial gradients positioned behind cards. | Delete all decorative blur blobs. Let content breathe over calm, tinted neutral surfaces. |
| **Glassmorphism Overkill** | `backdrop-blur-xl bg-white/10 border border-white/20` applied indiscriminately to every list item and dropdown. | Replace with opaque or semi-opaque calm surfaces. Keep backdrop blur strictly for transient floating elements like sticky command palettes or modals. |
| **Low-Contrast Gray-on-Gray** | `#71717a` text on `#18181b` card backgrounds failing WCAG AA (contrast $< 3:1$). | Enforce strict 4.5:1 minimum contrast. Use three semantic text tiers: Primary (high contrast), Secondary (4.5:1+), Muted (metadata and timestamps only). |
| **Rainbow Border Accents** | Neon green, cyan, or fuchsia borders around cards to make them "pop". | Hairline borders at 6% to 10% opacity (`border-white/[0.08]` in dark mode, `border-black/[0.08]` in light mode). |
| **Loud Chrome** | Sidebars or top bars tinted heavily with orange, blue, or purple. | Keep chrome neutral. Users stare at navigation for hours; the content alone carries chromatic meaning. |

---

## 2. Iconography & Badges

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Emoji Navigation & Actions** | Emojis used as icons: `🏠 Home`, `⚙️ Settings`, `🚀 Deploy`, `💰 Revenue`, `🔥 Trending`. | Replace with a cohesive line icon set (Lucide, Heroicons, Phosphor) sized uniformly at 16px or 18px with 1.5px stroke width. |
| **Emoji in Data Tables** | Emojis embedded inside badges or table rows: `Status: 🟢`, `Tier: ⭐ VIP`. | Use clean typography with a 6px solid monochromatic or semantic status indicator dot (`rounded-full w-1.5 h-1.5`). |
| **Hype Sparkle Badges** | Badges shouting `New ✨`, `AI Powered 💡`, `PRO 🚀`, `Smart 🔮`. | Eliminate promotional hype. If state must be shown, use quiet text (`v2.4`, `Automated`, `Active`). |
| **Multi-Colored Rainbow Icons** | Every icon in a vertical list has its own distinct bright color (red heart, yellow star, blue folder, green check). | Icons inherit the color of their accompanying text tier (`text-muted-foreground`). Color is reserved for semantic state changes (errors or warnings). |
| **Mismatched Icon Metrics** | Icons in navigation menus have varying bounding boxes, causing labels to stagger unevenly. | Enclose every icon in a fixed bounding container (`w-5 h-5 flex items-center justify-center`) so text begins on an identical vertical baseline. |

---

## 3. Spacing & Rhythm

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Arbitrary Nudges & Offsets** | `mt-[13px]`, `px-[19px]`, `top-[3px]`, `gap-[7px]` scattered across components. | Snap all spacing strictly to the 4px mathematical scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px. |
| **Sibling Padding Disparity** | Three cards in a grid having `p-4`, `p-6`, and `p-5` respectively. | Identical component roles share identical padding tokens across rows. |
| **Inverted Proximity** | Gap between child items inside a card is larger than the gap separating adjacent cards. | Grouping law: $gap_{\text{internal}} < gap_{\text{external}}$. Internal spacing must be noticeably tighter than boundary spacing. |
| **Sprawling Loose Sidebars** | Sidebar navigation links with 16px vertical padding and 20px gaps between items. | Sidebar density: Rows should be 32–36px tall with 2–4px gaps between them. Group headers sit 20–24px above and 6–8px below. |
| **Dead Space Bands** | Centered hero sections with 140px margins above and below a short two-line title. | Compose heroes intentionally. Pair headlines with tangible previews or scenes that run past the lower fold. |

---

## 4. Copywriting & Content Realism

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Buzzword Soup** | Headlines claiming to "Supercharge your workflow seamlessly with next-gen AI magic". | State what the software physically does: "Centralized latency monitoring and anomaly detection for PostgreSQL clusters." |
| **Shouting Exclamation Points** | Buttons or notices reading "Get Started Now!", "Welcome!", "Success!!". | Remove all exclamation points. Professional tools communicate in quiet, declarative statements. |
| **Generic Greeting Clichés** | "Welcome back, Alex! 👋" or "Good morning, user!". | Anchor titles to workspace context: "Production Metrics", "October 2026 Overview", or "Incident Feed". |
| **Vague Metrics Without Baseline** | Cards displaying "+14.8%!!" or "32% faster!". | Explicitly define the reference period: "+14.8% vs prior 30 days" or "140ms faster p99 response". |
| **Toy / Placeholder Numbers** | Metrics showing `$123,456.00`, `99.9%`, `User [Name]`, `Lorem ipsum dolor`. | Use plausible domain data: `$42,810.50`, specific real-world server nodes, realistic customer timestamps. |
| **Trailing Punctuation on Labels** | Buttons with "Submit Form.", labels with "Email Address:.". | Strip periods and unnecessary colons from buttons, navigation links, and input field labels. |

---

## 5. Typography & Numeric Alignment

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Ultra-Heavy Headings** | Display titles set to `font-extrabold` (800) or `font-black` (900). | Limit weights to 400 (regular) and 500 (medium). Hierarchy is achieved via font size and tonal contrast, not brute heaviness. |
| **Screaming Uppercase Labels** | Navigation links and card titles styled as `uppercase tracking-widest` (e.g. `RECENT TRANSACTIONS`). | Convert to standard sentence case: "Recent transactions". Uppercase is reserved strictly for acronyms (`API`, `AWS`) and 2-letter codes. |
| **Negative Tracking on Body Text** | `tracking-tight` applied to 12px or 14px paragraphs and labels. | Never apply negative tracking below 16px. Small text requires normal or slightly open tracking for legibility. |
| **Jittering Numerics** | Changing metrics or timers that cause surrounding text to shake because digits have variable widths. | Apply `tabular-nums` (`font-variant-numeric: tabular-nums`) or use a dedicated monospace font (`font-mono`). |
| **Inconsistent Numeric Formats** | Displaying `$1,420` in one card and `$48,200.419` in an adjacent card. | Standardize currency symbol placement, decimal precision, and grouping commas across the entire dashboard. |

---

## 6. Layout, Geometry & Details

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Pills on Everything** | Every button, card, input, and badge styled with `rounded-full` ($r = 9999\text{px}$). | Differentiate geometric roles: inputs and buttons 6–8px; cards 10–14px; modal surfaces 14–18px. Reserve pills exclusively for compact counters or status tags. |
| **Broken Nested Radii** | A card with `rounded-2xl` ($16\text{px}$) containing an inner button also styled with `rounded-2xl`. | Apply nested geometry: $r_{\text{inner}} = \max\left(4\text{px},\, r_{\text{outer}} - \text{padding}\right)$. Concentric corners produce optical calm. |
| **Cramped Centered Desktop App** | A desktop dashboard squeezed into a narrow 800px column in the center of a wide monitor. | Utilize true application shell proportions: fixed sidebar (240–280px), responsive content area expanding up to 1440–1600px. |
| **Equal-Width Bento Clutter** | Six identical square cards arranged in a grid with identical visual weight. | Establish visual hierarchy: one dominant wide section (e.g. primary metric chart) complemented by secondary compact list modules. |
| **Rainbow Chart Chaos** | Bar charts where every single bar has a different gradient color (purple, pink, yellow, cyan). | Monochrome discipline: neutral bars for historical or secondary items, with a single accent color highlighting the current or selected series. |

---

## 7. Motion & Micro-Interactions

| Slop Anti-Pattern | Tell / Indicator | Craft Remedy |
|---|---|---|
| **Infinite Looping Animations** | `animate-pulse` or `animate-ping` running endlessly on cards or icons that are not live. | Remove looping animations. Static interfaces should feel stable and grounded. |
| **Heavy Card Hover Transforms** | `hover:scale-105 hover:-translate-y-2` lifting entire dashboard cards. | Keep hovers subtle: a 1px border highlight shift or a 3% surface tint increase. Avoid drastic physical displacement. |
| **Overzealous `transition-all`** | `transition-all duration-500` applied to all DOM nodes, causing width/height layout stuttering. | Target specific CSS properties: `transition-colors duration-150`, `transition-transform duration-100 ease-out`. |
| **Disorienting Stagger Intros** | Ten cards flying in from ten different directions on initial page load. | At most, a single subtle 150ms opacity fade and 4px upward drift for the primary content container. |

