# Offline Inference

Offline inference runs a local generation entry point without opening an HTTP
port. Use it for model validation, kernel checks, profiling a single workload,
or running batch generation from a shell.

## Qwen3-14B

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 32
```

Useful options:

| Option | Purpose |
| --- | --- |
| `--devices 0,1 --tp 2` | Use one tensor-parallel worker group. |
| `--num-prompts N` | Replicate the prompt and call batched generation. |
| `--stream` | Print text deltas as they arrive. |
| `--profile` | Print timing and kernel summary at the end. |
| `--profile-verbose` | Print per-layer and per-step timing details. |
| `--no-enable-prefix-caching` | Disable prefix caching in the offline KV cache manager. |

## DeepSeek V4

DeepSeek V4 offline inference requires the converted W8A8 checkpoint and
exactly eight devices:

```bash
python examples/model/deepseek_v4/npu_generate.py \
  --model-dir /path/to/dsv4-flash-w8a8 \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --max-seq-len 512 \
  --max-new-tokens 32
```

Add `--enable-mtp` to enable one-token MTP speculative decoding in the offline
entry. Use `--profile --profile-output /path/to/profile` to capture a trace for
the generation window.

## Output

Offline entries print generated text, token IDs, finish reason, and a concise
throughput summary. If startup fails before generation, check the model path,
NPU visibility, CANN environment, and PyPTO kernel checkout first.
