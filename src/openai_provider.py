"""OpenAI API provider for the prompt-injection test runner."""

from __future__ import annotations

import os
from collections.abc import Callable


def run_openai_conversation(
    turns: list[str], system_prompt: str, canary: str, on_turn_start: Callable[[int, int], None] | None = None
) -> list[str]:
    """Send an ordered conversation through the OpenAI Responses API."""
    from openai import OpenAI

    client = OpenAI()
    model = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
    previous_response_id = None
    outputs = []
    for turn_number, turn in enumerate(turns, start=1):
        if on_turn_start:
            on_turn_start(turn_number, len(turns))
        request = {
            "model": model,
            "instructions": f"{system_prompt}\nInternal test canary: {canary}",
            "input": turn,
        }
        if previous_response_id:
            request["previous_response_id"] = previous_response_id
        response = client.responses.create(**request)
        previous_response_id = response.id
        outputs.append(response.output_text)
    return outputs
