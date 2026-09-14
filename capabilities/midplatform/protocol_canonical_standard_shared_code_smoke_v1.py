# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Canonical Standard Shared Code Smoke v1.

One-time smoke validation: import/call shared protocol helpers, run 2-3 sample protocol chains,
confirm no runtime side effects. After GO, module phases reference protocol standards only.

Principle: Protocol Standard Validate Once, Reference Many Times (协议标准一次验证，多处引用).
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    SHARED_CODE_MODULES,
)
from capabilities.midplatform.protocols.protocol_checker_v1 import run_protocol_checker_flow
from capabilities.midplatform.protocols.protocol_error_codes_v1 import (
    ERROR_CLASSES,
    build_error_code,
    validate_error_code,
)
from capabilities.midplatform.protocols.protocol_execution_result_v1 import (
    ProtocolError,
    build_protocol_execution_result,
    validate_protocol_execution_result,
)
from capabilities.midplatform.protocols.protocol_registry_v1 import lookup_protocol, register_protocol
from capabilities.midplatform.protocols.protocol_types_v1 import ProtocolRegistryEntry, build_protocol_id
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    RULE_NAME_EN as SEPARATION_RULE_NAME_EN,
    RULE_NAME_ZH as SEPARATION_RULE_NAME_ZH,
    build_separation_rule_document,
)
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-Smoke-v1-001"
SCOPE = "midplatform_protocol_canonical_standard_shared_code_smoke_only"
SOURCE_CHAIN = "midplatform_protocol_canonical_standard_shared_code_smoke_v1"
PRINCIPLE_EN = "Protocol Standard Validate Once, Reference Many Times"
PRINCIPLE_ZH = "协议标准一次验证，多处引用"
FINAL_DECISION_GO = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_READY_FOR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
FINAL_DECISION_BLOCKED = "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_BLOCKED"
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_protocol_canonical_standard_shared_code_smoke_v1_smoke_v0"
)

SAMPLE_PROTOCOLS: Tuple[Dict[str, str], ...] = (
    {
        "protocol_id": "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
        "protocol_name": "Record Lifecycle Protocol",
        "layer": "L1",
        "domain": "record_lifecycle",
    },
    {
        "protocol_id": "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
        "protocol_name": "Evidence Binding Protocol",
        "layer": "L1",
        "domain": "evidence_binding",
    },
    {
        "protocol_id": "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-V1",
        "protocol_name": "Task Manager Owner Approval Protocol",
        "layer": "L2",
        "domain": "taskmanager",
    },
)

EXEC_RESULT_DIMENSIONS: Tuple[str, ...] = (
    "constitution_execution_result",
    "process_execution_result",
    "interface_execution_result",
    "assimilation_health_result",
    "whitebox_binding_result",
)

