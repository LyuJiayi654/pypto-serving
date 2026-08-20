# Generation Arguments

Generation controls are available in both offline entries and HTTP request
bodies. HTTP request fields override server defaults.

## Common Controls

| Field or option | Default | Meaning |
| --- | --- | --- |
| `max_tokens` / `--max-new-tokens` | entry-specific | Maximum generated tokens. |
| `temperature` / `--temperature` | `0.0` in common examples | Sampling temperature. |
| `top_p` / `--top-p` | `1.0` | Nucleus sampling cutoff. |
| `top_k` / `--top-k` | disabled | Top-k sampling cutoff. |
| `stop` / `--stop` | empty | Stop strings. |
| `stream` / `--stream` | false | Stream text deltas. |

## HTTP Completions

`/v1/completions` accepts:

- `model`
- `prompt`
- `max_tokens`
- `temperature`
- `top_p`
- `top_k`
- `stop`
- `stream`

## HTTP Chat Completions

`/v1/chat/completions` accepts:

- `model`
- `messages`
- `max_tokens`
- `temperature`
- `top_p`
- `top_k`
- `stop`
- `stream`
- `chat_template_kwargs`

`chat_template_kwargs` is forwarded to the tokenizer's `apply_chat_template`.

## EOS Handling

Offline entries expose model-specific EOS behavior. The DeepSeek V4 offline
entry has `--ignore-eos`; the HTTP completion path ignores EOS for completion
requests and uses standard generation behavior for chat requests.
