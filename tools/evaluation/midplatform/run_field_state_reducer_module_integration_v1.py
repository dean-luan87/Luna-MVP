from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.module import (  # noqa: E402
    FieldStateReducerModuleRequestV1,
    FieldStateReducerModuleV1,
    module_result_to_dict,
)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _event(case_id: str, idx: int, stable: bool = True) -> Dict[str, Any]:
    eid = f"evt_{case_id}_{idx}" if stable else ""
    return {
        "event_id": eid,
        "source_id": "source_a" if idx % 2 == 0 else "source_b",
        "event_time": _iso_now(),
        "admission_id": f"admission_{case_id}_{idx}",
    }


def _base_request(case_id: str, state_type: str = "presence_state") -> Dict[str, Any]:
    return {
        "reducer_request_id": f"request_{case_id}",
        "reducer_run_id": f"run_{case_id}",
        "field_id": "field_001",
        "requested_state_type": state_type,
        "admitted_events": (_event(case_id, 1), _event(case_id, 2)),
        "existing_state_snapshot": {
            "state_id": f"state_{case_id}",
            "status": "candidate",
            "value": {"source": "existing"},
        },
        "temporal_snapshot": {
            "status": "active",
            "refresh_evidence_available": True,
            "new_event_available": True,
            "sufficient_evidence": True,
        },
        "policy_registry_snapshot": {"version": "v1"},
        "evaluation_contract_snapshot": {"version": "v1"},
        "selection_contract_snapshot": {"version": "v1"},
        "reduction_contract_snapshot": {"version": "v1"},
        "conflict_snapshot": {
            "conflict_type": "none",
            "unresolved": False,
            "preserve_conflict": False,
            "provisional_candidate_allowed": True,
            "conflicting_event_refs": [],
            "resolution_available": True,
        },
        "overlay_snapshot": {
            "overlay_refs": [],
            "overlay_active": False,
            "overlay_expired": False,
            "substrate_mutation_requested": False,
        },
        "owner_correction_snapshot": {"owner_correction_refs": []},
        "provenance_snapshot": {
            "source_id": "source_a",
            "event_id": f"evt_{case_id}_1",
            "event_time": _iso_now(),
            "admission_id": f"admission_{case_id}_1",
            "available_keys": ["source_id", "event_id", "event_time", "admission_id"],
            "source_ids": ["source_a", "source_b"],
            "confidence_policy_snapshot": {"measured_confidence": 0.9},
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
            "evaluation_requested_at": _iso_now(),
        },
        "version_snapshots": {
            "policy_registry_version": "v1",
            "eligibility_matrix_version": "v1",
            "precedence_matrix_version": "v1",
            "composition_contract_version": "v1",
            "replay_contract_version": "v1",
            "evaluation_contract_version": "v1",
            "reduction_contract_version": "v1",
        },
        "direct_mutation_requested": False,
        "runtime_request": False,
        "provider_request": False,
        "model_request": False,
        "external_lookup_request": False,
    }


