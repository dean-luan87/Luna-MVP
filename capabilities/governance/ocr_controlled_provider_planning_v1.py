# -*- coding: utf-8 -*-
"""OCR Controlled Provider Planning v1 — planning-only, no real OCR provider."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    REGISTRY_VERSION,
    SCHEMA_VERSION,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as VOV_POST_FINAL_GO,
    NEXT_PHASE_GO as VOV_POST_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Controlled-Provider-Planning-v1-001"
SCOPE = "ocr_controlled_provider_planning_only"
SOURCE_CHAIN = "ocr_controlled_provider_planning_v1"

UPSTREAM_POST_FINAL = VOV_POST_FINAL_GO
UPSTREAM_POST_NEXT = VOV_POST_NEXT_PHASE

FINAL_DECISION_GO = "OCR_CONTROLLED_PROVIDER_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "OCR_CONTROLLED_PROVIDER_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Controlled-Provider-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Controlled-Provider-Issue-Review-v1-001"

OCR_MODEL_ID = "ocr_model_mock"

OCR_ALLOWED: Tuple[str, ...] = (
    "controlled_provider_candidate",
    "ocr_request_candidate",
    "roi_candidate",
    "ocr_result_candidate",
    "ocr_evidence_pack_candidate",
    "provider_readiness_candidate",
    "timeout_fallback_candidate",
    "source_chain",
    "provenance",
    "confidence_candidate",
    "ttl",
)

OCR_FORBIDDEN: Tuple[str, ...] = (
    "paddleocr_invocation",
    "rapidocr_invocation",
    "real_ocr_provider_invocation",
    "ocr_fact_generation",
    "direct_world_model_write",
    "direct_memory_write",
    "direct_user_output",
    "task_commit",
)

PROVIDER_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "provider_candidate_id": "ocr_provider_mock_fixture",
        "provider_family": "mock_or_fixture",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "controlled_trial_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
        "output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_paddleocr_later",
        "provider_family": "paddleocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "controlled_trial_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
        "output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_rapidocr_later",
        "provider_family": "rapidocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "controlled_trial_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
        "output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_external_later",
        "provider_family": "external_ocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "controlled_trial_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
        "output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
    },
)

OCR_REQUEST_FIELDS: Tuple[str, ...] = (
    "request_id",
    "source_visual_candidate_ref",
    "source_frame_ref",
    "roi_ref",
    "requested_provider_candidate_ref",
    "request_scope",
    "text_region_expected",
    "ttl",
    "source_chain",
    "candidate_only",
    "submit_allowed",
    "provider_invocation_allowed",
)

ROI_FIELDS: Tuple[str, ...] = (
    "roi_id",
    "source_frame_ref",
    "bbox_or_region_ref",
    "crop_ref_optional",
    "confidence_candidate",
    "reason_for_ocr",
    "ttl",
    "source_chain",
    "candidate_only",
    "image_read_allowed",
)

OCR_RESULT_FIELDS: Tuple[str, ...] = (
    "ocr_result_candidate_id",
    "provider_candidate_ref",
    "provider_type",
    "text_candidate",
    "confidence_candidate",
    "source_roi_ref",
    "source_request_ref",
    "ttl",
    "source_chain",
    "candidate_only",
    "fact_status",
    "write_allowed",
    "user_facing_output_allowed",
)

EVIDENCE_PACK_FIELDS: Tuple[str, ...] = (
    "evidence_pack_candidate_id",
    "ocr_request_ref",
    "roi_ref",
    "ocr_result_ref",
    "provider_readiness_ref",
    "source_chain",
    "provenance",
    "confidence_candidate",
    "ttl",
    "validation_required",
    "candidate_only",
    "fact_status",
    "world_model_write_allowed",
    "memory_write_allowed",
)

HEALTH_BINDINGS: Tuple[Dict[str, str], ...] = (
    {"trigger": "provider_timeout", "target": "hold_candidate"},
    {"trigger": "provider_failed", "target": "fallback_candidate"},
    {"trigger": "low_confidence", "target": "reobserve_or_retry_candidate"},
    {"trigger": "empty_result", "target": "retry_or_hold_candidate"},
    {"trigger": "unsupported_region", "target": "fallback_to_visual_candidate"},
    {"trigger": "runtime_boundary_violation", "target": "block_candidate"},
)

CONSTITUTION_BLOCKS: Tuple[Dict[str, Any], ...] = (
    {"block_id": "ocr_request_candidate_to_provider_call", "blocked": True},
    {"block_id": "ocr_result_candidate_to_fact", "blocked": True},
    {"block_id": "ocr_result_candidate_to_user_output", "blocked": True},
    {"block_id": "ocr_result_candidate_to_world_model_write", "blocked": True},
    {"block_id": "ocr_result_candidate_to_memory_write", "blocked": True},
    {"block_id": "ocr_evidence_pack_candidate_to_scene_delta", "blocked": True},
    {"block_id": "provider_readiness_candidate_to_invocation", "blocked": True},
)

NO_RUNTIME_CHECKS: Tuple[Dict[str, str], ...] = (
    {"check_id": "provider_planned_not_enabled", "rule": "provider planned ≠ provider enabled"},
    {"check_id": "request_contract_not_submitted", "rule": "OCRRequest contract ≠ request submitted"},
    {"check_id": "roi_not_image_read", "rule": "ROI contract ≠ image read/crop executed"},
    {"check_id": "result_not_provider_invoked", "rule": "OCR result contract ≠ OCR provider invoked"},
    {"check_id": "evidence_not_fact", "rule": "Evidence pack contract ≠ fact/evidence generated"},
    {"check_id": "readiness_not_provider_call", "rule": "provider readiness ≠ provider call"},
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_controlled_provider_enabled_now",
    "ocr_controlled_provider_invoked_now",
    "ocr_provider_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "real_ocr_provider_invoked_now",
    "ocr_model_invoked_now",
    "model_runtime_invoked_now",
    "provider_runtime_invoked_now",
    "ocr_request_submitted_now",
    "ocr_evidence_pack_generated_now",
    "ocr_fact_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "user_facing_output_generated_now",
    "tts_invoked_now",
    "task_state_committed_now",
    "fallback_executed_now",
    "retry_executed_now",
    "provider_switch_executed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ OCR controlled provider enabled",
    "Planning GO ≠ PaddleOCR/RapidOCR invoked",
    "provider_readiness_candidate ≠ provider invocation",
    "OCRRequest candidate ≠ request submitted",
    "OCR result candidate ≠ OCR fact",
    "evidence pack candidate ≠ WorldModel/Memory write",
    "health binding planned ≠ fallback/retry executed",
    "DryRun next ≠ real OCR provider call",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_controlled_provider_planning_only": True,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "ocr_model_id": OCR_MODEL_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _contract_defaults() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "user_facing_output_allowed": False,
        "submit_allowed": False,
        "provider_invocation_allowed": False,
    }


def run_ocr_controlled_provider_planning_v1(
    *,
    vision_ocr_voice_controlled_optimization_post_dryrun_review_root: str,
    vision_ocr_voice_controlled_optimization_dryrun_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(vision_ocr_voice_controlled_optimization_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_route = _try_read_json(post_root / "next_route_readiness_decision_v1.json") or {}

    dryrun_root = Path(
        vision_ocr_voice_controlled_optimization_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "vision_ocr_voice_controlled_optimization_dryrun"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or post_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or post_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or post_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()
    task_post_root = Path(
        task_response_candidate_midplatform_integration_post_dryrun_review_root
        or post_root.parent / "task_response_candidate_midplatform_integration_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "upstream_post_review_root": str(post_root), "output_root": str(out_root)}

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    ocr_readiness = _try_read_json(dryrun_root / "ocr_readiness_candidate_result_v1.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    mm_sm = _try_read_json(mm_post_root / "summary.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}
    task_closure = _try_read_json(task_post_root / "post_dryrun_closure_decision_v1.json") or {}

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_NEXT:
        blockers.append("post-review recommended_next_phase mismatch")
    if post_sm.get("controlled_optimization_dryrun_closed") is not True:
        blockers.append("controlled_optimization_dryrun_closed required")
    if post_sm.get("three_chain_readiness_trusted") is not True:
        blockers.append("three_chain_readiness_trusted required")
    if next_route.get("preferred_next_chain") != "OCR":
        blockers.append("preferred_next_chain must be OCR")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("controlled optimization dryrun verifier should be GO")
    if ocr_readiness.get("mock_to_controlled_provider_planning_ready") is not True:
        blockers.append("OCR mock_to_controlled_provider_planning_ready required")
    for flag in (
        "ocr_request_candidate_supported",
        "roi_candidate_supported",
        "ocr_result_candidate_supported",
        "ocr_evidence_pack_candidate_supported",
        "provider_readiness_candidate_supported",
    ):
        if ocr_readiness.get(flag) is not True:
            blockers.append(f"OCR readiness {flag} required")
    for flag in ("paddleocr_allowed", "rapidocr_allowed", "real_ocr_provider_allowed"):
        if ocr_readiness.get(flag) is not False:
            blockers.append(f"OCR {flag} must be false")

    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management must be closed")
    if task_closure.get("perception_to_task_response_candidate_hub_closed") is not True:
        blockers.append("task_response_candidate integration must be closed")
    if mm_sm.get("governance_skeleton_consumable") is not True:
        blockers.append("model governance skeleton should be consumable")

    input_review = {
        "review_id": "upstream_controlled_optimization_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "controlled_optimization_dryrun_closed": post_sm.get("controlled_optimization_dryrun_closed"),
        "three_chain_readiness_trusted": post_sm.get("three_chain_readiness_trusted"),
        "ocr_readiness_ready": ocr_readiness.get("mock_to_controlled_provider_planning_ready"),
        "b_lite_closed": canonical_sm.get("b_lite_canonical_v0_baseline_closed"),
        "health_closed": health_sm.get("health_management_integration_dryrun_closed"),
        "task_response_closed": task_closure.get("perception_to_task_response_candidate_hub_closed"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    scope = {
        "scope_id": "ocr_controlled_provider_scope_v1",
        "allowed_now": list(OCR_ALLOWED),
        "forbidden_now": list(OCR_FORBIDDEN),
        "path": "mock/fixture ocr_result_candidate → controlled provider candidate planning",
        **meta,
    }

    provider_registry = {
        "plan_id": "ocr_provider_candidate_registry_plan_v1",
        "registry_version": REGISTRY_VERSION,
        "bound_model_id": OCR_MODEL_ID,
        "providers": list(PROVIDER_CANDIDATES),
        "provider_count": len(PROVIDER_CANDIDATES),
        "all_invocation_allowed_false": True,
        **meta,
    }

    admission_gate = {
        "plan_id": "ocr_provider_admission_gate_plan_v1",
        "gates": [
            "provider_status=planned_candidate",
            "invocation_allowed=false",
            "controlled_trial_required=true",
            "health_binding_required=true",
            "constitution_gate_required=true",
            "evidence_pack_required=true",
            "no_paddleocr_or_rapidocr_in_planning",
        ],
        "admission_pass_in_planning": True,
        **meta,
    }

    request_contract = {
        "contract_id": "ocr_request_candidate_contract_v1",
        "artifact_type": "ocr_request_candidate",
        "fields": list(OCR_REQUEST_FIELDS),
        "defaults": {
            **_contract_defaults(),
            "submit_allowed": False,
            "provider_invocation_allowed": False,
        },
        **meta,
    }

    roi_contract = {
        "contract_id": "ocr_roi_candidate_contract_v1",
        "artifact_type": "roi_candidate",
        "fields": list(ROI_FIELDS),
        "defaults": {
            **_contract_defaults(),
            "image_read_allowed": False,
        },
        **meta,
    }

    result_contract = {
        "contract_id": "ocr_result_candidate_contract_v1",
        "artifact_type": "ocr_result_candidate",
        "fields": list(OCR_RESULT_FIELDS),
        "defaults": _contract_defaults(),
        **meta,
    }

    evidence_contract = {
        "contract_id": "ocr_evidence_pack_candidate_contract_v1",
        "artifact_type": "ocr_evidence_pack_candidate",
        "fields": list(EVIDENCE_PACK_FIELDS),
        "defaults": {
            **_contract_defaults(),
            "validation_required": True,
            "world_model_write_allowed": False,
            "memory_write_allowed": False,
        },
        **meta,
    }

    timeout_fallback = {
        "plan_id": "ocr_timeout_fallback_plan_v1",
        "branches": [
            {"condition": "provider_timeout", "candidate": "hold_candidate"},
            {"condition": "provider_failed", "candidate": "fallback_candidate"},
            {"condition": "low_confidence", "candidate": "reobserve_or_retry_candidate"},
            {"condition": "empty_result", "candidate": "retry_or_hold_candidate"},
            {"condition": "unsupported_region", "candidate": "fallback_to_visual_candidate"},
            {"condition": "runtime_boundary_violation", "candidate": "block_candidate"},
        ],
        "executed_now": False,
        **meta,
    }

    health_plan = {
        "plan_id": "ocr_health_binding_plan_v1",
        "bindings": list(HEALTH_BINDINGS),
        "constraints": [
            "fallback_executed_now=false",
            "retry_executed_now=false",
            "provider_switch_executed_now=false",
            "health_signal_candidate_only",
        ],
        **meta,
    }

    constitution_plan = {
        "plan_id": "ocr_constitution_boundary_plan_v1",
        "blocks": list(CONSTITUTION_BLOCKS),
        "all_blocked_in_planning": True,
        **meta,
    }

    midplatform_flow = {
        "plan_id": "ocr_midplatform_flow_binding_plan_v1",
        "flow": [
            "visual_observation_candidate",
            "ocr_request_candidate",
            "roi_candidate",
            "ocr_result_candidate",
            "ocr_evidence_pack_candidate",
            "task_response_candidate (later)",
        ],
        "candidate_only_throughout": True,
        **meta,
    }

    boundary_checks = [{**c, "passed": True} for c in NO_RUNTIME_CHECKS]
    boundary_matrix = {
        "matrix_id": "ocr_no_runtime_boundary_matrix_v1",
        "checks": boundary_checks,
        "all_pass": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "ocr_controlled_provider_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "generate provider_readiness_candidate",
            "generate OCRRequest / ROI / OCR result / evidence pack candidate samples",
            "verify timeout/fallback/low_confidence/empty_result branches",
            "verify all provider invocations blocked",
            "no PaddleOCR / RapidOCR / real provider",
        ],
        **meta,
    }

    planning_ok = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and boundary_matrix.get("all_pass")
        and len(PROVIDER_CANDIDATES) >= 4
    )

    decision = {
        "decision_id": "ocr_controlled_provider_planning_decision_v1",
        "planning_pass": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    non_claims = {
        "register_id": "ocr_controlled_provider_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    policy = {
        "policy_id": "ocr_controlled_provider_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "high_risk_count": 0 if planning_ok else 1,
        **meta,
    }

    return {
        "ocr_controlled_provider_planning_policy": policy,
        "upstream_controlled_optimization_review_input_review": input_review,
        "ocr_controlled_provider_scope": scope,
        "ocr_provider_candidate_registry_plan": provider_registry,
        "ocr_provider_admission_gate_plan": admission_gate,
        "ocr_request_candidate_contract": request_contract,
        "ocr_roi_candidate_contract": roi_contract,
        "ocr_result_candidate_contract": result_contract,
        "ocr_evidence_pack_candidate_contract": evidence_contract,
        "ocr_timeout_fallback_plan": timeout_fallback,
        "ocr_health_binding_plan": health_plan,
        "ocr_constitution_boundary_plan": constitution_plan,
        "ocr_midplatform_flow_binding_plan": midplatform_flow,
        "ocr_no_runtime_boundary_matrix": boundary_matrix,
        "ocr_controlled_provider_dryrun_plan": dryrun_plan,
        "ocr_controlled_provider_non_claims_register": non_claims,
        "ocr_controlled_provider_planning_decision": decision,
        "summary": summary,
    }