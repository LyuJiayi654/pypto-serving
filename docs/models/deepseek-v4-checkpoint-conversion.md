# DeepSeek V4 Checkpoint Conversion

PyPTO Serving expects a DeepSeek V4 W8A8 compressed-tensors checkpoint. The
released DeepSeek V4 Flash checkpoint mixes FP8 weights with packed MXFP4
expert weights, so it must be converted before serving.

The conversion can run on CPU and does not require `torch_npu`. The source and
output directories must be different, and the host must have enough free disk
space for both copies.

## Prepare Dependencies

```bash
python -m pip install --upgrade huggingface_hub safetensors
python -c "import torch, safetensors; print(torch.__version__)"
```

Use the PyTorch build already validated for the active Ascend environment.

## Download or Locate the Source Checkpoint

```bash
hf download deepseek-ai/DeepSeek-V4-Flash \
  --local-dir /path/to/DeepSeek-V4-Flash
```

If an official mirror is already available locally, use that snapshot directory
as `--input-dir`.

## Dry Run

```bash
python scripts/convert_deepseek_v4_to_w8a8.py \
  --input-dir /path/to/DeepSeek-V4-Flash \
  --output-dir /path/to/dsv4-flash-w8a8 \
  --dry-run
```

## Convert

```bash
python scripts/convert_deepseek_v4_to_w8a8.py \
  --input-dir /path/to/DeepSeek-V4-Flash \
  --output-dir /path/to/dsv4-flash-w8a8
```

The converter writes one safetensors shard at a time using atomic replacement.
If the process is interrupted, rerun with `--resume`:

```bash
python scripts/convert_deepseek_v4_to_w8a8.py \
  --input-dir /path/to/DeepSeek-V4-Flash \
  --output-dir /path/to/dsv4-flash-w8a8 \
  --resume
```

A successful run prints `Conversion complete` and leaves a converted
`config.json`, `model.safetensors.index.json`, safetensors shards, and a
`.pypto-w8a8-conversion.json` marker in the output directory.
