# Installation

## Prerequisites

- Python 3.10 or later
- Ascend NPU environment with drivers and CANN toolkit
- PyPTO framework — see the [pypto](https://github.com/hw-native-sys/pypto) project for installation instructions
- torch, torch-npu, safetensors, transformers, fastapi, uvicorn, and other runtime dependencies (see `pypto_serving/requirements.txt`)

## Quick Install

Clone the repository and initialize submodules:

```bash
git clone https://github.com/hw-native-sys/pypto-serving.git
cd pypto-serving
git submodule update --init --recursive
```

Install the package in editable mode without runtime dependencies:

```bash
python -m pip install --no-deps -e .
```

## Verify

After installation, confirm the CLI is available:

```bash
pypto-serving --help
```
