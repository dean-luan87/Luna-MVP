# -*- coding: utf-8 -*-
"""Controlled Provider Readiness Harness v1 — reusable provider readiness factory (OCR first consumer)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REAL_DEP_POST_FINAL,
    NEXT_PHASE_GO as REAL_DEP_POST_NEXT,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    CHECK_SEQUENCE,
    FAILURE_HANDLING,
    ROLLBACK_RULES,
)

HARNESS_ID = "controlled_provider_readiness_harness_v1"
HARNESS_MODULE = "capabilities.governance.controlled_provider_readiness_harness_v1"

PHASE_ID = "Phase-OCR-Controlled-Provider-Readiness-Harness-v1-001"
SCOPE = "controlled_provider_readiness_harness_extraction_only"
SOURCE_CHAIN = "controlled_provider_readiness_harness_v1"

UPSTREAM_POST_REVIEW_FINAL = REAL_DEP_POST_FINAL
UPSTREAM_POST_REVIEW_NEXT = REAL_DEP_POST_NEXT

FINAL_DECISION_GO = "CONTROLLED_PROVIDER_READINESS_HARNESS_CLOSED_READY_FOR_OCR_PROVIDER_NEXT_ROADMAP_DECISION"
FINAL_DECISION_HOLD = "CONTROLLED_PROVIDER_READINESS_HARNESS_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Next-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Controlled-Provider-Readiness-Harness-Issue-Review-v1-001"

HARNESS_PHASES: Tuple[str, ...] = (
    "provider_candidate_inventory",
    "provider_selection_candidate",
    "dependency_readiness_candidate",
    "environment_readiness_candidate",
    "provider_comparison_sample",
    "real_dependency_check_plan",
    "real_dependency_check_dryrun",
    "evidence_package_candidate",
    "failure_route_candidate",
    "rollback_plan_candidate",
    "no_import_no_install_no_download_boundary",
    "authorization_readiness",
    "controlled_trial_readiness_later",
)

PROVIDER_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "provider_candidate_id",
    "provider_domain",
    "provider_family",
    "provider_status",
    "invocation_allowed",
    "authorization_required",
    "dependency_check_required",
    "environment_check_required",
    "controlled_trial_required",
    "health_binding_required",
    "constitution_gate_required",
    "output_contract",
    "evidence_package_required",
)

DEPENDENCY_READINESS_FIELDS: Tuple[str, ...] = (
    "package_check_planned",
    "cache_check_planned",
    "file_existence_check_planned",
    "file_hash_check_planned",
    "import_check_planned",
    "smoke_check_planned",
    "sample_execution_check_planned_later",
    "all_executed_now",
)

ENVIRONMENT_READINESS_FIELDS: Tuple[str, ...] = (
    "runtime_environment_requirement",
    "virtualenv_or_sandbox_required",
    "cache_directory_planned",
    "output_directory_planned",
    "readonly_fixture_directory_planned_later",
    "cpu_memory_guard_planned",
    "timeout_guard_planned",
    "network_dependency_default",
    "production_path_write_allowed",
)

EVIDENCE_SLOTS: Tuple[str, ...] = (
    "environment_snapshot_candidate",
    "runtime_version_snapshot_candidate",
    "package_presence_result_candidate",
    "import_result_candidate",
    "cache_result_candidate",
    "file_hash_result_candidate",
    "smoke_check_result_candidate",
    "sample_execution_result_later_candidate",
    "boundary_audit_result_candidate",
    "verifier_report_candidate",
)

BOUNDARY_BLOCKED_DEFAULT: Tuple[str, ...] = (
    "planning_to_dependency_check_execution",
    "dryrun_to_dependency_check_execution",
    "dependency_plan_to_dependency_install",
    "cache_plan_to_model_download",
    "provider_import_plan_to_import_execution",
    "provider_comparison_to_execution_selection",
    "provider_readiness_to_provider_invocation",
    "sample_execution_plan_to_execution",
    "candidate_to_fact_write",
    "candidate_to_user_output",
    "candidate_to_memory_write",
    "candidate_to_world_model_write",
)

OCR_CANDIDATE_FAMILIES: Tuple[str, ...] = (
    "mock_or_fixture",
    "paddleocr_later",
    "rapidocr_later",
    "external_ocr_later",
)

FUTURE_CONSUMERS: Tuple[Dict[str, Any], ...] = (
    {"consumer_id": "vision_provider_readiness", "domain": "vision", "status": "planned"},
    {"consumer_id": "voice_asr_tts_provider_readiness", "domain": "voice", "status": "planned"},
    {"consumer_id": "map_provider_readiness", "domain": "map", "status": "planned"},
    {"consumer_id": "library_provider_readiness", "domain": "library", "status": "planned"},
    {"consumer_id": "hive_provider_readiness", "domain": "hive", "status": "planned"},
    {"consumer_id": "memory_provider_readiness", "domain": "memory", "status": "planned"},
)

ANTI_RECURSION: Tuple[str, ...] = (
    "Do not regenerate full Provider Selection → Dependency → Environment → Real-Dep Planning/DryRun/Review per domain",
    "Subsequent domains must use ControlledProviderReadinessHarness contracts first",
    "Per domain only: domain_config + harness_validation_result + readiness_decision",
    "OCR-specific provider families must not auto-migrate to Vision/Voice without domain_config",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Harness extraction GO ≠ global harness runtime enforcement",
    "harness contract complete ≠ real dependency check executed",
    "OCR first consumer validated ≠ PaddleOCR enabled",
    "future consumer plan ≠ Vision/Voice runtime enabled",
    "harness closed ≠ OCR provider authorization granted",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "harness_runtime_enforced_globally_now",
    "provider_readiness_harness_invoked_for_runtime_now",
    "real_dependency_check_executed_now",
    "provider_import_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_smoke_check_executed_now",
    "sample_provider_execution_now",
    "provider_selection_finalized_now",
    "provider_authorization_started_now",
    "controlled_trial_started_now",
    "provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "future_consumer_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)


def _harness_meta() -> Dict[str, Any]:
    meta = {
        "controlled_provider_readiness_harness_extraction_only": True,
        "harness_contract_generated_now": True,
        "harness_first_consumer_validated_now": True,
        "harness_id": HARNESS_ID,
        "harness_module": HARNESS_MODULE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["harness_runtime_enforced_globally_now"] = False
    meta["future_consumer_runtime_enabled_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def build_harness_usage_guide_markdown() -> str:
    return """# Controlled Provider Readiness Harness v1 — Usage Guide

