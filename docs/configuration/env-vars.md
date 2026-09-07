# Environment Variables

Most PyPTO Serving configuration should be passed as CLI arguments. Environment
variables are reserved for local runtime integration, profiling helpers, and a
small number of debug controls.

## Public Variables

| Variable | Used by | Purpose |
| --- | --- | --- |
| `PYPTO_LIB_ROOT` | Model executors | Path to a `pypto-lib` checkout when it cannot be discovered from an editable source tree. |
| `PYPTO_PROG_BUILD_DIR` | Worker startup | Directory for generated kernel artifacts and compile-cache subdirectories. |
| `PYPTO_STAGING_THREADS` | Qwen weight staging | Optional thread count for Qwen parallel weight staging. |
| `PYPTO_WORKER_INIT_TIMEOUT` | Engine startup | Worker initialization timeout in seconds for large checkpoints or slow first launches. |
| `SERVING_WORKER_STEP_TIMEOUT` | Engine runtime | Worker step timeout in seconds. |
| `PYPTO_SERVING_GC_DEBUG` | Serving utilities | Set to `1` to log garbage-collection debug events in the process. |
| `SA_PROFILE_OUTPUT` | Profiling library and merge script | Profile output path for library users or `scripts/merge_profile.sh`. CLI users should prefer `--profile-output`. |
| `SA_PROFILE_LEVEL` | Profiling library | Comma-separated profile levels. CLI users should prefer `--profile-level`. |
| `PYPTO_RUNTIME_LOG` | PyPTO runtime | Runtime log control forwarded through the process environment. |

## Compile Cache

Set `PYPTO_PROG_BUILD_DIR` to a persistent directory and start with
`--use-compile-cache` to reuse compiled programs on later runs:

```bash
PYPTO_PROG_BUILD_DIR=/data/cache/pypto-build \
pypto-serving \
  --model /path/to/Qwen3-14B \
  --platform a2a3 \
  --device 0 \
  --use-compile-cache \
  --prompt 'Huawei is' \
  --generate-config '{"max_new_tokens":5}'
```

The compile cache has no fingerprint validation. Reuse it only with the same
model configuration, platform, assigned devices, and kernel sources. Clear the
directory after changing any of those inputs.

## PyPTO Library Discovery

Editable checkouts discover the bundled `pypto-lib/` submodule automatically.
For non-editable installs, set `PYPTO_LIB_ROOT` before loading a model:

```bash
PYPTO_LIB_ROOT=/path/to/pypto-lib pypto-serving --model /path/to/Qwen3-14B
```

If model startup reports that a kernel directory is missing, check this variable
and confirm the submodule was initialized.

## Profiling Environment

HTTP serving should use explicit CLI options:

```bash
pypto-serving \
  --model /path/to/Qwen3-14B \
  --profile \
  --profile-output /tmp/pypto-profile \
  --profile-level e2e,kernel
```

`SA_PROFILE_OUTPUT` and `SA_PROFILE_LEVEL` remain useful for lower-level library
users and for manual merge recovery:

```bash
SA_PROFILE_OUTPUT=/tmp/pypto-profile ./scripts/merge_profile.sh
```

Do not set `SA_PROFILE_MAIN_PID` manually. It is an internal coordination value
written by the profiler.

## Worker Timeouts

Large checkpoints and cold cache launches can take longer than the default worker
initialization window. Increase `PYPTO_WORKER_INIT_TIMEOUT` for that case:

```bash
PYPTO_WORKER_INIT_TIMEOUT=1800 pypto-serving --model /path/to/dsv4-flash-w8a8
```

`SERVING_WORKER_STEP_TIMEOUT` should only be raised after confirming that device
work is expected to exceed the current timeout. A timeout can also indicate a
stalled worker, mismatched kernel layout, or device/runtime failure.

## Legacy Ring Variables

Older examples may set `PTO2_RING_DEP_POOL`, `PTO2_RING_TASK_WINDOW`, or
`PTO2_RING_HEAP`. For `pypto-serving`, prefer the documented `--ring-*` CLI
arguments because they are applied per dispatch instead of resizing every worker
through process-wide environment.
