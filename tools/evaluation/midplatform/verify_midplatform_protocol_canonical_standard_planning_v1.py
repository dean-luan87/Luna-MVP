#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Protocol Canonical Standard Planning v1."""

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
    BOUNDARY_CONTRACT_STATEMENTS,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    GOVERNANCE_DEBTS,
    L1_PROTOCOLS,
    L2_FUTURE_MODULE_PROTOCOLS,
    L2_TASK_MANAGER_PROTOCOLS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_PRIMARY,
    NON_EXECUTION_FLAGS,
    NUMBERING_FORMAT,
    PHASE_ID,
    SCOPE,
    SHARED_CODE_MODULES,
    STANDARD_API_FUNCTIONS,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import ERROR_CLASSES

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "protocol_canonical_standard_plan_v1.json",
    "protocol_canonical_standard_plan_v1.md",
    "protocol_numbering_standard_v1.json",
    "protocol_error_code_standard_v1.json",
    "protocol_execution_result_schema_v1.json",
    "constitution_process_interface_assimilation_error_taxonomy_v1.json",
    "whitebox_diagnostic_binding_contract_v1.json",
    "protocol_first_development_rule_v1.json",
    "module_internal_vs_cross_module_protocol_layering_v1.json",
    "protocol_assimilation_supervision_standard_v1.json",
    "protocol_failure_handling_notification_standard_v1.json",
    "protocol_shared_code_design_v1.json",
    "protocol_shared_checker_flow_v1.json",
    "protocol_standard_api_contract_v1.json",
    "protocol_standard_verifier_contract_v1.json",
    "protocol_error_object_schema_v1.json",
    "protocol_health_monitor_contract_v1.json",
    "protocol_template_reuse_contract_v1.json",
    "existing_protocol_classification_registry_v1.json",
    "existing_protocol_layer_mapping_v1.json",
    "existing_protocol_error_namespace_mapping_v1.json",
    "existing_protocol_whitebox_binding_candidate_map_v1.json",
    "existing_protocol_governance_debt_update_v1.json",
    "summary.json",
)
REQUIRED_DEBT_TITLES: Tuple[str, ...] = tuple(d["debt_title"] for d in GOVERNANCE_DEBTS)
RESULT_DIMENSIONS: Tuple[str, ...] = (
    "constitution_execution_result",
    "process_execution_result",
    "interface_execution_result",
    "assimilation_health_result",
    "whitebox_binding_result",
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
    args = parser.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "protocol_canonical_standard_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for mod in SHARED_CODE_MODULES:
        _add(checks, f"shared_code.exists.{mod.split('/')[-1]}", (REPO_ROOT / mod).is_file())

    numbering = docs["protocol_numbering_standard_v1.json"]
    _add(checks, "numbering.format", NUMBERING_FORMAT in str(numbering.get("format", "")))
    _add(checks, "numbering.luna_proto_prefix", "LUNA-PROTO-" in json.dumps(numbering))
    _add(checks, "numbering.complete", numbering.get("protocol_numbering_standard_complete") is True)
    for ex in numbering.get("examples") or []:
        _add(checks, f"numbering.example.{ex}", ex.startswith("LUNA-PROTO-"))

    error_std = docs["protocol_error_code_standard_v1.json"]
    for cls in ERROR_CLASSES:
        _add(checks, f"error_code.class.{cls}", cls in (error_std.get("error_classes") or []))
    _add(checks, "error_code.complete", error_std.get("protocol_error_code_standard_complete") is True)

    result_schema = docs["protocol_execution_result_schema_v1.json"]
    for dim in RESULT_DIMENSIONS:
        _add(checks, f"result_schema.dimension.{dim}", dim in json.dumps(result_schema))
    _add(
        checks,
        "result_schema.complete",
        result_schema.get("protocol_execution_result_schema_complete") is True,
    )

    taxonomy = docs["constitution_process_interface_assimilation_error_taxonomy_v1.json"]
    _add(checks, "taxonomy.complete", taxonomy.get("error_taxonomy_complete") is True)
    _add(checks, "taxonomy.L0", bool(taxonomy.get("layers", {}).get("L0")))
    _add(checks, "taxonomy.L1", bool(taxonomy.get("layers", {}).get("L1")))

    whitebox = docs["whitebox_diagnostic_binding_contract_v1.json"]
    _add(checks, "whitebox.contract_only", whitebox.get("binding_mode") == "contract_only")
    _add(
        checks,
        "whitebox.not_runtime_integration",
        whitebox.get("whitebox_runtime_integration") is False,
    )
    _add(
        checks,
        "whitebox.complete",
        whitebox.get("whitebox_diagnostic_binding_contract_complete") is True,
    )

    layering = docs["module_internal_vs_cross_module_protocol_layering_v1.json"]
    _add(checks, "layering.L1_cross_module", bool(layering.get("L1_cross_module")))
    _add(checks, "layering.L2_module_internal", bool(layering.get("L2_module_internal")))
    _add(checks, "layering.complete", layering.get("module_protocol_layering_complete") is True)

    assimilation = docs["protocol_assimilation_supervision_standard_v1.json"]
    for dim in ("health", "drift", "fallback", "quarantine", "notification"):
        _add(checks, f"assimilation.dimension.{dim}", dim in (assimilation.get("dimensions") or []))
    _add(
        checks,
        "assimilation.complete",
        assimilation.get("protocol_assimilation_supervision_standard_complete") is True,
    )

    shared_design = docs["protocol_shared_code_design_v1.json"]
    _add(checks, "shared_design.modules", bool(shared_design.get("modules")))
    _add(checks, "shared_design.complete", shared_design.get("shared_protocol_code_design_complete") is True)

    checker_flow = docs["protocol_shared_checker_flow_v1.json"]
    _add(checks, "checker_flow.steps", bool(checker_flow.get("steps")))
    _add(checks, "checker_flow.complete", checker_flow.get("standard_checker_flow_complete") is True)

    api_contract = docs["protocol_standard_api_contract_v1.json"]
    for fn in STANDARD_API_FUNCTIONS:
        _add(checks, f"api_contract.fn.{fn}", fn in json.dumps(api_contract))

    verifier_contract = docs["protocol_standard_verifier_contract_v1.json"]
    _add(
        checks,
        "verifier_contract.reuse_helpers",
        "shared_protocol_helpers" in json.dumps(verifier_contract)
        or "reuse" in json.dumps(verifier_contract).lower(),
    )
    _add(
        checks,
        "verifier_contract.complete",
        verifier_contract.get("standard_verifier_contract_complete") is True,
    )

    registry = docs["existing_protocol_classification_registry_v1.json"]
    _add(checks, "registry.L1", len(registry.get("L1_system_protocols") or []) >= len(L1_PROTOCOLS))
    _add(
        checks,
        "registry.L2_task_manager",
        len(registry.get("L2_task_manager_protocols") or []) >= len(L2_TASK_MANAGER_PROTOCOLS),
    )
    _add(
        checks,
        "registry.L2_future",
        len(registry.get("L2_future_module_protocols") or []) >= len(L2_FUTURE_MODULE_PROTOCOLS),
    )
    _add(
        checks,
        "registry.complete",
        registry.get("existing_protocol_classification_complete") is True,
    )

    error_ns = docs["existing_protocol_error_namespace_mapping_v1.json"]
    entries = error_ns.get("entries") or []
    _add(checks, "error_ns.entries", len(entries) >= 29)
    for entry in entries:
        _add(
            checks,
            f"error_ns.{entry.get('protocol_id', 'unknown')}",
            bool(entry.get("error_namespace")),
        )

    wb_map = docs["existing_protocol_whitebox_binding_candidate_map_v1.json"]
    wb_entries = wb_map.get("entries") or []
    _add(checks, "wb_map.entries", len(wb_entries) >= 29)
    for entry in wb_entries:
        _add(
            checks,
            f"wb_map.{entry.get('protocol_id', 'unknown')}",
            entry.get("whitebox_binding_required") is True
            and entry.get("runtime_integration") is False,
        )

    debt_update = docs["existing_protocol_governance_debt_update_v1.json"]
    debts = debt_update.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 6)
    for title in REQUIRED_DEBT_TITLES:
        match = next((d for d in debts if d.get("debt_title") == title), {})
        _add(checks, f"debt.exists.{title[:40]}", bool(match))
        _add(checks, f"debt.priority.{title[:30]}", match.get("priority") == "P1")
        _add(
            checks,
            f"debt.classification.{title[:30]}",
            match.get("classification") == "L1 Midplatform System Protocols",
        )
        _add(checks, f"debt.must_not.{title[:30]}", match.get("must_not_implement_now") is True)

    first_rule = docs["protocol_first_development_rule_v1.json"]
    _add(checks, "first_rule.protocol_before_module", "protocol_before_module" in json.dumps(first_rule))
    _add(
        checks,
        "first_rule.complete",
        first_rule.get("protocol_first_development_rule_complete") is True,
    )

    plan = docs["protocol_canonical_standard_plan_v1.json"]
    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.plan.{stmt[:30]}", stmt in json.dumps(plan))

    all_registry_entries = (
        (registry.get("L1_system_protocols") or [])
        + (registry.get("L2_task_manager_protocols") or [])
        + (registry.get("L2_future_module_protocols") or [])
    )
    for entry in all_registry_entries:
        pid = entry.get("suggested_protocol_id", "unknown")
        _add(checks, f"registry.entry.{pid}.name", bool(entry.get("protocol_name")))
        _add(checks, f"registry.entry.{pid}.layer", entry.get("layer") in ("L1", "L2"))
        _add(checks, f"registry.entry.{pid}.domain", bool(entry.get("domain")))
        _add(checks, f"registry.entry.{pid}.status", bool(entry.get("status")))
        _add(checks, f"registry.entry.{pid}.canonical", entry.get("canonical_required") is True)
        _add(checks, f"registry.entry.{pid}.whitebox", entry.get("whitebox_binding_required") is True)
        _add(checks, f"registry.entry.{pid}.must_not", entry.get("must_not_implement_now") is True)
        _add(checks, f"registry.entry.{pid}.id_format", str(pid).startswith("LUNA-PROTO-"))

    for proto in L1_PROTOCOLS:
        _add(checks, f"L1.protocol.{proto['name'][:30]}", proto["name"] in json.dumps(registry))
    for name in L2_TASK_MANAGER_PROTOCOLS:
        _add(checks, f"L2.tm.{name[:30]}", name in json.dumps(registry))
    for name in L2_FUTURE_MODULE_PROTOCOLS:
        _add(checks, f"L2.future.{name[:30]}", name in json.dumps(registry))

    layer_map = docs["existing_protocol_layer_mapping_v1.json"]
    _add(checks, "layer_map.L0", bool(layer_map.get("L0")))
    _add(checks, "layer_map.L1", bool(layer_map.get("L1")))
    _add(checks, "layer_map.L2_tm", bool(layer_map.get("L2_task_manager")))
    _add(checks, "layer_map.L2_future", bool(layer_map.get("L2_future")))
    _add(checks, "layer_map.L3", bool(layer_map.get("L3")))

    error_obj = docs["protocol_error_object_schema_v1.json"]
    example = error_obj.get("example") or {}
    for field in (
        "error_code",
        "error_class",
        "severity",
        "detected_by",
        "phase_id",
        "artifact_ref",
        "field_path",
        "whitebox_trace_ref",
        "diagnostic_node_ref",
        "recommended_action",
        "notification_required",
        "owner_operator_notification_required",
    ):
        _add(checks, f"error_object.field.{field}", field in example)

    health = docs["protocol_health_monitor_contract_v1.json"]
    for dim in health.get("dimensions") or []:
        _add(checks, f"health.dimension.{dim}", True)
    _add(checks, "health.runtime_disabled", health.get("runtime_monitoring_enabled") is False)

    failure = docs["protocol_failure_handling_notification_standard_v1.json"]
    _add(checks, "failure.notification_blocker", failure.get("notification_required_on_blocker") is True)
    _add(
        checks,
        "failure.owner_operator_const",
        failure.get("owner_operator_notification_required_on_constitutional_violation") is True,
    )

    template_reuse = docs["protocol_template_reuse_contract_v1.json"]
    _add(checks, "template_reuse.no_full_scan", template_reuse.get("full_repo_scan_allowed") is False)

    for step in checker_flow.get("steps") or []:
        _add(checks, f"checker_flow.step.{step}", True)

    for ex in error_std.get("examples") or []:
        _add(checks, f"error_example.{ex.get('error_code', 'x')[:40]}", "::" in str(ex.get("error_code", "")))

    for debt in debts:
        did = debt.get("debt_id", "unknown")
        _add(checks, f"debt.field.{did}.id", bool(debt.get("debt_id")))
        _add(checks, f"debt.field.{did}.type", bool(debt.get("debt_type")))
        _add(checks, f"debt.field.{did}.risk", bool(debt.get("risk")))
        _add(checks, f"debt.field.{did}.future_phase", bool(debt.get("required_future_phase")))

    for name in REQUIRED_ARTIFACTS:
        if name.endswith(".json") and name != "summary.json":
            payload = docs.get(name) or {}
            _add(checks, f"artifact.phase.{name[:30]}", payload.get("phase") == PHASE_ID or "phase" in payload or bool(payload))
            _add(checks, f"artifact.scope.{name[:30]}", payload.get("scope") == SCOPE or "scope" in payload or bool(payload))

    summary = docs["summary.json"]
    for flag in NON_EXECUTION_FLAGS:
        _add(checks, f"non_execution.{flag}_false", summary.get(flag) is False)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{key}", summary.get(key) is True)

    _add(checks, "meta.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "meta.scope", summary.get("scope") == SCOPE)
    _add(checks, "next_phase.primary", summary.get("recommended_next_phase_primary") == NEXT_PHASE_PRIMARY)
    _add(checks, "next_phase.alt", summary.get("recommended_next_phase_alt") == NEXT_PHASE_ALT)

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
        "final_decision": FINAL_DECISION_GO if go else "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_PLANNING_BLOCKED",
        "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
        "recommended_next_phase_alt": NEXT_PHASE_ALT,
        "checks": checks,
        "blockers": blockers[:20],
        **{k: summary.get(k) for k in GO_CONDITIONS_KEYS},
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": len(blockers),
                "protocol_canonical_standard_plan_complete": summary.get(
                    "protocol_canonical_standard_plan_complete"
                ),
                "existing_protocol_classification_complete": summary.get(
                    "existing_protocol_classification_complete"
                ),
                "final_decision": report["final_decision"],
                "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
            },
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
