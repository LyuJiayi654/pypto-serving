# Compile Cache

Compile cache lets repeated serving launches reuse compiled kernels and device
binaries.

## Enable

```bash
export PYPTO_PROG_BUILD_DIR=/path/to/pypto-build
pypto-serving \
  --model /path/to/Qwen3-14B \
  --backend npu \
  --platform a2a3 \
  --device 0 \
  --use-compile-cache
```

## Safety Contract

The cache does not fingerprint kernel sources or runtime configuration. Reuse a
cache directory only for the same:

- Model family and model configuration.
- Platform.
- Device layout.
- Kernel sources.
- Relevant runtime arguments.

Clear the directory after changes.
