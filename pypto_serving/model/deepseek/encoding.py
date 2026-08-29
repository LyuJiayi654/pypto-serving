# Copyright (c) PyPTO Contributors.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# -----------------------------------------------------------------------------------------------------------

from __future__ import annotations

from collections.abc import Mapping, Sequence


BOS_TOKEN = "<｜begin▁of▁sentence｜>"
EOS_TOKEN = "<｜end▁of▁sentence｜>"
USER_TOKEN = "<｜User｜>"
ASSISTANT_TOKEN = "<｜Assistant｜>"
LATEST_REMINDER_TOKEN = "<｜latest_reminder｜>"
THINKING_START_TOKEN = "<think>"
THINKING_END_TOKEN = "</think>"

_MAX_REASONING_EFFORT_PROMPT = (
    "Reasoning Effort: Absolute maximum with no shortcuts permitted.\n"
    "You MUST be very thorough in your thinking and comprehensively decompose the problem to resolve "
    "the root cause, rigorously stress-testing your logic against all potential paths, edge cases, and "
    "adversarial scenarios.\n"
    "Explicitly write out your entire deliberation process, documenting every intermediate step, "
    "considered alternative, and rejected hypothesis to ensure absolutely no assumption is left "
    "unchecked.\n\n"
)


def encode_messages(
    messages: Sequence[Mapping[str, object]],
    *,
    thinking: bool = False,
    reasoning_effort: str | None = None,
) -> str:
    """Encode the string-only OpenAI messages supported by PyPTO for DeepSeek V4."""
    if not messages:
        raise ValueError("DeepSeek V4 chat requests require at least one message")

    if reasoning_effort == "none":
        thinking = False

    parts = [BOS_TOKEN]
    if thinking and reasoning_effort in {"max", "xhigh"}:
        parts.append(_MAX_REASONING_EFFORT_PROMPT)

    last_user_index = max(
        (index for index, message in enumerate(messages) if message.get("role") in {"user", "developer"}),
        default=-1,
    )
    for index, message in enumerate(messages):
        role = message.get("role")
        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("DeepSeek V4 chat message content must be a string")

        if role == "system":
            parts.append(content)
        elif role in {"user", "developer"}:
            parts.extend((USER_TOKEN, content))
        elif role == "latest_reminder":
            parts.extend((LATEST_REMINDER_TOKEN, content))
        elif role == "assistant":
            parts.extend((content, EOS_TOKEN))
        else:
            raise ValueError(f"DeepSeek V4 does not support chat message role {role!r}")

        next_role = messages[index + 1].get("role") if index + 1 < len(messages) else None
        if role in {"user", "developer"} and (next_role == "assistant" or next_role is None):
            parts.append(ASSISTANT_TOKEN)
            parts.append(
                THINKING_START_TOKEN
                if thinking and index >= last_user_index
                else THINKING_END_TOKEN
            )

    return "".join(parts)
