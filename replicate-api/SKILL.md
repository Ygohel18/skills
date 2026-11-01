---
name: replicate-api
description: >
  Comprehensive operational protocol and API integration standard for Replicate (replicate.com).
  Covers authentication, prediction lifecycles, synchronous execution (`Prefer: wait`), asynchronous polling,
  Server-Sent Events streaming, webhooks, and raw HTTP/SDK patterns (Python, Node/TS, cURL).
  Provides exact parameter configurations and schema templates for major Frontier LLMs and Reasoning models
  (OpenAI GPT-4o, o1; Anthropic Claude 3.5 Sonnet, Claude 3.5 Haiku; Google Gemini 2.0 Flash, Gemini 1.5 Pro)
  as well as leading Open-Weights LLMs (DeepSeek-R1, Llama 3.3 70B, Qwen 2.5), flagship Image generation
  (FLUX.1 schnell/dev/pro, Google Imagen 3, Recraft v3, SDXL, LoRA weights), Video generation
  (Minimax video-01, Kling 1.6, Luma Ray, CogVideoX), and Speech/Audio (Whisper-large-v3, MusicGen).
  Trigger whenever the user asks to "run a model on Replicate", "use Replicate API", "generate image/video with Replicate",
  "call FLUX on Replicate", "run GPT-4o on Replicate", "call Claude on Replicate", "run Gemini on Replicate",
  "run DeepSeek on Replicate", "stream LLM from Replicate", "set up Replicate webhooks",
  or configure any model endpoints and hardware deployments on replicate.com.
metadata:
  author: yash
  version: "1.0"
  scope: "replicate, replicate-api, llm, image-generation, video-generation, flux, deepseek, kling, minimax, ai-sdk"
allowed-tools: Bash(python3:*) Bash(node:*) Bash(curl:*) Read Write
---

# Replicate API Integration Standard

A production-grade operational standard for orchestrating AI workloads—LLMs, image synthesis, video generation, and speech—via Replicate's cloud API.

> **Sibling Standards & References:**
> - For exhaustive parameter dictionaries across the top 25 models, consult [`references/model-catalog-and-configs.md`](references/model-catalog-and-configs.md).
> - For raw cURL & HTTP endpoints, consult [`references/rest-api-reference.md`](references/rest-api-reference.md).
> - For Python SDK patterns (sync, async, streaming), consult [`references/sdk-recipes-python.md`](references/sdk-recipes-python.md).
> - For TypeScript / Node.js SDK patterns, consult [`references/sdk-recipes-node.md`](references/sdk-recipes-node.md).
> - For long-running prediction webhooks & HMAC verification, consult [`references/webhooks-and-async.md`](references/webhooks-and-async.md).

---

## 1. Authentication & API Fundamentals

### Authentication
Replicate authenticates all requests using a Bearer token in the `Authorization` header:
```bash
export REPLICATE_API_TOKEN="r8_************************************"
```
```http
Authorization: Bearer r8_************************************
```

### Official SDKs
- **Python:** `pip install replicate`
- **Node.js / TypeScript:** `npm install replicate`

---

## 2. Universal Execution Patterns

Replicate models run as **Predictions**. Predictions follow a strict lifecycle:
$$\text{starting} \longrightarrow \text{processing} \longrightarrow \text{succeeded} \;|\; \text{failed} \;|\; \text{canceled}$$

### Pattern A: Synchronous Blocking Execution (`Prefer: wait`)
Recommended for fast inference models (LLMs, FLUX.1 schnell, embeddings) completing under 60 seconds.

```bash
curl -s -X POST "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait=60" \
  -d '{
    "input": {
      "prompt": "An architectural render of a brutalist concrete villa in autumn, 35mm photography",
      "aspect_ratio": "16:9",
      "output_format": "webp"
    }
  }'
```
*When `Prefer: wait` is set, the API holds the HTTP connection open and returns HTTP 200 with `status: "succeeded"` and the populated `output` array/string.*

### Pattern B: Asynchronous Creation & Polling
Required for heavy jobs (video synthesis, fine-tunes, dense batches) taking between 30 and 300 seconds.

1. **Dispatch Prediction:**
   ```bash
   PRED_ID=$(curl -s -X POST "https://api.replicate.com/v1/models/kling-ai/kling-v1.6-pro/predictions" \
     -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"input": {"prompt": "Cinematic drone flyover of alpine glaciers, 4k", "duration": 5}}' \
     | jq -r .id)
   ```
2. **Poll Status:**
   ```bash
   curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
     "https://api.replicate.com/v1/predictions/$PRED_ID" | jq '{status: .status, output: .output}'
   ```

### Pattern C: Real-Time Token Streaming (Server-Sent Events)
Mandatory for interactive LLM applications.