## Purpose

Reusable governance factory for **provider candidate → selection → dependency → environment → comparison → real dependency check → evidence → failure/rollback → boundary → authorization** without duplicating long Planning/DryRun/Review chains per domain.

**OCR** is the first validated consumer. Vision, Voice, Map, Library, Hive, Memory adopt via `domain_config` only.

## Anti-recursion

1. Do **not** copy the full OCR provider selection / real dependency check phase chain for each new domain.
2. Register `domain_config` and run harness validation once per domain.
3. Open real runtime / import / install only after explicit authorization phases.

## Per-domain minimum outputs

- `domain_config` (provider_domain, candidates, output_contract, blocked_providers)
- `harness_validation_result` (from `run_validate_first_consumer` or equivalent)
- `readiness_decision` + `verifier_report`

## OCR first consumer (reference)

| Field | OCR value |
|-------|-----------|
| provider_domain | ocr |
| candidates | mock_or_fixture, paddleocr_later, rapidocr_later, external_ocr_later |
| output_contract | ocr_result_candidate |
| evidence_pack | ocr_evidence_pack_candidate |
| blocked at planning/dryrun | PaddleOCR, RapidOCR, real OCR import/invoke |

## Future adoption

Set `future_consumer_adoption_requires_config=true`. Map domain-specific fields in `domain_config`; do not inherit OCR package names or cache paths automatically.

