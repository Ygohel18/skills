# Replicate Model Catalog & Configuration Reference

An exhaustive parameter dictionary and configuration reference for premier AI models hosted on Replicate across Frontier Proprietary LLMs (OpenAI, Anthropic, Google), Open-Weights Foundation & Reasoning Models, Flagship Image Generation, and Video Synthesis.

---

## 1. Frontier Proprietary LLMs (OpenAI, Anthropic, Google)

Replicate provides managed access to the world's leading frontier proprietary models through its unified prediction lifecycle, streaming SSE, and webhook infrastructure.

---

### 1.1 OpenAI Family (`openai/gpt-4o`, `openai/gpt-4o-mini`, `openai/o1`)

#### Models:
- **`openai/gpt-4o`**: Flagship omni-multimodal model with high-speed intelligence across text and vision.
- **`openai/gpt-4o-mini`**: Cost-efficient, high-throughput model for lightweight tasks.
- **`openai/o1`**: Advanced reasoning model trained with reinforcement learning for complex multi-step reasoning.

#### Parameters:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | `string` | *(Required)* | Text prompt to send to the model (mutually exclusive with `messages`). |
| `messages` | `array` | `null` | Structured conversation history `[{"role": "user", "content": "..."}]`. |
| `system_prompt` | `string` | `"You are a helpful assistant."` | Directs tone, constraints, and instructions. |
| `image_input` | `array` / `string` | `null` | URL or array of image URLs for vision analysis. |
| `max_completion_tokens` | `integer` | `4096` | Upper bound for generated tokens. |
| `temperature` | `float` | `1.0` | Sampling randomness (`0.0` to `2.0`). For `o1`, use default `1.0`. |
| `top_p` | `float` | `1.0` | Nucleus sampling probability mass. |
| `frequency_penalty` | `float` | `0.0` | Penalizes token frequency (-2.0 to 2.0). |
| `presence_penalty` | `float` | `0.0` | Penalizes token recurrence (-2.0 to 2.0). |

#### Payload Example:
```json
{
  "input": {
    "prompt": "Analyze this system architecture diagram and identify single points of failure.",
    "system_prompt": "You are a principal distributed systems architect.",
    "image_input": "https://cdn.domain.com/assets/infra-diagram.png",
    "max_completion_tokens": 2048,
    "temperature": 0.2
  }
}
```

---

### 1.2 Anthropic Claude Family (`anthropic/claude-3.5-sonnet`, `anthropic/claude-3.5-haiku`, `anthropic/claude-3-opus`)

#### Models:
- **`anthropic/claude-3.5-sonnet`**: The industry benchmark for code generation, visual reasoning, and agentic workflows.
- **`anthropic/claude-3.5-haiku`**: Lightning-fast, cost-effective model with near-instant time-to-first-token.
- **`anthropic/claude-3-opus`**: Deep reasoning model for nuanced writing and strategic analysis.

#### Parameters:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | `string` | *(Required)* | The input prompt or instruction. |
| `system_prompt` | `string` | `""` | High-level system directive. |
| `max_tokens` | `integer` | `8192` | Output limit (up to 8192 tokens). |
| `effort` | `string` | `"low"` | Extended reasoning depth: `"none"`, `"low"`, `"medium"`, `"high"`, `"max"`. |
| `image` | `string URL` | `null` | Image URL or data URI for vision understanding. |
| `max_image_resolution` | `float` | `0.5` | Max image resolution in megapixels (0.001 to 2.0). |

#### Payload Example:
```json
{
  "input": {
    "prompt": "Refactor this asynchronous event bus in TypeScript to eliminate race conditions.",
    "system_prompt": "You are an expert TypeScript engineer. Output code with strict types.",
    "effort": "high",
    "max_tokens": 4096
  }
}
```

---

### 1.3 Google Gemini Family (`google/gemini-2.0-flash`, `google/gemini-1.5-pro`, `google/gemini-1.5-flash`)

