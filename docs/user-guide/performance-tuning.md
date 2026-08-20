# Performance Tuning

Tune PyPTO Serving by matching scheduler capacity, KV cache capacity, model
topology, and kernel compilation behavior to the workload.

## Startup Cost

The first run may compile kernels and assemble device binaries. For repeated
launches with the same model configuration, assigned devices, and kernel
sources, set a persistent build directory and enable compile cache:

```bash
export PYPTO_PROG_BUILD_DIR=/path/to/pypto-build
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --use-compile-cache
```

There is no fingerprint validation for the compile cache. Clear the directory
after changing kernel sources, model configuration, platform, or device layout.

## Request and Token Limits

| Option | Effect |
| --- | --- |
| `--max-model-len` | Maximum prompt plus generated tokens accepted by the server. |
| `--max-num-seqs` | Maximum active requests. |
| `--max-num-batched-tokens` | Maximum tokens scheduled in one engine iteration. |
| `--block-size` | KV cache page size. DeepSeek V4 requires 128. |
| `--npu-memory-utilization` | Fraction of NPU memory available for weights, activations, and KV cache. |

Larger values can improve batching but increase memory pressure. Start with the
quickstart values, then raise one limit at a time while watching startup logs,
request errors, and profile traces.

## Prefix Caching and Chunked Prefill

Prefix caching is enabled by default for Qwen and disabled for DeepSeek V4.
Chunked prefill is enabled by default and controlled by
`--long-prefill-token-threshold`.

Use profiling to confirm whether time is spent in prefill, decode, scheduler,
worker dispatch, or kernel execution before changing limits.

## DeepSeek V4 MTP

For DeepSeek V4, `--speculative-config '{"method":"mtp","num_speculative_tokens":K}'`
enables MTP speculative decoding. Larger `K` changes the decode layout and
reduces the allowed global batch size. If the server rejects `--max-num-seqs`,
lower it according to the error message.
