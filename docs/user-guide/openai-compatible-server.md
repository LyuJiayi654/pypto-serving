# OpenAI-Compatible Server

PyPTO Serving implements a focused OpenAI-compatible HTTP API subset. The
server is intended for clients that need basic completions, chat completions,
model listing, health checks, and streaming.

## Supported Endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | `GET` | Return server health. |
| `/v1/models` | `GET` | Return the served model name. |
| `/v1/completions` | `POST` | Generate text from a prompt. |
| `/v1/chat/completions` | `POST` | Apply the tokenizer chat template and generate a response. |
| `/start_profile` | `POST` | Start profiling when the server was launched with `--profile`. |
| `/stop_profile` | `POST` | Stop profiling and merge trace fragments. |

## Request Fields

Completions accept:

- `model`
- `prompt`
- `max_tokens`
- `temperature`
- `top_p`
- `top_k`
- `stop`
- `stream`

Chat completions accept:

- `model`
- `messages`
- `max_tokens`
- `temperature`
- `top_p`
- `top_k`
- `stop`
- `stream`
- `chat_template_kwargs`

Unsupported OpenAI fields are ignored only if the request model allows them as
extra data. Treat this as a subset, not a drop-in replacement for every OpenAI
or vLLM server feature.

## Chat Templates

Chat requests are converted to a prompt by the model tokenizer's official
`apply_chat_template` method. `chat_template_kwargs` is forwarded to the
tokenizer, which allows model-specific controls such as Qwen thinking-mode
options when the tokenizer supports them.

## Streaming

Streaming responses use Server-Sent Events. Each chunk is emitted as
`data: {...}` and the stream ends with:

```text
data: [DONE]
```

The terminal usage chunk has empty `choices` and authoritative token counts.