#### Models:
- **`google/gemini-2.0-flash`**: Google's next-gen multimodal speed champion with native tool calling and high reasoning speed.
- **`google/gemini-1.5-pro`**: 2-million-token context window capable of ingesting whole codebases, books, and hour-long videos.
- **`google/gemini-1.5-flash`**: High-volume, low-latency multimodal processing.

#### Parameters:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | `string` | *(Required)* | The query or instruction. |
| `system_instruction` | `string` | `""` | System-level instructions guiding model behavior. |
| `images` | `array of URLs` | `[]` | Array of image URLs (up to 10 images). |
| `videos` | `array of URLs` | `[]` | Array of video URLs for native video understanding. |
| `audio` | `string URL` | `null` | Audio file URL for direct audio comprehension. |
| `temperature` | `float` | `1.0` | Controls response randomness (0.0 to 2.0). |
| `top_p` | `float` | `0.95` | Nucleus sampling probability mass. |
| `max_output_tokens` | `integer` | `8192` | Maximum generated tokens (up to 65535). |
| `thinking_level` | `string` | `"low"` | For hybrid reasoning: `"none"`, `"low"`, `"medium"`, `"high"`. |
| `fps` | `float` | `1.0` | Frames per second for video ingestion (0.1 to 60.0). |

#### Payload Example:
```json
{
  "input": {
    "prompt": "Provide a timestamped breakdown of key events in this demonstration video.",
    "system_instruction": "You are a video analyst. Output bulleted markdown timestamps.",
    "videos": ["https://cdn.domain.com/recordings/demo-walkthrough.mp4"],
    "fps": 1.0,
    "max_output_tokens": 2048
  }
}
```

---

## 2. Open-Weights Foundation & Reasoning Models

### 2.1 DeepSeek-R1 (`deepseek-ai/deepseek-r1`)
Flagship open-weights reasoning model with state-of-the-art chain-of-thought mathematical and coding performance.

- **Model Identifier:** `deepseek-ai/deepseek-r1`
- **Default Hardware:** Nvidia 8x H100
- **Supported Parameters:**
  - `prompt` (*string, required*): The user inquiry or problem statement.
  - `system_prompt` (*string, optional*): System-level directives.
  - `max_tokens` (*integer, default: 2048*): Maximum generated tokens (up to 8192).
  - `temperature` (*float, default: 0.6*): Recommended range 0.5–0.7 for reasoning tasks.
  - `top_p` (*float, default: 0.95*): Nucleus sampling probability threshold.
  - `presence_penalty` (*float, default: 0.0*): Range: -2.0 to 2.0.
  - `frequency_penalty` (*float, default: 0.0*): Range: -2.0 to 2.0.

```json
{
  "input": {
    "prompt": "Derive the backpropagation equations for a multi-head self-attention layer.",
    "system_prompt": "You are a machine learning researcher. Show detailed tensor mathematics.",
    "max_tokens": 4096,
    "temperature": 0.5,
    "top_p": 0.95
  }
}
```

---

### 2.2 Meta Llama 3.3 70B Instruct (`meta/meta-llama-3.3-70b-instruct`)
Meta's premier open language model offering capabilities comparable to top proprietary models across multilingual reasoning and code.

- **Model Identifier:** `meta/meta-llama-3.3-70b-instruct`
- **Supported Parameters:**
  - `prompt` (*string, required*): Main dialog text.
  - `system_prompt` (*string, optional*): System guidelines.
  - `max_tokens` (*integer, default: 1024*): Maximum tokens to generate (up to 8192).
  - `temperature` (*float, default: 0.7*): Diversity control (0.0 to 2.0).
  - `top_p` (*float, default: 0.9*): Probability mass threshold.
  - `min_tokens` (*integer, default: 0*): Minimum generation length.
  - `stop_sequences` (*string, optional*): Comma-separated list of stop tokens.

```json
{
  "input": {
    "prompt": "Write a Rust implementation of a lock-free ring buffer.",
    "system_prompt": "Produce production-grade code with error handling and zero comments.",
    "max_tokens": 2048,
    "temperature": 0.2
  }
}
```

---

