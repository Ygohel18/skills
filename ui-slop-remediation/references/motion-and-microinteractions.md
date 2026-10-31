# Motion & Micro-Interactions

Guidelines for engineering purposeful, high-craft digital motion while eliminating disorienting AI animations, looping pulses, and layout-thrashing transitions.

---

## 1. Principles of Craft Motion

1. **Motion Must Explain State:** Motion should clarify spatial relationships (e.g., a modal emerging from its trigger button, a drawer sliding from the edge of the viewport, or a row deleting and adjacent rows collapsing smoothly).
2. **Never Animate Layout Properties:** Never transition `width`, `height`, `top`, `left`, or `margin`. These trigger full browser layout recalculations (reflow) and cause severe frame drops. Animate exclusively `transform` (scale, translate) and `opacity`.
3. **No Decorative Looping:** Remove infinite pulsing (`animate-pulse`), glowing breathing effects, and constant hovering cards. Stable interfaces instill confidence.
4. **Targeted Properties over `transition-all`:** Explicitly declare transitions (`transition-colors duration-150`, `transition-transform duration-100`) to prevent accidental animation of unexpected properties.

---

## 2. Standard Timing & Easing Curves

```css
:root {
  /* Durations */
  --duration-instant: 75ms;   /* Active button press, checkbox check */
  --duration-micro: 120ms;     /* Hover state, icon color shift */
  --duration-standard: 200ms;  /* Dropdown open, tooltip reveal */
  --duration-macro: 300ms;     /* Modal dialog enter, page slide */

  /* Easing Curves */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);    /* Smooth deceleration */
  --ease-snappy: cubic-bezier(0.16, 1, 0.3, 1);  /* Fast responsive spring */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);        /* Element departures */
}
```

---

## 3. Micro-Interaction Recipes

### Recipe 1: Tactile Button Press (Tailwind CSS)
A button that feels grounded and responsive to user input.

```html
<button class="px-4 py-2 text-sm font-medium rounded-md bg-zinc-900 text-zinc-100 border border-white/10 hover:bg-zinc-800 active:scale-[0.98] transition-[background-color,transform] duration-100 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500">
  Deploy cluster
</button>
```

### Recipe 2: Dropdown Menu Elevation (Smooth Fade & Drift)
Avoids jarring pop-ins while keeping latency under 150ms.

```html
<div class="origin-top-right transform opacity-0 scale-95 data-[state=open]:opacity-100 data-[state=open]:scale-100 transition-[opacity,transform] duration-150 ease-out">
  <!-- Menu Content -->
</div>
```

---

## 4. Accessibility: Reduced Motion Compliance

Always implement accessible fallbacks for users with vestibular disorders via `@media (prefers-reduced-motion: reduce)`:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

In Tailwind projects, pair interactive animations with the `motion-safe:` and `motion-reduce:` modifiers:
```html
<div class="motion-safe:transition-transform motion-safe:duration-150 motion-reduce:transform-none">
  <!-- Content -->
</div>
```

