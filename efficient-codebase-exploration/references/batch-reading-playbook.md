# Batch Reading Playbook

A tactical guide for AI IDE agents on orchestrating multi-file parallel reads, grouping related source modules, and eliminating single-file turn latency.

---

## 1. The Anti-Pattern: Sequential Read Lag

When an agent needs to understand a feature (e.g. an API endpoint), the naive sequential approach consumes 4–6 full conversation turns:

```text
Turn 1: Agent reads routes/api.ts
Turn 2: Agent reads controllers/user.controller.ts
Turn 3: Agent reads services/user.service.ts
Turn 4: Agent reads models/user.model.ts
Turn 5: Agent reads dtos/update-user.dto.ts
```

**Total Cost:** 5 conversational rounds, massive re-serialization of conversation history, and high token overhead.

---

## 2. The Solution: Parallel Batched Inspection

In turn 1, locate the relevant file cluster. In turn 2, issue **all independent read calls simultaneously**:

```json
// Turn 2: Batch tool calls issued in parallel
[
  { "tool": "read_file", "parameters": { "Path": "/app/routes/api.ts" } },
  { "tool": "read_file", "parameters": { "Path": "/app/controllers/user.controller.ts" } },
  { "tool": "read_file", "parameters": { "Path": "/app/services/user.service.ts" } },
  { "tool": "read_file", "parameters": { "Path": "/app/models/user.model.ts" } },
  { "tool": "read_file", "parameters": { "Path": "/app/dtos/update-user.dto.ts" } }
]
```

**Total Cost:** Exactly 1 conversational round. The agent immediately holds the entire vertical slice in context and can reason about data flow end-to-end.

---

## 3. Recommended Grouping Strategies

### Pattern A: The Vertical Slice (Web APIs)
When implementing or fixing an API route, batch-read:
1. Route registration (`routes/web.php`, `routes/api.ts`, `app/api/.../route.ts`).
2. Controller / Handler (`controllers/order.controller.ts`).
3. Domain Service / Repository (`services/order.service.ts`).
4. Data Model / Entity (`models/order.entity.ts`).
5. Validation Schema / DTO (`dto/create-order.dto.ts`).

### Pattern B: The Component Cluster (Frontend)
When modifying a UI component, batch-read:
1. The component implementation (`components/UserProfile.tsx`).
2. The subcomponents or child widgets imported by it (`components/Avatar.tsx`, `components/UserBadge.tsx`).
3. Custom hooks or state store (`hooks/useUser.ts`, `stores/userStore.ts`).
4. Type definition file (`types/user.ts`).

### Pattern C: The Bug Triage Cluster
When investigating an error stack trace:
1. The file and line where the exception threw.
2. The calling function that passed the unvalidated argument.
3. The configuration or mock fixture that provided the input data.

---

## 4. Range Reads vs Full File Reads

- **Small to Medium Files ($< 300\text{ lines}$):** Read the whole file. Partial reads force repeated follow-up tool calls when a missing function is referenced lower down.
- **Large Files ($> 800\text{ lines}$):**
  - Read lines 1–60 to inspect imports, configuration, and interface definitions.
  - Use targeted grep (`grep -n "function targetMethod"`) to find the exact line number.
  - Read lines $(N - 10)$ to $(N + 60)$ around the target method.
