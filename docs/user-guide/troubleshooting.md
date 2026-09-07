# Troubleshooting

Start with the failure boundary: installation, model loading, worker startup,
HTTP request handling, generation correctness, or profiling. Most PyPTO Serving
failures become clear once the model path, device placement, and runtime
environment are checked together.

## CLI Is Missing

Run the package install from the repository root:

```bash
python -m pip install --no-deps -e .
pypto-serving --help
```

`--no-deps` is expected. Runtime dependencies such as CANN, PyPTO, PyTorch,
`safetensors`, `transformers`, FastAPI, Uvicorn, and Pydantic must already match
the target environment.

## HTTP Dependencies Are Missing

If importing the server fails with a FastAPI or Pydantic error, install the HTTP
dependencies in the active environment:

```bash
python -m pip install fastapi uvicorn pydantic
```

## Kernel Directory Not Found

Initialize the submodule:

```bash
git submodule update --init --recursive
```

For non-editable installs, set `PYPTO_LIB_ROOT` to a `pypto-lib` checkout. See
[Environment Variables](../configuration/env-vars.md#pypto-library-discovery).

## First Launch Is Slow

Cold startup can include kernel compilation, executable assembly, model weight
staging, and checkpoint page faults. Use `--show-startup-logs` to make progress
visible. For repeated runs, set `PYPTO_PROG_BUILD_DIR` and pass
`--use-compile-cache`.

The compile cache is not fingerprinted. Clear it after changing kernel sources,
model configuration, platform, or assigned devices.

## Worker Initialization Times Out

Large checkpoints can exceed the default startup timeout on cold systems:

```bash
PYPTO_WORKER_INIT_TIMEOUT=1800 pypto-serving --model /path/to/dsv4-flash-w8a8
```

If increasing the timeout does not help, check the model path, submodule state,
CANN/PyPTO environment, device visibility, and DeepSeek V4 sidecar validity.

## Request Returns HTTP 400

Scheduler and engine rejections are returned as:

```json
{"object":"error","message":"..."}
```

Common causes:

- Prompt plus requested output exceeds `--max-model-len`.
- The request cannot fit within active KV cache capacity.
- DeepSeek V4 was started without the required eight-device topology.
- A model-specific feature, such as DeepSeek V4 MTP, received an invalid config.

## vLLM Client Sends Unsupported Fields

PyPTO Serving supports only the fields listed in
[vLLM Compatibility](vllm-compatibility.md). Remove vLLM-only parameters such as
`logprobs`, `best_of`, `use_beam_search`, `structured_outputs`, `tools`,
multimodal message parts, `stream_options`, and Responses API session fields.

## Chat Template Fails

Qwen uses the tokenizer's `apply_chat_template` method. Confirm the checkpoint
contains tokenizer files and a valid chat template.

DeepSeek V4 uses model-specific message encoding because the validated checkpoint
does not ship a Jinja chat template. Its chat schema accepts string content with
system, user, developer, assistant, and `latest_reminder` roles.

## DeepSeek V4 Startup Fails

Check these invariants first:

- The checkpoint was converted to the PyPTO W8A8 layout.
- Exactly eight device IDs were passed.
- Serving uses `--dp 8 --ep 8 --tp 1`.
- `--block-size 128` is set.
- Routine serving uses `--no-enable-prefix-caching`.
- MTP uses `--speculative-config '{"method":"mtp","num_speculative_tokens":K}'`.

If a prepacked sidecar exists, rebuild it with `pypto-prepack-deepseek-v4 --force`
after replacing checkpoint shards or changing the packed rank layout.

## Streaming Client Hangs

Streaming responses end with:

```text
data: [DONE]
```

Read Server-Sent Events until that terminal marker. The final JSON event before
`[DONE]` has an empty `choices` list and token `usage`. Clients that expect every
event to contain a text delta must skip that usage event.

## Profile Trace Has No Kernel Events

Confirm all of the following:

- The server was started with `--profile`.
- `--profile-level` includes `kernel`.
- `POST /start_profile` happened before the workload.
- `POST /stop_profile` happened after the workload completed.
- The merged trace path under `--profile-output` was opened, not an old trace.

If the process exited before merging, run `scripts/merge_profile.sh` with the
same profile output path after all profiled processes have stopped.
