"""Small fail-closed helpers for independent controlled-evaluation proofs.

The helper compares a producer artifact with a fresh reconstruction made from
the canonical fixture and engine.  Producer aggregate fields are deliberately
ignored; case identity, canonical case content, and required collections are
checked independently.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


_AGGREGATE_FIELDS = {
    "all_checks_passed",
    "passed_count",
    "final_decision",
    "cognitive_logic_result",
    "operational_result",
    "failed_checks",
    "checks",
}


def independent_case_proof(
    observed: Mapping[str, Any],
    recompute: Callable[[], Mapping[str, Any]],
    *,
    source: str,
    collections: tuple[str, ...] = ("cases",),
    compare_top_level: tuple[str, ...] = (),
) -> dict[str, bool]:
    """Return fail-closed checks for a fresh canonical reconstruction."""

    checks: dict[str, bool] = {
        "proof.expected_source_present": bool(source),
        "proof.observed_source_present": isinstance(observed, Mapping),
        "proof.recomputed_source_independent": False,
    }
    try:
        expected = recompute()
    except Exception:
        expected = None
    checks["proof.recomputed_source_independent"] = isinstance(expected, Mapping)
    if not isinstance(expected, Mapping):
        return checks

    for key in compare_top_level:
        checks[f"proof.top_level:{key}"] = observed.get(key) == expected.get(key)

    for collection in collections:
        actual_values = observed.get(collection)
        expected_values = expected.get(collection)
        actual_ok = isinstance(actual_values, list)
        expected_ok = isinstance(expected_values, list)
        checks[f"proof.{collection}:typed"] = actual_ok and expected_ok
        if not (actual_ok and expected_ok):
            continue

        actual_ids = [item.get("case_id") if isinstance(item, Mapping) else None for item in actual_values]
        expected_ids = [item.get("case_id") if isinstance(item, Mapping) else None for item in expected_values]
        checks[f"proof.{collection}:non_empty"] = bool(actual_ids) == bool(expected_ids)
        checks[f"proof.{collection}:unique_ids"] = len(actual_ids) == len(set(actual_ids))
        checks[f"proof.{collection}:exact_ids"] = actual_ids == expected_ids
        actual_by_id = {item.get("case_id"): item for item in actual_values if isinstance(item, Mapping)}
        expected_by_id = {item.get("case_id"): item for item in expected_values if isinstance(item, Mapping)}
        checks[f"proof.{collection}:exact_case_count"] = len(actual_values) == len(expected_values)
        for case_id, expected_item in expected_by_id.items():
            actual_item = actual_by_id.get(case_id)
            checks[f"proof.{collection}:{case_id}:independent_match"] = actual_item == expected_item

    for key, expected_value in expected.items():
        if key in collections or key in _AGGREGATE_FIELDS or key in compare_top_level:
            continue
        if isinstance(expected_value, (str, int, float, bool)) or expected_value is None:
            checks[f"proof.metadata:{key}"] = observed.get(key) == expected_value

    return checks


__all__ = ["independent_case_proof"]
