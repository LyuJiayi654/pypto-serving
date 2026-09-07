# vLLM Compatibility

PyPTO Serving follows a small, explicit subset of the vLLM and OpenAI-compatible
serving surface. It is not a drop-in replacement for vLLM. Use this page to
decide whether a vLLM client, benchmark, or deployment recipe can run unchanged
against `pypto-serving`.

The reference point is the public vLLM documentation at
[docs.vllm.ai](https://docs.vllm.ai/en/stable/).

## Scope

PyPTO Serving is focused on local generation with PyPTO kernels on Ascend NPUs.
The supported model families are listed in [Model Support Matrix](model-support.md).

The compatible surface is:

- OpenAI-style completions and chat completions for text generation.
- OpenAI-style model listing.
- Server-Sent Events streaming for completions and chat completions.
- vLLM-style profiling control endpoints when profiling is enabled.
- vLLM-style `--speculative-config` for DeepSeek V4 MTP speculative decoding.

The project does not expose the vLLM Python `LLM` API, vLLM engine classes, vLLM
worker plugins, or vLLM's generated API reference.

## Endpoint Matrix

| Endpoint | Status | Notes |
| --- | --- | --- |
| `/health` | Supported | Returns `{"status":"ok"}`. |
| `/v1/models` | Supported | Returns the served model name. |
| `/v1/completions` | Supported | Text prompt generation. The request `prompt` is a string. |
| `/v1/chat/completions` | Supported | String-content chat messages only. |
| `/start_profile` | Supported with `--profile` | Starts profiling in the API process and workers. |
| `/stop_profile` | Supported with `--profile` | Stops profiling and merges trace fragments. |
| `/v1/chat/completions/batch` | Not supported | Use repeated requests or offline repeated `--prompt` values. |
| `/v1/responses` | Not supported | The docs section named response schema is about response objects, not this API. |
| `/v1/embeddings` | Not supported | Pooling and embedding models are not exposed. |
| `/v1/audio/transcriptions` | Not supported | Speech-to-text models are not exposed. |
| `/v1/audio/translations` | Not supported | Speech-to-text models are not exposed. |

## Completion Request Fields

`/v1/completions` consumes the following fields:

| Field | Meaning |
| --- | --- |
| `model` | Optional response model name. It does not switch the loaded checkpoint. |
| `prompt` | Prompt text. Only a single string prompt is part of the public schema. |
| `max_tokens` | Maximum generated tokens for this request. |
| `temperature` | Sampling temperature. |
| `top_p` | Nucleus sampling cutoff. |
| `top_k` | Top-k sampling cutoff. |
| `seed` | Per-request sampling seed when the model path uses seeded sampling. |
| `stop` | Stop strings. An explicit empty list clears server defaults. |
| `stream` | Return Server-Sent Events instead of a single JSON response. |

Unsupported vLLM and OpenAI completion fields, such as `suffix`, `logprobs`,
`prompt_logprobs`, `best_of`, `use_beam_search`, `response_format`,
`structured_outputs`, `priority`, `guided_*`, and prompt embedding inputs, are
not part of the PyPTO Serving contract.

## Chat Request Fields

`/v1/chat/completions` consumes the following fields:

| Field | Meaning |
| --- | --- |
| `model` | Optional response model name. It does not switch the loaded checkpoint. |
| `messages` | Ordered chat messages with string `role` and string `content`. |
| `max_tokens` | Maximum generated tokens for this request. |
| `temperature` | Sampling temperature. |
| `top_p` | Nucleus sampling cutoff. |
| `top_k` | Top-k sampling cutoff. |
| `seed` | Per-request sampling seed when the model path uses seeded sampling. |
| `stop` | Stop strings. An explicit empty list clears server defaults. |
| `stream` | Return Server-Sent Events instead of a single JSON response. |
| `reasoning_effort` | Forwarded to model-specific chat templating for models that use it. |
| `chat_template_kwargs` | Extra tokenizer chat-template keyword arguments. |

The current chat schema accepts string content only. Tool calls, tool-choice
controls, multimodal message parts, structured outputs, parallel tool calls,
reasoning-output parsers, and OpenAI Responses API sessions are not exposed by
the request schema.

## Defaults and Overrides

Generation defaults are resolved in this order:

1. Fields present in an HTTP request.
2. Fields provided by `--generate-config` when starting `pypto-serving`.
3. The built-in `GenerateConfig` defaults.

This mirrors the practical vLLM client workflow where per-request parameters
override server defaults, but the set of accepted fields is much smaller.

## Streaming Behavior

Streaming responses use Server-Sent Events:

```text
data: {...}

data: [DONE]
```

Completion streams put text deltas in `choices[0].text`. Chat streams put text
deltas in `choices[0].delta.content`.

PyPTO Serving emits a terminal usage chunk with an empty `choices` list and
authoritative token counts before `data: [DONE]`. This is compatible with vLLM
benchmark parsers that read `usage.completion_tokens` from the stream.

The request schema does not expose vLLM's broader `stream_options` controls.

## OpenAI Python Client

Point the OpenAI client at the PyPTO Serving base URL and use only the supported
fields:

```python
from openai import OpenAI


client = OpenAI(base_url="http://127.0.0.1:8899/v1", api_key="unused")

completion = client.completions.create(
    model="Qwen3-14B",
    prompt="Huawei is",
    max_tokens=32,
    temperature=0.0,
)
print(completion.choices[0].text)

chat = client.chat.completions.create(
    model="Qwen3-14B",
    messages=[{"role": "user", "content": "What is 1+1?"}],
    max_tokens=32,
)
print(chat.choices[0].message.content)
```

Keep vLLM-specific `extra_body` parameters out of portable clients unless this
page lists the field explicitly.

## Migration Checklist

- Replace `vllm serve` with `pypto-serving`.
- Replace vLLM engine arguments with the options in
  [Runtime Capacity](../configuration/runtime-capacity.md).
- Keep only the request fields listed above.
- Confirm the model appears in [Model Support Matrix](model-support.md).
- Use [Benchmarking](benchmarking.md) for compatible benchmark client settings.
- Use [Troubleshooting](troubleshooting.md) when a vLLM recipe assumes unsupported
  endpoints, model families, or deployment plugins.
