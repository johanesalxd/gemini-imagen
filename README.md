# gemini-imagen

Generate images via Google's Nano Banana (Gemini Image API).

Nano Banana is Google's native image generation family built on Gemini. This tool wraps the API into a simple CLI with model aliases, aspect ratio control, and batch generation support.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Python 3.13
- `GOOGLE_API_KEY` set in your environment

## Installation

```bash
git clone https://github.com/johanesalxd/gemini-imagen.git
cd gemini-imagen
uv sync
```

## Usage

```bash
# Basic generation (Nano Banana 2, 1:1, 1 image)
uv run imagen.py generate "a photorealistic lobster astronaut"

# Multiple images, landscape
uv run imagen.py generate "prompt" --count 4 --aspect 16:9

# Nano Banana Pro (4K, Thinking — slow, 1 image only)
uv run imagen.py generate "prompt" --model nano-banana-pro --size 4K

# Custom output dir + JSON output
uv run imagen.py generate "prompt" --out ./images --json
```

## Models

| Alias | Model ID | Notes |
|---|---|---|
| `nano-banana-2` | `gemini-3.1-flash-image-preview` | **Default.** Best all-around. count 1-4. |
| `nano-banana-pro` | `gemini-3-pro-image-preview` | 4K, Thinking, Search grounding. count=1 only. |
| `nano-banana` | `gemini-2.5-flash-image` | Speed/volume. 1024px only. |

Raw model IDs also accepted (pass-through).

## Flags

| Flag | Default | Notes |
|---|---|---|
| `--model` | `nano-banana-2` | Alias or raw model ID |
| `--count` | `1` | 1-4; auto-capped to 1 for nano-banana-pro |
| `--aspect` | `1:1` | `1:1 16:9 9:16 3:2 2:3 4:3 3:4 4:5 5:4 21:9` |
| `--size` | `1K` | `1K 2K 4K` — Gemini 3 models only |
| `--out` | `./out` | Output directory |
| `--json` | off | Print JSON with file paths |

## Agent Skill

This repo includes a `SKILL.md` for use with AI coding agents (Claude Code, Cursor, Windsurf, OpenCode, and others).

### Install via skills CLI

```bash
npx skills add johanesalxd/gemini-imagen
```

### Manual install

```bash
# Copy to your agent's skills directory
cp SKILL.md ~/.claude/skills/gemini-imagen/SKILL.md         # Claude Code
cp SKILL.md .cursor/skills/gemini-imagen/SKILL.md           # Cursor
cp SKILL.md .opencode/skills/gemini-imagen/SKILL.md         # OpenCode
```

Once installed, your agent will load this skill when you ask it to generate images.

## License

MIT
