# Continuous Batching

Continuous batching lets the scheduler keep multiple requests active and pack
work across engine iterations. It is used by HTTP serving and by the DeepSeek
V4 offline path.

## Controls

| Option | Meaning |
| --- | --- |
| `--max-num-seqs` | Maximum active requests. |
| `--max-num-batched-tokens` | Maximum tokens scheduled in one iteration. |
| `--long-prefill-token-threshold` | Threshold for chunked prefill behavior. |

## Behavior

Requests can be in waiting, prefill, decode, or finished states. The scheduler
allocates KV cache pages and dispatches work that fits the configured request
and token limits.

## Tuning

Raise `--max-num-seqs` for more concurrency and raise
`--max-num-batched-tokens` for larger prefill/decode batches, but watch memory
pressure and model-specific batch limits.
