#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).absolute().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.core.field_event_admission_api_v1 import (  # noqa: E402
    admit_field_event,
)
from capabilities.midplatform.core.field_event_admission_types_v1 import (  # noqa: E402
    AdmissionContextV1,
    AdmissionPolicyV1,
)


REPORT_PATH = ROOT / "_tmp_eval_out/field_event_admission_temporal_validity_controlled_v1_smoke_v0/field_event_admission_temporal_validity_controlled_v1.json"
POLICY = AdmissionPolicyV1(
    evaluated_at="2026-07-20T12:00:00Z",
    max_event_age_seconds=3600,
    max_out_of_order_seconds=60,
    future_tolerance_seconds=30,
)


def _event(case_id: str) -> Dict[str, Any]:
    return {
        "event_id": f"event_{case_id}",
        "event_type": "field_transition_detected",
        "field_ref": "field_alpha",
        "occurred_at": "2026-07-20T11:55:00Z",
        "observed_at": "2026-07-20T11:56:00Z",
        "received_at": "2026-07-20T11:57:00Z",
        "source_chain": ["sensor:controlled", "adapter:v1"],
        "evidence_refs": [f"evidence_{case_id}"],
        "payload": {"candidate": "transition", "confidence": 0.9},
        "trace_ref": f"trace_{case_id}",
    }


def _case(
    case_id: str,
    event: Dict[str, Any],
    expected: str,
    context: AdmissionContextV1 = AdmissionContextV1(),
) -> Dict[str, Any]:
    original_event = copy.deepcopy(event)
    original_context = copy.deepcopy(context)
    result = asdict(admit_field_event(event, POLICY, context))
    immutable = event == original_event and context == original_context
    eligible_ok = result["reducer_eligible"] is (expected == "admitted_event")
    candidate_ok = (
        result["reducer_input_candidate"] is not None
        if expected == "admitted_event"
        else result["reducer_input_candidate"] is None
    )
    preserved = (
        result["evidence_refs"] == tuple(original_event.get("evidence_refs", ()))
        and result["source_chain"] == tuple(original_event.get("source_chain", ()))
        and result["trace_ref"] == str(original_event.get("trace_ref", ""))
    )
    boundary = all(
        (
            result["candidate_only"] is True,
            result["fact_admitted"] is False,
            result["field_state_modified"] is False,
            result["reducer_executed"] is False,
            result["external_io_executed"] is False,
        )
    )
    return {
        "case_id": case_id,
        "expected_status": expected,
        "actual_status": result["admission_status"],
        "reason_code": result["reason_code"],
        "passed": (
            result["admission_status"] == expected
            and eligible_ok and candidate_ok and immutable and preserved and boundary
        ),
        "input_immutability_preserved": immutable,
        "lineage_preserved": preserved,
        "boundary_preserved": boundary,
        "result": result,
    }


def run() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []
    cases.append(_case("admitted", _event("admitted"), "admitted_event"))

    missing = _event("missing")
    missing["field_ref"] = ""
    cases.append(_case("missing_required", missing, "rejected_event"))

    insufficient = _event("insufficient")
    insufficient["observed_at"] = None
    cases.append(_case("temporal_insufficient", insufficient, "deferred_event"))

    duplicate = _event("duplicate")
    cases.append(
        _case(
            "duplicate",
            duplicate,
            "duplicate_event",
            AdmissionContextV1(known_event_ids=(duplicate["event_id"],)),
        )
    )

    expired = _event("expired")
    expired.update(
        {
            "occurred_at": "2026-07-20T10:00:00Z",
            "observed_at": "2026-07-20T10:01:00Z",
            "received_at": "2026-07-20T10:02:00Z",
        }
    )
    cases.append(_case("expired", expired, "expired_event"))

    out_of_order = _event("out_of_order")
    cases.append(
        _case(
            "field_out_of_order",
            out_of_order,
            "out_of_order_event",
            AdmissionContextV1(
                latest_occurred_at_by_field={
                    "field_alpha": "2026-07-20T11:59:00Z"
                }
            ),
        )
    )

    chronology = _event("chronology")
    chronology["observed_at"] = "2026-07-20T11:54:00Z"
    cases.append(
        _case("chronology_out_of_order", chronology, "out_of_order_event")
    )

    future = _event("future")
    future.update(
        {
            "occurred_at": "2026-07-20T12:02:00Z",
            "observed_at": "2026-07-20T12:02:01Z",
            "received_at": "2026-07-20T12:02:02Z",
        }
    )
    cases.append(_case("future_deferred", future, "deferred_event"))

    invalid_time = _event("invalid_time")
    invalid_time["occurred_at"] = "2026-07-20 11:55:00"
    cases.append(_case("timezone_required", invalid_time, "rejected_event"))

    no_evidence = _event("no_evidence")
    no_evidence["evidence_refs"] = []
    cases.append(_case("evidence_required", no_evidence, "rejected_event"))

    deterministic_event = _event("deterministic")
    first = asdict(admit_field_event(copy.deepcopy(deterministic_event), POLICY))
    second = asdict(admit_field_event(copy.deepcopy(deterministic_event), POLICY))
    deterministic = first == second
    cases.append(
        {
            "case_id": "deterministic_output",
            "expected_status": "admitted_event",
            "actual_status": first["admission_status"],
            "reason_code": first["reason_code"],
            "passed": deterministic and first["admission_status"] == "admitted_event",
            "input_immutability_preserved": True,
            "lineage_preserved": True,
            "boundary_preserved": (
                first["field_state_modified"] is False
                and first["reducer_executed"] is False
            ),
            "deterministic_match": deterministic,
            "result": first,
        }
    )

    failed = [case["case_id"] for case in cases if not case["passed"]]
    report = {
        "module": "luna.field_event_admission_temporal_validity",
        "runner": "run_field_event_admission_temporal_validity_controlled_v1",
        "total_cases": len(cases),
        "passed_cases": len(cases) - len(failed),
        "failed_cases": failed,
        "boundary_preserved": all(case["boundary_preserved"] for case in cases),
        "input_immutability_preserved": all(
            case["input_immutability_preserved"] for case in cases
        ),
        "deterministic_output": deterministic,
        "reducer_executed": False,
        "field_state_modified": False,
        "external_io_executed": False,
        "unhandled_exceptions": 0,
        "cases": cases,
        "final_decision_candidate": (
            "READY_FOR_USER_TERMINAL_VERIFICATION"
            if not failed
            else "BLOCKED_BY_CONTROLLED_MODULE"
        ),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    output = run()
    print(json.dumps(output, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not output["failed_cases"] else 2)

