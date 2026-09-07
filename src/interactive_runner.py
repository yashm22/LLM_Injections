"""Interactive launcher for choosing a provider and model before a test run."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from . import test_runner

ROOT = Path(__file__).resolve().parents[1]

def choose_provider() -> str:
    options = {"1": "ollama", "2": "openai", "3": "claude", "4": "mock"}
    print("Choose a provider:")
    print("  1. Ollama (local, no API key)")
    print("  2. OpenAI API (requires OPENAI_API_KEY in .env)")
    print("  3. Claude API (requires ANTHROPIC_API_KEY in .env)")
    print("  4. Mock (offline demonstration)")
    while True:
        choice = input("Provider : ").strip() or "1"
        if choice in options:
            return options[choice]
        print("Enter 1, 2, 3, or 4.")


def choose_model(provider: str) -> None:
    if provider == "ollama":
        default = os.environ.get("OLLAMA_MODEL", "qwen3:4b")
        model = input(f"Ollama model [{default}]: ").strip() or default
        os.environ["OLLAMA_MODEL"] = model
    elif provider == "openai":
        default = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
        print(default)
        model = input(f"OpenAI model [{default}]: ").strip() or default
        os.environ["OPENAI_MODEL"] = model
    elif provider == "claude":
        default = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
        model = input(f"Claude model [{default}]: ").strip() or default
        os.environ["CLAUDE_MODEL"] = model
    else:
        print("Mock mode does not use a model.")


def choose_suite() -> str:
    options = {
        "1": "single-turn",
        "2": "multi-turn",
        "3": "real-world",
        "4": "all",
    }
    print("\nChoose a test suite:")
    print("  1. Single-turn attacks (50 cases)")
    print("  2. Multi-turn attacks (50 cases)")
    print("  3. Real-world scenarios (16 cases)")
    print("  4. All tests (116 cases)")
    while True:
        choice = input("Suite [4]: ").strip() or "4"
        if choice in options:
            return options[choice]
        print("Enter 1, 2, 3, or 4.")


def main() -> None:
    load_dotenv(ROOT / ".env")
    provider = choose_provider()
    choose_model(provider)
    suite = choose_suite()
    print(f"\nStarting the {suite} suite with {provider}...\n")
    test_runner.main(["--provider", provider, "--suite", suite])


if __name__ == "__main__":
    main()
