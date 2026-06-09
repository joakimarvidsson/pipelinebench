from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Difficulty = Literal["easy", "medium", "hard"]
ScoringType = Literal["pytest"]


class ScoringConfig(BaseModel):
    """Scoring configuration for a benchmark task."""

    type: ScoringType = "pytest"
    pass_threshold: float = Field(ge=0.0, le=1.0)


class TaskSpec(BaseModel):
    """Validated task.yaml metadata."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9_]*$")
    title: str = Field(min_length=3)
    category: str = Field(min_length=2)
    difficulty: Difficulty
    skills: list[str] = Field(min_length=1)
    entrypoint: str
    expected_outputs: list[str] = Field(min_length=1)
    time_budget_minutes: int = Field(gt=0)
    allowed_files: list[str] = Field(min_length=1)
    validation_command: str = Field(min_length=1)
    scoring: ScoringConfig
    task_dir: Path | None = None

    @field_validator("skills", "expected_outputs", "allowed_files")
    @classmethod
    def reject_blank_items(cls, values: list[str]) -> list[str]:
        blank = [value for value in values if not value.strip()]
        if blank:
            msg = "list values must not be blank"
            raise ValueError(msg)
        return values


class ValidationResult(BaseModel):
    """Serializable result for one validation command."""

    task_id: str
    title: str
    category: str
    difficulty: Difficulty
    passed: bool
    duration_seconds: float
    command: str
    return_code: int
    stdout_tail: str
    stderr_tail: str
    started_at: str
    finished_at: str
    workspace_path: str
    test_count: int | None = None
    error_summary: str = ""


class LeaderboardOutput(BaseModel):
    """Rendered leaderboard artifacts."""

    markdown: str
    summary: dict[str, object]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
