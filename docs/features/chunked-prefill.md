# Chunked Prefill

Chunked prefill breaks long prompts into scheduler-visible chunks so a long
prefill does not monopolize the engine indefinitely.

## Server Controls

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --enable-chunked-prefill \
  --long-prefill-token-threshold 2048
```

Chunked prefill is enabled by default. Use `--no-enable-chunked-prefill` to
disable it when validating behavior.

## DeepSeek V4

DeepSeek V4 has stricter model-specific constraints. The offline entry requires
`--long-prefill-token-threshold 128`; HTTP serving commonly uses a larger
threshold with the model-specific cache layout.
