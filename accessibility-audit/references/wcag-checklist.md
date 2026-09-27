# WCAG 2.2 Level AA Code Audit Checklist

> Companion reference for `accessibility-audit`.
> Mapped directly to the W3C Web Content Accessibility Guidelines (WCAG) 2.2 Level AA specification (October 2023 Recommendation), including all newly introduced 2.2 success criteria.

---

## 1. Principle 1: Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives
- [ ] **1.1.1 Non-text Content (Level A):**
  - Informative images have descriptive `alt="Description of content"`.
  - Decorative images have explicit empty `alt=""` (never omit the `alt` attribute entirely).
  - SVG icons have `<title>` or `aria-label`, or `aria-hidden="true"` if accompanied by text.

### 1.3 Adaptable Structure
- [ ] **1.3.1 Info and Relationships (Level A):**
  - Semantic HTML used for structure: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
  - Proper heading hierarchy: exactly one `<h1>` per page, no skipped levels (`<h1>` $\rightarrow$ `<h2>` $\rightarrow$ `<h3>`).
  - Lists formatted with `<ul>`/`<ol>` and `<li>`, not arbitrary `<div>` rows.
  - Tables use `<th>` headers with `scope="col"` or `scope="row"`.

### 1.4 Distinguishable & Contrast
- [ ] **1.4.1 Use of Color (Level A):**
  - Color is never the sole visual means of conveying information (e.g., error fields must have an icon or text error, not just a red border).
- [ ] **1.4.3 Contrast (Minimum) (Level AA):**
  - Normal text (< 18pt regular or < 14pt bold): **Minimum 4.5:1** contrast ratio against background.
  - Large text ($\ge$ 18pt regular or $\ge$ 14pt bold): **Minimum 3.0:1** contrast ratio.
- [ ] **1.4.11 Non-text Contrast (Level AA):**
  - User interface components (input borders, active tab indicators) and graphical objects have **minimum 3:1** contrast against adjacent colors.
- [ ] **1.4.10 Reflow (Level AA):**
  - Content can reflow without loss of information down to 320 CSS pixels width without horizontal scrolling.

---

## 2. Principle 2: Operable

User interface components and navigation must be operable via keyboard and assistive tech.

### 2.1 Keyboard Accessible
- [ ] **2.1.1 Keyboard (Level A):**
  - Every interactive control (buttons, links, form inputs, dropdowns) can be reached and activated using keyboard alone (`Tab`, `Shift+Tab`, `Enter`, `Space`, Arrows).
- [ ] **2.1.2 No Keyboard Trap (Level A):**
  - Keyboard focus is never trapped inside a widget or modal without a documented key (e.g. `Escape`) to exit.

### 2.4 Navigable & Focus
- [ ] **2.4.3 Focus Order (Level A):**
  - Focus progression through elements follows a logical reading order.
- [ ] **2.4.7 Focus Visible (Level AA):**
  - Every keyboard-focused element has a clearly visible focus indicator ring.
  - 🚫 **Never use `outline: none` or `outline: 0` without an equally visible alternative!**
- [ ] **2.4.11 Focus Not Obscured (Minimum) (Level AA — New in WCAG 2.2):**
  - When an element receives keyboard focus, it must not be entirely hidden behind sticky banners, floating cookie notices, or fixed headers.

### 2.5 Input Modalities
- [ ] **2.5.7 Dragging Movements (Level AA — New in WCAG 2.2):**
  - Any feature that uses dragging (e.g. Kanban card reordering, slider scrubbers) must provide an alternative single-pointer or button interaction (e.g. "Move Up" / "Move Down" buttons).
- [ ] **2.5.8 Target Size (Minimum) (Level AA — New in WCAG 2.2):**
  - Interactive touch and click targets have a minimum bounding size of **$24 \times 24$ CSS pixels** (or sufficient spacing to adjacent targets).

---

## 3. Principle 3: Understandable

Information and operation of user interface must be understandable.

### 3.1 Readable
- [ ] **3.1.1 Language of Page (Level A):**
  - Root `<html>` element declares valid primary language: `<html lang="en">`.

### 3.3 Input Assistance
- [ ] **3.3.1 Error Identification (Level A):**
  - Validation errors are identified in text and programmatically linked to fields via `aria-describedby="field-error-id"`.
- [ ] **3.3.2 Labels or Instructions (Level A):**
  - Every input has a visible, programmatically associated `<label for="input-id">`.
  - Placeholder text is **not** an acceptable substitute for a label.
- [ ] **3.3.7 Redundant Entry (Level A — New in WCAG 2.2):**
  - Information previously entered by the user in the same multi-step session (e.g. shipping address) is auto-populated or available for selection rather than re-typed.
- [ ] **3.3.8 Accessible Authentication (Minimum) (Level AA — New in WCAG 2.2):**
  - Cognitive function tests (memorizing passwords, solving math puzzles, CAPTCHAs) must offer an alternative (password manager copy-paste, WebAuthn passkeys, email magic links).

---

## 4. Principle 4: Robust

Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies.

- [ ] **4.1.2 Name, Role, Value (Level A):**
  - For all custom UI components (tabs, accordions, dialogs, sliders), the accessible name, role, and current state (`aria-expanded`, `aria-checked`, `aria-selected`) must be exposed to accessibility APIs.
- *Note:* Criterion **4.1.1 Parsing** was officially removed/obsolete in WCAG 2.2 because modern HTML5 parsers natively resolve parsing anomalies.
