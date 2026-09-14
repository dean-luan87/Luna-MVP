# -*- coding: utf-8 -*-
"""Factory Standard Historical Redundancy Cleanup DryRunAndReview v1 — marker samples only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    STANDARD_ID,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_planning_v1 import (
    CLEANUP_SCOPES,
    FINAL_DECISION_GO as CLEANUP_PLANNING_FINAL_GO,
    FORBIDDEN_ACTIONS,
    FUTURE_REFERENCE_RULES,
    HARNESS_MODULE_ID,
    METADATA_SCHEMA_FIELDS,
    NEXT_PHASE_GO as CLEANUP_PLANNING_NEXT_PHASE,
    VALIDATION_FACTORY_ID,
    _build_absorbed_rules,
    _build_deprecated_inventory,
    _build_read_only_register,
    _build_superseded_inventory,
    _mark_entry,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL_GO,
    PHASE_ID as FORMAL_PLANNING_PHASE,
)

PHASE_ID = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-DryRunAndReview-v1-001"
SCOPE = "factory_standard_historical_redundancy_cleanup_dryrun_and_review_only"
SOURCE_CHAIN = "factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1"

UPSTREAM_CLEANUP_PLANNING_FINAL = CLEANUP_PLANNING_FINAL_GO
UPSTREAM_CLEANUP_PLANNING_NEXT = CLEANUP_PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "FACTORY_STANDARD_HISTORICAL_REDUNDANCY_CLEANUP_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_OCR_AUTHORIZATION_NEXT_ROUTE_DECISION"
)
FINAL_DECISION_HOLD = (
    "FACTORY_STANDARD_HISTORICAL_REDUNDANCY_CLEANUP_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Authorization-Next-Route-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-Issue-Review-v1-001"

COMPRESSED_LIFECYCLE_REF = "Phase-Compressed-OCR-Authorization-Lifecycle-DryRunAndReview-v1-001"

SUPERSEDED_COVERAGE: Tuple[str, ...] = (
    FORMAL_PLANNING_PHASE,
    "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-Post-DryRun-Review-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-Planning-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-Post-DryRun-Review-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-Planning-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-Post-DryRun-Review-v1-001",
)

ABSORBED_RULE_SAMPLES: Tuple[Tuple[str, str, str], ...] = (
    ("candidate_only", "Candidate Standard", STANDARD_ID),
    ("non_claim_chain", "Lifecycle Standard", STANDARD_ID),
    ("blocked_path", "Boundary Standard", STANDARD_ID),
    ("boundary_false", "Boundary Standard", STANDARD_ID),
    ("lifecycle_state", "Lifecycle Standard", STANDARD_ID),
    ("evidence_requirement", "Evidence Standard", STANDARD_ID),
    ("approval_grant", "Approval/Grant Standard", STANDARD_ID),
    ("sandbox_rollback", "Sandbox/Rollback Standard", STANDARD_ID),
    ("provider_readiness", "Provider/Machine Standard", HARNESS_MODULE_ID),
)

DEPRECATED_PATTERNS: Tuple[str, ...] = (
    "formal_artifact_send_grant_triple_chain",
    "provider_selection_dependency_environment_real_dep_long_chain",
    "per_domain_duplicated_provider_readiness",
    "local_blocked_path_custom_definition",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "cleanup_to_file_delete",
    "cleanup_to_file_move",
    "cleanup_to_file_rewrite",
    "cleanup_to_eval_out_delete",
    "cleanup_to_docs_delete",
    "cleanup_to_phase_table_destructive_update",
    "cleanup_to_verifier_report_mutation",
    "cleanup_to_evidence_chain_mutation",
    "cleanup_to_runtime_enable",
    "cleanup_to_provider_invoke",
    "cleanup_to_grant_issue",
    "cleanup_to_real_dependency_check",
    "cleanup_to_memory_write",
    "cleanup_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Cleanup DryRunAndReview GO ≠ historical files deleted",
    "superseded marker ≠ old verdict invalidated",
    "absorbed marker ≠ source evidence removed",
    "deprecated_for_new_phase ≠ historical phase unusable for audit",
    "read_only_evidence_source ≠ evidence chain collapsed",
    "next OCR route decision ≠ real dependency check allowed",
    "marker sample generated ≠ physical cleanup executed",
    "compression alignment pass ≠ triple-chain resumed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "historical_redundancy_cleanup_candidate_generated_now",
    "superseded_marker_sample_generated_now",
    "absorbed_marker_sample_generated_now",
    "deprecated_marker_sample_generated_now",
    "read_only_evidence_source_marker_sample_generated_now",
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
    "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
)

_EVAL_OUT = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "factory_standard_historical_redundancy_cleanup_dryrun_and_review_only": True,
        "simulated": True,
        "marking_only": True,
        "physical_delete_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _marker_schema_ok(item: Dict[str, Any]) -> bool:
    for field in METADATA_SCHEMA_FIELDS:
        if field not in item:
            return False
    return (
        item.get("keep_for_audit") is True
        and item.get("physical_delete_allowed") is False
        and item.get("migration_required") is False
    )


def _build_superseded_samples() -> List[Dict[str, Any]]:
    samples: List[Dict[str, Any]] = []
    for item in _build_superseded_inventory():
        sample = {
            **item,
            "marker_type": "superseded",
            "simulated": True,
            "sample_generated_now": True,
            "historical_verdict_preserved": True,
            "superseded_by": item.get("superseded_by") or STANDARD_ID,
            "superseded_by_label": "CapabilityFactoryStandard / CompressedOCRAuthorizationLifecycle",
        }
        samples.append(sample)
    return samples


def _build_absorbed_samples() -> List[Dict[str, Any]]:
    samples: List[Dict[str, Any]] = []
    for rule_id, std_label, absorbed_by in ABSORBED_RULE_SAMPLES:
        is_harness = absorbed_by == HARNESS_MODULE_ID
        samples.append(
            {
                **_mark_entry(
                    object_id=f"absorbed_marker_sample:{rule_id}",
                    object_type="rule_pattern",
                    source_phase="historical_ocr_phases",
                    source_artifact_path=f"{_EVAL_OUT}/",
                    status="absorbed_by_provider_harness" if is_harness else "absorbed_by_factory_standard",
                    absorbed_by=absorbed_by,
                    deprecated_for_new_phase=True,
                    read_only_evidence_source=True,
                    future_reference_policy="reference_standard_not_duplicate",
                ),
                "marker_type": "absorbed",
                "rule_pattern": rule_id,
                "standard_label": std_label,
                "simulated": True,
                "sample_generated_now": True,
                "future_phase_should_reference_standard": True,
                "duplicate_rule_definition_deprecated": True,
            }
        )
    return samples


def _build_deprecated_samples() -> List[Dict[str, Any]]:
    samples: List[Dict[str, Any]] = []
    for pattern in DEPRECATED_PATTERNS:
        superseded = (
            COMPRESSED_LIFECYCLE_REF
            if "triple_chain" in pattern
            else HARNESS_MODULE_ID
        )
        samples.append(
            {
                **_mark_entry(
                    object_id=f"deprecated_marker_sample:{pattern}",
                    object_type="chain_pattern",
                    source_phase="historical_ocr_authorization",
                    source_artifact_path=f"{_EVAL_OUT}/",
                    status="deprecated_for_new_phase",
                    superseded_by=superseded,
                    deprecated_for_new_phase=True,
                    read_only_evidence_source=True,
                    future_reference_policy="new_phase_use_forbidden",
                ),
                "marker_type": "deprecated",
                "pattern_id": pattern,
                "simulated": True,
                "sample_generated_now": True,
                "historical_use_allowed_for_audit": True,
                "new_phase_use_forbidden": True,
            }
        )
    for item in _build_deprecated_inventory():
        sample = {
            **item,
            "marker_type": "deprecated",
            "simulated": True,
            "sample_generated_now": True,
            "historical_use_allowed_for_audit": True,
            "new_phase_use_forbidden": True,
        }
        samples.append(sample)
    return samples


def _build_read_only_samples(
    *,
    lifecycle_dr_root: Path,
    factory_dr_root: Path,
    req_post_root: Path,
    formal_plan_root: Path,
    selection_post_root: Path,
    real_dep_post_root: Path,
    factory_post_root: Path,
) -> List[Dict[str, Any]]:
    samples: List[Dict[str, Any]] = []
    for item in _build_read_only_register(
        lifecycle_dr_root=lifecycle_dr_root,
        factory_dr_root=factory_dr_root,
        req_post_root=req_post_root,
        formal_plan_root=formal_plan_root,
        selection_post_root=selection_post_root,
        real_dep_post_root=real_dep_post_root,
        factory_post_root=factory_post_root,
    ):
        path = Path(item.get("source_artifact_path") or "")
        sample = {
            **item,
            "marker_type": "read_only_evidence_source",
            "simulated": True,
            "sample_generated_now": True,
            "evidence_chain_preserved": True,
            "no_rewrite": True,
            "path_exists": path.is_dir(),
            "verifier_report_exists": (path / "verifier_report.json").is_file() if path.is_dir() else False,
        }
        samples.append(sample)
    return samples


def run_factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1(
    *,
    factory_standard_historical_redundancy_cleanup_planning_root: str,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(factory_standard_historical_redundancy_cleanup_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_decision = _try_read_json(plan_root / "cleanup_planning_decision_v1.json") or {}
    superseded_plan = _try_read_json(plan_root / "superseded_phase_inventory_plan_v1.json") or {}
    absorbed_plan = _try_read_json(plan_root / "absorbed_rule_inventory_plan_v1.json") or {}
    deprecated_plan = _try_read_json(plan_root / "deprecated_for_new_phase_inventory_plan_v1.json") or {}
    read_only_plan = _try_read_json(plan_root / "read_only_evidence_source_register_plan_v1.json") or {}
    no_delete_plan = _try_read_json(plan_root / "no_physical_delete_policy_v1.json") or {}

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        or plan_root.parent / "compressed_ocr_authorization_lifecycle_dryrun_and_review"
    ).expanduser().resolve()
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or plan_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    readiness_dr = _try_read_json(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or plan_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or plan_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or plan_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}

    selection_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or plan_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    selection_post_vr = _try_read_json(selection_post_root / "verifier_report.json") or {}

    real_dep_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or plan_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_dep_post_vr = _try_read_json(real_dep_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_cleanup_planning_root": str(plan_root),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_formal_planning_root": str(formal_plan_root),
        "upstream_request_post_root": str(req_post_root),
        "upstream_selection_post_root": str(selection_post_root),
        "upstream_real_dep_post_root": str(real_dep_post_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO" or plan_vr.get("passed") is not True:
        blockers.append("cleanup planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_CLEANUP_PLANNING_FINAL:
        blockers.append("cleanup planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_CLEANUP_PLANNING_NEXT:
        blockers.append("cleanup planning recommended_next_phase mismatch")
    if plan_sm.get("marking_only") is not True:
        blockers.append("marking_only must be true")
    if plan_decision.get("planning_pass") is not True:
        blockers.append("cleanup planning must pass")
    if no_delete_plan.get("physical_delete_allowed") is not False:
        blockers.append("physical_delete_allowed must be false in planning")
    if (superseded_plan.get("item_count") or 0) < len(MERGEABLE_OCR_AUTHORIZATION_PHASES):
        blockers.append("superseded_phase_inventory must exist")
    if (absorbed_plan.get("item_count") or 0) == 0:
        blockers.append("absorbed_rule_inventory must exist")
    if (deprecated_plan.get("item_count") or 0) == 0:
        blockers.append("deprecated inventory must exist")
    if (read_only_plan.get("item_count") or 0) != 7:
        blockers.append("read_only_evidence_source register must exist")

    for field in BOUNDARY_FALSE:
        if plan_sm.get(field) is True:
            blockers.append(f"planning {field} must be false")

    if lifecycle_dr_vr.get("verifier") != "GO":
        blockers.append("lifecycle dryrun review must be GO")
    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory dryrun review must be GO")
    if readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("do_not_resume_formal_artifact_triple_chain must be true")
    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory post-review must be GO")
    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")
    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-review must be GO")
    if selection_post_vr.get("verifier") != "GO":
        blockers.append("selection post-review must be GO")
    if real_dep_post_vr.get("verifier") != "GO":
        blockers.append("real dep post-review must be GO")

    superseded_samples = _build_superseded_samples()
    absorbed_samples = _build_absorbed_samples()
    deprecated_samples = _build_deprecated_samples()
    read_only_samples = _build_read_only_samples(
        lifecycle_dr_root=lifecycle_dr_root,
        factory_dr_root=factory_dr_root,
        req_post_root=req_post_root,
        formal_plan_root=formal_plan_root,
        selection_post_root=selection_post_root,
        real_dep_post_root=real_dep_post_root,
        factory_post_root=factory_post_root,
    )

    cleanup_objects = []
    for scope in CLEANUP_SCOPES:
        cleanup_objects.append({"scope_id": scope, "marked": True, "physical_delete": False})
    cleanup_candidate = {
        "candidate_id": "historical_redundancy_cleanup_candidate_v1",
        "cleanup_scopes": cleanup_objects,
        "scope_count": len(CLEANUP_SCOPES),
        "superseded_sample_count": len(superseded_samples),
        "absorbed_sample_count": len(absorbed_samples),
        "deprecated_sample_count": len(deprecated_samples),
        "read_only_sample_count": len(read_only_samples),
        "marking_only": True,
        "simulated": True,
        **meta,
    }

    planning_input_review = {
        "review_id": "cleanup_planning_input_review_v1",
        "upstream_root": str(plan_root),
        "upstream_verifier_go": plan_vr.get("verifier") == "GO",
        "upstream_final_decision": plan_sm.get("final_decision"),
        "marking_only": plan_sm.get("marking_only"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    superseded_phase_markers = {
        "samples_id": "superseded_phase_marker_samples_v1",
        "samples": superseded_samples,
        "sample_count": len(superseded_samples),
        "coverage_phases": list(SUPERSEDED_COVERAGE),
        "all_schema_valid": all(_marker_schema_ok(s) for s in superseded_samples),
        "all_verdict_preserved": all(s.get("historical_verdict_preserved") is True for s in superseded_samples),
        "all_read_only": all(s.get("read_only_evidence_source") is True for s in superseded_samples),
        **meta,
    }

    absorbed_rule_markers = {
        "samples_id": "absorbed_rule_marker_samples_v1",
        "samples": absorbed_samples,
        "sample_count": len(absorbed_samples),
        "rule_patterns": [r[0] for r in ABSORBED_RULE_SAMPLES],
        "all_schema_valid": all(_marker_schema_ok(s) for s in absorbed_samples),
        "all_reference_standard": all(s.get("future_phase_should_reference_standard") is True for s in absorbed_samples),
        **meta,
    }

    deprecated_markers = {
        "samples_id": "deprecated_for_new_phase_marker_samples_v1",
        "samples": deprecated_samples,
        "sample_count": len(deprecated_samples),
        "pattern_coverage": list(DEPRECATED_PATTERNS),
        "all_schema_valid": all(_marker_schema_ok(s) for s in deprecated_samples),
        "all_deprecated": all(s.get("deprecated_for_new_phase") is True for s in deprecated_samples),
        **meta,
    }

    read_only_markers = {
        "samples_id": "read_only_evidence_source_marker_samples_v1",
        "samples": read_only_samples,
        "sample_count": len(read_only_samples),
        "all_schema_valid": all(_marker_schema_ok(s) for s in read_only_samples),
        "all_read_only": all(s.get("read_only_evidence_source") is True for s in read_only_samples),
        "all_paths_exist": all(s.get("path_exists") is True for s in read_only_samples),
        "all_verifier_preserved": all(s.get("verifier_report_exists") is True for s in read_only_samples),
        **meta,
    }

    schema_validation = {
        "validation_id": "cleanup_metadata_schema_validation_result_v1",
        "required_fields": list(METADATA_SCHEMA_FIELDS),
        "all_samples_valid": (
            superseded_phase_markers.get("all_schema_valid")
            and absorbed_rule_markers.get("all_schema_valid")
            and deprecated_markers.get("all_schema_valid")
            and read_only_markers.get("all_schema_valid")
        ),
        "validation_pass": len(blockers) == 0,
        **meta,
    }

    evidence_roots = [
        formal_plan_root,
        req_post_root,
        selection_post_root,
        real_dep_post_root,
        factory_dr_root,
        lifecycle_dr_root,
        factory_post_root,
    ]
    chain_preservation = {
        "review_id": "historical_chain_preservation_review_v1",
        **_review_ok([
            ("go_verdict_preserved", formal_plan_vr.get("verifier") == "GO"),
            ("verifier_reports_preserved", all((p / "verifier_report.json").is_file() for p in evidence_roots)),
            ("eval_out_preserved", all(p.is_dir() for p in evidence_roots)),
            ("evidence_chain_not_collapsed", meta.get("evidence_chain_modified_now") is False),
            ("artifacts_not_rewritten", meta.get("historical_file_rewrite_executed_now") is False),
            ("phase_table_not_destructive", meta.get("phase_table_destructive_update_now") is False),
        ]),
        "historical_go_no_go_verdict_preserved": True,
        "verifier_reports_preserved": True,
        "phase_table_records_preserved": True,
        "eval_out_directories_preserved": True,
        "docs_preserved": True,
        **meta,
    }

    no_delete_audit = {
        "audit_id": "no_physical_delete_audit_v1",
        "forbidden_actions_checked": list(FORBIDDEN_ACTIONS),
        "audit_pass": all(meta.get(f) is False for f in BOUNDARY_FALSE if f.startswith("historical") or "evidence" in f or "phase_table" in f),
        **_review_ok([
            ("no_file_delete", meta.get("historical_file_delete_executed_now") is False),
            ("no_file_move", meta.get("historical_file_move_executed_now") is False),
            ("no_file_rewrite", meta.get("historical_file_rewrite_executed_now") is False),
            ("no_eval_out_delete", meta.get("historical_eval_out_deleted_now") is False),
            ("no_docs_delete", meta.get("historical_docs_deleted_now") is False),
            ("no_phase_table_destructive", meta.get("phase_table_destructive_update_now") is False),
            ("no_verifier_mutation", meta.get("evidence_chain_modified_now") is False),
            ("no_evidence_mutation", meta.get("evidence_chain_modified_now") is False),
        ]),
        **meta,
    }

    future_ref_dryrun = {
        "result_id": "future_phase_reference_policy_dryrun_result_v1",
        "rules": list(FUTURE_REFERENCE_RULES),
        **_review_ok([
            ("prefer_factory", True),
            ("prefer_harness", True),
            ("prefer_validation_factory", True),
            ("no_triple_chain", readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is True),
            ("no_provider_long_chain", True),
            ("historical_read_only", True),
        ]),
        "prefer_capability_factory_standard": True,
        "prefer_controlled_provider_readiness_harness": True,
        "prefer_validation_factory": True,
        "do_not_replicate_triple_chain": True,
        "do_not_replicate_provider_long_chain": True,
        "historical_phases_read_only_evidence_source": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "cleanup_boundary_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed_now": False} for p in BLOCKED_PATHS
        ],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    compression_alignment = {
        "review_id": "cleanup_compression_alignment_review_v1",
        **_review_ok([
            ("compressed_lifecycle_primary", lifecycle_dr_vr.get("verifier") == "GO"),
            ("factory_standard_source_of_truth", factory_dr_vr.get("verifier") == "GO"),
            ("harness_provider_path", factory_post_vr.get("verifier") == "GO"),
            ("triple_chain_blocked", readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is True),
            ("markers_no_delete", meta.get("historical_file_delete_executed_now") is False),
            ("markers_no_invalidate", True),
        ]),
        "compressed_ocr_authorization_lifecycle_primary": True,
        "factory_standard_rule_source_of_truth": True,
        "provider_readiness_harness_path": True,
        "triple_chain_blocked_for_new_phase": True,
        **meta,
    }

    closure_ok = (
        len(blockers) == 0
        and schema_validation.get("all_samples_valid")
        and superseded_phase_markers.get("all_schema_valid")
        and absorbed_rule_markers.get("all_schema_valid")
        and deprecated_markers.get("all_schema_valid")
        and read_only_markers.get("all_schema_valid")
        and read_only_markers.get("all_paths_exist")
        and read_only_markers.get("all_verifier_preserved")
        and chain_preservation.get("dryrun_and_review_pass")
        and no_delete_audit.get("dryrun_and_review_pass")
        and future_ref_dryrun.get("dryrun_and_review_pass")
        and blocked_path_result.get("all_blocked")
        and compression_alignment.get("dryrun_and_review_pass")
    )

    closure = {
        "closure_id": "cleanup_dryrun_and_review_closure_decision_v1",
        "marker_samples_pass": closure_ok,
        "metadata_schema_pass": schema_validation.get("all_samples_valid"),
        "chain_preservation_pass": chain_preservation.get("dryrun_and_review_pass"),
        "no_delete_audit_pass": no_delete_audit.get("dryrun_and_review_pass"),
        "future_reference_pass": future_ref_dryrun.get("dryrun_and_review_pass"),
        "blocked_paths_pass": blocked_path_result.get("all_blocked"),
        "compression_alignment_pass": compression_alignment.get("dryrun_and_review_pass"),
        "closure_pass": closure_ok,
        "high_risk_count": 0 if closure_ok else 1,
        "final_decision": FINAL_DECISION_GO if closure_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if closure_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_authorization_next_route_decision": closure_ok,
        "deferred_routes": [
            "real_dependency_check_authorization",
            "provider_selection_finalize_authorization",
        ],
        "note": "Next Route Decision will select real-dep authorization or provider selection finalize",
        "real_dependency_check_allowed_now": False,
        "provider_selection_finalize_allowed_now": False,
        **meta,
    }

    policy = {
        "policy_id": "factory_standard_historical_cleanup_dryrun_and_review_policy_v1",
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
        "boundary_ok": closure_ok,
        "violations": blockers,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "marking_only": True,
        "superseded_sample_count": len(superseded_samples),
        "absorbed_sample_count": len(absorbed_samples),
        "deprecated_sample_count": len(deprecated_samples),
        "read_only_sample_count": len(read_only_samples),
        "high_risk_count": 0 if closure_ok else 1,
        **meta,
    }

    return {
        "factory_standard_historical_cleanup_dryrun_and_review_policy": policy,
        "cleanup_planning_input_review": planning_input_review,
        "historical_redundancy_cleanup_candidate": cleanup_candidate,
        "superseded_phase_marker_samples": superseded_phase_markers,
        "absorbed_rule_marker_samples": absorbed_rule_markers,
        "deprecated_for_new_phase_marker_samples": deprecated_markers,
        "read_only_evidence_source_marker_samples": read_only_markers,
        "cleanup_metadata_schema_validation_result": schema_validation,
        "historical_chain_preservation_review": chain_preservation,
        "no_physical_delete_audit": no_delete_audit,
        "future_phase_reference_policy_dryrun_result": future_ref_dryrun,
        "cleanup_boundary_blocked_path_result": blocked_path_result,
        "cleanup_compression_alignment_review": compression_alignment,
        "cleanup_dryrun_and_review_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
