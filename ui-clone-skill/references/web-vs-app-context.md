# Web vs App Context — What Applies Where

This reference defines which rules, features, and standards are **web-only**, **app-only**, or **universal**. Always consult this before generating code so you never mix web-specific patterns into an app build or vice versa.

---

## Quick Decision Chart

| Feature / Concern                    | Web (HTML/React/Astro/Laravel) | Mobile App (Android/Flutter/RN) |
|--------------------------------------|:------------------------------:|:--------------------------------:|
| Back-to-top button                   | ✅ Required on all pages       | ❌ Not applicable                |
| Responsive breakpoints (sm/md/lg/xl) | ✅ Required                    | ❌ Use adaptive layouts instead  |
| SEO meta tags / Open Graph           | ✅ Required                    | ❌ Not applicable                |
| Sitemap / robots.txt                 | ✅ Required                    | ❌ Not applicable                |
| Cookie / GDPR consent banner         | ✅ Required                    | ❌ Not applicable                |
| Keyboard navigation (Tab/Enter/Esc)  | ✅ Required                    | ❌ Use touch targets instead     |
| ARIA roles & screen reader support   | ✅ Required                    | ✅ Required (platform-native)    |
| Touch targets (min 48×48dp)          | ❌ Not primary                 | ✅ Required                      |
| Bottom navigation bar                | ❌ Avoid                       | ✅ Primary nav pattern           |
| Hamburger / slide-out drawer nav     | ✅ Mobile web only             | ✅ Common pattern                |
| Sticky header / navbar               | ✅ Standard                    | ✅ AppBar / TopBar               |
| Footer with link groups              | ✅ Required                    | ❌ Not applicable                |
| Legal pages (Privacy / Terms)        | ✅ Required as web pages       | ✅ In-app screen or webview      |
| Blog listing + detail pages          | ✅ Required                    | Optional (webview or screens)   |
| Back-navigation button               | ❌ Browser handles this        | ✅ Required (hardware + in-app)  |
| Push notifications                   | Optional (web push)            | ✅ Standard                      |
| Offline / PWA support                | Optional                       | ✅ Expected                      |
| Splash screen / onboarding flow      | ❌ Not applicable              | ✅ Required                      |
| Deep links / universal links         | ❌ URL routing                 | ✅ Required                      |
| Safe area / notch handling           | ❌ Not applicable              | ✅ Required                      |
| Font loading via Google Fonts        | ✅ Standard                    | ❌ Bundle fonts locally          |
| CSS variables / Tailwind tokens      | ✅ Standard                    | ❌ Use platform theme system     |
| Platform theme (Material / Cupertino)| ❌ Not applicable              | ✅ Required                      |

---

## Web-Only Requirements

These features MUST be included in every web project (HTML, React, Next.js, Astro, Laravel):

### 1. Back-to-Top Button
Every web page with scrollable content must include a "Back to top" button.

**Behaviour:**
- Appears only after the user scrolls down ≥ 400px
- Fixed position: bottom-right corner (`bottom-6 right-6` or equivalent)
- Smooth-scrolls to `window.scrollTop = 0`
- Accessible: `aria-label="Back to top"`, focusable, keyboard activatable
- Has a subtle fade-in / fade-out animation

**HTML + Tailwind implementation:**
```html
<!-- In every page template / layout -->
<button id="back-to-top"
        aria-label="Back to top"
        class="fixed bottom-6 right-6 z-50 p-3 rounded-full bg-primary text-white shadow-lg
               opacity-0 pointer-events-none transition-all duration-300
               hover:bg-primary/90 hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-primary/50">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
       fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M18 15l-6-6-6 6"/>
  </svg>
</button>
<script>
(function () {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  const toggle = () => {
    const show = window.scrollY > 400;
    btn.classList.toggle('opacity-0', !show);
    btn.classList.toggle('pointer-events-none', !show);
  };
  window.addEventListener('scroll', toggle, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  btn.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); } });
})();
</script>
```

**React (Next.js / Vite / Astro) implementation:**
```tsx
// components/layout/BackToTop.tsx
'use client';
import { useEffect, useState } from 'react';
import { ChevronUp } from 'lucide-react';

export function BackToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 400);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' });

  return (
    <button
      onClick={scrollToTop}
      aria-label="Back to top"
      className={[
        'fixed bottom-6 right-6 z-50 p-3 rounded-full bg-primary text-white shadow-lg',
        'hover:bg-primary/90 hover:-translate-y-1 active:scale-95',
        'focus:outline-none focus:ring-2 focus:ring-primary/50',
        'transition-all duration-300',
        visible ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none',
      ].join(' ')}
    >
      <ChevronUp className="h-5 w-5" />
    </button>
  );
}
```

