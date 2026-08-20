# Python API

The public Python API is intentionally small. Import stable entry points from
`pypto_serving`.

```python
from pypto_serving import (
    AsyncLLMEngine,
    EngineConfig,
    GenerateConfig,
    KVCacheGroupSpec,
    KVCacheSpec,
    LLMEngine,
    ModelLoader,
    ParallelConfig,
    ReplicaEngineCore,
    RuntimeConfig,
)
```

## Main Objects

| Object | Purpose |
| --- | --- |
| `GenerateConfig` | User-facing generation options. |
| `RuntimeConfig` | Runtime limits, dtype metadata, cache settings, and memory utilization. |
| `ParallelConfig` | Device topology for serving placement. |
| `LLMEngine` | Synchronous local engine used by Qwen offline generation. |
| `AsyncLLMEngine` | Async serving engine used by HTTP serving and DeepSeek V4 offline generation. |
| `EngineConfig` | Full async engine startup configuration. |
| `ModelLoader` | Model loading entry point. |
| `KVCacheSpec` | Generic KV cache page description. |
| `KVCacheGroupSpec` | Model-specific grouped cache family description. |

## Stability

The public package exports are the supported import surface. Internal modules
under `pypto_serving.serving`, `pypto_serving.model`, and `pypto_serving.tools`
may change as model integrations evolve.
