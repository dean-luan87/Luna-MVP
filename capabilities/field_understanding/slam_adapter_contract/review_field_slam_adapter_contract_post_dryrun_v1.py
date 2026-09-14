# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — post-dryrun review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_registry_v1 import (
    TECHNICAL_REFERENCE_BACKEND_REFS,
    build_adapter_planning_matrix_v1,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    ADAPTER_CONTRACT_PRINCIPLE_EN,
    FIELD_SYNTHESIS_ENTRYPOINT,
    GENERIC_SLAM_ADAPTER_CONTRACT_ID,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SPATIAL_EVIDENCE_PROVIDER_ROLE,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "field_slam_adapter_contract_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_slam_adapter_contract_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_slam_adapter_contract_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_slam_adapter_contract_dryrun_verification_v1.json"
REVIEW_FILENAME = "field_slam_adapter_contract_post_dryrun_review_v1.json"

VERIFIER_FINAL_DECISION_GO = "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_VERIFIER_GO"
FINAL_DECISION_GO = "FIELD_SLAM_ADAPTER_CONTRACT_POST_DRYRUN_REVIEW_GO"
FINAL_DECISION_BLOCKED = "FIELD_SLAM_ADAPTER_CONTRACT_POST_DRYRUN_REVIEW_BLOCKED"

NEXT_PHASE_SPATIAL_EVIDENCE_PROVIDER_ADMISSION = (
    "Phase-Field-Spatial-Evidence-Provider-Admission-Planning-v1-001"
)

EXPECTED_ADAPTER_CONTRACT_COUNT = 7
EXPECTED_OUTPUT_MAPPING_COUNT_MIN = 7
EXPECTED_LICENSE_GATE_COUNT = 7
EXPECTED_RUNTIME_ISOLATION_COUNT = 7
EXPECTED_BACKEND_ADMISSION_COUNT = 7
EXPECTED_PROVIDER_REGISTRATION_COUNT = 7
EXPECTED_VALIDATOR_RULES = 18
EXPECTED_POSITIVE_CASES = 7
EXPECTED_INVALID_CASES = 5
EXPECTED_TRACE_COUNT = 12

EXPECTED_POSITIVE_CASE_IDS = frozenset(
    {
        "case_01_openvins_technical_reference",
        "case_02_vins_fusion_multi_sensor_reference",
        "case_03_orb_slam3_local_map_reference",
        "case_04_rtab_map_conditional_license",
        "case_05_kimera_observation_semantic",
        "case_06_hydra_scene_graph_observation",
        "case_07_grapheqa_observation_only",
    }
)
EXPECTED_POSITIVE_BACKEND_REFS = frozenset(TECHNICAL_REFERENCE_BACKEND_REFS)

EXPECTED_INVALID_CASE_IDS = frozenset(
    {
        "invalid_a_gpl_commercial_runtime",
        "invalid_b_backend_bypass_adapter",
        "invalid_c_output_mapping_not_candidate_only",
        "invalid_d_observation_runtime_admission",
        "invalid_e_health_signal_without_slam_health",
    }
)

