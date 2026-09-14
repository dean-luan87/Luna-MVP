from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.state_reduction import (  # noqa: E402
    build_handoff_input_from_selection_result,
    reduce_selected_policy_to_state_candidate_v1,
    result_to_dict,
)


def _selection_result(
    case_id: str,
    selection_status: str,
    selected_policy_ids: List[str],
    composition_sequence: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "selection_id": f"selection_{case_id}",
        "reducer_run_id": f"run_{case_id}",
        "field_id": "field_001",
        "state_type": "presence_state",
        "selection_status": selection_status,
        "selected_policy_ids": selected_policy_ids,
        "composition_sequence": composition_sequence or selected_policy_ids,
        "selection_trace_ref": f"selection_trace_{case_id}",
        "replay_key": f"selection_replay_{case_id}",
        "evaluated_contract_versions": {
            "policy_registry_version": "v1",
            "eligibility_matrix_version": "v1",
            "precedence_matrix_version": "v1",
            "composition_contract_version": "v1",
            "replay_contract_version": "v1",
        },
    }


def _policy_metadata(selected_policy_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    return {pid: {"policy_version": "v1"} for pid in selected_policy_ids}


def _handoff_from_selection(
    selection_result: Dict[str, Any],
    *,
    existing_status: str,
    temporal_status: str,
    conflict_unresolved: bool = False,
    overlay_active: bool = False,
    overlay_expired: bool = False,
    refresh_evidence_available: bool = True,
    new_event_available: bool = True,
    sufficient_evidence: bool = True,
    direct_write: bool = False,
    action_trigger: bool = False,
    missing_metadata: bool = False,
) -> Any:
    selected = list(selection_result.get("selected_policy_ids", []))
    metadata = {} if missing_metadata else _policy_metadata(selected)
    return build_handoff_input_from_selection_result(
        selection_result,
        existing_state_snapshot={
            "state_id": f"state_{selection_result['selection_id']}",
            "status": existing_status,
            "value": {"source": "existing"},
        },
        admitted_event_refs=("evt_1", "evt_2"),
        temporal_snapshot={
            "status": temporal_status,
            "refresh_evidence_available": refresh_evidence_available,
            "new_event_available": new_event_available,
            "sufficient_evidence": sufficient_evidence,
            "confidence_snapshot": {"confidence": 0.9},
        },
        conflict_snapshot={
            "conflict_type": "direct_vs_inferred",
            "unresolved": conflict_unresolved,
            "preserve_conflict": True,
            "provisional_candidate_allowed": True,
            "conflicting_event_refs": ["evt_conflict_1", "evt_conflict_2"]
            if conflict_unresolved
            else [],
            "resolution_available": False,
        },
        overlay_snapshot={
            "overlay_refs": ["overlay_1"]
            if (overlay_active or overlay_expired)
            else [],
            "overlay_active": overlay_active,
            "overlay_expired": overlay_expired,
            "substrate_mutation_requested": False,
        },
        owner_correction_snapshot={"owner_correction_refs": ["owner_ref_1"]},
        policy_evaluation_refs=("eval_ref_1", "eval_ref_2"),
        selected_policy_metadata=metadata,
        direct_state_write_requested=direct_write,
        action_trigger_requested=action_trigger,
    )


def run_field_state_reducer_state_reduction_internal_integration_v1() -> Dict[str, Any]:
    cases: List[Tuple[str, str, Dict[str, Any], str]] = []

    cases.append(
        (
            "create_new_candidate",
            "state_candidate_built",
            _selection_result("create", "selected_single", ["latest_valid_event"]),
            "candidate",
        )
    )
    cases.append(
        (
            "update_existing_candidate",
            "state_candidate_built",
            _selection_result(
                "update", "selected_single", ["highest_confidence_valid_event"]
            ),
            "candidate",
        )
    )
    cases.append(
        (
            "maintain_state",
            "state_candidate_built",
            _selection_result("maintain", "selected_single", ["multi_event_consensus"]),
            "active",
        )
    )
    cases.append(
        (
            "no_state_change",
            "no_state_change",
            _selection_result("no_change", "no_state_change", ["no_state_change"]),
            "active",
        )
    )
    cases.append(
        (
            "expired_state",
            "state_candidate_built",
            _selection_result("expired", "selected_single", ["expiration_degrade"]),
            "active",
        )
    )
    cases.append(
        (
            "suspended_without_refresh",
            "state_candidate_built",
            _selection_result("suspended", "selected_single", ["latest_valid_event"]),
            "suspended",
        )
    )
    cases.append(
        (
            "revoked_state",
            "state_candidate_built",
            _selection_result("revoked", "selected_single", ["revocation_override"]),
            "active",
        )
    )
    cases.append(
        (
            "superseded_state",
            "state_candidate_built",
            _selection_result(
                "superseded", "selected_single", ["explicit_owner_override_candidate"]
            ),
            "active",
        )
    )
    cases.append(
        (
            "unresolved_conflict",
            "state_candidate_built",
            _selection_result(
                "unresolved", "selected_single", ["conflict_preservation"]
            ),
            "active",
        )
    )
    cases.append(
        (
            "temporary_overlay",
            "state_candidate_built",
            _selection_result(
                "overlay", "selected_single", ["temporary_overlay_separation"]
            ),
            "active",
        )
    )
    cases.append(
        (
            "expired_overlay",
            "state_candidate_built",
            _selection_result(
                "overlay_expired", "selected_single", ["temporary_overlay_separation"]
            ),
            "active",
        )
    )
    cases.append(
        (
            "owner_correction_candidate",
            "state_candidate_built",
            _selection_result(
                "owner", "selected_single", ["explicit_owner_override_candidate"]
            ),
            "candidate",
        )
    )
    cases.append(
        (
            "missing_evidence",
            "state_candidate_built",
            _selection_result(
                "missing_evidence",
                "selected_single",
                ["insufficient_evidence_unresolved"],
            ),
            "unresolved",
        )
    )
    cases.append(
        (
            "invalid_transition",
            "invalid_transition",
            _selection_result(
                "invalid_transition", "selected_single", ["latest_valid_event"]
            ),
            "revoked",
        )
    )

    results: List[Dict[str, Any]] = []
    failed_cases: List[str] = []

    for case_id, expected_reduction_status, selection_row, existing_status in cases:
        handoff = _handoff_from_selection(
            selection_row,
            existing_status=existing_status,
            temporal_status=(
                "expired"
                if case_id == "expired_state"
                else "suspended"
                if case_id == "suspended_without_refresh"
                else "revoked"
                if case_id == "revoked_state"
                else "superseded"
                if case_id == "superseded_state"
                else "active"
            ),
            conflict_unresolved=(case_id == "unresolved_conflict"),
            overlay_active=(case_id == "temporary_overlay"),
            overlay_expired=(case_id == "expired_overlay"),
            refresh_evidence_available=(case_id != "suspended_without_refresh"),
            new_event_available=(case_id != "invalid_transition"),
            sufficient_evidence=(case_id != "missing_evidence"),
            missing_metadata=(case_id == "owner_correction_candidate" and False),
        )

        result, trace = reduce_selected_policy_to_state_candidate_v1(handoff)
        row = result_to_dict(result)
        row["trace_present"] = bool(trace.get("trace_id"))
        row["case_id"] = case_id
        row["expected_reduction_status"] = expected_reduction_status
        row["status_matched"] = row["reduction_status"] == expected_reduction_status
        results.append(row)
        if not row["status_matched"]:
            failed_cases.append(case_id)

    # Extra reject-path checks under selection handoff constraints.
    reject_rows: List[Dict[str, Any]] = []
    reject_inputs = [
        (
            "reject_unresolved_precedence",
            _selection_result(
                "rej_precedence", "unresolved_precedence", ["latest_valid_event"]
            ),
            False,
            False,
            False,
        ),
        (
            "reject_unresolved_exclusion",
            _selection_result(
                "rej_exclusion", "unresolved_exclusion", ["latest_valid_event"]
            ),
            False,
            False,
            False,
        ),
        (
            "reject_invalid_input",
            _selection_result("rej_invalid", "invalid_input", ["latest_valid_event"]),
            False,
            False,
            False,
        ),
        (
            "reject_missing_version",
            {
                **_selection_result(
                    "rej_missing_version", "selected_single", ["latest_valid_event"]
                ),
                "evaluated_contract_versions": {},
            },
            False,
            False,
            False,
        ),
        (
            "reject_missing_metadata",
            _selection_result(
                "rej_missing_meta", "selected_single", ["latest_valid_event"]
            ),
            True,
            False,
            False,
        ),
        (
            "reject_direct_write",
            _selection_result(
                "rej_direct_write", "selected_single", ["latest_valid_event"]
            ),
            False,
            True,
            False,
        ),
        (
            "reject_action_trigger",
            _selection_result("rej_action", "selected_single", ["latest_valid_event"]),
            False,
            False,
            True,
        ),
    ]

    reject_failed: List[str] = []
    for (
        case_id,
        selection_row,
        missing_meta,
        direct_write,
        action_trigger,
    ) in reject_inputs:
        handoff = _handoff_from_selection(
            selection_row,
            existing_status="active",
            temporal_status="active",
            missing_metadata=missing_meta,
            direct_write=direct_write,
            action_trigger=action_trigger,
        )
        result, trace = reduce_selected_policy_to_state_candidate_v1(handoff)
        row = result_to_dict(result)
        row["trace_present"] = bool(trace.get("trace_id"))
        row["case_id"] = case_id
        row["handoff_should_reject"] = True
        row["handoff_rejected"] = row["handoff_status"] == "rejected"
        reject_rows.append(row)
        if not row["handoff_rejected"]:
            reject_failed.append(case_id)

    boundary_ok = all(
        r["real_state_store_write_implemented"] is False
        and r["fact_admission_implemented"] is False
        and r["action_trigger_implemented"] is False
        and r["runtime_implemented"] is False
        and (r.get("state_candidate") or {}).get("persisted", False) is False
        and (r.get("state_candidate") or {}).get("fact_admitted", False) is False
        for r in results + reject_rows
    )

    report = {
        "module": "Luna Field State Reducer",
        "internal_segment": "Policy Selection To State Reduction Core",
        "execution_mode": "Function Module Continuous Build",
        "total_cases": len(cases),
        "passed_cases": len(cases) - len(failed_cases),
        "failed_cases": failed_cases,
        "handoff_reject_cases": len(reject_inputs),
        "handoff_reject_failed_cases": reject_failed,
        "trace_present_all": all(
            bool(r.get("trace_present")) for r in results + reject_rows
        ),
        "replay_present_all": all(
            bool(r.get("replay_key")) for r in results + reject_rows
        ),
        "boundary_preserved": boundary_ok,
        "module_status": {
            "selection_handoff_implemented": True,
            "policy_application_planner_implemented": True,
            "state_reduction_core_implemented": True,
            "state_transition_engine_implemented": True,
            "conflict_reduction_implemented": True,
            "overlay_reduction_implemented": True,
            "state_candidate_builder_implemented": True,
            "provenance_trace_replay_implemented": True,
            "internal_integration_runner_created": True,
            "real_state_store_write_implemented": False,
            "fact_admission_implemented": False,
            "action_trigger_implemented": False,
            "runtime_implemented": False,
        },
        "results": results,
        "handoff_reject_results": reject_rows,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    out = run_field_state_reducer_state_reduction_internal_integration_v1()
    failed = list(out.get("failed_cases", [])) + list(
        out.get("handoff_reject_failed_cases", [])
    )
    raise SystemExit(0 if not failed else 1)
