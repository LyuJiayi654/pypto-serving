# Troubleshooting

Start with the exact command, model path, device list, and first exception. Most
failures fall into environment, checkpoint, topology, or capacity categories.

## CLI Starts but Model Loading Fails

Check that the model directory contains `config.json`, tokenizer files, and
weight shards:

```bash
test -f /path/to/model/config.json
```

For DeepSeek V4, verify that the checkpoint is the converted W8A8
compressed-tensors checkpoint, not the original Hybrid FP8/MXFP4 release.

## Device or Topology Errors

- Qwen replica placement requires `len(devices) == dp * tp`.
- DeepSeek V4 requires exactly eight devices.
- DeepSeek V4 HTTP serving requires `--dp 8 --ep 8 --tp 1`.
- Pipeline parallelism is not supported.

## Kernel Startup Is Slow

The first launch may compile kernels. Use `--show-startup-logs` to see startup
progress. Use `PYPTO_PROG_BUILD_DIR` and `--use-compile-cache` only when the
configuration and kernel sources are unchanged.

## Requests Return HTTP 400

Common causes:

- Prompt plus `max_tokens` exceeds `--max-model-len`.
- `--max-num-seqs` exceeds the model-specific decode batch limit.
- DeepSeek V4 `--block-size` is not 128.
- DeepSeek V4 is using an unconverted checkpoint.

## Profile File Is Missing or Empty

For HTTP serving, launch with `--profile`, then call `/start_profile` before
the workload and `/stop_profile` after the workload. For offline Qwen, the
timing report flags are separate from `SA_PROFILE_OUTPUT`; see
[Profiling](profile.md).
