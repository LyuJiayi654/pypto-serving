# Parallel Configuration

The `ParallelConfig` object defines how devices are grouped for serving.

## Replica Placement

Replica placement is used by standard models such as Qwen.

```text
devices = dp * tp
replicas = dp
worker_group_size = tp
```

Example:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --devices 0,1,2,3 \
  --dp 2 \
  --tp 2
```

This creates two independently routed replicas. Each replica owns one
two-device tensor-parallel worker group.

## Overlapped Placement

Overlapped placement is used by DeepSeek V4. The DP and EP axes reuse the same
physical worker group.

```bash
pypto-serving \
  --model /path/to/dsv4-flash-w8a8 \
  --devices 0,1,2,3,4,5,6,7 \
  --dp 8 \
  --ep 8 \
  --tp 1
```

This is one model replica with eight physical ranks.

## Validation Rules

- All parallel sizes must be at least 1.
- Pipeline parallel size must be 1.
- Device IDs must not contain duplicates.
- Replica placement does not support expert parallelism.
- Overlapped axes must be singleton or span the full worker group.
- `least_pending_tokens` is the only current data-parallel routing policy.
