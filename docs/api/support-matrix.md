# Support Matrix

This matrix describes the current documented support surface. Anything not
listed here should be treated as unsupported until the code and docs say
otherwise.

## Models

| Model | Checkpoint | Offline | HTTP serving | Notes |
| --- | --- | --- | --- | --- |
| Qwen3-14B | Hugging Face style local checkpoint | Supported | Supported | Default model path for quickstart. |
| DeepSeek V4 Flash | Converted W8A8 compressed-tensors checkpoint | Supported | Supported | Original Hybrid FP8/MXFP4 checkpoint must be converted. |

## Backends and Platforms

| Area | Support |
| --- | --- |
| Backend | `npu` only. |
| Platforms | `a2a3` is the default; offline entries also expose simulator names where supported. |
| CPU serving | Not supported. |
| GPU serving | Not supported. |

## Parallelism

| Mode | Qwen3-14B | DeepSeek V4 |
| --- | --- | --- |
| Single-device serving | Supported | Not supported. |
| Data-parallel serving replicas | Supported through replica placement | Not supported as independent replicas. |
| Tensor-parallel worker group | Supported for Qwen offline and serving placement | HTTP requires `--tp 1`. |
| Expert parallelism | Not supported | Required as overlapped `--ep 8`. |
| Pipeline parallelism | Not supported | Not supported. |

## Serving API

| Endpoint | Status |
| --- | --- |
| `/health` | Supported. |
| `/v1/models` | Supported. |
| `/v1/completions` | Supported subset. |
| `/v1/chat/completions` | Supported subset. |
| `/start_profile`, `/stop_profile` | Supported only when launched with `--profile`. |
| Embeddings, rerank, pooling, tool calls, guided decoding | Not supported. |

## Features

| Feature | Qwen3-14B | DeepSeek V4 |
| --- | --- | --- |
| Continuous batching | Supported in serving | Supported in serving and offline batch path. |
| Chunked prefill | Supported | Supported with model-specific constraints. |
| Prefix caching | Supported | Disabled. |
| MTP speculative decoding | Not supported | Supported. |
| Compile cache | Supported | Supported with the same caller-managed cache contract. |
| Prepacked weights | Not applicable | Optional sidecar supported. |
| Chrome trace profiling | Supported | Supported. |
