"""Compact deterministic governance cases for the B5 baseline layer."""

from __future__ import annotations

from typing import Callable, Dict

from .brain_golden_baseline_governance_v1 import (
    classify_change_impact,
    classify_compatibility,
    load_baseline_snapshot,
    validate_baseline,
)


def _valid() -> bool:
    return not validate_baseline(load_baseline_snapshot())


def _phase_membership() -> bool:
    return load_baseline_snapshot().manifest.get("phase_set") == ["S3-Y11", "B1", "B2", "B3", "B4"]


def _owner_unique() -> bool:
    owners = load_baseline_snapshot().owner_matrix["owners"]
    return len({item["concept"] for item in owners}) == len(owners)


def _task_is_subrange() -> bool:
    suites = load_baseline_snapshot().regression_index["suites"]
    task = next(item for item in suites if item["id"] == "TASK-B3-SUBRANGE")
    return task["scenario_count"] == "not independently declared; B3-16..B3-20 and B3-26"


def _impact(domain: str, expected: tuple[str, ...]) -> bool:
    return classify_change_impact(domain).required_regressions == expected


def _compatibility(classification: str, expected: str, **kwargs: object) -> bool:
    return classify_compatibility(declared_classification=classification, **kwargs).classification == expected


def build_cases() -> Dict[str, Callable[[], bool]]:
    return {
        "B5-01": _valid,
        "B5-02": _phase_membership,
        "B5-03": _owner_unique,
        "B5-04": lambda: not any(issue.code == "OWNER_RECORD_INCOMPLETE" for issue in validate_baseline()),
        "B5-05": lambda: "hypothesis_as_fact" in load_baseline_snapshot().guards["false"],
        "B5-06": lambda: bool(load_baseline_snapshot().real_synthetic.get("real_components")) and bool(load_baseline_snapshot().real_synthetic.get("controlled_or_synthetic_components")),
        "B5-07": lambda: bool(load_baseline_snapshot().deferred.get("deferred")),
        "B5-08": lambda: len(load_baseline_snapshot().trace["required_ref_classes"]) == 6,
        "B5-09": lambda: len(load_baseline_snapshot().regression_index["suites"]) == 10,
        "B5-10": _task_is_subrange,
        "B5-11": lambda: _impact("VISUAL_EVIDENCE_CONTRACT", ("S3", "B1", "downstream evidence compatibility")),
        "B5-12": lambda: _impact("CURRENT_WORLD", ("B1", "B2", "B3", "B4")),
        "B5-13": lambda: _impact("COGNITIVE_STATE_FORMATION", ("B2", "B3", "B4")),
        "B5-14": lambda: _impact("DECISION_GOVERNANCE", ("B3", "B4")) and _impact("TASK_MANAGER", ("B3", "B4")),
        "B5-15": lambda: _impact("NEGATIVE_GUARD", ("FULL_GOLDEN_BASELINE_REVIEW",)),
        "B5-16": lambda: _compatibility("BACKWARD_COMPATIBLE", "BACKWARD_COMPATIBLE", semantic_change=False),
        "B5-17": lambda: _compatibility("BREAKING_CHANGE", "BREAKING_CHANGE", semantic_change=True),
        "B5-18": lambda: load_baseline_snapshot().manifest.get("manifest_does_not_duplicate_contracts") is True,
        "B5-19": lambda: "Observation Gateway" in load_baseline_snapshot().manifest.get("real_synthetic_boundary", "") or bool(load_baseline_snapshot().real_synthetic),
        "B5-20": lambda: not any(issue.code == "EXECUTION_REFERENCE" for issue in validate_baseline()),
    }
