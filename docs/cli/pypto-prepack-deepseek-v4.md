# `pypto-prepack-deepseek-v4`

`pypto-prepack-deepseek-v4` builds the optional DeepSeek V4 hidden-layer weight
sidecar used to reduce repeated startup work.

## Usage

```bash
pypto-prepack-deepseek-v4 /path/to/dsv4-flash-w8a8
```

## Options

| Argument | Default | Description |
| --- | --- | --- |
| `model_dir` | Required | DeepSeek V4 W8A8 checkpoint directory. |
| `--ranks` | `8` | Rank count for the packed layout. |
| `--output PATH` | auto-discovery path | Sidecar output path. |
| `--force` | off | Replace an existing sidecar. |

See [DeepSeek V4 Prepacked Weights](../models/deepseek-v4-prepacked-weights.md).
