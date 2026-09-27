# GraphQL Schema Design & Best Practices

> Companion reference for `api-design`.
> Guidance for schema-first architecture, nullability discipline, N+1 query prevention, security limits, and error handling.

---

## 1. Schema-First Design Principles

1. **Design from the Client's Perspective:** Model schemas around user interface workflows and domain entities, not an exact 1:1 mirroring of database tables.
2. **Prefer Explicit Mutations with Payload Types:**
   - Avoid generic mutations with ambiguous return types.
   - Always return an object type containing the affected entity and optional user errors:
   ```graphql
   # Good: Dedicated input and payload types
   input CreateOrderInput {
     customerId: ID!
     items: [OrderItemInput!]!
   }

   type CreateOrderPayload {
     order: Order
     userErrors: [UserError!]!
   }

   type Mutation {
     createOrder(input: CreateOrderInput!): CreateOrderPayload!
   }
   ```

---

## 2. Nullability Discipline (`!` Usage)

A common mistake is making all output fields non-null (`!`). In GraphQL, if a non-null field resolver throws an error, the null bubbles up and destroys the entire parent object.

### The Nullability Rules:
1. **Inputs: Be Strict (Non-Null `!` where required):** If an argument or input field is strictly required for the query or mutation to execute, mark it `!`.
2. **Outputs: Default to Nullable:** Make entity fields nullable so that if one resolver fails (e.g., a microservice timeout fetching `author.avatar`), the rest of the payload (`author.name`, `author.id`) still renders gracefully.
3. **Array Nullability Combinations:**
   - `[Item]`: Array can be null; elements can be null.
   - `[Item]!`: Array is guaranteed to exist (may be empty `[]`); elements can be null.
   - `[Item!]!`: Array is guaranteed to exist; every element is guaranteed non-null. *(Preferred for item lists)*.

---

## 3. Solving the N+1 Problem with DataLoaders

When querying nested relationships (e.g. 50 orders, each requesting their customer), naive GraphQL resolvers execute 1 query for orders + 50 separate queries for each customer (the N+1 problem).

### The DataLoader Pattern:
- **Batching:** Collects all individual keys requested within a single tick of the event loop and executes a single batched query: `SELECT * FROM customers WHERE id IN (1, 2, 3...)`.
- **Caching:** Memoizes results within the lifecycle of a single request to avoid duplicate database fetches.

```javascript
// Example DataLoader instantiation (per-request)
const customerLoader = new DataLoader(async (customerIds) => {
  const customers = await db.findCustomersByIds(customerIds);
  // Must return items in exact matching order of keys
  return customerIds.map(id => customers.find(c => c.id === id));
});

// Resolver
const resolvers = {
  Order: {
    customer: (order, _, { loaders }) => loaders.customer.load(order.customerId),
  }
};
```

---

## 4. Security & Public API Defenses

Unlike REST where endpoints have fixed compute profiles, a single GraphQL query can traverse circular relationships infinitely and crash a server.

### Essential Security Guardrails:
1. **Query Depth Limiting:** Reject queries exceeding a safe nesting depth (typical limit: 5 to 7 levels).
   ```graphql
   # Malicious circular attack:
   query {
     user { friends { friends { friends { friends { friends { ... } } } } } }
   }
   ```
2. **Query Complexity Analysis:** Assign a point cost to fields (e.g., scalar = 1 point, list = 10 points $\times$ limit). Reject queries exceeding a budget (e.g. 1,000 points).
3. **Persisted Queries (Automatic Persisted Queries / APQ):** In production, allow clients to send a SHA-256 hash of pre-registered queries rather than arbitrary raw query strings.
4. **Disable Introspection in Production:** Turn off `__schema` introspection for public APIs unless public API exploration is an explicit goal.

---

## 5. Modern Error Handling: Union Results

Instead of relying solely on the top-level `errors` array, represent expected domain errors as explicit schema types:

```graphql
union CheckoutResult = CheckoutSuccess | OutOfStockError | PaymentDeclinedError

type Mutation {
  checkout(cartId: ID!): CheckoutResult!
}
```

The client handles error states using standard GraphQL fragments:
```graphql
mutation DoCheckout($cartId: ID!) {
  checkout(cartId: $cartId) {
    ... on CheckoutSuccess {
      orderId
      totalAmount
    }
    ... on OutOfStockError {
      outOfStockItemIds
      message
    }
    ... on PaymentDeclinedError {
      reasonCode
    }
  }
}
```

---

## 6. REST vs. GraphQL Decision Matrix

| Dimension | Choose REST When... | Choose GraphQL When... |
|---|---|---|
| **Client Types** | Public 3rd-party developers, standard webhook consumers, simple integrations. | Multi-platform internal apps (Mobile, Web, Watch) with widely differing screen data needs. |
| **Caching** | Heavy reliance on HTTP edge CDN caching (Cloudflare, Fastly, Varnish via GET/ETag). | Fine-grained field-level caching via Apollo Client / Relay normalized cache. |
| **Payload Size** | Standardized, predictable entity representations. | Mobile clients requiring over-fetching elimination over high-latency cellular networks. |
| **Tooling & Setup**| Zero special client libraries required (`fetch` / `cURL` out of the box). | Complex frontend teams benefiting from end-to-end TypeScript code generation from schema. |