```python
import replicate

for event in replicate.stream(
    "deepseek-ai/deepseek-r1",
    input={
        "prompt": "Explain quantum decoherence in three succinct paragraphs.",
        "max_tokens": 1024,
        "temperature": 0.6
    }
):
    print(str(event), end="", flush=True)
```

### Pattern D: Production Webhook Delivery
Eliminates polling overhead on video generation and batch pipelines.

```json
{
  "input": { "prompt": "A continuous tracking shot through an antique library" },
  "webhook": "https://api.yourdomain.com/api/webhooks/replicate",
  "webhook_events_filter": ["start", "completed"]
}
```
*Replicate signs webhook payloads using HMAC-SHA256 headers (`webhook-id`, `webhook-timestamp`, `webhook-signature`). Always verify signatures in production.*

---

## 3. Large Language Models (LLMs) & Reasoning Models

Replicate hosts both major **Frontier Proprietary Models** (OpenAI, Anthropic, Google) and state-of-the-art **Open-Weights Foundation & Reasoning Models** (DeepSeek, Meta, Alibaba) under a unified prediction and streaming API.

### 3.1 Frontier Proprietary Models (OpenAI, Anthropic, Google)
- **OpenAI GPT-4o & Reasoning:** `openai/gpt-4o`, `openai/gpt-4o-mini`, `openai/o1`
- **Anthropic Claude 3.5:** `anthropic/claude-3.5-sonnet`, `anthropic/claude-3.5-haiku`, `anthropic/claude-3-opus`
- **Google Gemini 2.0 & 1.5:** `google/gemini-2.0-flash`, `google/gemini-1.5-pro`, `google/gemini-1.5-flash`

#### Frontier Model Input Parameters:
- **OpenAI (`openai/gpt-4o`):** `prompt`, `system_prompt`, `image_input`, `max_completion_tokens` (default `4096`), `temperature` (default `1.0`), `top_p`.
- **Anthropic (`anthropic/claude-3.5-sonnet`):** `prompt`, `system_prompt`, `image`, `max_tokens` (default `8192`), `effort` (`"low"`, `"medium"`, `"high"`, `"max"` for reasoning depth).
- **Google (`google/gemini-2.0-flash`):** `prompt`, `system_instruction`, `images` (array of image URLs), `videos` (array of video URLs), `audio` (file URL), `max_output_tokens` (default `8192`), `thinking_level`.

### 3.2 Open-Weights Foundation & Reasoning Models
- **DeepSeek-R1 (Flagship Reasoning):** `deepseek-ai/deepseek-r1`
- **Llama 3.3 70B Instruct (Meta Flagship):** `meta/meta-llama-3.3-70b-instruct`
- **Qwen 2.5 72B Instruct (Alibaba Flagship):** `qwen/qwen-2.5-72b-instruct`

### Standard LLM Parameter Schema

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | `string` | *(Required)* | The user instruction or dialog history. |
| `system_prompt` | `string` | `""` | Guides persona, response format, and constraints (use `system_instruction` for Gemini). |
| `max_tokens` | `integer` | `1024` | Maximum tokens to generate (named `max_completion_tokens` on OpenAI). |
| `temperature` | `float` | `0.6` | Diversity scale: 0.1 for deterministic logic/code; 0.7 for creative writing. |
| `top_p` | `float` | `0.9` | Nucleus sampling threshold. |
| `presence_penalty` | `float` | `0.0` | Penalizes token reoccurrence (-2.0 to 2.0). |
| `frequency_penalty` | `float` | `0.0` | Penalizes token frequency (-2.0 to 2.0). |

### Production Python Snippet: Calling Frontier Models on Replicate
```python
import replicate

# 1. Calling OpenAI GPT-4o on Replicate
gpt4o_output = replicate.run(
    "openai/gpt-4o",
    input={
        "system_prompt": "You are a senior data architect.",
        "prompt": "Design a high-throughput event ingestion pipeline using Kafka and ClickHouse.",
        "max_completion_tokens": 1500,
        "temperature": 0.2
    }
)
print("".join(gpt4o_output))

# 2. Streaming Claude 3.5 Sonnet on Replicate with Extended Thinking
for chunk in replicate.stream(
    "anthropic/claude-3.5-sonnet",
    input={
        "prompt": "Evaluate security vulnerabilities in this smart contract.",
        "effort": "high",
        "max_tokens": 4096
    }
):
    print(str(chunk), end="", flush=True)
```

---

## 4. Flagship Image Generation & Inpainting

Replicate provides instant access to the FLUX.1 family, Google Imagen 3, Recraft, and Stable Diffusion.

