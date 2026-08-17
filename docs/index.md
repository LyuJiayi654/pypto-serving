# PyPTO Serving

PyPTO Serving is a local inference serving stack for running Qwen3-14B and
DeepSeek V4 generation with PyPTO kernels on Ascend NPUs. It includes an
installable Python package, model executor integrations, CLI entry points, and
an OpenAI-compatible HTTP API.

## Features

- **Model support**: Qwen3-14B and DeepSeek V4 Flash W8A8
- **OpenAI-compatible API**: `/v1/completions`, `/v1/chat/completions`, streaming
- **Profiling**: Built-in Chrome Trace Event Format profiling
- **Offline generation**: One-shot generation without HTTP server

## Quick Links

- [Installation](get-started/installation.md) — set up the environment
- [Quickstart](get-started/quickstart.md) — run your first generation
- [Parallel Serving](user-guide/parallel.md) — DP/TP/EP configuration
- [Profiling](user-guide/profile.md) — performance tracing
- [CLI Reference](user-guide/cli-reference.md) — command-line arguments reference
- [Qwen3](models/qwen.md) — Qwen3-14B model notes
- [DeepSeek V4](models/deepseek-v4.md) — DeepSeek V4 Flash W8A8 model notes
