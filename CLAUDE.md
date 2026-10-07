# Project Instructions

## Running Python files
- Always use `python` to run files (e.g., `python script.py`), not `py`, `python3`, or any other launcher.

## Git commits
- Never include a `Co-Authored-By:` line (or any co-author attribution) in commit messages.
- Never stage or commit files listed in `.gitignore` (do not use `git add -f` to bypass it).

## Secrets
- Never read, print, or write API keys, tokens, or `.env` contents into chat, files, or commit messages.
- If a secret is exposed, stop and tell the user to rotate it.

## LLM API calls
- Always set an explicit `max_tokens` on `chat.completions.create` calls (OpenRouter free tier reserves credits up-front).
- Default to small caps (e.g., 500) for experiments unless the prompt clearly needs more.
- **When a Python program is pasted:** Automatically convert it to use the local model server at `http://127.0.0.1:1234` (OpenAI-compatible API with `api_key="local"`) instead of any remote API provider. Never use external API keys for pasted scripts.

## Git safety
- Never run destructive git commands (`reset --hard`, `push --force`, `clean -f`, `branch -D`) without confirmation.
- Never push to a remote unless explicitly asked.
- Always run `git status` before suggesting a commit, and verify `.env` and other ignored files aren't staged.

## Local model server (http://127.0.0.1:1234)
Available models:
- `qwen/qwen3.6-35b-a3b` — Qwen 3.6 (chat/completions)
- `google/gemma-4-12b-qat` — Google Gemma 4
- `text-embedding-nomic-embed-text-v1.5` — Embeddings

When converting scripts to use the local server, use these exact model IDs, not alternative names.
- Qwen and Gemma are thinking models: reasoning tokens count toward `max_tokens`. Caps of ~100-500 can return an empty `content`. Use 1000+ (2000 for structured/JSON output).
- The server rejects `response_format={"type": "json_object"}` (only `json_schema` or `text`). Ask for JSON in the prompt instead.
