# `pypto-serving`

`pypto-serving` starts the OpenAI-compatible HTTP server.

## Minimal Example

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

## Argument Groups

- Model: `--model`, `--served-model-name`
- Backend and device: `--backend`, `--platform`, `--device`, `--devices`,
  `--use-compile-cache`
- Parallelism: `--dp`, `--tp`, `--ep`, `--data-parallel-routing`
- Dtype: `--dtype`, `--kv-cache-dtype`
- Runtime: `--max-model-len`, `--block-size`, `--npu-memory-utilization`
- Generation defaults: `--temperature`, `--top-p`, `--top-k`
- Speculative decoding: `--speculative-config`,
  `--num-speculative-tokens`, `--enable-mtp`
- Serving limits: `--host`, `--port`, `--max-num-seqs`,
  `--max-num-batched-tokens`, `--long-prefill-token-threshold`
- Features: `--enable-prefix-caching`, `--enable-chunked-prefill`
- Profiling: `--profile`, `--profile-output`, `--profile-level`
- Misc: `--show-startup-logs`

See [Server Arguments](../configuration/server-arguments.md) for descriptions.
