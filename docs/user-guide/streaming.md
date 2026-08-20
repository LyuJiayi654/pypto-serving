# Streaming

Set `stream: true` on completion or chat completion requests to receive text
deltas as Server-Sent Events.

## Completion Stream

```bash
curl --noproxy "*" http://127.0.0.1:8899/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Huawei is","max_tokens":32,"stream":true}'
```

Each event contains a completion chunk with one choice. The final non-`DONE`
event contains usage counts and an empty `choices` list.

## Chat Stream

```bash
curl --noproxy "*" http://127.0.0.1:8899/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Write one sentence."}],"max_tokens":32,"stream":true}'
```

Chat chunks use `object: chat.completion.chunk` and return deltas under
`choices[0].delta.content`.

## Client Expectations

- Read events until `data: [DONE]`.
- Accumulate `choices[0].text` for completions.
- Accumulate `choices[0].delta.content` for chat completions.
- Read usage from the terminal usage chunk, not from intermediate chunks.
