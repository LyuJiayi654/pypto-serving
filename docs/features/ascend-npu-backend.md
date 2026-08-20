# Ascend NPU Backend

The current PyPTO Serving backend is `npu`. It assumes the host already has an
Ascend driver, CANN toolkit, PyPTO runtime pieces, and a compatible Python
environment.

## How It Is Selected

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0
```

`--platform` selects the target platform name passed into the model executor.
Offline entries also accept simulator platform names such as `a2a3sim` and
`a5sim` where supported by the entry point.

## Device Placement

Single-device Qwen serving uses `--device`. Multi-device placement uses
`--devices` with the selected parallel configuration. DeepSeek V4 requires
exactly eight device IDs.

## Boundary

The backend is not a generic accelerator abstraction. Model support, kernel
layout, cache layout, and supported parallelism are implemented per model
family.
