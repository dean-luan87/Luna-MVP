# -*- coding: utf-8 -*-
"""Factory Standard Historical Redundancy Cleanup Planning v1 — marking-only, no physical delete."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DRYRUN_REVIEW_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    SOURCE_PHASE_INVENTORY,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL_GO,
    NEXT_PHASE_GO as LIFECYCLE_DR_NEXT_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL_GO,
    PHASE_ID as FORMAL_PLANNING_PHASE,
)

PHASE_ID = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-Planning-v1-001"
SCOPE = "factory_standard_historical_redundancy_cleanup_planning_only"
SOURCE_CHAIN = "factory_standard_historical_redundancy_cleanup_planning_v1"

UPSTREAM_LIFECYCLE_DR_FINAL = LIFECYCLE_DR_FINAL_GO
UPSTREAM_LIFECYCLE_DR_NEXT = LIFECYCLE_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "FACTORY_STANDARD_HISTORICAL_REDUNDANCY_CLEANUP_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "FACTORY_STANDARD_HISTORICAL_REDUNDANCY_CLEANUP_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-Issue-Review-v1-001"

HARNESS_MODULE_ID = "controlled_provider_readiness_harness_v1"
VALIDATION_FACTORY_ID = "luna_validation_factory_v1"

CLEANUP_SCOPES: Tuple[str, ...] = (
    "ocr_authorization_long_chain",
    "formal_artifact_send_grant_triple_chain_duplicate_rules",
    "provider_selection_dependency_environment_duplicate_rules",
    "blocked_path_non_claims_evidence_lifecycle_duplicate_definitions",
    "factory_standard_absorbed_generic_rules",
    "controlled_provider_readiness_harness_absorbed_provider_rules",
)

MARKER_STATUSES: Tuple[str, ...] = (
    "active",
    "superseded_for_new_phase",
    "absorbed_by_factory_standard",
    "absorbed_by_provider_harness",
    "deprecated_for_new_phase",
    "read_only_evidence_source",
    "historical_reference_only",
)

METADATA_SCHEMA_FIELDS: Tuple[str, ...] = (
    "object_id",
    "object_type",
    "source_phase",
    "source_artifact_path",
    "status",
    "superseded_by",
    "absorbed_by",
    "deprecated_for_new_phase",
    "read_only_evidence_source",
    "keep_for_audit",
    "physical_delete_allowed",
    "migration_required",
    "future_reference_policy",
)

FORBIDDEN_ACTIONS: Tuple[str, ...] = (
    "delete historical files",
    "rewrite historical eval_out",
    "move historical artifacts",
    "remove phase table records",
    "erase GO/NO-GO evidence",
    "mutate verifier reports",
    "collapse evidence chain",
)

FUTURE_REFERENCE_RULES: Tuple[str, ...] = (
    "prefer Capability Factory Standard for new phases",
    "prefer ControlledProviderReadinessHarness for provider readiness",
    "prefer Validation Factory for unified validation",
    "do not replicate Formal Artifact / Send / Grant triple chain",
    "do not replicate provider selection→dependency→environment→real-dep long chain",
    "historical phases are read_only_evidence_source only",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Cleanup Planning GO ≠ historical files deleted",
    "superseded marking ≠ historical verdict erased",
    "absorbed_by marking ≠ source artifact removed",
    "deprecated_for_new_phase ≠ phase table record deleted",
    "read_only_evidence_source ≠ evidence chain collapsed",
    "DryRunAndReview next ≠ physical cleanup executed",
    "cleanup planning ≠ runtime enabled",
    "cleanup planning ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "historical_file_delete_executed_now",
    "historical_file_move_executed_now",
    "historical_file_rewrite_executed_now",
    "phase_table_destructive_update_now",
    "evidence_chain_modified_now",
    "historical_eval_out_deleted_now",
    "historical_docs_deleted_now",
    "runtime_enabled_now",
    "provider_invoked_now",
    "formal_request_artifact_generated_now",
    "grant_issued_now",
    "real_dependency_check_executed_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_planning"
)

_EVAL_OUT = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "factory_standard_historical_redundancy_cleanup_planning_only": True,
        "marking_only": True,
        "physical_delete_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _mark_entry(
    *,
    object_id: str,
    object_type: str,
    source_phase: str,
    source_artifact_path: str,
    status: str,
    superseded_by: Optional[str] = None,
    absorbed_by: Optional[str] = None,
    deprecated_for_new_phase: bool = False,
    read_only_evidence_source: bool = False,
    future_reference_policy: str = "read_only_evidence_source",
) -> Dict[str, Any]:
    return {
        "object_id": object_id,
        "object_type": object_type,
        "source_phase": source_phase,
        "source_artifact_path": source_artifact_path,
        "status": status,
        "superseded_by": superseded_by,
        "absorbed_by": absorbed_by,
        "deprecated_for_new_phase": deprecated_for_new_phase,
        "read_only_evidence_source": read_only_evidence_source,
        "keep_for_audit": True,
        "physical_delete_allowed": False,
        "migration_required": False,
        "future_reference_policy": future_reference_policy,
    }


def _phase_dir_slug(phase_id: str) -> str:
    return phase_id.replace("Phase-", "").replace("-v1-001", "").lower().replace("-", "_")


def _build_superseded_inventory() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for phase_id in MERGEABLE_OCR_AUTHORIZATION_PHASES:
        slug = _phase_dir_slug(phase_id)
        items.append(
            _mark_entry(
                object_id=f"superseded_phase:{phase_id}",
                object_type="phase",
                source_phase=phase_id,
                source_artifact_path=f"{_EVAL_OUT}/{slug}/",
                status="superseded_for_new_phase",
                superseded_by="Phase-Compressed-OCR-Authorization-Lifecycle-DryRunAndReview-v1-001",
                absorbed_by=STANDARD_ID,
                deprecated_for_new_phase=True,
                read_only_evidence_source=True,
                future_reference_policy="do_not_resume_triple_chain",
            )
        )
    items.append(
        _mark_entry(
            object_id=f"superseded_phase:{FORMAL_PLANNING_PHASE}",
            object_type="phase",
            source_phase=FORMAL_PLANNING_PHASE,
            source_artifact_path=f"{_EVAL_OUT}/ocr_provider_authorization_formal_request_artifact_generation_planning/",
            status="superseded_for_new_phase",
            superseded_by=STANDARD_ID,
            absorbed_by=STANDARD_ID,
            deprecated_for_new_phase=True,
            read_only_evidence_source=True,
            future_reference_policy="planning_go_preserved_as_evidence_only",
        )
    )
    return items


def _build_absorbed_rules() -> List[Dict[str, Any]]:
    categories = (
        ("lifecycle", "Lifecycle Standard"),
        ("boundary", "Boundary Standard"),
        ("evidence", "Evidence Standard"),
        ("approval_grant", "Approval/Grant Standard"),
        ("sandbox_rollback", "Sandbox/Rollback Standard"),
        ("candidate", "Candidate Standard"),
        ("artifact", "Artifact Standard"),
        ("provider_machine", "Provider/Machine Standard"),
        ("upstream_downstream", "Transfer Standard"),
    )
    items: List[Dict[str, Any]] = []
    for src in SOURCE_PHASE_INVENTORY:
        for cat in src.get("rule_categories") or ():
            std = next((s for c, s in categories if c == cat), STANDARD_ID)
            items.append(
                _mark_entry(
                    object_id=f"absorbed_rule:{src['phase_id']}:{cat}",
                    object_type="rule_category",
                    source_phase=src["phase_id"],
                    source_artifact_path=f"{_EVAL_OUT}/",
                    status="absorbed_by_factory_standard",
                    absorbed_by=std,
                    deprecated_for_new_phase=True,
                    read_only_evidence_source=True,
                    future_reference_policy="reference_factory_standard_not_duplicate",
                )
            )
    harness_rules = (
        "provider_candidate_registration",
        "dependency_readiness_check_plan",
        "environment_readiness_check_plan",
        "health_binding",
        "constitution_gate",
    )
    for rule in harness_rules:
        items.append(
            _mark_entry(
                object_id=f"absorbed_rule:harness:{rule}",
                object_type="provider_readiness_rule",
                source_phase="Phase-OCR-Controlled-Provider-Readiness-Harness-v1-001",
                source_artifact_path=f"{_EVAL_OUT}/ocr_controlled_provider_readiness_harness/",
                status="absorbed_by_provider_harness",
                absorbed_by=HARNESS_MODULE_ID,
                deprecated_for_new_phase=True,
                read_only_evidence_source=True,
                future_reference_policy="reference_harness_not_duplicate",
            )
        )
    return items


def _build_deprecated_inventory() -> List[Dict[str, Any]]:
    triple_labels = (
        "formal_artifact_generation_triple",
        "request_send_triple",
        "grant_triple",
    )
    items: List[Dict[str, Any]] = []
    for label in triple_labels:
        items.append(
            _mark_entry(
                object_id=f"deprecated_chain:{label}",
                object_type="authorization_chain_pattern",
                source_phase="historical_ocr_authorization",
                source_artifact_path=f"{_EVAL_OUT}/",
                status="deprecated_for_new_phase",
                superseded_by="compressed_authorization_lifecycle_via_factory_standard",
                deprecated_for_new_phase=True,
                read_only_evidence_source=True,
                future_reference_policy="do_not_replicate_triple_chain",
            )
        )
    provider_chain_phases = (
        "Phase-OCR-Provider-Selection-Dependency-Environment-Planning-v1-001",
        "Phase-OCR-Provider-Selection-Dependency-Environment-DryRun-v1-001",
        "Phase-OCR-Provider-Selection-Dependency-Environment-Post-DryRun-Review-v1-001",
    )
    for phase_id in provider_chain_phases:
        slug = _phase_dir_slug(phase_id)
        items.append(
            _mark_entry(
                object_id=f"deprecated_chain:provider_selection:{phase_id}",
                object_type="phase",
                source_phase=phase_id,
                source_artifact_path=f"{_EVAL_OUT}/{slug}/",
                status="deprecated_for_new_phase",
                superseded_by=HARNESS_MODULE_ID,
                deprecated_for_new_phase=True,
                read_only_evidence_source=True,
                future_reference_policy="use_harness_and_validation_factory",
            )
        )
    duplicate_defs = (
        "blocked_path_definitions",
        "non_claims_definitions",
        "evidence_requirement_definitions",
        "lifecycle_state_definitions",
    )
    for defn in duplicate_defs:
        items.append(
            _mark_entry(
                object_id=f"deprecated_duplicate:{defn}",
                object_type="rule_definition",
                source_phase="historical_ocr_phases",
                source_artifact_path=f"{_EVAL_OUT}/",
                status="deprecated_for_new_phase",
                absorbed_by=STANDARD_ID,
                deprecated_for_new_phase=True,
                read_only_evidence_source=True,
                future_reference_policy="reference_factory_standard",
            )
        )
    return items


def _build_read_only_register(
    *,
    lifecycle_dr_root: Path,
    factory_dr_root: Path,
    req_post_root: Path,
    formal_plan_root: Path,
    selection_post_root: Path,
    real_dep_post_root: Path,
    factory_post_root: Path,
) -> List[Dict[str, Any]]:
    evidence_phases = (
        (FORMAL_PLANNING_PHASE, str(formal_plan_root), "formal_generation_planning_go_evidence"),
        (
            "Phase-OCR-Provider-Authorization-Request-Post-DryRun-Review-v1-001",
            str(req_post_root),
            "request_artifact_candidate_ready_evidence",
        ),
        (
            "Phase-OCR-Provider-Selection-Dependency-Environment-Post-DryRun-Review-v1-001",
            str(selection_post_root),
            "provider_selection_candidate_evidence",
        ),
        (
            "Phase-OCR-Provider-Real-Dependency-Check-Post-DryRun-Review-v1-001",
            str(real_dep_post_root),
            "real_dependency_check_flow_evidence",
        ),
        (
            "Phase-Capability-Factory-Admission-and-Operation-Standard-DryRunAndReview-v1-001",
            str(factory_dr_root),
            "nine_standards_validation_evidence",
        ),
        (
            "Phase-Compressed-OCR-Authorization-Lifecycle-DryRunAndReview-v1-001",
            str(lifecycle_dr_root),
            "compressed_lifecycle_closure_evidence",
        ),
        (
            "Phase-Controlled-Provider-Readiness-Harness-Factory-Registration-Post-DryRun-Review-v1-001",
            str(factory_post_root),
            "harness_factory_registration_evidence",
        ),
    )
    return [
        _mark_entry(
            object_id=f"read_only:{phase_id}",
            object_type="phase_evidence_root",
            source_phase=phase_id,
            source_artifact_path=path,
            status="read_only_evidence_source",
            read_only_evidence_source=True,
            future_reference_policy=policy,
        )
        for phase_id, path, policy in evidence_phases
    ]


def run_factory_standard_historical_redundancy_cleanup_planning_v1(
    *,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: str,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_planning_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
    ).expanduser().resolve()
    lifecycle_dr_sm = _try_read_json(lifecycle_dr_root / "summary.json") or {}
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}
    lifecycle_closure = _try_read_json(lifecycle_dr_root / "compressed_lifecycle_closure_decision_v1.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or lifecycle_dr_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    readiness_dr = _try_read_json(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json") or {}

    factory_plan_root = Path(
        capability_factory_admission_and_operation_standard_planning_root
        or lifecycle_dr_root.parent / "capability_factory_admission_and_operation_standard_planning"
    ).expanduser().resolve()
    factory_plan_vr = _try_read_json(factory_plan_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or lifecycle_dr_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or lifecycle_dr_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or lifecycle_dr_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}

    selection_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or lifecycle_dr_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    selection_post_vr = _try_read_json(selection_post_root / "verifier_report.json") or {}

    real_dep_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or lifecycle_dr_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_dep_post_vr = _try_read_json(real_dep_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_planning_root": str(factory_plan_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_formal_planning_root": str(formal_plan_root),
        "upstream_request_post_root": str(req_post_root),
        "upstream_selection_post_root": str(selection_post_root),
        "upstream_real_dep_post_root": str(real_dep_post_root),
        "output_root": str(out_root),
    }

    if lifecycle_dr_vr.get("verifier") != "GO" or lifecycle_dr_vr.get("passed") is not True:
        blockers.append("lifecycle dryrun and review verifier must be GO")
    if lifecycle_dr_sm.get("final_decision") != UPSTREAM_LIFECYCLE_DR_FINAL:
        blockers.append("lifecycle dryrun final_decision mismatch")
    if lifecycle_dr_sm.get("recommended_next_phase") != UPSTREAM_LIFECYCLE_DR_NEXT:
        blockers.append("lifecycle dryrun recommended_next_phase mismatch")
    if lifecycle_closure.get("closure_pass") is not True:
        blockers.append("lifecycle closure must pass")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun and review must be GO")
    if factory_dr_sm.get("final_decision") != FACTORY_DRYRUN_REVIEW_FINAL_GO:
        blockers.append("factory dryrun review final_decision mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")
    if factory_dr_sm.get("compression_validated") is not True:
        blockers.append("compression_validated must be true")
    if readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("do_not_resume_formal_artifact_triple_chain must be true")

    if factory_plan_vr.get("verifier") != "GO":
        blockers.append("factory standard planning must be GO")
    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")
    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal artifact planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")
    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-dryrun review must be GO")
    if selection_post_vr.get("verifier") != "GO":
        blockers.append("selection dependency environment post-review must be GO")
    if real_dep_post_vr.get("verifier") != "GO":
        blockers.append("real dependency check post-review must be GO")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    lifecycle_input_review = {
        "review_id": "compressed_lifecycle_input_review_v1",
        "upstream_root": str(lifecycle_dr_root),
        "upstream_verifier_go": lifecycle_dr_vr.get("verifier") == "GO",
        "upstream_final_decision": lifecycle_dr_sm.get("final_decision"),
        "closure_pass": lifecycle_closure.get("closure_pass"),
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    redundancy_scope = {
        "scope_id": "historical_redundancy_scope_v1",
        "scopes": list(CLEANUP_SCOPES),
        "scope_count": len(CLEANUP_SCOPES),
        "marking_only": True,
        "physical_delete_allowed": False,
        **meta,
    }

    superseded_inventory = {
        "inventory_id": "superseded_phase_inventory_plan_v1",
        "items": _build_superseded_inventory(),
        "item_count": len(MERGEABLE_OCR_AUTHORIZATION_PHASES) + 1,
        **meta,
    }

    absorbed_items = _build_absorbed_rules()
    deprecated_items = _build_deprecated_inventory()

    absorbed_inventory = {
        "inventory_id": "absorbed_rule_inventory_plan_v1",
        "items": absorbed_items,
        "item_count": len(absorbed_items),
        **meta,
    }

    deprecated_inventory = {
        "inventory_id": "deprecated_for_new_phase_inventory_plan_v1",
        "items": deprecated_items,
        "item_count": len(deprecated_items),
        **meta,
    }

    read_only_register = {
        "register_id": "read_only_evidence_source_register_plan_v1",
        "items": _build_read_only_register(
            lifecycle_dr_root=lifecycle_dr_root,
            factory_dr_root=factory_dr_root,
            req_post_root=req_post_root,
            formal_plan_root=formal_plan_root,
            selection_post_root=selection_post_root,
            real_dep_post_root=real_dep_post_root,
            factory_post_root=factory_post_root,
        ),
        "item_count": 7,
        **meta,
    }

    no_delete_policy = {
        "policy_id": "no_physical_delete_policy_v1",
        "physical_delete_allowed": False,
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "historical_file_delete_executed_now": False,
        "historical_file_move_executed_now": False,
        "historical_file_rewrite_executed_now": False,
        "historical_eval_out_deleted_now": False,
        "historical_docs_deleted_now": False,
        **meta,
    }

    chain_preservation = {
        "policy_id": "historical_chain_preservation_policy_v1",
        "evidence_chain_modified_now": False,
        "phase_table_destructive_update_now": False,
        "preserve_verifier_reports": True,
        "preserve_go_no_go_evidence": True,
        "preserve_phase_table_records": True,
        "collapse_evidence_chain_forbidden": True,
        **meta,
    }

    future_reference = {
        "policy_id": "future_phase_reference_policy_v1",
        "rules": list(FUTURE_REFERENCE_RULES),
        "prefer_factory_standard": True,
        "prefer_controlled_provider_readiness_harness": True,
        "prefer_validation_factory": True,
        "do_not_resume_formal_artifact_triple_chain": True,
        "historical_phases_read_only": True,
        **meta,
    }

    metadata_schema = {
        "schema_id": "cleanup_metadata_schema_v1",
        "required_fields": list(METADATA_SCHEMA_FIELDS),
        "field_count": len(METADATA_SCHEMA_FIELDS),
        "allowed_statuses": list(MARKER_STATUSES),
        "keep_for_audit_default": True,
        "physical_delete_allowed_default": False,
        "migration_required_default": False,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "cleanup_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "generate historical_redundancy_cleanup_candidate",
            "generate superseded / absorbed / deprecated / read_only marker samples",
            "verify no physical deletion",
            "verify historical evidence chain preserved",
            "verify future phases reference standard modules",
            "do not mutate real historical files",
        ],
        "historical_file_delete_executed_now": False,
        "evidence_chain_modified_now": False,
        **meta,
    }

    planning_decision = {
        "decision_id": "cleanup_planning_decision_v1",
        "planning_pass": boundary_ok,
        "marking_only": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "factory_standard_historical_cleanup_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "marking_only": True,
        "superseded_phase_count": superseded_inventory["item_count"],
        "absorbed_rule_count": absorbed_inventory["item_count"],
        "deprecated_item_count": deprecated_inventory["item_count"],
        "read_only_source_count": read_only_register["item_count"],
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "factory_standard_historical_cleanup_planning_policy": policy,
        "compressed_lifecycle_input_review": lifecycle_input_review,
        "historical_redundancy_scope": redundancy_scope,
        "superseded_phase_inventory_plan": superseded_inventory,
        "absorbed_rule_inventory_plan": absorbed_inventory,
        "deprecated_for_new_phase_inventory_plan": deprecated_inventory,
        "read_only_evidence_source_register_plan": read_only_register,
        "no_physical_delete_policy": no_delete_policy,
        "historical_chain_preservation_policy": chain_preservation,
        "future_phase_reference_policy": future_reference,
        "cleanup_metadata_schema": metadata_schema,
        "cleanup_dryrun_plan": dryrun_plan,
        "cleanup_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
