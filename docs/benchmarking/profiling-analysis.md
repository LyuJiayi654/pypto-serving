# Profile Analysis

Use Chrome trace profiles to explain benchmark results. Profiles complement
latency and throughput metrics by showing where time is spent.

## Capture

For HTTP serving:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --profile \
  --profile-output /tmp/pypto-profile \
  --profile-level e2e,kernel
```

```bash
curl --noproxy "*" -X POST http://127.0.0.1:8000/start_profile
# run benchmark workload
curl --noproxy "*" -X POST http://127.0.0.1:8000/stop_profile
```

Open `/tmp/pypto-profile/trace.json` in Perfetto.

## What to Inspect

- Long prefill spans relative to prompt length.
- Decode step duration and variance.
- Scheduler gaps between worker dispatches.
- Worker or executor spans that dominate kernel time.
- Missing kernel spans, which usually indicate profiling was not enabled at
  the right level or during the workload window.
