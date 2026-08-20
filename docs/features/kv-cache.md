# KV Cache

PyPTO Serving uses paged KV cache allocation for active requests. The scheduler
assigns pages to requests and releases them when generation finishes.

## Generic Cache

For standard models, the runtime uses a generic page layout controlled by:

- `--block-size`
- `--max-model-len`
- `--max-num-seqs`
- `--npu-memory-utilization`

## DeepSeek V4 Grouped Cache

DeepSeek V4 uses model-specific grouped cache pools. The cache groups follow
the decode layout and compressed state requirements of the DeepSeek V4 kernels.
The server validates the model topology and runtime limits before startup.

## Prefix Cache

Prefix caching can reuse previously computed prompt prefixes for supported
models. It is enabled by default for Qwen and disabled for DeepSeek V4.
