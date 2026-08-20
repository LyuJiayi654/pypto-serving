# Qwen3-14B

PyPTO Serving supports Qwen3-14B through the bundled Qwen model loader, NPU
executor, and PyPTO kernels. Use this path for single-device validation,
offline tensor-parallel runs, and HTTP serving with one or more data-parallel
replicas.

## Checkpoint

Use a local Hugging Face style Qwen3-14B checkpoint directory. The directory
must contain `config.json`, tokenizer files, and model weight shards readable
by the active Python environment.

## Offline Generation

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 32
```

For one tensor-parallel worker group, provide `--devices` and `--tp`:

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --devices 0,1 \
  --tp 2 \
  --max-seq-len 512 \
  --max-new-tokens 32
```

The offline entry intentionally rejects `--dp > 1`; data parallelism is an
online serving concept in this project.

## HTTP Serving

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

Send a request after startup:

```bash
curl --noproxy "*" http://127.0.0.1:8899/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Huawei is","max_tokens":32,"temperature":0.0}'
```

## DP=2 Serving

Data parallel serving creates independent replicas and routes requests by the
`least_pending_tokens` policy:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --devices 0,1 \
  --dp 2 \
  --tp 1 \
  --max-model-len 512 \
  --port 8899
```

## Supported Controls

- `--max-model-len`, `--block-size`, `--max-num-seqs`, and
  `--max-num-batched-tokens` control runtime capacity.
- `--temperature`, `--top-p`, and `--top-k` set default sampling values for the
  server. Per-request API fields override those defaults.
- Prefix caching and chunked prefill are enabled by default for Qwen serving.
- `--use-compile-cache` can reduce repeated startup cost when the model config,
  devices, and kernel sources are unchanged.