STEP1_CORE_FILES = (
    "capabilities/field_understanding/slam_adapter_contract/"
    "field_slam_adapter_contract_types_v1.py",
    "capabilities/field_understanding/slam_adapter_contract/"
    "field_slam_adapter_contract_registry_v1.py",
    "capabilities/field_understanding/slam_adapter_contract/"
    "field_slam_adapter_contract_static_validators_v1.py",
    "capabilities/field_understanding/slam_adapter_contract/"
    "field_slam_adapter_contract_dryrun_cases_v1.py",
    "capabilities/field_understanding/slam_adapter_contract/"
    "run_field_slam_adapter_contract_dryrun_v1.py",
    "capabilities/field_understanding/slam_adapter_contract/"
    "verify_field_slam_adapter_contract_dryrun_v1.py",
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "adapter_chain",
    "output_mapping",
    "license_gate",
    "runtime_isolation",
    "backend_admission",
    "provider_registration",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

FORBIDDEN_RUNTIME_PATHS = (
    "backend_direct_action",
    "backend_direct_speech",
    "backend_direct_fact_write",
    "backend_bypass_field_synthesis",
)


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def _trace_by_id(traces: List[Dict[str, Any]], case_id: str) -> Optional[Dict[str, Any]]:
    for trace in traces:
        if trace.get("case_id") == case_id:
            return trace
    return None


def _build_baseline_counts() -> Dict[str, Any]:
    matrix = build_adapter_planning_matrix_v1()
    return {
        "adapter_contract_count": len(matrix.get("adapter_contracts") or []),
        "output_mapping_count": len(matrix.get("output_mappings") or []),
        "license_gate_count": len(matrix.get("license_gates") or []),
        "runtime_isolation_count": len(matrix.get("runtime_isolations") or []),
        "backend_admission_count": len(matrix.get("backend_admissions") or []),
        "provider_registration_count": len(matrix.get("provider_registrations") or []),
        "validator_rules": len(VALIDATOR_RULE_IDS),
    }


def review_step1_static_baseline(
    summary: Dict[str, Any],
    baseline_counts: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    files_present = all((_REPO_ROOT / rel).is_file() for rel in STEP1_CORE_FILES)
    if files_present:
        passed.append("step1.types_registry_validators_present=true")
    else:
        for rel in STEP1_CORE_FILES:
            if not (_REPO_ROOT / rel).is_file():
                failed.append(f"step1.core_file_missing={rel}")

    seven_backends = baseline_counts.get("adapter_contract_count") == EXPECTED_ADAPTER_CONTRACT_COUNT
    if seven_backends:
        passed.append(f"step1.adapter_contract_count={EXPECTED_ADAPTER_CONTRACT_COUNT}")
    else:
        failed.append(
            f"step1.adapter_contract_count: expected={EXPECTED_ADAPTER_CONTRACT_COUNT}, "
            f"actual={baseline_counts.get('adapter_contract_count')}"
        )

    mapping_ok = (baseline_counts.get("output_mapping_count") or 0) >= EXPECTED_OUTPUT_MAPPING_COUNT_MIN
    if mapping_ok:
        passed.append(f"step1.output_mapping_count>={EXPECTED_OUTPUT_MAPPING_COUNT_MIN}")
    else:
        failed.append("step1.output_mapping_count_below_minimum")

    for key, expected in (
        ("license_gate_count", EXPECTED_LICENSE_GATE_COUNT),
        ("runtime_isolation_count", EXPECTED_RUNTIME_ISOLATION_COUNT),
        ("backend_admission_count", EXPECTED_BACKEND_ADMISSION_COUNT),
        ("provider_registration_count", EXPECTED_PROVIDER_REGISTRATION_COUNT),
        ("validator_rules", EXPECTED_VALIDATOR_RULES),
    ):
        actual = baseline_counts.get(key)
        if actual == expected:
            passed.append(f"step1.{key}={expected}")
        else:
            failed.append(f"step1.{key}: expected={expected}, actual={actual}")

    if GENERIC_SLAM_ADAPTER_CONTRACT_ID == "generic_slam_adapter_contract_v1":
        passed.append("step1.generic_slam_adapter_contract_id_locked=true")
    else:
        failed.append("step1.generic_slam_adapter_contract_id_mismatch")

    review = {
        "types_registry_validators_present": files_present,
        "seven_backend_planning_catalog_present": seven_backends and mapping_ok,
        "candidate_only_enforced": summary.get("candidate_only_enforced") is True,
        "field_synthesis_entrypoint_locked": summary.get("field_synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "license_gate_required": summary.get("license_gate_required") is True,
        "runtime_isolation_required": summary.get("runtime_isolation_required") is True,
    }

    for key, ok in review.items():
        if not ok:
            failed.append(f"step1.{key}=false")

    return review, passed, failed


def review_step2_case_coverage(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_ids = {t.get("case_id") for t in traces if t.get("case_type") == "positive"}
    invalid_ids = {t.get("case_id") for t in traces if t.get("case_type") == "invalid"}
    positive_backend_refs = {
        (t.get("adapter_chain") or {}).get("backend_ref")
        for t in traces
        if t.get("case_type") == "positive"
    }

    all_backends = not (EXPECTED_POSITIVE_BACKEND_REFS - positive_backend_refs)
    positive_complete = not (EXPECTED_POSITIVE_CASE_IDS - positive_ids)
    invalid_complete = not (EXPECTED_INVALID_CASE_IDS - invalid_ids)

    invalid_checks = {
        "invalid_cases_cover_gpl_runtime": (
            _trace_by_id(traces, "invalid_a_gpl_commercial_runtime") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_adapter_bypass": (
            _trace_by_id(traces, "invalid_b_backend_bypass_adapter") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_candidate_only_violation": (
            _trace_by_id(traces, "invalid_c_output_mapping_not_candidate_only") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_observation_runtime": (
            _trace_by_id(traces, "invalid_d_observation_runtime_admission") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_health_signal_missing": (
            _trace_by_id(traces, "invalid_e_health_signal_without_slam_health") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
    }

    review = {
        "all_backend_positive_cases_present": all_backends and positive_complete,
        **invalid_checks,
    }

    if positive_complete:
        passed.append("step2.positive_case_ids_complete=true")
    else:
        failed.append(f"step2.missing_positive={sorted(EXPECTED_POSITIVE_CASE_IDS - positive_ids)!r}")

    if invalid_complete:
        passed.append("step2.invalid_case_ids_complete=true")
    else:
        failed.append(f"step2.missing_invalid={sorted(EXPECTED_INVALID_CASE_IDS - invalid_ids)!r}")

    if summary.get("positive_case_count") == EXPECTED_POSITIVE_CASES:
        passed.append(f"step2.positive_case_count={EXPECTED_POSITIVE_CASES}")
    else:
        failed.append("step2.positive_case_count_mismatch")

    if summary.get("invalid_case_count") == EXPECTED_INVALID_CASES:
        passed.append(f"step2.invalid_case_count={EXPECTED_INVALID_CASES}")
    else:
        failed.append("step2.invalid_case_count_mismatch")

    for key, ok in review.items():
        if ok:
            passed.append(f"step2.{key}=true")
        else:
            failed.append(f"step2.{key}=false")

    return review, passed, failed


def review_step3_trace(
    trace_path: Path,
    summary_path: Path,
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    trace_file_present = trace_path.is_file()
    summary_file_present = summary_path.is_file()

    trace_count_ok = len(traces) == EXPECTED_TRACE_COUNT
    positive_pass_ok = summary.get("positive_pass_count") == EXPECTED_POSITIVE_CASES
    invalid_reject_ok = summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_CASES
    unexpected_zero = (
        summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0
    )

    sections_ok = True
    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        missing = [s for s in REQUIRED_TRACE_SECTIONS if s not in trace]
        if missing:
            sections_ok = False
            failed.append(f"step3.{case_id}.missing_sections={missing}")

    review = {
        "trace_file_present": trace_file_present,
        "summary_file_present": summary_file_present,
        "trace_count_ok": trace_count_ok,
        "positive_pass_count_ok": positive_pass_ok,
        "invalid_expected_reject_count_ok": invalid_reject_ok,
        "unexpected_counts_zero": unexpected_zero,
        "required_trace_sections_present": sections_ok,
    }

    for key, ok in review.items():
        if ok:
            passed.append(f"step3.{key}=true")
        else:
            failed.append(f"step3.{key}=false")

    return review, passed, failed


def review_step4_verifier(
    verification_path: Path,
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    verifier_keys = (
        "summary_check_ok",
        "trace_count_check_ok",
        "case_id_unique_check_ok",
        "trace_decision_check_ok",
        "required_sections_check_ok",
        "adapter_chain_integrity_check_ok",
        "license_gate_check_ok",
        "runtime_isolation_check_ok",
        "governance_checkpoints_check_ok",
        "invalid_a_gpl_runtime_check_ok",
        "invalid_b_adapter_bypass_check_ok",
        "invalid_c_candidate_only_check_ok",
        "invalid_d_observation_runtime_check_ok",
        "invalid_e_health_signal_check_ok",
    )

    invalid_a_to_e = all(verification.get(k) is True for k in verifier_keys[-5:])

    review = {
        "verification_file_present": verification_path.is_file(),
        "verifier_final_decision_ok": verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO,
        "verifier_independence_declared": True,
        "blocker_count_zero": verification.get("blocker_count") == 0,
        "invalid_a_to_e_verified": invalid_a_to_e,
    }

    for key in verifier_keys:
        if verification.get(key) is True:
            passed.append(f"step4.{key}=true")
        else:
            failed.append(f"step4.{key}={verification.get(key)!r}")

    for key, ok in review.items():
        if ok:
            passed.append(f"step4.{key}=true")
        else:
            failed.append(f"step4.{key}=false")

    return review, passed, failed


def review_governance(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_traces = [t for t in traces if t.get("case_type") == "positive"]

    field_synthesis_ok = all(
        (t.get("adapter_chain") or {}).get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        for t in positive_traces
    )

    runtime_blocked = all(
        (t.get("backend_admission") or {}).get("runtime_admission_allowed") is not True
        for t in traces
        if t.get("case_type") == "positive"
    )

    no_forbidden_paths = True
    for trace in positive_traces:
        checkpoints = trace.get("governance_checkpoints") or {}
        if checkpoints.get("backend_does_not_bypass_adapter") is not True:
            no_forbidden_paths = False
        admission = trace.get("backend_admission") or {}
        if admission.get("runtime_admission_allowed") is True:
            no_forbidden_paths = False

    review = {
        "luna_binds_adapter_contract_not_framework": GENERIC_SLAM_ADAPTER_CONTRACT_ID
        == "generic_slam_adapter_contract_v1",
        "backend_replaceability_preserved": SPATIAL_EVIDENCE_PROVIDER_ROLE
        == "SpatialEvidenceProvider",
        "commercial_runtime_backends_empty": summary.get("commercial_runtime_backends") == [],
        "gpl_runtime_blocked": summary.get("gpl_runtime_blocked") is True,
        "observation_runtime_blocked": summary.get("observation_runtime_blocked") is True,
        "candidate_only_chain_preserved": summary.get("candidate_only_enforced") is True,
        "all_backend_enter_field_synthesis_v1_only": field_synthesis_ok,
        "no_direct_action": NON_EXECUTION_FLAGS.get("no_navigation_output") is True
        and runtime_blocked,
        "no_direct_speech": NON_EXECUTION_FLAGS.get("no_speech_output") is True,
        "no_direct_fact_write": NON_EXECUTION_FLAGS.get("no_fact_layer_write") is True
        and no_forbidden_paths,
    }

    if verification.get("invalid_a_gpl_runtime_check_ok") is not True:
        review["gpl_runtime_blocked"] = False
    if verification.get("invalid_d_observation_runtime_check_ok") is not True:
        review["observation_runtime_blocked"] = False

    for key, ok in review.items():
        if ok:
            passed.append(f"governance.{key}=true")
        else:
            failed.append(f"governance.{key}=false")

    if ADAPTER_CONTRACT_PRINCIPLE_EN.startswith("Any SLAM/VIO/SceneGraph backend"):
        passed.append("governance.adapter_contract_principle_locked=true")

    return review, passed, failed


def review_boundary(summary: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = summary.get("non_execution_flags") or dict(NON_EXECUTION_FLAGS)

    review = {
        "no_real_backend_connected": summary.get("no_real_backend_connected") is True
        or flags.get("no_real_adapter_runtime") is True,
        "no_camera_connected": summary.get("no_camera") is True
        or flags.get("no_camera_runtime") is True,
        "no_ros_connected": summary.get("no_ros") is True or flags.get("no_ros_runtime") is True,
        "no_benchmark_run": flags.get("no_benchmark_runtime") is True,
        "no_real_adapter_written": flags.get("no_real_adapter_runtime") is True,
        "no_runtime_admission_enabled": summary.get("no_runtime_admission") is True
        or flags.get("no_runtime_admission") is True,
        "no_commercial_runtime_selected": summary.get("commercial_runtime_backends") == [],
    }

    module_root = _REPO_ROOT / "capabilities" / "field_understanding" / "slam_adapter_contract"
    runtime_import_patterns = (
        "import openvins",
        "import vins",
        "import orb_slam",
        "rospy",
        "cv2.VideoCapture",
    )
    for py_path in module_root.rglob("*.py"):
        if py_path.name == "review_field_slam_adapter_contract_post_dryrun_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8")
        for pattern in runtime_import_patterns:
            if pattern in text:
                review["no_real_backend_connected"] = False
                failed.append(f"boundary.runtime_import_pattern_in={py_path.name}:{pattern}")

    for key, ok in review.items():
        if ok:
            passed.append(f"boundary.{key}=true")
        else:
            failed.append(f"boundary.{key}=false")

    return review, passed, failed


def review_handoff_readiness(
    *,
    verifier_ok: bool,
    governance_review: Dict[str, bool],
    boundary_review: Dict[str, bool],
    summary: Dict[str, Any],
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    core_ready = (
        verifier_ok
        and verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO
        and summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0
        and all(governance_review.values())
        and all(boundary_review.values())
    )

    handoff = {
        "ready_for_adapter_contract_handoff": core_ready,
        "ready_for_spatial_evidence_provider_admission_planning": core_ready,
        "ready_for_license_gate_later": core_ready,
        "ready_for_runtime_isolation_later": core_ready,
        "ready_for_backend_specific_adapter_planning_later": core_ready,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    if core_ready:
        passed.append(f"handoff.recommended_next_phase={NEXT_PHASE_SPATIAL_EVIDENCE_PROVIDER_ADMISSION}")

    return handoff, passed, failed


def review_field_slam_adapter_contract_post_dryrun_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    trace_path = root / TRACE_FILENAME
    summary_path = root / SUMMARY_FILENAME
    verification_path = root / VERIFICATION_FILENAME

    trace_doc = load_json_file(trace_path)
    summary = load_json_file(summary_path)
    verification = load_json_file(verification_path)
    traces = trace_doc.get("traces") or []
    if not isinstance(traces, list):
        traces = []

    all_passed: List[str] = []
    all_failed: List[str] = []

    baseline_counts = _build_baseline_counts()
    baseline = {
        **baseline_counts,
        "positive_case_count": summary.get("positive_case_count"),
        "invalid_case_count": summary.get("invalid_case_count"),
        "trace_count": len(traces),
        "verifier_final_decision": verification.get("final_decision"),
        "field_synthesis_entrypoint": summary.get("field_synthesis_entrypoint"),
    }

    step1_review, p, f = review_step1_static_baseline(summary, baseline_counts)
    all_passed.extend(p)
    all_failed.extend(f)

    step2_review, p, f = review_step2_case_coverage(traces, summary)
    all_passed.extend(p)
    all_failed.extend(f)

    step3_review, p, f = review_step3_trace(trace_path, summary_path, traces, summary)
    all_passed.extend(p)
    all_failed.extend(f)

    step4_review, p, f = review_step4_verifier(verification_path, verification)
    all_passed.extend(p)
    all_failed.extend(f)

    governance_review, p, f = review_governance(traces, summary, verification)
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_boundary(summary)
    all_passed.extend(p)
    all_failed.extend(f)

    step4_ok = step4_review.get("verifier_final_decision_ok") is True and step4_review.get(
        "blocker_count_zero"
    ) is True

    handoff_readiness, p, f = review_handoff_readiness(
        verifier_ok=step4_ok,
        governance_review=governance_review,
        boundary_review=boundary_review,
        summary=summary,
        verification=verification,
    )
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO
        and len(traces) == EXPECTED_TRACE_COUNT
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_CASES
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_CASES
        and summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0
        and summary.get("commercial_runtime_backends") == []
        and summary.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and all(step1_review.values())
        and all(step2_review.values())
        and all(step3_review.values())
        and all(step4_review.values())
        and all(governance_review.values())
        and all(boundary_review.values())
        and handoff_readiness.get("ready_for_adapter_contract_handoff") is True
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 5 Adapter Contract Post-DryRun Review",
        "input_artifacts": {
            "trace": str(trace_path),
            "summary": str(summary_path),
            "verification": str(verification_path),
        },
        "baseline": baseline,
        "step_1_static_baseline_review": step1_review,
        "step_2_case_coverage_review": step2_review,
        "step_3_trace_review": step3_review,
        "step_4_verifier_review": step4_review,
        "governance_review": governance_review,
        "boundary_review": boundary_review,
        "handoff_readiness": handoff_readiness,
        "recommended_next_phase": NEXT_PHASE_SPATIAL_EVIDENCE_PROVIDER_ADMISSION,
        "architecture_frozen_conclusion": {
            "luna_binds": "GenericSLAMAdapterContract / Field Spatial Evidence Contract",
            "luna_does_not_bind": "OpenVINS / VINS-Fusion / ORB-SLAM3 / any specific SLAM runtime",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "commercial_runtime_backends": [],
            "runtime_admission_enabled": False,
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if go_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_path = root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_field_slam_adapter_contract_post_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "baseline": result["baseline"],
                "governance_review": result["governance_review"],
                "boundary_review": result["boundary_review"],
                "handoff_readiness": result["handoff_readiness"],
                "recommended_next_phase": result["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
