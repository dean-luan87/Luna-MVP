# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — post-dryrun review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    FORBIDDEN_PROVIDER_ADMISSION_POLICIES,
    build_provider_admission_planning_matrix_v1,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    ADMISSION_PRINCIPLE_EN,
    ADMISSION_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_spatial_evidence_provider_admission_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_spatial_evidence_provider_admission_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_spatial_evidence_provider_admission_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_spatial_evidence_provider_admission_dryrun_verification_v1.json"
REVIEW_FILENAME = "field_spatial_evidence_provider_admission_post_dryrun_review_v1.json"

VERIFIER_FINAL_DECISION_GO = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_VERIFIER_GO"
)
FINAL_DECISION_GO = "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POST_DRYRUN_REVIEW_GO"
FINAL_DECISION_BLOCKED = "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POST_DRYRUN_REVIEW_BLOCKED"

NEXT_PHASE_PROVIDER_ADMISSION_HANDOFF = (
    "Phase-Field-Spatial-Evidence-Provider-Admission-Handoff-v1-001"
)
NEXT_PHASE_PROVIDER_MANAGER_SKELETON = (
    "Phase-Field-Spatial-Evidence-Provider-Manager-Skeleton-Planning-v1-001"
)

EXPECTED_PROVIDER_POLICY_COUNT = 7
EXPECTED_CAPABILITY_PROFILE_COUNT = 7
EXPECTED_HEALTH_GATE_COUNT = 7
EXPECTED_FALLBACK_POLICY_COUNT = 7
EXPECTED_RUNTIME_ADMISSION_CANDIDATE_COUNT = 7
EXPECTED_VALIDATOR_RULES = 20
EXPECTED_POSITIVE_CASES = 7
EXPECTED_INVALID_CASES = 6
EXPECTED_TRACE_COUNT = 13

EXPECTED_POSITIVE_CASE_IDS = frozenset(
    {
        "case_01_openvins_technical_reference",
        "case_02_vins_fusion_technical_reference",
        "case_03_orb_slam3_local_map_reference",
        "case_04_rtab_map_legal_review_blocked",
        "case_05_kimera_observation_only",
        "case_06_hydra_observation_only",
        "case_07_grapheqa_observation_only",
    }
)

EXPECTED_INVALID_CASE_IDS = frozenset(
    {
        "invalid_a_gpl_provider_commercial_runtime",
        "invalid_b_observation_provider_runtime_admission",
        "invalid_c_runtime_admission_without_health_gate",
        "invalid_d_fallback_required_missing_policy",
        "invalid_e_field_synthesis_entrypoint_bypass",
        "invalid_f_required_candidates_not_in_profile",
    }
)

