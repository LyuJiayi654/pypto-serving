# Prerequisites

PyPTO Serving runs close to the hardware stack. Before installing the package,
prepare the host, Python environment, model checkpoint, and NPU runtime.

## Host Environment

- Linux host with Ascend NPUs visible to the user running the process.
- Ascend driver, firmware, and CANN toolkit configured for the target platform.
- Python 3.10 or later.
- Sufficient host memory and disk space for the selected model checkpoint.
- Network access or an internal mirror for downloading model snapshots, unless
  the checkpoints are already present locally.

## Python Environment

The environment must provide packages compatible with the local Ascend runtime:

- PyTorch and, when required by the environment, `torch_npu`.
- PyPTO runtime and kernel framework.
- `transformers` for tokenizer and model config loading.
- `safetensors` for checkpoint loading and DeepSeek V4 conversion.
- `fastapi`, `uvicorn`, `sse-starlette`, and `pydantic` for HTTP serving.

Install PyPTO Serving with `--no-deps` so these environment-specific packages
are not replaced by generic wheels.

## Model Checkpoints

Qwen3-14B expects a local Hugging Face style checkpoint directory containing
`config.json`, tokenizer files, and weight shards.

DeepSeek V4 serving expects a converted W8A8 compressed-tensors checkpoint.
The released DeepSeek V4 Flash checkpoint must be converted before use; see
[DeepSeek V4 Checkpoint Conversion](../models/deepseek-v4-checkpoint-conversion.md).

## Device Requirements

| Model | Offline | HTTP serving | Notes |
| --- | --- | --- | --- |
| Qwen3-14B | 1 or more devices in one TP worker group | 1 device by default, DP replicas supported | TP is model-worker local. |
| DeepSeek V4 Flash W8A8 | Exactly 8 devices | Exactly 8 devices | Requires overlapped attention DP=8 and MoE EP=8. |

## First Checks

Verify that the checkout, Python package, and CLI are available:

```bash
git submodule update --init --recursive
python -m pip install --no-deps -e .
pypto-serving --help
```

Verify that your model path exists before starting a long NPU run:

```bash
test -f /path/to/model/config.json
```
