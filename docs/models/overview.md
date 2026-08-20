# Model Overview

PyPTO Serving is model-specific. Each supported model family has a loader,
runtime configuration, NPU executor, runner, and PyPTO kernel path.

| Model | Status | Main path | Device topology |
| --- | --- | --- | --- |
| Qwen3-14B | Supported | Offline and HTTP serving | Single device by default; Qwen supports replica DP online and one TP worker group. |
| DeepSeek V4 Flash W8A8 | Supported | Offline and HTTP serving | Exactly eight devices with overlapped attention DP=8 and MoE EP=8. |

## Model Selection

The server detects DeepSeek V4 from `config.json` metadata. Any other supported
checkpoint path is treated as the Qwen path.

## Checkpoint Expectations

- Qwen3-14B uses a local Hugging Face style checkpoint.
- DeepSeek V4 uses a converted W8A8 compressed-tensors checkpoint.

For new model families, see [Add a Model](../developer-guide/add-a-model.md).
