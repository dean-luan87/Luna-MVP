# -*- coding: utf-8 -*-
"""Field-First Core Model Preinstall Plan v1."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_model_preinstall_plan_items_v1 import (
    CAPABILITY_REVIEW_QUEUE,
    CONFIG_MANIFEST_FILES,
    DO_NOT_MISCLASSIFY,
    MODEL_ROOM_DIRECTORIES,
    MODEL_ROOM_PREINSTALL_PLANS,
    PREINSTALL_MANIFEST_ENTRIES,
    PREINSTALL_PRINCIPLES,
    PRIOR_ASSET_REPOSITIONING,
    PROHIBITED_PREINSTALL_ACTIONS,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_lineage_v1 import (
    FIELD_FIRST_PREINSTALL_STAGE_ADDITIONS,
    FIELD_FIRST_PREINSTALL_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_PREINSTALL_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IDEAL_OP_ROOT,
    FINAL_DECISION_GO as IDEAL_OP_FINAL_GO,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_RECAL_ROOT,
    FINAL_DECISION_GO as RECAL_FINAL_GO,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ROLE_REDEF_ROOT,
    FINAL_DECISION_GO as ROLE_REDEF_FINAL_GO,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.model_adapters.field_first_adapter_contracts_v1 import (
    ADAPTER_CONTRACT_ID,
    ADAPTER_REQUIRED_FIELDS,
    CANDIDATE_OUTPUT_CONTRACTS,
    PROHIBITED_ADAPTER_ACTIONS,
    PROHIBITED_ADAPTER_IMPORTS,
)
from capabilities.midplatform.model_adapters.field_first_adapter_placeholders_v1 import (
    ADAPTER_PLACEHOLDERS,
    list_adapter_placeholders,
)
from capabilities.midplatform.model_adapters.field_first_adapter_static_validators_v1 import (
    validate_all_manifests,
    validate_no_prohibited_imports_in_source,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

PHASE_ID = "Phase-Midplatform-Field-First-Core-Model-Preinstall-Plan-and-Cache-Manifest-Prepare-v1-001"
SCOPE = "field_first_core_model_preinstall_plan_only"
SOURCE_CHAIN = "field_first_core_model_preinstall_plan_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_READY_FOR_MODEL_DOCUMENT_CAPABILITY_REVIEW"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_BLOCKED_BY_PLAN_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Model-Preinstall-Plan-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_model_preinstall_plan_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_PREINSTALL_PLAN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_model_preinstall_plan_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_preinstall_plan_v1.py",
    "capabilities/midplatform/field_first_core_model_preinstall_plan_items_v1.py",
    "capabilities/midplatform/field_first_core_model_preinstall_plan_lineage_v1.py",
    "capabilities/midplatform/model_adapters/field_first_adapter_types_v1.py",
    "capabilities/midplatform/model_adapters/field_first_adapter_contracts_v1.py",
    "capabilities/midplatform/model_adapters/field_first_adapter_placeholders_v1.py",
    "capabilities/midplatform/model_adapters/field_first_adapter_static_validators_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_preinstall_plan_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_preinstall_plan_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ideal_operation_go",
    "prior_field_first_role_redef_go",
    "prior_field_first_recal_go",
    "preinstall_manifest_complete",
    "model_room_registry_complete",
    "adapter_placeholder_registry_complete",
    "capability_review_queue_complete",
    "download_authorization_all_false",
    "model_preinstall_is_planning_only",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, ideal_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_model_preinstall_plan_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "ideal_operation_root": str(ideal_root),
    }


def _upstream_go(path: Path, final_go: str, pass_key: str, min_checks: int = 340) -> bool:
    s, v = _read_json(path / "summary.json"), _read_json(path / "verifier_report.json")
    return s.get("final_decision") == final_go and v.get("verifier") == "GO" and int(v.get("passed_checks", 0)) >= min_checks and s.get(pass_key) is True


def run_field_first_core_model_preinstall_plan_v1(
    *,
    ideal_operation_root: str,
    role_redef_root: str = DEFAULT_ROLE_REDEF_ROOT,
    recal_root: str = DEFAULT_RECAL_ROOT,
    output_root: Optional[str] = None,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    ideal_upstream = Path(ideal_operation_root or DEFAULT_IDEAL_OP_ROOT).expanduser().resolve()
    role_upstream = Path(role_redef_root).expanduser().resolve()
    recal_upstream = Path(recal_root).expanduser().resolve()
    repo = Path(repo_root or Path(__file__).resolve().parents[2]).expanduser().resolve()
    meta = _meta(out, ideal_upstream)
    issues: List[str] = []

    prior_ideal_operation_go = _upstream_go(ideal_upstream, IDEAL_OP_FINAL_GO, "field_first_core_ideal_operation_mechanism_pass", 380)
    prior_field_first_role_redef_go = _upstream_go(role_upstream, ROLE_REDEF_FINAL_GO, "field_first_core_role_function_redefinition_pass", 380)
    prior_field_first_recal_go = _upstream_go(recal_upstream, RECAL_FINAL_GO, "field_first_core_recalibration_pass", 340)
    if not prior_ideal_operation_go:
        issues.append("ideal_operation_not_go")
    if not prior_field_first_role_redef_go:
        issues.append("role_redef_not_go")
    if not prior_field_first_recal_go:
        issues.append("recal_not_go")

    ideal_s = _read_json(ideal_upstream / "summary.json")
    absence = {k: ideal_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_ideal_operation_go and ideal_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    for d in MODEL_ROOM_DIRECTORIES:
        (repo / d).mkdir(parents=True, exist_ok=True)

    manifest_entries = [dict(e) for e in PREINSTALL_MANIFEST_ENTRIES]
    manifest_ok, manifest_issues = validate_all_manifests(manifest_entries)
    if not manifest_ok:
        issues.extend(manifest_issues[:5])

    preinstall_manifest_complete = len(manifest_entries) >= 15 and manifest_ok
    model_room_registry_complete = len(MODEL_ROOM_PREINSTALL_PLANS) >= 8
    adapter_list = [dataclasses.asdict(p) for p in list_adapter_placeholders()]
    adapter_placeholder_registry_complete = len(adapter_list) >= 15
    capability_review_queue_complete = len(CAPABILITY_REVIEW_QUEUE) >= 18
    download_auth = [{"model_project_id": e["model_project_id"], "download_authorized": False, "authorization_reason": "capability_review_not_complete"} for e in manifest_entries]
    download_authorization_all_false = all(not x["download_authorized"] for x in download_auth)

    for forbidden in ("capabilities/midplatform/model_adapters/field_first_adapter_placeholders_v1.py",):
        src = (repo / forbidden).read_text(encoding="utf-8") if (repo / forbidden).is_file() else ""
        imp_ok, imp_found = validate_no_prohibited_imports_in_source(src)
        if not imp_ok:
            issues.append(f"prohibited_import:{imp_found[0]}")

    room_reg = {"registry_id": "model_room_registry_v1", "model_room_registry_complete": model_room_registry_complete, "rooms": list(MODEL_ROOM_PREINSTALL_PLANS), **meta}
    preinstall_manifest = {"manifest_id": "preinstall_manifest_v1", "preinstall_manifest_complete": preinstall_manifest_complete, "entries": manifest_entries, **meta}
    download_auth_doc = {"authorization_id": "model_download_authorization_v1", "download_authorization_all_false": download_authorization_all_false, "entries": download_auth, **meta}
    adapter_reg = {"registry_id": "model_adapter_placeholder_registry_v1", "adapter_placeholder_registry_complete": adapter_placeholder_registry_complete, "placeholders": adapter_list, **meta}
    review_queue = {"queue_id": "model_capability_review_queue_v1", "capability_review_queue_complete": capability_review_queue_complete, "targets": list(CAPABILITY_REVIEW_QUEUE), **meta}
    status_matrix = {
        "matrix_id": "model_preinstall_status_matrix_v1",
        "rows": [{"model_project_id": e["model_project_id"], "recommended_preinstall_status": e["recommended_preinstall_status"], "weights_downloaded": False, "inference_ready": False} for e in manifest_entries],
        **meta,
    }
    prohibited = {"registry_id": "prohibited_preinstall_actions_v1", "actions": list(PROHIBITED_PREINSTALL_ACTIONS), **meta}
    adapter_contract = {
        "contract_id": ADAPTER_CONTRACT_ID,
        "candidate_output_contract_defined": True,
        "required_fields": list(ADAPTER_REQUIRED_FIELDS),
        "candidate_output_contracts": list(CANDIDATE_OUTPUT_CONTRACTS),
        "prohibited_imports": list(PROHIBITED_ADAPTER_IMPORTS),
        "prohibited_actions": list(PROHIBITED_ADAPTER_ACTIONS),
        **meta,
    }
    doc_targets = {"targets_id": "next_document_review_targets_v1", "targets": list(CAPABILITY_REVIEW_QUEUE), **meta}
    reposition = {"register_id": "prior_asset_repositioning_v1", "assets": list(PRIOR_ASSET_REPOSITIONING), **meta}
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "rationale": "Preinstall structure ready; next review model docs against requirement matrix",
        **meta,
    }
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    config_payloads = {
        "configs/models/field_first/preinstall_manifest_v1.json": preinstall_manifest,
        "configs/models/field_first/model_room_registry_v1.json": room_reg,
        "configs/models/field_first/model_download_authorization_v1.json": download_auth_doc,
        "configs/models/field_first/model_adapter_placeholder_registry_v1.json": adapter_reg,
        "configs/models/field_first/model_capability_review_queue_v1.json": review_queue,
    }
    for rel, payload in config_payloads.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    plan_pass = (
        prior_ideal_operation_go and prior_field_first_role_redef_go and prior_field_first_recal_go
        and preinstall_manifest_complete and model_room_registry_complete
        and adapter_placeholder_registry_complete and capability_review_queue_complete
        and download_authorization_all_false and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Ideal-Operation-Mechanism-and-Model-Requirement-Mapping-v1-001",
        base_capability=FIELD_FIRST_PREINSTALL_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_PREINSTALL_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_PREINSTALL_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Model-Preinstall-Plan-and-Cache-Manifest-Prepare-v1-001",
        stage_term_overrides=FIELD_FIRST_PREINSTALL_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_PREINSTALL_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_PREINSTALL_WHITELIST_FILES,
        repo_root=repo,
        upstream_review_phase="Midplatform-Field-First-Core-Ideal-Operation-Mechanism-and-Model-Requirement-Mapping-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    ideal_fs = _read_json(ideal_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=ideal_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    plan_pass = plan_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if plan_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if plan_pass else (FINAL_DECISION_UPSTREAM if not prior_ideal_operation_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_ideal_operation_go": prior_ideal_operation_go,
        "prior_field_first_role_redef_go": prior_field_first_role_redef_go,
        "prior_field_first_recal_go": prior_field_first_recal_go,
        "preinstall_manifest_complete": preinstall_manifest_complete,
        "model_room_registry_complete": model_room_registry_complete,
        "adapter_placeholder_registry_complete": adapter_placeholder_registry_complete,
        "capability_review_queue_complete": capability_review_queue_complete,
        "download_authorization_all_false": download_authorization_all_false,
        "model_preinstall_is_planning_only": True,
        "candidate_output_contract_defined": True,
        "adapter_required": True,
        "model_document_capability_review_still_required": True,
        "field_first_route_preserved": True,
        "ipc_repositioned_as_source_normalization_asset": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "clm_deferred": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_repo_clone": True,
        "no_large_dependency_install": True,
        "no_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_real_field_model_creation": True,
        "no_world_model_fact_creation": True,
        "no_model_selected_as_production": True,
        "no_model_marked_ready": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": plan_pass,
        "field_first_core_model_preinstall_plan_pass": plan_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "model_room_count": len(MODEL_ROOM_PREINSTALL_PLANS),
        "model_candidate_count": len(manifest_entries),
        "adapter_placeholder_count": len(adapter_list),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(ideal_s.get("chain_trace_nodes") or []) + ["field_first_model_preinstall_plan"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Model Preinstall Plan v1",
        f"Model rooms: `{len(MODEL_ROOM_PREINSTALL_PLANS)}` | Candidates: `{len(manifest_entries)}` | Adapters: `{len(adapter_list)}`",
        f"Review queue: `{len(CAPABILITY_REVIEW_QUEUE)}` | download_authorized: all false",
        f"Planning only — no weights, no inference, no runtime",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])
    return {
        "model_preinstall_plan_report": {**go_values, "final_decision": final_decision, **meta},
        "model_preinstall_plan_report_md": md,
        "model_room_registry": room_reg,
        "preinstall_manifest": preinstall_manifest,
        "model_download_authorization": download_auth_doc,
        "model_adapter_placeholder_registry": adapter_reg,
        "model_capability_review_queue": review_queue,
        "model_preinstall_status_matrix": status_matrix,
        "prohibited_preinstall_actions": prohibited,
        "adapter_placeholder_contract": adapter_contract,
        "next_document_review_targets": doc_targets,
        "prior_asset_repositioning": reposition,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
