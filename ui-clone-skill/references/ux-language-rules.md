# UX Language Rules — Writing for Real People

## The Golden Rule

> Every word on the screen is for a real person who is NOT a developer.
> Never write for yourself. Write for your grandmother, your neighbor, or a busy shop owner.

This applies to **every** piece of text in every project: labels, buttons, headings, error messages, empty states, tooltips, placeholders, confirmation dialogs, status messages, and helper text.

---

## Who Uses This Product

Assume the user:
- Is **not** a developer, designer, or technical professional
- Has never heard of terms like "API", "authentication", "payload", "middleware", "schema", "null", "boolean", "endpoint", or "token" (in the programming sense)
- Uses the product to accomplish a real-world goal (e.g., send a message, manage their store, view their reports)
- Is busy and may be on their phone
- Gets frustrated quickly if they don't understand something

---

## Banned Words & Phrases

Never use these in any UI text:

| ❌ Technical Jargon          | ✅ Human Alternative                          |
|-----------------------------|-----------------------------------------------|
| Authentication failed        | Wrong email or password. Please try again.    |
| Unauthorized                 | You need to sign in to view this.             |
| 403 Forbidden                | You don't have permission to see this page.   |
| 404 Not Found                | We couldn't find that page.                   |
| 500 Internal Server Error    | Something went wrong on our end. Try again.   |
| Invalid input                | Please check what you entered and try again.  |
| Invalid credentials          | Wrong email or password.                      |
| Token expired                | Your session has ended. Please sign in again. |
| Null / undefined / NaN       | — (never show these to users)                 |
| Failed to fetch              | We couldn't connect. Check your internet.     |
| Payload too large            | The file you uploaded is too large.           |
| Validation error             | Please fix the highlighted fields.            |
| Rate limit exceeded          | Too many attempts. Please wait a minute.      |
| Submit                       | Save / Send / Continue / Done (context-based) |
| Abort                        | Cancel                                        |
| Toggle                       | Turn on / Turn off / Switch                   |
| Execute                      | Run / Start / Do                              |
| Initialize                   | Set up / Get started                          |
| Deploy                       | Publish / Go live                             |
| Query                        | Search / Find                                 |
| Config / Configuration       | Settings                                      |
| Parameters                   | Options / Details                             |
| Schema                       | — (never show to users)                       |
| Repository / Repo            | — (never show to users)                       |
| Cache cleared                | Refreshed / Updated                           |
| Sync / Synced                | Updated / Saved                               |
| Deprecated                   | — (never show to users)                       |

---

## Button Labels

Buttons must describe the **action** the user is taking, not a generic verb.

| ❌ Bad              | ✅ Good                                 |
|--------------------|----------------------------------------|
| Submit             | Save changes / Send message / Continue |
| OK                 | Got it / Done / Yes, delete it         |
| Cancel             | Never mind / Go back / Keep it         |
| Confirm            | Yes, I'm sure / Confirm booking        |
| Delete             | Remove / Delete this post              |
| Abort              | Stop / Cancel                          |
| Execute            | Run report / Start scan                |
| Proceed            | Continue / Next step                   |

---

## Error Messages

Every error must tell the user:
1. **What went wrong** — in plain words
2. **What to do next** — a specific action

| ❌ Bad                          | ✅ Good                                                         |
|---------------------------------|-----------------------------------------------------------------|
| Invalid email address           | Please enter a valid email (e.g. you@example.com)               |
| Password too short              | Your password must be at least 8 characters long                |
| Required field missing          | Please fill in your name before continuing                      |
| Authentication error            | Wrong email or password. Try again or reset your password.      |
| Network error                   | We couldn't connect. Check your internet and try again.         |
| File upload failed              | We couldn't upload that file. Try a smaller one (max 5MB).      |
| Permission denied               | You don't have permission to do that. Contact your admin.       |
| Session expired                 | You've been signed out for security. Please sign in again.      |

---

## Empty States

Every list, table, or feed that can be empty must show:
- A friendly illustration or icon (no error iconography)
- A short, warm message explaining why it's empty
- A clear action button (if applicable)

