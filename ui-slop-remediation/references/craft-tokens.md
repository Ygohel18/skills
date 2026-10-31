# Craft Design Tokens & World Palettes

A rigorous design token specification providing mathematical scales, surface elevation ramps, typography hierarchies, and six distinct architectural "World Palettes" designed to replace generic AI purple-gradient slop.

---

## 1. The Six Architectural World Palettes

Every interface should originate from a physical domain. Select the World that matches your product's domain.

### World 1: Graphite & Steel (Developer Tools, Cloud Infrastructure)
- **Character:** Dense, technical, precise, grounded.
- **Canvas / Root:** `#0d0d0f` (deep graphite with a microscopic cold tint).
- **Surface Level 1 (Panels / Sidebars):** `#131316`
- **Surface Level 2 (Cards / Raised):** `#1a1a1f`
- **Surface Level 3 (Inputs / Modals):** `#222228`
- **Hairline Border:** `rgba(255, 255, 255, 0.08)`
- **Text Primary:** `#f2f2f5`
- **Text Secondary:** `#a0a0ab`
- **Text Muted:** `#636370`
- **Accent (Single):** `#3b82f6` (Steel Blue) or `#10b981` (Telemetry Emerald).

```css
:root[data-world="graphite"] {
  --canvas: #0d0d0f;
  --surface-1: #131316;
  --surface-2: #1a1a1f;
  --surface-3: #222228;
  --border: rgba(255, 255, 255, 0.08);
  --text-primary: #f2f2f5;
  --text-secondary: #a0a0ab;
  --text-muted: #636370;
  --accent: #3b82f6;
  --accent-contrast: #ffffff;
}
```

---

### World 2: Swiss & Archival (Publishing, Documentation, Knowledge Bases)
- **Character:** High-contrast, typographic, editorial, timeless.
- **Canvas / Root:** `#fcfcfc` (light) / `#101012` (dark)
- **Surface Level 1:** `#f4f4f5` (light) / `#18181b` (dark)
- **Surface Level 2:** `#ffffff` (light) / `#222225` (dark)
- **Surface Level 3:** `#ebebef` (light) / `#2c2c31` (dark)
- **Hairline Border:** `rgba(0, 0, 0, 0.09)` (light) / `rgba(255, 255, 255, 0.08)` (dark)
- **Text Primary:** `#09090b` (light) / `#f8f8fa` (dark)
- **Text Secondary:** `#52525b` (light) / `#a1a1aa` (dark)
- **Text Muted:** `#71717a` (light) / `#71717a` (dark)
- **Accent (Single):** `#e11d48` (Swiss Vermilion) or `#18181b` (Off-Black Monument).

---

### World 3: Avionics & Cockpit (Observability, Telemetry, Real-Time Data)
- **Character:** Clinical, dark-adapted, high-density, instrumentation.
- **Canvas / Root:** `#08090a` (vacuum black)
- **Surface Level 1:** `#0e1013` (console chassis)
- **Surface Level 2:** `#15181d` (instrument cluster)
- **Surface Level 3:** `#1d2128` (active readout bay)
- **Hairline Border:** `rgba(148, 163, 184, 0.12)`
- **Text Primary:** `#e2e8f0`
- **Text Secondary:** `#94a3b8`
- **Text Muted:** `#64748b`
- **Accent (Single):** `#06b6d4` (Radar Cyan) or `#22c55e` (Telemetry Phosphor).

---

### World 4: Paper & Ink (Notes, Law, Finance, Personal Productivity)
- **Character:** Warm, tactile, literary, contemplative.
- **Canvas / Root:** `#f9f8f5` (cream parchment) / `#181614` (warm soot)
- **Surface Level 1:** `#f2efe9` (light) / `#211e1a` (dark)
- **Surface Level 2:** `#ffffff` (light) / `#2a2722` (dark)
- **Surface Level 3:** `#e8e4db` (light) / `#34302a` (dark)
- **Hairline Border:** `rgba(60, 40, 20, 0.08)` (light) / `rgba(240, 220, 190, 0.07)` (dark)
- **Text Primary:** `#24201c` (light) / `#f0ebe1` (dark)
- **Text Secondary:** `#665f57` (light) / `#a89f94` (dark)
- **Text Muted:** `#968e83` (light) / `#736b60` (dark)
- **Accent (Single):** `#b45309` (Warm Ochre) or `#047857` (Library Forest).

---

