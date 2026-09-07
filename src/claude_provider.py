"""Anthropic Claude API provider for the prompt-injection test runner."""

from __future__ import annotations

import os
from collections.abc import Callable


def run_claude_conversation(
    turns: list[str], system_prompt: str, canary: str, on_turn_start: Callable[[int, int], None] | None = None
) -> list[str]:
    """Send full conversation history to Claude's stateless Messages API."""
    from anthropic import Anthropic

    client = Anthropic()
    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
    max_tokens = int(os.environ.get("CLAUDE_MAX_TOKENS", "1024"))
    messages = []
    outputs = []

    for turn_number, turn in enumerate(turns, start=1):
        if on_turn_start:
            on_turn_start(turn_number, len(turns))
        messages.append({"role": "user", "content": turn})
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=f"{system_prompt}\nInternal test canary: {canary}",
            messages=messages,
        )
        output = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        outputs.append(output)
        messages.append({"role": "assistant", "content": output})

    return outputs
