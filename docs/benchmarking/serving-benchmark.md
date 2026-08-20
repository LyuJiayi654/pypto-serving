# Serving Benchmarking

Serving benchmarks measure the HTTP path, scheduler behavior, worker dispatch,
and model execution under client load.

## Start the Server

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --max-num-seqs 16 \
  --max-num-batched-tokens 4096 \
  --port 8899
```

## Generate Load

Use a client that records:

- Request rate or concurrency.
- Time to first token for streaming.
- End-to-end latency.
- Output token throughput.
- Error rate.

The server accepts simple `curl` requests for smoke tests, but benchmark runs
should use a repeatable client script or a known serving benchmark tool pointed
at `/v1/completions` or `/v1/chat/completions`.

## Keep Workloads Explicit

Report prompt length, output length, sampling settings, stream mode, and model
topology with every result. Small changes in `max_tokens`, chunked prefill,
MTP, or `max_num_seqs` can change results materially.