### World 5: Warm Industrial (E-Commerce, Hardware, Logistics, Manufacturing)
- **Character:** Utilitarian, physical, structural, durable.
- **Canvas / Root:** `#121213` (cast iron)
- **Surface Level 1:** `#19191b` (milled chassis)
- **Surface Level 2:** `#222225` (compartment tray)
- **Surface Level 3:** `#2d2d32` (latched control)
- **Hairline Border:** `rgba(255, 255, 255, 0.09)`
- **Text Primary:** `#f0f0f2`
- **Text Secondary:** `#9e9ea6`
- **Text Muted:** `#686870`
- **Accent (Single):** `#ea580c` (Industrial Safety Amber).

---

### World 6: Obsidian Terminal (Cybersecurity, Low-Light Operations, Cryptography)
- **Character:** Monochromatic, stealth, tactical, zero-glare.
- **Canvas / Root:** `#050505` (deep obsidian)
- **Surface Level 1:** `#0d0d0d`
- **Surface Level 2:** `#141414`
- **Surface Level 3:** `#1e1e1e`
- **Hairline Border:** `rgba(255, 255, 255, 0.07)`
- **Text Primary:** `#ececec`
- **Text Secondary:** `#8e8e8e`
- **Text Muted:** `#545454`
- **Accent (Single):** `#22c55e` (CRT Green) or `#f5f5f5` (Pure Silver Highlight).

---

## 2. Spacing Rhythm: The Strict 4px Scale

All gaps, paddings, margins, and component heights align to multiples of 4:

| Step | Value (px) | Value (rem) | Typical Role |
|---|---|---|---|
| `space-1` | 4px | 0.25rem | Micro-nudges, icon-to-badge gap, inner dot offset |
| `space-2` | 8px | 0.5rem | Gap between icon and label, chip padding, table cell vertical |
| `space-3` | 12px | 0.75rem | Compact button padding vertical, inner list group gap |
| `space-4` | 16px | 1.0rem | Standard input padding, compact card padding, sidebar item height base |
| `space-5` | 20px | 1.25rem | Standard card internal padding, medium gaps between stacked items |
| `space-6` | 24px | 1.5rem | Wide card padding, gap between major grid columns |
| `space-8` | 32px | 2.0rem | Section padding, modal header offset, dashboard outer margin |
| `space-10` | 40px | 2.5rem | Gap between distinct dashboard panels, hero vertical spacing |
| `space-12` | 48px | 3.0rem | Major section separation on landing pages |
| `space-16` | 64px | 4.0rem | Hero padding top/bottom |

---

## 3. Nested Radius Mathematics

Avoid mismatched curves that destroy optical calmness. Inner radius must always relate to outer radius and padding:

$$r_{\text{inner}} = \max\left(0\text{px},\, r_{\text{outer}} - \text{padding}\right)$$

### Quick Calculation Reference:
- **Card $r = 16\text{px}$, Padding = $12\text{px}$:** Inner button radius must be $16 - 12 = \mathbf{4\text{px}}$.
- **Card $r = 14\text{px}$, Padding = $8\text{px}$:** Inner image radius must be $14 - 8 = \mathbf{6\text{px}}$.
- **Card $r = 12\text{px}$, Padding = $16\text{px}$:** Inner elements have $r = \mathbf{0\text{px}}$ or $\mathbf{4\text{px}}$.

---

## 4. Typography Scale & Hierarchy

Avoid font-weight 800 or 900. Use size and tonal contrast for hierarchy:

| Role | Size | Line Height | Weight | Letter Spacing |
|---|---|---|---|---|
| **Display Title** | 36px–44px | 1.15 | 500 (Medium) | `-0.02em` |
| **Section Heading** | 22px–26px | 1.25 | 500 (Medium) | `-0.01em` |
| **Card Header** | 15px–17px | 1.35 | 500 (Medium) | `0em` |
| **Body Primary** | 14px | 1.5 | 400 (Regular) | `0em` |
| **Body Secondary** | 13px | 1.45 | 400 (Regular) | `0em` |
| **Metadata / Mono** | 11px–12px | 1.3 | 400 (Regular) | `+0.02em` (`tabular-nums`) |

---

## 5. Hairline Border Specification

Replace heavy 1px saturated borders with quiet, opacity-based hairlines:

- **Dark Mode:**
  ```css
  border: 1px solid rgba(255, 255, 255, 0.08);
  /* Tailwind: border-white/[0.08] */
  ```
- **Light Mode:**
  ```css
  border: 1px solid rgba(0, 0, 0, 0.08);
  /* Tailwind: border-black/[0.08] */
  ```
- **Active / Focused Hairline:**
  ```css
  border-color: rgba(255, 255, 255, 0.22);
  /* Tailwind: border-white/[0.22] */
  ```

