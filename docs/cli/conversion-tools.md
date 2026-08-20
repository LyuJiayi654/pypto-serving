# Conversion Tools

The repository includes a DeepSeek V4 conversion utility under `scripts/`.

## `convert_deepseek_v4_to_w8a8.py`

Convert the released DeepSeek V4 Flash Hybrid FP8/MXFP4 checkpoint into the
W8A8 compressed-tensors checkpoint expected by PyPTO Serving.

```bash
python scripts/convert_deepseek_v4_to_w8a8.py \
  --input-dir /path/to/DeepSeek-V4-Flash \
  --output-dir /path/to/dsv4-flash-w8a8
```

Options:

| Argument | Description |
| --- | --- |
| `--input-dir PATH` | Original DeepSeek V4 Flash checkpoint. |
| `--output-dir PATH` | Converted checkpoint directory. |
| `--resume` | Skip validated shards after an interrupted conversion. |
| `--dry-run` | Validate and print the conversion plan without writing output. |

See [DeepSeek V4 Checkpoint Conversion](../models/deepseek-v4-checkpoint-conversion.md).
