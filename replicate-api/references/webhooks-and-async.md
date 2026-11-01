# Production Webhooks & Asynchronous Execution

A comprehensive engineering guide for handling asynchronous predictions, polling strategies, and verifying HMAC-SHA256 webhook signatures from Replicate.

---

## 1. Why Webhooks are Mandatory for Video & Batches

Video models (Minimax, Kling, Luma) take anywhere from **60 to 180 seconds** to complete. Maintaining persistent HTTP connections for this duration introduces:
- Edge gateway timeouts (Cloudflare and AWS ALB default to 60s or 100s timeouts).
- Serverless execution timeouts (Vercel free tier limits functions to 10s–60s).
- Unnecessary network bandwidth consumption from rapid HTTP polling loops.

**Webhooks solve this by inverting control:** Replicate dispatches a `POST` request to your designated endpoint the instant the GPU finishes processing.

---

## 2. Configuring Webhooks on Predictions

When creating any prediction via REST or SDK, supply the `webhook` URL and event filters:

```json
{
  "input": {
    "prompt": "Cinematic 4k tracking shot across Norwegian fjords at golden hour",
    "prompt_optimizer": true
  },
  "webhook": "https://api.yourdomain.com/api/webhooks/replicate",
  "webhook_events_filter": ["start", "completed"]
}
```

### Event Filter Options:
- `"start"`: Dispatched when model finishes cold-boot and begins processing.
- `"output"`: Dispatched whenever an intermediate chunk/frame is available.
- `"completed"`: Dispatched when prediction reaches a terminal state (`succeeded`, `failed`, or `canceled`).

---

## 3. Webhook Payload Schema

Replicate sends the complete prediction object in the POST body:

```json
{
  "id": "gm3q2v7n8srg00chg9q89g954w",
  "status": "succeeded",
  "model": "minimax/video-01",
  "input": {
    "prompt": "Cinematic 4k tracking shot across Norwegian fjords"
  },
  "output": "https://replicate.delivery/yhqm/video-output.mp4",
  "error": null,
  "metrics": {
    "predict_time": 94.2
  },
  "created_at": "2026-11-01T12:00:00.000Z",
  "started_at": "2026-11-01T12:00:05.000Z",
  "completed_at": "2026-11-01T12:01:39.200Z"
}
```

---

## 4. Webhook Security: HMAC-SHA256 Signature Verification

To ensure webhook requests genuinely originate from Replicate and prevent spoofing, verify the cryptographic signature sent in the HTTP headers:

- `webhook-id`: Unique message identifier.
- `webhook-timestamp`: Unix timestamp (seconds).
- `webhook-signature`: Space-delimited list of base64-encoded signatures prefixed with `v1,`.

### Signature Verification Algorithm:
1. Retrieve your Webhook Signing Secret from your Replicate account settings (starts with `whsec_...`).
2. Construct the signed payload string: `"${webhook-id}.${webhook-timestamp}.${raw_body}"`.
3. Compute the HMAC-SHA256 hash using the decoded signing secret.
4. Compare computed signature against `webhook-signature`.

---

### Python Verification Handler (FastAPI / Flask)

```python
import hmac
import hashlib
import base64
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
WEBHOOK_SECRET = "whsec_your_secret_key_here"

def verify_replicate_signature(body: bytes, headers: dict) -> bool:
    webhook_id = headers.get("webhook-id")
    webhook_timestamp = headers.get("webhook-timestamp")
    webhook_signature = headers.get("webhook-signature")

    if not (webhook_id and webhook_timestamp and webhook_signature):
        return False

    # Extract base64 secret after 'whsec_'
    secret_bytes = base64.b64decode(WEBHOOK_SECRET.replace("whsec_", ""))
    
    # Construct verification message
    signed_content = f"{webhook_id}.{webhook_timestamp}.".encode("utf-8") + body
    
    # Compute expected signature
    computed = hmac.new(secret_bytes, signed_content, hashlib.sha256).digest()
    expected_sig = base64.b64encode(computed).decode("utf-8")

    # Signatures are formatted as 'v1,base64_hash ...'
    signatures = [s.split(",")[1] for s in webhook_signature.split(" ") if s.startswith("v1,")]
    return any(hmac.compare_digest(expected_sig, sig) for sig in signatures)

@app.post("/api/webhooks/replicate")
async def handle_replicate_webhook(request: Request):
    raw_body = await request.body()
    if not verify_replicate_signature(raw_body, dict(request.headers)):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")

    payload = await request.json()
    prediction_id = payload.get("id")
    status = payload.get("status")

    if status == "succeeded":
        video_url = payload.get("output")
        print(f"Prediction {prediction_id} succeeded! Video: {video_url}")
        # Save to database or push notification to user

    return {"received": True}
```

---

### Node.js / TypeScript Verification Handler (Express / Next.js)

```typescript
import crypto from "node:crypto";
import { Request, Response } from "express";

const WEBHOOK_SECRET = process.env.REPLICATE_WEBHOOK_SECRET!; // whsec_...

export function verifyWebhook(req: Request): boolean {
  const id = req.headers["webhook-id"] as string;
  const timestamp = req.headers["webhook-timestamp"] as string;
  const signature = req.headers["webhook-signature"] as string;

  if (!id || !timestamp || !signature) return false;

  const rawSecret = WEBHOOK_SECRET.startsWith("whsec_")
    ? WEBHOOK_SECRET.slice(6)
    : WEBHOOK_SECRET;
  const secretBuffer = Buffer.from(rawSecret, "base64");

  const signedPayload = `${id}.${timestamp}.${req.body.toString("utf-8")}`;
  const computedSignature = crypto
    .createHmac("sha256", secretBuffer)
    .update(signedPayload)
    .digest("base64");

  const passedSignatures = signature
    .split(" ")
    .filter((s) => s.startsWith("v1,"))
    .map((s) => s.slice(3));

  return passedSignatures.some((sig) =>
    crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(computedSignature))
  );
}
```

---

## 5. Webhook Engineering Best Practices

1. **Respond with HTTP 200 Fast:** Return `200 OK` within 2 seconds of receiving the webhook. Offload heavy processing (e.g. downloading and transcribing 1GB video files) to a background worker or task queue (e.g. BullMQ, Celery, SQS).
2. **Handle Idempotency:** Webhooks may be redelivered if a network blip occurs. Store `prediction.id` in a database and verify whether it has already been processed before executing side-effects.
3. **Fallback Poller:** In mission-critical workflows, run a lightweight cron job that polls predictions stuck in `processing` for longer than 15 minutes in case of webhook endpoint downtime.

