# 🤖 OpenRouter Code Agent

A minimal, from-scratch AI coding agent built in Python. It talks to any model on [OpenRouter](https://openrouter.ai) through an OpenAI-compatible API, and gives the LLM four tools it can call on its own — list files, read files, write files, and run Python scripts — inside a sandboxed working directory.

Built as part of a [boot.dev](https://boot.dev) AI/backend challenge, using OpenRouter instead of the usual provider.

## What it does

You give it a plain-English instruction — "what does main.py do?" or "add a modulo operator to the calculator" — and the agent:

1. Sends your prompt, a system prompt, and a list of available tools to an LLM via OpenRouter.
2. Reads the model's response. If it wants to call a tool (e.g. "read calculator/main.py"), the agent executes that function locally.
3. Feeds the tool's result back to the model as part of the conversation.
4. Repeats — up to 20 iterations — until the model responds with a final plain-text answer instead of another tool call.

This loop is the core of every "agentic" coding tool (Claude Code, Cursor, Aider, etc.), built by hand here to understand what's actually happening under the hood.

## Tools available to the agent

| Tool               | What it does                                                                |
| ------------------ | --------------------------------------------------------------------------- |
| `get_files_info`   | Lists files and directories, with sizes                                     |
| `get_file_content` | Reads a file's contents (truncated at 10,000 characters)                    |
| `write_file`       | Writes or overwrites a file                                                 |
| `run_python_file`  | Executes a `.py` file, optionally with arguments, and returns stdout/stderr |

For safety, every path the agent touches is resolved relative to a fixed working directory — the model can't read or write anything outside of it, even if it tries.

## Why "calculator"?

The repo ships with a small sample Python project (a calculator CLI) inside `calculator/` for the agent to operate on — read its code, debug it, extend it, and so on. It's the sandbox the agent plays in, not the point of the project. Point `WORKING_DIR` in `config.py` at any other folder and the agent will operate there instead.

## Getting started

### Prerequisites

- Python 3.14+
- An [OpenRouter API key](https://openrouter.ai/keys) (the free tier works — the agent defaults to the `openrouter/free` model)
- [uv](https://docs.astral.sh/uv/) (recommended — the repo includes a `uv.lock`), or plain `pip`

### Install

```bash
git clone https://github.com/acjr1910/ai-agent.git
cd ai-agent
uv sync            # or: pip install -e .
```

### Configure

```bash
cp .env.sample .env
```

Then add your key to `.env`:

```
OPENROUTER_API_KEY=sk-or-...
```

### Run it

```bash
uv run main.py "list the files in the working directory"
uv run main.py "what does calculator.py do?"
uv run main.py "add a modulo operator to the calculator" --verbose
```

`--verbose` prints prompt/response token usage and each tool call's result as the agent works, which is handy for seeing the loop in action.

## Project structure

```
ai-agent/
├── main.py           # CLI entry point and the agent's tool-calling loop
├── prompts.py         # System prompt
├── config.py           # Working directory + output size limits
├── functions/            # Tool implementations exposed to the LLM
├── calculator/             # Sample project the agent reads/edits/runs
├── test_*.py                # Unit tests for each tool
└── .env.sample
```

## Testing

```bash
uv run pytest
```

## Built with

- [OpenRouter](https://openrouter.ai) — model routing via an OpenAI-compatible API
- `openai` Python SDK, pointed at OpenRouter's base URL
- `python-dotenv` for config

## Notes / limitations

- Single-threaded and synchronous — no persistent chat history between runs, each invocation starts fresh.
- Hard-capped at 20 tool-call iterations per prompt to avoid runaway loops.
- Built for learning — not hardened for untrusted input or production use.

## License

No license file yet — add one (MIT is a common, permissive choice for learning projects like this) if you want others to be able to reuse the code.
