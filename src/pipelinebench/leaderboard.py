from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from pipelinebench.schema import LeaderboardOutput, ValidationResult


def build_leaderboard(
    results_payload: Iterable[dict[str, object] | ValidationResult],
) -> LeaderboardOutput:
    results = [
        item if isinstance(item, ValidationResult) else ValidationResult.model_validate(item)
        for item in results_payload
    ]
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    pass_rate = (passed / total * 100) if total else 0.0
    total_duration = sum(result.duration_seconds for result in results)

    rows = [
        "| Task | Category | Difficulty | Result | Tests | Duration |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ]
    for result in sorted(results, key=lambda item: item.task_id):
        status = "PASS" if result.passed else "FAIL"
        tests = result.test_count if result.test_count is not None else "-"
        rows.append(
            f"| `{result.task_id}` | {result.category} | {result.difficulty} | "
            f"{status} | {tests} | {result.duration_seconds:.3f}s |"
        )

    markdown = "\n".join(
        [
            "# PipelineBench Leaderboard",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Tasks | {total} |",
            f"| Passed | {passed} |",
            f"| Pass rate | {pass_rate:.1f}% |",
            f"| Total duration | {total_duration:.3f}s |",
            "",
            "## Task Results",
            "",
            *rows,
            "",
        ]
    )
    summary: dict[str, object] = {
        "total_tasks": total,
        "passed_tasks": passed,
        "pass_rate": round(pass_rate / 100, 4),
        "total_duration_seconds": round(total_duration, 3),
        "tasks": [result.model_dump(mode="json") for result in results],
    }
    return LeaderboardOutput(markdown=markdown, summary=summary)


def write_leaderboard(leaderboard: LeaderboardOutput, output_prefix: Path) -> tuple[Path, Path]:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    markdown_path = output_prefix.with_suffix(".md")
    json_path = output_prefix.with_suffix(".json")
    markdown_path.write_text(leaderboard.markdown, encoding="utf-8")
    json_path.write_text(json.dumps(leaderboard.summary, indent=2) + "\n", encoding="utf-8")
    return markdown_path, json_path
