# Local Ascend Runs

PyPTO Serving is currently documented for local Ascend NPU environments. This
page collects the operational pieces that vLLM deployment guides usually spread
across Docker, Kubernetes, proxy, and production-stack pages.

## Host Checklist

- Linux host with visible Ascend NPUs.
- CANN and PyPTO runtime pieces loaded in the active shell.
- Ascend-compatible Python 3.10+ environment with PyTorch.
- `pypto-serving` installed from a source checkout.
- `pypto-lib` submodule initialized, or `PYPTO_LIB_ROOT` set.
- Local model checkpoint available on a filesystem visible to the serving user.

## Source Checkout

```bash
git submodule update --init --recursive
python -m pip install --no-deps -e .
```

The package intentionally does not vendor CANN, PyPTO, PyTorch, or model weights.
Keep those aligned with the target machine.

## Task-Submit Validation

When using `task-submit`, keep the runtime environment variables required by the
local scheduler and pass the complete command as one run string:

```bash
task-submit --device auto --max-time 0 --run \
  "PTO2_RING_HEAP=536870912 PTO2_RING_TASK_WINDOW=131072 PTO2_RING_DEP_POOL=131072 \
  pypto-serving --model /data/linyifan/models/Qwen3-14B \
    --prompt 'Huawei is' \
    --platform a2a3 \
    --max-model-len 512 \
    --generate-config '{\"max_new_tokens\": 5}'"
```

Use this for basic NPU availability and model-path validation before starting a
long-running HTTP server.

## Single-Device Server

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --max-model-len 512 \
  --port 8899
```

Wait for `Application startup complete`, then check readiness:

```bash
curl --noproxy "*" http://127.0.0.1:8899/health
curl --noproxy "*" http://127.0.0.1:8899/v1/models
```

## Multi-Device Server

Qwen data-parallel serving creates independent replicas:

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

DeepSeek V4 uses a fixed eight-device overlapped topology:

```bash
PYPTO_RUNTIME_LOG=error \
pypto-serving \
  --model /path/to/dsv4-flash-w8a8 \
  --served-model-name dsv4-flash-w8a8 \
  --backend npu \
  --platform a2a3 \
  --devices 0,1,2,3,4,5,6,7 \
  --dp 8 \
  --ep 8 \
  --tp 1 \
  --block-size 128 \
  --max-model-len 512 \
  --max-num-seqs 32 \
  --max-num-batched-tokens 512 \
  --long-prefill-token-threshold 2048 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":1}' \
  --no-enable-prefix-caching \
  --port 8225
```

## Network Binding

The default bind host is `0.0.0.0`. For local validation, use `127.0.0.1` if the
server does not need to accept remote connections:

```bash
pypto-serving --model /path/to/Qwen3-14B --host 127.0.0.1 --port 8899
```

For shared machines, put access control in the surrounding environment. PyPTO
Serving does not implement authentication, TLS termination, tenant isolation, or
request authorization.

## Startup Cost

First launch can include kernel compilation, executable assembly, checkpoint
packing, and NPU memory setup. For repeated launches, set a persistent
`PYPTO_PROG_BUILD_DIR` and pass `--use-compile-cache`. For DeepSeek V4, also
consider the optional prepacked weight sidecar documented in
[DeepSeek V4](../user-guide/deepseek-v4.md#prepacked-weights).

## Shutdown

Stop the process with the normal signal used by the environment. A graceful
shutdown attempts to stop active profilers and merge available trace fragments.
If the process was interrupted during profiling, use
[Profiling](../user-guide/profile.md#merge-profile-fragments-manually) to merge
fragments after all profiled processes have exited.
