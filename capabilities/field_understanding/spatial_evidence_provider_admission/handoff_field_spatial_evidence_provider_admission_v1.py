# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission — planning handoff v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    FORBIDDEN_PROVIDER_ADMISSION_POLICIES,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    ADMISSION_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    NON_EXECUTION_FLAGS,
    PHASE_ID as SOURCE_PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_spatial_evidence_provider_admission_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "field_spatial_evidence_provider_admission_post_dryrun_review_v1.json"
SUMMARY_FILENAME = "field_spatial_evidence_provider_admission_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_spatial_evidence_provider_admission_dryrun_verification_v1.json"
HANDOFF_FILENAME = "field_spatial_evidence_provider_admission_handoff_v1.json"

PHASE_ID = "Phase-Field-Spatial-Evidence-Provider-Admission-Handoff-v1-001"
SOURCE_FINAL_DECISION = "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POST_DRYRUN_REVIEW_GO"
VERIFIER_FINAL_DECISION_GO = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_VERIFIER_GO"
)
FINAL_DECISION_HANDOFF_READY = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_HANDOFF_READY_FOR_PROVIDER_MANAGER_SKELETON_PLANNING"
)
FINAL_DECISION_HANDOFF_BLOCKED = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_HANDOFF_BLOCKED"
)

NEXT_PHASE_PROVIDER_MANAGER_SKELETON = (
    "Phase-Field-Spatial-Evidence-Provider-Manager-Skeleton-Planning-v1-001"
)

EXPECTED_BASELINE = {
    "provider_policy_count": 7,
    "capability_profile_count": 7,
    "health_gate_count": 7,
    "fallback_policy_count": 7,
    "runtime_admission_candidate_count": 7,
    "validator_rules": 20,
    "positive_case_count": 7,
    "invalid_case_count": 6,
    "trace_count": 13,
}

def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def _blocked_paths_snapshot() -> Dict[str, bool]:
    forbidden = set(FORBIDDEN_PROVIDER_ADMISSION_POLICIES)
    return {
        "provider_direct_action": "provider_direct_action" in forbidden,
        "provider_direct_speech": "provider_direct_speech" in forbidden,
        "provider_direct_fact_write": "provider_direct_fact_write" in forbidden,
        "provider_direct_field_rewrite": "provider_direct_fact_write" in forbidden
        and "provider_bypass_field_synthesis" in forbidden,
        "gpl_commercial_runtime": "gpl_provider_commercial_runtime" in forbidden,
        "observation_runtime_admission": "observation_provider_runtime_admission" in forbidden,
        "field_synthesis_bypass": "provider_bypass_field_synthesis" in forbidden,
        "runtime_without_health_gate": "provider_runtime_without_health_gate" in forbidden,
        "runtime_without_fallback": "provider_runtime_without_fallback" in forbidden,
    }


def _frozen_governance_from_review(review: Dict[str, Any]) -> Dict[str, bool]:
    governance = review.get("governance_review") or {}
    step1 = review.get("step_1_static_baseline_review") or {}
    arch = review.get("architecture_frozen_conclusion") or {}

    return {
        "translation_does_not_equal_enablement": governance.get(
            "translation_does_not_equal_enablement"
        )
        is True
        and ADMISSION_PRINCIPLE_ZH == "能翻译，不等于能启用。",
        "adapter_contract_passed_does_not_imply_runtime_admission": step1.get(
            "adapter_contract_does_not_imply_runtime_enabled"
        )
        is True
        and arch.get("adapter_contract_passed_does_not_imply_runtime_enabled") is True,
        "runtime_admission_candidates_empty": governance.get(
            "runtime_admission_candidates_empty"
        )
        is True,
        "commercial_runtime_candidates_empty": governance.get(
            "commercial_runtime_candidates_empty"
        )
        is True,
        "field_synthesis_v1_only": governance.get("field_synthesis_v1_only") is True
        and arch.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_required": step1.get("health_gate_required") is True
        and governance.get("health_gate_enforced") is True,
        "fallback_gate_required": step1.get("fallback_required") is True
        and governance.get("fallback_gate_enforced") is True,
        "capability_coverage_required": governance.get("capability_coverage_enforced") is True,
        "provider_replaceability_required": step1.get("provider_replaceability_required")
        is True,
        "candidate_only_chain_preserved": governance.get("candidate_only_chain_preserved")
        is True,
    }


def _handoff_readiness_from_review(review: Dict[str, Any]) -> Dict[str, bool]:
    prior = review.get("handoff_readiness") or {}
    return {
        "ready_for_provider_manager_skeleton_planning": prior.get(
            "ready_for_provider_manager_skeleton_later"
        )
        is True,
        "ready_for_runtime_admission_skeleton_design": prior.get(
            "ready_for_runtime_admission_skeleton_planning"
        )
        is True,
        "ready_for_provider_enable_disable_contract": prior.get(
            "ready_for_provider_admission_handoff"
        )
        is True,
        "ready_for_health_fallback_runtime_contract": prior.get(
            "ready_for_health_fallback_runtime_later"
        )
        is True,
        "ready_for_license_gate_runtime_contract": prior.get(
            "ready_for_license_gate_runtime_later"
        )
        is True,
    }


