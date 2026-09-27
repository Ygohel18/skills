# Screenshot to Prompt — UI Analysis → Structured Prompt Generator

## What This Mode Does

Instead of (or before) generating code, this mode **reads a screenshot and produces a detailed natural-language prompt** that describes the UI so thoroughly that any AI model, developer, or design tool can recreate it from the text alone.

This is useful when:
- The user wants to hand off the design to a different tool or AI
- The user wants a reusable prompt they can use to generate multiple variations
- The user wants to understand the design before committing to a stack
- The user wants to share the design spec as text (e.g. in a Notion doc, Figma description, or README)

---

## Trigger Phrases

Activate this mode when the user says:
- "describe this UI as a prompt"
- "screenshot to prompt"
- "convert this to a prompt"
- "generate a prompt from this design"
- "write a prompt that describes this"
- "what prompt would recreate this?"
- "give me the AI prompt for this"
- "extract the prompt from this screenshot"
- "make a reusable prompt from this"

---

## Output Format

Produce a structured prompt with these sections, in order:

```
## UI Rebuild Prompt: [Page/Component Name]

### Overview
[1–2 sentence summary of what this UI is and its purpose]

### Layout
[Describe the overall structure in plain spatial language]

### Color Palette
[List each color with its role and approximate value]

### Typography
[Describe fonts, sizes, weights per element]

### Components
[List every visible component with its variant/state]

### Spacing & Sizing
[Estimate key measurements]

### Visual Effects
[Shadows, radius, gradients, animations]

### Content
[Sample text, labels, placeholder values visible in screenshot]

### Interactions
[Hover states, dropdown behavior, any visible states]

### Responsive Behavior
[Infer desktop vs mobile treatment from the screenshot]
```

---

## Detailed Instructions

### Section 1: Overview
Write 1–2 sentences that describe:
- What type of page/component this is (landing page hero, admin dashboard, login card, pricing table, etc.)
- The general mood/aesthetic (dark, minimal, vibrant, corporate, etc.)

**Example:**
```
A modern SaaS landing page hero section with a dark background, centered headline,
and a prominent primary CTA button. The aesthetic is clean and minimal with subtle
gradient accents.
```

---

### Section 2: Layout
Describe the spatial arrangement using plain language:
- Is it full-width or contained in a max-width container?
- Top-aligned, centered, or bottom-anchored?
- How many columns? Grid or flex?
- What sticky/fixed elements are present?
- Describe each major zone (header / hero / features / footer)

**Example:**
```
Full-viewport dark hero section. Content is centered horizontally and vertically
with a max-width container of ~800px. Above it sits a fixed 64px tall navigation
bar with logo on the left and 4 nav links + 1 CTA button on the right.
Below the hero are 3 equal-width feature cards in a horizontal flex row with 24px
gaps, full-width on mobile (stacked).
```

---

### Section 3: Color Palette
List every distinct color with:
- Its role (background, primary text, muted text, primary CTA, accent, border, etc.)
- Approximate hex/HSL value (estimate from visual)

**Example:**
```
- Background:        #0F172A  (very dark navy)
- Surface / Card:   #1E293B  (slightly lighter dark blue)
- Primary CTA:      #6366F1  (indigo)
- Primary text:     #F8FAFC  (near white)
- Muted text:       #94A3B8  (slate gray)
- Border:           #334155  (dark border)
- Accent highlight: #818CF8  (lighter indigo, used for gradient)
```

---

### Section 4: Typography
For each text element visible:
- Font family (estimate: sans-serif, serif, monospace; identify if it looks like Inter, Geist, etc.)
- Size (px or Tailwind equivalent)
- Weight (light/regular/medium/semibold/bold)
- Color
- Letter spacing (tight / normal / wide)

**Example:**
```
- Main headline:    ~56px, bold (700), near-white, tight tracking (-0.02em)
- Subheadline:      ~20px, regular (400), muted-foreground (#94A3B8), normal tracking
- Nav links:        ~14px, medium (500), near-white, normal
- CTA button label: ~16px, semibold (600), white on primary background
- Feature card title: ~18px, semibold (600), white
- Feature card body:  ~14px, regular (400), muted
- Badge label:      ~12px, medium (500), indigo, uppercase, wide tracking
```

---

### Section 5: Components
List every distinct UI component visible. For each:
- Component type
- Variant (primary / outline / ghost / etc.)
- Size
- Any visible state (hover, active, disabled, selected)
- Notable styling details

**Example:**
```
- Navbar: horizontal, sticky, transparent background with subtle border-bottom.
  Logo: text mark "BrandName" in bold white. Nav links: 4 plain text links in muted color.
  CTA: small primary button with rounded-full pill shape.

- Hero Badge: pill-shaped label "New Feature", indigo bg with 20% opacity, indigo text.
  Centered above headline.

- Primary CTA Button: large, indigo (#6366F1), rounded-lg (8px radius), white text,
  px-8 py-3. Has a subtle box-shadow. Hover: slightly lighter + upward translate.

- Secondary Button: outline variant, white border, white text, same size as primary,
  placed to the right with 12px gap.

- Feature Cards: 3 cards in a row. White-on-dark. Border: 1px #334155.
  Border-radius: 12px. Padding: 24px. Icon at top (24px, indigo). Title then body text.
  Subtle hover: border highlights to indigo.
```

