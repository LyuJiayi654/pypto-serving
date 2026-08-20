# Installation

Install PyPTO Serving from a source checkout. The package does not vendor the
Ascend runtime, PyPTO runtime, PyTorch, or model weights; those must be provided
by the active environment.

## Clone

Clone the repository and initialize the kernel submodule:

```bash
git clone https://github.com/hw-native-sys/pypto-serving.git
cd pypto-serving
git submodule update --init --recursive
```

## Install the Python Package

Install the package in editable mode:

```bash
python -m pip install --no-deps -e .
```

`--no-deps` is intentional. The project expects the Python environment to
already contain the Ascend-compatible PyTorch build, PyPTO runtime pieces, and
serving dependencies that match the target machine.

For HTTP serving, make sure the environment also has:

```bash
python -m pip install fastapi uvicorn sse-starlette pydantic
```

For model conversion and checkpoint loading, make sure `safetensors` and
`transformers` are available:

```bash
python -m pip install safetensors transformers
```

Use the package versions required by your Ascend runtime environment. Avoid
replacing a working PyTorch or `torch_npu` installation with a generic wheel.

## Kernel Checkout Discovery

An editable checkout discovers the bundled `pypto-lib/` submodule automatically.
If PyPTO Serving is installed from another location, set `PYPTO_LIB_ROOT` to a
separate `pypto-lib` checkout before loading a model:

```bash
export PYPTO_LIB_ROOT=/path/to/pypto-lib
```

## Verify the Install

After installation, confirm the CLI is available:

```bash
pypto-serving --help
```

Then run the Qwen quickstart once the model checkpoint is available:

```bash
python examples/model/qwen3_14b/npu_generate.py \
  --model-dir /path/to/Qwen3-14B \
  --prompt 'Huawei is' \
  --platform a2a3 \
  --device-id 0 \
  --max-seq-len 512 \
  --max-new-tokens 5
```