## Forbidden in harness-only phases

- Real dependency check execution
- pip install / model download
- provider import / smoke / sample execution
- provider selection finalize
- controlled trial without authorization

## Module

`capabilities.governance.controlled_provider_readiness_harness_v1`

Harness ID: `controlled_provider_readiness_harness_v1`
"""


def _real_dep_step_contracts() -> List[Dict[str, Any]]:
    labels = (
        "environment isolation check",
        "package presence check",
        "cache directory check",
        "file existence check",
        "file hash check",
        "provider import check",
        "provider initialization dry check",
        "runtime smoke check",
        "sample execution check later",
    )
    steps: List[Dict[str, Any]] = []
    for i, spec in enumerate(CHECK_SEQUENCE):
        steps.append(
            {
                "step_order": i + 1,
                "step_id": spec["step_id"],
                "step_name": labels[i] if i < len(labels) else spec["step_label"],
                "precondition": spec["precondition"],
                "execution_allowed_later": True,
                "current_executed_now": False,
                "evidence_required": True,
                "failure_route": spec["failure_route"],
                "rollback_required": bool(spec["rollback_required"]),
                "blocked_now": True,
            }
        )
    return steps


def run_controlled_provider_readiness_harness_extraction_v1(
    *,
    ocr_provider_real_dependency_check_post_dryrun_review_root: str,
    ocr_provider_real_dependency_check_dryrun_root: Optional[str] = None,
    ocr_provider_real_dependency_check_planning_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_dryrun_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    real_post = Path(ocr_provider_real_dependency_check_post_dryrun_review_root).expanduser().resolve()
    real_post_sm = _try_read_json(real_post / "summary.json") or {}
    real_post_vr = _try_read_json(real_post / "verifier_report.json") or {}
    real_post_closure = _try_read_json(real_post / "real_dependency_check_closure_decision_v1.json") or {}
    next_route = _try_read_json(real_post / "next_route_readiness_decision_v1.json") or {}

    real_dryrun_root = Path(
        ocr_provider_real_dependency_check_dryrun_root
        or real_post.parent / "ocr_provider_real_dependency_check_dryrun"
    ).resolve()
    sel_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or real_post.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or real_post.parent / "ocr_controlled_provider_post_dryrun_review"
    ).resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_harness_meta(), "upstream_real_dep_post_review_root": str(real_post), "output_root": str(out_root)}

    sel_post_sm = _try_read_json(sel_post_root / "summary.json") or {}
    ocr_post_sm = _try_read_json(ocr_post_root / "summary.json") or {}
    real_dryrun_sm = _try_read_json(real_dryrun_root / "summary.json") or {}

    post_go = real_post_vr.get("verifier") == "GO" and real_post_vr.get("passed") is True
    if not post_go:
        blockers.append("real dependency post-review verifier must be GO")
    if real_post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-review final_decision mismatch")
    if real_post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-review recommended_next_phase mismatch")
    if next_route.get("ready_for_controlled_provider_readiness_harness") is not True:
        blockers.append("ready_for_controlled_provider_readiness_harness required")
    if next_route.get("do_not_execute_real_dependency_check_now") is not True:
        blockers.append("do_not_execute_real_dependency_check_now required")
    if real_post_sm.get("real_dependency_check_flow_trusted") is not True:
        blockers.append("real_dependency_check_flow_trusted required")
    evidence_trusted = (
        real_post_closure.get("evidence_package_candidate_trusted") is True
        or real_post_sm.get("evidence_package_candidate_trusted") is True
    )
    if not evidence_trusted:
        blockers.append("evidence_package_candidate_trusted required")

    if sel_post_sm.get("ocr_provider_selection_dependency_environment_dryrun_closed") is not True:
        blockers.append("OCR selection dryrun must be closed")
    if ocr_post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("OCR controlled provider dryrun must be closed")

    for field in (
        "paddleocr_imported_now",
        "rapidocr_invoked_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
        "provider_invoked_now",
    ):
        if real_dryrun_sm.get(field) is True or real_post_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")

    input_review = {
        "review_id": "ocr_first_consumer_input_review_v1",
        "upstream_real_dep_post_root": str(real_post),
        "upstream_selection_post_root": str(sel_post_root),
        "upstream_ocr_controlled_post_root": str(ocr_post_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": real_post_sm.get("final_decision"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "controlled_provider_readiness_harness_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "harness_id": HARNESS_ID,
        "first_consumer": "ocr",
        "extraction_goals": list(HARNESS_PHASES),
        **meta,
    }

    harness_contract = {
        "contract_id": "controlled_provider_readiness_harness_contract_v1",
        "harness_id": HARNESS_ID,
        "harness_module": HARNESS_MODULE,
        "phases": list(HARNESS_PHASES),
        "phase_count": len(HARNESS_PHASES),
        "anti_recursion_rules": list(ANTI_RECURSION),
        "sub_contracts": [
            "provider_candidate_contract_v1",
            "dependency_readiness_contract_v1",
            "environment_readiness_contract_v1",
            "provider_comparison_matrix_contract_v1",
            "real_dependency_check_contract_v1",
            "provider_evidence_package_contract_v1",
            "provider_failure_route_contract_v1",
            "provider_rollback_contract_v1",
            "provider_boundary_guard_contract_v1",
            "provider_authorization_readiness_contract_v1",
        ],
        **meta,
    }

    provider_candidate_contract = {
        "contract_id": "provider_candidate_contract_v1",
        "required_fields": list(PROVIDER_CANDIDATE_FIELDS),
        "defaults": {
            "provider_status": "planned_candidate",
            "invocation_allowed": False,
            "authorization_required": True,
            "dependency_check_required": True,
            "environment_check_required": True,
            "controlled_trial_required": True,
            "health_binding_required": True,
            "constitution_gate_required": True,
            "evidence_package_required": True,
        },
        **meta,
    }

    dependency_contract = {
        "contract_id": "dependency_readiness_contract_v1",
        "required_fields": list(DEPENDENCY_READINESS_FIELDS),
        "defaults": {"all_executed_now": False},
        "planned_flags": {
            "package_check_planned": True,
            "cache_check_planned": True,
            "file_existence_check_planned": True,
            "file_hash_check_planned": True,
            "import_check_planned": True,
            "smoke_check_planned": True,
            "sample_execution_check_planned_later": True,
        },
        **meta,
    }

    environment_contract = {
        "contract_id": "environment_readiness_contract_v1",
        "required_fields": list(ENVIRONMENT_READINESS_FIELDS),
        "defaults": {
            "virtualenv_or_sandbox_required": True,
            "network_dependency_default": False,
            "production_path_write_allowed": False,
        },
        **meta,
    }

    comparison_contract = {
        "contract_id": "provider_comparison_matrix_contract_v1",
        "comparison_sample_only": True,
        "comparison_result_does_not_finalize_provider": True,
        "dimension_config_required_per_domain": True,
        **meta,
    }

    real_dep_contract = {
        "contract_id": "real_dependency_check_contract_v1",
        "step_count": 9,
        "steps": _real_dep_step_contracts(),
        "all_current_executed_now_false": True,
        **meta,
    }

    evidence_contract = {
        "contract_id": "provider_evidence_package_contract_v1",
        "evidence_slots": list(EVIDENCE_SLOTS),
        "slot_count": len(EVIDENCE_SLOTS),
        "evidence_collected_now_default": False,
        "evidence_only_output": True,
        **meta,
    }

    failure_contract = {
        "contract_id": "provider_failure_route_contract_v1",
        "routes": list(FAILURE_HANDLING),
        "route_count": len(FAILURE_HANDLING),
        "executed_now_default": False,
        **meta,
    }

    rollback_contract = {
        "contract_id": "provider_rollback_contract_v1",
        "rules": list(ROLLBACK_RULES),
        "rollback_executed_now_default": False,
        "failed_check_does_not_trigger_install": True,
        **meta,
    }

    boundary_contract = {
        "contract_id": "provider_boundary_guard_contract_v1",
        "default_blocked_paths": list(BOUNDARY_BLOCKED_DEFAULT),
        "path_count": len(BOUNDARY_BLOCKED_DEFAULT),
        "all_blocked_by_default": True,
        **meta,
    }

    auth_contract = {
        "contract_id": "provider_authorization_readiness_contract_v1",
        "real_dependency_check_authorization_required": True,
        "provider_authorization_required_before_invocation": True,
        "controlled_trial_readiness_later": True,
        "authorization_granted_now_default": False,
        **meta,
    }

    ocr_mapping = {
        "mapping_id": "ocr_first_consumer_mapping_v1",
        "provider_domain": "ocr",
        "first_consumer_status": "validated",
        "provider_candidate_families": list(OCR_CANDIDATE_FAMILIES),
        "output_contract": "ocr_result_candidate",
        "evidence_pack_contract": "ocr_evidence_pack_candidate",
        "blocked_providers_at_planning_dryrun": [
            "paddleocr",
            "rapidocr",
            "external_ocr",
            "real_ocr_provider",
        ],
        "upstream_artifacts_mapped": {
            "selection_post_review": str(sel_post_root),
            "real_dep_post_review": str(real_post),
            "controlled_provider_post_review": str(ocr_post_root),
        },
        "mapping_pass": len(blockers) == 0,
        **meta,
    }

    future_plan = {
        "plan_id": "future_consumer_adoption_plan_v1",
        "consumers": list(FUTURE_CONSUMERS),
        "future_consumer_runtime_enabled_now": False,
        "future_consumer_adoption_requires_config": True,
        "no_automatic_migration_of_ocr_specific_fields": True,
        **meta,
    }

    validation = {
        "validation_id": "controlled_provider_readiness_harness_validation_result_v1",
        "harness_contract_complete": len(blockers) == 0,
        "ocr_first_consumer_validated": len(blockers) == 0 and ocr_mapping.get("mapping_pass"),
        "no_runtime_boundary_preserved": True,
        "no_provider_invocation": True,
        "no_install_download_import": True,
        "harness_global_enforcement_now": False,
        "validation_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    extraction_ok = validation.get("validation_pass") is True and input_review.get("review_pass") is True
    boundary_ok = extraction_ok

    decision = {
        "decision_id": "controlled_provider_readiness_harness_decision_v1",
        "extraction_pass": extraction_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
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
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "harness_id": HARNESS_ID,
        **meta,
    }

    return {
        "controlled_provider_readiness_harness_policy": policy,
        "ocr_first_consumer_input_review": input_review,
        "controlled_provider_readiness_harness_contract": harness_contract,
        "provider_candidate_contract": provider_candidate_contract,
        "dependency_readiness_contract": dependency_contract,
        "environment_readiness_contract": environment_contract,
        "provider_comparison_matrix_contract": comparison_contract,
        "real_dependency_check_contract": real_dep_contract,
        "provider_evidence_package_contract": evidence_contract,
        "provider_failure_route_contract": failure_contract,
        "provider_rollback_contract": rollback_contract,
        "provider_boundary_guard_contract": boundary_contract,
        "provider_authorization_readiness_contract": auth_contract,
        "ocr_first_consumer_mapping": ocr_mapping,
        "future_consumer_adoption_plan": future_plan,
        "harness_usage_guide_markdown": build_harness_usage_guide_markdown(),
        "controlled_provider_readiness_harness_validation_result": validation,
        "controlled_provider_readiness_harness_decision": decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
