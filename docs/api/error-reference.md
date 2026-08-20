# Error Reference

PyPTO Serving normalizes many validation failures to `ValueError`. HTTP
requests that raise `ValueError` return status 400 with:

```json
{"object":"error","message":"..."}
```

## Common Startup Errors

| Message pattern | Meaning | Action |
| --- | --- | --- |
| `Model directory does not exist` | The model path is wrong or inaccessible. | Check the path and permissions. |
| `Missing config.json` | The checkpoint is incomplete. | Use a full local checkpoint directory. |
| `DeepSeekV4 serving requires the quantized W8A8 compressed-tensors checkpoint` | The original DeepSeek checkpoint was passed to serving. | Run checkpoint conversion first. |
| `DeepSeekV4 serving requires --dp 8 --ep 8 with --tp 1` | Invalid DeepSeek topology. | Use the documented eight-device topology. |
| `DeepSeekV4 serving requires exactly 8 NPU device ids` | Too few or too many devices were passed. | Pass exactly eight unique IDs. |
| `DeepSeekV4 kernels require --block-size 128` | Invalid block size. | Use `--block-size 128`. |
| `number of devices does not match the parallel placement` | `--devices`, `--dp`, and `--tp` do not agree. | For replica placement, use `len(devices) == dp * tp`. |

## Common Request Errors

| Symptom | Likely cause | Action |
| --- | --- | --- |
| HTTP 400 on a long prompt | Prompt plus output exceeds `--max-model-len`. | Lower prompt length or raise `--max-model-len` if the model supports it. |
| HTTP 400 during batching | `--max-num-seqs` exceeds model limits. | Lower `--max-num-seqs`. |
| Stream ends early | EOS, stop string, or max length was reached. | Inspect `finish_reason`. |

## Debugging

Use `--show-startup-logs` for model loading and kernel compilation progress.
Use profiling only after the server is healthy; profiling does not fix startup
or model format errors.
