# Python SDK Recipes & Production Patterns

Production-ready implementation patterns for Replicate using the official `replicate` Python package.

---

## 1. Setup & Client Initialization

```bash
pip install replicate
```

```python
import os
import replicate

# Client automatically reads os.environ["REPLICATE_API_TOKEN"]
client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
```

---

## 2. Recipe: Synchronous Blocking Run (`replicate.run`)

Best suited for fast text generation or low-step image models (FLUX.1 schnell).

```python
import replicate

def generate_architectural_render(prompt: str) -> str:
    """Generates an image via FLUX.1 schnell and returns the asset URL."""
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "output_format": "webp",
            "output_quality": 90,
            "go_fast": True
        }
    )
    # output is a list of replicate.helpers.FileOutput objects or URLs
    return str(output[0])

if __name__ == "__main__":
    url = generate_architectural_render("A cantilevered glass studio over a redwood canyon at dusk")
    print(f"Generated asset: {url}")
```

---

## 3. Recipe: Real-Time Token Streaming (`replicate.stream`)

Streams generated tokens instantly to stdout or a WebSocket connection across OpenAI, Anthropic, Google, and open-weights reasoning models.

```python
import replicate

def stream_frontier_llm(model_id: str, prompt: str, **kwargs):
    """Streams token chunks from any frontier model on Replicate."""
    input_payload = {"prompt": prompt, **kwargs}
    
    print(f"--- [STREAMING FROM {model_id}] ---")
    for event in replicate.stream(model_id, input=input_payload):
        # event is a ServerSentEvent object
        print(str(event), end="", flush=True)
    print("\n--- [STREAM COMPLETE] ---\n")

if __name__ == "__main__":
    # 1. Stream Claude 3.5 Sonnet with extended thinking effort
    stream_frontier_llm(
        "anthropic/claude-3.5-sonnet",
        "Explain quantum entanglement with an analogy.",
        effort="medium",
        max_tokens=2048
    )

    # 2. Stream OpenAI GPT-4o
    stream_frontier_llm(
        "openai/gpt-4o",
        "Summarize the Paxos consensus algorithm in bullet points.",
        max_completion_tokens=1024,
        temperature=0.3
    )

    # 3. Stream Google Gemini 2.0 Flash
    stream_frontier_llm(
        "google/gemini-2.0-flash",
        "Write a Python script to verify TLS certificate expiry.",
        max_output_tokens=1024
    )
```

if __name__ == "__main__":
    stream_reasoning_model("Explain how Raft prevents split-brain scenarios during network partitions.")
```

---

## 4. Recipe: Non-Blocking Predictions & Polling (Video Generation)

Essential for long-running video models (Minimax, Kling) taking 60–180 seconds.

```python
import time
import replicate

def create_video_job(prompt: str, first_frame_url: str = None) -> str:
    """Dispatches a Minimax video generation job and polls until complete."""
    input_payload = {
        "prompt": prompt,
        "prompt_optimizer": True
    }
    if first_frame_url:
        input_payload["first_frame_image"] = first_frame_url

    # Create prediction without blocking
    prediction = replicate.predictions.create(
        model="minimax/video-01",
        input=input_payload
    )
    print(f"Prediction initiated: {prediction.id} (Status: {prediction.status})")

    # Poll with exponential backoff
    backoff = 2
    while prediction.status not in ["succeeded", "failed", "canceled"]:
        time.sleep(backoff)
        prediction.reload()
        print(f"[{time.strftime('%X')}] Status: {prediction.status}")
        backoff = min(backoff * 1.25, 10)

    if prediction.status == "succeeded":
        return prediction.output
    else:
        raise RuntimeError(f"Prediction failed: {prediction.error}")
```

---

## 5. Recipe: Native Asyncio Pipeline (`replicate.async_run`)

Runs parallel multimodal generations concurrently without blocking the async event loop.

```python
import asyncio
import replicate

async def generate_multimodal_package(concept: str):
    """Generates an image and a marketing description concurrently."""
    
    # Run both jobs in parallel across GPUs
    image_task = replicate.async_run(
        "black-forest-labs/flux-schnell",
        input={"prompt": f"Hero packaging photograph for {concept}, studio lighting", "aspect_ratio": "1:1"}
    )
    copy_task = replicate.async_run(
        "meta/meta-llama-3.3-70b-instruct",
        input={"prompt": f"Write a 2-sentence punchy marketing tagline for {concept}", "temperature": 0.7}
    )

    image_output, copy_output = await asyncio.gather(image_task, copy_task)
    
    return {
        "image_url": str(image_output[0]),
        "copy": "".join(copy_output).strip()
    }

if __name__ == "__main__":
    result = asyncio.run(generate_multimodal_package("ergonomic mechanical split keyboard in milled brass"))
    print(result)
```

---

## 6. Recipe: Local File Uploads via Python File Handlers

The Replicate Python SDK automatically uploads local open file handles to `/v1/files` behind the scenes!

```python
import replicate

def transcribe_local_recording(audio_filepath: str) -> str:
    """Passes a local binary file directly into Whisper."""
    with open(audio_filepath, "rb") as file_handle:
        output = replicate.run(
            "openai/whisper",
            input={
                "audio": file_handle,
                "model": "large-v3",
                "transcription": "plain text"
            }
        )
    return output["transcription"]
```

---

## 7. Recipe: Robust Exception & Error Handling

```python
import replicate
from replicate.exceptions import ModelError, ReplicateError

try:
    output = replicate.run(
        "black-forest-labs/flux-dev",
        input={"prompt": "Mountain vista", "num_inference_steps": 28}
    )
except ModelError as e:
    # Triggered if code inside the Cog container crashes (e.g. OOM, bad weights)
    print(f"Container runtime failure: {e}")
except ReplicateError as e:
    # Triggered on 401 Unauthorized, 422 Bad Parameter, or 429 Rate Limit
    print(f"Replicate API Error [Code {e.status}]: {e.title} - {e.detail}")
except Exception as e:
    print(f"Network or client error: {e}")
```