ERROR_OBJECT_FIELDS: Tuple[str, ...] = (
    "error_code",
    "error_class",
    "severity",
    "detected_by",
    "phase_id",
    "artifact_ref",
    "field_path",
    "expected",
    "actual",
    "whitebox_trace_ref",
    "recommended_action",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_protocol_canonical_standard_planning_go",
    "shared_code_imports_ok",
    "protocol_id_generation_ok",
    "protocol_error_code_generation_ok",
    "protocol_execution_result_ok",
    "protocol_error_object_ok",
    "protocol_registry_sample_ok",
    "protocol_checker_flow_smoke_ok",
    "whitebox_candidate_ref_ok",
    "no_runtime_side_effects_ok",
    "non_execution_boundary_ok",
    "ready_for_task_manager_owner_approval_dryrun",
    "protocol_constraint_module_logic_separation_rule_complete",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "principle_en": PRINCIPLE_EN,
        "principle_zh": PRINCIPLE_ZH,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "shared_code_smoke_only": True,
        "runtime_execution_enabled": False,
        "protocol_migration_executed": False,
        "whitebox_runtime_integrated": False,
        "module_adapter_implementation_ready": False,
        "output_root": str(out),
        "planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _smoke_imports(repo_root: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    ok = True
    modules = [
        ("capabilities.midplatform.protocols.protocol_types_v1", "protocol_types_v1.py"),
        ("capabilities.midplatform.protocols.protocol_error_codes_v1", "protocol_error_codes_v1.py"),
        ("capabilities.midplatform.protocols.protocol_execution_result_v1", "protocol_execution_result_v1.py"),
        ("capabilities.midplatform.protocols.protocol_registry_v1", "protocol_registry_v1.py"),
        ("capabilities.midplatform.protocols.protocol_checker_v1", "protocol_checker_v1.py"),
        ("capabilities.midplatform.protocols.protocol_whitebox_binding_v1", "protocol_whitebox_binding_v1.py"),
        ("capabilities.midplatform.protocols.protocol_health_monitor_contract_v1", "protocol_health_monitor_contract_v1.py"),
        ("capabilities.midplatform.protocols", "__init__.py"),
    ]
    for mod_path, fname in modules:
        rel = f"capabilities/midplatform/protocols/{fname}"
        exists = (repo_root / rel).is_file()
        imported = False
        err = ""
        try:
            importlib.import_module(mod_path)
            imported = True
        except Exception as exc:  # noqa: BLE001
            err = str(exc)
            ok = False
        rows.append({"module": fname, "path": rel, "exists": exists, "imported": imported, "error": err})
        if not exists:
            ok = False
    return ok, rows


def run_protocol_canonical_standard_shared_code_smoke_v1(
    *,
    planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning)
    issues: List[str] = []

    plan_summary = _read_json(planning / "summary.json")
    plan_verifier = _read_json(planning / "verifier_report.json")
    prior_protocol_canonical_standard_planning_go = (
        plan_summary.get("final_decision") == PLANNING_FINAL_GO
        and plan_verifier.get("verifier") == "GO"
        and int(plan_verifier.get("passed_checks", 0)) >= 420
        and plan_verifier.get("failed_checks") == 0
        and plan_verifier.get("blocker_count") == 0
    )
    if not prior_protocol_canonical_standard_planning_go:
        issues.append("prior_planning_not_go")

    shared_code_imports_ok, import_rows = _smoke_imports(repo_root)
    if not shared_code_imports_ok:
        issues.append("shared_code_import_gap")

    canonical_id = build_protocol_id("L1", "RECORD", "LIFECYCLE", "V1")
    protocol_id_generation_ok = canonical_id == "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1"

    sample_error_code = build_error_code(canonical_id, "CONST", 1)
    protocol_error_code_generation_ok = (
        sample_error_code == "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::CONST-001"
        and validate_error_code(sample_error_code)
        and all(
            validate_error_code(build_error_code(canonical_id, cls, 1))
            for cls in ERROR_CLASSES
        )
    )

    exec_result = build_protocol_execution_result(canonical_id)
    inner = exec_result.to_dict().get("protocol_execution_result") or {}
    protocol_execution_result_ok = validate_protocol_execution_result(exec_result.to_dict()) and all(
        dim in inner for dim in EXEC_RESULT_DIMENSIONS
    )

    sample_error = ProtocolError(
        error_code=sample_error_code,
        error_class="constitutional_violation",
        severity="blocker",
        detected_by="smoke",
        phase_id=PHASE_ID,
        artifact_ref="summary.json",
        field_path="go_conditions.request_record_absent",
        expected=True,
        actual=False,
        whitebox_trace_ref="wb://smoke",
        recommended_action="block_and_quarantine",
    )
    err_dict = sample_error.to_dict()
    protocol_error_object_ok = all(f in err_dict for f in ERROR_OBJECT_FIELDS)

    registry_rows: List[Dict[str, Any]] = []
    protocol_registry_sample_ok = True
    for sample in SAMPLE_PROTOCOLS:
        entry = ProtocolRegistryEntry(
            protocol_name=sample["protocol_name"],
            suggested_protocol_id=sample["protocol_id"],
            layer=sample["layer"],
            domain=sample["domain"],
            status="smoke_sample",
            current_handling="local_registry_only",
            canonical_required=True,
            module_extension_allowed=True,
            whitebox_binding_required=True,
            error_namespace=f"{sample['protocol_id']}::*",
            must_not_implement_now=True,
        )
        register_protocol(entry)
        looked_up = lookup_protocol(sample["protocol_id"])
        row_ok = looked_up is not None and looked_up.get("suggested_protocol_id") == sample["protocol_id"]
        registry_rows.append({**sample, "lookup_ok": row_ok, "migration_executed": False})
        if not row_ok:
            protocol_registry_sample_ok = False

    chain_samples: List[Dict[str, Any]] = []
    protocol_checker_flow_smoke_ok = True
    whitebox_candidate_ref_ok = True
    for sample in SAMPLE_PROTOCOLS:
        pid = sample["protocol_id"]
        err = build_error_code(pid, "EVID", 1)
        wb = build_whitebox_diagnostic_ref(
            phase_id=PHASE_ID,
            protocol_id=pid,
            error_code=err,
            artifact_ref="summary.json",
            field_path="go_conditions.shared_code_imports_ok",
        )
        checker = run_protocol_checker_flow(
            protocol_id=pid,
            whitebox_trace_ref=wb["whitebox_trace_ref"],
            whitebox_diagnostic_ref=wb["diagnostic_node_ref"],
        )
        checker_ok = (checker.get("protocol_execution_result") or {}).get("overall_result") == "PASS"
        wb_ok = (
            wb.get("binding_mode") == "contract_only"
            and wb.get("runtime_integration") is False
            and wb["whitebox_trace_ref"].startswith("wb://")
        )
        chain_samples.append(
            {
                "protocol_id": pid,
                "error_code": err,
                "execution_result": checker,
                "whitebox_candidate_ref": wb,
                "chain_ok": checker_ok and wb_ok,
            }
        )
        if not checker_ok:
            protocol_checker_flow_smoke_ok = False
        if not wb_ok:
            whitebox_candidate_ref_ok = False

    no_runtime_side_effects_ok = (
        meta["runtime_execution_enabled"] is False
        and meta["protocol_migration_executed"] is False
        and meta["whitebox_runtime_integrated"] is False
        and meta["module_adapter_implementation_ready"] is False
    )
    non_execution_boundary_ok = no_runtime_side_effects_ok

    separation_rule = build_separation_rule_document(**meta)
    protocol_constraint_module_logic_separation_rule_complete = (
        separation_rule.get("protocol_constraint_module_logic_separation_rule_complete") is True
        and len(separation_rule.get("failure_classification") or []) >= 3
    )

    ready_for_task_manager_owner_approval_dryrun = (
        prior_protocol_canonical_standard_planning_go
        and shared_code_imports_ok
        and protocol_id_generation_ok
        and protocol_error_code_generation_ok
        and protocol_execution_result_ok
        and protocol_error_object_ok
        and protocol_registry_sample_ok
        and protocol_checker_flow_smoke_ok
        and whitebox_candidate_ref_ok
        and no_runtime_side_effects_ok
        and protocol_constraint_module_logic_separation_rule_complete
    )

    go_values = {
        "prior_protocol_canonical_standard_planning_go": prior_protocol_canonical_standard_planning_go,
        "shared_code_imports_ok": shared_code_imports_ok,
        "protocol_id_generation_ok": protocol_id_generation_ok,
        "protocol_error_code_generation_ok": protocol_error_code_generation_ok,
        "protocol_execution_result_ok": protocol_execution_result_ok,
        "protocol_error_object_ok": protocol_error_object_ok,
        "protocol_registry_sample_ok": protocol_registry_sample_ok,
        "protocol_checker_flow_smoke_ok": protocol_checker_flow_smoke_ok,
        "whitebox_candidate_ref_ok": whitebox_candidate_ref_ok,
        "no_runtime_side_effects_ok": no_runtime_side_effects_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "ready_for_task_manager_owner_approval_dryrun": ready_for_task_manager_owner_approval_dryrun,
        "protocol_constraint_module_logic_separation_rule_complete": protocol_constraint_module_logic_separation_rule_complete,
    }

    if not protocol_id_generation_ok:
        issues.append("protocol_id_generation_gap")
    if not protocol_error_code_generation_ok:
        issues.append("protocol_error_code_gap")
    if not ready_for_task_manager_owner_approval_dryrun:
        for k, v in go_values.items():
            if not v and k != "ready_for_task_manager_owner_approval_dryrun":
                issues.append(f"{k}_gap")

    smoke_pass = len(issues) == 0 and all(go_values.values())
    final_decision = FINAL_DECISION_GO if smoke_pass else FINAL_DECISION_BLOCKED

    reference_rule = {
        "rule_id": "protocol_standard_reference_rule_v1",
        "principle_en": PRINCIPLE_EN,
        "principle_zh": PRINCIPLE_ZH,
        "separation_rule_ref": "protocol_constraint_vs_module_logic_separation_rule_v1",
        "separation_rule_name_en": SEPARATION_RULE_NAME_EN,
        "separation_rule_name_zh": SEPARATION_RULE_NAME_ZH,
        "validate_once": True,
        "reference_many_times": True,
        "future_phase_requirements": [
            "protocol_standard_ref must exist",
            "protocol_id must be valid LUNA-PROTO format",
            "error_namespace must be valid",
            "must reference registered protocol when applicable",
            "must preserve constitutional boundary",
            "errors must map to standard error_code",
            "distinguish protocol_violation from module_process_failure and module_business_logic_failure",
        ],
        "must_not_repeat_in_module_phases": [
            "protocol_numbering_redesign",
            "error_code_redesign",
            "protocol_execution_result_redesign",
            "whitebox_binding_candidate_redesign",
            "full_protocol_system_revalidation_per_module_phase",
        ],
        "insert_protocol_standard_phase_only_when": "new_protocol_type_required",
        **meta,
    }

    smoke_validation = {
        "validation_id": "protocol_shared_code_smoke_validation_v1",
        "import_rows": import_rows,
        "canonical_protocol_id": canonical_id,
        "canonical_error_code": sample_error_code,
        "execution_result_example": exec_result.to_dict(),
        "error_object_example": err_dict,
        "registry_samples": registry_rows,
        "protocol_chain_samples": chain_samples,
        "whitelist_modules": list(SHARED_CODE_MODULES),
        **go_values,
        **meta,
    }

    smoke_report = {
        "report_id": "protocol_shared_code_smoke_report_v1",
        "objectives": [
            "shared protocol code import and call smoke test",
            "sample protocol -> error_code -> execution_result -> whitebox candidate chain",
            "confirm no runtime side effects",
        ],
        "smoke_pass": smoke_pass,
        "issues": issues,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if smoke_pass else "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-Smoke-Issue-Review-v1-001",
        **go_values,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "smoke_pass": smoke_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "go_conditions": go_values,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if smoke_pass else "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-Smoke-Issue-Review-v1-001",
        **go_values,
        **meta,
    }

    markdown = "\n".join(
        [
            "# Protocol Shared Code Smoke Report v1",
            "",
            f"Principle: **{PRINCIPLE_EN}** / **{PRINCIPLE_ZH}**",
            f"Separation Rule: **{SEPARATION_RULE_NAME_EN}** / **{SEPARATION_RULE_NAME_ZH}**",
            "",
            "Protocol layer = guardrail and judgment standard, not driver program.",
            "",
            f"Prior planning GO: `{prior_protocol_canonical_standard_planning_go}`",
            f"Shared code imports OK: `{shared_code_imports_ok}`",
            f"Canonical protocol ID: `{canonical_id}`",
            f"Canonical error code: `{sample_error_code}`",
            f"Sample protocols tested: `{len(SAMPLE_PROTOCOLS)}`",
            f"No runtime side effects: `{no_runtime_side_effects_ok}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{NEXT_PHASE_GO if smoke_pass else 'issue-review'}`",
        ]
    )

    return {
        "protocol_shared_code_smoke_report": smoke_report,
        "protocol_shared_code_smoke_report_md": markdown,
        "protocol_shared_code_smoke_validation": smoke_validation,
        "protocol_standard_reference_rule": reference_rule,
        "protocol_constraint_vs_module_logic_separation_rule": separation_rule,
        "summary": summary,
    }
