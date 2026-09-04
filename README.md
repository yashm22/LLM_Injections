# LLM Prompt Injection Tester

Local test harness for evaluating prompt-injection defenses in an LLM-backed application.

The bundled test set covers direct overrides, authority claims, role-play escapes,
prompt extraction, delimiter and encoding confusion, indirect document and web
injections, unauthorized tool-use requests, data exfiltration, multi-turn attacks,
and a benign control.

## Setup

1. Install Python 3.12 for Windows if it is not already installed:

   ```powershell
   winget install Python.Python.3.12
   ```

   If `python --version` still opens the Microsoft Store after installing, this
   project will use the standard Python 3.12 installation path automatically.

2. Create the virtual environment and install dependencies:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
   ```

   This is a one-time execution-policy bypass for the setup command; it does
   not change your permanent PowerShell policy.

3. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If activation is blocked, allow scripts for the current PowerShell window
   only, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

4. Run the offline demo (no API key required):

   ```powershell
   python -m src.test_runner --provider mock
   ```

5. To run a local model through Ollama (no API key required), install Ollama,
   download a model once, and run the suite:

   ```powershell
   ollama run qwen3:4b
   python -m src.test_runner --provider ollama --suite all
   ```

   `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in `.env` can change the local server
   address or model name. The default endpoint is `http://localhost:11434`.
   The Ollama-only integration is kept in `src/ollama_provider.py`.

6. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if using the OpenAI API. Then run against OpenAI:

   ```powershell
   python -m src.test_runner --provider openai
   ```

## Interactive launcher

To choose the provider and model each time, run:

```powershell
python -m src.interactive_runner
```

Choose Ollama, OpenAI API, or mock mode when prompted. Ollama-specific code is
in `src/ollama_provider.py`; OpenAI-specific code is in `src/openai_provider.py`.
The launcher then lets you select the single-turn suite, multi-turn suite, or
all 100 tests.

Results are written to `results/`. Use only systems you own or are authorized to test. Test canaries are fake by design.
The grader detects the protected canary in plain text and common reversible forms,
including Base64, hexadecimal, ROT13, reversed, spaced, and fragmented output.
Every run displays live progress for each test case, including its number, ID,
turn count, status, and elapsed time. Errors are recorded per case so the rest
of the suite can continue running.

Multi-turn cases use a `turns` array. The runner preserves the conversation with
the target model and fails the case if a prohibited marker appears in *any* turn.
The bundled suites are separate files in `cases/` and can be selected with:

```powershell
python -m src.test_runner --provider mock --suite single-turn
python -m src.test_runner --provider mock --suite multi-turn
python -m src.test_runner --provider mock --suite all
```

## Sources and next steps

The categories are informed by public red-team frameworks, including NVIDIA Garak,
Promptfoo, AgentDojo, and Microsoft BIPIA. The advanced cases cover encoding and
Unicode-style smuggling, structured-data boundary confusion, forged authority,
cross-source trust transfer, delayed activation, and multi-turn escalation. Keep
this curated suite as a baseline, then add cases that simulate your own application
inputs, tools, user roles, and retrieval sources.
