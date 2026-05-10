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

## Git safety
- Never run destructive git commands (`reset --hard`, `push --force`, `clean -f`, `branch -D`) without confirmation.
- Never push to a remote unless explicitly asked.
- Always run `git status` before suggesting a commit, and verify `.env` and other ignored files aren't staged.
