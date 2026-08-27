# DeepSeek V4

PyPTO Serving supports DeepSeek V4 Flash through a converted W8A8 compressed-tensors checkpoint and a fixed eight-device NPU topology. The model uses overlapped attention data parallelism and MoE expert parallelism: the same eight physical ranks are attention DP=8 and MoE EP=8 ranks.

## Requirements

- A converted W8A8 compressed-tensors checkpoint.
- Exactly eight NPU device IDs.
- `--dp 8 --ep 8 --tp 1` for HTTP serving.
- `--block-size 128`.
- `--long-prefill-token-threshold 2048` or another explicit long-prompt dispatch limit up to the DeepSeek V4 8192-token main-prefill ceiling.

See [DeepSeek V4 Checkpoint Conversion](deepseek-v4-checkpoint-conversion.md) before starting a serving run with a source checkpoint that has not been converted to the PyPTO W8A8 layout.

## 8-Device Offline Generation

The offline entry uses the same scheduler, worker process, rank-partitioned cache pools, and MTP acceptance path as HTTP serving, without opening a port.

```bash
PYPTO_RUNTIME_LOG=error \
pypto-serving \
  --model /path/to/dsv4-flash-w8a8 \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --dp 8 \
  --ep 8 \
  --tp 1 \
  --block-size 128 \
  --max-model-len 512 \
  --long-prefill-token-threshold 2048 \
  --ring-dep-pool 131072 \
  --ring-task-window 131072 \
  --ring-heap 2147483648 \
  --generate-config '{"max_new_tokens": 20}' \
  --speculative-config '{"method":"mtp","num_speculative_tokens":1}'
```

Repeat `--prompt` to exercise continuous batching, or add `--profile --profile-output /path/to/profile` to capture only the generation window after model initialization.

## 8-Device DP/EP Serving

Use the converted W8A8 checkpoint and run with overlapped attention DP=8 and MoE EP=8. Both parallel axes use the same eight physical ranks, so this is one model replica rather than eight independent serving replicas:

```bash
PYPTO_RUNTIME_LOG=error \
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
  --ring-dep-pool 131072 \
  --ring-task-window 131072 \
  --ring-heap 2147483648 \
  --port 8225 \
  --show-startup-logs
```

Each NPU runs one prefill row at a time, so DP=8 admits up to eight prefill requests in one global step. The vLLM-style `--speculative-config` selects `method="mtp"`; `num_speculative_tokens` is the maximum number of draft tokens, and any positive value enables MTP. The 16-row MTP decode tile uses B8S2 for K=1, B4S4 for K=2-3, and B2S8 for K>=4. K values larger than seven are supported through repeated target verification chunks. Set `--max-num-seqs` no higher than 64, 32, or 16, respectively. Non-MTP decode retains B8S1T8. The deprecated `--num-speculative-tokens K` flag remains as a compatibility alias.

The server applies DeepSeek V4's model-specific message encoding for chat requests because the checkpoint does not ship a Jinja chat template. Chat mode is the default:

```bash
curl --noproxy "*" http://127.0.0.1:8225/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 1+1?"}],"max_tokens":32}'
```

Pass `"reasoning_effort":"high"` or `"chat_template_kwargs":{"enable_thinking":true}` to use the model's thinking prompt. An explicit `enable_thinking` value takes priority when both are given. The current API supports string content with system, user, developer, assistant, and `latest_reminder` roles; tool calls and multimodal content are not yet exposed by the PyPTO request schema. Generation defaults to greedy sampling (`temperature=0`).

The main prefill kernel accepts a dynamic request extent up to 8192 tokens and walks it internally in 128-token tiles. The effective dispatch extent is the minimum of 8192, `--max-num-batched-tokens`, `--long-prefill-token-threshold`, and `--max-model-len`. An 8191-token prompt can therefore use one 8192-row main-prefill dispatch when those configured limits permit it, instead of 64 serving dispatches.

For repeated launches, set `PYPTO_PROG_BUILD_DIR` to a persistent directory and add `--use-compile-cache`. The first launch populates a device-specific worker subdirectory after executable assembly. Later launches reuse the compiled programs without fingerprint validation, so use the same model configuration, assigned devices, and kernel sources, and clear the directory after any change.

For MTP K greater than 1, prefix caching is disabled automatically. For routine DeepSeek V4 serving, pass `--no-enable-prefix-caching` unless you are explicitly validating prefix-cache behavior.

## Weight Staging

The 49 per-layer weights are described declaratively in `pypto_serving/model/deepseek/weight_spec.py` and evaluated by the shared pipeline documented in [Weight Staging](../developer-guide/weight-staging.md). DeepSeek V4 stages serially on purpose: packing one layer allocates roughly 8 GB of intermediates, so overlapping layers increases peak memory instead of hiding latency.

DeepSeek V4 layers form three slab groups: `fwd` over all layers, `csa` over the `compress_ratio==4` layers, and `hca` over the `compress_ratio==128` layers. Each group stores its layers contiguously in first-appearance order.

See [DeepSeek V4 Prepacked Weights](deepseek-v4-prepacked-weights.md) for the optional sidecar that reduces repeated startup work.

## Completion Check

Check server health first:

```bash
curl --noproxy "*" http://127.0.0.1:8225/health
```

Then send a deterministic completion request:

```bash
curl --noproxy "*" -s http://127.0.0.1:8225/v1/completions -H "Content-Type: application/json" -d '{"model":"dsv4-flash-w8a8","prompt":"Huawei is","max_tokens":25,"temperature":0.0}'
```
