# Replicate REST API Reference

A definitive HTTP and cURL specification for Replicate's `/v1` REST endpoints, covering model predictions, polling, streaming, cancellation, and file uploads.

---

## 1. Global Request Headers

| Header | Format | Requirement | Purpose |
|---|---|---|---|
| `Authorization` | `Bearer <token>` | **Mandatory** | Injects your Replicate API token (`r8_...`). |
| `Content-Type` | `application/json` | Mandatory for POST | Declares JSON payload encoding. |
| `Prefer` | `wait=60` | Optional | Holds HTTP connection open for synchronous response (up to 60s). |
| `Accept` | `text/event-stream` | Optional | Requests Server-Sent Events (SSE) token stream. |

---

## 2. Prediction Endpoints

### 2.1 Create Prediction by Model
Creates a prediction for the default/public version of an official model.

```http
POST /v1/models/{model_owner}/{model_name}/predictions
Host: api.replicate.com
Authorization: Bearer r8_************************************
Content-Type: application/json
Prefer: wait=60

{
  "input": {
    "prompt": "Cyberpunk terminal interface with emerald phosphorus monospace characters",
    "aspect_ratio": "16:9"
  },
  "stream": false,
  "webhook": "https://api.domain.com/webhooks/replicate",
  "webhook_events_filter": ["start", "completed"]
}
```

#### cURL Example:
```bash
curl -s -X POST "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait=60" \
  -d '{
    "input": {
      "prompt": "Aerial view of misty pine forest at sunrise",
      "aspect_ratio": "16:9"
    }
  }'
```

---

### 2.2 Create Prediction by Explicit Version ID
Used when targeting an exact immutable model version hash.

```http
POST /v1/predictions
Host: api.replicate.com
Authorization: Bearer r8_************************************
Content-Type: application/json

{
  "version": "b26b207191bf0884866d6d3725145b0e5f2508402e85f7ac3e26180805ada779",
  "input": {
    "prompt": "An astronaut riding a horse on Mars"
  }
}
```

---

### 2.3 Retrieve Prediction Status
Fetches the current lifecycle state, error message, metrics, and output array.

```http
GET /v1/predictions/{prediction_id}
Host: api.replicate.com
Authorization: Bearer r8_************************************
```

#### Response Payload (HTTP 200 OK):
```json
{
  "id": "gm3q2v7n8srg00chg9q89g954w",
  "model": "black-forest-labs/flux-schnell",
  "version": "latest",
  "status": "succeeded",
  "input": {
    "prompt": "Aerial view of misty pine forest at sunrise"
  },
  "output": [
    "https://replicate.delivery/yhqm/e84s9.../output.webp"
  ],
  "error": null,
  "logs": "Running 4 steps on Nvidia A100...\nStep 4/4 complete.\n",
  "metrics": {
    "predict_time": 1.28
  },
  "created_at": "2026-11-01T12:00:00.000Z",
  "started_at": "2026-11-01T12:00:01.000Z",
  "completed_at": "2026-11-01T12:00:02.280Z",
  "urls": {
    "cancel": "https://api.replicate.com/v1/predictions/gm3q2v7n8srg00chg9q89g954w/cancel",
    "get": "https://api.replicate.com/v1/predictions/gm3q2v7n8srg00chg9q89g954w",
    "stream": "https://stream.replicate.com/v1/files/..."
  }
}
```

---

### 2.4 Cancel a Running Prediction
Immediately halts GPU execution to terminate per-second compute billing.

```http
POST /v1/predictions/{prediction_id}/cancel
Host: api.replicate.com
Authorization: Bearer r8_************************************
```

#### cURL Example:
```bash
curl -s -X POST "https://api.replicate.com/v1/predictions/gm3q2v7n8srg00chg9q89g954w/cancel" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN"
```

---

## 3. Server-Sent Events (SSE) Streaming

To stream token-by-token generation from an LLM:

1. Dispatch request with `stream: true` or retrieve the `urls.stream` field from the response.
2. Read the SSE stream:

```bash
curl -N -s -X POST "https://api.replicate.com/v1/models/deepseek-ai/deepseek-r1/predictions" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "input": {
      "prompt": "Draft a formal apology letter from an airline.",
      "max_tokens": 512
    },
    "stream": true
  }'
```

#### Event Format:
```text
event: output
data: Dear

event: output
data:  Valued

event: output
data:  Passenger,

event: done
data: {}
```

---

## 4. Replicate Files API (`/v1/files`)

Use this endpoint to upload local binary files (images, audio clips, video frames) and receive an ephemeral, public HTTPS URL suitable for passing into model input fields.

### Upload Binary File:
```bash
curl -s -X POST "https://api.replicate.com/v1/files" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: image/png" \
  --data-binary "@/Users/apple/Pictures/input-frame.png"
```

#### Response (HTTP 201 Created):
```json
{
  "id": "file_01jb87g92v...",
  "name": "input-frame.png",
  "size": 1845920,
  "content_type": "image/png",
  "urls": {
    "get": "https://replicate.delivery/xezq/file_01jb87g92v.../input-frame.png"
  }
}
```
*Pass `.urls.get` into the target model's `image` or `first_frame_image` parameter.*

