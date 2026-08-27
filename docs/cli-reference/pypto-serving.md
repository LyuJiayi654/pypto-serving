# `pypto-serving`

`pypto-serving` is the main command for offline generation and HTTP serving. It starts the OpenAI-compatible server by default. Passing one or more `--prompt` arguments switches to offline generate mode and exits after the scheduled requests finish.

## Offline Generate Mode

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --generate-config '{"max_new_tokens":32,"temperature":0.0}'
```

Repeat `--prompt` to schedule multiple offline requests through the same serving engine.

## HTTP Server Mode

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --host 0.0.0.0 \
  --port 8000 \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512
```

## Model, Backend, and Device Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--model PATH` | Required | Model directory. |
| `--served-model-name NAME` | Directory name | Model name returned by the API. |
| `--backend npu` | `npu` | Inference backend. `npu` is the only supported backend. |
| `--platform NAME` | `a2a3` | Target NPU platform. |
| `--device ID` | `0` | Single default device ID. |
| `--devices LIST` | unset | Comma-separated device IDs for multi-device placement. |
| `--dtype DTYPE` | `bfloat16` | Weight data type. |
| `--kv-cache-dtype DTYPE` | `bfloat16` | KV cache data type. `auto` follows `--dtype`. |
| `--use-compile-cache` | off | Reuse compiled kernels from `PYPTO_PROG_BUILD_DIR`. |
| `--show-startup-logs` | off | Show model loading and kernel compilation logs. |

## Parallelism Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--data-parallel-size`, `--dp` | `1` | Data-parallel size. |
| `--tensor-parallel-size`, `--tp` | `1` | Tensor-parallel group size. |
| `--expert-parallel-size`, `--ep` | `1` | Expert-parallel size for supported overlapped placement. |
| `--data-parallel-routing` | `least_pending_tokens` | DP request routing policy. |

For Qwen-style replica placement, the number of device IDs must equal `dp * tp`. DeepSeek V4 uses overlapped placement and requires exactly eight devices with `--dp 8 --ep 8 --tp 1`.

## Runtime Capacity Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--max-model-len` | `1024` | Maximum prompt plus generated token length. |
| `--block-size` | `128` | KV cache block size. |
| `--npu-memory-utilization` | `0.90` | Fraction of NPU memory available to the server. |
| `--max-num-seqs` | `16` | Maximum concurrent requests in serving mode. |
| `--max-num-batched-tokens` | `4096` | Maximum scheduled tokens per iteration. |
| `--long-prefill-token-threshold` | `2048` | Chunked-prefill threshold in serving mode. |
| `--ring-dep-pool` | runtime default | Simpler ring dependency-edge pool capacity. A single integer broadcasts to all scope-depth rings; a comma-separated four-integer list sizes rings 0..3, with `0` leaving that ring at its default. |
| `--ring-task-window` | runtime default | Simpler ring task-slot window capacity. Accepts the same single integer or four-entry list form as `--ring-dep-pool`. |
| `--ring-heap` | runtime default | Simpler per-ring output-heap size in bytes. Accepts the same single integer or four-entry list form as `--ring-dep-pool`. |

## Serving Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | HTTP bind host. |
| `--port` | `8000` | HTTP bind port. |

## Generation Controls

Server defaults and offline generate mode use `--generate-config`. HTTP request fields override the server defaults.

| Field or option | Meaning |
| --- | --- |
| `max_tokens` / `max_new_tokens` | Maximum generated tokens. |
| `temperature` | Sampling temperature. |
| `top_p` | Nucleus sampling cutoff. |
| `top_k` | Top-k sampling cutoff. |
| `stop` | Stop strings. |
| `stream` | Stream text deltas. |
| `ignore_eos` | Generate-mode EOS handling. |

The HTTP completion path ignores EOS for completion requests and uses standard generation behavior for chat requests.

## Feature Flags

| Argument | Default | Description |
| --- | --- | --- |
| `--enable-prefix-caching` / `--no-enable-prefix-caching` | enabled | Enable or disable prefix caching for supported paths. |
| `--enable-chunked-prefill` / `--no-enable-chunked-prefill` | enabled | Enable or disable chunked prefill. |
| `--speculative-config JSON` | unset | DeepSeek V4 MTP config. |
| `--num-speculative-tokens K` | unset | Deprecated DeepSeek V4 MTP alias. |

## Profiling Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--profile` | off | Enable `/start_profile` and `/stop_profile`, or profile the offline generation window. |
| `--profile-output PATH` | `./profile_out` | Profile output directory or JSON path. |
| `--profile-level LEVELS` | `e2e,kernel` | Comma-separated profile levels. |

## Help Output

Use the installed command's help output as the source of truth for the exact arguments available in the active package:

```bash
pypto-serving --help
```
