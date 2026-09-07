# Configuration

PyPTO Serving keeps configuration close to the executable surface: command-line
arguments configure the server and runtime, HTTP request fields configure one
generation, and a small set of environment variables handles integration with
PyPTO, profiling, and local process behavior.

This differs from vLLM's broad configuration surface. vLLM engine, server,
scheduler, hardware, plugin, LoRA, quantization, and multimodal options are not
accepted unless they are documented here or in the
[`pypto-serving`](../cli-reference/pypto-serving.md) reference.

## Precedence

Generation parameters are resolved in this order:

1. HTTP request fields such as `max_tokens`, `temperature`, `top_p`, `top_k`,
   `seed`, `stop`, and `stream`.
2. Server defaults from `--generate-config`.
3. Built-in `GenerateConfig` defaults.

Runtime capacity, model placement, profiling, and HTTP bind settings are process
startup choices. Change them by restarting `pypto-serving`.

## Configuration Map

| Area | Use |
| --- | --- |
| [Runtime Capacity](runtime-capacity.md) | Model path, device placement, parallelism, batching, KV cache, ring sizing, profiling flags. |
| [Environment Variables](env-vars.md) | PyPTO checkout discovery, compile cache directory, worker timeouts, profiling environment, and debug toggles. |
| [CLI Reference](../cli-reference/pypto-serving.md) | Exact argument names, defaults, aliases, and examples. |
| [vLLM Compatibility](../user-guide/vllm-compatibility.md) | HTTP request fields and endpoint compatibility. |

## Configuration Hygiene

- Record the full command line with every benchmark or validation result.
- Keep `--model`, `--platform`, device IDs, parallel sizes, and kernel sources
  fixed when reusing compile cache artifacts.
- Prefer CLI flags over legacy process-wide runtime environment variables when
  both forms exist.
- Keep model-specific constraints in the model guide. DeepSeek V4 is intentionally
  stricter than Qwen because its cache and parallel layout are fixed by the
  kernels.
