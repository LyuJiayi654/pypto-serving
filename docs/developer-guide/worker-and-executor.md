# Worker and Executor

Serving workers isolate model execution from the API process. A worker owns the
model executor, compiled kernel handles, and device-facing runtime state.

## Worker Responsibilities

- Load model runtime state.
- Initialize model executors.
- Run prefill and decode commands.
- Participate in profiling start and stop commands.
- Return generated token state to the engine.

## Executor Responsibilities

Model executors implement the model-specific bridge from serving batches to
PyPTO kernels. Qwen and DeepSeek V4 have separate executors and runners because
their kernel layouts, cache layouts, and parallel contracts differ.

## Profiling

Worker and executor spans are recorded by `pypto_serving.tools.profile` when
profiling is enabled. Keep event arguments small and JSON serializable.
