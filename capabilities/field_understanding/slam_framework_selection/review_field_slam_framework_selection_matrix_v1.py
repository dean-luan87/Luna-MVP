# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — matrix review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_matrix_v1 import (
    build_framework_selection_matrix_v1,
    summarize_framework_selection_matrix_v1,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_registry_v1 import (
    GPL_LICENSE_TYPES,
    P0_EVIDENCE_FIT_LEVELS,
    SLAM_BACKEND_REGISTRY,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    validate_framework_selection_matrix_v1,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_types_v1 import (
    BACKEND_ADMISSION_PIPELINE,
    FINAL_DECISION_MATRIX_READY,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_ID,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES,
    GENERIC_SLAM_ADAPTER_CONTRACT_ID,
    LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SPATIAL_EVIDENCE_PROVIDER_ROLE,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_slam_framework_selection_v1_smoke_v0"
)
REVIEW_FILENAME = "field_slam_framework_selection_matrix_review_v1.json"

FINAL_DECISION_GO = "FIELD_SLAM_FRAMEWORK_SELECTION_MATRIX_REVIEW_GO"
FINAL_DECISION_BLOCKED = "FIELD_SLAM_FRAMEWORK_SELECTION_MATRIX_REVIEW_BLOCKED"

EXPECTED_FRAMEWORK_COUNT = 7
EXPECTED_EVALUATION_COUNT = 7
EXPECTED_VALIDATOR_RULES = 15

EXPECTED_FRAMEWORK_REFS = frozenset(
    {"openvins", "vins_fusion", "orb_slam3", "rtab_map", "kimera", "hydra", "grapheqa"}
)
EXPECTED_P0_TECHNICAL = ("openvins", "vins_fusion")
EXPECTED_P1 = ("orb_slam3",)
EXPECTED_P2 = ("rtab_map",)
EXPECTED_OBSERVATION = ("kimera", "hydra", "grapheqa")
OBSERVATION_FRAMEWORKS = frozenset(EXPECTED_OBSERVATION)
P0_TECHNICAL_FRAMEWORKS = frozenset(EXPECTED_P0_TECHNICAL)

STEP1_MATRIX_FILES = (
    "capabilities/field_understanding/slam_framework_selection/field_slam_framework_selection_types_v1.py",
    "capabilities/field_understanding/slam_framework_selection/field_slam_framework_selection_registry_v1.py",
    "capabilities/field_understanding/slam_framework_selection/field_slam_framework_selection_matrix_v1.py",
    "capabilities/field_understanding/slam_framework_selection/field_slam_framework_selection_static_validators_v1.py",
)

SLAM_INTERFACE_EVIDENCE_TYPES = (
    "capabilities/field_understanding/slam_interface/field_slam_interface_types_v1.py",
)

RUNTIME_BINDING_PATTERNS = (
    "import openvins",
    "import vins",
    "orb_slam3",
    "rtabmap",
    "rtab_map",
    "kimera::",
    "hydra::",
    "grapheqa",
    "ros::",
    "rospy",
    "cv2.VideoCapture",
)


def _framework_by_ref(frameworks: List[Dict[str, Any]], ref: str) -> Optional[Dict[str, Any]]:
    for fw in frameworks:
        if fw.get("framework_ref") == ref:
            return fw
    return None


def _evaluation_by_ref(
    evaluations: List[Dict[str, Any]], ref: str
) -> Optional[Dict[str, Any]]:
    for ev in evaluations:
        if ev.get("framework_ref") == ref:
            return ev
    return None


def review_matrix_baseline(matrix: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    frameworks = matrix.get("frameworks") or []
    evaluations = matrix.get("evaluations") or []
    decision = matrix.get("decision") or {}

    framework_refs = {f.get("framework_ref") for f in frameworks}
    if len(frameworks) == EXPECTED_FRAMEWORK_COUNT:
        passed.append(f"baseline.framework_count={EXPECTED_FRAMEWORK_COUNT}")
    else:
        failed.append(f"baseline.framework_count={len(frameworks)}")

    if len(evaluations) == EXPECTED_EVALUATION_COUNT:
        passed.append(f"baseline.evaluation_count={EXPECTED_EVALUATION_COUNT}")
    else:
        failed.append(f"baseline.evaluation_count={len(evaluations)}")

    if decision:
        passed.append("baseline.selection_decision_present=true")
    else:
        failed.append("baseline.selection_decision_missing")

    missing_fw = EXPECTED_FRAMEWORK_REFS - framework_refs
    if not missing_fw:
        passed.append("baseline.all_framework_refs_present=true")
    else:
        failed.append(f"baseline.missing_framework_refs={sorted(missing_fw)!r}")

    baseline = {
        "framework_count": len(frameworks),
        "evaluation_count": len(evaluations),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "recommended_p0_technical": list(decision.get("recommended_p0_technical") or ()),
        "recommended_p0_commercial_safe": list(decision.get("recommended_p0_commercial_safe") or ()),
        "recommended_p1": list(decision.get("recommended_p1") or ()),
        "recommended_p2": list(decision.get("recommended_p2") or ()),
        "recommended_observation": list(decision.get("recommended_observation") or ()),
    }

    ok = len(failed) == 0
    return ok, baseline, passed, failed


def review_license_governance(
    frameworks: List[Dict[str, Any]],
    decision: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    gpl_blocked = all(
        not fw.get("commercial_runtime_candidate")
        for fw in frameworks
        if fw.get("license_type") in GPL_LICENSE_TYPES
    )
    p0_tech = tuple(decision.get("recommended_p0_technical") or ())
    p0_safe = tuple(decision.get("recommended_p0_commercial_safe") or ())
    commercial_safe_empty = len(p0_safe) == 0
    p0_not_commercial = all(
        not _framework_by_ref(frameworks, ref).get("commercial_runtime_candidate")  # type: ignore[union-attr]
        for ref in p0_tech
        if _framework_by_ref(frameworks, ref)
    )
    license_gate = decision.get("license_gate_required") is True
    no_overlap = not (set(p0_tech) & set(p0_safe))

    license_review = {
        "gpl_frameworks_blocked_from_commercial_runtime": gpl_blocked,
        "commercial_safe_p0_empty_ok": commercial_safe_empty,
        "license_gate_required": license_gate,
        "license_gate_not_skipped": license_gate and no_overlap,
        "p0_technical_not_commercial_runtime": p0_not_commercial,
    }

    for key, ok in license_review.items():
        if ok:
            passed.append(f"license.{key}=true")
        else:
            failed.append(f"license.{key}=false")

    return license_review, passed, failed


def review_selection_governance(
    frameworks: List[Dict[str, Any]],
    evaluations: List[Dict[str, Any]],
    decision: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    p0_tech = tuple(decision.get("recommended_p0_technical") or ())
    p0_pose_motion_ok = True
    for ref in p0_tech:
        ev = _evaluation_by_ref(evaluations, ref)
        if not ev:
            p0_pose_motion_ok = False
            failed.append(f"selection.p0_evaluation_missing={ref}")
            continue
        pose = ev.get("pose_candidate_fit")
        motion = ev.get("motion_candidate_fit")
        health = ev.get("slam_health_fit")
        if not (
            pose in P0_EVIDENCE_FIT_LEVELS
            or motion in P0_EVIDENCE_FIT_LEVELS
            or health in P0_EVIDENCE_FIT_LEVELS
        ):
            p0_pose_motion_ok = False
            failed.append(f"selection.p0_not_pose_motion_health_fit={ref}")

    p0_not_mapping_only = True
    for ref in p0_tech:
        ev = _evaluation_by_ref(evaluations, ref)
        if not ev:
            continue
        local_map = ev.get("local_map_fit")
        pose = ev.get("pose_candidate_fit")
        motion = ev.get("motion_candidate_fit")
        if local_map in P0_EVIDENCE_FIT_LEVELS and pose not in P0_EVIDENCE_FIT_LEVELS and motion not in P0_EVIDENCE_FIT_LEVELS:
            p0_not_mapping_only = False
            failed.append(f"selection.p0_selected_by_mapping_only={ref}")

    orb_p1 = (
        tuple(decision.get("recommended_p1") or ()) == EXPECTED_P1
        and "orb_slam3" not in p0_tech
        and "orb_slam3" not in (decision.get("recommended_p0_commercial_safe") or ())
    )
    rtab_p2 = tuple(decision.get("recommended_p2") or ()) == EXPECTED_P2

    semantic_observation = (
        set(decision.get("recommended_observation") or ()) == OBSERVATION_FRAMEWORKS
    )
    grapheqa = _framework_by_ref(frameworks, "grapheqa")
    grapheqa_observation_only = (
        grapheqa is not None
        and grapheqa.get("runtime_priority") == "observation"
        and grapheqa.get("commercial_runtime_candidate") is False
        and "grapheqa" not in p0_tech
        and "grapheqa" not in (decision.get("recommended_p0_commercial_safe") or ())
    )

    governance = {
        "p0_selected_by_pose_motion_need": p0_pose_motion_ok,
        "p0_not_selected_by_mapping_power": p0_not_mapping_only,
        "orb_slam3_kept_as_p1": orb_p1,
        "rtab_map_kept_as_p2": rtab_p2,
        "semantic_scene_graph_kept_as_observation": semantic_observation,
        "grapheqa_not_runtime_slam": grapheqa_observation_only,
    }

    for key, ok in governance.items():
        if ok:
            passed.append(f"selection_governance.{key}=true")
        else:
            failed.append(f"selection_governance.{key}=false")

    return governance, passed, failed


def review_field_spatial_evidence_provider_boundary() -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for rel in SLAM_INTERFACE_EVIDENCE_TYPES:
        path = _REPO_ROOT / rel
        if not path.is_file():
            failed.append(f"slam_interface.missing={rel}")
            continue
        passed.append(f"slam_interface.present={path.name}")

    try:
        from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
            ROLE_EN,
            SLAM_INTERFACE_CANDIDATE_TYPES,
        )

        if ROLE_EN == "Field Spatial Evidence Provider":
            passed.append("slam_interface.role=Field Spatial Evidence Provider")
        else:
            failed.append(f"slam_interface.role_mismatch={ROLE_EN!r}")

        if len(SLAM_INTERFACE_CANDIDATE_TYPES) == 7:
            passed.append("slam_interface.evidence_types=7")
        else:
            failed.append(f"slam_interface.evidence_types={len(SLAM_INTERFACE_CANDIDATE_TYPES)}")
    except ImportError as exc:
        failed.append(f"slam_interface.import_failed={exc}")

    selection_root = _REPO_ROOT / "capabilities" / "field_understanding" / "slam_framework_selection"
    for py_path in selection_root.rglob("*.py"):
        if py_path.name == "review_field_slam_framework_selection_matrix_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8").lower()
        for pattern in RUNTIME_BINDING_PATTERNS:
            if pattern in text and "framework_ref" not in pattern:
                if pattern in ("grapheqa", "openvins", "vins", "orb_slam3", "rtab_map", "kimera", "hydra"):
                    continue
                failed.append(f"selection_module.runtime_binding={py_path.name}:{pattern}")

    ok = len(failed) == 0
    return ok, passed, failed


def review_boundary_scope() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = dict(NON_EXECUTION_FLAGS)
    boundary = {
        "no_runtime_framework_connected": flags.get("no_slam_framework_execution") is True,
        "no_camera_connected": flags.get("no_camera_runtime") is True,
        "no_ros_connected": flags.get("no_ros_runtime") is True,
        "no_benchmark_run": flags.get("no_benchmark_execution") is True,
        "no_adapter_written": flags.get("no_adapter_implementation") is True,
        "no_commercial_final_selection": flags.get("no_commercial_final_selection") is True,
    }

    for key, expected in boundary.items():
        if expected:
            passed.append(f"boundary.{key}=true")
        else:
            failed.append(f"boundary.{key}=false")

    return boundary, passed, failed


def review_framework_replaceability_governance(
    frameworks: List[Dict[str, Any]],
    decision: Dict[str, Any],
) -> Tuple[Dict[str, bool], bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    p0_tech = set(decision.get("recommended_p0_technical") or ())
    p0_not_runtime_binding = (
        p0_tech == {"openvins", "vins_fusion"}
        and all(
            _framework_by_ref(frameworks, ref).get("technical_reference_candidate") is True  # type: ignore[union-attr]
            and _framework_by_ref(frameworks, ref).get("commercial_runtime_candidate") is False  # type: ignore[union-attr]
            for ref in p0_tech
            if _framework_by_ref(frameworks, ref)
        )
    )

    adapter_contract_independent = decision.get("adapter_contract_required") is True
    all_backend_candidates = all(
        fw.get("technical_reference_candidate") is True
        and fw.get("commercial_runtime_candidate") is False
        for fw in frameworks
        if fw.get("framework_ref") in EXPECTED_FRAMEWORK_REFS
    )

    backend_registry_ok = all(
        ref in SLAM_BACKEND_REGISTRY for ref in EXPECTED_FRAMEWORK_REFS
    ) and SLAM_BACKEND_REGISTRY.get("openvins", {}).get("commercial_runtime_allowed") is False

    evidence_contract_ok = len(LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES) == 7
    admission_pipeline_ok = len(BACKEND_ADMISSION_PIPELINE) == 9

    try:
        from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
            SLAM_INTERFACE_CANDIDATE_TYPES,
        )

        field_chain_stable = set(SLAM_INTERFACE_CANDIDATE_TYPES) == set(LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES)
    except ImportError:
        field_chain_stable = False

    replaceability = {
        "p0_not_bound_as_irreplaceable_runtime": p0_not_runtime_binding,
        "adapter_contract_independent": adapter_contract_independent,
        "each_framework_is_backend_candidate": all_backend_candidates,
        "backend_registry_declared": backend_registry_ok,
        "field_understanding_main_chain_stable": field_chain_stable,
        "generic_adapter_contract_declared": GENERIC_SLAM_ADAPTER_CONTRACT_ID == "generic_slam_adapter_contract_v1",
        "spatial_evidence_provider_role_declared": SPATIAL_EVIDENCE_PROVIDER_ROLE == "SpatialEvidenceProvider",
        "backend_admission_pipeline_declared": admission_pipeline_ok,
        "evidence_contract_types_match_slam_interface": evidence_contract_ok,
    }

    for key, ok in replaceability.items():
        if ok:
            passed.append(f"replaceability.{key}=true")
        else:
            failed.append(f"replaceability.{key}=false")

    if len(FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES) == 8:
        passed.append("replaceability.governance_rules_count=8")
    else:
        failed.append("replaceability.governance_rules_incomplete")

    all_ok = len(failed) == 0
    return replaceability, all_ok, passed, failed


def review_handoff_readiness(
    *,
    matrix_review_ok: bool,
    license_review: Dict[str, bool],
    selection_governance: Dict[str, bool],
    boundary_review: Dict[str, bool],
    evidence_provider_ok: bool,
    replaceability_ok: bool,
    decision: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    ready = (
        matrix_review_ok
        and all(license_review.values())
        and all(selection_governance.values())
        and all(boundary_review.values())
        and evidence_provider_ok
        and replaceability_ok
        and decision.get("adapter_contract_required") is True
        and decision.get("license_gate_required") is True
    )

    handoff = {
        "ready_for_decision_handoff": ready,
        "ready_for_slam_adapter_contract_planning": ready,
        "ready_for_license_gate_later": decision.get("license_gate_required") is True,
        "ready_for_weekly_open_spatial_stack_watch": ready,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    return handoff, passed, failed


def review_field_slam_framework_selection_matrix_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_framework_selection_matrix_v1()
    step1_summary = summarize_framework_selection_matrix_v1()
    matrix_ok, matrix_issues = validate_framework_selection_matrix_v1(matrix)

    frameworks = matrix.get("frameworks") or []
    evaluations = matrix.get("evaluations") or []
    decision = matrix.get("decision") or {}

    all_passed: List[str] = []
    all_failed: List[str] = []

    for rel in STEP1_MATRIX_FILES:
        if (_REPO_ROOT / rel).is_file():
            all_passed.append(f"step1.file_present={rel.split('/')[-1]}")
        else:
            all_failed.append(f"step1.file_missing={rel}")

    if step1_summary.get("final_decision") == FINAL_DECISION_MATRIX_READY:
        all_passed.append(f"step1.final_decision={FINAL_DECISION_MATRIX_READY}")
    else:
        all_failed.append(f"step1.final_decision={step1_summary.get('final_decision')!r}")

    if matrix_ok:
        all_passed.append("matrix_validation_ok=true")
    else:
        all_failed.extend(matrix_issues)

    baseline_ok, baseline, p, f = review_matrix_baseline(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    license_review, p, f = review_license_governance(frameworks, decision)
    all_passed.extend(p)
    all_failed.extend(f)

    selection_governance, p, f = review_selection_governance(frameworks, evaluations, decision)
    all_passed.extend(p)
    all_failed.extend(f)

    evidence_provider_ok, p, f = review_field_spatial_evidence_provider_boundary()
    all_passed.extend(p)
    all_failed.extend(f)

    replaceability_review, replaceability_ok, p, f = review_framework_replaceability_governance(
        frameworks, decision
    )
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_boundary_scope()
    all_passed.extend(p)
    all_failed.extend(f)

    handoff_readiness, p, f = review_handoff_readiness(
        matrix_review_ok=matrix_ok and baseline_ok,
        license_review=license_review,
        selection_governance=selection_governance,
        boundary_review=boundary_review,
        evidence_provider_ok=evidence_provider_ok,
        replaceability_ok=replaceability_ok,
        decision=decision,
    )
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        matrix_ok
        and baseline_ok
        and step1_summary.get("final_decision") == FINAL_DECISION_MATRIX_READY
        and all(license_review.values())
        and all(selection_governance.values())
        and all(boundary_review.values())
        and evidence_provider_ok
        and replaceability_ok
        and decision.get("adapter_contract_required") is True
        and decision.get("license_gate_required") is True
        and blocker_count == 0
        and handoff_readiness.get("ready_for_decision_handoff") is True
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 2 Matrix Review",
        "input_matrix_module": "field_slam_framework_selection_matrix_v1.py",
        "matrix_review_ok": matrix_ok and baseline_ok,
        "review_scope": {
            "framework_candidates_reviewed": baseline_ok,
            "framework_evaluations_reviewed": baseline_ok,
            "selection_decision_reviewed": bool(decision),
            "license_risk_reviewed": license_review.get("gpl_frameworks_blocked_from_commercial_runtime") is True,
            "commercial_runtime_boundary_reviewed": license_review.get("p0_technical_not_commercial_runtime") is True,
            "field_spatial_evidence_provider_boundary_reviewed": evidence_provider_ok,
            "framework_replaceability_governance_reviewed": replaceability_ok,
        },
        "baseline": baseline,
        "license_review": license_review,
        "selection_governance_review": selection_governance,
        "framework_replaceability_governance_review": {
            "governance_id": FRAMEWORK_REPLACEABILITY_GOVERNANCE_ID,
            "governance_rules": list(FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES),
            "framework_replaceability_governance_ok": replaceability_ok,
            **replaceability_review,
        },
        "boundary_review": boundary_review,
        "field_spatial_evidence_provider_independent": evidence_provider_ok,
        "handoff_readiness": handoff_readiness,
        "step1_summary": {
            "gpl_runtime_blocked": step1_summary.get("gpl_runtime_blocked"),
            "grapheqa_runtime_blocked": step1_summary.get("grapheqa_runtime_blocked"),
            "adapter_contract_required": step1_summary.get("adapter_contract_required"),
            "license_gate_required": step1_summary.get("license_gate_required"),
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if go_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_field_slam_framework_selection_matrix_v1()
    print(
        json.dumps(
            {
                "matrix_review_ok": result["matrix_review_ok"],
                "framework_count": result["baseline"]["framework_count"],
                "evaluation_count": result["baseline"]["evaluation_count"],
                "gpl_runtime_blocked": result["license_review"]["gpl_frameworks_blocked_from_commercial_runtime"],
                "p0_technical_not_commercial_runtime": result["license_review"]["p0_technical_not_commercial_runtime"],
                "grapheqa_observation_only": result["selection_governance_review"]["grapheqa_not_runtime_slam"],
                "framework_replaceability_governance_ok": result["framework_replaceability_governance_review"][
                    "framework_replaceability_governance_ok"
                ],
                "adapter_contract_required": result["step1_summary"]["adapter_contract_required"],
                "license_gate_required": result["step1_summary"]["license_gate_required"],
                "blocker_count": result["blocker_count"],
                "output_review_file": result.get("output_review_file"),
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
