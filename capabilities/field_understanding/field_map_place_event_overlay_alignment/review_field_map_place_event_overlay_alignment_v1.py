# -*- coding: utf-8 -*-
"""Field Map Place / Realtime Context / Event Overlay Alignment — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.field_map_place_event_overlay_alignment.field_map_place_event_overlay_alignment_registry_v1 import (
    REGISTRY_ID,
    build_field_map_place_event_overlay_alignment_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.field_map_place_event_overlay_alignment.field_map_place_event_overlay_alignment_types_v1 import (
    ALIGNMENT_PRINCIPLE_ZH,
    FIELD_ALIGNMENT_GOVERNANCE_RULES,
    FIELD_ALIGNMENT_SCENARIO_REFS,
    FIELD_DEFINITION_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_ALIGNMENT_BLOCKED,
    FINAL_DECISION_ALIGNMENT_READY,
    INTERFACE_LAYER_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SEALED_UPSTREAM_PHASE_REFS,
    SPATIAL_EVIDENCE_CHAIN_REF,
    SPATIAL_ODOMETRY_FUSION_REF,
    TARGET_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_map_place_event_overlay_alignment_v1_smoke_v0"
)
REVIEW_FILENAME = "field_map_place_event_overlay_alignment_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/field_map_place_event_overlay_alignment/"
    "field_map_place_event_overlay_alignment_types_v1.py",
    "capabilities/field_understanding/field_map_place_event_overlay_alignment/"
    "field_map_place_event_overlay_alignment_registry_v1.py",
    "capabilities/field_understanding/field_map_place_event_overlay_alignment/"
    "review_field_map_place_event_overlay_alignment_v1.py",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _candidate_ok(candidate: Optional[Dict[str, Any]]) -> bool:
    if not candidate:
        return True
    if candidate.get("candidate_only") is not True:
        return False
    chain = candidate.get("source_chain")
    if not chain:
        return False
    if candidate.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        return False
    return True


def validate_alignment_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_field_map_place_event_overlay_alignment_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("field_map_place_alignment_profile") or {}
    if profile.get("field_definition_ref") != FIELD_DEFINITION_REF:
        issues.append("field_definition_ref_mismatch")
    if profile.get("spatial_evidence_chain_ref") != SPATIAL_EVIDENCE_CHAIN_REF:
        issues.append("spatial_evidence_chain_ref_mismatch")
    if profile.get("spatial_odometry_fusion_ref") != SPATIAL_ODOMETRY_FUSION_REF:
        issues.append("spatial_odometry_fusion_ref_mismatch")
    if profile.get("interface_layer_protocol_ref") != INTERFACE_LAYER_PROTOCOL_REF:
        issues.append("interface_layer_protocol_ref_mismatch")
    if profile.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if tuple(profile.get("governance_rules") or ()) != FIELD_ALIGNMENT_GOVERNANCE_RULES:
        issues.append("governance_rules_mismatch")

    scenarios = matrix.get("field_alignment_scenario_matrix") or []
    if len(scenarios) != 6:
        issues.append(f"scenario_count:{len(scenarios)}")

    scenario_refs = {s.get("scenario_ref") for s in scenarios}
    if scenario_refs != set(FIELD_ALIGNMENT_SCENARIO_REFS):
        issues.append(f"scenario_refs_mismatch:{sorted(scenario_refs)!r}")

    for scenario in scenarios:
        ref = scenario.get("scenario_ref")
        for key in (
            "map_place_candidate",
            "realtime_context_candidate",
            "event_overlay_candidate",
            "spatial_evidence_binding",
            "field_interaction_label",
        ):
            if not _candidate_ok(scenario.get(key)):
                issues.append(f"{ref}.{key}_invalid")

        event = scenario.get("event_overlay_candidate")
        if event:
            if not event.get("time_window"):
                issues.append(f"{ref}.event_overlay_missing_time_window")
            if event.get("map_place_ref_rewrite_allowed") is True:
                issues.append(f"{ref}.event_overlay_rewrites_map_place")

        rtc = scenario.get("realtime_context_candidate")
        if rtc and rtc.get("direct_fact_write_allowed") is True:
            issues.append(f"{ref}.realtime_context_direct_fact_write")

        map_place = scenario.get("map_place_candidate")
        if map_place and map_place.get("field_identity_mutation_allowed") is True:
            issues.append(f"{ref}.map_place_field_identity_mutation")

        label = scenario.get("field_interaction_label")
        if label:
            if not label.get("underlying_map_place_ref"):
                issues.append(f"{ref}.field_label_missing_underlying_map_place")
            if not label.get("internal_field_state_ref"):
                issues.append(f"{ref}.field_interaction_label_not_separated")

        if scenario.get("conflict_candidate_required") and not scenario.get("conflict_candidate"):
            issues.append(f"{ref}.conflict_candidate_missing")

    decision = matrix.get("field_alignment_decision") or {}
    if decision.get("field_synthesis_entrypoint_locked") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_not_locked")

    return len(issues) == 0 and registry_ok, issues


def review_sealed_upstream_artifacts(
    matrix: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in matrix.get("sealed_upstream_go_artifacts") or []:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        artifact, artifact_exists = _load_upstream_artifact(entry["artifact_rel"])

        module_ok = module_path.is_file()
        checks[f"{phase_ref}.module_present"] = module_ok
        if not module_ok:
            issues.append(f"upstream_module_missing:{phase_ref}")

        checks[f"{phase_ref}.artifact_present"] = artifact_exists
        if not artifact_exists:
            issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

    return checks, issues


def derive_capability_flags(scenarios: List[Dict[str, Any]]) -> Dict[str, bool]:
    has_map_place = any(s.get("map_place_candidate") for s in scenarios)
    has_rtc = any(s.get("realtime_context_candidate") for s in scenarios)
    has_event = any(s.get("event_overlay_candidate") for s in scenarios)
    has_binding = any(s.get("spatial_evidence_binding") for s in scenarios)
    has_label_sep = all(
        (s.get("field_interaction_label") or {}).get("internal_field_state_ref")
        for s in scenarios
        if s.get("field_interaction_label")
    )
    event_override = any(s.get("event_overlay_can_override_user_facing_label") for s in scenarios)
    event_no_rewrite = all(
        not (s.get("event_overlay_candidate") or {}).get("map_place_ref_rewrite_allowed", False)
        for s in scenarios
    )
    map_not_full = any(s.get("map_place_fully_defines_field") is False for s in scenarios) or any(
        s.get("map_place_field_anchor") for s in scenarios
    )
    conflict_required = any(
        s.get("conflict_candidate_required") and s.get("conflict_candidate") for s in scenarios
    )
    event_time_window = all(
        (s.get("event_overlay_candidate") or {}).get("time_window") for s in scenarios if s.get("event_overlay_candidate")
    )
    source_chain_ok = all(
        _candidate_ok(s.get(key))
        for s in scenarios
        for key in (
            "map_place_candidate",
            "realtime_context_candidate",
            "event_overlay_candidate",
            "spatial_evidence_binding",
            "field_interaction_label",
        )
    )
    gps_no_override = not any(s.get("gps_overrides_field_identity") for s in scenarios)
    slam_no_override = not any(s.get("slam_overrides_field_identity") for s in scenarios)

    return {
        "map_place_field_anchor_supported": has_map_place,
        "realtime_context_overlay_supported": has_rtc,
        "event_overlay_supported": has_event,
        "spatial_evidence_binding_supported": has_binding,
        "field_interaction_label_separated": has_label_sep,
        "event_overlay_can_override_user_facing_label": event_override,
        "event_overlay_does_not_rewrite_map_place": event_no_rewrite,
        "map_place_does_not_fully_define_field": map_not_full,
        "gps_does_not_override_field_identity": gps_no_override,
        "slam_does_not_override_field_identity": slam_no_override,
        "map_place_spatial_conflict_candidate_required": conflict_required,
        "event_time_window_required": event_time_window,
        "source_chain_required": source_chain_ok,
        "candidate_only_enforced": source_chain_ok,
    }


def review_field_map_place_event_overlay_alignment_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_field_map_place_event_overlay_alignment_matrix_v1()
    matrix_ok, matrix_issues = validate_alignment_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    if matrix_ok:
        passed_checks.append("matrix_validation_ok=true")
    else:
        failed_checks.extend(matrix_issues)

    if registry_ok:
        passed_checks.append("registry_validation_ok=true")
    else:
        failed_checks.extend(registry_issues)

    upstream_checks, upstream_issues = review_sealed_upstream_artifacts(matrix)
    failed_checks.extend(upstream_issues)

    scenarios = matrix.get("field_alignment_scenario_matrix") or []
    capability_flags = derive_capability_flags(scenarios)
    decision = matrix.get("field_alignment_decision") or {}

    review_checkpoints: Dict[str, Any] = {
        "scenario_count": len(scenarios),
        **capability_flags,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT
        if decision.get("field_synthesis_entrypoint_locked") == FIELD_SYNTHESIS_ENTRYPOINT
        else None,
        "real_map_api_connected": decision.get("real_map_api_connected"),
        "real_gps_connected": decision.get("real_gps_connected"),
        "real_event_api_connected": decision.get("real_event_api_connected"),
        "runtime_activation_allowed": decision.get("runtime_activation_allowed"),
        "direct_action_allowed": decision.get("direct_action_allowed"),
        "direct_speech_allowed": decision.get("direct_speech_allowed"),
        "direct_fact_write_allowed": decision.get("direct_fact_write_allowed"),
        "sealed_upstream_phases_verified": all(
            upstream_checks.get(f"{phase}.go_sealed", False) for phase in SEALED_UPSTREAM_PHASE_REFS
        ),
    }

    go_conditions = {
        "scenario_count_eq_6": review_checkpoints["scenario_count"] == 6,
        "map_place_field_anchor_supported": capability_flags["map_place_field_anchor_supported"],
        "realtime_context_overlay_supported": capability_flags["realtime_context_overlay_supported"],
        "event_overlay_supported": capability_flags["event_overlay_supported"],
        "spatial_evidence_binding_supported": capability_flags["spatial_evidence_binding_supported"],
        "field_interaction_label_separated": capability_flags["field_interaction_label_separated"],
        "event_overlay_can_override_user_facing_label": capability_flags[
            "event_overlay_can_override_user_facing_label"
        ],
        "event_overlay_does_not_rewrite_map_place": capability_flags[
            "event_overlay_does_not_rewrite_map_place"
        ],
        "map_place_does_not_fully_define_field": capability_flags["map_place_does_not_fully_define_field"],
        "gps_does_not_override_field_identity": capability_flags["gps_does_not_override_field_identity"],
        "slam_does_not_override_field_identity": capability_flags["slam_does_not_override_field_identity"],
        "map_place_spatial_conflict_candidate_required": capability_flags[
            "map_place_spatial_conflict_candidate_required"
        ],
        "event_time_window_required": capability_flags["event_time_window_required"],
        "source_chain_required": capability_flags["source_chain_required"],
        "candidate_only_enforced": capability_flags["candidate_only_enforced"],
        "field_synthesis_entrypoint_locked": review_checkpoints["field_synthesis_entrypoint_locked"]
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "real_event_api_connected_false": review_checkpoints["real_event_api_connected"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
        "sealed_upstream_phases_verified": review_checkpoints["sealed_upstream_phases_verified"] is True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = matrix_ok and registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Field Map Place / Realtime Context / Event Overlay Alignment Matrix + Review",
        "lifecycle_variant": "compressed_field_protocol_alignment_review",
        "alignment_principle_zh": ALIGNMENT_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "field_definition_ref": FIELD_DEFINITION_REF,
        "field_alignment_pipeline": list(matrix.get("field_alignment_pipeline") or []),
        "field_alignment_governance_rules": list(FIELD_ALIGNMENT_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "alignment_matrix": matrix,
        "conclusions": {
            "field_definition_user_layer": "map_place_or_poi_or_user_cognitive_location",
            "field_definition_internal": (
                "map_place_plus_realtime_context_plus_event_overlay_"
                "plus_spatial_evidence_plus_task_context"
            ),
            "spatial_evidence_chain_ref": SPATIAL_EVIDENCE_CHAIN_REF,
            "spatial_odometry_fusion_ref": SPATIAL_ODOMETRY_FUSION_REF,
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "field_protocol_status": "aligned_for_synthesis_dryrun" if review_ok else "blocked",
            "recommended_next_step": (
                "Field synthesis dry-run: mall, metro station, stadium concert, "
                "temporary market, GPS/SLAM conflict scenarios"
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": (
            FINAL_DECISION_ALIGNMENT_READY if review_ok else FINAL_DECISION_ALIGNMENT_BLOCKED
        ),
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_field_map_place_event_overlay_alignment_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "scenario_count": checkpoints["scenario_count"],
                "spatial_evidence_binding_supported": checkpoints["spatial_evidence_binding_supported"],
                "field_interaction_label_separated": checkpoints["field_interaction_label_separated"],
                "sealed_upstream_phases_verified": checkpoints["sealed_upstream_phases_verified"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_ALIGNMENT_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
