#!/usr/bin/env python3
"""
Replicate Multi-Modal CLI Utility

A versatile command-line interface for testing Replicate API endpoints across
Large Language Models, Image Generation, Video Generation, and File Ingestion.

Usage:
    python3 replicate_cli.py check
    python3 replicate_cli.py model <owner/name>
    python3 replicate_cli.py llm --model deepseek-ai/deepseek-r1 --prompt "Explain Raft"
    python3 replicate_cli.py image --model black-forest-labs/flux-schnell --prompt "Cyberpunk city" --aspect-ratio 16:9
    python3 replicate_cli.py upload <local-file-path>
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def get_headers(prefer_wait: int = None, content_type: str = "application/json"):
    if not REPLICATE_API_TOKEN:
        print("Error: REPLICATE_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("Run: export REPLICATE_API_TOKEN=\"r8_...\"", file=sys.stderr)
        sys.exit(1)
        
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "User-Agent": "ReplicateAgentCLI/1.0"
    }
    if content_type:
        headers["Content-Type"] = content_type
    if prefer_wait is not None:
        headers["Prefer"] = f"wait={prefer_wait}"
    return headers

def check_auth():
    """Validates the token against Replicate's API."""
    print("Checking Replicate API connection...")
    req = urllib.request.Request("https://api.replicate.com/v1/models/black-forest-labs/flux-schnell", headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"✅ Success! Authenticated. Verified access to model: {data.get('owner')}/{data.get('name')}")
    except urllib.error.HTTPError as e:
        print(f"❌ Authentication check failed: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)

def inspect_model(model_id: str):
    """Fetches schema information for any model."""
    url = f"https://api.replicate.com/v1/models/{model_id}"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"=== Model: {data.get('owner')}/{data.get('name')} ===")
            print(f"Description: {data.get('description')}")
            print(f"Run Count:   {data.get('run_count'):,}")
            print(f"Visibility:  {data.get('visibility')}")
            latest_version = data.get("latest_version", {})
            schema = latest_version.get("openapi_schema", {}).get("components", {}).get("schemas", {}).get("Input", {})
            properties = schema.get("properties", {})
            print("\nAvailable Input Parameters:")
            for param, info in properties.items():
                req_mark = "(REQUIRED)" if param in schema.get("required", []) else ""
                default_val = f"[Default: {info.get('default')}]" if "default" in info else ""
                print(f"  • {param} ({info.get('type')}) {req_mark} {default_val}")
                if "description" in info:
                    print(f"    {info.get('description')[:80]}...")
    except urllib.error.HTTPError as e:
        print(f"Error inspecting model: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)

def run_image(prompt: str, model: str, aspect_ratio: str, output_format: str):
    """Dispatches a synchronous image generation request."""
    url = f"https://api.replicate.com/v1/models/{model}/predictions"
    payload = {
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "go_fast": True
        }
    }
    print(f"Dispatching image prediction to '{model}' (aspect ratio: {aspect_ratio})...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers(prefer_wait=60)
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status")
            if status == "succeeded":
                output = data.get("output", [])
                print(f"✅ Image Generated Successfully!")
                for idx, item in enumerate(output if isinstance(output, list) else [output]):
                    print(f"  URL [{idx+1}]: {item}")
            else:
                print(f"Prediction status: {status} (ID: {data.get('id')})")
                print("Output may be available asynchronously.")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"Execution Error: HTTP {e.code} - {err_body}", file=sys.stderr)

def run_llm(prompt: str, model: str, system_prompt: str, max_tokens: int, temperature: float):
    """Executes an LLM prediction across OpenAI, Anthropic, Google, or open-weights models."""
    url = f"https://api.replicate.com/v1/models/{model}/predictions"
    inp = {
        "prompt": prompt,
        "temperature": temperature
    }

    # Model family adaptations
    if "openai" in model.lower():
        inp["max_completion_tokens"] = max_tokens
        if system_prompt:
            inp["system_prompt"] = system_prompt
    elif "google" in model.lower() or "gemini" in model.lower():
        inp["max_output_tokens"] = max_tokens
        if system_prompt:
            inp["system_instruction"] = system_prompt
    else:
        inp["max_tokens"] = max_tokens
        if system_prompt:
            inp["system_prompt"] = system_prompt

    payload = {"input": inp}
        
    print(f"Dispatching query to {model}...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers(prefer_wait=60)
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status")
            if status == "succeeded":
                output = data.get("output", "")
                text = "".join(output) if isinstance(output, list) else str(output)
                print("\n=== Model Response ===")
                print(text)
                print("======================")
            else:
                print(f"Prediction Status: {status} (ID: {data.get('id')})")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"Execution Error: HTTP {e.code} - {err_body}", file=sys.stderr)

def upload_file(file_path: str):
    """Uploads a local file to Replicate's /v1/files endpoint."""
    if not os.path.exists(file_path):
        print(f"Error: Local file '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    print(f"Uploading '{filename}' ({file_size:,} bytes) to Replicate Files API...")
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    # Determine Content-Type
    ext = os.path.splitext(filename)[1].lower()
    content_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".mp4": "video/mp4"
    }
    ctype = content_types.get(ext, "application/octet-stream")
    
    url = "https://api.replicate.com/v1/files"
    req = urllib.request.Request(url, data=file_bytes, headers=get_headers(content_type=ctype))
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            public_url = data.get("urls", {}).get("get")
            print(f"✅ Upload Complete!")
            print(f"  File ID: {data.get('id')}")
            print(f"  Input URL: {public_url}")
            print(f"  (Pass this URL into any model input field)")
    except urllib.error.HTTPError as e:
        print(f"Upload Error: HTTP {e.code} - {e.read().decode()}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Replicate API CLI Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    subparsers.add_parser("check", help="Verify REPLICATE_API_TOKEN authorization")

    # model
    model_parser = subparsers.add_parser("model", help="Inspect a model schema")
    model_parser.add_argument("model_id", help="Format: owner/model-name (e.g. black-forest-labs/flux-schnell)")

    # image
    img_parser = subparsers.add_parser("image", help="Generate an image")
    img_parser.add_argument("--prompt", required=True, help="Image prompt")
    img_parser.add_argument("--model", default="black-forest-labs/flux-schnell", help="Model ID")
    img_parser.add_argument("--aspect-ratio", default="16:9", help="1:1, 16:9, 21:9, etc.")
    img_parser.add_argument("--output-format", default="webp", help="webp, png, or jpg")

    # llm
    llm_parser = subparsers.add_parser("llm", help="Run an LLM prompt")
    llm_parser.add_argument("--prompt", required=True, help="Prompt text")
    llm_parser.add_argument("--model", default="deepseek-ai/deepseek-r1", help="LLM Model ID")
    llm_parser.add_argument("--system-prompt", default="", help="Optional system directive")
    llm_parser.add_argument("--max-tokens", type=int, default=1024, help="Max tokens")
    llm_parser.add_argument("--temperature", type=float, default=0.6, help="Temperature")

    # upload
    upload_parser = subparsers.add_parser("upload", help="Upload a local file to Replicate")
    upload_parser.add_argument("file_path", help="Local file path")

    args = parser.parse_args()

    if args.command == "check":
        check_auth()
    elif args.command == "model":
        inspect_model(args.model_id)
    elif args.command == "image":
        run_image(args.prompt, args.model, args.aspect_ratio, args.output_format)
    elif args.command == "llm":
        run_llm(args.prompt, args.model, args.system_prompt, args.max_tokens, args.temperature)
    elif args.command == "upload":
        upload_file(args.file_path)

if __name__ == "__main__":
    main()