---

### Section 6: Spacing & Sizing
Estimate key measurements:

**Example:**
```
- Navbar height:           64px
- Hero section padding:    96px top / 80px bottom
- Container max-width:     ~1200px (with 32px horizontal padding)
- CTA button height:       ~48px, padding: 12px 32px
- Feature card padding:    24px all sides
- Gap between cards:       24px
- Gap: headline to sub:    16px
- Gap: sub to CTAs:        40px
- Icon size in cards:      32px
- Section divider spacing: 80px between major sections
```

---

### Section 7: Visual Effects
Describe any non-color visual treatments:

**Example:**
```
- Background: solid dark (#0F172A) with a subtle radial gradient glow in the center
  (indigo at ~10% opacity, roughly 600px diameter)
- Cards: 1px solid border, no box-shadow
- Primary button: box-shadow 0 4px 24px rgba(99,102,241,0.4)
- Hover on cards: border-color transitions to indigo over 200ms
- Hover on button: transform translateY(-2px) + shadow intensifies
- Badge: backdrop-blur-sm with semi-transparent bg
- Border radius: buttons 8px, cards 12px, badge 9999px (pill)
- No visible animations in static screenshot; hover states inferred from design style
```

---

### Section 8: Content
Extract all visible text/content:

**Example:**
```
- Nav links:       "Product", "Pricing", "Blog", "Contact"
- Nav CTA:         "Get started"
- Badge:           "New · v2.0 is here"
- H1:              "Build faster with less code"
- Subheading:      "The modern toolkit for shipping beautiful products. Zero config, maximum control."
- Primary CTA:     "Start for free"
- Secondary CTA:   "See how it works"
- Card 1 title:    "Lightning fast"
- Card 1 body:     "Optimized for performance from day one. Scores 100 on Lighthouse."
- Card 2 title:    "Fully customizable"
- Card 2 body:     "Every component is built to match your brand, not the other way around."
- Card 3 title:    "Production ready"
- Card 3 body:     "Battle-tested in real apps. Ships with TypeScript, a11y, and dark mode."
```

---

### Section 9: Interactions
Note any interactive states visible or implied:

**Example:**
```
- Primary button: hover → slight upward lift + deeper shadow
- Nav CTA: hover → filled with slightly lighter indigo
- Feature cards: hover → border lights up to indigo
- Nav links: hover → text brightens to white
- No modal, dropdown, or form interactions visible in this screenshot
```

---

### Section 10: Responsive Behavior
Infer responsive adaptations from visible clues:

**Example:**
```
- Desktop (shown): 3-column card row, centered hero with wide container
- Mobile (inferred):
  → Cards stack to 1-column
  → Headline reduces to ~32px
  → Nav collapses to hamburger menu
  → CTA buttons go full-width
  → Section padding reduces to 48px top/bottom
```

---

## Complete Output Example

When a user uploads a screenshot, output this format:

````markdown
## UI Rebuild Prompt: SaaS Landing Page Hero

### Overview
A premium dark-mode SaaS landing page hero section. Clean minimal aesthetic
with an indigo primary accent, centered layout, and strong typographic hierarchy.

### Layout
Full-viewport dark section. Sticky 64px navbar (logo left, nav+CTA right).
Hero content centered at ~800px max-width. Below: 3-column feature card row
at 1200px container. Mobile: everything stacks to single column.

### Color Palette
- Background:    #0F172A
- Surface/Card:  #1E293B
- Primary:       #6366F1 (indigo)
- Text:          #F8FAFC
- Muted:         #94A3B8
- Border:        #334155
- Accent:        #818CF8

### Typography
- H1: 56px bold, white, tight tracking
- Subheading: 20px regular, muted, normal tracking
- Nav links: 14px medium, near-white
- CTA label: 16px semibold, white
- Card title: 18px semibold, white
- Card body: 14px regular, muted
- Badge: 12px medium, indigo, uppercase wide-tracking

### Components
[...full component descriptions...]

### Spacing
- Navbar: 64px | Hero padding: 96px/80px | Cards: 24px padding, 24px gap

### Visual Effects
- Radial gradient glow center (indigo 10%)
- Button shadow: 0 4px 24px rgba(99,102,241,0.4)
- Hover: cards border → indigo, button translates -2px
- Radius: buttons 8px, cards 12px, badge pill

### Content
"Build faster with less code" / "Start for free" / "See how it works"
[...all extracted text...]

### Interactions
Button hover: lift + deeper shadow. Card hover: border highlights. Nav: links brighten.

### Responsive
Mobile: cards stack, headline shrinks to 32px, nav collapses, CTAs go full-width.
````

---

## When to Combine with Code Generation

After producing the UI prompt, ask the user:

```
Here's your UI prompt. Would you like me to:

A) Use this prompt to generate the full code now (choose a stack above)
B) Save this prompt as PROMPT.md in the project
C) Both — save the prompt and generate the code
D) Just the prompt for now — I'll handle the code later
```

Default to **C** if the user said "build this" or "clone this" alongside the screenshot.
Default to **B** if they said "give me a prompt" or "save this as a prompt".
