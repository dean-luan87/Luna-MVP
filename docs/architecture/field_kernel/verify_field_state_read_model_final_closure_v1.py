#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


VERIFIER = "verify_field_state_read_model_final_closure_v1"


def _is_workspace_root(candidate: Path) -> bool:
    return (candidate / "AGENTS.md").exists() and (candidate / "capabilities").exists()


def _find_workspace_root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_workspace_root(cwd):
        return cwd
    script_path = Path(__file__).absolute()
    for candidate in (script_path.parent, *script_path.parents):
        if _is_workspace_root(candidate):
            return candidate
    raise RuntimeError("Unable to locate Luna workspace root")


ROOT = _find_workspace_root()
REPORT_PATH = ROOT / "_tmp_eval_out/field_state_read_model_final_closure_v1_smoke_v0/field_state_read_model_final_closure_v1.json"
RECORD_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_final_closure_record_v1.json"
DOC_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_final_closure_v1.md"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(check_id: int, title: str, passed: bool) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": bool(passed)}


def main() -> int:
    report = _read_json(REPORT_PATH)
    record = _read_json(RECORD_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")
    statuses = record.get("module_status", {})
    handoffs = record.get("handoffs", {})
    boundaries = record.get("preserved_boundaries", {})

    checks: List[Dict[str, Any]] = [
        _check(1, "required closure files exist", all(path.exists() for path in (REPORT_PATH, RECORD_PATH, DOC_PATH))),
        _check(2, "runner completed all checks", report.get("passed_checks") == report.get("total_checks") == 20),
        _check(3, "runner has no failures", report.get("failed_checks") == 0 and report.get("failed_items") == []),
        _check(4, "runner boundary preserved", report.get("boundary_preserved") is True),
        _check(5, "closure status is candidate", record.get("closure_status") == "final_closure_candidate"),
        _check(6, "promotion remains candidate", statuses.get("promotion") == "promotion_candidate"),
        _check(7, "baseline freeze remains candidate", statuses.get("baseline_freeze") == "baseline_freeze_candidate"),
        _check(8, "governance admission remains candidate", statuses.get("governance_admission") == "governance_admission_candidate"),
        _check(9, "lifecycle closure remains candidate", statuses.get("lifecycle_closure") == "lifecycle_closure_candidate"),
        _check(10, "production not activated", statuses.get("production") is False and report.get("production_activated") is False),
        _check(11, "formal L1 admission not executed", statuses.get("formal_l1_admission_executed") is False and report.get("formal_l1_admission_executed") is False),
        _check(12, "active baseline not modified", handoffs.get("baseline_freeze", {}).get("active_baseline_modified") is False),
        _check(13, "formal lifecycle not modified", handoffs.get("lifecycle_closure", {}).get("formal_lifecycle_modified") is False and report.get("formal_lifecycle_modified") is False),
        _check(14, "formal registry not modified", handoffs.get("lifecycle_closure", {}).get("formal_registry_modified") is False),
        _check(15, "Reducer authority preserved", boundaries.get("reducer_is_sole_mutation_authority") is True and boundaries.get("state_mutation") is False),
        _check(16, "Read Model remains read only", boundaries.get("read_only") is True and boundaries.get("candidate_only") is True),
        _check(17, "real storage remains disconnected", boundaries.get("real_state_store_connected") is False),
        _check(18, "downstream dispatch remains disconnected", boundaries.get("downstream_dispatch") is False),
        _check(19, "read semantics unchanged", boundaries.get("read_semantics_changed") is False),
        _check(20, "runtime semantics unchanged", boundaries.get("runtime_semantics_changed") is False),
        _check(21, "five-stage evidence recorded", len(record.get("accepted_phase_evidence", {})) == 5),
        _check(22, "deferred authority actions recorded", len(record.get("deferred_actions", [])) == 5),
        _check(23, "user-terminal stop status recorded", record.get("agent_stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION"),
        _check(24, "document preserves V2 V3 authority", "V2:" in doc and "V3:" in doc and "does not declare GO" in doc),
    ]
    failed = [item for item in checks if not item["passed"]]
    passed_count = len(checks) - len(failed)
    decision = "READY_FOR_CHATGPT_V3_AUDIT" if not failed else "BLOCKED_BY_VERIFIER_FAILURE"
    next_step = "RETURN_COMPLETE_OUTPUT_TO_CHATGPT" if not failed else "REMEDIATE_FINAL_CLOSURE_ONLY_AND_RERUN"

    output = {
        "module": "luna.field_state_read_model",
        "verifier": VERIFIER,
        "CHECKS": checks,
        "FAILED_CHECKS": failed,
        "PASSED_CHECK_COUNT": passed_count,
        "FAILED_CHECK_COUNT": len(failed),
        "BLOCKER_COUNT": len(failed),
        "FINAL_DECISION": decision,
        "NEXT": next_step,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