def run_field_state_reducer_module_integration_v1() -> Dict[str, Any]:
    cases: List[Tuple[str, str, Dict[str, Any], bool]] = []

    req = _base_request("create")
    req["existing_state_snapshot"] = {}
    cases.append(("create_new_state_candidate", "completed_candidate", req, True))

    req = _base_request("update")
    req["existing_state_snapshot"]["status"] = "active"
    cases.append(("update_existing_candidate", "completed_candidate", req, True))

    req = _base_request("maintain")
    req["existing_state_snapshot"]["status"] = "active"
    cases.append(("maintain_state", "completed_candidate", req, True))

    req = _base_request("no_change")
    req["admitted_events"] = tuple()
    cases.append(("no_state_change", "no_state_change", req, True))

    req = _base_request("insufficient")
    req["admitted_events"] = (_event("insufficient", 1),)
    req["provenance_snapshot"]["source_ids"] = ["source_a"]
    cases.append(("insufficient_evidence", "insufficient_evidence", req, True))

    req = _base_request("expired")
    req["temporal_snapshot"]["status"] = "expired"
    cases.append(("expired_support", "temporally_invalid", req, True))

    req = _base_request("suspended")
    req["temporal_snapshot"]["status"] = "suspended"
    req["temporal_snapshot"]["refresh_evidence_available"] = False
    cases.append(("suspended_without_refresh", "temporally_invalid", req, True))

    req = _base_request("revoked")
    req["temporal_snapshot"]["status"] = "revoked"
    cases.append(("revoked_support", "temporally_invalid", req, True))

    req = _base_request("superseded")
    req["temporal_snapshot"]["status"] = "superseded"
    cases.append(("superseded_state", "temporally_invalid", req, True))

    req = _base_request("unresolved")
    req["conflict_snapshot"]["unresolved"] = True
    req["conflict_snapshot"]["conflicting_event_refs"] = ["evt_unresolved_1"]
    req["conflict_snapshot"]["resolution_available"] = False
    cases.append(("unresolved_conflict", "unresolved", req, True))

    req = _base_request("overlay")
    req["requested_state_type"] = "temporary_overlay_state"
    req["overlay_snapshot"]["overlay_active"] = True
    req["overlay_snapshot"]["overlay_refs"] = ["overlay_ref_1"]
    cases.append(("temporary_overlay", "completed_candidate", req, True))

    req = _base_request("overlay_expired")
    req["requested_state_type"] = "temporary_overlay_state"
    req["overlay_snapshot"]["overlay_expired"] = True
    req["overlay_snapshot"]["overlay_refs"] = ["overlay_ref_2"]
    cases.append(("overlay_expired", "completed_candidate", req, True))

    req = _base_request("owner_review")
    req["provenance_snapshot"]["governance_snapshot"]["owner_correction_review"] = False
    req["owner_correction_snapshot"]["owner_correction_refs"] = ["owner_ref_1"]
    cases.append(
        ("owner_correction_review_required", "governance_review_required", req, True)
    )

    req = _base_request("invalid_input")
    req["admitted_events"] = (_event("invalid_input", 1, stable=False),)
    cases.append(("invalid_input", "rejected_input", req, False))

    req = _base_request("invalid_transition")
    req["existing_state_snapshot"]["status"] = "revoked"
    req["temporal_snapshot"]["status"] = "active"
    req["temporal_snapshot"]["new_event_available"] = False
    req["conflict_snapshot"]["preserve_conflict"] = False
    cases.append(("invalid_transition", "internal_error", req, True))

    req = _base_request("deterministic_replay")
    cases.append(("deterministic_replay", "completed_candidate", req, True))

    results: List[Dict[str, Any]] = []
    failed_cases: List[str] = []
    deterministic_pair: List[Dict[str, Any]] = []

    for case_id, expected_status, request_payload, expect_candidate in cases:
        request = FieldStateReducerModuleRequestV1(**request_payload)
        result = FieldStateReducerModuleV1.reduce(request)
        row = module_result_to_dict(result)
        row["case_id"] = case_id
        row["expected_module_status"] = expected_status
        row["status_matched"] = row["module_status"] == expected_status
        candidate_exists = row.get("field_state_candidate") is not None
        row["candidate_expectation_matched"] = candidate_exists == expect_candidate
        row["matched"] = row["status_matched"] and row["candidate_expectation_matched"]
        results.append(row)
        if not row["matched"]:
            failed_cases.append(case_id)
        if case_id == "deterministic_replay":
            deterministic_pair.append(row)

    # replay determinism check with same input.
    replay_deterministic = True
    if deterministic_pair:
        payload = _base_request("deterministic_replay")
        request_a = FieldStateReducerModuleRequestV1(**payload)
        request_b = FieldStateReducerModuleRequestV1(**payload)
        out_a = module_result_to_dict(FieldStateReducerModuleV1.reduce(request_a))
        out_b = module_result_to_dict(FieldStateReducerModuleV1.reduce(request_b))
        replay_deterministic = out_a.get("replay_key") == out_b.get("replay_key")
        if not replay_deterministic:
            failed_cases.append("deterministic_replay")

    boundary_ok = all(
        r["candidate_only"] is True
        and r["fact_admitted"] is False
        and r["state_store_write_executed"] is False
        and r["action_trigger_executed"] is False
        and r["runtime_execution"] is False
        and ((r.get("field_state_candidate") or {}).get("persisted", False) is False)
        for r in results
    )

    report = {
        "module": "Luna Field State Reducer",
        "internal_segment": "Output Surface And Module Assembly",
        "execution_mode": "Functional Module Continuous Assembly",
        "total_cases": len(cases),
        "passed_cases": len(cases) - len(failed_cases),
        "failed_cases": sorted(set(failed_cases)),
        "deterministic_replay": replay_deterministic,
        "trace_present_all": all(
            bool(r.get("trace_ref")) or r.get("module_status") == "rejected_input"
            for r in results
        ),
        "replay_present_all": all(
            bool(r.get("replay_key")) or r.get("module_status") == "rejected_input"
            for r in results
        ),
        "boundary_preserved": boundary_ok,
        "module_status": {
            "module_input_adapter_implemented": True,
            "module_facade_implemented": True,
            "module_output_surface_implemented": True,
            "read_projection_candidate_implemented": True,
            "module_status_registry_implemented": True,
            "module_diagnostics_implemented": True,
            "module_api_contract_implemented": True,
            "full_module_integration_runner_created": True,
            "fact_admission_implemented": False,
            "state_store_persistence_implemented": False,
            "read_model_store_write_implemented": False,
            "action_execution_implemented": False,
            "provider_access_implemented": False,
            "model_call_implemented": False,
            "runtime_implemented": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    out = run_field_state_reducer_module_integration_v1()
    raise SystemExit(0 if not out.get("failed_cases") else 1)
