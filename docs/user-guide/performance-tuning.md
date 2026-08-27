# Performance Tuning

Tune PyPTO Serving by matching scheduler capacity, KV cache capacity, model topology, and kernel compilation behavior to the workload.

## Startup Cost

The first run may compile kernels and assemble device binaries. For repeated launches with the same model configuration, assigned devices, and kernel sources, set a persistent build directory and enable compile cache:

```bash
export PYPTO_PROG_BUILD_DIR=/path/to/pypto-build
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --use-compile-cache
```

There is no fingerprint validation for the compile cache. Clear the directory after changing kernel sources, model configuration, platform, or device layout.

## Continuous Batching

Continuous batching keeps multiple requests active across engine iterations. Requests move through waiting, prefill, decode, and finished states. The scheduler allocates KV cache pages and dispatches work that fits the configured request and token limits.

The relevant scheduler limits are documented in [Runtime Capacity Arguments](../cli-reference/pypto-serving.md#runtime-capacity-arguments). Raise the active-request limit for more concurrency and raise the scheduled token limit for larger batches, but watch memory pressure and model-specific batch limits.

## KV Cache Capacity

Paged KV cache capacity is bounded by sequence length, page size, active request count, and available NPU memory.

For standard models, the runtime uses a generic page layout. DeepSeek V4 uses model-specific grouped cache pools that follow the decode layout and compressed-state requirements of its kernels.

Larger capacity values can improve batching but increase memory pressure. Start with the quickstart values, then raise one limit at a time while watching startup logs, request errors, and profile traces.

## Chunked Prefill

Chunked prefill breaks long prompts into scheduler-visible chunks so a long prefill does not monopolize the engine indefinitely. It is enabled by default and controlled by `--long-prefill-token-threshold`.

Use `--no-enable-chunked-prefill` only when validating behavior. For DeepSeek V4, the model runner also caps one request's main-prefill dispatch at 8192 tokens and pads the kernel extent to 128-token tiles. Set the threshold intentionally instead of treating the 128-token tile as the serving chunk size.

## Prefix Caching

Prefix caching reuses KV cache state for repeated prompt prefixes when the model path supports it. It is enabled by default for Qwen. Disable it with `--no-enable-prefix-caching` when isolating scheduler or kernel behavior.

Use profiling to confirm whether time is spent in prefill, decode, scheduler, worker dispatch, or kernel execution before changing limits.

## DeepSeek V4 MTP

For DeepSeek V4, `--speculative-config '{"method":"mtp","num_speculative_tokens":K}'` enables MTP speculative decoding. Larger `K` changes the decode layout and reduces the allowed global batch size. If the server rejects `--max-num-seqs`, lower it according to the error message.
