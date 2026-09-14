#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


REPO_ROOT = Path(__file__).absolute().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "field_state_read_model_controlled_skeleton_v1_smoke_v0"
    / "field_state_read_model_controlled_skeleton_v1.json"
)

from capabilities.midplatform.core.field_state_read_model.module import (  # noqa: E402
    READ_STATUS_REGISTRY_V1,
    read_field_state,
)


ALLOWED_FINAL_DECISIONS = {
    "READY_FOR_USER_TERMINAL_VERIFICATION",
    "BLOCKED_BY_CONTROLLED_SKELETON",
}


def _base_query(
    case_id: str, required_fields: Tuple[str, ...] = ("status", "entities")
) -> Dict[str, Any]:
    return {
        "query_id": f"query_{case_id}",
        "requester_ref": "controlled_runner",
        "query_scope": "field_state",
        "field_state_ref": f"state_ref_{case_id}",
        "snapshot_ref": None,
        "task_ref": None,
        "scene_ref": None,
        "object_ref": None,
        "temporal_scope": None,
        "required_fields": list(required_fields),
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
        "metadata": {"case_id": case_id},
    }


def _base_state(case_id: str) -> Dict[str, Any]:
    return {
        "source_state_ref": f"state_ref_{case_id}",
        "state_version": "v1",
        "state_payload": {
            "entities": ["pedestrian", "road"],
            "status": "active",
            "region": "front_corridor",
            "confidence": 0.92,
        },
        "available_fields": ["confidence", "entities", "region", "status"],
        "provenance_refs": [f"prov_{case_id}_1", f"prov_{case_id}_2"],
        "temporal_status": "active",
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
    }


def _result_to_dict(result: Any) -> Dict[str, Any]:
    return asdict(result)


def _boundary_ok(result: Dict[str, Any]) -> bool:
    flags = dict(result.get("boundary_flags") or {})
    return (
        flags
        == {
            "read_only": True,
            "state_mutation": False,
            "event_reduction": False,
            "fact_admission": False,
            "evidence_fabrication": False,
            "real_model_execution": False,
            "action_execution": False,
            "runtime_loop": False,
            "real_state_store_connected": False,
            "candidate_only": True,
        }
        and result.get("runtime_executed") is False
    )


def _run_case(
    case_id: str,
    query: Dict[str, Any],
    state_candidate: Dict[str, Any] | None,
    expected_status: str,
) -> Dict[str, Any]:
    original_query = copy.deepcopy(query)
    original_state = copy.deepcopy(state_candidate)
    result = _result_to_dict(read_field_state(query, state_candidate))

    query_unchanged = query == original_query
    state_unchanged = state_candidate == original_state
    immutable = query_unchanged and state_unchanged
    boundary_ok = _boundary_ok(result)
    status_ok = result.get("read_status") == expected_status

    return {
        "case_id": case_id,
        "expected_status": expected_status,
        "read_status": result.get("read_status"),
        "module_status": result.get("module_status"),
        "passed": status_ok and boundary_ok and immutable,
        "query_unchanged": query_unchanged,
        "state_candidate_unchanged": state_unchanged,
        "input_immutability_preserved": immutable,
        "boundary_preserved": boundary_ok,
        "trace_ref": result.get("trace_ref"),
        "replay_key": result.get("replay_key"),
        "projection": result.get("projection"),
        "provenance_refs": result.get("provenance_refs"),
        "state_version": result.get("state_version"),
        "source_state_ref": result.get("source_state_ref"),
        "result": result,
    }


