# -*- coding: utf-8 -*-
"""Spatial Odometry Fusion Interface — planning matrix + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_odometry_fusion_interface.spatial_odometry_fusion_interface_registry_v1 import (
    REGISTRY_ID,
    build_spatial_odometry_fusion_interface_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.spatial_odometry_fusion_interface.spatial_odometry_fusion_interface_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_PLANNING_READY,
    FINAL_DECISION_REVIEW_BLOCKED,
    FUSION_GOVERNANCE_RULES,
    FUSION_INTERFACE_REF,
    FUSION_PRINCIPLE_ZH,
    FUSION_SCENARIO_REFS,
    INPUT_EVIDENCE_SOURCE_REFS,
    INTERFACE_LAYER_PROTOCOL_REF,
    INTERNAL_STANDARD_FORMAT,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    PLANNING_OBJECT_TYPES,
    SOURCE_INTERFACE_PROFILE,
    TARGET_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "spatial_odometry_fusion_interface_v1_smoke_v0"
)
REVIEW_FILENAME = "spatial_odometry_fusion_interface_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/spatial_odometry_fusion_interface/"
    "spatial_odometry_fusion_interface_types_v1.py",
    "capabilities/field_understanding/spatial_odometry_fusion_interface/"
    "spatial_odometry_fusion_interface_registry_v1.py",
    "capabilities/field_understanding/spatial_odometry_fusion_interface/"
    "review_spatial_odometry_fusion_interface_v1.py",
)


def _candidate_has_source_chain(candidate: Optional[Dict[str, Any]]) -> bool:
    if not candidate:
        return True
    chain = candidate.get("source_chain")
    return isinstance(chain, (list, tuple)) and len(chain) > 0


def _candidate_has_coordinate_scope(candidate: Optional[Dict[str, Any]]) -> bool:
    if not candidate:
        return True
    return bool(candidate.get("coordinate_scope"))


def validate_fusion_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_spatial_odometry_fusion_interface_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    fusion_interface = matrix.get("spatial_odometry_fusion_interface") or {}
    if fusion_interface.get("interface_ref") != FUSION_INTERFACE_REF:
        issues.append("fusion_interface_ref_mismatch")
    if fusion_interface.get("interface_layer_protocol_ref") != INTERFACE_LAYER_PROTOCOL_REF:
        issues.append("interface_layer_protocol_ref_mismatch")
    if fusion_interface.get("model_management_protocol_ref") != MODEL_MANAGEMENT_PROTOCOL_REF:
        issues.append("model_management_protocol_ref_mismatch")
    if fusion_interface.get("source_interface_profile") != SOURCE_INTERFACE_PROFILE:
        issues.append("source_interface_profile_mismatch")
    if fusion_interface.get("internal_standard_format") != INTERNAL_STANDARD_FORMAT:
        issues.append("internal_standard_format_mismatch")
    if fusion_interface.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if tuple(fusion_interface.get("governance_rules") or ()) != FUSION_GOVERNANCE_RULES:
        issues.append("governance_rules_mismatch")

    scenarios = matrix.get("fusion_scenario_matrix") or []
    if len(scenarios) != 5:
        issues.append(f"fusion_scenario_count:{len(scenarios)}")

    scenario_refs = {s.get("scenario_ref") for s in scenarios}
    if scenario_refs != set(FUSION_SCENARIO_REFS):
        issues.append(f"fusion_scenario_refs_mismatch:{sorted(scenario_refs)!r}")

    input_refs = matrix.get("input_evidence_source_refs") or []
    if list(input_refs) != list(INPUT_EVIDENCE_SOURCE_REFS):
        issues.append("input_evidence_source_refs_mismatch")

    if not matrix.get("planning_decision"):
        issues.append("planning_decision_missing")

    for scenario in scenarios:
        ref = scenario.get("scenario_ref")
        fusion = scenario.get("fusion_candidate") or {}
        if not _candidate_has_source_chain(fusion):
            issues.append(f"{ref}.fusion_candidate_missing_source_chain")
        if not fusion.get("coordinate_scope"):
            issues.append(f"{ref}.fusion_candidate_missing_coordinate_scope")
        if fusion.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
            issues.append(f"{ref}.fusion_candidate_field_synthesis_bypass")
        if fusion.get("candidate_only") is not True:
            issues.append(f"{ref}.fusion_candidate_not_candidate_only")

        for key in ("gps_candidate", "slam_candidate", "rtab_graph_candidate"):
            candidate = scenario.get(key)
            if not candidate:
                continue
            if not _candidate_has_source_chain(candidate):
                issues.append(f"{ref}.{key}_missing_source_chain")
            if not _candidate_has_coordinate_scope(candidate):
                issues.append(f"{ref}.{key}_missing_coordinate_scope")
            if candidate.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
                issues.append(f"{ref}.{key}_field_synthesis_bypass")

        gps = scenario.get("gps_candidate")
        if gps:
            if gps.get("field_identity_mutation_allowed") is True:
                issues.append(f"{ref}.gps_field_identity_mutation_forbidden")
            for flag in ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed"):
                if gps.get(flag) is True:
                    issues.append(f"{ref}.gps_{flag}_forbidden")

        slam = scenario.get("slam_candidate")
        if slam:
            for flag in ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed"):
                if slam.get(flag) is True:
                    issues.append(f"{ref}.slam_{flag}_forbidden")

        rtab = scenario.get("rtab_graph_candidate")
        if rtab and rtab.get("restore_runtime_trust") is True:
            issues.append(f"{ref}.rtab_restore_runtime_trust_forbidden")
        if scenario.get("restore_runtime_trust") is True:
            issues.append(f"{ref}.scenario_restore_runtime_trust_forbidden")

        if scenario.get("conflict_candidate_required") is True:
            if fusion.get("conflict_candidate_emitted") is not True:
                issues.append(f"{ref}.conflict_candidate_not_emitted")

    return len(issues) == 0 and registry_ok, issues


def review_governance_rules(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str]]:
    fusion_interface = matrix.get("spatial_odometry_fusion_interface") or {}
    rules = tuple(fusion_interface.get("governance_rules") or ())
    decision = matrix.get("planning_decision") or {}

    checks = {
        "gps_does_not_override_field_identity": "gps_gnss_must_not_override_field_identity" in rules,
        "gps_slam_conflict_candidate_required": "gps_slam_conflict_must_emit_conflict_candidate" in rules,
        "rtab_relocalization_does_not_restore_runtime_trust": (
            "rtab_graph_relocalization_must_not_restore_runtime_trust" in rules
        ),
        "source_chain_required": "source_chain_must_be_preserved" in rules,
        "coordinate_scope_required": "coordinate_scope_must_be_explicit" in rules,
        "field_synthesis_entrypoint_locked": decision.get("field_synthesis_entrypoint_locked")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "real_gps_connected": decision.get("real_gps_connected") is True,
        "runtime_activation_allowed": decision.get("runtime_activation_allowed") is True,
        "direct_action_allowed": decision.get("direct_action_allowed") is True,
        "direct_speech_allowed": decision.get("direct_speech_allowed") is True,
        "direct_fact_write_allowed": decision.get("direct_fact_write_allowed") is True,
    }
    return checks, [
        key
        for key, ok in checks.items()
        if (
            key
            in (
                "real_gps_connected",
                "runtime_activation_allowed",
                "direct_action_allowed",
                "direct_speech_allowed",
                "direct_fact_write_allowed",
            )
            and ok
        )
        or (
            key
            not in (
                "real_gps_connected",
                "runtime_activation_allowed",
                "direct_action_allowed",
                "direct_speech_allowed",
                "direct_fact_write_allowed",
            )
            and not ok
        )
    ]


def review_capability_support(matrix: Dict[str, Any]) -> Dict[str, bool]:
    scenarios = matrix.get("fusion_scenario_matrix") or []
    input_refs = set(matrix.get("input_evidence_source_refs") or [])

    has_gps = any(s.get("gps_candidate") for s in scenarios)
    has_slam = any(s.get("slam_candidate") for s in scenarios)
    has_rtab = any(s.get("rtab_graph_candidate") for s in scenarios)

    return {
        "fusion_interface_count": 1 if matrix.get("spatial_odometry_fusion_interface") else 0,
        "gps_gnss_stub_supported": has_gps and "gps_gnss_coarse_position_stub" in input_refs,
        "slam_local_odometry_supported": has_slam
        and "generic_json_spatial_trace_pose_motion" in input_refs,
        "rtab_graph_anchor_supported": has_rtab and "rtab_map_graph_export_subset" in input_refs,
        "fusion_scenario_count": len(scenarios),
    }


def review_spatial_odometry_fusion_interface_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_spatial_odometry_fusion_interface_matrix_v1()
    matrix_ok, matrix_issues = validate_fusion_matrix_v1(matrix)
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

    governance_checks, governance_failures = review_governance_rules(matrix)
    failed_checks.extend(governance_failures)

    capability_checks = review_capability_support(matrix)

    review_checkpoints: Dict[str, Any] = {
        **capability_checks,
        "gps_does_not_override_field_identity": governance_checks["gps_does_not_override_field_identity"],
        "gps_slam_conflict_candidate_required": governance_checks["gps_slam_conflict_candidate_required"],
        "rtab_relocalization_does_not_restore_runtime_trust": governance_checks[
            "rtab_relocalization_does_not_restore_runtime_trust"
        ],
        "source_chain_required": governance_checks["source_chain_required"],
        "coordinate_scope_required": governance_checks["coordinate_scope_required"],
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT
        if governance_checks["field_synthesis_entrypoint_locked"]
        else None,
        "real_gps_connected": governance_checks["real_gps_connected"],
        "runtime_activation_allowed": governance_checks["runtime_activation_allowed"],
        "direct_action_allowed": governance_checks["direct_action_allowed"],
        "direct_speech_allowed": governance_checks["direct_speech_allowed"],
        "direct_fact_write_allowed": governance_checks["direct_fact_write_allowed"],
        "generic_json_spatial_trace_reused": INTERNAL_STANDARD_FORMAT == "generic_json_spatial_trace",
        "interface_layer_protocol_ref_ok": (
            (matrix.get("spatial_odometry_fusion_interface") or {}).get("interface_layer_protocol_ref")
            == INTERFACE_LAYER_PROTOCOL_REF
        ),
        "model_management_protocol_ref_ok": (
            (matrix.get("spatial_odometry_fusion_interface") or {}).get("model_management_protocol_ref")
            == MODEL_MANAGEMENT_PROTOCOL_REF
        ),
    }

    go_conditions = {
        "fusion_interface_count_eq_1": capability_checks["fusion_interface_count"] == 1,
        "gps_gnss_stub_supported": capability_checks["gps_gnss_stub_supported"],
        "slam_local_odometry_supported": capability_checks["slam_local_odometry_supported"],
        "rtab_graph_anchor_supported": capability_checks["rtab_graph_anchor_supported"],
        "fusion_scenario_count_eq_5": capability_checks["fusion_scenario_count"] == 5,
        "gps_does_not_override_field_identity": governance_checks["gps_does_not_override_field_identity"],
        "gps_slam_conflict_candidate_required": governance_checks["gps_slam_conflict_candidate_required"],
        "rtab_relocalization_does_not_restore_runtime_trust": governance_checks[
            "rtab_relocalization_does_not_restore_runtime_trust"
        ],
        "source_chain_required": governance_checks["source_chain_required"],
        "coordinate_scope_required": governance_checks["coordinate_scope_required"],
        "field_synthesis_entrypoint_locked": governance_checks["field_synthesis_entrypoint_locked"],
        "real_gps_connected_false": governance_checks["real_gps_connected"] is False,
        "runtime_activation_allowed_false": governance_checks["runtime_activation_allowed"] is False,
        "direct_action_allowed_false": governance_checks["direct_action_allowed"] is False,
        "direct_speech_allowed_false": governance_checks["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": governance_checks["direct_fact_write_allowed"] is False,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = matrix_ok and registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
        "step": "Spatial Odometry Fusion Interface Planning Matrix + Review",
        "lifecycle_variant": "compressed_fusion_interface_planning_review",
        "fusion_principle_zh": FUSION_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "fusion_pipeline": list(matrix.get("fusion_pipeline") or []),
        "fusion_governance_rules": list(FUSION_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "planning_matrix": matrix,
        "conclusions": {
            "fusion_interface_ref": FUSION_INTERFACE_REF,
            "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
            "source_interface_profile": SOURCE_INTERFACE_PROFILE,
            "internal_standard_format": INTERNAL_STANDARD_FORMAT,
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "input_evidence_source_refs": list(INPUT_EVIDENCE_SOURCE_REFS),
            "fusion_scenario_refs": list(FUSION_SCENARIO_REFS),
            "division_of_labor": {
                "gps_gnss": "global coarse positioning",
                "slam_vio": "local relative positioning and motion",
                "rtab_map_graph": "anchor / relocalization / drift hints",
                "field_synthesis": "evidence fusion only",
            },
            "next_step_hint": (
                "Align with Field Protocol: Field = Map Place + Realtime Context + Event Overlay; "
                "unify GPS/map address, SLAM local field, and transient event field into field_synthesis_v1"
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": (
            FINAL_DECISION_PLANNING_READY if review_ok else FINAL_DECISION_REVIEW_BLOCKED
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
    result = review_spatial_odometry_fusion_interface_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "fusion_interface_count": checkpoints["fusion_interface_count"],
                "fusion_scenario_count": checkpoints["fusion_scenario_count"],
                "gps_gnss_stub_supported": checkpoints["gps_gnss_stub_supported"],
                "slam_local_odometry_supported": checkpoints["slam_local_odometry_supported"],
                "rtab_graph_anchor_supported": checkpoints["rtab_graph_anchor_supported"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "real_gps_connected": checkpoints["real_gps_connected"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_PLANNING_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
