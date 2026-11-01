# TypeScript & Node.js SDK Recipes

Production patterns for Replicate using the official `replicate` npm package in modern JavaScript, TypeScript, and Next.js environments.

---

## 1. Setup & Initialization

```bash
npm install replicate
```

```typescript
import Replicate from "replicate";

// Automatically loads process.env.REPLICATE_API_TOKEN
const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

---

## 2. Recipe: Synchronous Image Generation (`replicate.run`)

```typescript
import Replicate from "replicate";

const replicate = new Replicate();

export async function generateHeroAsset(prompt: string): Promise<string> {
  const output = (await replicate.run("black-forest-labs/flux-schnell", {
    input: {
      prompt,
      aspect_ratio: "16:9",
      output_format: "webp",
      output_quality: 90,
      go_fast: true,
    },
  })) as string[];

  // Output contains an array of direct image URLs
  return output[0];
}
```

---

## 3. Recipe: Streaming LLM in Next.js App Router (Server-Sent Events)

Modern Next.js 14/15 route handler streaming tokens directly to the client browser.

```typescript
// app/api/chat/route.ts
import { NextRequest } from "next/server";
import Replicate from "replicate";

const replicate = new Replicate();

export async function POST(req: NextRequest) {
  const { prompt, model = "openai/gpt-4o" } = await req.json();

  // Model-specific payload tailoring
  const inputPayload: Record<string, any> = { prompt };
  if (model.includes("openai")) {
    inputPayload.max_completion_tokens = 2048;
    inputPayload.temperature = 0.7;
  } else if (model.includes("claude") || model.includes("anthropic")) {
    inputPayload.max_tokens = 4096;
    inputPayload.effort = "medium";
  } else if (model.includes("gemini") || model.includes("google")) {
    inputPayload.max_output_tokens = 4096;
  } else {
    inputPayload.max_tokens = 2048;
    inputPayload.temperature = 0.6;
  }

  const stream = await replicate.stream(model, { input: inputPayload });

  // Convert the Replicate SSE stream to a standard Web ReadableStream
  const responseStream = new ReadableStream({
    async start(controller) {
      for await (const event of stream) {
        // Encode each token string into binary Uint8Array
        controller.enqueue(new TextEncoder().encode(event.toString()));
      }
      controller.close();
    },
  });

  return new Response(responseStream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-cache",
    },
  });
}
```

---

## 4. Recipe: Asynchronous Prediction Creation & Webhook Dispatch

```typescript
import Replicate from "replicate";

const replicate = new Replicate();

export async function dispatchVideoJob(prompt: string, webhookUrl: string) {
  const prediction = await replicate.predictions.create({
    model: "minimax/video-01",
    input: {
      prompt,
      prompt_optimizer: true,
    },
    webhook: webhookUrl,
    webhook_events_filter: ["completed"],
  });

  console.log(`Video prediction created: ${prediction.id}`);
  return prediction;
}
```

---

## 5. Recipe: Local File Uploads via Node.js Buffer

To pass a local image buffer into a model without external cloud storage:

```typescript
import { readFile } from "node:fs/promises";
import Replicate from "replicate";

const replicate = new Replicate();

export async function transcribeLocalAudio(filePath: string) {
  const fileBuffer = await readFile(filePath);

  // The SDK automatically handles Buffer instances by uploading to /v1/files
  const output = (await replicate.run("openai/whisper", {
    input: {
      audio: fileBuffer,
      model: "large-v3",
      transcription: "plain text",
    },
  })) as { transcription: string };

  return output.transcription;
}
```

---

## 6. Recipe: Typed Error Handling

```typescript
import Replicate from "replicate";

const replicate = new Replicate();

try {
  const output = await replicate.run("black-forest-labs/flux-dev", {
    input: { prompt: "Architectural sketch", num_inference_steps: 28 },
  });
} catch (error: any) {
  if (error.status === 422) {
    console.error("Validation error: Invalid model input parameter", error.detail);
  } else if (error.status === 401) {
    console.error("Unauthorized: Verify REPLICATE_API_TOKEN environment variable.");
  } else {
    console.error(`Replicate execution failure (${error.status}):`, error.message);
  }
}
```

