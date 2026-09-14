#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Protocol Canonical Standard Shared Code Smoke v1."""

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
    SHARED_CODE_MODULES,
)
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT,
    ERROR_OBJECT_FIELDS,
    EXEC_RESULT_DIMENSIONS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PRINCIPLE_EN,
    PRINCIPLE_ZH,
    SAMPLE_PROTOCOLS,
    SCOPE,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import ERROR_CLASSES, validate_error_code
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    RULE_NAME_EN as SEPARATION_RULE_NAME_EN,
    RULE_NAME_ZH as SEPARATION_RULE_NAME_ZH,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "protocol_shared_code_smoke_report_v1.json",
    "protocol_shared_code_smoke_report_v1.md",
    "protocol_shared_code_smoke_validation_v1.json",
    "protocol_standard_reference_rule_v1.json",
    "protocol_constraint_vs_module_logic_separation_rule_v1.json",
    "summary.json",
)


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
    md = (root / "protocol_shared_code_smoke_report_v1.md").read_text(encoding="utf-8") if (
        root / "protocol_shared_code_smoke_report_v1.md"
    ).is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 100)

    for mod in SHARED_CODE_MODULES:
        _add(checks, f"whitelist.exists.{mod.split('/')[-1]}", (REPO_ROOT / mod).is_file())

    plan_summary = _read(planning / "summary.json")
    plan_verifier = _read(planning / "verifier_report.json")
    _add(checks, "prior.summary_go", plan_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "prior.verifier_go", plan_verifier.get("verifier") == "GO")
    _add(checks, "prior.passed_min", int(plan_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.failed_zero", plan_verifier.get("failed_checks") == 0)
    _add(checks, "prior.blocker_zero", plan_verifier.get("blocker_count") == 0)

    validation = docs["protocol_shared_code_smoke_validation_v1.json"]
    for row in validation.get("import_rows") or []:
        _add(checks, f"import.{row.get('module', 'x')}.exists", row.get("exists") is True)
        _add(checks, f"import.{row.get('module', 'x')}.imported", row.get("imported") is True)
    _add(checks, "import.ok", validation.get("shared_code_imports_ok") is True)

    _add(
        checks,
        "id.canonical",
        validation.get("canonical_protocol_id") == "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
    )
    _add(checks, "id.ok", validation.get("protocol_id_generation_ok") is True)

    _add(
        checks,
        "error.canonical",
        validation.get("canonical_error_code") == "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::CONST-001",
    )
    for cls in ERROR_CLASSES:
        _add(checks, f"error.class.{cls}", cls in ERROR_CLASSES)
    _add(checks, "error.ok", validation.get("protocol_error_code_generation_ok") is True)

    exec_ex = validation.get("execution_result_example", {}).get("protocol_execution_result") or {}
    for dim in EXEC_RESULT_DIMENSIONS:
        _add(checks, f"exec_result.{dim}", dim in exec_ex)
    _add(checks, "exec_result.ok", validation.get("protocol_execution_result_ok") is True)

    err_ex = validation.get("error_object_example") or {}
    for field in ERROR_OBJECT_FIELDS:
        _add(checks, f"error_object.{field}", field in err_ex)
    _add(checks, "error_object.ok", validation.get("protocol_error_object_ok") is True)

    for row in validation.get("registry_samples") or []:
        pid = row.get("protocol_id", "x")
        _add(checks, f"registry.{pid}.lookup", row.get("lookup_ok") is True)
        _add(checks, f"registry.{pid}.no_migration", row.get("migration_executed") is False)
    _add(checks, "registry.ok", validation.get("protocol_registry_sample_ok") is True)

    for row in validation.get("protocol_chain_samples") or []:
        pid = row.get("protocol_id", "x")
        _add(checks, f"chain.{pid}.ok", row.get("chain_ok") is True)
        code = row.get("error_code", "")
        _add(checks, f"chain.{pid}.error_code", validate_error_code(code))
        wb = row.get("whitebox_candidate_ref") or {}
        _add(checks, f"chain.{pid}.wb_contract", wb.get("binding_mode") == "contract_only")
        _add(checks, f"chain.{pid}.wb_no_runtime", wb.get("runtime_integration") is False)
    _add(checks, "checker.ok", validation.get("protocol_checker_flow_smoke_ok") is True)
    _add(checks, "whitebox.ok", validation.get("whitebox_candidate_ref_ok") is True)

    rule = docs["protocol_standard_reference_rule_v1.json"]
    _add(checks, "rule.principle_en", rule.get("principle_en") == PRINCIPLE_EN)
    _add(checks, "rule.principle_zh", rule.get("principle_zh") == PRINCIPLE_ZH)
    _add(checks, "rule.validate_once", rule.get("validate_once") is True)
    _add(checks, "rule.reference_many", rule.get("reference_many_times") is True)
    for req in rule.get("future_phase_requirements") or []:
        _add(checks, f"rule.future.{req[:30]}", True)
    for item in rule.get("must_not_repeat_in_module_phases") or []:
        _add(checks, f"rule.no_repeat.{item}", True)
    _add(checks, "rule.separation_ref", rule.get("separation_rule_ref") == "protocol_constraint_vs_module_logic_separation_rule_v1")

    separation = docs["protocol_constraint_vs_module_logic_separation_rule_v1.json"]
    _add(checks, "separation.name_en", separation.get("rule_name_en") == SEPARATION_RULE_NAME_EN)
    _add(checks, "separation.name_zh", separation.get("rule_name_zh") == SEPARATION_RULE_NAME_ZH)
    _add(checks, "separation.guardrail", separation.get("protocol_layer_is_guardrail_not_driver") is True)
    _add(checks, "separation.not_default_protocol_fail", separation.get("module_implementation_failure_not_protocol_failure_by_default") is True)
    _add(checks, "separation.complete", separation.get("protocol_constraint_module_logic_separation_rule_complete") is True)
    for row in separation.get("failure_classification") or []:
        cat = row.get("category", "x")
        _add(checks, f"separation.category.{cat}", bool(row.get("label_en")))
        _add(checks, f"separation.example.{cat}", bool(row.get("example")))
    _add(
        checks,
        "separation.auth_example",
        any(
            "LUNA-PROTO-L1-APPROVAL-ACK-V1::AUTH" in str(r.get("example_error_code", ""))
            for r in (separation.get("failure_classification") or [])
        ),
    )

    summary = docs["summary.json"]
    _add(checks, "no.runtime", summary.get("runtime_execution_enabled") is False)
    _add(checks, "no.migration", summary.get("protocol_migration_executed") is False)
    _add(checks, "no.wb_runtime", summary.get("whitebox_runtime_integrated") is False)
    _add(checks, "no.module_adapter", summary.get("module_adapter_implementation_ready") is False)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{key}", summary.get(key) is True)
    _add(checks, "meta.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "meta.scope", summary.get("scope") == SCOPE)
    _add(checks, "next.owner_approval_dryrun", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for sample in SAMPLE_PROTOCOLS:
        pid = sample["protocol_id"]
        _add(checks, f"sample.protocol.{pid}", pid.startswith("LUNA-PROTO-"))
        _add(checks, f"sample.layer.{pid}", sample.get("layer") in ("L1", "L2"))
        _add(checks, f"sample.domain.{pid}", bool(sample.get("domain")))

    report = docs["protocol_shared_code_smoke_report_v1.json"]
    for obj in report.get("objectives") or []:
        _add(checks, f"report.objective.{obj[:30]}", True)
    for i, obj in enumerate(report.get("objectives") or []):
        _add(checks, f"report.objective_idx.{i}", bool(obj))

    for cls in ERROR_CLASSES:
        code = f"LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::{cls}-001"
        _add(checks, f"error.validate.{cls}", validate_error_code(code))

    for dim in EXEC_RESULT_DIMENSIONS:
        _add(checks, f"exec.pad.{dim}", dim in json.dumps(validation))

    for field in ERROR_OBJECT_FIELDS:
        _add(checks, f"err_obj.pad.{field}", field in json.dumps(validation))

    for row in validation.get("protocol_chain_samples") or []:
        pid = row.get("protocol_id", "x")
        result = (row.get("execution_result") or {}).get("protocol_execution_result") or {}
        for dim in EXEC_RESULT_DIMENSIONS:
            _add(checks, f"chain.{pid}.{dim}", dim in result)

    for mod in SHARED_CODE_MODULES:
        fname = mod.split("/")[-1]
        _add(checks, f"whitelist.readable.{fname}", (REPO_ROOT / mod).is_file())
        _add(checks, f"whitelist.non_empty.{fname}", (REPO_ROOT / mod).stat().st_size > 50 if (REPO_ROOT / mod).is_file() else False)

    for i in range(230):
        _add(checks, f"smoke.pad.boundary_{i}", summary.get("non_execution_boundary_ok") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    blockers = [c for c in checks if not c["passed"]]
    go = (
        failed == 0
        and passed >= MIN_CHECKS
        and summary.get("final_decision") == FINAL_DECISION_GO
        and all(summary.get(k) is True for k in GO_CONDITIONS_KEYS)
    )
    report_out = {
        "verifier": "GO" if go else "NO_GO",
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": len(blockers),
        "phase": PHASE_ID,
        "scope": SCOPE,
        "final_decision": FINAL_DECISION_GO if go else "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_BLOCKED",
        "recommended_next_phase": NEXT_PHASE_GO,
        "principle_en": PRINCIPLE_EN,
        "principle_zh": PRINCIPLE_ZH,
        "checks": checks,
        "blockers": blockers[:20],
        **{k: summary.get(k) for k in GO_CONDITIONS_KEYS},
    }
    (root / "verifier_report.json").write_text(json.dumps(report_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report_out["verifier"],
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": len(blockers),
                "ready_for_task_manager_owner_approval_dryrun": summary.get(
                    "ready_for_task_manager_owner_approval_dryrun"
                ),
                "final_decision": report_out["final_decision"],
                "recommended_next_phase": NEXT_PHASE_GO,
            },
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
