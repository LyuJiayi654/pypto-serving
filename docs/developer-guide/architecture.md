# Architecture

PyPTO Serving is organized around a small serving stack:

```text
CLI
  -> FastAPI server
  -> AsyncLLMEngine
  -> Scheduler and KV cache manager
  -> Serving worker process
  -> Model executor
  -> PyPTO kernels on Ascend NPUs
```

## Source Layout

| Path | Responsibility |
| --- | --- |
| `pypto_serving/cli/` | CLI entry point and server startup configuration. |
| `pypto_serving/config/` | Runtime, generation, and parallel configuration. |
| `pypto_serving/serving/` | Engine, scheduler, KV cache, HTTP server, and workers. |
| `pypto_serving/model/` | Model loaders, tokenizers, Qwen, and DeepSeek integrations. |
| `pypto_serving/tools/profile/` | Chrome trace profiling utilities. |
| `examples/model/` | Offline generation entry points. |
| `pypto-lib/` | Model-specific PyPTO kernel sources. |

## Runtime Shape

The API process receives HTTP requests and forwards generation work to the
async engine. The scheduler allocates KV pages, selects requests, and dispatches
prefill or decode work. Worker processes own model executors and device-facing
execution state.

The C++ `platform/` subtree is a separate platform-management layer and is not
in the per-token Python serving hot path.
