# -*- coding: utf-8 -*-
"""Capability Factory Admission and Operation Standard Planning v1 — rule consolidation only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import EVIDENCE_REQUIREMENTS
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Capability-Factory-Admission-and-Operation-Standard-Planning-v1-001"
SCOPE = "capability_factory_standard_planning_only"
SOURCE_CHAIN = "capability_factory_admission_and_operation_standard_planning_v1"
STANDARD_ID = "capability_factory_admission_and_operation_standard_v1"

FINAL_DECISION_GO = (
    "CAPABILITY_FACTORY_ADMISSION_AND_OPERATION_STANDARD_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "CAPABILITY_FACTORY_ADMISSION_AND_OPERATION_STANDARD_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Capability-Factory-Admission-and-Operation-Standard-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Capability-Factory-Issue-Review-v1-001"

LIFECYCLE_STATES: Tuple[str, ...] = (
    "planned",
    "candidate_ready",
    "formal_artifact_planned",
    "formal_artifact_candidate_ready",
    "formal_artifact_generated_later",
    "review_pending_later",
    "sent_later",
    "grant_pending_later",
    "grant_issued_later",
    "execution_window_opened_later",
    "execution_completed_later",
    "post_execution_review_required",
    "closed",
)

BOUNDARY_STANDARD_BLOCKED: Tuple[str, ...] = (
    "candidate_to_fact",
    "candidate_to_user_output",
    "candidate_to_memory_write",
    "candidate_to_world_model_write",
    "readiness_to_provider_invocation",
    "planning_to_execution",
    "dryrun_to_execution",
    "request_candidate_to_send",
    "artifact_candidate_to_grant",
    "grant_candidate_to_execution_window",
    "execution_window_candidate_to_provider_call",
)

NON_CLAIM_CHAIN: Tuple[str, ...] = (
    "planned ≠ generated",
    "candidate ≠ formal artifact",
    "formal artifact ≠ persisted",
    "persisted ≠ sent",
    "sent ≠ grant",
    "grant ≠ execution window opened",
    "execution window opened ≠ provider invocation",
    "provider invocation ≠ fact",
    "fact ≠ user output",
)

NON_CLAIMS: Tuple[str, ...] = (
    *NON_CLAIM_CHAIN,
    "Factory Standard Planning GO ≠ factory standard runtime enforced",
    "Standard planning ≠ formal artifact generated",
    "Standard adoption ≠ Midplatform consumption",
    "DryRunAndReview next ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "factory_standard_generated_now",
    "factory_standard_runtime_enforced_now",
    "formal_request_artifact_generated_now",
    "authorization_request_sent_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "provider_invoked_now",
    "real_dependency_check_executed_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

SOURCE_PHASE_INVENTORY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_id": "Phase-OCR-Provider-Authorization-Planning-v1-001",
        "rule_categories": ("lifecycle", "boundary", "approval_grant", "sandbox_rollback", "evidence"),
    },
    {
        "phase_id": "Phase-OCR-Provider-Authorization-DryRun-v1-001",
        "rule_categories": ("candidate", "lifecycle", "boundary", "evidence"),
    },
    {
        "phase_id": "Phase-OCR-Provider-Authorization-Request-Planning-v1-001",
        "rule_categories": ("artifact", "lifecycle", "boundary", "validation"),
    },
    {
        "phase_id": "Phase-OCR-Provider-Authorization-Request-DryRun-v1-001",
        "rule_categories": ("candidate", "artifact", "boundary", "evidence"),
    },
    {
        "phase_id": "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Post-DryRun-Review-v1-001",
        "rule_categories": ("provider_machine", "upstream_downstream", "boundary"),
    },
    {
        "phase_id": "Phase-Vision-Voice-Provider-Harness-Adoption-Post-DryRun-Review-v1-001",
        "rule_categories": ("provider_machine", "upstream_downstream", "candidate"),
    },
    {
        "phase_id": "Phase-Luna-Validation-Factory-Consolidation-v1-001",
        "rule_categories": ("upstream_downstream", "evidence", "boundary"),
    },
    {
        "phase_id": "Phase-OCR-Controlled-Provider-Readiness-Harness-v1-001",
        "rule_categories": ("provider_machine", "candidate", "boundary"),
    },
)

MERGEABLE_OCR_AUTHORIZATION_PHASES: Tuple[str, ...] = (
    "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-Planning-v1-001",
    "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-Post-DryRun-Review-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-Planning-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Request-Send-Post-DryRun-Review-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-Planning-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-DryRun-v1-001",
    "Phase-OCR-Provider-Authorization-Grant-Post-DryRun-Review-v1-001",
)

STANDALONE_AUTHORIZATION_PHASES: Tuple[str, ...] = (
    "real_dependency_check_authorization",
    "controlled_trial_authorization",
    "provider_selection_finalize_authorization",
    "production_runtime_authorization",
)

COMPRESSED_PATH: Tuple[str, ...] = (
    "Authorization Lifecycle via Factory Standard",
    "Request Candidate",
    "Formal Artifact Candidate",
    "Send Candidate",
    "Grant Candidate",
    "Execution Window Candidate",
    "Review",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "capability_factory_standard_planning_only": True,
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


def run_capability_factory_admission_and_operation_standard_planning_v1(
    *,
    ocr_provider_authorization_request_post_dryrun_review_root: str,
    ocr_provider_authorization_request_dryrun_root: Optional[str] = None,
    ocr_provider_authorization_planning_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    vision_voice_provider_harness_adoption_post_dryrun_review_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    req_post_root = Path(ocr_provider_authorization_request_post_dryrun_review_root).expanduser().resolve()
    req_post_sm = _try_read_json(req_post_root / "summary.json") or {}
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}
    req_post_closure = _try_read_json(req_post_root / "authorization_request_closure_decision_v1.json") or {}

    req_dryrun_root = Path(
        ocr_provider_authorization_request_dryrun_root
        or req_post_root.parent / "ocr_provider_authorization_request_dryrun"
    ).expanduser().resolve()

    auth_planning_root = Path(
        ocr_provider_authorization_planning_root
        or req_post_root.parent / "ocr_provider_authorization_planning"
    ).expanduser().resolve()

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or req_post_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}
    factory_closure = _try_read_json(factory_post_root / "factory_registration_closure_decision_v1.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or req_post_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    harness_sm = _try_read_json(harness_root / "summary.json") or {}

    vision_voice_post_root = Path(
        vision_voice_provider_harness_adoption_post_dryrun_review_root
        or req_post_root.parent / "vision_voice_provider_harness_adoption_post_dryrun_review"
    ).expanduser().resolve()
    vision_voice_post_vr = _try_read_json(vision_voice_post_root / "verifier_report.json") or {}
    vision_voice_closure = _try_read_json(
        vision_voice_post_root / "vision_voice_harness_adoption_closure_decision_v1.json"
    ) or {}

    validation_factory_root = Path(
        luna_validation_factory_consolidation_root
        or req_post_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()
    validation_factory_vr = _try_read_json(validation_factory_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_request_post_dryrun_review_root": str(req_post_root),
        "upstream_request_dryrun_root": str(req_dryrun_root),
        "upstream_authorization_planning_root": str(auth_planning_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_harness_root": str(harness_root),
        "upstream_vision_voice_post_review_root": str(vision_voice_post_root),
        "upstream_validation_factory_root": str(validation_factory_root),
        "output_root": str(out_root),
    }

    req_post_go = req_post_vr.get("verifier") == "GO" and req_post_vr.get("passed") is True
    if not req_post_go:
        blockers.append("OCR Authorization Request Post-DryRun Review verifier must be GO")
    if req_post_sm.get("final_decision") != REQUEST_POST_REVIEW_FINAL_GO:
        blockers.append("request post-dryrun review final_decision mismatch")
    if req_post_closure.get("ocr_provider_authorization_request_dryrun_closed") is not True:
        blockers.append("ocr_provider_authorization_request_dryrun_closed must be true")
    if req_post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if req_post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("lifecycle must be request_artifact_candidate_ready")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("ControlledProviderReadinessHarness Factory Registration Post-Review must be GO")
    if factory_closure.get("validation_factory_registry_candidate_trusted") is not True:
        blockers.append("Validation Factory registry candidate must be trusted")
    if factory_closure.get("controlled_provider_readiness_harness_seventh_module_candidate_trusted") is not True:
        blockers.append("ControlledProviderReadinessHarness 7th module candidate must be trusted")

    if vision_voice_post_vr.get("verifier") != "GO":
        blockers.append("Vision/Voice harness adoption post-review must be GO")
    if vision_voice_closure.get("ocr_vision_voice_three_consumer_harness_validated") is not True:
        blockers.append("OCR/Vision/Voice three consumer validation required")

    if validation_factory_vr.get("verifier") != "GO":
        blockers.append("Luna Validation Factory consolidation should be GO")

    if harness_sm.get("harness_first_consumer_validated_now") is not True:
        blockers.append("ControlledProviderReadinessHarness first consumer should be validated")

    for field in (
        "formal_request_artifact_generated_now",
        "authorization_request_sent_now",
        "grant_issued_now",
        "execution_window_opened_now",
        "provider_invoked_now",
        "real_dependency_check_executed_now",
    ):
        if req_post_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    inventory = {
        "inventory_id": "source_phase_rule_inventory_v1",
        "source_phases": list(SOURCE_PHASE_INVENTORY),
        "source_phase_count": len(SOURCE_PHASE_INVENTORY),
        "rule_category_coverage": [
            "candidate",
            "artifact",
            "lifecycle",
            "boundary",
            "evidence",
            "approval_grant",
            "sandbox_rollback",
            "provider_machine",
            "upstream_downstream",
        ],
        "consolidation_rationale": (
            "Extract repeated schema/precondition/binding/validation/send-boundary/lifecycle/"
            "blocked-path/non-claims rules into factory-level defaults"
        ),
        **meta,
    }

    candidate_standard = {
        "standard_id": "candidate_standard_v1",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "user_facing_output_allowed": False,
        "source_chain_required": True,
        "ttl_required": True,
        "confidence_candidate_required_when_applicable": True,
        "validation_required_before_promotion": True,
        **meta,
    }

    artifact_standard = {
        "standard_id": "artifact_standard_v1",
        "candidate_not_formal_artifact": True,
        "formal_artifact_generation_requires_explicit_phase": True,
        "generated_artifact_not_persisted": True,
        "persisted_artifact_not_sent": True,
        "required_fields": [
            "schema_version",
            "source_ref",
            "evidence_ref",
            "lifecycle_state",
        ],
        "non_claim_chain": list(NON_CLAIM_CHAIN[:4]),
        **meta,
    }

    lifecycle_standard = {
        "standard_id": "lifecycle_standard_v1",
        "states": list(LIFECYCLE_STATES),
        "state_count": len(LIFECYCLE_STATES),
        "current_authorization_state": CURRENT_REQUEST_DRYRUN_STATE,
        "transitions_require_explicit_phase": True,
        "non_claim_chain": list(NON_CLAIM_CHAIN),
        **meta,
    }

    boundary_standard = {
        "standard_id": "boundary_standard_v1",
        "paths": [{"path_id": p, "blocked": True, "default": True} for p in BOUNDARY_STANDARD_BLOCKED],
        "path_count": len(BOUNDARY_STANDARD_BLOCKED),
        "all_blocked_by_default": True,
        "factory_default_denials": [
            "no import",
            "no install",
            "no download",
            "no invoke",
            "no memory write",
            "no world model write",
            "no user output",
            "no provider selection finalize",
        ],
        **meta,
    }

    evidence_standard = {
        "standard_id": "evidence_standard_v1",
        "required_artifact_types": [
            "source_phase_ref",
            "source_candidate_ref",
            "boundary_audit",
            "validation_result",
            "failure_route_result",
            "rollback_plan_ref",
            "verifier_report",
            "post_execution_review_result",
        ],
        "ocr_authorization_artifacts": list(EVIDENCE_REQUIREMENTS),
        "evidence_candidate_distinction": "evidence candidate ≠ evidence collected",
        **meta,
    }

    approval_grant_standard = {
        "standard_id": "approval_grant_standard_v1",
        "approval_required_later": True,
        "approval_collected_now": False,
        "grant_candidate_not_grant_issued": True,
        "grant_issued_not_execution_window_opened": True,
        "execution_window_opened_not_provider_invocation": True,
        "revocation_condition_required": True,
        "non_claim_chain": list(NON_CLAIM_CHAIN[4:7]),
        **meta,
    }

    sandbox_rollback_standard = {
        "standard_id": "sandbox_rollback_standard_v1",
        "no_production_path_write": True,
        "workspace_controlled_output_only": True,
        "no_global_env_mutation": True,
        "no_untracked_install": True,
        "no_model_download_without_separate_authorization": True,
        "failed_check_does_not_trigger_repair_install_download": True,
        "rollback_required_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    provider_machine_standard = {
        "standard_id": "provider_machine_standard_v1",
        "provider_candidate_id_required": True,
        "provider_domain_required": True,
        "provider_family_required": True,
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "dependency_check_required": True,
        "environment_check_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
        "evidence_package_required": True,
        "validated_consumers": ["ocr", "vision", "voice"],
        "seventh_module_candidate": "controlled_provider_readiness_harness_v1",
        **meta,
    }

    transfer_standard = {
        "standard_id": "upstream_downstream_transfer_standard_v1",
        "upstream_input_contract_required": True,
        "downstream_output_contract_required": True,
        "no_direct_downstream_user_output": True,
        "no_direct_fact_write_path": True,
        "market_validation_required": True,
        "validation_factory_pass_required_before_midplatform_consumption": True,
        **meta,
    }

    role_standard = {
        "standard_id": "factory_role_responsibility_standard_v1",
        "roles": [
            {
                "role_id": "machine",
                "description": "Model / provider runtime unit",
                "may_do": ["candidate emission under harness"],
                "must_not": ["direct user output", "direct fact write", "unauthorized invocation"],
            },
            {
                "role_id": "factory_floor",
                "description": "Capability domain production line",
                "may_do": ["candidate generation", "dryrun simulation", "evidence packaging"],
                "must_not": ["skip lifecycle phase", "bypass boundary audit"],
            },
            {
                "role_id": "validation_factory",
                "description": "Market testing center",
                "may_do": ["registry candidate", "contract validation", "consumer mapping"],
                "must_not": ["runtime enforcement without authorization", "Midplatform direct adoption"],
            },
            {
                "role_id": "midplatform",
                "description": "Market consumption layer",
                "may_do": ["consume validated candidates after factory pass"],
                "must_not": ["accept unvalidated provider output", "direct user output from candidate"],
            },
            {
                "role_id": "consumer",
                "description": "End user",
                "receives": ["validated user-facing output only after full chain"],
            },
        ],
        **meta,
    }

    contract_outline = {
        "outline_id": "factory_standard_contract_outline_v1",
        "standard_name": "Capability Factory Admission and Operation Standard",
        "standard_alias": "Capability Factory Operating Standard",
        "covers": [
            "admission standard",
            "operation standard",
            "role handbook",
        ],
        "nine_standards": [
            "candidate_standard_v1",
            "artifact_standard_v1",
            "lifecycle_standard_v1",
            "boundary_standard_v1",
            "evidence_standard_v1",
            "approval_grant_standard_v1",
            "sandbox_rollback_standard_v1",
            "provider_machine_standard_v1",
            "upstream_downstream_transfer_standard_v1",
        ],
        **meta,
    }

    adoption_plan = {
        "plan_id": "factory_standard_adoption_plan_v1",
        "adopt_via_lifecycle_harness": True,
        "replace_per_phase_rule_duplication": True,
        "first_consumer_chain": "ocr_provider_authorization",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        **meta,
    }

    compression = {
        "assessment_id": "compression_impact_assessment_v1",
        "mergeable_ocr_authorization_phases": list(MERGEABLE_OCR_AUTHORIZATION_PHASES),
        "mergeable_phase_count": len(MERGEABLE_OCR_AUTHORIZATION_PHASES),
        "factory_level_defaults": [
            "non_claim_chain",
            "boundary_false_defaults",
            "blocked_path_defaults",
            "candidate_only_defaults",
            "evidence_package_template",
            "approval_grant_chain",
            "sandbox_rollback_defaults",
        ],
        "standalone_authorization_still_required": list(STANDALONE_AUTHORIZATION_PHASES),
        "proposed_compressed_path": list(COMPRESSED_PATH),
        "estimated_phase_reduction": "3x planning/dryrun/review segments → 1 lifecycle harness pass per artifact type",
        **meta,
    }

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "capability_factory_standard_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ready_for_dryrun_and_review": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "capability_factory_standard_planning_policy_v1",
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
        "standard_id": STANDARD_ID,
        "nine_standard_count": 9,
        "source_phase_count": len(SOURCE_PHASE_INVENTORY),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "capability_factory_standard_planning_policy": policy,
        "source_phase_rule_inventory": inventory,
        "candidate_standard_plan": candidate_standard,
        "artifact_standard_plan": artifact_standard,
        "lifecycle_standard_plan": lifecycle_standard,
        "boundary_standard_plan": boundary_standard,
        "evidence_standard_plan": evidence_standard,
        "approval_grant_standard_plan": approval_grant_standard,
        "sandbox_rollback_standard_plan": sandbox_rollback_standard,
        "provider_machine_standard_plan": provider_machine_standard,
        "upstream_downstream_transfer_standard_plan": transfer_standard,
        "factory_role_responsibility_standard_plan": role_standard,
        "factory_standard_contract_outline": contract_outline,
        "factory_standard_adoption_plan": adoption_plan,
        "compression_impact_assessment": compression,
        "capability_factory_standard_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
