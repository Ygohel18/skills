# Multi-Stack Remediation Recipes

Concrete, framework-specific before-and-after code transformations across modern web stacks demonstrating how to eliminate AI slop patterns and implement production-grade digital craft.

---

## 1. React / Next.js with Tailwind CSS

### Before (AI Vibecoded Slop)
```tsx
// ❌ AI Slop: Purple gradients, glowing text, emoji buttons, arbitrary spacing, hype copy
export function MetricCard() {
  return (
    <div className="bg-gradient-to-br from-purple-900/40 via-black to-indigo-950 p-[19px] rounded-3xl border border-purple-500/30 shadow-[0_0_25px_rgba(168,85,247,0.4)] mt-[13px]">
      <div className="flex justify-between items-center">
        <span className="uppercase tracking-widest text-xs text-purple-300 font-bold">TOTAL REVENUE 🔥</span>
        <button className="bg-purple-600 hover:bg-purple-500 px-3 py-1 rounded-full text-xs text-white shadow-lg animate-pulse">
          New ✨
        </button>
      </div>
      <h2 className="text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500 my-2">
        $124,500.00
      </h2>
      <p className="text-sm text-gray-400">
        Supercharge your growth with effortless AI automation!! 🚀
      </p>
    </div>
  );
}
```

### After (High-Craft Remediated)
```tsx
// ✅ High Craft: Graphite World, quiet chrome, 4px grid, tabular-nums, real baseline, accessible
import { ArrowUpRight } from "lucide-react";

export function MetricCard() {
  return (
    <div className="bg-[#141416] p-5 rounded-xl border border-white/[0.08] shadow-sm">
      <div className="flex justify-between items-center">
        <span className="text-xs text-zinc-400 font-medium">Gross revenue</span>
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 tabular-nums">
          <ArrowUpRight className="w-3 h-3" />
          +14.2%
        </span>
      </div>
      <div className="mt-2 text-2xl font-medium tracking-tight text-zinc-100 tabular-nums">
        $124,500.00
      </div>
      <p className="mt-1 text-xs text-zinc-500">
        Compared to $109,000.00 in the previous 30 days
      </p>
    </div>
  );
}
```

---

## 2. shadcn/ui Component Refinement

### Button Remediation
```tsx
// ❌ Slop Button
<Button className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 shadow-[0_0_20px_rgba(147,51,234,0.5)] rounded-full px-6 py-3 font-bold">
  Unlock Magic ✨
</Button>

// ✅ Craft Button (Concentric radius, crisp state, accessible focus)
<Button className="bg-zinc-100 text-zinc-900 hover:bg-zinc-200 active:scale-[0.98] rounded-md px-4 py-2 text-sm font-medium border border-white/20 transition-[background-color,transform] duration-100">
  Connect repository
</Button>
```

### Card Remediation
```tsx
// ❌ Slop Card
<Card className="bg-black/40 backdrop-blur-2xl border-purple-500/40 shadow-2xl rounded-3xl p-[17px]">
  <CardHeader className="uppercase tracking-wider text-purple-400 text-xs">
    SYSTEM HEALTH ⚡
  </CardHeader>
</Card>

// ✅ Craft Card
<Card className="bg-[#121214] border-white/[0.08] rounded-lg p-5 shadow-sm">
  <CardHeader className="p-0 pb-3">
    <CardTitle className="text-sm font-medium text-zinc-300">Cluster telemetry</CardTitle>
    <CardDescription className="text-xs text-zinc-500">eu-central-1 · 4 active nodes</CardDescription>
  </CardHeader>
</Card>
```

---

## 3. Vue 3 (Composition API & Scoped Tailwind)

### Before (Slop Component)
```vue
<template>
  <nav class="bg-gradient-to-r from-indigo-950 via-purple-900 to-black p-[13px] rounded-full border border-purple-400/50 shadow-purple-500/50 shadow-lg">
    <div class="flex items-center justify-between">
      <span class="text-xl font-black bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-purple-400">
        NEXUS.AI 🚀
      </span>
      <div class="flex gap-4">
        <a href="#" class="text-xs uppercase tracking-widest text-purple-200">DASHBOARD 📈</a>
        <a href="#" class="text-xs uppercase tracking-widest text-purple-200">SETTINGS ⚙️</a>
      </div>
    </div>
  </nav>
</template>
```

### After (Craft Component)
```vue
<template>
  <header class="h-12 border-b border-white/[0.08] bg-[#0d0d0f] px-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <span class="font-sans font-medium text-sm text-zinc-100 tracking-tight">Nexus Telemetry</span>
      <span class="text-zinc-600">/</span>
      <span class="text-xs text-zinc-400">Production</span>
    </div>
    <nav class="flex items-center gap-1">
      <RouterLink 
        to="/dashboard" 
        class="px-2.5 py-1 text-xs font-medium text-zinc-300 rounded hover:bg-white/[0.06] transition-colors"
      >
        Overview
      </RouterLink>
      <RouterLink 
        to="/settings" 
        class="px-2.5 py-1 text-xs font-medium text-zinc-400 hover:text-zinc-200 rounded hover:bg-white/[0.06] transition-colors"
      >
        Settings
      </RouterLink>
    </nav>
  </header>
</template>
```

---

## 4. Svelte 5 (Runes & Scoped CSS)

```svelte
<!-- ✅ High-Craft Svelte 5 Component -->
<script lang="ts">
  let { title = "Active sessions", count = 4821, delta = "+4.2% vs yesterday" } = $props();
</script>

<div class="card">
  <div class="header">
    <span class="title">{title}</span>
    <span class="dot" aria-hidden="true"></span>
  </div>
  <div class="value">{count.toLocaleString()}</div>
  <div class="delta">{delta}</div>
</div>

<style>
  .card {
    background-color: #121215;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .title {
    font-size: 13px;
    color: #9f9fa8;
    font-weight: 500;
  }
  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #10b981;
  }
  .value {
    font-size: 24px;
    font-weight: 500;
    color: #f4f4f6;
    letter-spacing: -0.01em;
    font-variant-numeric: tabular-nums;
  }
  .delta {
    font-size: 11px;
    color: #6a6a75;
  }
</style>
```

