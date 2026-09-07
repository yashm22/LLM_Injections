"""Local Ollama provider for the prompt-injection test runner."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from urllib.error import URLError
from urllib.request import Request, urlopen


def run_ollama_conversation(
    turns: list[str], system_prompt: str, canary: str, on_turn_start: Callable[[int, int], None] | None = None
) -> list[str]:
    """Send an ordered conversation to Ollama's local /api/chat endpoint."""
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = os.environ.get("OLLAMA_MODEL", "qwen3:4b")
    messages = [{"role": "system", "content": f"{system_prompt}\nInternal test canary: {canary}"}]
    outputs = []

    for turn_number, turn in enumerate(turns, start=1):
        if on_turn_start:
            on_turn_start(turn_number, len(turns))
        messages.append({"role": "user", "content": turn})
        body = json.dumps({"model": model, "messages": messages, "stream": False}).encode("utf-8")
        request = Request(
            f"{base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=300) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except URLError as error:
            raise RuntimeError(
                f"Could not reach Ollama at {base_url}. Start Ollama, then run `ollama run {model}`. ({error.reason})"
            ) from error
        output = payload["message"]["content"]
        outputs.append(output)
        messages.append({"role": "assistant", "content": output})

    return outputs
