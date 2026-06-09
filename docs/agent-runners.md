# Agent Runners

PipelineBench v0.1 is agent-agnostic. It prepares local workspaces and leaves agent operation to the
user.

## Standard workflow

```bash
uv run pipelinebench run-task TASK_ID --workspace .workspaces/TASK_ID
```

Then:

1. Open `.workspaces/TASK_ID` in your chosen agent or editor.
2. Give the agent `problem.md`.
3. Ask it to make `python -m pytest tests` pass.
4. Run:

```bash
uv run pipelinebench evaluate TASK_ID --submission .workspaces/TASK_ID
```

## Tool hints

Claude Code:

```bash
claude .workspaces/TASK_ID
```

Codex:

```bash
codex .workspaces/TASK_ID
```

Cursor:

```bash
cursor .workspaces/TASK_ID
```

Antigravity:

Open the workspace folder and point the agent at `problem.md`.

OpenCode:

```bash
opencode .workspaces/TASK_ID
```

Local OpenAI-compatible endpoint, Ollama, Qwen, or Kimi:

Run your local coding-agent loop against the workspace folder. The task does not require network
access after dependencies are installed.
