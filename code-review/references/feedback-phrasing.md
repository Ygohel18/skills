# Constructive Feedback Phrasing Guide

> Companion reference for `code-review`.
> Practical before-and-after examples demonstrating how to deliver actionable, respectful, and high-impact code review feedback.

---

## 1. Core Principles of Review Phrasing

1. **Depersonalize the Criticism:** Focus on the code, the function, or the behavior, not the author. Use *"this function"* or *"this approach"*, never *"you failed to"* or *"your code"*.
2. **Inquire Before Accusing:** When code looks surprising, ask clarifying questions instead of declaring it broken. The author might know an edge case or business constraint you don't.
3. **Always State the "Why":** Explain the concrete risk (race condition, memory leak, user-facing crash) rather than issuing bare commands.
4. **Offer Concrete Solutions:** Whenever flagging a problem, provide a code snippet, alternative pattern, or documentation link.
5. **Acknowledge Good Engineering:** Point out elegant abstractions, comprehensive tests, and clean refactorings. Reviews should not be 100% negative critique.

---

## 2. Before & After Review Comment Examples

### Scenario A: Potential Bug / Unhandled Edge Case
- ❌ **Harsh / Accusatory:**
  > *"You forgot to handle when `user` is null. This will crash in production."*
- ⚠️ **Vague:**
  > *"Handle null here."*
- ✅ **Constructive & Specific:**
  > *"What happens here if `user` is null (e.g. an unauthenticated guest session)? It looks like `user.profile` might raise a `NullPointerException`. Could we add an early guard clause or optional chaining like `user?.profile`?"*

---

### Scenario B: Missing Test Coverage
- ❌ **Harsh / Dismissive:**
  > *"Where are the tests? I'm not approving without tests."*
- ⚠️ **Passive:**
  > *"Needs more tests."*
- ✅ **Constructive & Specific:**
  > *"The new currency conversion logic in `convertRate()` handles rounding nicely. Could we add a unit test covering boundary cases like zero amount, negative inputs, and unsupported currency codes to lock in this behavior?"*

---

### Scenario C: Performance Concern (Unmeasured)
- ❌ **Premature / Demanding:**
  > *"This is terrible for performance. Doing an array search inside this loop is $O(N^2)$! Rewrite it with a hash map."*
- ⚠️ **Speculative:**
  > *"Might be slow."*
- ✅ **Constructive & Measured:**
  > *"Since `userList` could grow up to several thousand items in enterprise tenants, calling `find()` inside this `forEach` loop might become an $O(N^2)$ bottleneck. If we convert `userList` to a `Map<UserId, User>` beforehand, lookup drops to $O(1)$:*
  > ```typescript
  > const userMap = new Map(userList.map(u => [u.id, u]));
  > ```
  > *"What do you think?"*

---

### Scenario D: Subjective Style Preference (Nit)
- ❌ **Prescriptive / Blocking:**
  > *"Don't use `reduce` here, it's unreadable. Use a `for...of` loop."*
- ⚠️ **Dressed Up as Blocker:**
  > *"Change this `reduce` to a `for` loop before merging."*
- ✅ **Constructive Nit:**
  > *"**Nit (non-blocking):** A simple `for...of` loop or `filter().map()` pipeline might be slightly easier to scan for readers unfamiliar with accumulator patterns here, but I leave it to your preference."*

---

### Scenario E: Security Risk (SQL / Injection)
- ❌ **Alarmist / Accusatory:**
  > *"You introduced an SQL injection vulnerability! Never write code like this."*
- ⚠️ **Cryptic:**
  > *"Security issue with query."*
- ✅ **Constructive & Actionable (BLOCKER):**
  > *"**BLOCKER:** String interpolation inside this raw SQL query (`WHERE id = '${userId}'`) exposes us to SQL injection if `userId` contains unescaped single quotes. We should switch to parameterized query bindings:*
  > ```python
  > # Suggested fix:
  > cursor.execute("SELECT * FROM accounts WHERE id = %s", (user_id,))
  > ```
  > *"This ensures the database driver safely escapes all input parameters."*

---

### Scenario F: Scope Creep / Unrelated Changes
- ❌ **Blunt:**
  > *"Why did you touch 15 other files? Revert them."*
- ⚠️ **Unclear:**
  > *"Too many changes."*
- ✅ **Constructive & Collaborative:**
  > *"I noticed the changes in `auth/` also include reformatting and minor refactors in `billing/`. The core auth changes look great! Would you be open to splitting the `billing/` cleanup into a separate follow-up PR? It will make this PR much faster to review and safer to backport if needed."*

---

### Scenario G: Positive Reinforcement (Appreciating Quality)
- ✅ **Specific Praise:**
  > *"Great catch adding this mutex lock around the shared cache write. That prevents a subtle race condition under concurrent requests."*
- ✅ **Appreciating Documentation:**
  > *"Thank you for the thorough PR description and the diagram of the state machine! It made reviewing this complex flow much easier."*
- ✅ **Appreciating Tests:**
  > *"Really appreciate the parameterized edge-case tests here—especially covering the leap-year date calculation."*
