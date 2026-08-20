# Environment Variables

PyPTO Serving primarily uses CLI arguments. Environment variables are reserved
for runtime integration, PyPTO kernel behavior, and profiling.

## PyPTO and Kernel Paths

| Variable | Purpose |
| --- | --- |
| `PYPTO_LIB_ROOT` | Path to a `pypto-lib` checkout when it is not discoverable from the editable source tree. |
| `PYPTO_ROOT` | Optional PyPTO root used by some DeepSeek V4 offline paths. |
| `PYPTO_SAVE_KERNELS_DIR` | Optional directory for saved kernels in DeepSeek V4 offline setup. |
| `PYPTO_PROG_BUILD_DIR` | Persistent compiled-program directory used with `--use-compile-cache`. |

## Profiling

| Variable | Purpose |
| --- | --- |
| `SA_PROFILE_OUTPUT` | Offline profile output path for legacy/profile helper flows. |
| `SA_PROFILE_LEVEL` | Offline profile levels such as `e2e,kernel`. |

For HTTP serving, prefer `--profile`, `--profile-output`, and
`--profile-level`. `SA_PROFILE_OUTPUT` and `SA_PROFILE_LEVEL` do not enable
HTTP profiling by themselves.

## Runtime Tuning

Some deployments need lower-level PyPTO runtime variables. Common examples in
DeepSeek V4 validation commands include:

| Variable | Purpose |
| --- | --- |
| `PYPTO_RUNTIME_LOG` | Runtime log level. |
| `PTO2_RING_DEP_POOL` | Ring dependency pool size. |
| `PTO2_RING_TASK_WINDOW` | Ring task window size. |
| `PTO2_RING_HEAP` | Ring heap size. |
| `PTO2_OP_EXECUTE_TIMEOUT_US` | Operation timeout in microseconds. |
| `PTO2_STREAM_SYNC_TIMEOUT_MS` | Stream synchronization timeout. |
| `PTO2_SCHEDULER_TIMEOUT_MS` | Scheduler timeout. |
| `SERVING_WORKER_STEP_TIMEOUT` | Serving worker step timeout. |

Keep the runtime values used by a known-good environment unless you are
debugging a specific timeout, memory, or scheduling issue.
