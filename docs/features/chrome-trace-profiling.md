# Chrome Trace Profiling

PyPTO Serving records profiling events in the Chrome Trace Event Format. The
merged trace can be opened in Perfetto or another compatible trace viewer.

## What Is Captured

Events can cover:

- HTTP request handling.
- Scheduler decisions.
- Engine and worker dispatch.
- Executor calls.
- NPU kernel dispatch spans.

## Serving Flow

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --profile \
  --profile-output /tmp/pypto-profile \
  --profile-level e2e,kernel
```

Then start and stop recording:

```bash
curl --noproxy "*" -X POST http://127.0.0.1:8000/start_profile
curl --noproxy "*" -X POST http://127.0.0.1:8000/stop_profile
```

See [Profiling](../user-guide/profile.md) for the complete workflow.
