# PyPTO Kernels

PyPTO Serving executes model-specific PyPTO kernels through the NPU executors.
The bundled `pypto-lib/` submodule provides the kernel sources used by the
current model integrations.

## Discovery

Editable checkouts discover `pypto-lib/` automatically. Other installation
layouts should set:

```bash
export PYPTO_LIB_ROOT=/path/to/pypto-lib
```

## Startup

The first run may compile kernels and assemble device binaries. Startup time is
therefore not representative of steady-state generation performance.

Use `--show-startup-logs` on the server to inspect model loading and kernel
compilation progress.

## Compile Cache

Compile cache can be enabled with `--use-compile-cache` and a persistent
`PYPTO_PROG_BUILD_DIR`. It must be cleared after kernel, model, platform, or
device-layout changes.
