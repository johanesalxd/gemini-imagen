# gemini-imagen

Generate images via Google's Nano Banana (Gemini Image API).

## Usage

```bash
# Basic generation
mise exec -- uv run imagen.py generate "a photorealistic lobster astronaut"

# Nano Banana Pro (4K, Thinking)
mise exec -- uv run imagen.py generate "prompt" --model nano-banana-pro --size 4K

# Multiple images, landscape
mise exec -- uv run imagen.py generate "prompt" --count 4 --aspect 16:9

# JSON output
mise exec -- uv run imagen.py generate "prompt" --json

# Custom output dir
mise exec -- uv run imagen.py generate "prompt" --out /tmp/images
```

## Models

| Alias | Model ID | Notes |
|---|---|---|
| `nano-banana-2` | `gemini-3.1-flash-image-preview` | Default. Best all-around. |
| `nano-banana-pro` | `gemini-3-pro-image-preview` | 4K, Thinking, Search grounding. count=1 only. |
| `nano-banana` | `gemini-2.5-flash-image` | Speed/volume, 1024px only. |

## Auth

`GOOGLE_API_KEY` in env or `~/clawd/.secrets/vader.env`.