### Flagship Image Model Identifiers
- **FLUX.1 [schnell] (Ultra-Fast 4-Step):** `black-forest-labs/flux-schnell`
- **FLUX.1 [dev] (High-Fidelity Guidance):** `black-forest-labs/flux-dev`
- **FLUX.1 [pro] (API Commercial Top-Tier):** `black-forest-labs/flux-1.1-pro`
- **Google Imagen 3 (Google Photorealism Flagship):** `google/imagen-3`
- **Recraft v3 (Vector & Design Specialist):** `recraft-ai/recraft-v3`
- **SDXL (Custom LoRA / Inpainting Standard):** `stability-ai/sdxl`

### FLUX Parameter Schema & Best Practices

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `prompt` | `string` | *(Required)* | Natural language scene description. Avoid comma salad; use prose. |
| `aspect_ratio` | `string` | `"1:1"` | `"1:1"`, `"16:9"`, `"21:9"`, `"3:2"`, `"2:3"`, `"4:5"`, `"9:16"`, `"9:21"`. |
| `num_inference_steps` | `integer` | `4` (schnell) / `28` (dev) | Schnell requires 4 steps; Dev operates optimally at 25–35 steps. |
| `guidance_scale` | `float` | `3.5` (dev) | Applicable to `flux-dev`. Schnell does not use guidance scale. |
| `output_format` | `string` | `"webp"` | `"webp"`, `"jpg"`, or `"png"`. WebP offers optimal size-to-quality ratio. |
| `output_quality` | `integer` | `85` | 1–100. Set to `95` for print or high-end design assets. |
| `go_fast` | `boolean` | `true` | Enables FP8 quantization for 2x faster generation with imperceptible loss. |
| `megapixels` | `string` | `"1"` | Target resolution (e.g. `"1"` for 1024x1024, `"0.25"` for 512x512). |
| `seed` | `integer` | `null` | Deterministic pseudo-random seed. |

### Production Python Snippet: FLUX.1 [dev] with LoRA Weights
```python
import replicate

output = replicate.run(
    "black-forest-labs/flux-dev",
    input={
        "prompt": "Macro photo of vintage analog synthesizer knobs, studio lighting, matte finish",
        "aspect_ratio": "16:9",
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
        "output_format": "png",
        "output_quality": 95,
        "extra_lora": "https://huggingface.co/owner/lora-name/resolve/main/lora.safetensors",
        "extra_lora_scale": 0.8
    }
)
# Output returns a list of file URLs
print(f"Generated Image: {output[0]}")
```

---

## 5. State-of-the-Art Video Generation

Replicate hosts world-class generative video models supporting Text-to-Video (T2V) and Image-to-Video (I2V).

### Flagship Video Model Identifiers
- **Minimax Video-01 (Flagship Cinematic Physics):** `minimax/video-01`
- **Kling v1.6 Pro (Ultra-Realistic Motion & Hands):** `kling-ai/kling-v1.6-pro`
- **Luma Dream Machine / Ray (Hyper-Dynamic Motion):** `luma/ray`
- **CogVideoX 5B (Open Source Video Standard):** `fofr/cogvideox-5b`

### Video Model Configuration Matrix

| Capability | Model | Duration | Resolution | Key Input Fields |
|---|---|---|---|---|
| **Text-to-Video** | `minimax/video-01` | 6s | 720p / 1080p | `prompt`, `prompt_optimizer` (`true`) |
| **Image-to-Video** | `minimax/video-01` | 6s | 720p / 1080p | `first_frame_image`, `prompt` |
| **Realistic Cinematic** | `kling-ai/kling-v1.6-pro` | 5s / 10s | 1080p | `prompt`, `duration` (`5` or `10`), `cfg_scale` (`0.5`) |
| **Dynamic Camera Motion** | `luma/ray` | 5s | 720p | `prompt`, `loop` (`false`), `aspect_ratio` (`"16:9"`) |

### Production Python Snippet: Image-to-Video with Minimax
```python
import replicate

# Dispatch asynchronous prediction (video takes ~60-120s)
prediction = replicate.predictions.create(
    model="minimax/video-01",
    input={
        "first_frame_image": "https://example.com/start-frame.png",
        "prompt": "Camera pushes forward slowly as atmospheric fog drifts through the forest",
        "prompt_optimizer": True
    }
)

print(f"Prediction initiated: {prediction.id}. Polling status...")
prediction.wait()

if prediction.status == "succeeded":
    print(f"Generated Video URL: {prediction.output}")
else:
    print(f"Failed with error: {prediction.error}")
```

---

## 6. Audio, Speech & Vision Modalities

### Automatic Speech Recognition (Transcription)
- **Model:** `openai/whisper` (Whisper Large v3)
- **Input:**
  ```json
  {
    "audio": "https://example.com/recording.mp3",
    "model": "large-v3",
    "language": "auto",
    "translate": false,
    "temperature": 0.0,
    "transcription": "plain text"
  }
  ```

