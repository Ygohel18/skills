---
name: accessibility-audit
description: >
  Language- and framework-agnostic accessibility protocol for auditing, remediating, and validating
  web UI code against WCAG 2.2 Level AA standards. Triggers whenever an agent is asked to "check accessibility",
  "is this WCAG compliant?", "add ARIA to this component", "conduct an a11y audit", "keyboard navigation is broken",
  or "screen reader doesn't read this". Covers semantic HTML, color contrast (4.5:1), visible focus states,
  ARIA widget patterns, form labelling, reduced motion, and multi-layer manual testing.
metadata:
  author: yash
  version: "1.0"
  scope: "accessibility, a11y, wcag-2.2, aria, screen-readers, keyboard-nav"
allowed-tools: Read Write Bash
---

# Accessibility (A11y) Audit Protocol

A comprehensive operational standard for auditing, repairing, and testing web interfaces against **WCAG 2.2 Level AA** compliance.

> **Sibling Standards:**
> - For visual styling and theme tokens, refer to [`design-system-adapter`](file:///Users/apple/Projects/yash/skills/design-system-adapter/SKILL.md).
> - *Scope Notice:* This skill strictly governs **semantic structure, assistive tech compliance, and keyboard operability**, independent of visual styling.

---

## 1. Semantic Structure & Keyboard Operability

- [ ] **1.1 Native Semantic HTML Over `div`/`span`:**
  - Always prefer native semantic tags (`<button>`, `<nav>`, `<header>`, `<main>`, `<dialog>`, `<label>`).
  - 🚫 Never use `<div onclick="...">` when a native `<button>` can be used.
- [ ] **1.2 Strict Heading Hierarchy:**
  - Every page must have exactly one `<h1>`.
  - Never skip heading levels (e.g. `<h1>` followed directly by `<h4>`).
- [ ] **1.3 Complete Keyboard Operability:**
  - Every interactive element must be reachable and operable using keyboard alone (`Tab`, `Shift+Tab`, `Enter`, `Space`, Arrows).
  - No mouse-only interactions (hover dropdowns must activate on focus or click).

---

## 2. Color, Contrast & Focus Indicators

- [ ] **2.1 Minimum Text Contrast Ratios (WCAG AA):**
  - **Normal text (< 18pt regular or < 14pt bold):** Minimum **4.5:1** contrast ratio against background.
  - **Large text ($\ge$ 18pt regular or $\ge$ 14pt bold):** Minimum **3.0:1** contrast ratio.
  - Test actual rendered colors with dark/light themes, not theoretical brand values.
- [ ] **2.2 Never Rely on Color Alone:**
  - Form errors, badges, and statuses must pair color with text labels, icons, or visual underlines.
- [ ] **2.3 Visible & Unobscured Focus Rings (WCAG 2.2):**
  - 🚫 **Never write `outline: none` or `outline: 0`** without providing a high-contrast replacement.
  - Focus indicators must meet 3:1 non-text contrast against background.
  - Ensure focused elements are not hidden behind sticky headers or floating cookies (Criterion 2.4.11).
- [ ] **2.4 Target Size Minimum (WCAG 2.2):**
  - All clickable/tappable elements must have at least **$24 \times 24$ CSS pixels** bounding box (Criterion 2.5.8).

---

## 3. ARIA Rules & State Synchronization

- [ ] **3.1 First Rule of ARIA:** If a native HTML element provides the behavior, do not use ARIA.
- [ ] **3.2 Eliminate Redundant ARIA:**
  - ❌ `<button role="button">` (Redundant).
  - ❌ `<div role="button">` without `tabindex="0"` and keyboard handlers (Inaccessible).
- [ ] **3.3 Synchronize ARIA State Dynamically:**
  - Every state attribute must reflect real DOM state:
    - Collapsible accordions: `aria-expanded="true"` when open, `"false"` when closed.
    - Checkboxes: `aria-checked="true"`.
    - Selected tab: `aria-selected="true"`.
  - Stale ARIA state actively deceives screen reader users.

---

## 4. Form Accessibility

- [ ] **4.1 Programmatic Labels:**
  - Every form input must have a `<label for="field-id">` matching the input's `id`.
  - Placeholder text is not a substitute for a persistent label.
- [ ] **4.2 Error Association:**
  - Link error messages to inputs via `aria-describedby="error-id"` so assistive tech reads the error upon focus.
  - Mark invalid fields with `aria-invalid="true"`.
- [ ] **4.3 Mark Required Fields Programmatically:**
  - Use native `required` and `aria-required="true"`.

---

## 5. Media & Dynamic Content

- [ ] **5.1 Meaningful vs. Decorative Images:**
  - Informative images have descriptive `alt="Graph showing 20% revenue growth"`.
  - Decorative icons or background illustrations must have explicit empty `alt=""`.
- [ ] **5.2 Dynamic Live Regions (`aria-live`):**
  - Notify screen reader users of live asynchronous updates (e.g. search results count, "Saving draft...") using `<div aria-live="polite">`.
- [ ] **5.3 Respect Reduced Motion:**
  - Wrap animations in CSS `@media (prefers-reduced-motion: reduce)` to disable high-motion zooms or parallax for vestibular-sensitive users.

---

## 6. Multi-Layer Testing Protocol

Automated scanning tools catch at most 30–40% of accessibility defects. Every audit must combine three layers:

```text
Layer 1: Automated Scanners (axe-core, Lighthouse, Pa11y)
  │      Quickly identifies contrast failures, missing alt text, duplicate IDs.
  ▼
Layer 2: Keyboard-Only Navigation
  │      Tab through entire page. Can you reach every button? Can you close modals with Escape?
  ▼
Layer 3: Screen Reader Smoke Test (VoiceOver on macOS / NVDA on Windows)
         Listen to how forms, live regions, and custom widgets are announced.
```

---

## Detailed References

- [`references/wcag-checklist.md`](file:///Users/apple/Projects/yash/skills/accessibility-audit/references/wcag-checklist.md): Complete WCAG 2.2 Level AA success criteria mapped to concrete code-level checks (including new 2.2 rules on target size, focus obscured, and redundant entry).
- [`references/aria-patterns.md`](file:///Users/apple/Projects/yash/skills/accessibility-audit/references/aria-patterns.md): Official WAI-ARIA Authoring Practices Guide (APG) templates for **Modal Dialogs**, **Tabs**, **Accordions**, **Comboboxes**, and **Live Regions**.
