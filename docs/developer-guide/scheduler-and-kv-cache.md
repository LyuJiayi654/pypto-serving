# Scheduler and KV Cache

The scheduler tracks request state, enforces runtime limits, allocates KV cache
pages, and dispatches work to the engine.

## Request Flow

1. A request enters the engine with a prompt and `GenerateConfig`.
2. The tokenizer produces prompt token IDs.
3. The scheduler assigns the request to prefill.
4. KV pages are allocated for the request.
5. The model executor runs prefill and then decode steps.
6. The scheduler releases cache pages when the request finishes.

## KV Cache

The generic KV cache uses page IDs and a fixed block size. DeepSeek V4 uses
grouped cache specs for model-specific cache families and rank-local
partitions.

## Extension Points

Changes to request scheduling or cache allocation should include focused unit
tests under `tests/unit/serving/` and NPU validation when model behavior or
device dispatch is affected.
