# Architecture Decision Record (ADR) Template & Worked Example

> Companion reference for `docs-and-adr`.
> Contains an industry-standard ADR template and a complete worked example illustrating trade-off analysis.

---

## 1. Ready-to-Copy ADR Template

```markdown
# ADR-[NUMBER]: [Short Title Describing the Decision]

- **Status:** [Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXXX]
- **Date:** YYYY-MM-DD
- **Author(s):** [Names / Team]
- **Deciders:** [Key Decision Makers]
- **Technical Story / Ticket:** [Link to Issue / JIRA Ticket]

---

## Context & Problem Statement
[Describe the business or technical context, user forces, and specific problem that triggered this decision. What constraints (performance, cost, team velocity, security) apply?]

## Decision Drivers
- [Driver 1: e.g. Support 10,000 concurrent websocket connections]
- [Driver 2: e.g. Minimize operational cloud infrastructure costs]
- [Driver 3: e.g. Zero data loss guarantee during network partitions]

## Considered Options
1. **Option 1:** [Name of option]
2. **Option 2:** [Name of option]
3. **Option 3:** [Name of option]

---

## Decision Outcome
Chosen option: **"[Option X]"**, because [concise justification summarizing why this option best addresses the decision drivers].

### Positive Consequences
- [Advantage 1: e.g. Eliminates polling load on the relational database]
- [Advantage 2: e.g. Native client-side support in modern browsers]

### Negative Consequences & Trade-offs
- [Trade-off 1: e.g. Requires maintaining sticky sessions or Redis Pub/Sub backplane]
- [Trade-off 2: e.g. Team must learn and adopt new connection monitoring tools]

---

## Pros & Cons of the Options

### Option 1: [Name]
- ✅ Good, because [argument]
- ❌ Bad, because [argument]

### Option 2: [Name]
- ✅ Good, because [argument]
- ❌ Bad, because [argument]

---

## Links & References
- [Link to benchmark / proof of concept]
- [Related ADRs, e.g., Supersedes ADR-0001]
```

---

## 2. Complete Worked Example

```markdown
# ADR-0004: Adopt Redis Pub/Sub for Live Order Status Updates

- **Status:** Accepted
- **Date:** 2026-09-15
- **Author(s):** Alex Rivera, Platform Team
- **Deciders:** Architecture Guild
- **Technical Story / Ticket:** PROJ-842

---

## Context & Problem Statement
Currently, our merchant dashboard polls the `/api/orders` endpoint every 3 seconds to check for new incoming orders. During peak holiday rush hours, 50,000 active merchant dashboards generate ~16,600 read requests per second on PostgreSQL, causing connection pool exhaustion and read latency spikes above 2.5 seconds. We need a real-time push mechanism to deliver live order updates to web dashboards with under 500ms latency.

## Decision Drivers
- Eliminate continuous polling load on the primary PostgreSQL database.
- Deliver order status updates to connected merchant browsers within 500ms.
- Support up to 75,000 concurrent open connections with minimal memory footprint.
- Low operational complexity for our current Kubernetes infrastructure.

## Considered Options
1. **Option 1: Server-Sent Events (SSE) backed by Redis Pub/Sub**
2. **Option 2: Bi-directional WebSockets on dedicated Node gateway**
3. **Option 3: Retain HTTP Polling with an aggressive edge Redis cache**

---

## Decision Outcome
Chosen option: **"Option 1: Server-Sent Events (SSE) backed by Redis Pub/Sub"**, because:
- Order updates are strictly server-to-client notifications (unidirectional); SSE uses standard HTTP/2 streams without custom framing protocols.
- Our existing Redis cluster easily handles 100k messages/second with sub-millisecond broadcast latency.
- SSE reconnects automatically and works seamlessly with standard corporate firewalls.

### Positive Consequences
- Database read load drops by ~92% during peak traffic.
- Latency for order arrival drops from ~3,000ms (poll interval) to < 150ms.
- Native browser `EventSource` API requires zero extra client libraries.

### Negative Consequences & Trade-offs
- Requires long-lived HTTP connections, necessitating higher connection limits on the NGINX ingress controller.
- Redis Pub/Sub does not persist missed messages; if a client disconnects, they must fetch the latest snapshot upon reconnection.

---

## Pros & Cons of the Options

### Option 1: SSE + Redis Pub/Sub (Chosen)
- ✅ Standard HTTP/2 protocol, works through all reverse proxies.
- ✅ Built-in browser reconnection logic via `EventSource`.
- ❌ Unidirectional only (cannot send client messages back over the same stream).

### Option 2: Full WebSockets
- ✅ Full bidirectional communication.
- ❌ Overhead of custom websocket handshake and ping/pong keepalives.
- ❌ Unnecessary complexity since merchants never send data across this channel.

### Option 3: Short HTTP Polling with Edge Cache
- ✅ Simplest architectural change.
- ❌ Still generates massive request volumes and wastes mobile battery.

---

## Links & References
- Proof-of-concept load test: `https://github.com/internal/sse-benchmark`
- Supersedes: None
```