def run() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []

    cases.append(
        _run_case(
            "full_projection_read_ready",
            _base_query("full"),
            _base_state("full"),
            "read_ready",
        )
    )

    partial_state = _base_state("partial")
    partial_state["state_payload"].pop("entities")
    partial_state["available_fields"] = ["confidence", "region", "status"]
    cases.append(
        _run_case(
            "partial_projection",
            _base_query("partial"),
            partial_state,
            "partial_projection",
        )
    )

    insufficient_state = _base_state("insufficient")
    insufficient_state["state_payload"] = {"region": "front_corridor"}
    insufficient_state["available_fields"] = ["region"]
    cases.append(
        _run_case(
            "insufficient_state",
            _base_query("insufficient"),
            insufficient_state,
            "insufficient_state",
        )
    )

    stale_state = _base_state("stale")
    stale_state["temporal_status"] = "stale"
    cases.append(
        _run_case("stale_state", _base_query("stale"), stale_state, "stale_state")
    )

    cases.append(
        _run_case(
            "state_unavailable", _base_query("unavailable"), None, "state_unavailable"
        )
    )

    invalid_missing = _base_query("invalid_missing")
    invalid_missing["requester_ref"] = ""
    cases.append(
        _run_case(
            "invalid_query_missing_required_field",
            invalid_missing,
            _base_state("invalid_missing"),
            "query_rejected",
        )
    )

    invalid_no_ref = _base_query("invalid_no_ref")
    invalid_no_ref["field_state_ref"] = None
    invalid_no_ref["snapshot_ref"] = None
    cases.append(
        _run_case(
            "invalid_query_no_state_reference",
            invalid_no_ref,
            _base_state("invalid_no_ref"),
            "query_rejected",
        )
    )

    provenance_query = _base_query("provenance", ("status",))
    provenance_state = _base_state("provenance")
    cases.append(
        _run_case(
            "provenance_trace_version_preserved",
            provenance_query,
            provenance_state,
            "read_ready",
        )
    )

    immut_query = _base_query("immutability", ("region", "status"))
    immut_state = _base_state("immutability")
    cases.append(
        _run_case("input_immutability", immut_query, immut_state, "read_ready")
    )

    det_query = _base_query("deterministic", ("region", "status"))
    det_state = _base_state("deterministic")
    first = _result_to_dict(
        read_field_state(copy.deepcopy(det_query), copy.deepcopy(det_state))
    )
    second = _result_to_dict(
        read_field_state(copy.deepcopy(det_query), copy.deepcopy(det_state))
    )
    deterministic_match = all(
        first.get(key) == second.get(key)
        for key in (
            "read_status",
            "projection",
            "source_state_ref",
            "state_version",
            "provenance_refs",
            "replay_key",
            "boundary_flags",
        )
    )
    cases.append(
        {
            "case_id": "deterministic_replay",
            "expected_status": "read_ready",
            "read_status": first.get("read_status"),
            "module_status": first.get("module_status"),
            "passed": deterministic_match
            and first.get("read_status") == "read_ready"
            and _boundary_ok(first),
            "query_unchanged": True,
            "state_candidate_unchanged": True,
            "input_immutability_preserved": True,
            "boundary_preserved": _boundary_ok(first),
            "trace_ref": first.get("trace_ref"),
            "replay_key": first.get("replay_key"),
            "projection": first.get("projection"),
            "provenance_refs": first.get("provenance_refs"),
            "state_version": first.get("state_version"),
            "source_state_ref": first.get("source_state_ref"),
            "deterministic_match": deterministic_match,
            "result": first,
        }
    )

    status_registry_ok = tuple(READ_STATUS_REGISTRY_V1) == (
        "read_ready",
        "partial_projection",
        "insufficient_state",
        "stale_state",
        "state_unavailable",
        "query_rejected",
    )
    failed_cases = [case["case_id"] for case in cases if not case["passed"]]
    total_cases = len(cases)
    passed_cases = total_cases - len(failed_cases)
    boundary_preserved = (
        all(case.get("boundary_preserved", False) for case in cases)
        and status_registry_ok
    )
    input_immutability_preserved = all(
        case.get("input_immutability_preserved", False) for case in cases
    )
    deterministic_replay = bool(cases[-1].get("deterministic_match", False))
    unhandled_exceptions = 0
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if not failed_cases
        and boundary_preserved
        and deterministic_replay
        and input_immutability_preserved
        else "BLOCKED_BY_CONTROLLED_SKELETON"
    )

    report = {
        "module": "luna.field_state_read_model",
        "runner": "run_field_state_read_model_controlled_skeleton_v1",
        "skeleton_only": True,
        "runtime_executed": False,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "boundary_preserved": boundary_preserved,
        "deterministic_replay": deterministic_replay,
        "input_immutability_preserved": input_immutability_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "cases": cases,
        "final_decision_candidate": final_decision_candidate,
    }
    return report


def main() -> int:
    report = run()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["final_decision_candidate"] == "READY_FOR_USER_TERMINAL_VERIFICATION"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
