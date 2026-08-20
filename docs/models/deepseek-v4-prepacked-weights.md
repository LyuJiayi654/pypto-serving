# DeepSeek V4 Prepacked Weights

DeepSeek V4 hidden-layer weights can be converted once into the rank-stacked
host layout consumed by the serving runner. The optional sidecar reduces
repeated startup work on later launches.

## Build the Sidecar

```bash
pypto-prepack-deepseek-v4 /path/to/dsv4-flash-w8a8
```

The command writes `pypto-deepseek-v4-stacked-r8.safetensors` beside the
checkpoint by default.

## Replace an Existing Sidecar

```bash
pypto-prepack-deepseek-v4 /path/to/dsv4-flash-w8a8 --force
```

Rebuild the sidecar after replacing checkpoint shards or changing the packed
rank layout.

## Runtime Behavior

On startup, the DeepSeek V4 loader checks the sidecar and validates it against
the checkpoint and deployment fingerprint. A hot, valid sidecar is memory
mapped as the final layout. A missing, cold, or stale sidecar falls back to the
original checkpoint path.
