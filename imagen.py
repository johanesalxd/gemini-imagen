#!/usr/bin/env python3
"""
gemini-imagen — Generate images via Google Nano Banana (Gemini Image API)

Usage:
    uv run imagen.py generate "a photorealistic lobster astronaut"
    uv run imagen.py generate "prompt" --model nano-banana-pro
    uv run imagen.py generate "prompt" --count 4 --aspect 16:9
    uv run imagen.py generate "prompt" --size 2K --out ./out
    uv run imagen.py generate "prompt" --json

Env:
    GOOGLE_API_KEY — Gemini API key (or set in ~/clawd/.secrets/vader.env)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

MODEL_ALIASES = {
    "nano-banana": "gemini-2.5-flash-image",
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "nano-banana-pro": "gemini-3-pro-image-preview",
    # also accept raw model IDs directly
}

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2


def get_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    vader_env = os.path.expanduser("~/clawd/.secrets/vader.env")
    if os.path.exists(vader_env):
        with open(vader_env) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GOOGLE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"')
    print("ERROR: GOOGLE_API_KEY not found in env or vader.env", file=sys.stderr)
    sys.exit(1)


def resolve_model(model_str: str) -> str:
    return MODEL_ALIASES.get(model_str, model_str)


def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    count: int = 1,
    aspect_ratio: str = "1:1",
    image_size: str | None = None,
    out_dir: str = "./out",
    as_json: bool = False,
) -> None:
    key = get_api_key()

    # Lazy import
    from google import genai
    from google.genai import types

    resolved_model = resolve_model(model)

    # Nano Banana Pro only supports 1 image at a time
    if resolved_model == "gemini-3-pro-image-preview" and count > 1:
        print(
            "WARNING: nano-banana-pro only supports count=1. Setting count=1.",
            file=sys.stderr,
        )
        count = 1

    # image_size only supported on Gemini 3 models
    size_supported = resolved_model in (
        "gemini-3.1-flash-image-preview",
        "gemini-3-pro-image-preview",
    )
    if image_size and not size_supported:
        print(
            f"WARNING: --size not supported for {resolved_model}. Ignoring.",
            file=sys.stderr,
        )
        image_size = None

    image_config_kwargs: dict = {
        "number_of_images": count,
        "aspect_ratio": aspect_ratio,
    }
    if image_size:
        image_config_kwargs["image_size"] = image_size

    config = types.GenerateContentConfig(
        image_config=types.ImageConfig(**image_config_kwargs),
    )

    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=resolved_model,
            contents=prompt,
            config=config,
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract images from response
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    saved_files = []

    for i, candidate in enumerate(response.candidates):
        for part in candidate.content.parts:
            if part.inline_data is not None:
                mime_type = part.inline_data.mime_type  # e.g. "image/png"
                ext = mime_type.split("/")[-1] if "/" in mime_type else "png"
                filename = f"imagen-{timestamp}-{i + 1}.{ext}"
                filepath = out_path / filename
                filepath.write_bytes(part.inline_data.data)
                saved_files.append(str(filepath))

    if not saved_files:
        print("ERROR: No images returned in response.", file=sys.stderr)
        sys.exit(1)

    if as_json:
        print(
            json.dumps(
                {
                    "prompt": prompt,
                    "model": resolved_model,
                    "count": len(saved_files),
                    "aspect_ratio": aspect_ratio,
                    "image_size": image_size,
                    "files": saved_files,
                },
                indent=2,
            )
        )
        return

    # Default human-readable output
    print(f"Prompt:  {prompt}")
    print(f"Model:   {resolved_model}")
    print(f"Aspect:  {aspect_ratio}" + (f"  Size: {image_size}" if image_size else ""))
    print()
    print(f"=== GENERATED {len(saved_files)} IMAGE(S) ===")
    for f in saved_files:
        print(f"  {f}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate images via Nano Banana (Gemini Image API)"
    )
    subparsers = parser.add_subparsers(dest="command")

    gen = subparsers.add_parser("generate", help="Generate image(s) from a text prompt")
    gen.add_argument("prompt", type=str, help="Text prompt for image generation")
    gen.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Model alias or ID. Aliases: nano-banana, nano-banana-2 (default), nano-banana-pro",
    )
    gen.add_argument(
        "--count", type=int, default=1, help="Number of images (1-4; 1 for pro)"
    )
    gen.add_argument(
        "--aspect",
        type=str,
        default="1:1",
        help="Aspect ratio: 1:1 (default), 16:9, 9:16, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 21:9",
    )
    gen.add_argument(
        "--size",
        type=str,
        default=None,
        help="Image size: 1K (default), 2K, 4K — Gemini 3 models only",
    )
    gen.add_argument(
        "--out", type=str, default="./out", help="Output directory (default: ./out)"
    )
    gen.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output JSON with file paths",
    )

    args = parser.parse_args()

    if args.command == "generate":
        generate(
            prompt=args.prompt,
            model=args.model,
            count=args.count,
            aspect_ratio=args.aspect,
            image_size=args.size,
            out_dir=args.out,
            as_json=args.as_json,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
