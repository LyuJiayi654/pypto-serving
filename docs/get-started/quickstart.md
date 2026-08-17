# Quickstart

## One-Shot NPU Generation

Run a single Qwen3-14B generation on an Ascend NPU:

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 5
```

For DeepSeek V4 Flash W8A8 offline generation on eight devices:

```bash
python examples/model/deepseek_v4/npu_generate.py \
  --model-dir /data/models/dsv4-flash-w8a8 \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --max-seq-len 512 \
  --max-new-tokens 20
```

## HTTP Serving

Start the OpenAI-compatible HTTP server:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

Wait for the server to log `Application startup complete`, then send requests:

```bash
# Health check
curl --noproxy "*" http://127.0.0.1:8899/health

# Completion
curl --noproxy "*" http://127.0.0.1:8899/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Huawei is", "max_tokens": 32, "temperature": 0.0}'

# Streaming
curl --noproxy "*" http://127.0.0.1:8899/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Huawei is", "max_tokens": 32, "stream": true}'

# Chat completion
curl --noproxy "*" http://127.0.0.1:8899/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is 1+1?"}], "max_tokens": 32}'
```

## Next Steps

- [Parallel Serving](../user-guide/parallel.md) — configure DP, TP, and EP
- [Profiling](../user-guide/profile.md) — enable performance tracing