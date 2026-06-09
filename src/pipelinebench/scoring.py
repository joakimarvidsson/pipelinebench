from __future__ import annotations

from pipelinebench.schema import ValidationResult


def pass_rate(results: list[ValidationResult]) -> float:
    if not results:
        return 0.0
    return sum(1 for result in results if result.passed) / len(results)
