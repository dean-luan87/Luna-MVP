#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


CAPABILITY_ID = "luna.field_state_read_model"
RUNNER = "run_field_state_read_model_final_closure_v1"


def _is_workspace_root(candidate: Path) -> bool:
    return all(
        marker.exists()
        for marker in (
            candidate / "AGENTS.md",
            candidate / "capabilities",
            candidate / "tools" / "evaluation" / "midplatform",
        )
    )


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
DOC_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_final_closure_v1.md"
RECORD_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_final_closure_record_v1.json"
ELIGIBILITY_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_promotion_eligibility_record_v1.json"
FREEZE_PATH = ROOT / "capabilities/registry/baselines/field_state_read_model_module_baseline_freeze_candidate_v1.json"
ADMISSION_PATH = ROOT / "docs/architecture/field_kernel/field_state_read_model_governance_admission_review_v1.json"
MANIFEST_PATH = ROOT / "capabilities/registry/manifests/field_state_read_model_manifest_v1.json"
PROMOTION_REPORT_PATH = ROOT / "_tmp_eval_out/field_state_read_model_promotion_governance_admission_v1_smoke_v0/field_state_read_model_promotion_governance_admission_v1.json"
REPORT_PATH = ROOT / "_tmp_eval_out/field_state_read_model_final_closure_v1_smoke_v0/field_state_read_model_final_closure_v1.json"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(check_id: int, title: str, passed: bool) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": bool(passed)}


def run() -> Dict[str, Any]:
    record = _read_json(RECORD_PATH)
    eligibility = _read_json(ELIGIBILITY_PATH)
    freeze = _read_json(FREEZE_PATH)
    admission = _read_json(ADMISSION_PATH)
    manifest = _read_json(MANIFEST_PATH)
    promotion = _read_json(PROMOTION_REPORT_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")
    statuses = record.get("module_status", {})
    handoffs = record.get("handoffs", {})
    boundaries = record.get("preserved_boundaries", {})
    evidence = record.get("accepted_phase_evidence", {})

    expected_evidence = {
        "controlled_skeleton": ("10/10", "18/18"),
        "contract_dryrun": ("45/45", "20/20"),
        "controlled_runtime": ("24/24", "25/25"),
        "module_integration": ("25/25", "26/26"),
        "promotion_governance_admission": ("30/30", "28/28"),
    }
    evidence_complete = all(
        evidence.get(stage, {}).get("runner") == results[0]
        and evidence.get(stage, {}).get("verifier") == results[1]
        for stage, results in expected_evidence.items()
    )
    expected_boundaries = {
        "reducer_is_sole_mutation_authority": True,
        "read_only": True,
        "state_mutation": False,
        "event_reduction": False,
        "fact_admission": False,
        "real_state_store_connected": False,
        "downstream_dispatch": False,
        "read_semantics_changed": False,
        "runtime_semantics_changed": False,
        "candidate_only": True,
    }

    checks: List[Dict[str, Any]] = [
        _check(1, "closure artifacts exist", DOC_PATH.exists() and RECORD_PATH.exists()),
        _check(2, "closure identity correct", record.get("capability_id") == CAPABILITY_ID),
        _check(3, "closure is candidate only", record.get("closure_status") == "final_closure_candidate"),
        _check(4, "agent stop status correct", record.get("agent_stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION"),
        _check(5, "five-stage evidence complete", evidence_complete),
        _check(6, "promotion evidence passed", promotion.get("passed_checks") == promotion.get("total_checks") == 30 and promotion.get("failed_checks") == 0),
        _check(7, "promotion candidate preserved", statuses.get("promotion") == "promotion_candidate" and eligibility.get("recommended_promotion_status") == "promotion_candidate"),
        _check(8, "baseline freeze candidate preserved", statuses.get("baseline_freeze") == "baseline_freeze_candidate" and freeze.get("freeze_candidate") is True),
        _check(9, "governance candidate preserved", statuses.get("governance_admission") == "governance_admission_candidate" and admission.get("review_status") == "governance_admission_candidate"),
        _check(10, "lifecycle closure candidate only", statuses.get("lifecycle_closure") == "lifecycle_closure_candidate" and handoffs.get("lifecycle_closure", {}).get("formal_lifecycle_modified") is False),
        _check(11, "no production status", statuses.get("production") is False and eligibility.get("production_status") is False),
        _check(12, "no formal L1 admission", statuses.get("formal_l1_admission_executed") is False and admission.get("formal_l1_admission_executed") is False),
        _check(13, "baseline handoff candidate only", handoffs.get("baseline_freeze", {}).get("status") == "candidate_only"),
        _check(14, "active baseline unchanged", handoffs.get("baseline_freeze", {}).get("active_baseline_modified") is False),
        _check(15, "baseline excluded from normal runtime", handoffs.get("baseline_freeze", {}).get("normal_runtime_load_allowed") is False),
        _check(16, "formal registry unchanged", handoffs.get("lifecycle_closure", {}).get("formal_registry_modified") is False),
        _check(17, "rule counts preserved", handoffs.get("governance_admission", {}).get("l1_candidate_count") == 8 and handoffs.get("governance_admission", {}).get("module_rule_count") == 10),
        _check(18, "read-only boundaries preserved", boundaries == expected_boundaries),
        _check(19, "manifest authority remains read only", manifest.get("authority") == "read_only" and manifest.get("mutation_authority") is False),
        _check(20, "closure document disclaims GO", "does not declare GO" in doc and "WAITING_FOR_USER_TERMINAL_VERIFICATION" in doc),
    ]
    failed_items = [item for item in checks if not item["passed"]]
    output = {
        "module": CAPABILITY_ID,
        "runner": RUNNER,
        "total_checks": len(checks),
        "passed_checks": len(checks) - len(failed_items),
        "failed_checks": len(failed_items),
        "failed_items": failed_items,
        "boundary_preserved": boundaries == expected_boundaries,
        "production_activated": False,
        "formal_l1_admission_executed": False,
        "formal_lifecycle_modified": False,
        "final_decision_candidate": "READY_FOR_USER_TERMINAL_VERIFICATION" if not failed_items else "BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION",
        "checks": checks,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["failed_checks"] == 0 else 2)
