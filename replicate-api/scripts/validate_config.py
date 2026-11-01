#!/usr/bin/env python3
"""
Replicate Input Configuration Pre-Flight Validator

Validates model input dictionaries against known schemas and constraints before
dispatching requests, preventing unprocessable entity (HTTP 422) errors.

Usage:
    python3 validate_config.py --model black-forest-labs/flux-schnell --input '{"prompt": "Photo", "aspect_ratio": "16:9"}'
    python3 validate_config.py --file payload.json
"""

import sys
import json
import argparse

FLUX_ASPECT_RATIOS = {"1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "9:16", "9:21"}
FLUX_FORMATS = {"webp", "jpg", "png"}
KLING_DURATIONS = {5, 10}

def validate(model: str, input_data: dict) -> list[str]:
    """Returns a list of validation error strings. Empty list indicates valid config."""
    errors = []

    # General prompt check
    if "prompt" not in input_data and "whisper" not in model:
        errors.append("Missing required field: 'prompt'.")

    # FLUX.1 family
    if "flux" in model.lower():
        if "aspect_ratio" in input_data:
            ratio = input_data["aspect_ratio"]
            if ratio not in FLUX_ASPECT_RATIOS:
                errors.append(f"Invalid 'aspect_ratio': '{ratio}'. Must be one of: {sorted(list(FLUX_ASPECT_RATIOS))}")
        
        if "output_format" in input_data:
            fmt = input_data["output_format"].lower()
            if fmt not in FLUX_FORMATS:
                errors.append(f"Invalid 'output_format': '{fmt}'. Must be one of: {sorted(list(FLUX_FORMATS))}")

        if "schnell" in model.lower():
            if "guidance_scale" in input_data:
                errors.append("Model 'flux-schnell' does not support 'guidance_scale'. Use 'flux-dev' instead.")
            if "num_inference_steps" in input_data:
                steps = input_data["num_inference_steps"]
                if not (1 <= steps <= 4):
                    errors.append(f"For 'flux-schnell', 'num_inference_steps' must be between 1 and 4 (received: {steps}).")

        if "dev" in model.lower():
            if "num_inference_steps" in input_data:
                steps = input_data["num_inference_steps"]
                if not (1 <= steps <= 50):
                    errors.append(f"For 'flux-dev', 'num_inference_steps' must be between 1 and 50 (received: {steps}).")
            if "guidance_scale" in input_data:
                scale = input_data["guidance_scale"]
                if not (1.0 <= scale <= 10.0):
                    errors.append(f"'guidance_scale' must be between 1.0 and 10.0 (received: {scale}).")

    # Kling Video
    if "kling" in model.lower():
        if "duration" in input_data:
            duration = input_data["duration"]
            if duration not in KLING_DURATIONS:
                errors.append(f"For Kling video models, 'duration' must be 5 or 10 seconds (received: {duration}).")

    # OpenAI Models
    if "openai" in model.lower() and "whisper" not in model.lower():
        if "temperature" in input_data:
            temp = input_data["temperature"]
            if not (0.0 <= temp <= 2.0):
                errors.append(f"OpenAI 'temperature' must be between 0.0 and 2.0 (received: {temp}).")
        if "max_completion_tokens" in input_data:
            tokens = input_data["max_completion_tokens"]
            if not (1 <= tokens <= 16384):
                errors.append(f"OpenAI 'max_completion_tokens' must be between 1 and 16384 (received: {tokens}).")

    # Anthropic Claude Models
    if "anthropic" in model.lower() or "claude" in model.lower():
        if "effort" in input_data:
            effort = input_data["effort"]
            valid_efforts = {"none", "low", "medium", "high", "max"}
            if effort not in valid_efforts:
                errors.append(f"Anthropic reasoning 'effort' must be one of: {sorted(list(valid_efforts))} (received: '{effort}').")
        if "max_tokens" in input_data:
            tokens = input_data["max_tokens"]
            if not (1 <= tokens <= 64000):
                errors.append(f"Anthropic 'max_tokens' must be between 1 and 64000 (received: {tokens}).")

    # Google Gemini & Imagen Models
    if "google" in model.lower() or "gemini" in model.lower():
        if "imagen" in model.lower():
            if "aspect_ratio" in input_data:
                valid_imagen_ratios = {"1:1", "16:9", "9:16", "4:3", "3:4"}
                if input_data["aspect_ratio"] not in valid_imagen_ratios:
                    errors.append(f"Google Imagen 3 'aspect_ratio' must be one of: {sorted(list(valid_imagen_ratios))}")
        else:
            if "thinking_level" in input_data:
                valid_thinking = {"none", "low", "medium", "high"}
                if input_data["thinking_level"] not in valid_thinking:
                    errors.append(f"Gemini 'thinking_level' must be one of: {sorted(list(valid_thinking))}")
            if "max_output_tokens" in input_data:
                tokens = input_data["max_output_tokens"]
                if not (1 <= tokens <= 65535):
                    errors.append(f"Gemini 'max_output_tokens' must be between 1 and 65535 (received: {tokens}).")

    # Open-Weights LLM Parameters (DeepSeek, Llama, Qwen, Mixtral)
    if any(k in model.lower() for k in ["llama", "deepseek", "qwen", "mixtral"]):
        if "temperature" in input_data:
            temp = input_data["temperature"]
            if not (0.0 <= temp <= 2.0):
                errors.append(f"'temperature' must be between 0.0 and 2.0 (received: {temp}).")
        if "max_tokens" in input_data:
            tokens = input_data["max_tokens"]
            if not (1 <= tokens <= 16384):
                errors.append(f"'max_tokens' must be between 1 and 16384 (received: {tokens}).")

    # Whisper
    if "whisper" in model.lower():
        if "audio" not in input_data:
            errors.append("Model 'whisper' requires an 'audio' URL or file descriptor input.")

    return errors

def main():
    parser = argparse.ArgumentParser(description="Replicate Input Config Validator")
    parser.add_argument("--model", help="Model identifier (e.g. black-forest-labs/flux-schnell)")
    parser.add_argument("--input", help="JSON string representing the input payload")
    parser.add_argument("--file", help="Path to JSON file containing {model, input}")

    args = parser.parse_args()

    model = args.model
    input_data = {}

    if args.file:
        with open(args.file, "r") as f:
            data = json.load(f)
            model = model or data.get("model")
            input_data = data.get("input", data)
    elif args.input:
        input_data = json.loads(args.input)
    else:
        parser.print_help()
        sys.exit(1)

    if not model:
        print("Error: Model name must be provided via --model or inside the JSON file.", file=sys.stderr)
        sys.exit(1)

    print(f"Validating payload for model: '{model}'...")
    errors = validate(model, input_data)

    if errors:
        print(f"❌ Validation Failed with {len(errors)} error(s):")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("✅ Validation Passed! Input payload is structurally sound and ready for inference.")

if __name__ == "__main__":
    main()

