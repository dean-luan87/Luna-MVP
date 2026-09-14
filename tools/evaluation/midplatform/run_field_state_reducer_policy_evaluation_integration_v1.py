from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.behavior_policy.policy_evaluation import (  # noqa: E402
    EvaluationInput,
    evaluate_single_policy_v1,
    result_to_dict,
)


def _iso_now(delta_hours: int = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=delta_hours)).isoformat()


def _base_input(case_id: str, policy_id: str, state_type: str) -> Dict[str, Any]:
    now = _iso_now()
    return {
        "evaluation_id": f"eval_{case_id}",
        "reducer_run_id": f"run_{case_id}",
        "field_id": "field_001",
        "state_type": state_type,
        "policy_id": policy_id,
        "admitted_events": (
            {
                "event_id": f"evt_{case_id}_1",
                "source_id": "source_a",
                "event_time": now,
                "contradictory": False,
            },
            {
                "event_id": f"evt_{case_id}_2",
                "source_id": "source_b",
                "event_time": now,
                "contradictory": False,
            },
        ),
        "existing_state_snapshot": {"status": "candidate"},
        "temporal_snapshot": {
            "status": "active",
            "refresh_evidence_available": True,
            "new_event_available": True,
        },
        "confidence_policy_snapshot": {"measured_confidence": 0.9},
        "conflict_snapshot": {
            "conflict_type": "direct_vs_inferred",
            "unresolved": False,
            "tags": [],
            "negative_signal_present": True,
            "revocation_present": True,
        },
        "owner_correction_snapshot": {"candidate_only": True},
        "overlay_snapshot": {"separate_from_substrate": True},
        "provenance_snapshot": {
            "source_id": "source_a",
            "event_id": f"evt_{case_id}_1",
            "event_time": now,
            "admission_id": "admission_1",
            "available_keys": ["source_id", "event_id", "event_time", "admission_id"],
            "source_ids": ["source_a", "source_b"],
        },
        "governance_snapshot": {
            "owner_correction_review": True,
            "fact_admission_dependency": True,
            "permission_admission_dependency": True,
            "human_review_dependency": True,
            "protocol_version_dependency": True,
            "provenance_dependency": True,
            "change_control_dependency": True,
            "runtime_boundary_dependency": True,
        },
        "policy_registry_version": "v1",
        "eligibility_matrix_version": "v1",
        "evaluation_contract_version": "v1",
        "evaluation_requested_at": now,
        "runtime_state_dependency_requested": False,
        "provider_recall_requested": False,
        "external_lookup_requested": False,
        "model_call_requested": False,
        "state_write_requested": False,
        "action_trigger_requested": False,
    }


def run_field_state_reducer_policy_evaluation_integration_v1() -> Dict[str, Any]:
    cases: List[Tuple[str, str, Dict[str, Any]]] = []

    eligible = _base_input("eligible", "latest_valid_event", "path_state")
    cases.append(("eligible_case", "eligible_candidate", eligible))

    ineligible = _base_input(
        "ineligible", "highest_confidence_valid_event", "presence_state"
    )
    ineligible["confidence_policy_snapshot"] = {"measured_confidence": 0.1}
    cases.append(("ineligible_case", "ineligible", ineligible))

    insufficient = _base_input("insufficient", "multi_event_consensus", "service_state")
    insufficient["admitted_events"] = tuple(insufficient["admitted_events"][:1])
    insufficient["provenance_snapshot"]["source_ids"] = ["source_a"]
    cases.append(("insufficient_evidence_case", "insufficient_evidence", insufficient))

    expired = _base_input("expired", "expiration_degrade", "presence_state")
    expired["temporal_snapshot"]["status"] = "expired"
    cases.append(("expired_case", "temporally_invalid", expired))

    suspended = _base_input("suspended", "expiration_degrade", "service_state")
    suspended["temporal_snapshot"]["status"] = "suspended"
    suspended["temporal_snapshot"]["refresh_evidence_available"] = False
    cases.append(("suspended_without_refresh_case", "temporally_invalid", suspended))

    revoked = _base_input("revoked", "revocation_override", "accessibility_state")
    revoked["temporal_snapshot"]["status"] = "revoked"
    cases.append(("revoked_case", "temporally_invalid", revoked))

    unresolved = _base_input("unresolved", "conflict_preservation", "conflict_state")
    unresolved["conflict_snapshot"]["unresolved"] = True
    unresolved["conflict_snapshot"]["tags"] = ["unresolved"]
    cases.append(("unresolved_conflict_case", "unresolved_conflict", unresolved))

    owner_review = _base_input(
        "owner_review", "explicit_owner_override_candidate", "facility_state"
    )
    owner_review["governance_snapshot"]["owner_correction_review"] = False
    cases.append(
        ("owner_review_required_case", "governance_review_required", owner_review)
    )

    overlay = _base_input(
        "overlay", "temporary_overlay_separation", "temporary_overlay_state"
    )
    cases.append(("overlay_separation_case", "eligible_candidate", overlay))

    missing_version = _base_input("missing_version", "no_state_change", "path_state")
    missing_version["evaluation_contract_version"] = ""
    cases.append(("missing_version_snapshot_case", "invalid_input", missing_version))

    results: List[Dict[str, Any]] = []
    failed_cases: List[str] = []

    for case_id, expected_status, payload in cases:
        result = evaluate_single_policy_v1(EvaluationInput(**payload))
        row = result_to_dict(result)
        row["case_id"] = case_id
        row["expected_status"] = expected_status
        row["status_matched"] = row["evaluation_status"] == expected_status
        results.append(row)
        if not row["status_matched"]:
            failed_cases.append(case_id)

    boundary_ok = all(
        r["policy_selection_executed"] is False
        and r["policy_execution_executed"] is False
        and r["state_mutation_executed"] is False
        and r["fact_promotion_executed"] is False
        and r["action_trigger_executed"] is False
        and r["runtime_execution"] is False
        for r in results
    )

    report = {
        "module": "Field State Reducer Policy Evaluation",
        "execution_mode": "Function Module Engineering Build",
        "total_cases": len(cases),
        "passed_cases": len(cases) - len(failed_cases),
        "failed_cases": failed_cases,
        "trace_present_all": all(bool(r.get("evaluation_trace_ref")) for r in results),
        "replay_present_all": all(bool(r.get("replay_key")) for r in results),
        "boundary_preserved": boundary_ok,
        "module_status": {
            "evaluation_types_implemented": True,
            "condition_evaluator_implemented": True,
            "evidence_evaluator_implemented": True,
            "temporal_evaluator_implemented": True,
            "confidence_evaluator_implemented": True,
            "conflict_evaluator_implemented": True,
            "governance_evaluator_implemented": True,
            "evaluation_orchestrator_implemented": True,
            "trace_replay_implemented": True,
            "integration_runner_created": True,
            "policy_selection_implemented": False,
            "state_mutation_implemented": False,
            "runtime_implemented": False,
        },
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    out = run_field_state_reducer_policy_evaluation_integration_v1()
    raise SystemExit(0 if not out.get("failed_cases") else 1)
