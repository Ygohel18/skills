# Token Budget Heuristics & Context Management

Techniques for preserving context window capacity, minimizing unnecessary tool invocations, and preventing context degradation during deep codebase exploration.

---

## 1. Context Decay & Cost Economics

Every file read by an AI agent remains in the conversation transcript for all subsequent turns.
- In turn 1, reading a 500-line file consumes $\sim 2,000$ tokens.
- By turn 10, that same file has been re-sent to the model 9 more times, totaling $\sim 20,000$ cumulative tokens.
- Loading five 2,000-line minified bundles or data fixtures can permanently consume 50,000+ tokens of context, degrading reasoning quality and inflating API latency.

---

## 2. High-Yield Token Preservation Rules

### Rule 1: Never Ingest Data Fixtures or Minified Artifacts
- Check file sizes before reading. If a file is $> 500\text{KB}$ or contains `.min.js`, `.map`, or thousands of lines of seed mock data (`fixtures/data.json`), do **not** read the whole file.
- Inspect only the first 20 lines to understand the JSON schema:
  ```bash
  head -n 20 large_fixture.json
  ```

### Rule 2: Chain Shell Calls
Instead of running separate commands across multiple turns:
```bash
# ❌ VULNERABLE TO TURN BLOAT (3 turns):
# Turn 1: git status
# Turn 2: ls src/
# Turn 3: cat package.json

# ✅ TOKEN-CONSCIOUS SINGLE TURN:
git status && ls src/ && head -n 30 package.json
```

### Rule 3: Summarize Findings Internally
When exploring a complex directory structure:
- **Do not** paste long directory listings into conversation responses.
- Synthesize findings into compact, high-signal architectural summaries:
  > *"The project uses Next.js 14 App Router with Supabase authentication. Handlers are isolated in `app/api/` and shared database models live in `lib/db/schema.ts`."*

### Rule 4: Zero Redundant Tool Calls
- If a file's content has already been retrieved in Turn 2, reference it directly from conversation memory in Turn 5.
- Never call `read_file` on the same unchanged path twice in one session.
