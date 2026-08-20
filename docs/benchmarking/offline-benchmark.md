# Offline Benchmarking

Offline benchmarking uses the repository example entry points. This is the
fastest way to validate kernel behavior and measure generation without HTTP
server overhead.

## Qwen3-14B

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 128 \
  --profile
```

The entry prints generated tokens, total generation time, overall tokens per
second, prefill time, decode time, and per-token decode time.

## DeepSeek V4

```bash
python examples/model/deepseek_v4/npu_generate.py \
  --model-dir /path/to/dsv4-flash-w8a8 \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --max-seq-len 512 \
  --max-new-tokens 128 \
  --num-prompts 8 \
  --profile \
  --profile-output /tmp/pypto-dsv4-offline
```

Use `--num-prompts` to exercise continuous batching.

## Interpreting Results

Offline numbers include prefill and decode but not HTTP request overhead.
Separate cold-start measurements from steady-state measurements.
