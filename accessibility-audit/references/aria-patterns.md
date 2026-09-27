# WAI-ARIA Authoring Practices (APG) Patterns

> Companion reference for `accessibility-audit`.
> Accessible markup patterns, keyboard interactions, and state management for common custom interactive UI widgets based on the W3C WAI-ARIA Authoring Practices Guide (APG).

---

## 1. Accessible Modal Dialog

### Required Semantics & Attributes:
- Container: `role="dialog"` or native `<dialog>`, `aria-modal="true"`, `aria-labelledby="dialog-title-id"`.
- Keyboard trap: `Tab` and `Shift+Tab` must cycle exclusively within the modal while open.
- Close trigger: `Escape` key must close the dialog.
- Focus restoration: When closed, focus must return to the element that triggered opening.

```html
<div
  role="dialog"
  id="confirm-modal"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
  tabindex="-1"
>
  <h2 id="modal-title">Delete Project</h2>
  <p id="modal-desc">Are you sure you want to permanently delete this project?</p>

  <button type="button" id="cancel-btn">Cancel</button>
  <button type="button" id="confirm-btn">Delete</button>
</div>
```

---

## 2. Accessible Tabs Widget

### Required Semantics & Attributes:
- Tab list container: `role="tablist"` with `aria-label="Section tabs"`.
- Each tab: `<button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" tabindex="0">`.
- Inactive tabs: `aria-selected="false"` and `tabindex="-1"`.
- Each panel: `<div role="tabpanel" id="panel-1" aria-labelledby="tab-1" tabindex="0">`.
- Keyboard navigation: Left/Right Arrow keys move focus between tabs.

```html
<div class="tabs-container">
  <div role="tablist" aria-label="Account Settings">
    <button
      role="tab"
      id="tab-profile"
      aria-selected="true"
      aria-controls="panel-profile"
      tabindex="0"
    >
      Profile
    </button>
    <button
      role="tab"
      id="tab-security"
      aria-selected="false"
      aria-controls="panel-security"
      tabindex="-1"
    >
      Security
    </button>
  </div>

  <div
    role="tabpanel"
    id="panel-profile"
    aria-labelledby="tab-profile"
    tabindex="0"
  >
    <!-- Profile form content -->
  </div>

  <div
    role="tabpanel"
    id="panel-security"
    aria-labelledby="tab-security"
    tabindex="0"
    hidden
  >
    <!-- Security settings content -->
  </div>
</div>
```

---

## 3. Accessible Accordion

### Required Semantics & Attributes:
- Heading wraps an interactive `<button>`.
- Button: `aria-expanded="false"`, `aria-controls="sect-1"`.
- Panel: `<div id="sect-1" role="region" aria-labelledby="accordion-header-1">`.
- Panel is hidden via CSS `hidden` or `display: none` when collapsed.

```html
<div class="accordion-item">
  <h3>
    <button
      type="button"
      id="acc-header-1"
      aria-expanded="false"
      aria-controls="acc-panel-1"
    >
      What is your cancellation policy?
    </button>
  </h3>
  <div
    id="acc-panel-1"
    role="region"
    aria-labelledby="acc-header-1"
    hidden
  >
    <p>You can cancel your subscription at any time from your billing dashboard.</p>
  </div>
</div>
```

---

## 4. Accessible Combobox / Autocomplete Search

### Required Semantics & Attributes:
- Input element: `role="combobox"`, `aria-expanded="false"`, `aria-autocomplete="list"`, `aria-controls="suggestions-list"`, `aria-activedescendant="opt-selected"`.
- Dropdown list: `role="listbox"`, `id="suggestions-list"`.
- Options: `role="option"`, `id="opt-1"`, `aria-selected="true"`.
- Keyboard: Up/Down arrow keys highlight options; `Enter` selects; `Escape` closes.

```html
<label for="country-search">Search Country:</label>
<div class="combobox-wrapper">
  <input
    type="text"
    id="country-search"
    role="combobox"
    aria-expanded="true"
    aria-autocomplete="list"
    aria-controls="country-listbox"
    aria-activedescendant="opt-2"
  />
  <ul id="country-listbox" role="listbox" aria-label="Countries">
    <li role="option" id="opt-1" aria-selected="false">Australia</li>
    <li role="option" id="opt-2" aria-selected="true" class="highlighted">Austria</li>
    <li role="option" id="opt-3" aria-selected="false">Azerbaijan</li>
  </ul>
</div>
```

---

## 5. Live Region for Dynamic Content (`aria-live`)

Notify screen reader users when content updates asynchronously without shifting focus:

```html
<!-- Status updates (e.g. "Saving draft...", "Saved") -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  Item added to shopping cart.
</div>

<!-- Critical alerts (e.g. connection lost) -->
<div role="alert" aria-live="assertive" class="error-banner">
  Your payment session has expired.
</div>
```
- `aria-live="polite"`: Waits for user to pause before speaking. Use for status messages.
- `aria-live="assertive"`: Interrupts user immediately. Reserve strictly for time-critical emergencies.
