# Parallelism and Scaling

PyPTO Serving supports two placement modes: replica placement for standard
models and overlapped placement for DeepSeek V4. Single-device serving remains
the default.

## Replica Placement

Replica placement is used by Qwen. Data parallelism creates independent
serving replicas. Tensor parallelism passes one device group to the PyPTO L3
distributed worker for each replica.

The number of devices must equal `dp * tp`.

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --devices 0,1 \
  --dp 2 \
  --tp 1 \
  --max-model-len 512 \
  --port 8899
```

The server routes requests across replicas using `least_pending_tokens`.

## Tensor Parallel Offline Runs

The Qwen offline entry can run one tensor-parallel worker group:

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1 \
  --tp 2 \
  --max-seq-len 512 \
  --max-new-tokens 16
```

Offline `npu_generate.py` intentionally rejects `--dp > 1`; launch separate
offline jobs if data-parallel offline generation is needed.

## DeepSeek V4 Overlapped Placement

DeepSeek V4 uses a model-local overlapped placement. Its attention DP ranks and
MoE EP ranks reuse the same eight physical devices. This is one model replica,
not eight independent replicas.

```bash
pypto-serving \
  --model /path/to/dsv4-flash-w8a8 \
  --served-model-name dsv4-flash-w8a8 \
  --backend npu \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --dp 8 \
  --ep 8 \
  --tp 1 \
  --block-size 128 \
  --max-model-len 512 \
  --max-num-seqs 32 \
  --max-num-batched-tokens 512 \
  --port 8225
```

## Current Limits

- Pipeline parallelism is not supported.
- General-purpose expert parallel placement is not supported for standard
  models.
- Only `least_pending_tokens` is supported for data-parallel request routing.
- DeepSeek V4 requires exactly eight devices and `--dp 8 --ep 8 --tp 1`.
