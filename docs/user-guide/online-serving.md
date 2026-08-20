# Online Serving

Online serving starts `pypto-serving`, loads the model in worker processes, and
exposes an OpenAI-compatible HTTP API subset.

## Start a Qwen Server

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

The startup log prints the model name, platform, device groups, parallelism,
request limits, scheduler token limit, and enabled endpoints. Wait for
`Application startup complete` before sending traffic.

## Health and Models

```bash
curl --noproxy "*" http://127.0.0.1:8899/health
curl --noproxy "*" http://127.0.0.1:8899/v1/models
```

## Completion Request

```bash
curl --noproxy "*" http://127.0.0.1:8899/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Huawei is","max_tokens":32,"temperature":0.0}'
```

## Chat Request

```bash
curl --noproxy "*" http://127.0.0.1:8899/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 1+1?"}],"max_tokens":32}'
```

## Shutdown

Stop the server with the normal process signal for your environment. On a
graceful shutdown, active profile recorders are stopped and profile fragments
are merged when profiling is enabled.
