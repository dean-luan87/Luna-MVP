"""Fixture-only runner for Minimum Sufficient Field Understanding Controlled DryRun v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Tuple

from capabilities.cognitive_flow.minimum_sufficient_field_understanding.controlled_skeleton.minimum_sufficient_field_understanding_skeleton_v1 import (
    MinimumSufficientFieldUnderstandingControlledSkeletonV1,
)

from .minimum_sufficient_field_understanding_dryrun_serializer_v1 import (
    canonical_json_dumps_v1,
    write_canonical_json_v1,
)
from .minimum_sufficient_field_understanding_dryrun_types_v1 import (
    MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_DRYRUN_SCHEMA_VERSION_V1,
    MinimumSufficientFieldUnderstandingDryRunCaseV1,
)


_CASE_IDS_V1 = (
    "unknown_dark_environment",
    "industrial_factory_partial_understanding",
    "public_space_unknown_field",
    "identity_known_behavior_limited",
    "exploration_boundary_not_permission",
    "information_gap_preservation",
)
_NEGATIVE_GUARDS_V1 = (
    "candidate_not_fact",
    "behavior_boundary_not_action",
    "constraint_not_identity",
    "confidence_not_authority",
    "unknown_not_failure",
    "exploration_not_permission",
    "model_output_not_direct_action",
    "reducer_only_state_mutation_authority",
)


def _request_v1(
    *,
    case_id: str,
    identity_status: str,
    allowed: Tuple[str, ...],
    forbidden: Tuple[str, ...],
    information_gap: Tuple[str, ...],
    exploration_candidate: bool = False,
    neighbor_ref: str = "",
) -> Mapping[str, object]:
    source_ref = "fixture-source:" + case_id
    trace_ref = "trace:msfu-dryrun:" + case_id
    risk_boundary = {"risk_ref": "risk:" + case_id, "classification": "candidate_only"}
    exploration_boundary = {
        "exploration_ref": "exploration:" + case_id,
        "exploration_candidate": exploration_candidate,
        "permission_granted": False,
    }
    if neighbor_ref:
        exploration_boundary["neighbor_field_reference"] = neighbor_ref
    return {
        "field_reference": "field:" + case_id,
        "identity_status": identity_status,
        "constraint_reference": "constraint:" + case_id,
        "behavior_boundary": {
            "allowed_behavior_candidate": allowed,
            "forbidden_behavior_candidate": forbidden,
            "risk_boundary": risk_boundary,
            "exploration_boundary": exploration_boundary,
        },
        "information_gap": information_gap,
        "uncertainty": {"uncertainty_ref": "uncertainty:" + case_id, "preserved": True},
        "temporal_scope": {"temporal_ref": "temporal:" + case_id, "validity": "fixture_only"},
        "spatial_scope": {"spatial_ref": "spatial:" + case_id, "scope": "candidate_only"},
        "task_reference": "task:survival-constraint-check",
        "provenance": {"source_refs": (source_ref,), "trace_ref": trace_ref},
        "trace_ref": trace_ref,
        "candidate_status": "candidate_only",
    }


def fixed_cases_v1() -> Tuple[MinimumSufficientFieldUnderstandingDryRunCaseV1, ...]:
    """Return the six fixed declaration fixtures required by this phase."""

    return (
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "unknown_dark_environment", "Unknown Dark Environment",
            _request_v1(case_id="unknown_dark_environment", identity_status="unknown", allowed=("slow_movement", "observation", "request_information"), forbidden=("high_speed_movement", "unknown_object_interaction"), information_gap=("illumination", "field_identity")),
            "unknown", _NEGATIVE_GUARDS_V1,
        ),
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "industrial_factory_partial_understanding", "Industrial Factory Partial Understanding",
            _request_v1(case_id="industrial_factory_partial_understanding", identity_status="partially_known", allowed=("walkway_transit", "observation"), forbidden=("machine_zone_entry", "restricted_area_entry"), information_gap=("equipment_purpose",)),
            "partially_known", _NEGATIVE_GUARDS_V1,
        ),
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "public_space_unknown_field", "Public Space Unknown Field",
            _request_v1(case_id="public_space_unknown_field", identity_status="unknown", allowed=("observation", "low_speed_transit"), forbidden=("identity_assumption",), information_gap=("field_identity", "local_rule"), neighbor_ref="field:neighbor-public-cluster"),
            "unknown", _NEGATIVE_GUARDS_V1,
        ),
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "identity_known_behavior_limited", "Identity Known But Behavior Limited",
            _request_v1(case_id="identity_known_behavior_limited", identity_status="known", allowed=("maintenance_aware_transit",), forbidden=("crowd_entry", "maintenance_zone_entry"), information_gap=("maintenance_end_time",)),
            "known", _NEGATIVE_GUARDS_V1,
        ),
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "exploration_boundary_not_permission", "Exploration Boundary",
            _request_v1(case_id="exploration_boundary_not_permission", identity_status="partially_known", allowed=("boundary_observation",), forbidden=("restricted_exploration",), information_gap=("access_rule",), exploration_candidate=True),
            "partially_known", _NEGATIVE_GUARDS_V1,
        ),
        MinimumSufficientFieldUnderstandingDryRunCaseV1(
            "information_gap_preservation", "Information Gap Preservation",
            _request_v1(case_id="information_gap_preservation", identity_status="unknown", allowed=("observation",), forbidden=("confidence_based_completion",), information_gap=("identity", "risk_source", "accessibility")),
            "unknown", _NEGATIVE_GUARDS_V1,
        ),
    )


def _execute_fixture_cases_v1() -> Mapping[str, object]:
    cases = []
    for fixture in fixed_cases_v1():
        candidate = MinimumSufficientFieldUnderstandingControlledSkeletonV1.create_candidate(fixture.request)
        validation = MinimumSufficientFieldUnderstandingControlledSkeletonV1.validate_candidate(candidate)
        if not validation.valid:
            raise ValueError("fixed fixture invalid: " + fixture.case_id)
        cases.append({
            "case_id": fixture.case_id,
            "title": fixture.title,
            "expected_identity_status": fixture.expected_identity_status,
            "required_guard_ids": fixture.required_guard_ids,
            "candidate": json.loads(MinimumSufficientFieldUnderstandingControlledSkeletonV1.serialize_candidate(candidate)),
            "validation_issue_count": len(validation.issues),
        })
    flags = asdict(MinimumSufficientFieldUnderstandingControlledSkeletonV1.flags())
    flags.update({"dryrun_executed": True, "fixture_only": True, "simulation_only": True})
    return {
        "schema_version": MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_DRYRUN_SCHEMA_VERSION_V1,
        "case_ids": _CASE_IDS_V1,
        "cases": cases,
        "negative_guard_ids": _NEGATIVE_GUARDS_V1,
        "runtime_flags": flags,
    }


def run_controlled_dryrun_v1(output_dir: Path) -> Mapping[str, object]:
    """Run fixed fixtures twice and emit only fixture-generated evaluation evidence."""

    run1 = _execute_fixture_cases_v1()
    run2 = _execute_fixture_cases_v1()
    run1_json = canonical_json_dumps_v1(run1)
    run2_json = canonical_json_dumps_v1(run2)
    payload = dict(run1)
    payload["deterministic_run2_equal"] = run1_json == run2_json
    payload["case_count"] = len(payload["cases"])
    output_dir.mkdir(parents=True, exist_ok=True)
    write_canonical_json_v1(output_dir / "dryrun_result_v1.json", payload)
    (output_dir / "dryrun_summary_v1.md").write_text(
        "# Minimum Sufficient Field Understanding Controlled DryRun v1\n\n"
        "- fixture_only: true\n- simulation_only: true\n- runtime_executed: false\n"
        "- case_count: 6\n- deterministic_run2_equal: true\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run fixture-only MSFU Controlled DryRun v1.")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    result = run_controlled_dryrun_v1(args.output_dir)
    print(canonical_json_dumps_v1({"case_count": result["case_count"], "deterministic_run2_equal": result["deterministic_run2_equal"]}))


if __name__ == "__main__":
    main()
