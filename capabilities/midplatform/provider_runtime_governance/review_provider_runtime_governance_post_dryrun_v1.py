# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — post-dryrun review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SHARED,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_VERIFIER_GO,
    FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED,
    FINAL_DECISION_POST_DRYRUN_REVIEW_GO,
    GOVERNANCE_PRINCIPLE_ZH,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SHARED_MANAGER_REF,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "shared_provider_runtime_governance_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "provider_runtime_governance_dryrun_trace_v1.json"
SUMMARY_FILENAME = "provider_runtime_governance_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "provider_runtime_governance_dryrun_verification_v1.json"
REVIEW_FILENAME = "provider_runtime_governance_post_dryrun_review_v1.json"

EXPECTED_SHARED_DATACLASS_COUNT = 10
EXPECTED_VALIDATOR_RULES = len(VALIDATOR_RULE_IDS)
EXPECTED_POSITIVE_CASES = 10
EXPECTED_INVALID_CASES = 7
EXPECTED_TRACE_COUNT = 17

SUPPORTED_DOMAINS = (DOMAIN_SHARED, DOMAIN_SPATIAL_EVIDENCE, DOMAIN_VISION_OCR)

EXPECTED_COMMON_CASE_IDS = frozenset(
    {
        "case_common_01_registered_default_disabled",
        "case_common_02_enable_request_candidate_only",
        "case_common_03_disable_request_planned_not_executed",
        "case_common_04_health_snapshot_degrade_disable",
        "case_common_05_fallback_route_preserves_chain",
        "case_common_06_admission_check_not_runtime_enabled",
    }
)

EXPECTED_SPATIAL_CASE_IDS = frozenset(
    {
        "case_spatial_01_profile_attached",
        "case_spatial_02_inherits_admission_boundaries",
    }
)

EXPECTED_VISION_OCR_CASE_IDS = frozenset(
    {
        "case_vision_ocr_01_compatibility_aligned",
        "case_vision_ocr_02_no_spatial_pollution",
    }
)

EXPECTED_INVALID_CASE_IDS = frozenset(
    {
        "invalid_a_default_enabled_provider",
        "invalid_b_runtime_activation_allowed",
        "invalid_c_missing_domain_profile",
        "invalid_d_direct_action_forbidden",
        "invalid_e_fallback_no_source_chain",
        "invalid_f_spatial_bypass_field_synthesis",
        "invalid_g_vision_ocr_spatial_candidate_pollution",
    }
)

STEP1_CORE_FILES = (
    "capabilities/midplatform/provider_runtime_governance/provider_runtime_governance_types_v1.py",
    "capabilities/midplatform/provider_runtime_governance/provider_runtime_governance_registry_v1.py",
    "capabilities/midplatform/provider_runtime_governance/provider_runtime_governance_static_validators_v1.py",
    "capabilities/midplatform/provider_runtime_governance/domain_profiles/"
    "spatial_evidence_provider_governance_profile_v1.py",
    "capabilities/midplatform/provider_runtime_governance/domain_profiles/"
    "vision_ocr_governance_compatibility_v1.py",
)

PIPELINE_FILES = (
    "capabilities/midplatform/provider_runtime_governance/provider_runtime_governance_dryrun_cases_v1.py",
    "capabilities/midplatform/provider_runtime_governance/run_provider_runtime_governance_dryrun_v1.py",
    "capabilities/midplatform/provider_runtime_governance/verify_provider_runtime_governance_dryrun_v1.py",
)

SUPERSEDED_MANAGER_DIR = (
    _REPO_ROOT / "capabilities" / "field_understanding" / "spatial_evidence_provider_manager"
)
PRIMARY_GOVERNANCE_DIR = _REPO_ROOT / "capabilities" / "midplatform" / "provider_runtime_governance"

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "manager",
    "domain_profile",
    "registry",
    "enable_disable",
    "runtime_state",
    "health_and_fallback",
    "runtime_admission",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

