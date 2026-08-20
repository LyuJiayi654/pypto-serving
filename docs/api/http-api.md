# HTTP API

PyPTO Serving exposes a focused OpenAI-compatible HTTP API subset. This page is
the precise reference for the current server routes.

## `GET /health`

Returns:

```json
{"status":"ok"}
```

## `GET /v1/models`

Returns the served model name:

```json
{
  "object": "list",
  "data": [
    {"id": "Qwen3-14B", "object": "model", "owned_by": "pypto"}
  ]
}
```

## `POST /v1/completions`

Request:

```json
{
  "model": "",
  "prompt": "Huawei is",
  "max_tokens": 32,
  "temperature": 0.0,
  "top_p": 1.0,
  "top_k": null,
  "stop": null,
  "stream": false
}
```

Response:

```json
{
  "id": "cmpl-...",
  "object": "text_completion",
  "created": 0,
  "model": "Qwen3-14B",
  "choices": [
    {"index": 0, "text": "...", "finish_reason": "length"}
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

## `POST /v1/chat/completions`

Request:

```json
{
  "model": "",
  "messages": [
    {"role": "user", "content": "What is 1+1?"}
  ],
  "max_tokens": 32,
  "temperature": 0.0,
  "top_p": 1.0,
  "top_k": null,
  "stop": null,
  "stream": false,
  "chat_template_kwargs": null
}
```

The server applies the tokenizer chat template before generation.

## Streaming

When `stream` is true, responses are Server-Sent Events. The stream ends with:

```text
data: [DONE]
```

The terminal usage event has empty `choices`.

## Finish Reasons

Internal finish reasons are mapped to:

| API value | Meaning |
| --- | --- |
| `eos` | The model produced EOS. |
| `length` | The request reached `max_tokens` or model length. |
| `stop` | A stop string matched or an unknown finish state was normalized. |
| `aborted` | The request was aborted. |

## Errors

`ValueError` exceptions are returned as HTTP 400:

```json
{"object":"error","message":"..."}
```
