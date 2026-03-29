---
name: gemini-imagen
description: "Generate images via Google Nano Banana (Gemini Image API). Use when: user asks to generate, create, or make an image. NOT for: video generation, image analysis/understanding."
---

# gemini-imagen — Google Nano Banana Image Generation

Generate images via Gemini's native image generation API (Nano Banana family).

## Auth

`GOOGLE_API_KEY` environment variable required.

## Usage

```bash
# Basic generation (Nano Banana 2, 1:1, 1 image)
uv run imagen.py generate "a photorealistic lobster astronaut"

# Multiple images, landscape
uv run imagen.py generate "prompt" --count 4 --aspect 16:9

# Nano Banana Pro (4K, Thinking — slow, 1 image only)
uv run imagen.py generate "prompt" --model nano-banana-pro --size 4K

# Custom output dir + JSON output
uv run imagen.py generate "prompt" --out /tmp/images --json
```

## Models

| Alias | Model ID | Notes |
|---|---|---|
| `nano-banana-2` | `gemini-3.1-flash-image-preview` | **Default.** Best all-around. count 1-4. |
| `nano-banana-pro` | `gemini-3-pro-image-preview` | 4K, Thinking, Search grounding. count=1 only. Slow. |
| `nano-banana` | `gemini-2.5-flash-image` | Speed/volume. 1024px only. No --size support. |

## Flags

| Flag | Default | Notes |
|---|---|---|
| `--model` | `nano-banana-2` | Alias or raw model ID |
| `--count` | `1` | 1-4; auto-capped to 1 for nano-banana-pro |
| `--aspect` | `1:1` | `1:1 16:9 9:16 3:2 2:3 4:3 3:4 4:5 5:4 21:9` |
| `--size` | `1K` | `1K 2K 4K` — Gemini 3 models only |
| `--out` | `./out` | Output directory |
| `--json` | off | Print JSON with file paths |

## Gotchas

- **Output is JPEG** (API returns `image/jpeg`). Extension set dynamically from mime type.
- **Latency:** Nano Banana 2 ~10-20s. Nano Banana Pro ~30-60s.
