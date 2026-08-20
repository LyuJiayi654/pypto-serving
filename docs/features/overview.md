# Feature Overview

PyPTO Serving is a focused inference stack for selected LLMs on Ascend NPUs.
The feature set is intentionally tied to the model executors and PyPTO kernels
available in this repository.

## Current Feature Set

| Feature | Status | Notes |
| --- | --- | --- |
| Ascend NPU backend | Supported | The only serving backend today is `npu`. |
| PyPTO kernels | Supported | Model-specific kernels are loaded from `pypto-lib/`. |
| Offline inference | Supported | Qwen3-14B and DeepSeek V4 entries are available under `examples/model/`. |
| HTTP serving | Supported | OpenAI-compatible completions and chat completions subset. |
| Streaming | Supported | Server-Sent Events for completion and chat streams. |
| Continuous batching | Supported | Scheduler batches active requests across prefill and decode steps. |
| Paged KV cache | Supported | Generic KV pages plus DeepSeek V4 grouped cache pools. |
| Chunked prefill | Supported | Enabled by default. |
| Prefix caching | Qwen path | Enabled by default for Qwen and disabled for DeepSeek V4. |
| MTP speculative decoding | DeepSeek V4 | Enabled with `--speculative-config` or offline `--enable-mtp`. |
| Chrome trace profiling | Supported | HTTP and offline trace paths are available. |
| Compile cache | Supported | Optional and caller-managed. |

## Non-Goals Today

- CPU or GPU serving backends.
- Full OpenAI API parity.
- Full vLLM feature parity.
- Pipeline parallelism.
- General-purpose expert parallelism for standard models.
- Automatic production deployment orchestration.
