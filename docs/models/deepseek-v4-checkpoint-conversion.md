# DeepSeek V4 Checkpoint Conversion

PyPTO Serving expects a DeepSeek V4 W8A8 compressed-tensors checkpoint. The DeepSeek V4 Flash source checkpoint variant validated by this repository mixes FP8 weights with packed MXFP4 expert weights, so it must be converted before serving.

The conversion can run on CPU and does not require `torch_npu`. The source and output directories must be different, and the host must have enough free disk space for both copies.

Run the repository conversion utility documented in [DeepSeek V4 Conversion](../cli-reference/deepseek-v4-conversion.md). The converter writes one safetensors shard at a time using atomic replacement and supports resumable conversion after an interrupted run.

A successful run prints `Conversion complete` and leaves a converted `config.json`, `model.safetensors.index.json`, safetensors shards, and a `.pypto-w8a8-conversion.json` marker in the output directory.

After conversion, [DeepSeek V4 Prepacked Weights](deepseek-v4-prepacked-weights.md) describes the optional sidecar that reduces repeated startup work.
