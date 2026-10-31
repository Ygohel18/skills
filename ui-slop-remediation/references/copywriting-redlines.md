# Copywriting Redlines & Content Realism

A systematic manual for stripping marketing fluff, AI hype jargon, and placeholder clichés from digital interfaces, replacing them with authentic, context-anchored copy and realistic domain data.

---

## 1. The De-Hyping Dictionary

AI models default to superlative, breathy marketing language. Replace generic AI verbs with direct, technical descriptions of what the software does.

| AI Slop Buzzword | Why It Fails | Craft Replacement |
|---|---|---|
| **"Supercharge your workflow"** | Meaningless cliché that explains nothing about capabilities. | "Automate incident triage and ticket assignment across Slack and PagerDuty." |
| **"Seamlessly integrate"** | Overused filler adverb. Everything promises to be seamless. | "Connect with PostgreSQL, Redis, and Snowflake via read replicas." |
| **"Unlock the power of AI"** | Vague, theatrical, and patronizing. | "Generate automated PR review summaries and test coverage reports." |
| **"Next-gen / Revolutionary"** | Unprovable self-praise that diminishes technical credibility. | State concrete specifications: "Sub-10ms query execution across 50M rows." |
| **"Game-changing insights"** | Empty corporate buzzword. | "Real-time CPU throttling and memory leak alerts." |
| **"All-in-one platform"** | False promise that signals lack of specialized focus. | "Unified telemetry dashboard for Kubernetes clusters." |
| **"AI-powered / Smart"** | Prefixing "AI" or "Smart" to every button, filter, and card is pure slop. | "Auto-complete", "Synthesized", "Clustered", or simply omit the adjective. |
| **"Effortlessly manage"** | Fluff word. | "Manage", "Configure", "Deploy". |

---

## 2. Headline & Title Craft

### Rule 2.1: Ban Greeting Clichés
- 🚫 **Slop:** `Welcome back, Alex! 👋` or `Good morning! Ready to crush your goals? 🚀`
- ✅ **Craft:** Name the active system context or operating period:
  - `Production Telemetry · eu-central-1`
  - `October 2026 Financial Overview`
  - `Database Migration Status`

### Rule 2.2: Context over Hype
- 🚫 **Slop:** `The Future of Finance is Here ✨`
- ✅ **Craft:** `Multi-currency corporate cards with automated receipt reconciliation`

### Rule 2.3: Zero Trailing Periods on Headlines
- 🚫 **Slop:** `System Overview.` or `Filter Records:.`
- ✅ **Craft:** `System overview`, `Filter records`

---

## 3. Metric & Numerical Realism

Vibecoded interfaces always showcase fake numbers like `$123,456.00`, `99.9%`, or `+20%!!`. Authentic interfaces use realistic figures and explicit comparison baselines.

### Rule 3.1: Explicit Comparison Benchmarks
Every percentage or differential indicator must define what it is measured against:
- 🚫 **Slop:** `+14.8%!!`
- 🚫 **Slop:** `3 fewer errors!`
- ✅ **Craft:** `+14.8% vs last 30 days`
- ✅ **Craft:** `3 fewer incidents vs prior release`
- ✅ **Craft:** `-42ms response latency vs p99 target`

### Rule 3.2: Plausible Numerical Precision
Match decimal precision to real-world domain expectations:
- **Financial Balances:** Fixed 2 decimals with tabular alignment (`$42,819.50`).
- **Percentage Changes:** 1 decimal place (`+4.2%`), rarely 4 decimals unless trading crypto.
- **Latency / Response Times:** Integer milliseconds (`184ms`, `28ms`).
- **Server Health:** 2 decimal uptime percentages (`99.98%`).

---

## 4. Microcopy Redlines

### Buttons & CTAs
- 🚫 `Get Started Free Today!` $\to$ ✅ `Create organization` or `Start 14-day trial`
- 🚫 `Submit!` $\to$ ✅ `Save changes` or `Deploy cluster`
- 🚫 `Click Here` $\to$ ✅ `View documentation`

### Input Placeholders
- 🚫 `Search anything you can imagine...` $\to$ ✅ `Search repositories, branches, or PRs (⌘K)`
- 🚫 `Type your prompt here ✨...` $\to$ ✅ `Describe error or paste stack trace...`

### Status Badges
- 🚫 `PRO ✨` $\to$ ✅ `Tier 2` or `Enterprise`
- 🚫 `New 🔥` $\to$ ✅ `v2.4` or `Preview`
- 🚫 `Active 🟢` $\to$ ✅ Quiet text with 6px solid dot: `● Connected`

