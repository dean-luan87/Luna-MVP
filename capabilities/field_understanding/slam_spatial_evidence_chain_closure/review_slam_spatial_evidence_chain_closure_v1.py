# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Chain Closure — matrix + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_spatial_evidence_chain_closure.slam_spatial_evidence_chain_closure_registry_v1 import (
    REGISTRY_ID,
    build_slam_spatial_evidence_chain_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.slam_spatial_evidence_chain_closure.slam_spatial_evidence_chain_closure_types_v1 import (
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CLOSURE_BLOCKED,
    FINAL_DECISION_CLOSURE_GO,
    INGEST_CHAIN_REFS,
    INTERFACE_LAYER_PROTOCOL_REF,
    INTERNAL_STANDARD_FORMAT,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SEALED_UPSTREAM_PHASE_REFS,
    TARGET_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "slam_spatial_evidence_chain_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "slam_spatial_evidence_chain_closure_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
    "slam_spatial_evidence_chain_closure_types_v1.py",
    "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
    "slam_spatial_evidence_chain_closure_registry_v1.py",
    "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
    "review_slam_spatial_evidence_chain_closure_v1.py",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def validate_closure_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_slam_spatial_evidence_chain_closure_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    closure = matrix.get("slam_spatial_evidence_chain_closure") or {}
    if closure.get("interface_layer_protocol_ref") != INTERFACE_LAYER_PROTOCOL_REF:
        issues.append("interface_layer_protocol_ref_mismatch")
    if closure.get("model_management_protocol_ref") != MODEL_MANAGEMENT_PROTOCOL_REF:
        issues.append("model_management_protocol_ref_mismatch")
    if closure.get("internal_standard_format") != INTERNAL_STANDARD_FORMAT:
        issues.append("internal_standard_format_mismatch")
    if closure.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if tuple(closure.get("governance_rules") or ()) != CLOSURE_GOVERNANCE_RULES:
        issues.append("closure_governance_rules_mismatch")

    chains = matrix.get("ingest_chain_refs") or []
    if len(chains) < 5:
        issues.append(f"chain_count:{len(chains)}")

    chain_refs = {chain.get("chain_ref") for chain in chains}
    if chain_refs != set(INGEST_CHAIN_REFS):
        issues.append(f"ingest_chain_refs_mismatch:{sorted(chain_refs)!r}")

    for chain in chains:
        ref = chain.get("chain_ref")
        if chain.get("generic_json_spatial_trace_required") is not True:
            issues.append(f"{ref}.generic_json_spatial_trace_not_required")
        if chain.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
            issues.append(f"{ref}.field_synthesis_entrypoint_bypass")
        if chain.get("candidate_only") is not True:
            issues.append(f"{ref}.not_candidate_only")
        pipeline = chain.get("pipeline") or []
        if INTERNAL_STANDARD_FORMAT not in pipeline and ref != "spatial_odometry_fusion_chain":
            issues.append(f"{ref}.generic_json_spatial_trace_missing_from_pipeline")
        if FIELD_SYNTHESIS_ENTRYPOINT not in pipeline:
            issues.append(f"{ref}.field_synthesis_missing_from_pipeline")

    coverage = matrix.get("candidate_coverage") or {}
    for flag in (
        "pose_supported",
        "motion_supported",
        "health_supported",
        "anchor_supported",
        "relocalization_supported",
        "drift_supported",
        "gps_gnss_stub_supported",
        "spatial_odometry_fusion_supported",
        "conflict_candidate_supported",
    ):
        if coverage.get(flag) is not True:
            issues.append(f"candidate_coverage.{flag}=false")

    if coverage.get("field_synthesis_entrypoint_locked") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("candidate_coverage.field_synthesis_entrypoint_not_locked")

    decision = matrix.get("field_alignment_decision") or {}
    if decision.get("backend_native_output_direct_to_field_blocked") is not True:
        issues.append("backend_native_output_direct_to_field_not_blocked")
    if decision.get("gps_does_not_override_field_identity") is not True:
        issues.append("gps_does_not_override_field_identity=false")
    if decision.get("relocalization_does_not_restore_runtime_trust") is not True:
        issues.append("relocalization_does_not_restore_runtime_trust=false")

    binding = matrix.get("model_binding") or {}
    if binding.get("interface_layer_protocol_ref") != INTERFACE_LAYER_PROTOCOL_REF:
        issues.append("model_binding.interface_layer_protocol_ref_mismatch")
    if binding.get("model_management_protocol_ref") != MODEL_MANAGEMENT_PROTOCOL_REF:
        issues.append("model_binding.model_management_protocol_ref_mismatch")

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

    checks["sealed_upstream_phase_count"] = len(matrix.get("sealed_upstream_go_artifacts") or []) == 8
    if not checks["sealed_upstream_phase_count"]:
        issues.append("sealed_upstream_phase_count_not_8")

    return checks, issues


def review_slam_spatial_evidence_chain_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_slam_spatial_evidence_chain_closure_matrix_v1()
    matrix_ok, matrix_issues = validate_closure_matrix_v1(matrix)
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
    for key, ok in upstream_checks.items():
        if ok:
            passed_checks.append(f"upstream.{key}=true")
        else:
            failed_checks.append(f"upstream.{key}=false")

    coverage = matrix.get("candidate_coverage") or {}
    decision = matrix.get("field_alignment_decision") or {}
    chains = matrix.get("ingest_chain_refs") or []
    binding = matrix.get("model_binding") or {}

    review_checkpoints: Dict[str, Any] = {
        "chain_count": len(chains),
        "pose_supported": coverage.get("pose_supported"),
        "motion_supported": coverage.get("motion_supported"),
        "health_supported": coverage.get("health_supported"),
        "anchor_supported": coverage.get("anchor_supported"),
        "relocalization_supported": coverage.get("relocalization_supported"),
        "drift_supported": coverage.get("drift_supported"),
        "gps_gnss_stub_supported": coverage.get("gps_gnss_stub_supported"),
        "spatial_odometry_fusion_supported": coverage.get("spatial_odometry_fusion_supported"),
        "conflict_candidate_supported": coverage.get("conflict_candidate_supported"),
        "generic_json_spatial_trace_required": all(
            chain.get("generic_json_spatial_trace_required") is True for chain in chains
        ),
        "interface_layer_protocol_ref_ok": binding.get("interface_layer_protocol_ref")
        == INTERFACE_LAYER_PROTOCOL_REF,
        "model_management_protocol_ref_ok": binding.get("model_management_protocol_ref")
        == MODEL_MANAGEMENT_PROTOCOL_REF,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT
        if coverage.get("field_synthesis_entrypoint_locked") == FIELD_SYNTHESIS_ENTRYPOINT
        else None,
        "backend_native_output_direct_to_field_blocked": decision.get(
            "backend_native_output_direct_to_field_blocked"
        ),
        "gps_does_not_override_field_identity": decision.get("gps_does_not_override_field_identity"),
        "relocalization_does_not_restore_runtime_trust": decision.get(
            "relocalization_does_not_restore_runtime_trust"
        ),
        "runtime_activation_allowed": decision.get("runtime_activation_allowed"),
        "direct_action_allowed": decision.get("direct_action_allowed"),
        "direct_speech_allowed": decision.get("direct_speech_allowed"),
        "direct_fact_write_allowed": decision.get("direct_fact_write_allowed"),
        "sealed_upstream_phases_verified": all(
            upstream_checks.get(f"{phase}.go_sealed", False)
            for phase in SEALED_UPSTREAM_PHASE_REFS
        ),
    }

    go_conditions = {
        "chain_count_gte_5": review_checkpoints["chain_count"] >= 5,
        "pose_supported": review_checkpoints["pose_supported"] is True,
        "motion_supported": review_checkpoints["motion_supported"] is True,
        "health_supported": review_checkpoints["health_supported"] is True,
        "anchor_supported": review_checkpoints["anchor_supported"] is True,
        "relocalization_supported": review_checkpoints["relocalization_supported"] is True,
        "drift_supported": review_checkpoints["drift_supported"] is True,
        "gps_gnss_stub_supported": review_checkpoints["gps_gnss_stub_supported"] is True,
        "spatial_odometry_fusion_supported": review_checkpoints[
            "spatial_odometry_fusion_supported"
        ]
        is True,
        "conflict_candidate_supported": review_checkpoints["conflict_candidate_supported"] is True,
        "generic_json_spatial_trace_required": review_checkpoints[
            "generic_json_spatial_trace_required"
        ]
        is True,
        "interface_layer_protocol_ref_ok": review_checkpoints["interface_layer_protocol_ref_ok"]
        is True,
        "model_management_protocol_ref_ok": review_checkpoints["model_management_protocol_ref_ok"]
        is True,
        "field_synthesis_entrypoint_locked": review_checkpoints["field_synthesis_entrypoint_locked"]
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "backend_native_output_direct_to_field_blocked": review_checkpoints[
            "backend_native_output_direct_to_field_blocked"
        ]
        is True,
        "gps_does_not_override_field_identity": review_checkpoints[
            "gps_does_not_override_field_identity"
        ]
        is True,
        "relocalization_does_not_restore_runtime_trust": review_checkpoints[
            "relocalization_does_not_restore_runtime_trust"
        ]
        is True,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
        "sealed_upstream_phases_verified": review_checkpoints["sealed_upstream_phases_verified"]
        is True,
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
        "step": "SLAM Spatial Evidence Chain Field Alignment Closure Matrix + Review",
        "lifecycle_variant": "compressed_chain_closure_review",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "standard_evidence_pipeline": list(matrix.get("standard_evidence_pipeline") or []),
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "closure_matrix": matrix,
        "conclusions": {
            "slam_evidence_chain_status": "closed_for_field_alignment" if review_ok else "blocked",
            "sealed_upstream_phase_refs": list(SEALED_UPSTREAM_PHASE_REFS),
            "ingest_chain_refs": list(INGEST_CHAIN_REFS),
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "division_of_labor": {
                "gps_gnss": "global coarse positioning (stub/planning)",
                "slam_vio": "local relative motion",
                "rtab_map": "trajectory / odometry / graph anchors",
                "fusion": "spatial_odometry_fusion_candidate",
                "field_synthesis": "evidence fusion into field judgment",
            },
            "recommended_next_step": (
                "Phase Field Protocol Alignment: Field = Map Place + Realtime Context + "
                "Event Overlay; prove SLAM/GPS/map/event evidence serves field construction"
            ),
            "deferred_paths": [
                "Kimera/Hydra Scene Graph Observation",
                "Real GPS/GNSS runtime ingest",
            ],
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_CLOSURE_GO if review_ok else FINAL_DECISION_CLOSURE_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_slam_spatial_evidence_chain_closure_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "chain_count": checkpoints["chain_count"],
                "pose_supported": checkpoints["pose_supported"],
                "spatial_odometry_fusion_supported": checkpoints["spatial_odometry_fusion_supported"],
                "sealed_upstream_phases_verified": checkpoints["sealed_upstream_phases_verified"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_CLOSURE_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
