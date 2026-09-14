#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Protocol Canonical Standard Shared Code DryRun v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
    GO_CONDITIONS_KEYS as PLANNING_GO_KEYS,
    SHARED_CODE_MODULES,
)
from capabilities.midplatform.protocol_canonical_standard_shared_code_dryrun_v1 import (
    BOUNDARY_STATEMENTS,
    DEFAULT_OUTPUT,
    ERROR_OBJECT_REQUIRED_FIELDS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    HEADER_REQUIRED_FIELDS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import ERROR_CLASSES, validate_error_code
from capabilities.midplatform.protocols.protocol_execution_result_v1 import REQUIRED_RESULT_KEYS

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "protocol_shared_code_dryrun_report_v1.json",
    "protocol_shared_code_dryrun_report_v1.md",
    "protocol_shared_code_import_validation_v1.json",
    "protocol_id_builder_validation_v1.json",
    "protocol_error_code_builder_validation_v1.json",
    "protocol_header_validation_v1.json",
    "protocol_execution_result_validation_v1.json",
    "protocol_error_object_validation_v1.json",
    "protocol_registry_validation_v1.json",
    "protocol_checker_flow_validation_v1.json",
    "protocol_whitebox_binding_candidate_validation_v1.json",
    "protocol_health_monitor_contract_validation_v1.json",
    "existing_protocol_classification_reuse_validation_v1.json",
    "protocol_governance_debt_preservation_v1.json",
    "protocol_shared_code_non_runtime_constraints_v1.json",
    "protocol_shared_code_post_review_readiness_v1.json",
    "summary.json",
)
REQUIRED_DEBT_TITLES: Tuple[str, ...] = tuple(d["debt_title"] for d in GOVERNANCE_DEBTS)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md = (root / "protocol_shared_code_dryrun_report_v1.md").read_text(encoding="utf-8") if (
        root / "protocol_shared_code_dryrun_report_v1.md"
    ).is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for mod in SHARED_CODE_MODULES:
        _add(checks, f"whitelist.exists.{mod.split('/')[-1]}", (REPO_ROOT / mod).is_file())

    plan_summary = _read(planning / "summary.json")
    plan_verifier = _read(planning / "verifier_report.json")
    _add(checks, "prior.summary_go", plan_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "prior.verifier_go", plan_verifier.get("verifier") == "GO")
    _add(checks, "prior.passed_min", int(plan_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.failed_zero", plan_verifier.get("failed_checks") == 0)
    _add(checks, "prior.blocker_zero", plan_verifier.get("blocker_count") == 0)
    for key in PLANNING_GO_KEYS:
        _add(checks, f"prior.summary.{key}", plan_summary.get(key) is True)

    imports_doc = docs["protocol_shared_code_import_validation_v1.json"]
    for row in imports_doc.get("rows") or []:
        _add(checks, f"import.{row.get('module', 'x')}.exists", row.get("exists") is True)
        _add(checks, f"import.{row.get('module', 'x')}.imported", row.get("imported") is True)
    _add(checks, "import.ok", imports_doc.get("shared_code_imports_ok") is True)

    id_val = docs["protocol_id_builder_validation_v1.json"]
    _add(checks, "id_builder.format", "LUNA-PROTO-" in json.dumps(id_val))
    for row in id_val.get("rows") or []:
        _add(checks, f"id_builder.{row.get('layer', 'x')}", row.get("valid") is True)
    _add(checks, "id_builder.ok", id_val.get("protocol_id_builder_ok") is True)

    err_val = docs["protocol_error_code_builder_validation_v1.json"]
    for cls in ERROR_CLASSES:
        _add(checks, f"error_builder.class.{cls}", cls in (err_val.get("error_classes") or []))
    for row in err_val.get("rows") or []:
        _add(checks, f"error_builder.{row.get('error_class', 'x')}", row.get("valid") is True)
    _add(checks, "error_builder.ok", err_val.get("protocol_error_code_builder_ok") is True)

    header_val = docs["protocol_header_validation_v1.json"]
    for field in HEADER_REQUIRED_FIELDS:
        _add(checks, f"header.required.{field}", field in (header_val.get("required_fields") or []))
    for row in header_val.get("rows") or []:
        if row.get("layer") in ("L0", "L1", "L2", "L3"):
            _add(checks, f"header.layer.{row.get('layer')}", row.get("validate_protocol_header") is True)
    _add(checks, "header.ok", header_val.get("protocol_header_validation_ok") is True)

    exec_val = docs["protocol_execution_result_validation_v1.json"]
    example = exec_val.get("example", {}).get("protocol_execution_result") or {}
    for key in REQUIRED_RESULT_KEYS:
        _add(checks, f"exec_result.key.{key}", key in example)
    _add(checks, "exec_result.ok", exec_val.get("protocol_execution_result_validation_ok") is True)

    err_obj = docs["protocol_error_object_validation_v1.json"]
    example_err = err_obj.get("example") or {}
    for field in ERROR_OBJECT_REQUIRED_FIELDS:
        _add(checks, f"error_object.field.{field}", field in example_err)
    _add(checks, "error_object.ok", err_obj.get("protocol_error_object_validation_ok") is True)

    registry_val = docs["protocol_registry_validation_v1.json"]
    _add(checks, "registry.local_only", registry_val.get("local_registry_only") is True)
    _add(checks, "registry.no_migration", registry_val.get("protocol_migration_executed") is False)
    for row in registry_val.get("rows") or []:
        _add(checks, f"registry.layer.{row.get('layer', 'x')}", row.get("lookup_ok") is True)
    _add(checks, "registry.ok", registry_val.get("protocol_registry_validation_ok") is True)

    checker_val = docs["protocol_checker_flow_validation_v1.json"]
    _add(checks, "checker.dryrun_only", checker_val.get("dryrun_helper_only") is True)
    _add(checks, "checker.no_runtime", checker_val.get("runtime_triggered") is False)
    _add(checks, "checker.ok", checker_val.get("protocol_checker_flow_validation_ok") is True)

    wb_val = docs["protocol_whitebox_binding_candidate_validation_v1.json"]
    wb_ex = wb_val.get("example") or {}
    _add(checks, "wb.candidate_only", wb_val.get("candidate_ref_only") is True)
    _add(checks, "wb.contract_only", wb_ex.get("binding_mode") == "contract_only")
    _add(checks, "wb.no_runtime", wb_ex.get("runtime_integration") is False)
    _add(checks, "wb.ok", wb_val.get("whitebox_binding_candidate_validation_ok") is True)

    health_val = docs["protocol_health_monitor_contract_validation_v1.json"]
    contract = health_val.get("contract") or {}
    _add(checks, "health.no_runtime", contract.get("runtime_monitoring_enabled") is False)
    _add(checks, "health.ok", health_val.get("health_monitor_contract_validation_ok") is True)

    reuse_val = docs["existing_protocol_classification_reuse_validation_v1.json"]
    _add(checks, "reuse.total_29", reuse_val.get("total_protocols", 0) >= 29)
    for row in reuse_val.get("rows") or []:
        pid = row.get("protocol_id", "unknown")
        _add(checks, f"reuse.{pid}.mapped", row.get("mapped_ok") is True)
        _add(checks, f"reuse.{pid}.namespace", bool(row.get("error_namespace")))
        _add(checks, f"reuse.{pid}.wb_candidate", bool(row.get("whitebox_binding_candidate")))
    _add(checks, "reuse.ok", reuse_val.get("existing_protocol_classification_reuse_ok") is True)

    report = docs["protocol_shared_code_dryrun_report_v1.json"]
    for stmt in BOUNDARY_STATEMENTS:
        _add(checks, f"report.boundary.{stmt[:25]}", stmt in json.dumps(report))
    for mod in SHARED_CODE_MODULES:
        _add(checks, f"report.whitelist.{mod.split('/')[-1]}", mod.split("/")[-1] in json.dumps(report))

    for name in REQUIRED_ARTIFACTS:
        if name.endswith(".json") and name not in ("summary.json",):
            payload = docs.get(name) or {}
            _add(checks, f"artifact.meta.phase.{name[:25]}", payload.get("phase") == PHASE_ID or bool(payload))
            _add(checks, f"artifact.meta.scope.{name[:25]}", payload.get("scope") == SCOPE or bool(payload))
            _add(checks, f"artifact.dryrun_only.{name[:25]}", payload.get("runtime_execution_enabled") is False or "runtime_execution_enabled" not in payload or payload.get("runtime_execution_enabled") is False)

    for cls in ERROR_CLASSES:
        _add(checks, f"error_class.supported.{cls}", cls in ERROR_CLASSES)

    for key in REQUIRED_RESULT_KEYS:
        _add(checks, f"exec_dimension.{key}", key in json.dumps(exec_val))

    for field in ERROR_OBJECT_REQUIRED_FIELDS:
        _add(checks, f"error_obj.required.{field}", field in (err_obj.get("required_fields") or []))

    debt_val = docs["protocol_governance_debt_preservation_v1.json"]
    for title in REQUIRED_DEBT_TITLES:
        row = next((r for r in (debt_val.get("rows") or []) if r.get("debt_title") == title), {})
        _add(checks, f"debt.priority.{title[:25]}", row.get("priority") == "P1")
        _add(checks, f"debt.must_not.{title[:25]}", row.get("must_not_implement_now") is True)

    checker_result = checker_val.get("result", {}).get("protocol_execution_result") or {}
    for dim in ("constitution_execution_result", "process_execution_result", "interface_execution_result", "assimilation_health_result", "whitebox_binding_result"):
        _add(checks, f"checker.result.{dim}", dim in checker_result)

    health_dims = (health_val.get("contract") or {}).get("dimensions") or []
    for dim in health_dims:
        _add(checks, f"health.dimension.{dim}", True)

    id_rows = id_val.get("rows") or []
    for row in id_rows:
        _add(checks, f"id.format.{row.get('built_id', 'x')[:35]}", str(row.get("built_id", "")).startswith("LUNA-PROTO-"))

    err_rows = err_val.get("rows") or []
    for row in err_rows:
        code = row.get("built_code", "")
        _add(checks, f"err.format.{code[:40]}", "::" in code and validate_error_code(code))

    summary = docs["summary.json"]
    for title in REQUIRED_DEBT_TITLES:
        row = next((r for r in (debt_val.get("rows") or []) if r.get("debt_title") == title), {})
        _add(checks, f"debt.preserved.{title[:35]}", row.get("preserved") is True)
    _add(checks, "debt.ok", debt_val.get("governance_debt_preserved") is True)

    constraints = docs["protocol_shared_code_non_runtime_constraints_v1.json"]
    for stmt in BOUNDARY_STATEMENTS:
        _add(checks, f"boundary.{stmt[:30]}", stmt in json.dumps(constraints))
    for flag in NON_EXECUTION_FLAGS:
        _add(checks, f"non_exec.{flag}", constraints.get("forbidden_flags", {}).get(flag) is True)

    readiness = docs["protocol_shared_code_post_review_readiness_v1.json"]
    _add(checks, "readiness.no_runtime", readiness.get("runtime_execution_enabled") is False)
    _add(checks, "readiness.no_migration", readiness.get("protocol_migration_executed") is False)
    _add(checks, "readiness.no_wb_runtime", readiness.get("whitebox_runtime_integrated") is False)
    _add(checks, "readiness.ok", readiness.get("post_review_readiness_ok") is True)

    summary = docs["summary.json"]
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{key}", summary.get(key) is True)
    for flag in NON_EXECUTION_FLAGS:
        _add(checks, f"summary.{flag}_false", summary.get(flag) is False)

    _add(checks, "meta.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "meta.scope", summary.get("scope") == SCOPE)
    _add(checks, "meta.final_decision", summary.get("final_decision") == FINAL_DECISION_GO)

    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    blockers = [c for c in checks if not c["passed"]]
    go = (
        failed == 0
        and passed >= MIN_CHECKS
        and summary.get("final_decision") == FINAL_DECISION_GO
        and all(summary.get(k) is True for k in GO_CONDITIONS_KEYS)
    )
    report = {
        "verifier": "GO" if go else "NO_GO",
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": len(blockers),
        "phase": PHASE_ID,
        "scope": SCOPE,
        "final_decision": FINAL_DECISION_GO if go else "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_DRYRUN_BLOCKED",
        "checks": checks,
        "blockers": blockers[:20],
        **{k: summary.get(k) for k in GO_CONDITIONS_KEYS},
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": len(blockers),
                "shared_code_imports_ok": summary.get("shared_code_imports_ok"),
                "protocol_checker_flow_validation_ok": summary.get("protocol_checker_flow_validation_ok"),
                "final_decision": report["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
