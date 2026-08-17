# CLI Reference

## pypto-serving

Start PyPTO Serving with an OpenAI-compatible API.

```bash
pypto-serving --model /path/to/model [OPTIONS]
```

### Model

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--model` | `str` | *required* | Path to the model directory. |
| `--served-model-name` | `str` | `None` | Model name used in the API. Defaults to the model directory name. |

### Backend and Device

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--backend` | `str` | `"npu"` | Inference backend. Choices: `npu`. |
| `--platform` | `str` | `"a2a3"` | NPU platform. |
| `--use-compile-cache` | flag | `False` | Reuse compiled kernels across launches. Each kernel is written to `<pypto_build_dir>/<name>` and reloaded on the next launch, skipping the JIT and the device-binary assembly. NOTE: there is no fingerprinting, so reuse the same build dir only for the same config and kernel sources. |
| `--device` | `int` | `0` | NPU device ID. |
| `--devices` | `str` | `None` | Comma-separated NPU device IDs for the requested parallel placement. |
| `--data-parallel-size`, `--dp` | `int` | `1` | Data-parallel size. DeepSeek V4 uses model-local attention DP. |
| `--tensor-parallel-size`, `--tp` | `int` | `1` | Tensor-parallel group size. |
| `--expert-parallel-size`, `--ep` | `int` | `1` | Expert-parallel group size. |
| `--data-parallel-routing` | `str` | `"least_pending_tokens"` | Data-parallel request routing policy. Choices: `least_pending_tokens`. |

### Data Type

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--dtype` | `str` | `"bfloat16"` | Weight data type. |
| `--kv-cache-dtype` | `str` | `"bfloat16"` | KV cache data type. `"auto"` follows `--dtype`. |

### Runtime

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--max-model-len` | `int` | `1024` | Maximum sequence length (prompt + generated tokens). |
| `--block-size` | `int` | `128` | KV cache block size. |
| `--npu-memory-utilization` | `float` | `0.90` | Fraction of total NPU HBM the server is allowed to use (weights + activations + KV cache). |

### Generation

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--temperature` | `float` | `0.0` | Sampling temperature. |
| `--top-p` | `float` | `1.0` | Nucleus sampling probability. |
| `--top-k` | `int` | `None` | Top-k sampling cutoff (disabled by default). |
| `--enable-mtp`, `--no-enable-mtp` | flag | `None` | Deprecated alias for DeepSeek V4 MTP with one draft token. |
| `--num-speculative-tokens` | `int` | `None` | Maximum DeepSeek V4 MTP draft tokens per iteration. Any positive value enables MTP; 0 disables it. |
| `--speculative-config` | `JSON` | `None` | Speculative decoding configuration as JSON. DeepSeek V4 supports `method='mtp'` and a positive `num_speculative_tokens` value. |

### Serving

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--host` | `str` | `"0.0.0.0"` | Host to bind the serving server. |
| `--port` | `int` | `8000` | Port for the serving server. |
| `--max-num-seqs` | `int` | `16` | Maximum concurrent requests in serving mode. |
| `--max-num-batched-tokens` | `int` | `4096` | Maximum tokens scheduled per iteration. |
| `--long-prefill-token-threshold` | `int` | `2048` | Chunked prefill threshold in serving mode. |
| `--enable-prefix-caching`, `--no-enable-prefix-caching` | flag | `True` | Enable prefix caching. Use `--no-enable-prefix-caching` to disable. |
| `--enable-chunked-prefill`, `--no-enable-chunked-prefill` | flag | `True` | Enable chunked prefill. Use `--no-enable-chunked-prefill` to disable. |

### Profiling

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--profile` | flag | `False` | Enable on-demand SA profiling through `POST /start_profile` and `POST /stop_profile`. |
| `--profile-output` | `str` | `None` | Profile output directory or `.json` path (default: `./profile_out`). |
| `--profile-level` | `str` | `None` | Comma-separated profile levels: `e2e`, `kernel`, or `verbose` (default: `e2e,kernel`). |

### Misc

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--show-startup-logs` | flag | `False` | Show model loading and kernel compilation logs. Startup logs are suppressed by default. |

---

## pypto-prepack-deepseek-v4

Prepack DeepSeek V4 hidden-layer weights once so serving can mmap the final rank-stacked layout on later starts.

```bash
pypto-prepack-deepseek-v4 <model_dir> [OPTIONS]
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `model_dir` | `Path` | *required* | DeepSeek V4 W8A8 checkpoint directory. |
| `--ranks` | `int` | `8` | Rank count for the packed layout. |
| `--output` | `Path` | `None` | Output sidecar path; defaults to the serving auto-discovery path. |
| `--force` | flag | `False` | Replace an existing sidecar. |