Add `<BackToTop />` to every layout component:
```tsx
// app/layout.tsx or layouts/app.tsx
<body>
  {children}
  <BackToTop />
</body>
```

**Laravel Blade implementation:**
```blade
{{-- resources/views/partials/back-to-top.blade.php --}}
<button id="back-to-top" aria-label="Back to top"
        class="fixed bottom-6 right-6 z-50 p-3 rounded-full bg-primary text-white shadow-lg
               opacity-0 pointer-events-none transition-all duration-300
               hover:opacity-90 hover:-translate-y-1">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
    <path d="M18 15l-6-6-6 6"/>
  </svg>
</button>
@push('scripts')
<script>
  const btn = document.getElementById('back-to-top');
  window.addEventListener('scroll', () => {
    btn.classList.toggle('opacity-0', window.scrollY <= 400);
    btn.classList.toggle('pointer-events-none', window.scrollY <= 400);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
</script>
@endpush
```
Include in `layouts/app.blade.php`: `@include('partials.back-to-top')`

---

### 2. SEO Meta Tags (every web page)
```html
<meta name="description" content="Page-specific description (150–160 chars)" />
<meta property="og:title" content="Page Title — Site Name" />
<meta property="og:description" content="Page-specific description" />
<meta property="og:image" content="/og-image.png" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="canonical" href="https://example.com/page-url" />
```

### 3. Cookie / Consent Banner (web only)
Simple dismissible banner at the bottom of every web layout. Does not require a library — a simple `localStorage`-checked banner is sufficient for clones.

### 4. Accessible Keyboard Navigation
- All interactive elements reachable via `Tab`
- Dropdown menus close on `Escape`
- Modals trap focus inside
- Skip-to-main-content link at top of page

---

## App-Only Requirements

These apply ONLY to Android (Compose/XML), Flutter, and React Native:

### 1. Splash Screen / Onboarding
- Show brand logo + colors on app launch
- Optional: 2-3 slide onboarding for first-time users

### 2. Safe Area Handling
- Always account for notch, status bar, and home bar
- Android: `WindowInsets` / `fitsSystemWindows`
- Flutter: `SafeArea` widget
- React Native: `SafeAreaView` or `useSafeAreaInsets()`

### 3. Touch Targets
- All tappable elements must be at least **48 × 48dp**
- Never make links or buttons too small to tap accurately on mobile

### 4. Back Navigation
- Android: Handle hardware back button + in-app back arrows
- Flutter: `WillPopScope` or `PopScope` for custom back behaviour
- React Native: `BackHandler` for Android hardware back

### 5. Local Font Bundling
- Do NOT use Google Fonts CDN in apps
- Bundle font `.ttf` files in `res/font/` (Android), `assets/` (Flutter), or link via `react-native-vector-icons` (RN)

### 6. Platform-Native Theme
- Android: `MaterialTheme` (Compose) or `Theme.MaterialComponents` (XML)
- Flutter: `ThemeData` with `useMaterial3: true`
- React Native: `StyleSheet` or NativeWind with platform-aware tokens

### 7. Bottom Navigation Bar
- Primary navigation goes in a `BottomNavigationBar` (Flutter), `NavigationBar` (Compose), `BottomNavigationView` (XML), or `createBottomTabNavigator` (RN)
- Maximum 5 tabs, label + icon for each

### 8. No Footer
- App screens do NOT have a footer. Navigation is via the bottom nav bar.

---

## Universal Requirements (Both Web & App)

These apply to every project regardless of platform:

- **Auth flows**: Login, Register, Forgot Password, OTP verification
- **Legal content**: Privacy Policy, Terms of Service, Refund Policy (web page or in-app screen)
- **Error states**: Empty state UI, error messages, retry actions
- **Loading states**: Skeletons, spinners, progress indicators
- **Brand consistency**: Colors, fonts, and spacing from DESIGN.md
- **Accessibility**: Sufficient color contrast, readable font sizes, clear focus indicators
- **Responsive layouts**: Web = CSS breakpoints, App = adaptive/flexible layouts
- **Form validation**: Client-side validation with clear, human-readable error messages (never "Invalid input" — always explain what to fix)
