#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def _is_root(path: Path) -> bool:
    return (path / "AGENTS.md").exists() and (path / "capabilities").is_dir()


def _root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_root(cwd):
        return cwd
    script = Path(__file__).absolute()
    for path in (script.parent, *script.parents):
        if _is_root(path):
            return path
    raise RuntimeError("Unable to locate Luna workspace root")


ROOT = _root()
CORE_DIR = ROOT / "capabilities/midplatform/core"
TYPES_PATH = CORE_DIR / "field_event_admission_types_v1.py"
API_PATH = CORE_DIR / "field_event_admission_api_v1.py"
SCHEMA_PATH = CORE_DIR / "field_event_admission_contract_v1.json"
RUNNER_PATH = ROOT / "tools/evaluation/midplatform/run_field_event_admission_temporal_validity_controlled_v1.py"
REPORT_PATH = ROOT / "_tmp_eval_out/field_event_admission_temporal_validity_controlled_v1_smoke_v0/field_event_admission_temporal_validity_controlled_v1.json"
DOC_PATH = ROOT / "docs/architecture/field_kernel/field_event_admission_temporal_validity_module_v1.md"


def _check(check_id: int, title: str, passed: bool) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": bool(passed)}


def main() -> int:
    types_text = TYPES_PATH.read_text(encoding="utf-8")
    api_text = API_PATH.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    runner_text = RUNNER_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    all_text = types_text + api_text + runner_text
    required = (
        TYPES_PATH, API_PATH, SCHEMA_PATH, DOC_PATH, RUNNER_PATH, REPORT_PATH
    )
    statuses = (
        "admitted_event", "rejected_event", "deferred_event",
        "duplicate_event", "expired_event", "out_of_order_event",
    )
    input_fields = (
        "event_id", "event_type", "field_ref", "occurred_at", "observed_at",
        "received_at", "source_chain", "evidence_refs", "payload", "trace_ref",
    )
    result_fields = (
        "admission_status", "reason_code", "event_ref", "field_ref",
        "temporal_assessment", "evidence_refs", "source_chain", "trace_ref",
        "evaluated_at", "reducer_eligible",
    )
    forbidden = (
        "sqlite", "redis", "kafka", "rabbitmq", "requests", "httpx",
        "field_state_reducer_module_api", "while True", "model_manager",
    )

    checks: List[Dict[str, Any]] = [
        _check(1, "required files exist", all(path.exists() for path in required)),
        _check(2, "six admission statuses exist", all(value in types_text for value in statuses)),
        _check(3, "required input fields exist", all(value in types_text for value in input_fields)),
        _check(4, "required result fields exist", all(value in types_text for value in result_fields)),
        _check(5, "stable reason registry exists", "ADMISSION_REASON_CODE_REGISTRY_V1" in types_text),
        _check(6, "timezone-aware parsing required", "parsed.tzinfo is None" in api_text and "timezone.utc" in api_text),
        _check(7, "system clock not read", "now(" not in api_text and "utcnow(" not in api_text),
        _check(8, "duplicate handling exists", "DUPLICATE_EVENT_ID" in api_text),
        _check(9, "expiration handling exists", "EVENT_EXPIRED" in api_text),
        _check(10, "out-of-order handling exists", "FIELD_SEQUENCE_OUT_OF_ORDER" in api_text and "TEMPORAL_SEQUENCE_OUT_OF_ORDER" in api_text),
        _check(11, "insufficient time defers", "TIME_INFORMATION_INSUFFICIENT" in api_text and "DEFERRED_EVENT" in api_text),
        _check(12, "only admitted is reducer eligible", "reducer_eligible = status is AdmissionStatusV1.ADMITTED_EVENT" in api_text),
        _check(13, "candidate is not fact", '"not_fact": True' in api_text and "fact_admitted: bool = False" in types_text),
        _check(14, "Reducer not executed", "reducer_executed: bool = False" in types_text and report.get("reducer_executed") is False),
        _check(15, "Field State not modified", "field_state_modified: bool = False" in types_text and report.get("field_state_modified") is False),
        _check(16, "no forbidden integration", not any(token in all_text for token in forbidden)),
        _check(17, "contract schema identifies input and output", "$defs" in schema and "event_candidate" in schema["$defs"] and "admission_result" in schema["$defs"]),
        _check(18, "runner covers required branches", all(value in runner_text for value in ("missing_required", "duplicate", "expired", "field_out_of_order", "temporal_insufficient", "deterministic_output"))),
        _check(19, "runner cases all passed", report.get("passed_cases") == report.get("total_cases") == 11),
        _check(20, "runner failures empty", report.get("failed_cases") == []),
        _check(21, "input immutability preserved", report.get("input_immutability_preserved") is True),
        _check(22, "deterministic output preserved", report.get("deterministic_output") is True),
        _check(23, "boundary preserved", report.get("boundary_preserved") is True and report.get("external_io_executed") is False),
        _check(24, "unhandled exceptions zero", report.get("unhandled_exceptions") == 0),
        _check(25, "governance stop point documented", "WAITING_FOR_USER_TERMINAL_VERIFICATION" in doc_text and "does not declare GO" in doc_text),
    ]
    failed = [item for item in checks if not item["passed"]]
    output = {
        "module": "luna.field_event_admission_temporal_validity",
        "verifier": "verify_field_event_admission_temporal_validity_module_v1",
        "CHECKS": checks,
        "FAILED_CHECKS": failed,
        "PASSED_CHECK_COUNT": len(checks) - len(failed),
        "FAILED_CHECK_COUNT": len(failed),
        "BLOCKER_COUNT": len(failed),
        "FINAL_DECISION": (
            "READY_FOR_CHATGPT_V3_AUDIT"
            if not failed
            else "BLOCKED_BY_VERIFIER_FAILURE"
        ),
        "NEXT": (
            "RETURN_COMPLETE_OUTPUT_TO_CHATGPT"
            if not failed
            else "REMEDIATE_MODULE_ONLY_AND_RERUN"
        ),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())

