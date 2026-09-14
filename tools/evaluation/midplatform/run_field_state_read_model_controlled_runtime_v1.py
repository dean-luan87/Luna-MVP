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
    / "field_state_read_model_controlled_runtime_v1_smoke_v0"
    / "field_state_read_model_controlled_runtime_v1.json"
)

from capabilities.midplatform.core.field_state_read_model.runtime import (  # noqa: E402
    RUNTIME_STATUS_REGISTRY_V1,
    SOURCE_MODE_REGISTRY_V1,
    run_controlled_read_runtime,
)
from capabilities.midplatform.core.field_state_read_model.module import (  # noqa: E402
    get_default_boundary_flags_v1,
    read_field_state,
)


EXPECTED_BOUNDARY_FLAGS = get_default_boundary_flags_v1()
ALLOWED_FINAL_DECISIONS = {
    "READY_FOR_USER_TERMINAL_VERIFICATION",
    "BLOCKED_BY_CONTROLLED_RUNTIME",
}


def _base_query(
    case_id: str, required_fields: Tuple[str, ...] = ("status", "entities")
) -> Dict[str, Any]:
    return {
        "query_id": f"query_{case_id}",
        "requester_ref": "controlled_runtime_runner",
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


def _base_source_request(
    case_id: str, source_mode: str, state_candidate: Dict[str, Any] | None
) -> Dict[str, Any]:
    return {
        "source_request_id": f"source_req_{case_id}",
        "requested_state_ref": f"state_ref_{case_id}",
        "requested_snapshot_ref": None,
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
        "source_mode": source_mode,
        "controlled_payload": {"state_candidate": state_candidate},
    }


def _base_runtime_request(
    case_id: str, query: Dict[str, Any], source_request: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "runtime_request_id": f"runtime_req_{case_id}",
        "query": query,
        "source_request": source_request,
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
        "metadata": {"case_id": case_id},
    }


def _envelope_to_dict(envelope: Any) -> Dict[str, Any]:
    return asdict(envelope)


def _stable_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_boundary(envelope: Dict[str, Any]) -> bool:
    return (
        envelope.get("external_io_executed") is False
        and envelope.get("state_mutation_executed") is False
        and envelope.get("runtime_loop_executed") is False
        and envelope.get("candidate_only") is True
        and dict(envelope.get("boundary_flags") or {}) == EXPECTED_BOUNDARY_FLAGS
    )


def _run_case(
    case_id: str,
    runtime_request: Dict[str, Any],
    expected_runtime_status: str,
    expected_read_status: str,
    expected_source_status: str,
) -> Dict[str, Any]:
    original_request = copy.deepcopy(runtime_request)
    original_query = (
        copy.deepcopy(runtime_request.get("query"))
        if isinstance(runtime_request.get("query"), dict)
        else runtime_request.get("query")
    )
    original_source_request = (
        copy.deepcopy(runtime_request.get("source_request"))
        if isinstance(runtime_request.get("source_request"), dict)
        else runtime_request.get("source_request")
    )
    envelope = _envelope_to_dict(run_controlled_read_runtime(runtime_request))
    read_result = dict(envelope.get("read_result") or {})

    request_unchanged = runtime_request == original_request
    query_unchanged = runtime_request.get("query") == original_query
    source_request_unchanged = (
        runtime_request.get("source_request") == original_source_request
    )
    passed = (
        envelope.get("runtime_status") == expected_runtime_status
        and str(envelope.get("source_status") or "") == expected_source_status
        and str(envelope.get("read_status") or "") == expected_read_status
        and _assert_boundary(envelope)
        and request_unchanged
        and query_unchanged
        and source_request_unchanged
    )
    return {
        "case_id": case_id,
        "runtime_status": envelope.get("runtime_status"),
        "source_status": envelope.get("source_status"),
        "read_status": envelope.get("read_status"),
        "passed": passed,
        "request_unchanged": request_unchanged,
        "query_unchanged": query_unchanged,
        "source_request_unchanged": source_request_unchanged,
        "input_immutability_preserved": request_unchanged
        and query_unchanged
        and source_request_unchanged,
        "boundary_preserved": _assert_boundary(envelope),
        "read_api_invoked": envelope.get("read_api_invoked"),
        "runtime_attempted": envelope.get("runtime_attempted"),
        "external_io_executed": envelope.get("external_io_executed"),
        "state_mutation_executed": envelope.get("state_mutation_executed"),
        "runtime_loop_executed": envelope.get("runtime_loop_executed"),
        "candidate_only": envelope.get("candidate_only"),
        "trace_ref": envelope.get("trace_ref"),
        "replay_key": envelope.get("replay_key"),
        "source_reason": envelope.get("source_reason"),
        "error_reason": envelope.get("error_reason"),
        "provenance_refs": read_result.get("provenance_refs", []),
        "read_result": read_result,
        "stable_json": _stable_json(envelope),
    }


def run() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []

    q = _base_query("available_read_ready")
    s = _base_state("available_read_ready")
    cases.append(
        _run_case(
            "available_read_ready",
            _base_runtime_request(
                "available_read_ready",
                q,
                _base_source_request("available_read_ready", "candidate_available", s),
            ),
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    q = _base_query("available_partial_projection")
    s = _base_state("available_partial_projection")
    s["state_payload"].pop("entities")
    s["available_fields"] = ["confidence", "region", "status"]
    cases.append(
        _run_case(
            "available_partial_projection",
            _base_runtime_request(
                "available_partial_projection",
                q,
                _base_source_request(
                    "available_partial_projection", "candidate_available", s
                ),
            ),
            "runtime_partial",
            "partial_projection",
            "candidate_available",
        )
    )

    q = _base_query("available_insufficient_state")
    s = _base_state("available_insufficient_state")
    s["state_payload"] = {"region": "front_corridor"}
    s["available_fields"] = ["region"]
    cases.append(
        _run_case(
            "available_insufficient_state",
            _base_runtime_request(
                "available_insufficient_state",
                q,
                _base_source_request(
                    "available_insufficient_state", "candidate_available", s
                ),
            ),
            "runtime_partial",
            "insufficient_state",
            "candidate_available",
        )
    )

    q = _base_query("available_stale_state")
    s = _base_state("available_stale_state")
    s["temporal_status"] = "stale"
    cases.append(
        _run_case(
            "available_stale_state",
            _base_runtime_request(
                "available_stale_state",
                q,
                _base_source_request("available_stale_state", "candidate_available", s),
            ),
            "runtime_partial",
            "stale_state",
            "candidate_available",
        )
    )

    q = _base_query("source_unavailable")
    cases.append(
        _run_case(
            "source_unavailable",
            _base_runtime_request(
                "source_unavailable",
                q,
                _base_source_request(
                    "source_unavailable", "candidate_unavailable", None
                ),
            ),
            "runtime_unavailable",
            "state_unavailable",
            "candidate_unavailable",
        )
    )

    q = _base_query("malformed_candidate")
    malformed = {
        "source_state_ref": f"state_ref_malformed_candidate",
        "state_version": "v1",
        "state_payload": "bad_payload",
        "available_fields": ["status"],
        "provenance_refs": ["prov_bad_1"],
        "temporal_status": "active",
        "trace_ref": "trace_malformed_candidate",
        "replay_key": "replay_malformed_candidate",
    }
    cases.append(
        _run_case(
            "malformed_candidate",
            _base_runtime_request(
                "malformed_candidate",
                q,
                _base_source_request(
                    "malformed_candidate", "candidate_malformed", malformed
                ),
            ),
            "runtime_unavailable",
            "state_unavailable",
            "candidate_malformed",
        )
    )

    q = _base_query("source_rejected")
    source_request = _base_source_request("source_rejected", "source_rejected", None)
    source_request["controlled_payload"]["source_reason"] = "source_denied"
    cases.append(
        _run_case(
            "source_rejected",
            _base_runtime_request("source_rejected", q, source_request),
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "invalid_runtime_missing_id",
        _base_query("invalid_runtime_missing_id"),
        _base_source_request(
            "invalid_runtime_missing_id",
            "candidate_available",
            _base_state("invalid_runtime_missing_id"),
        ),
    )
    runtime_request["runtime_request_id"] = ""
    cases.append(
        _run_case(
            "invalid_runtime_missing_id",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "invalid_runtime_query_type",
        _base_query("invalid_runtime_query_type"),
        _base_source_request(
            "invalid_runtime_query_type",
            "candidate_available",
            _base_state("invalid_runtime_query_type"),
        ),
    )
    runtime_request["query"] = "not_a_dict"
    cases.append(
        _run_case(
            "invalid_runtime_query_type",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "invalid_runtime_source_request_type",
        _base_query("invalid_runtime_source_request_type"),
        _base_source_request(
            "invalid_runtime_source_request_type",
            "candidate_available",
            _base_state("invalid_runtime_source_request_type"),
        ),
    )
    runtime_request["source_request"] = "not_a_dict"
    cases.append(
        _run_case(
            "invalid_runtime_source_request_type",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "unknown_runtime_field",
        _base_query("unknown_runtime_field"),
        _base_source_request(
            "unknown_runtime_field",
            "candidate_available",
            _base_state("unknown_runtime_field"),
        ),
    )
    runtime_request["unexpected_field"] = True
    cases.append(
        _run_case(
            "unknown_runtime_field",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "trace_mismatch_runtime_query",
        _base_query("trace_mismatch_runtime_query"),
        _base_source_request(
            "trace_mismatch_runtime_query",
            "candidate_available",
            _base_state("trace_mismatch_runtime_query"),
        ),
    )
    runtime_request["query"]["trace_ref"] = "other_trace"
    cases.append(
        _run_case(
            "trace_mismatch_runtime_query",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "replay_mismatch_runtime_query",
        _base_query("replay_mismatch_runtime_query"),
        _base_source_request(
            "replay_mismatch_runtime_query",
            "candidate_available",
            _base_state("replay_mismatch_runtime_query"),
        ),
    )
    runtime_request["query"]["replay_key"] = "other_replay"
    cases.append(
        _run_case(
            "replay_mismatch_runtime_query",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "trace_mismatch_runtime_source",
        _base_query("trace_mismatch_runtime_source"),
        _base_source_request(
            "trace_mismatch_runtime_source",
            "candidate_available",
            _base_state("trace_mismatch_runtime_source"),
        ),
    )
    runtime_request["source_request"]["trace_ref"] = "other_trace"
    cases.append(
        _run_case(
            "trace_mismatch_runtime_source",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "replay_mismatch_runtime_source",
        _base_query("replay_mismatch_runtime_source"),
        _base_source_request(
            "replay_mismatch_runtime_source",
            "candidate_available",
            _base_state("replay_mismatch_runtime_source"),
        ),
    )
    runtime_request["source_request"]["replay_key"] = "other_replay"
    cases.append(
        _run_case(
            "replay_mismatch_runtime_source",
            runtime_request,
            "runtime_rejected",
            "",
            "source_rejected",
        )
    )

    det_query = _base_query("deterministic_replay", ("region", "status"))
    det_state = _base_state("deterministic_replay")
    det_request = _base_runtime_request(
        "deterministic_replay",
        det_query,
        _base_source_request("deterministic_replay", "candidate_available", det_state),
    )
    first = _envelope_to_dict(run_controlled_read_runtime(copy.deepcopy(det_request)))
    second = _envelope_to_dict(run_controlled_read_runtime(copy.deepcopy(det_request)))
    cases.append(
        {
            "case_id": "deterministic_replay",
            "runtime_status": first.get("runtime_status"),
            "source_status": first.get("source_status"),
            "read_status": first.get("read_status"),
            "passed": _stable_json(first) == _stable_json(second),
            "request_unchanged": True,
            "query_unchanged": True,
            "source_request_unchanged": True,
            "input_immutability_preserved": True,
            "boundary_preserved": _assert_boundary(first),
            "read_api_invoked": first.get("read_api_invoked"),
            "runtime_attempted": first.get("runtime_attempted"),
            "external_io_executed": first.get("external_io_executed"),
            "state_mutation_executed": first.get("state_mutation_executed"),
            "runtime_loop_executed": first.get("runtime_loop_executed"),
            "candidate_only": first.get("candidate_only"),
            "trace_ref": first.get("trace_ref"),
            "replay_key": first.get("replay_key"),
            "source_reason": first.get("source_reason"),
            "error_reason": first.get("error_reason"),
            "provenance_refs": (first.get("read_result") or {}).get(
                "provenance_refs", []
            ),
            "read_result": dict(first.get("read_result") or {}),
            "stable_json": _stable_json(first),
        }
    )

    runtime_request = _base_runtime_request(
        "input_immutability",
        _base_query("input_immutability", ("region", "status")),
        _base_source_request(
            "input_immutability",
            "candidate_available",
            _base_state("input_immutability"),
        ),
    )
    cases.append(
        _run_case(
            "input_immutability",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    runtime_request = _base_runtime_request(
        "exception_containment",
        _base_query("exception_containment"),
        _base_source_request(
            "exception_containment",
            "candidate_available",
            _base_state("exception_containment"),
        ),
    )
    runtime_request["source_request"]["controlled_payload"][
        "force_adapter_exception"
    ] = True
    cases.append(
        _run_case(
            "exception_containment",
            runtime_request,
            "runtime_error_contained",
            "",
            "source_rejected",
        )
    )

    runtime_request = _base_runtime_request(
        "no_external_io",
        _base_query("no_external_io", ("status",)),
        _base_source_request(
            "no_external_io", "candidate_available", _base_state("no_external_io")
        ),
    )
    cases.append(
        _run_case(
            "no_external_io",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    runtime_request = _base_runtime_request(
        "no_state_mutation",
        _base_query("no_state_mutation", ("status",)),
        _base_source_request(
            "no_state_mutation", "candidate_available", _base_state("no_state_mutation")
        ),
    )
    cases.append(
        _run_case(
            "no_state_mutation",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    runtime_request = _base_runtime_request(
        "no_runtime_loop",
        _base_query("no_runtime_loop", ("status",)),
        _base_source_request(
            "no_runtime_loop", "candidate_available", _base_state("no_runtime_loop")
        ),
    )
    cases.append(
        _run_case(
            "no_runtime_loop",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    runtime_request = _base_runtime_request(
        "candidate_only",
        _base_query("candidate_only", ("status",)),
        _base_source_request(
            "candidate_only", "candidate_available", _base_state("candidate_only")
        ),
    )
    cases.append(
        _run_case(
            "candidate_only",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    runtime_request = _base_runtime_request(
        "provenance_preserved",
        _base_query("provenance_preserved", ("status",)),
        _base_source_request(
            "provenance_preserved",
            "candidate_available",
            _base_state("provenance_preserved"),
        ),
    )
    runtime_request["source_request"]["controlled_payload"]["state_candidate"][
        "provenance_refs"
    ] = ["prov_b", "prov_a", "prov_c"]
    cases.append(
        _run_case(
            "provenance_preserved",
            runtime_request,
            "runtime_completed",
            "read_ready",
            "candidate_available",
        )
    )

    compat_query = _base_query("contract_dryrun_compatibility")
    compat_state = _base_state("contract_dryrun_compatibility")
    compat_request = _base_runtime_request(
        "contract_dryrun_compatibility",
        compat_query,
        _base_source_request(
            "contract_dryrun_compatibility", "candidate_available", compat_state
        ),
    )
    compat_envelope = _envelope_to_dict(
        run_controlled_read_runtime(copy.deepcopy(compat_request))
    )
    direct = asdict(
        read_field_state(copy.deepcopy(compat_query), copy.deepcopy(compat_state))
    )
    cases.append(
        {
            "case_id": "contract_dryrun_compatibility",
            "runtime_status": compat_envelope.get("runtime_status"),
            "source_status": compat_envelope.get("source_status"),
            "read_status": compat_envelope.get("read_status"),
            "passed": compat_envelope.get("read_result") == direct
            and _assert_boundary(compat_envelope),
            "request_unchanged": True,
            "query_unchanged": True,
            "source_request_unchanged": True,
            "input_immutability_preserved": True,
            "boundary_preserved": _assert_boundary(compat_envelope),
            "read_api_invoked": compat_envelope.get("read_api_invoked"),
            "runtime_attempted": compat_envelope.get("runtime_attempted"),
            "external_io_executed": compat_envelope.get("external_io_executed"),
            "state_mutation_executed": compat_envelope.get("state_mutation_executed"),
            "runtime_loop_executed": compat_envelope.get("runtime_loop_executed"),
            "candidate_only": compat_envelope.get("candidate_only"),
            "trace_ref": compat_envelope.get("trace_ref"),
            "replay_key": compat_envelope.get("replay_key"),
            "source_reason": compat_envelope.get("source_reason"),
            "error_reason": compat_envelope.get("error_reason"),
            "provenance_refs": (compat_envelope.get("read_result") or {}).get(
                "provenance_refs", []
            ),
            "read_result": dict(compat_envelope.get("read_result") or {}),
            "stable_json": _stable_json(compat_envelope),
        }
    )

    total_cases = len(cases)
    failed_cases = [case["case_id"] for case in cases if not case["passed"]]
    passed_cases = total_cases - len(failed_cases)
    source_adapter_deterministic = cases[15]["passed"]
    runtime_deterministic = cases[15]["passed"]
    contract_dryrun_compatible = next(
        case for case in cases if case["case_id"] == "contract_dryrun_compatibility"
    )["passed"]
    provenance_validation_cases = {
        "provenance_preserved": ["prov_b", "prov_a", "prov_c"],
        "contract_dryrun_compatibility": [
            "prov_contract_dryrun_compatibility_1",
            "prov_contract_dryrun_compatibility_2",
        ],
    }
    provenance_preserved = all(
        list(
            next(case for case in cases if case["case_id"] == case_id)[
                "provenance_refs"
            ]
            or []
        )
        == expected_refs
        for case_id, expected_refs in provenance_validation_cases.items()
    )
    input_immutability_preserved = all(
        case.get("input_immutability_preserved", False) for case in cases
    )
    boundary_preserved = all(case.get("boundary_preserved", False) for case in cases)
    external_io_executed = any(bool(case.get("external_io_executed")) for case in cases)
    state_mutation_executed = any(
        bool(case.get("state_mutation_executed")) for case in cases
    )
    runtime_loop_executed = any(
        bool(case.get("runtime_loop_executed")) for case in cases
    )
    unhandled_exceptions = 0
    source_modes_covered = sorted(
        {
            case.get("source_status")
            for case in cases
            if case.get("source_status") in SOURCE_MODE_REGISTRY_V1
        }
    )
    runtime_statuses_covered = sorted(
        {
            case.get("runtime_status")
            for case in cases
            if case.get("runtime_status") in RUNTIME_STATUS_REGISTRY_V1
        }
    )
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if not failed_cases
        and source_adapter_deterministic
        and runtime_deterministic
        and contract_dryrun_compatible
        and provenance_preserved
        and input_immutability_preserved
        and boundary_preserved
        and not external_io_executed
        and not state_mutation_executed
        and not runtime_loop_executed
        else "BLOCKED_BY_CONTROLLED_RUNTIME"
    )
    if final_decision_candidate not in ALLOWED_FINAL_DECISIONS:
        final_decision_candidate = "BLOCKED_BY_CONTROLLED_RUNTIME"

    return {
        "module": "luna.field_state_read_model",
        "runner": "run_field_state_read_model_controlled_runtime_v1",
        "controlled_runtime_only": True,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "source_adapter_deterministic": source_adapter_deterministic,
        "runtime_deterministic": runtime_deterministic,
        "contract_dryrun_compatible": contract_dryrun_compatible,
        "provenance_preserved": provenance_preserved,
        "input_immutability_preserved": input_immutability_preserved,
        "boundary_preserved": boundary_preserved,
        "external_io_executed": external_io_executed,
        "state_mutation_executed": state_mutation_executed,
        "runtime_loop_executed": runtime_loop_executed,
        "unhandled_exceptions": unhandled_exceptions,
        "source_modes_covered": source_modes_covered,
        "runtime_statuses_covered": runtime_statuses_covered,
        "cases": cases,
        "final_decision_candidate": final_decision_candidate,
    }


def main() -> int:
    report = run()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["final_decision_candidate"] == "READY_FOR_USER_TERMINAL_VERIFICATION"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
