# Quickstart

This page runs the shortest end-to-end path: one Qwen3-14B offline generation,
then the OpenAI-compatible HTTP server. See the DeepSeek V4 model guide for
the eight-device W8A8 path.

## Offline Qwen3-14B Generation

Run one generation on a single Ascend NPU:

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 5
```

Expected output includes generated text, token IDs, a finish reason, and a
throughput summary. The first run may spend extra time compiling kernels.

## HTTP Serving

Start the server on one device:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

Wait for `Application startup complete`, then send requests from another shell:

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

The completion response includes one choice and usage counts when the request
finishes. Streaming responses are Server-Sent Events and end with
`data: [DONE]`.

## Next Steps

- [Offline Inference](../user-guide/offline-inference.md): run larger offline
  validation workloads.
- [Online Serving](../user-guide/online-serving.md): configure the HTTP server.
- [OpenAI-Compatible Server](../user-guide/openai-compatible-server.md):
  understand the supported API subset.
- [Parallelism and Scaling](../user-guide/parallel.md): configure DP, TP, and
  DeepSeek V4 overlapped DP/EP.
- [Profiling](../user-guide/profile.md): capture Chrome trace profiles.
