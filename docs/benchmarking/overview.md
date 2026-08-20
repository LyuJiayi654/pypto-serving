# Benchmarking Overview

Benchmark PyPTO Serving at two levels:

- Offline generation for a single process or controlled batch.
- HTTP serving for request latency, throughput, and concurrency behavior.

Use profiling when you need to explain where time is spent. Use benchmarking
when you need externally visible throughput or latency numbers.

## Recommended Reporting Fields

Record the following with every result:

- Git commit.
- Model and checkpoint path.
- Platform and device IDs.
- Command line.
- Prompt length and generated token count.
- `--max-model-len`, `--max-num-seqs`, and `--max-num-batched-tokens`.
- Whether compile cache or prepacked weights were used.
- Whether profiling was enabled.

## Warmup

Separate first-run startup cost from steady-state generation. Kernel compile
and checkpoint packing work can dominate first launch results.
