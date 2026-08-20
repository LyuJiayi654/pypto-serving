# DeepSeek V4

PyPTO Serving supports DeepSeek V4 Flash through a converted W8A8
compressed-tensors checkpoint and a fixed eight-device NPU topology. The model
uses overlapped attention data parallelism and MoE expert parallelism: the same
eight physical ranks are attention DP=8 and MoE EP=8 ranks.

## Requirements

- A converted W8A8 compressed-tensors checkpoint.
- Exactly eight NPU device IDs.
- `--dp 8 --ep 8 --tp 1` for HTTP serving.
- `--block-size 128`.
- Prefix caching disabled; the server disables it automatically for DeepSeek V4.

See [DeepSeek V4 Checkpoint Conversion](deepseek-v4-checkpoint-conversion.md)
before starting a serving run with the released checkpoint.

## 8-Device Offline Generation

The offline entry uses the same scheduler, worker process, rank-partitioned
cache pools, and MTP acceptance path as HTTP serving, without opening a port.

```bash
PYPTO_RUNTIME_LOG=error \
PTO2_RING_DEP_POOL=131072 \
PTO2_RING_TASK_WINDOW=131072 \
PTO2_RING_HEAP=2147483648 \
PTO2_OP_EXECUTE_TIMEOUT_US=400000000 \
PTO2_STREAM_SYNC_TIMEOUT_MS=440000 \
PTO2_SCHEDULER_TIMEOUT_MS=320000 \
SERVING_WORKER_STEP_TIMEOUT=1800 \
python examples/model/deepseek_v4/npu_generate.py \
  --model-dir /path/to/dsv4-flash-w8a8 \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --max-seq-len 512 \
  --max-new-tokens 20 \
  --enable-mtp
```

Use `--num-prompts N` to exercise continuous batching, or add
`--profile --profile-output /path/to/profile` to capture only the generation
window after model initialization.

## 8-Device DP/EP Serving

Use the quantized checkpoint under `/data/models/dsv4-flash-w8a8` and run with
overlapped attention DP=8 and MoE EP=8 on devices 8-15. Both parallel axes use
the same eight physical ranks, so this is one model replica rather than eight
independent serving replicas:

```bash
PYPTO_RUNTIME_LOG=error \
PTO2_RING_DEP_POOL=131072 \
PTO2_RING_TASK_WINDOW=131072 \
PTO2_RING_HEAP=2147483648 \
PTO2_OP_EXECUTE_TIMEOUT_US=400000000 \
PTO2_STREAM_SYNC_TIMEOUT_MS=440000 \
PTO2_SCHEDULER_TIMEOUT_MS=320000 \
SERVING_WORKER_STEP_TIMEOUT=1800 \
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
  --long-prefill-token-threshold 2048 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --no-enable-prefix-caching \
  --port 8225 \
  --show-startup-logs
```

Each NPU runs one prefill row at a time, so DP=8 admits up to eight prefill
requests in one global step. The vLLM-style `--speculative-config` selects
`method="mtp"`; `num_speculative_tokens` is the maximum number of draft tokens,
and any positive value enables MTP. The
16-row MTP decode tile uses B8S2 for K=1, B4S4 for K=2-3, and B2S8 for
K>=4. K values larger than seven are supported through repeated target
verification chunks. Set `--max-num-seqs` no higher than 64, 32, or 16,
respectively. Non-MTP decode retains B8S1T8. The deprecated
`--num-speculative-tokens K` and `--enable-mtp`
flags remain compatibility aliases; `--enable-mtp` selects K=1.

For repeated launches, set `PYPTO_PROG_BUILD_DIR` to a persistent directory and
add `--use-compile-cache`. The first launch populates a device-specific worker
subdirectory after executable assembly. Later launches reuse the compiled
programs without fingerprint validation, so use the same model configuration,
assigned devices, and kernel sources, and clear the directory after any change.

MTP prefill context, draft token, recurrent hidden state, and acceptance
counters are owned by request ID. MTP prefill and decode share one
worker-resident cache, but each request addresses it with the scheduler-owned
rank-local `ori` block IDs.
The scheduler reserves all K speculative positions before dispatch, including
when a draft sequence crosses a 128-token page boundary.

Before the first decode is prepared, each request owns a stable rank-local
device-state slot and reuse generation. Terminal prefill fills that reserved
slot with the committed tail token, next draft token, tail position, and
committed count. The fused decode kernel
uses `(rank, slot, generation)` to build the next `[tail, draft]` input rows and
sequence metadata before main decode, then updates the same slot after MTP
verification. Host output processing mirrors the state for scheduling and
statistics, but is not an input dependency of the next steady-state decode.
Generation matching prevents a stale queued step from updating a slot after
preemption and reuse.

The seven main-model KV/state pools are allocated during runner preflight as
rank-sharded worker-resident tensors. Prefill and decode pass the same device
handles and address them with scheduler-owned group block IDs; there is no
prefill CPU snapshot or cache handoff. Reassigned pages are cleared with
targeted host-to-device copies before their new owner writes them.

See [DeepSeek V4 Prepacked Weights](deepseek-v4-prepacked-weights.md) for the
optional sidecar that reduces repeated startup work.

## Completion Check

Check server health first:

```bash
curl --noproxy "*" http://127.0.0.1:8225/health
```

Then send a deterministic completion request:

```bash
curl --noproxy "*" -s http://127.0.0.1:8225/v1/completions -H "Content-Type: application/json" -d '{"model":"dsv4-flash-w8a8","prompt":"Huawei is","max_tokens":25,"temperature":0.0}'
```