### 2.3 Qwen 2.5 72B Instruct (`qwen/qwen-2.5-72b-instruct`)
Alibaba's flagship foundation model, renowned for elite coding, mathematics, and complex structured JSON output generation.

- **Model Identifier:** `qwen/qwen-2.5-72b-instruct`
- **Supported Parameters:**
  - `prompt` (*string, required*): The prompt string.
  - `max_tokens` (*integer, default: 1024*): Generation limit.
  - `temperature` (*float, default: 0.7*): Sampling temperature.
  - `repetition_penalty` (*float, default: 1.05*): Prevents repetitive phrases.

---

## 3. Flagship Image Generation

### 3.1 FLUX.1 [schnell] (`black-forest-labs/flux-schnell`)
Ultra-low-latency 4-step latent rectified flow model. Ideal for real-time web applications.

- **Model Identifier:** `black-forest-labs/flux-schnell`
- **Cost / Speed:** ~1.0 second per image on Nvidia A100.
- **Supported Parameters:**
  - `prompt` (*string, required*): Scene description.
  - `aspect_ratio` (*string, default: "1:1"*):
    - Valid enums: `"1:1"`, `"16:9"`, `"21:9"`, `"3:2"`, `"2:3"`, `"4:5"`, `"5:4"`, `"9:16"`, `"9:21"`.
  - `num_inference_steps` (*integer, default: 4*): Fixed range 1 to 4 steps.
  - `output_format` (*string, default: "webp"*): `"webp"`, `"jpg"`, `"png"`.
  - `output_quality` (*integer, default: 80*): 1 to 100.
  - `go_fast` (*boolean, default: true*): Enables FP8 optimization.
  - `seed` (*integer, optional*): Deterministic seed.

```json
{
  "input": {
    "prompt": "An isometric cutaway 3D architectural diagram of a solar-powered research station on Mars, blueprint grid lines, clean industrial design",
    "aspect_ratio": "16:9",
    "output_format": "webp",
    "output_quality": 90,
    "go_fast": true
  }
}
```

---

### 3.2 FLUX.1 [dev] (`black-forest-labs/flux-dev`)
Guidance-distilled 12-billion parameter model producing photorealistic details, accurate typography, and complex compositions.

- **Model Identifier:** `black-forest-labs/flux-dev`
- **Supported Parameters:**
  - `prompt` (*string, required*): Natural language scene.
  - `aspect_ratio` (*string, default: "1:1"*): Standard ratio strings.
  - `guidance_scale` (*float, default: 3.5*): Optimal range 2.5–4.5.
  - `num_inference_steps` (*integer, default: 28*): Range 1 to 50 steps.
  - `image` (*string URL, optional*): Input image for image-to-image or inpainting.
  - `prompt_strength` (*float, default: 0.8*): Image-to-image conditioning strength.
  - `extra_lora` (*string URL, optional*): Hugging Face or public URL to `.safetensors` LoRA.
  - `extra_lora_scale` (*float, default: 1.0*): Weight of external LoRA (-1.0 to 2.0).

---

### 3.3 Google Imagen 3 (`google/imagen-3`)
Google's premier photorealistic image generation model with exceptional detail rendering, rich lighting, and text generation accuracy.

- **Model Identifier:** `google/imagen-3`
- **Supported Parameters:**
  - `prompt` (*string, required*): Scene description.
  - `aspect_ratio` (*string, default: "1:1"*): `"1:1"`, `"16:9"`, `"9:16"`, `"4:3"`, `"3:4"`.
  - `output_format` (*string, default: "jpg"*): `"jpg"`, `"png"`.
  - `safety_filter_level` (*string, default: "block_medium_and_above"*): Safety threshold.

---

### 3.4 Recraft v3 (`recraft-ai/recraft-v3`)
Specialized model for vector art, icon design, typography rendering, and UI brand graphics.

- **Model Identifier:** `recraft-ai/recraft-v3`
- **Supported Parameters:**
  - `prompt` (*string, required*): Description.
  - `style` (*string, default: "any"*): `"any"`, `"realistic_image"`, `"digital_illustration"`, `"vector_illustration"`, `"icon"`.
  - `size` (*string, default: "1024x1024"*): Dimensions.