### Music & Sound FX Synthesis
- **Model:** `meta/musicgen`
- **Input:**
  ```json
  {
    "prompt": "Deep cinematic synthwave bassline with 80s analog drums, 118 BPM",
    "duration": 15,
    "model_version": "stereo-melody-large",
    "output_format": "mp3"
  }
  ```

---

## 7. File Ingestion & Binary Inputs

When passing images, audio, or video files into Replicate models, use one of three sanctioned approaches:

### Approach 1: Public HTTPS URL (Recommended)
Pass any publicly accessible S3, Cloudflare R2, or CDN URL directly in the input field:
```json
{ "image": "https://cdn.yourdomain.com/inputs/portrait.jpg" }
```

### Approach 2: Replicate Files API (`/v1/files`)
For private or local files without hosting infrastructure:
```bash
# Upload local binary file to Replicate
FILE_URL=$(curl -s -X POST "https://api.replicate.com/v1/files" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: image/jpeg" \
  --data-binary "@/path/to/local-image.jpg" | jq -r .urls.get)

# Pass resulting URL into model
curl -s -X POST "https://api.replicate.com/v1/models/black-forest-labs/flux-dev/predictions" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": {"prompt": "Remix this photo", "image": "'"$FILE_URL"'"}}'
```

### Approach 3: Base64 Data URI
Suitable for small icons or thumbnails ($< 5\text{MB}$):
```json
{ "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." }
```

---

## 8. Hardware, Deployments & Cost Controls

### Hardware Tiers & Pricing Context
Replicate bills predictions down to the millisecond based on hardware execution time:
- **CPU:** General utilities, lightweight scripts.
- **Nvidia T4 (16GB VRAM):** Fast audio transcription, classic Stable Diffusion 1.5.
- **Nvidia A40 (48GB VRAM) / A100 (40GB/80GB VRAM):** Standard for FLUX.1, Llama 3.3 70B, and video diffusion.
- **Nvidia H100 (80GB SXM5):** Ultra-fast reasoning and LLM serving.

### Deployments for Zero Cold-Starts
Public models may incur cold boot times (30–60s) if idle. For sub-second production latency, create a **Dedicated Deployment**:
```bash
# Target dedicated deployment endpoint
POST https://api.replicate.com/v1/deployments/{owner}/{deployment_name}/predictions
```

### Cost Guardrails
1. **Prefer `schnell` over `dev` for real-time applications:** FLUX.1 schnell requires only 4 inference steps, resulting in a ~70% cost reduction compared to 28-step Dev.
2. **Cap Token Limits:** Always set `max_tokens` explicitly on open LLMs to avoid runaway loops.
3. **Cancel Stale Predictions:** When a user navigates away, cancel the prediction via `POST /v1/predictions/{id}/cancel` to halt GPU billing immediately.

---

## 9. Error Handling & Status Lifecycles

### HTTP Status Code Semantics
- `200 OK`: Synchronous prediction succeeded (`Prefer: wait`).
- `201 Created`: Asynchronous prediction created and queued.
- `401 Unauthorized`: Invalid or missing `REPLICATE_API_TOKEN`.
- `404 Not Found`: Model or prediction ID does not exist.
- `422 Unprocessable Entity`: Input parameter validation failed (invalid aspect ratio, missing required field). Check `.detail` in the response JSON.
- `429 Too Many Requests`: Rate limit exceeded. Implement exponential backoff jitter.

### Python Error Handling Pattern
```python
import replicate
from replicate.exceptions import ModelError, ReplicateError

try:
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={"prompt": "Studio portrait of an architect", "aspect_ratio": "16:9"}
    )
except ModelError as e:
    # Model runtime exception inside GPU container
    print(f"Model failed: {e}")
except ReplicateError as e:
    # API rate limit, auth, or network failure
    print(f"API Error ({e.status}): {e.title}")
```

---

## 10. Verification & Pre-Flight Checklist

Before deploying any Replicate API pipeline to production:
- [ ] `REPLICATE_API_TOKEN` is injected via environment variables (never committed to git).
- [ ] Model identifier matches the canonical format (`owner/model-name` or `owner/model-name:version-id`).
- [ ] Synchronous jobs include `Prefer: wait=60` header and handle 200 vs 201 statuses.
- [ ] Video jobs ($> 30\text{s}$) implement polling with exponential backoff or signed webhooks.
- [ ] Aspect ratios match exact model enums (e.g. FLUX `"16:9"`, not `"1920x1080"`).
- [ ] Local file inputs are converted to valid HTTPS URLs via `/v1/files` or cloud buckets.
- [ ] Cancellation hooks are wired up for user-aborted client sessions (`/cancel`).
- [ ] Reduced-step or quantized models (`go_fast: true`, `schnell`) are chosen for cost-sensitive workloads.