VERIFIER_INVALID_KEYS = (
    "invalid_a_default_enable_check_ok",
    "invalid_b_runtime_activation_check_ok",
    "invalid_c_domain_profile_missing_check_ok",
    "invalid_d_direct_output_check_ok",
    "invalid_e_fallback_source_chain_check_ok",
    "invalid_f_spatial_synthesis_bypass_check_ok",
    "invalid_g_vision_ocr_spatial_pollution_check_ok",
)

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})


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


def _positive_traces(traces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [t for t in traces if t.get("case_type") == "positive"]


def review_step1_static_baseline(
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    files_present = all((_REPO_ROOT / rel).is_file() for rel in STEP1_CORE_FILES)
    domain_profile_present = (
        (_REPO_ROOT / STEP1_CORE_FILES[3]).is_file()
        and (_REPO_ROOT / STEP1_CORE_FILES[4]).is_file()
    )

    review = {
        "types_registry_validators_present": files_present,
        "shared_provider_runtime_governance_ready": summary.get(
            "shared_provider_runtime_governance_ready"
        )
        is True,
        "domain_profile_abstraction_present": domain_profile_present,
        "runtime_activation_disabled_by_default": summary.get("runtime_activation_allowed") is False,
        "provider_runtime_disabled_by_default": summary.get("provider_runtime_enabled") is False,
    }

    if files_present:
        passed.append("step1.core_files_present=true")
    else:
        for rel in STEP1_CORE_FILES:
            if not (_REPO_ROOT / rel).is_file():
                failed.append(f"step1.core_file_missing={rel}")

    if GOVERNANCE_PRINCIPLE_ZH.startswith("共享 Provider Runtime Governance"):
        passed.append("step1.governance_principle_zh_locked=true")

    for key, ok in review.items():
        if ok:
            passed.append(f"step1.{key}=true")
        else:
            failed.append(f"step1.{key}=false")

    return review, passed, failed


def review_step2_case_coverage(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    trace_ids = {t.get("case_id") for t in traces}

    common_present = EXPECTED_COMMON_CASE_IDS.issubset(trace_ids)
    spatial_present = EXPECTED_SPATIAL_CASE_IDS.issubset(trace_ids)
    vision_present = EXPECTED_VISION_OCR_CASE_IDS.issubset(trace_ids)
    invalid_present = EXPECTED_INVALID_CASE_IDS.issubset(trace_ids)

    review = {
        "common_governance_cases_present": common_present,
        "spatial_evidence_profile_cases_present": spatial_present,
        "vision_ocr_compatibility_cases_present": vision_present,
        "invalid_cases_cover_runtime_activation": (
            _trace_by_id(traces, "invalid_b_runtime_activation_allowed") or {}
        ).get("trace_decision")
        == "EXPECTED_REJECT",
        "invalid_cases_cover_missing_domain_profile": (
            _trace_by_id(traces, "invalid_c_missing_domain_profile") or {}
        ).get("trace_decision")
        == "EXPECTED_REJECT",
        "invalid_cases_cover_direct_output": (
            _trace_by_id(traces, "invalid_d_direct_action_forbidden") or {}
        ).get("trace_decision")
        == "EXPECTED_REJECT",
        "invalid_cases_cover_fallback_source_chain": (
            _trace_by_id(traces, "invalid_e_fallback_no_source_chain") or {}
        ).get("trace_decision")
        == "EXPECTED_REJECT",
        "invalid_cases_cover_domain_pollution": (
            _trace_by_id(traces, "invalid_g_vision_ocr_spatial_candidate_pollution") or {}
        ).get("trace_decision")
        == "EXPECTED_REJECT",
    }

    if invalid_present:
        passed.append("step2.invalid_case_ids_complete=true")
    else:
        failed.append(
            f"step2.missing_invalid={sorted(EXPECTED_INVALID_CASE_IDS - trace_ids)!r}"
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

    sections_ok = True
    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        missing = [s for s in REQUIRED_TRACE_SECTIONS if s not in trace]
        if missing:
            sections_ok = False
            failed.append(f"step3.{case_id}.missing_sections={missing}")

    review = {
        "trace_file_present": trace_path.is_file(),
        "summary_file_present": summary_path.is_file(),
        "trace_count_ok": len(traces) == EXPECTED_TRACE_COUNT,
        "positive_pass_count_ok": summary.get("positive_pass_count") == EXPECTED_POSITIVE_CASES,
        "invalid_expected_reject_count_ok": summary.get("invalid_expected_reject_count")
        == EXPECTED_INVALID_CASES,
        "unexpected_counts_zero": summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0,
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

    invalid_a_to_g = all(verification.get(k) is True for k in VERIFIER_INVALID_KEYS)

    review = {
        "verification_file_present": verification_path.is_file(),
        "verifier_final_decision_ok": verification.get("final_decision")
        == FINAL_DECISION_DRYRUN_VERIFIER_GO,
        "verifier_independence_declared": True,
        "blocker_count_zero": verification.get("blocker_count") == 0,
        "invalid_a_to_g_verified": invalid_a_to_g,
    }

    for key in VERIFIER_INVALID_KEYS:
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

    positive = _positive_traces(traces)

    runtime_disabled = all(
        (t.get("manager") or {}).get("runtime_activation_allowed") is not True
        and (t.get("manager") or {}).get("provider_runtime_enabled") is not True
        and (t.get("runtime_state") or {}).get("provider_runtime_enabled") is not True
        and not (t.get("runtime_state") or {}).get("runtime_enabled_provider_refs")
        for t in positive
    )

    spatial_positive = [
        t
        for t in positive
        if (t.get("domain_profile") or {}).get("domain_id") == DOMAIN_SPATIAL_EVIDENCE
    ]
    spatial_can_require_spatial_candidates = bool(spatial_positive) and all(
        FIELD_SYNTHESIS_ENTRYPOINT
        in str((t.get("domain_profile") or {}).get("synthesis_entrypoint") or "")
        and any(
            ctype in ((t.get("domain_profile") or {}).get("candidate_types") or ())
            for ctype in _SPATIAL_POLLUTION_CANDIDATES
        )
        for t in spatial_positive
    )

    vision_positive = [
        t
        for t in positive
        if (t.get("domain_profile") or {}).get("domain_id") == DOMAIN_VISION_OCR
    ]
    vision_not_polluted = all(
        not any(
            ctype in ((t.get("domain_profile") or {}).get("candidate_types") or ())
            for ctype in _SPATIAL_POLLUTION_CANDIDATES
        )
        and (t.get("governance_checkpoints") or {}).get("vision_ocr_compatibility_preserved")
        is True
        for t in vision_positive
    )

    direct_output_blocked = all(
        (t.get("governance_checkpoints") or {}).get("no_direct_action") is True
        and (t.get("governance_checkpoints") or {}).get("no_direct_speech") is True
        and (t.get("governance_checkpoints") or {}).get("no_direct_fact_write") is True
        for t in positive
    )

    fallback_ok = all(
        (t.get("governance_checkpoints") or {}).get("fallback_preserves_source_chain") is True
        for t in positive
    )

    runtime_frozen = (
        summary.get("runtime_activation_allowed") is False
        and summary.get("provider_runtime_enabled") is False
        and runtime_disabled
    )

    review = {
        "shared_provider_runtime_governance_ready": summary.get(
            "shared_provider_runtime_governance_ready"
        )
        is True,
        "vision_ocr_compatibility_preserved": summary.get("vision_ocr_compatibility_preserved")
        is True
        and vision_not_polluted
        and verification.get("vision_ocr_compatibility_boundary_check_ok") is True,
        "spatial_evidence_profile_supported": summary.get("spatial_evidence_profile_supported")
        is True
        and spatial_can_require_spatial_candidates,
        "no_domain_specific_manager_duplication": summary.get(
            "no_domain_specific_manager_duplication"
        )
        is True
        and verification.get("no_domain_specific_manager_duplication_check_ok") is True,
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "candidate_only_enforced": summary.get("candidate_only_enforced") is True,
        "domain_profile_required": summary.get("domain_profile_required") is True,
        "fallback_preserves_source_chain": fallback_ok,
        "no_direct_action": direct_output_blocked
        and NON_EXECUTION_FLAGS.get("no_navigation_output") is True,
        "no_direct_speech": direct_output_blocked
        and NON_EXECUTION_FLAGS.get("no_speech_output") is True,
        "no_direct_fact_write": direct_output_blocked
        and NON_EXECUTION_FLAGS.get("no_fact_layer_write") is True,
    }

    if not runtime_frozen:
        failed.append("governance.runtime_not_frozen")

    for key, ok in review.items():
        if key in ("runtime_activation_allowed", "provider_runtime_enabled"):
            if ok is False and runtime_frozen:
                passed.append(f"governance.{key}=false")
            else:
                failed.append(f"governance.{key}={ok!r}")
        elif ok is True:
            passed.append(f"governance.{key}=true")
        else:
            failed.append(f"governance.{key}={ok!r}")

    return review, passed, failed


def review_superseded_path() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    superseded_marked = False
    if SUPERSEDED_MANAGER_DIR.is_dir():
        for py_path in SUPERSEDED_MANAGER_DIR.rglob("*.py"):
            text = py_path.read_text(encoding="utf-8")
            if "SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE" in text:
                superseded_marked = True
                break

    step2_not_continued = not any(
        name.startswith("field_spatial_evidence_provider_manager_dryrun")
        or name.startswith("run_field_spatial_evidence_provider_manager")
        for name in (p.name for p in SUPERSEDED_MANAGER_DIR.rglob("*.py"))
    )

    primary_pipeline = all((_REPO_ROOT / rel).is_file() for rel in PIPELINE_FILES)
    primary_has_shared_manager = any(
        SHARED_MANAGER_REF in py_path.read_text(encoding="utf-8")
        for py_path in PRIMARY_GOVERNANCE_DIR.rglob("*.py")
        if py_path.name != "review_provider_runtime_governance_post_dryrun_v1.py"
    )

    review = {
        "spatial_evidence_independent_manager_marked_superseded": superseded_marked,
        "spatial_evidence_manager_step2_not_continued": step2_not_continued,
        "shared_midplatform_governance_is_primary": primary_pipeline and primary_has_shared_manager,
    }

    for key, ok in review.items():
        if ok:
            passed.append(f"superseded.{key}=true")
        else:
            failed.append(f"superseded.{key}=false")

    return review, passed, failed


def review_handoff_readiness(
    *,
    step4_ok: bool,
    governance_review: Dict[str, bool],
    superseded_review: Dict[str, bool],
    summary: Dict[str, Any],
    verification: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    core_ready = (
        step4_ok
        and verification.get("final_decision") == FINAL_DECISION_DRYRUN_VERIFIER_GO
        and summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0
        and governance_review.get("shared_provider_runtime_governance_ready") is True
        and governance_review.get("no_domain_specific_manager_duplication") is True
        and superseded_review.get("shared_midplatform_governance_is_primary") is True
    )

    runtime_frozen = (
        summary.get("runtime_activation_allowed") is False
        and summary.get("provider_runtime_enabled") is False
        and governance_review.get("runtime_activation_allowed") is False
        and governance_review.get("provider_runtime_enabled") is False
    )

    handoff = {
        "ready_for_domain_profile_handoff": core_ready,
        "ready_for_spatial_evidence_profile_followup": core_ready
        and governance_review.get("spatial_evidence_profile_supported") is True,
        "ready_for_vision_ocr_profile_followup": core_ready
        and governance_review.get("vision_ocr_compatibility_preserved") is True,
        "ready_for_provider_runtime_governance_shared_use": core_ready,
        "ready_for_future_provider_manager_runtime_skeleton": core_ready and runtime_frozen,
    }

    for key, ok in handoff.items():
        if ok:
            passed.append(f"handoff.{key}=true")
        else:
            failed.append(f"handoff.{key}=false")

    return handoff, passed, failed


def review_provider_runtime_governance_post_dryrun_v1(
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

    baseline = {
        "shared_dataclass_count": EXPECTED_SHARED_DATACLASS_COUNT,
        "validator_rules": EXPECTED_VALIDATOR_RULES,
        "positive_case_count": summary.get("positive_case_count"),
        "invalid_case_count": summary.get("invalid_case_count"),
        "trace_count": len(traces),
        "supported_domains": list(SUPPORTED_DOMAINS),
    }

    step1_review, p, f = review_step1_static_baseline(summary)
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

    superseded_review, p, f = review_superseded_path()
    all_passed.extend(p)
    all_failed.extend(f)

    step4_ok = (
        step4_review.get("verifier_final_decision_ok") is True
        and step4_review.get("blocker_count_zero") is True
    )

    handoff_readiness, p, f = review_handoff_readiness(
        step4_ok=step4_ok,
        governance_review=governance_review,
        superseded_review=superseded_review,
        summary=summary,
        verification=verification,
    )
    all_passed.extend(p)
    all_failed.extend(f)

    governance_ok = (
        governance_review.get("shared_provider_runtime_governance_ready") is True
        and governance_review.get("vision_ocr_compatibility_preserved") is True
        and governance_review.get("spatial_evidence_profile_supported") is True
        and governance_review.get("no_domain_specific_manager_duplication") is True
        and governance_review.get("runtime_activation_allowed") is False
        and governance_review.get("provider_runtime_enabled") is False
        and governance_review.get("candidate_only_enforced") is True
        and governance_review.get("domain_profile_required") is True
        and governance_review.get("fallback_preserves_source_chain") is True
        and governance_review.get("no_direct_action") is True
        and governance_review.get("no_direct_speech") is True
        and governance_review.get("no_direct_fact_write") is True
    )

    blocker_count = len(all_failed)
    go_ok = (
        verification.get("final_decision") == FINAL_DECISION_DRYRUN_VERIFIER_GO
        and len(traces) == EXPECTED_TRACE_COUNT
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_CASES
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_CASES
        and summary.get("unexpected_pass_count") == 0
        and summary.get("unexpected_fail_count") == 0
        and summary.get("vision_ocr_compatibility_preserved") is True
        and summary.get("spatial_evidence_profile_supported") is True
        and summary.get("no_domain_specific_manager_duplication") is True
        and summary.get("runtime_activation_allowed") is False
        and summary.get("provider_runtime_enabled") is False
        and all(step1_review.values())
        and all(step2_review.values())
        and all(step3_review.values())
        and all(step4_review.values())
        and governance_ok
        and all(superseded_review.values())
        and handoff_readiness.get("ready_for_provider_runtime_governance_shared_use") is True
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 5 Shared Provider Runtime Governance Post-DryRun Review",
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
        "superseded_review": superseded_review,
        "handoff_readiness": handoff_readiness,
        "architecture_frozen_conclusion": {
            "governance_principle_zh": GOVERNANCE_PRINCIPLE_ZH,
            "layer_l1": "Provider Runtime Governance Skeleton (shared midplatform)",
            "layer_l2": "Spatial Evidence / Vision-OCR domain profiles",
            "runtime_activation_allowed": False,
            "provider_runtime_enabled": False,
            "runtime_enabled_provider_refs": [],
            "primary_path": "capabilities/midplatform/provider_runtime_governance",
            "superseded_reference_path": (
                "capabilities/field_understanding/spatial_evidence_provider_manager"
            ),
            "do_not_continue": "spatial_evidence_provider_manager Step 2+",
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": (
            FINAL_DECISION_POST_DRYRUN_REVIEW_GO if go_ok else FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED
        ),
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
    try:
        result = review_provider_runtime_governance_post_dryrun_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "baseline": result["baseline"],
                "governance_review": result["governance_review"],
                "superseded_review": result["superseded_review"],
                "handoff_readiness": result["handoff_readiness"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_POST_DRYRUN_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
