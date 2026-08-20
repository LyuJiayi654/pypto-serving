# Prefix Caching

Prefix caching reuses KV cache state for repeated prompt prefixes when the
model path supports it.

## Qwen

Prefix caching is enabled by default for Qwen serving:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --enable-prefix-caching
```

Disable it with:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --no-enable-prefix-caching
```

## DeepSeek V4

DeepSeek V4 serving disables prefix caching. Its grouped cache and MTP state
layout are model-specific and are not compatible with the generic prefix-cache
path.