def build_provider_admission_handoff_v1(
    *,
    review: Dict[str, Any],
    summary: Optional[Dict[str, Any]] = None,
    verification: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    baseline = dict(review.get("baseline") or {})
    boundary = review.get("boundary_review") or {}

    if review.get("final_decision") != SOURCE_FINAL_DECISION:
        failed_checks.append(
            f"review.final_decision: expected={SOURCE_FINAL_DECISION!r}, "
            f"actual={review.get('final_decision')!r}"
        )
    if review.get("blocker_count", 1) != 0:
        failed_checks.append(f"review.blocker_count={review.get('blocker_count')!r}")

    for key, expected in EXPECTED_BASELINE.items():
        actual = baseline.get(key)
        if actual != expected:
            failed_checks.append(f"baseline.{key}: expected={expected!r}, actual={actual!r}")

    if summary:
        if summary.get("final_decision") != (
            "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_TRACE_READY_FOR_VERIFIER"
        ):
            failed_checks.append("summary.final_decision_not_trace_ready")
        if summary.get("no_runtime_admission") is not True:
            failed_checks.append("summary.no_runtime_admission_not_true")

    if verification:
        if verification.get("final_decision") != VERIFIER_FINAL_DECISION_GO:
            failed_checks.append("verification.final_decision_not_go")
        if verification.get("blocker_count", 1) != 0:
            failed_checks.append("verification.blocker_count_not_zero")

    frozen_governance = _frozen_governance_from_review(review)
    for key, ok in frozen_governance.items():
        if not ok:
            failed_checks.append(f"frozen_governance.{key}=false")

    blocked_paths = _blocked_paths_snapshot()
    for key, ok in blocked_paths.items():
        if not ok:
            failed_checks.append(f"blocked_paths.{key}=false")

    handoff_scope = {
        "provider_admission_baseline_frozen": review.get("final_decision") == SOURCE_FINAL_DECISION
        and not failed_checks,
        "runtime_admission_not_enabled": boundary.get("no_runtime_admission_enabled") is True
        and NON_EXECUTION_FLAGS.get("no_runtime_admission") is True,
        "commercial_runtime_not_selected": boundary.get("no_commercial_runtime_selected") is True,
        "provider_manager_not_written": boundary.get("no_provider_manager_written") is True
        and NON_EXECUTION_FLAGS.get("no_provider_manager_runtime") is True,
    }
    for key, ok in handoff_scope.items():
        if not ok:
            failed_checks.append(f"handoff_scope.{key}=false")

    handoff_readiness = _handoff_readiness_from_review(review)
    for key, ok in handoff_readiness.items():
        if not ok:
            failed_checks.append(f"handoff_readiness.{key}=false")

    go_ok = len(failed_checks) == 0 and all(handoff_scope.values()) and all(
        handoff_readiness.values()
    )

    return {
        "phase_id": PHASE_ID,
        "source_phase_id": SOURCE_PHASE_ID,
        "source_final_decision": SOURCE_FINAL_DECISION,
        "admission_principle_zh": ADMISSION_PRINCIPLE_ZH,
        "handoff_note": (
            "Provider Admission Planning baseline is frozen and may hand off to "
            "Provider Manager Skeleton Planning. Real provider runtime must not be enabled."
        ),
        "handoff_note_zh": (
            "Provider Admission Planning 基线已冻结，可交接给 Provider Manager Skeleton Planning；"
            "但当前仍不得启用真实 provider runtime。"
        ),
        "handoff_scope": handoff_scope,
        "frozen_baseline": {
            "provider_policy_count": baseline.get("provider_policy_count"),
            "capability_profile_count": baseline.get("capability_profile_count"),
            "health_gate_count": baseline.get("health_gate_count"),
            "fallback_policy_count": baseline.get("fallback_policy_count"),
            "runtime_admission_candidate_count": baseline.get("runtime_admission_candidate_count"),
            "validator_rules": baseline.get("validator_rules"),
            "positive_case_count": baseline.get("positive_case_count"),
            "invalid_case_count": baseline.get("invalid_case_count"),
            "trace_count": baseline.get("trace_count"),
        },
        "frozen_governance": frozen_governance,
        "blocked_paths": blocked_paths,
        "next_phase_recommendation": {
            "recommended_next_phase": NEXT_PHASE_PROVIDER_MANAGER_SKELETON,
            "recommended_next_step": "Step 1 Types / Registry / Validators",
            "do_not_start_real_runtime": True,
            "do_not_connect_real_backend": True,
            "do_not_connect_camera_or_ros": True,
        },
        "handoff_readiness": handoff_readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "input_review_final_decision": review.get("final_decision"),
        "input_verifier_final_decision": (
            verification or {}
        ).get("final_decision") or baseline.get("verifier_final_decision"),
        "blocker_count": len(failed_checks),
        "failed_checks": failed_checks,
        "final_decision": FINAL_DECISION_HANDOFF_READY if go_ok else FINAL_DECISION_HANDOFF_BLOCKED,
    }


def handoff_field_spatial_evidence_provider_admission_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    review_path = root / REVIEW_FILENAME
    summary_path = root / SUMMARY_FILENAME
    verification_path = root / VERIFICATION_FILENAME

    review = load_json_file(review_path)
    summary = load_json_file(summary_path) if summary_path.is_file() else None
    verification = load_json_file(verification_path) if verification_path.is_file() else None

    result = build_provider_admission_handoff_v1(
        review=review,
        summary=summary,
        verification=verification,
    )

    result["input_artifacts"] = {
        "review": str(review_path),
        "summary": str(summary_path) if summary_path.is_file() else None,
        "verification": str(verification_path) if verification_path.is_file() else None,
    }

    if write_file:
        root.mkdir(parents=True, exist_ok=True)
        out_path = root / HANDOFF_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result["output_handoff_file"] = str(out_path)

    return result


def main() -> int:
    result = handoff_field_spatial_evidence_provider_admission_v1()
    print(
        json.dumps(
            {
                "output_handoff_file": result.get("output_handoff_file"),
                "source_phase_id": result["source_phase_id"],
                "handoff_scope": result["handoff_scope"],
                "next_phase_recommendation": result["next_phase_recommendation"],
                "handoff_readiness": result["handoff_readiness"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_HANDOFF_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