| Section             | ❌ Bad empty text             | ✅ Good empty text                                           |
|---------------------|-------------------------------|--------------------------------------------------------------|
| Messages inbox      | No messages found             | Your inbox is empty. Start a conversation!                   |
| Orders list         | 0 records                     | No orders yet. Share your store link to get your first sale! |
| Search results      | No results                    | Nothing found for "shoes". Try different words.              |
| Notifications       | No notifications               | You're all caught up! No new notifications.                  |
| Blog posts          | No posts                      | No posts published yet. Write your first one!                |

---

## Loading States

- Never show "Loading..." alone — add context: "Loading your messages…" / "Getting your orders ready…"
- Never leave a blank screen — always show a skeleton or placeholder
- For slow operations (>3 seconds), show progress feedback

---

## Confirmation Dialogs

Follow this structure:
- **Title**: What is about to happen (active verb, not a question where possible)
- **Body**: Brief consequence of the action in plain words
- **Confirm button**: Describes the irreversible action ("Yes, delete post")
- **Cancel button**: Lets them walk back ("Keep post" / "Never mind")

```
Title:   Delete this post?
Body:    This will permanently remove "My first blog post" and it can't be undone.
[Delete post]   [Keep post]
```

---

## Form Labels & Placeholders

- **Labels**: Short noun phrases. Never truncate. Always visible (not hidden inside the input).
- **Placeholders**: Optional example values. Never use placeholder as the only label — it disappears when typing.
- **Helper text**: One line below the input explaining the requirement BEFORE the user makes a mistake.

| ❌ Bad label        | ✅ Good label                | Helper text example                            |
|--------------------|------------------------------|------------------------------------------------|
| usr_name           | Username                     | Only letters, numbers, and underscores         |
| pwd                | Password                     | Must be at least 8 characters                  |
| DOB                | Date of birth                | Enter as DD/MM/YYYY                            |
| Org                | Company or organisation name | —                                              |
| Tel                | Phone number                 | Include your country code (e.g. +91)           |

---

## Admin Dashboards — Special Rules

When building admin dashboards or management interfaces:

1. **No developer metrics on user-facing screens** — No "API calls", "response time (ms)", "error rate (%)". Use plain counters: "Messages sent", "Orders this week", "New customers".

2. **Sidebar labels must be plain nouns** — "Users" not "User Management", "Reports" not "Analytics Dashboard", "Settings" not "Configuration".

3. **Status badges must be human words** — "Active", "Paused", "Pending review", "Completed", "Cancelled". Never: "ENABLED", "INACTIVE_SCHEDULED", "ERR_TIMEOUT".

4. **Data tables** — Every column header must be a plain noun/phrase. Avoid abbreviations. "Last sign in" not "last_auth_ts". "Monthly revenue" not "rev_mtd_usd".

5. **Action menus** — "Edit details", "Remove from list", "Send a message", not "PUT /users/:id", "DELETE record", "POST message".

6. **Notifications / Toasts** — Always friendly:
   - ✅ "Changes saved!" / "Post published!" / "Message sent!"
   - ❌ "200 OK" / "Record updated successfully in database" / "Cache invalidated"

---

## Page Titles & Headings

- `<h1>` must describe the page purpose, not the app name: "Your Orders" not "Orders Module"
- Heading hierarchy: one `<h1>` per page, logical `h2`/`h3` nesting
- No ALL CAPS in headings (use CSS for visual treatment if needed)
- Avoid periods at the end of headings

---

## Tone

| ❌ Cold / Corporate           | ✅ Warm / Human                                          |
|-------------------------------|----------------------------------------------------------|
| User account created.         | Welcome! Your account is ready.                          |
| Password updated successfully.| Your password has been changed. You're all set!          |
| Record deleted.               | Done! That item has been removed.                        |
| Insufficient funds.           | You don't have enough balance for this. Top up to continue.|
| Access revoked.               | [User] can no longer access this workspace.              |

---

## Quick Checklist (Before Shipping Any Screen)

- [ ] Zero technical terms visible to the end user
- [ ] Every error message explains what went wrong AND what to do
- [ ] Every empty state has friendly copy + action (if applicable)
- [ ] Every button label describes the specific action being taken
- [ ] Form validation messages are sentence-case, specific, and helpful
- [ ] Loading states include context ("Loading your dashboard…")
- [ ] Confirmation dialogs have descriptive action buttons
- [ ] No status codes, HTTP verbs, or developer-speak anywhere on screen
- [ ] Admin labels use plain nouns, not module/system names