---

### 3.5 Stability SDXL (`stability-ai/sdxl`)
The open-source foundation standard for custom community LoRAs, ControlNet, and structured inpainting.

- **Model Identifier:** `stability-ai/sdxl`
- **Supported Parameters:**
  - `prompt` (*string, required*): Positive prompt.
  - `negative_prompt` (*string, optional*): Negative conditioning tags.
  - `width` / `height` (*integer, default: 1024*): Dimension tokens.
  - `scheduler` (*string, default: "K_EULER"*): Sampling scheduler.
  - `lora_weights` (*string URL, optional*): Custom fine-tune weights.

---

## 4. High-Fidelity Video Generation

### 4.1 Minimax Video-01 (`minimax/video-01`)
Cinematic video synthesis engine with superior fluid dynamics, motion coherence, and photorealism.

- **Model Identifier:** `minimax/video-01`
- **Generation Time:** ~90–150 seconds.
- **Supported Parameters:**
  - `prompt` (*string, required*): Detailed scene and camera motion prompt.
  - `first_frame_image` (*string URL, optional*): Image input for Image-to-Video.
  - `prompt_optimizer` (*boolean, default: true*): LLM prompt expansion module.

```json
{
  "input": {
    "first_frame_image": "https://cdn.domain.com/assets/initial-frame.png",
    "prompt": "Camera executes a low-angle tracking push through neon-lit streets with cinematic rain reflections",
    "prompt_optimizer": true
  }
}
```

---

### 4.2 Kling v1.6 Pro (`kling-ai/kling-v1.6-pro`)
State-of-the-art Chinese video model with outstanding anatomy consistency and realistic human physics.

- **Model Identifier:** `kling-ai/kling-v1.6-pro`
- **Supported Parameters:**
  - `prompt` (*string, required*): Cinematic description.
  - `duration` (*integer, default: 5*): Value must be either `5` or `10` seconds.
  - `aspect_ratio` (*string, default: "16:9"*): `"16:9"`, `"9:16"`, `"1:1"`.
  - `cfg_scale` (*float, default: 0.5*): Guidance adherence (0.0 to 1.0).
  - `camera_control` (*object, optional*): Explicit pan, tilt, zoom coordinates.

---

### 4.3 Luma Ray / Dream Machine (`luma/ray`)
Hyper-dynamic 3D camera sweeps and physical lighting simulations.

- **Model Identifier:** `luma/ray`
- **Supported Parameters:**
  - `prompt` (*string, required*): Scene prompt.
  - `aspect_ratio` (*string, default: "16:9"*): `"16:9"`, `"9:16"`, `"4:3"`, `"3:4"`.
  - `loop` (*boolean, default: false*): Generates seamless looping animations.

---

## 5. Audio & Multimodal Perception

### 5.1 OpenAI Whisper Large v3 (`openai/whisper`)
Universal automatic speech recognition and translation across 99+ languages with timestamp generation.

- **Model Identifier:** `openai/whisper`
- **Supported Parameters:**
  - `audio` (*string URL, required*): URL to audio file (mp3, wav, m4a, flac).
  - `model` (*string, default: "large-v3"*): `"large-v3"`, `"base"`, `"small"`.
  - `transcription` (*string, default: "plain text"*): `"plain text"`, `"srt"`, `"vtt"`, `"verbose_json"`.
  - `translate` (*boolean, default: false*): Translates foreign speech to English.
  - `language` (*string, default: "auto"*): ISO language code or auto-detection.

---

### 5.2 Meta MusicGen (`meta/musicgen`)
Conditional music generation from textual prompts or harmonic melody guidance.

- **Model Identifier:** `meta/musicgen`
- **Supported Parameters:**
  - `prompt` (*string, required*): Musical genre, instruments, and mood.
  - `duration` (*integer, default: 15*): Seconds of audio (up to 30s).
  - `model_version` (*string, default: "stereo-melody-large"*): Quality tier.
  - `output_format` (*string, default: "mp3"*): `"mp3"` or `"wav"`.
