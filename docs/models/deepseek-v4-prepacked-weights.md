# DeepSeek V4 Prepacked Weights

DeepSeek V4 hidden-layer weights can be converted once into the rank-stacked host layout consumed by the serving runner. The optional sidecar reduces repeated startup work on later launches.

## Build the Sidecar

Use the [`pypto-prepack-deepseek-v4`](../cli-reference/pypto-prepack-deepseek-v4.md) CLI after converting a DeepSeek V4 Flash checkpoint to the W8A8 layout. The default sidecar path is `pypto-deepseek-v4-stacked-r8.safetensors` beside the checkpoint.

## Runtime Behavior

On startup, the DeepSeek V4 loader samples the sidecar's Linux page-cache residency before opening it, then validates a hot sidecar against the checkpoint-file and deployment fingerprint. A hot, valid sidecar is memory mapped as the final layout instead of repacking every hidden layer.

A cold, missing, or stale sidecar falls back to the original checkpoint path, avoiding a cold 323 GiB page-fault stream on the weight-upload path. Rebuild with `--force` after replacing checkpoint shards or changing the packed rank layout.

## Layout Contract

The sidecar layout follows the order produced by `DEEPSEEK_V4_LAYER_RULES`, and its metadata records a name-to-offset map built from that order. Reordering the rule table invalidates already-written sidecars.

The fingerprint covers the config, weight map, and each source shard's size and modification time, which lets startup detect a stale sidecar instead of silently using the wrong layout.
