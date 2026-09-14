"""User-terminal fail-closed Verifier for the replay evaluation integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from capabilities.evaluation.a_route_cognitive_whitebox_foundation.types_v1 import (
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.archive_v1 import (
    read_evaluation_run_record_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import (
    GOVERNANCE_ASSERTION_IDS,
    validate_plane_g_compliance_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.types_v1 import (
    validate_evaluation_run_record_v1,
    validate_plane_b_result_v1,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


CANONICAL_COGNITION_OWNER = "Cognitive State Formation Governance"
FORBIDDEN_EXECUTION_OUTPUT_ROOTS = ("_eval_out", "_tmp_eval_out")


def verify_summary_v1(summary: Dict[str, Any], *, repository_root: Path | None = None) -> Dict[str, Any]:
    checks: Dict[str, bool] = {
        "controlled_replay_mode": summary.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME,
        "registered_linkage_valid": summary.get("run_boundary_valid") is True
        and not summary.get("run_boundary_errors"),
        "replay_fixture_labeled_truthfully": summary.get("replay_origin_class") == "CONTROLLED_RECORDED_FIXTURE",
        "gateway_admitted": summary.get("observation_gateway_admitted") is True
        and bool(summary.get("observation_gateway_admission_ref")),
        "canonical_a_route_refs_present": bool(summary.get("a_route_ingress_ref"))
        and bool(summary.get("a_route_execution_ref")),
        "canonical_cognition_executed": summary.get("cognition_execution") is True
        and summary.get("runtime_executed") is True,
        "canonical_transition_proof": summary.get("cognitive_transition_count", 0) >= 1
        and len(summary.get("cognitive_transition_refs") or []) == summary.get("cognitive_transition_count"),
        "canonical_cognition_owner": summary.get("canonical_cognition_owner_ref") == CANONICAL_COGNITION_OWNER,
        "whitebox_refs_present": bool(summary.get("whitebox_trace_ref"))
        and bool(summary.get("whitebox_profile_ref")),
        "plane_a_separate": summary.get("plane_a_result", {}).get("status") == "EXECUTION_OBSERVED",
        "plane_b_not_evaluated": summary.get("plane_b_result", {}).get("status") == "NOT_EVALUATED",
        "plane_g_compliant": summary.get("plane_g_result", {}).get("compliance_status") == "COMPLIANT",
        "plane_g_assertions_complete": tuple(
            summary.get("governance_assertion_summary", {}).keys()
        ) == GOVERNANCE_ASSERTION_IDS,
        "negative_governance_check_passed": summary.get("negative_governance_check", {}).get("passed") is True,
        "archive_created": summary.get("archive_record_created") is True,
        "archive_declared_immutable": summary.get("archive_record_immutable") is True,
        "archive_not_execution_output": not any(
            root in str(summary.get("archive_location", ""))
            for root in FORBIDDEN_EXECUTION_OUTPUT_ROOTS
        ),
        "no_forbidden_runtime_capability": all(
            summary.get(key) is False
            for key in (
                "model_invocation",
                "provider_invocation",
                "live_observation_execution",
                "action_execution",
                "field_mutation",
                "world_truth_declared",
                "memory_promotion",
                "knowledge_promotion",
                "experience_promotion",
            )
        ),
        "no_validation_or_boundary_errors": not summary.get("validation_errors")
        and not summary.get("boundary_errors"),
        "unavailable_metrics_explicit": bool(summary.get("unavailable_metrics")),
    }
    issues: List[str] = [name for name, passed in checks.items() if not passed]
    archive_location = str(summary.get("archive_location", ""))
    if repository_root is not None and archive_location:
        archive_path = repository_root / archive_location
        checks["archive_readable"] = archive_path.is_file()
        if archive_path.is_file():
            try:
                record = read_evaluation_run_record_v1(archive_path)
                checks["archive_record_contract_valid"] = not validate_evaluation_run_record_v1(record)
                checks["archive_run_identity_matches"] = record.evaluation_run.evaluation_run_id == summary.get("evaluation_run_id")
                checks["archive_refs_match_summary"] = (
                    record.evaluation_run.trace_ref == summary.get("whitebox_trace_ref")
                    and record.evaluation_run.execution_profile_ref == summary.get("whitebox_profile_ref")
                    and record.evaluation_run.a_route_execution_ref == summary.get("a_route_execution_ref")
                )
                metadata = record.bounded_metadata
                whitebox_trace = metadata.get("whitebox_trace") or {}
                whitebox_profile = metadata.get("whitebox_profile") or {}
                checks["archive_whitebox_v1_payload_present"] = bool(
                    whitebox_trace.get("trace_id")
                    and whitebox_trace.get("nodes")
                    and whitebox_profile.get("execution_profile_id")
                )
                checks["archive_whitebox_trace_profile_linked"] = (
                    whitebox_trace.get("trace_id") == record.evaluation_run.trace_ref
                    and whitebox_profile.get("cognitive_trace_ref") == whitebox_trace.get("trace_id")
                    and tuple(whitebox_trace.get("transition_refs") or ())
                    == tuple(summary.get("cognitive_transition_refs") or ())
                )
                plane_g = metadata.get("plane_g_result") or {}
                checks["archive_plane_g_valid"] = not validate_plane_g_compliance_v1(
                    _plane_g_from_dict(plane_g)
                ) if plane_g else False
                plane_b = metadata.get("plane_b_result") or {}
                checks["archive_plane_b_valid"] = not validate_plane_b_result_v1(
                    _plane_b_from_dict(plane_b)
                ) if plane_b else False
            except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                checks["archive_record_contract_valid"] = False
                issues.append(f"archive_read_failed:{type(exc).__name__}")
    for name, passed in checks.items():
        if not passed and name not in issues:
            issues.append(name)
    return {
        "phase": "Phase-P1-Luna-Level1-Replay-Evaluation-Whitebox-Archive-And-Governance-Integration-v1-001",
        "checks": checks,
        "issues": list(dict.fromkeys(issues)),
        "all_checks_passed": not issues,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def _plane_b_from_dict(raw: Dict[str, Any]):
    from .types_v1 import PlaneBResultV1

    return PlaneBResultV1(
        result_ref=str(raw.get("result_ref", "")),
        status=str(raw.get("status", "")),
        reason=str(raw.get("reason", "")),
        evaluation_only=bool(raw.get("evaluation_only", True)),
    )


def _plane_g_from_dict(raw: Dict[str, Any]):
    from .governance_v1 import (
        GovernanceAssertionResultV1,
        PlaneGComplianceResultV1,
    )

    assertions = tuple(
        GovernanceAssertionResultV1(
            assertion_id=str(item.get("assertion_id", "")),
            status=str(item.get("status", "")),
            passed=item.get("passed"),
            policy_family=str(item.get("policy_family", "")),
            contract_ref=item.get("contract_ref"),
            contract_ref_availability=str(item.get("contract_ref_availability", "")),
            actor_ref=str(item.get("actor_ref", "")),
            target_refs=tuple(item.get("target_refs") or ()),
            evidence_refs=tuple(item.get("evidence_refs") or ()),
            violation_refs=tuple(item.get("violation_refs") or ()),
            notes=str(item.get("notes", "")),
        )
        for item in raw.get("assertion_results") or ()
    )
    return PlaneGComplianceResultV1(
        result_ref=str(raw.get("result_ref", "")),
        plane_id=str(raw.get("plane_id", "")),
        compliance_status=str(raw.get("compliance_status", "")),
        assertion_results=assertions,
        violation_refs=tuple(raw.get("violation_refs") or ()),
        violated_contract_refs=tuple(raw.get("violated_contract_refs") or ()),
        severity=str(raw.get("severity", "")),
        actor_refs=tuple(raw.get("actor_refs") or ()),
        target_refs=tuple(raw.get("target_refs") or ()),
        evidence_refs=tuple(raw.get("evidence_refs") or ()),
        unavailable_assertions=tuple(raw.get("unavailable_assertions") or ()),
        provenance_refs=tuple(raw.get("provenance_refs") or ()),
        contract_ref_availability=str(raw.get("contract_ref_availability", "")),
        evaluation_only=bool(raw.get("evaluation_only", True)),
        governance_mutation=bool(raw.get("governance_mutation", False)),
    )


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_controlled_replay_integration_v1 <runner_summary.json>"
        )
    summary_path = Path(sys.argv[1])
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    result = verify_summary_v1(summary, repository_root=Path.cwd())
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
