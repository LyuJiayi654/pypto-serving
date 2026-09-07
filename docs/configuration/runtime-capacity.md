# Runtime Capacity

Runtime capacity decides which requests can be admitted, how much work can be
scheduled in one engine iteration, and how device memory is split between model
state and KV cache.

For exact flags and defaults, use the
[`pypto-serving`](../cli-reference/pypto-serving.md) CLI reference. This page
explains how the main groups of options fit together.

## Model and Device Placement

| Option | Purpose |
| --- | --- |
| `--model` | Local model directory. |
| `--served-model-name` | Model name returned from `/v1/models` and generation responses. |
| `--backend` | Runtime backend. The documented value is `npu`. |
| `--platform` | Target Ascend platform name. |
| `--device` | Single NPU device ID. |
| `--devices` | Comma-separated device IDs for multi-device placement. |
| `--dtype` | Weight dtype used by the model path. |
| `--kv-cache-dtype` | KV cache dtype. `auto` follows `--dtype`. |

Qwen-style placement uses `dp * tp` device IDs. Each data-parallel group is an
independent serving replica, and tensor-parallel groups are passed to the model
executor for one replica.

DeepSeek V4 uses overlapped placement. It requires the same eight physical
devices to act as attention DP=8 and MoE EP=8 ranks:

```bash
--devices 0,1,2,3,4,5,6,7 --dp 8 --ep 8 --tp 1
```

## Scheduler Capacity

| Option | Meaning |
| --- | --- |
| `--max-model-len` | Maximum prompt plus generated token length. |
| `--block-size` | KV cache block size. DeepSeek V4 requires `128`. |
| `--npu-memory-utilization` | Fraction of NPU memory available to the server. |
| `--max-num-seqs` | Maximum active requests in serving mode. |
| `--max-num-batched-tokens` | Maximum tokens scheduled in one engine iteration. |
| `--long-prefill-token-threshold` | Chunked-prefill threshold and long-prompt dispatch limit. |

`--max-num-seqs` limits active request count. `--max-num-batched-tokens` limits
the amount of token work selected by one scheduler iteration. KV cache capacity
comes from model cache shape, `--max-model-len`, `--block-size`, cache dtype,
active request count, and available NPU memory.

Small values are useful for correctness tests because they make scheduler
decisions easy to inspect. Benchmark runs should use values that match the target
workload's prompt length, output length, concurrency, and device memory budget.

## Feature Flags

| Option | Meaning |
| --- | --- |
| `--enable-prefix-caching` / `--no-enable-prefix-caching` | Reuse KV cache state for repeated prompt prefixes when supported. |
| `--enable-chunked-prefill` / `--no-enable-chunked-prefill` | Split long prompts into scheduler-visible chunks. |
| `--speculative-config` | DeepSeek V4 MTP speculative decoding configuration. |
| `--num-speculative-tokens` | Deprecated DeepSeek V4 MTP alias. |

Qwen serving enables prefix caching and chunked prefill by default. DeepSeek V4
serving normally disables prefix caching unless that behavior is under test.

## Ring Runtime Sizing

| Option | Meaning |
| --- | --- |
| `--ring-dep-pool` | Simpler ring dependency-edge pool capacity. |
| `--ring-task-window` | Simpler ring task-slot window capacity. |
| `--ring-heap` | Simpler per-ring output-heap size in bytes. |

Each ring option accepts either one integer, broadcast to every scope-depth ring,
or a comma-separated four-integer list for rings 0 through 3. A value of `0` in a
four-entry list keeps that ring at the runtime default.

Prefer these CLI flags for `pypto-serving` runs. They replace the older
process-wide `PTO2_RING_*` environment variables for the serving dispatch path.

## Profiling Capacity

Profiling does not change scheduler capacity, but it does add host-side recording
work. Use `--profile --profile-output PATH --profile-level e2e,kernel` for a
trace that can explain benchmark results. See [Profiling](../user-guide/profile.md).
