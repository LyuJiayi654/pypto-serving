# Model Support Matrix

PyPTO Serving intentionally supports a small set of model and feature
combinations. This matrix is the public compatibility contract for the docs.

## Models

| Model family | Checkpoint layout | Devices | Parallelism | Offline | HTTP serving | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3-14B | Hugging Face style checkpoint | One or more Ascend NPUs | Single device, TP offline, DP online replicas | Supported | Supported | Uses the Qwen model loader, tokenizer, NPU executor, and PyPTO kernels. |
| DeepSeek V4 Flash W8A8 | Converted compressed-tensors checkpoint | Exactly eight Ascend NPUs | Overlapped attention DP=8 and MoE EP=8, TP=1 | Supported | Supported | Requires `--dp 8 --ep 8 --tp 1` and `--block-size 128`. |

See [Qwen3-14B](qwen.md) and [DeepSeek V4](deepseek-v4.md) for complete command
lines and model-specific runtime notes.

## Serving Features

| Feature | Qwen3-14B | DeepSeek V4 Flash W8A8 | Notes |
| --- | --- | --- | --- |
| Text generation | Supported | Supported | Offline and HTTP paths share the serving engine. |
| `/v1/completions` | Supported | Supported | See [vLLM Compatibility](vllm-compatibility.md). |
| `/v1/chat/completions` | Supported | Supported | DeepSeek V4 uses model-specific message encoding. |
| Streaming | Supported | Supported | Completion and chat streams use Server-Sent Events. |
| Usage counts | Supported | Supported | Non-streaming responses and terminal stream chunks include token counts. |
| Continuous batching | Supported | Supported | Scheduler behavior is controlled by runtime capacity settings. |
| Paged KV cache | Supported | Supported | DeepSeek V4 uses grouped, model-specific cache pools. |
| Chunked prefill | Supported | Supported | Enabled by default; controlled by CLI flags. |
| Prefix caching | Supported | Limited | Qwen enables it by default. Routine DeepSeek V4 serving should disable it. |
| MTP speculative decoding | Not supported | Supported | Use `--speculative-config '{"method":"mtp","num_speculative_tokens":K}'`. |
| General speculative decoding | Not supported | Not supported | Draft-model, n-gram, EAGLE, and suffix speculation are not exposed. |
| Logprobs and prompt logprobs | Not supported | Not supported | Request schemas do not expose logprob fields. |
| Beam search and best-of | Not supported | Not supported | Generation uses greedy or sampling controls only. |
| Structured outputs | Not supported | Not supported | JSON schema, grammar, and guided decoding are not exposed. |
| Tool calling | Not supported | Not supported | Tool schemas and tool-call response parsing are not exposed. |
| Multimodal inputs | Not supported | Not supported | Chat content is string-only. |
| Embeddings and pooling | Not supported | Not supported | `/v1/embeddings` is not exposed. |
| LoRA adapters | Not supported | Not supported | Runtime adapter loading is not exposed. |
| General quantization matrix | Not supported | Limited | DeepSeek V4 uses the validated W8A8 conversion path only. |

## Hardware Scope

The public runtime backend is Ascend NPU with PyPTO kernels. `--backend npu` is
the only documented backend. CPU, CUDA, ROCm, XPU, TPU, Apple Silicon, and other
vLLM hardware backends are outside the PyPTO Serving docs contract.

## Adding a Model

New models need more than a Hugging Face `config.json`. A model integration must
provide the model loader, tokenizer behavior, weight staging rules, executor,
runner, KV cache contract, PyPTO kernel layout, and NPU validation. Start with
[Model Integration](../developer-guide/model-integration.md).