STEP1_CORE_FILES = (
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "field_spatial_evidence_provider_admission_types_v1.py",
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "field_spatial_evidence_provider_admission_registry_v1.py",
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "field_spatial_evidence_provider_admission_static_validators_v1.py",
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "field_spatial_evidence_provider_admission_dryrun_cases_v1.py",
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "run_field_spatial_evidence_provider_admission_dryrun_v1.py",
    "capabilities/field_understanding/spatial_evidence_provider_admission/"
    "verify_field_spatial_evidence_provider_admission_dryrun_v1.py",
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "provider_policy",
    "capability_profile",
    "health_gate",
    "fallback_policy",
    "runtime_admission",
    "planning_decision",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

FORBIDDEN_PROVIDER_PATHS = (
    "provider_direct_action",
    "provider_direct_speech",
    "provider_direct_fact_write",
    "provider_bypass_field_synthesis",
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
    matrix = build_provider_admission_planning_matrix_v1()
    decision = matrix.get("decision") or {}
    return {
        "provider_policy_count": len(matrix.get("admission_policies") or []),
        "capability_profile_count": len(matrix.get("capability_profiles") or []),
        "health_gate_count": len(matrix.get("health_gates") or []),
        "fallback_policy_count": len(matrix.get("fallback_policies") or []),
        "runtime_admission_candidate_count": len(
            matrix.get("runtime_admission_candidates") or []
        ),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "runtime_admission_candidates_empty": not decision.get("runtime_admission_candidates"),
        "commercial_runtime_candidates_empty": not decision.get("commercial_runtime_candidates"),
    }


def review_step1_static_baseline(
    summary: Dict[str, Any],
    baseline_counts: Dict[str, Any],
    traces: List[Dict[str, Any]],
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

    catalog_checks = {
        "provider_policy_count": EXPECTED_PROVIDER_POLICY_COUNT,
        "capability_profile_count": EXPECTED_CAPABILITY_PROFILE_COUNT,
        "health_gate_count": EXPECTED_HEALTH_GATE_COUNT,
        "fallback_policy_count": EXPECTED_FALLBACK_POLICY_COUNT,
        "runtime_admission_candidate_count": EXPECTED_RUNTIME_ADMISSION_CANDIDATE_COUNT,
        "validator_rules": EXPECTED_VALIDATOR_RULES,
    }
    seven_catalog = True
    for key, expected in catalog_checks.items():
        actual = baseline_counts.get(key)
        if actual == expected:
            passed.append(f"step1.{key}={expected}")
        else:
            seven_catalog = False
            failed.append(f"step1.{key}: expected={expected}, actual={actual}")

    positive_traces = [t for t in traces if t.get("case_type") == "positive"]
    adapter_implies_runtime = all(
        (t.get("runtime_admission") or {}).get("adapter_contract_passed") is True
        and (t.get("runtime_admission") or {}).get("runtime_admission_allowed") is not True
        for t in positive_traces
    )

    review = {
        "types_registry_validators_present": files_present,
        "seven_provider_planning_catalog_present": seven_catalog,
        "provider_admission_layer_declared": ADMISSION_PRINCIPLE_ZH == "能翻译，不等于能启用。",
        "adapter_contract_does_not_imply_runtime_enabled": adapter_implies_runtime,
        "field_synthesis_entrypoint_locked": summary.get("field_synthesis_entrypoint_locked")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_required": summary.get("health_gate_required") is True,
        "fallback_required": summary.get("fallback_required") is True,
        "provider_replaceability_required": summary.get("provider_replaceability_required")
        is True,
    }

    for key, ok in review.items():
        if ok:
            passed.append(f"step1.{key}=true")
        else:
            failed.append(f"step1.{key}=false")

    if ADMISSION_PRINCIPLE_EN.startswith("Provider Admission is the runtime admission layer"):
        passed.append("step1.admission_principle_en_locked=true")

    return review, passed, failed


def review_step2_case_coverage(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_ids = {t.get("case_id") for t in traces if t.get("case_type") == "positive"}
    invalid_ids = {t.get("case_id") for t in traces if t.get("case_type") == "invalid"}

    positive_complete = not (EXPECTED_POSITIVE_CASE_IDS - positive_ids)
    invalid_complete = not (EXPECTED_INVALID_CASE_IDS - invalid_ids)

    invalid_checks = {
        "invalid_cases_cover_gpl_commercial_runtime": (
            _trace_by_id(traces, "invalid_a_gpl_provider_commercial_runtime") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_observation_runtime": (
            _trace_by_id(traces, "invalid_b_observation_provider_runtime_admission") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_health_gate_bypass": (
            _trace_by_id(traces, "invalid_c_runtime_admission_without_health_gate") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_fallback_missing": (
            _trace_by_id(traces, "invalid_d_fallback_required_missing_policy") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_field_synthesis_bypass": (
            _trace_by_id(traces, "invalid_e_field_synthesis_entrypoint_bypass") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
        "invalid_cases_cover_capability_gap": (
            _trace_by_id(traces, "invalid_f_required_candidates_not_in_profile") or {}
        ).get("trace_decision") == "EXPECTED_REJECT",
    }

    review = {
        "all_provider_positive_cases_present": positive_complete,
        **invalid_checks,
    }

    if positive_complete:
        passed.append("step2.positive_case_ids_complete=true")
    else:
        failed.append(
            f"step2.missing_positive={sorted(EXPECTED_POSITIVE_CASE_IDS - positive_ids)!r}"
        )

    if invalid_complete:
        passed.append("step2.invalid_case_ids_complete=true")
    else:
        failed.append(
            f"step2.missing_invalid={sorted(EXPECTED_INVALID_CASE_IDS - invalid_ids)!r}"
        )

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
        "positive_runtime_still_disabled_check_ok",
        "field_synthesis_entrypoint_locked_check_ok",
        "health_gate_check_ok",
        "fallback_gate_check_ok",
        "capability_coverage_check_ok",
        "invalid_a_gpl_commercial_check_ok",
        "invalid_b_observation_runtime_check_ok",
        "invalid_c_health_gate_check_ok",
        "invalid_d_fallback_missing_check_ok",
        "invalid_e_field_synthesis_bypass_check_ok",
        "invalid_f_capability_coverage_check_ok",
    )

    invalid_a_to_f = all(verification.get(k) is True for k in verifier_keys[-6:])

    review = {
        "verification_file_present": verification_path.is_file(),
        "verifier_final_decision_ok": verification.get("final_decision") == VERIFIER_FINAL_DECISION_GO,
        "verifier_independence_declared": True,
        "blocker_count_zero": verification.get("blocker_count") == 0,
        "invalid_a_to_f_verified": invalid_a_to_f,
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
    baseline_counts: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    positive_traces = [t for t in traces if t.get("case_type") == "positive"]

    field_synthesis_ok = all(
        (t.get("provider_policy") or {}).get("field_synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT
        for t in positive_traces
    )

    runtime_blocked = all(
        (t.get("runtime_admission") or {}).get("runtime_admission_allowed") is not True
        for t in positive_traces
    )

    planning_runtime_empty = all(
        not (t.get("planning_decision") or {}).get("runtime_admission_candidates")
        for t in positive_traces
    )
    planning_commercial_empty = all(
        not (t.get("planning_decision") or {}).get("commercial_runtime_candidates")
        for t in positive_traces
    )

    candidate_only_ok = all(
        (t.get("governance_checkpoints") or {}).get("candidate_only_preserved") is True
        for t in positive_traces
    )

    capability_ok = all(
        (t.get("governance_checkpoints") or {}).get("required_candidates_covered_by_profile")
        is True
        for t in positive_traces
    )

    health_enforced = all(
        (t.get("governance_checkpoints") or {}).get("health_gate_required") is True
        for t in positive_traces
    )
    fallback_enforced = all(
        (t.get("governance_checkpoints") or {}).get("fallback_required") is True
        for t in positive_traces
    )

    translation_blocked = all(
        (t.get("governance_checkpoints") or {}).get(
            "adapter_contract_passed_does_not_imply_runtime_enabled"
        )
        is True
        for t in positive_traces
    )

    forbidden_present = all(path in FORBIDDEN_PROVIDER_ADMISSION_POLICIES for path in FORBIDDEN_PROVIDER_PATHS)

    review = {
        "translation_does_not_equal_enablement": (
            ADMISSION_PRINCIPLE_ZH == "能翻译，不等于能启用。" and translation_blocked
        ),
        "runtime_admission_candidates_empty": (
            summary.get("runtime_admission_candidates_empty") is True
            and baseline_counts.get("runtime_admission_candidates_empty") is True
            and planning_runtime_empty
        ),
        "commercial_runtime_candidates_empty": (
            summary.get("commercial_runtime_candidates_empty") is True
            and baseline_counts.get("commercial_runtime_candidates_empty") is True
            and planning_commercial_empty
        ),
        "gpl_commercial_blocked": summary.get("gpl_commercial_blocked") is True,
        "observation_runtime_blocked": summary.get("observation_runtime_blocked") is True,
        "field_synthesis_v1_only": field_synthesis_ok
        and summary.get("field_synthesis_entrypoint_locked") == FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_enforced": health_enforced
        and summary.get("health_gate_required") is True,
        "fallback_gate_enforced": fallback_enforced
        and summary.get("fallback_required") is True,
        "capability_coverage_enforced": capability_ok,
        "candidate_only_chain_preserved": candidate_only_ok,
        "no_direct_action": forbidden_present
        and NON_EXECUTION_FLAGS.get("no_navigation_output") is True
        and runtime_blocked,
        "no_direct_speech": forbidden_present
        and NON_EXECUTION_FLAGS.get("no_speech_output") is True,
        "no_direct_fact_write": forbidden_present
        and NON_EXECUTION_FLAGS.get("no_fact_layer_write") is True,
    }

    if verification.get("invalid_a_gpl_commercial_check_ok") is not True:
        review["gpl_commercial_blocked"] = False
    if verification.get("invalid_b_observation_runtime_check_ok") is not True:
        review["observation_runtime_blocked"] = False
    if verification.get("invalid_e_field_synthesis_bypass_check_ok") is not True:
        review["field_synthesis_v1_only"] = False
    if verification.get("invalid_f_capability_coverage_check_ok") is not True:
        review["capability_coverage_enforced"] = False

    for key, ok in review.items():
        if ok:
            passed.append(f"governance.{key}=true")
        else:
            failed.append(f"governance.{key}=false")

    return review, passed, failed


def review_boundary(summary: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = dict(NON_EXECUTION_FLAGS)

    review = {
        "no_real_provider_connected": summary.get("no_real_provider_connected") is True
        or flags.get("no_real_provider_runtime") is True,
        "no_real_backend_connected": summary.get("no_real_backend_connected") is True
        or flags.get("no_real_slam_backend") is True,
        "no_camera_connected": summary.get("no_camera") is True
        or flags.get("no_camera_runtime") is True,
        "no_ros_connected": summary.get("no_ros") is True or flags.get("no_ros_runtime") is True,
        "no_benchmark_run": flags.get("no_benchmark_runtime") is True,
        "no_provider_manager_written": flags.get("no_provider_manager_runtime") is True,
        "no_runtime_admission_enabled": summary.get("no_runtime_admission") is True
        or flags.get("no_runtime_admission") is True,
        "no_commercial_runtime_selected": flags.get("no_commercial_runtime_selection") is True
        and summary.get("commercial_runtime_candidates_empty") is True,
    }

    module_root = (
        _REPO_ROOT / "capabilities" / "field_understanding" / "spatial_evidence_provider_admission"
    )
    runtime_import_patterns = (
        "import openvins",
        "import vins",
        "import orb_slam",
        "import rtab",
        "import kimera",
        "import hydra",
        "rospy",
        "cv2.VideoCapture",
    )
    for py_path in module_root.rglob("*.py"):
        if py_path.name == "review_field_spatial_evidence_provider_admission_post_dryrun_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8")
        for pattern in runtime_import_patterns:
            if pattern in text:
                review["no_real_provider_connected"] = False
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
        "ready_for_provider_admission_handoff": core_ready,
        "ready_for_runtime_admission_skeleton_planning": core_ready,
        "ready_for_provider_manager_skeleton_later": core_ready,
        "ready_for_license_gate_runtime_later": core_ready,
        "ready_for_health_fallback_runtime_later": core_ready,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    if core_ready:
        passed.append(f"handoff.recommended_next_phase={NEXT_PHASE_PROVIDER_ADMISSION_HANDOFF}")
        passed.append(
            f"handoff.recommended_provider_manager_phase={NEXT_PHASE_PROVIDER_MANAGER_SKELETON}"
        )

    return handoff, passed, failed


def review_field_spatial_evidence_provider_admission_post_dryrun_v1(
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
        "field_synthesis_entrypoint": summary.get("field_synthesis_entrypoint_locked"),
    }

    step1_review, p, f = review_step1_static_baseline(summary, baseline_counts, traces)
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

    governance_review, p, f = review_governance(
        traces, summary, verification, baseline_counts
    )
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
        and summary.get("runtime_admission_candidates_empty") is True
        and summary.get("commercial_runtime_candidates_empty") is True
        and summary.get("field_synthesis_entrypoint_locked") == FIELD_SYNTHESIS_ENTRYPOINT
        and all(step1_review.values())
        and all(step2_review.values())
        and all(step3_review.values())
        and all(step4_review.values())
        and all(governance_review.values())
        and all(boundary_review.values())
        and handoff_readiness.get("ready_for_provider_admission_handoff") is True
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 5 Provider Admission Post-DryRun Review",
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
        "recommended_next_phase": NEXT_PHASE_PROVIDER_ADMISSION_HANDOFF,
        "recommended_provider_manager_phase": NEXT_PHASE_PROVIDER_MANAGER_SKELETON,
        "architecture_frozen_conclusion": {
            "admission_principle_zh": ADMISSION_PRINCIPLE_ZH,
            "adapter_contract_passed_does_not_imply_runtime_enabled": True,
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "runtime_admission_candidates": [],
            "commercial_runtime_candidates": [],
            "runtime_admission_enabled": False,
            "forbidden_provider_paths": list(FORBIDDEN_PROVIDER_PATHS),
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
    result = review_field_spatial_evidence_provider_admission_post_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "baseline": result["baseline"],
                "governance_review": result["governance_review"],
                "boundary_review": result["boundary_review"],
                "handoff_readiness": result["handoff_readiness"],
                "recommended_next_phase": result["recommended_next_phase"],
                "recommended_provider_manager_phase": result["recommended_provider_manager_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
