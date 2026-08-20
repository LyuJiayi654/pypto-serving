# MTP Speculative Decoding

DeepSeek V4 supports MTP speculative decoding. This feature drafts additional
tokens and verifies them with the target model path.

## HTTP Serving

Use the vLLM-style speculative config:

```bash
pypto-serving \
  --model /path/to/dsv4-flash-w8a8 \
  --devices 0,1,2,3,4,5,6,7 \
  --dp 8 \
  --ep 8 \
  --tp 1 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

Deprecated compatibility aliases remain available:

- `--num-speculative-tokens K`
- `--enable-mtp`

## Offline

The DeepSeek V4 offline entry exposes:

```bash
--enable-mtp
```

Offline MTP currently requires deterministic generation with
`--temperature 0`.

## Limits

MTP changes the decode layout and therefore the maximum accepted
`--max-num-seqs`. If the requested batch size is too high, startup fails with a
model-specific error message.
