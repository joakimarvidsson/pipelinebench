from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentAdapter:
    """Manual workflow instructions for an agent tool."""

    name: str
    command_hint: str
    instructions: tuple[str, ...]


def get_adapters() -> list[AgentAdapter]:
    common = (
        "Run `pipelinebench run-task TASK_ID --workspace .workspaces/TASK_ID`.",
        "Open `.workspaces/TASK_ID` in the agent tool.",
        "Give the agent `problem.md` and ask it to make `python -m pytest tests` pass.",
        "Run `pipelinebench evaluate TASK_ID --submission .workspaces/TASK_ID`.",
        "Save the result JSON and generate a leaderboard.",
    )
    return [
        AgentAdapter("Claude Code", "claude .workspaces/TASK_ID", common),
        AgentAdapter("Codex", "codex .workspaces/TASK_ID", common),
        AgentAdapter("Cursor", "cursor .workspaces/TASK_ID", common),
        AgentAdapter("Antigravity", "Open the workspace folder in Antigravity.", common),
        AgentAdapter("OpenCode", "opencode .workspaces/TASK_ID", common),
        AgentAdapter(
            "OpenAI-compatible local endpoint",
            "Use your local agent wrapper against `.workspaces/TASK_ID`.",
            common,
        ),
        AgentAdapter("Ollama/Qwen/Kimi local model", "Run your local coding-agent loop.", common),
    ]
