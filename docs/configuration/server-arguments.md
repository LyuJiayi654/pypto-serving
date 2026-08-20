# Server Arguments

`pypto-serving` starts the HTTP server and builds an `EngineConfig` from CLI
arguments. This page groups the commonly used arguments by purpose.

## Model

| Argument | Default | Description |
| --- | --- | --- |
| `--model PATH` | Required | Model directory. |
| `--served-model-name NAME` | Directory name | Model name returned by the API. |

## Backend and Devices

| Argument | Default | Description |
| --- | --- | --- |
| `--backend npu` | `npu` | Inference backend. |
| `--platform NAME` | `a2a3` | Target NPU platform. |
| `--device ID` | `0` | Single default device ID. |
| `--devices LIST` | unset | Comma-separated device IDs for multi-device placement. |
| `--use-compile-cache` | off | Reuse compiled kernels from `PYPTO_PROG_BUILD_DIR`. |

## Parallelism

| Argument | Default | Description |
| --- | --- | --- |
| `--data-parallel-size`, `--dp` | `1` | Data-parallel size. |
| `--tensor-parallel-size`, `--tp` | `1` | Tensor-parallel group size. |
| `--expert-parallel-size`, `--ep` | `1` | Expert-parallel size for supported overlapped placement. |
| `--data-parallel-routing` | `least_pending_tokens` | DP request routing policy. |

## Runtime Capacity

| Argument | Default | Description |
| --- | --- | --- |
| `--max-model-len` | `1024` | Maximum prompt plus generated token length. |
| `--block-size` | `128` | KV cache block size. |
| `--npu-memory-utilization` | `0.90` | Fraction of NPU memory available to the server. |
| `--max-num-seqs` | `16` | Maximum concurrent requests. |
| `--max-num-batched-tokens` | `4096` | Maximum scheduled tokens per iteration. |
| `--long-prefill-token-threshold` | `2048` | Chunked-prefill threshold. |

## Generation Defaults

| Argument | Default | Description |
| --- | --- | --- |
| `--temperature` | `0.0` | Default sampling temperature. |
| `--top-p` | `1.0` | Default nucleus sampling probability. |
| `--top-k` | disabled | Default top-k cutoff. |

Per-request API fields override these defaults.

## Feature Flags

| Argument | Default | Description |
| --- | --- | --- |
| `--enable-prefix-caching` / `--no-enable-prefix-caching` | enabled | Enable or disable prefix caching. |
| `--enable-chunked-prefill` / `--no-enable-chunked-prefill` | enabled | Enable or disable chunked prefill. |
| `--speculative-config JSON` | unset | DeepSeek V4 MTP config. |
| `--num-speculative-tokens K` | unset | Deprecated DeepSeek V4 MTP alias. |
| `--enable-mtp` | unset | Deprecated DeepSeek V4 MTP alias selecting one draft token. |

## Profiling and Server

| Argument | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Bind host. |
| `--port` | `8000` | Bind port. |
| `--profile` | off | Enable `/start_profile` and `/stop_profile`. |
| `--profile-output PATH` | `./profile_out` | Profile output directory or JSON path. |
| `--profile-level LEVELS` | `e2e,kernel` | Comma-separated profile levels. |
| `--show-startup-logs` | off | Show model loading and kernel compilation logs. |
