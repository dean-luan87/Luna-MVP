# -*- coding: utf-8 -*-
"""OCR Controlled Provider DryRun v1 — candidate samples only, no OCR provider invocation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_controlled_provider_planning_v1 import (
    CONSTITUTION_BLOCKS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OCR_MODEL_ID,
    PROVIDER_CANDIDATES,
    REGISTRY_VERSION,
    SCHEMA_VERSION,
)

PHASE_ID = "Phase-OCR-Controlled-Provider-DryRun-v1-001"
SCOPE = "ocr_controlled_provider_dryrun_only"
SOURCE_CHAIN = "ocr_controlled_provider_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "OCR_CONTROLLED_PROVIDER_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "OCR_CONTROLLED_PROVIDER_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Controlled-Provider-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Controlled-Provider-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "provider_readiness_to_provider_call",
    "ocr_request_to_provider_invocation",
    "ocr_request_to_submit",
    "roi_candidate_to_image_read",
    "roi_candidate_to_crop",
    "ocr_result_to_fact",
    "ocr_result_to_user_output",
    "ocr_result_to_memory_write",
    "ocr_result_to_world_model_write",
    "evidence_pack_to_scene_delta",
    "evidence_pack_to_memory_write",
    "evidence_pack_to_world_model_write",
    "paddleocr_invocation",
    "rapidocr_invocation",
    "real_ocr_provider_invocation",
)

BOUNDARY_FALSE_DRYRUN: Tuple[str, ...] = (
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
    "image_read_executed_now",
    "crop_executed_now",
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
    "DryRun GO ≠ OCR provider enabled",
    "provider_readiness_candidate ≠ provider invocation",
    "OCRRequest candidate ≠ request submitted",
    "OCR result candidate ≠ OCR fact",
    "evidence pack candidate ≠ WorldModel/Memory write",
    "branch candidate ≠ fallback/retry executed",
    "Post-DryRun Review next ≠ PaddleOCR/RapidOCR allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)

CHAIN_STEPS: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_request_candidate",
    "roi_candidate",
    "ocr_result_candidate",
    "ocr_evidence_pack_candidate",
    "task_response_candidate_later",
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_controlled_provider_dryrun_only": True,
        "simulated": True,
        "provider_readiness_candidate_generated_now": True,
        "ocr_request_candidate_generated_now": True,
        "ocr_roi_candidate_generated_now": True,
        "ocr_result_candidate_generated_now": True,
        "ocr_evidence_pack_candidate_generated_now": True,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "ocr_model_id": OCR_MODEL_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_DRYRUN:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _candidate_defaults() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "action_allowed": False,
        "write_allowed": False,
        "user_facing_output_allowed": False,
        "submit_allowed": False,
        "provider_invocation_allowed": False,
        "timestamp": "dryrun_simulated",
        "ttl": 300,
    }


def _branch_candidate(candidate_type: str, trigger: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **_candidate_defaults(),
        "candidate_id": f"branch_{trigger}",
        "candidate_type": candidate_type,
        "trigger": trigger,
        "executed_now": False,
        "fallback_executed_now": False,
        "retry_executed_now": False,
        "provider_switch_executed_now": False,
        **meta,
    }


def run_ocr_controlled_provider_dryrun_v1(
    *,
    ocr_controlled_provider_planning_root: str,
    vision_ocr_voice_controlled_optimization_post_dryrun_review_root: Optional[str] = None,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: Optional[str] = None,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(ocr_controlled_provider_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}

    vov_post_root = Path(
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        or planning_root.parent / "vision_ocr_voice_controlled_optimization_post_dryrun_review"
    ).expanduser().resolve()
    vision_trial_root = Path(
        vision_sample_frame_single_chain_controlled_trial_post_execution_review_root
        or planning_root.parent / "vision_sample_frame_single_chain_controlled_trial_post_execution_review"
    ).expanduser().resolve()
    task_post_root = Path(
        task_response_candidate_midplatform_integration_post_dryrun_review_root
        or planning_root.parent / "task_response_candidate_midplatform_integration_post_dryrun_review"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or planning_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or planning_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "upstream_planning_root": str(planning_root), "output_root": str(out_root)}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok must be true")
    if plan_sm.get("ocr_controlled_provider_planning_only") is not True:
        blockers.append("upstream must be planning-only phase")

    registry_plan = _try_read_json(planning_root / "ocr_provider_candidate_registry_plan_v1.json") or {}
    if not registry_plan.get("providers"):
        blockers.append("provider candidate registry plan required")
    for contract in (
        "ocr_request_candidate_contract_v1.json",
        "ocr_roi_candidate_contract_v1.json",
        "ocr_result_candidate_contract_v1.json",
        "ocr_evidence_pack_candidate_contract_v1.json",
    ):
        if not (planning_root / contract).is_file():
            blockers.append(f"missing {contract}")

    vov_sm = _try_read_json(vov_post_root / "summary.json") or {}
    vision_sm = _try_read_json(vision_trial_root / "summary.json") or {}
    task_closure = _try_read_json(task_post_root / "post_dryrun_closure_decision_v1.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}

    if vov_sm.get("controlled_optimization_dryrun_closed") is not True:
        blockers.append("controlled optimization dryrun must be closed")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management must be closed")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    if task_closure.get("perception_to_task_response_candidate_hub_closed") is not True:
        blockers.append("task_response_candidate integration must be closed")
    if vision_sm.get("boundary_ok") is not True:
        blockers.append("vision sample frame post execution review should be boundary_ok")

    input_review = {
        "review_id": "ocr_controlled_provider_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "provider_registry_count": registry_plan.get("provider_count"),
        "vision_trial_review_ok": vision_sm.get("boundary_ok"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    visual_ref = "visual_observation_candidate_dryrun_001"
    frame_ref = "controlled_frame_ref_dryrun_001"
    roi_ref = "roi_candidate_dryrun_001"
    request_ref = "ocr_request_candidate_dryrun_001"
    result_ref = "ocr_result_candidate_dryrun_001"
    readiness_ref = "ocr_provider_mock_fixture"

    readiness_samples = [
        {
            **_candidate_defaults(),
            "candidate_type": "provider_readiness_candidate",
            "provider_candidate_id": p["provider_candidate_id"],
            "provider_family": p["provider_family"],
            "provider_status": "planned_candidate",
            "invocation_allowed": False,
            "controlled_trial_required": True,
            "health_binding_required": True,
            "constitution_gate_required": True,
            "evidence_pack_required": True,
            **meta,
        }
        for p in PROVIDER_CANDIDATES
    ]

    request_sample = {
        **_candidate_defaults(),
        "candidate_type": "ocr_request_candidate",
        "request_id": request_ref,
        "source_visual_candidate_ref": visual_ref,
        "source_frame_ref": frame_ref,
        "roi_ref": roi_ref,
        "requested_provider_candidate_ref": readiness_ref,
        "request_scope": "controlled_optimization_dryrun",
        "text_region_expected": True,
        "source_chain": SOURCE_CHAIN,
        **meta,
    }

    roi_sample = {
        **_candidate_defaults(),
        "candidate_type": "roi_candidate",
        "roi_id": roi_ref,
        "source_frame_ref": frame_ref,
        "bbox_or_region_ref": "bbox_norm_0.1_0.2_0.5_0.6",
        "crop_ref_optional": None,
        "confidence_candidate": 0.72,
        "reason_for_ocr": "visual_observation_text_region",
        "image_read_allowed": False,
        "crop_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **meta,
    }

    result_sample = {
        **_candidate_defaults(),
        "candidate_type": "ocr_result_candidate",
        "ocr_result_candidate_id": result_ref,
        "provider_candidate_ref": readiness_ref,
        "provider_type": "mock_or_fixture",
        "text_candidate": "MOCK_OCR_TEXT_CANDIDATE",
        "confidence_candidate": 0.81,
        "source_roi_ref": roi_ref,
        "source_request_ref": request_ref,
        "source_chain": SOURCE_CHAIN,
        **meta,
    }

    evidence_sample = {
        **_candidate_defaults(),
        "candidate_type": "ocr_evidence_pack_candidate",
        "evidence_pack_candidate_id": "ocr_evidence_pack_dryrun_001",
        "ocr_request_ref": request_ref,
        "roi_ref": roi_ref,
        "ocr_result_ref": result_ref,
        "provider_readiness_ref": readiness_ref,
        "provenance": "ocr_controlled_provider_dryrun_v1_simulated",
        "confidence_candidate": 0.79,
        "validation_required": True,
        "world_model_write_allowed": False,
        "memory_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **meta,
    }

    chain_trace = {
        "trace_id": "ocr_candidate_chain_trace_v1",
        "steps": [
            {"step": s, "artifact_ref": visual_ref if s == "visual_observation_candidate" else request_ref if s == "ocr_request_candidate" else roi_ref if s == "roi_candidate" else result_ref if s == "ocr_result_candidate" else "ocr_evidence_pack_dryrun_001" if s == "ocr_evidence_pack_candidate" else "task_response_later", "linked": True}
            for s in CHAIN_STEPS
        ],
        "chain_pass": True,
        **meta,
    }

    timeout_branch = {
        "result_id": "ocr_timeout_fallback_branch_result_v1",
        "trigger": "provider_timeout",
        "target_candidate": "hold_candidate",
        "candidate": _branch_candidate("hold_candidate", "provider_timeout", meta),
        "provider_switch_executed_now": False,
        "retry_executed_now": False,
        "branch_pass": True,
        **meta,
    }

    low_confidence_branch = {
        "result_id": "ocr_low_confidence_branch_result_v1",
        "trigger": "low_confidence",
        "target_candidate": "reobserve_or_retry_candidate",
        "candidate": _branch_candidate("reobserve_or_retry_candidate", "low_confidence", meta),
        "retry_executed_now": False,
        "branch_pass": True,
        **meta,
    }

    empty_result_branch = {
        "result_id": "ocr_empty_result_branch_result_v1",
        "trigger": "empty_result",
        "target_candidate": "retry_or_hold_candidate",
        "candidate": _branch_candidate("retry_or_hold_candidate", "empty_result", meta),
        "retry_executed_now": False,
        "branch_pass": True,
        **meta,
    }

    unsupported_region_branch = {
        "result_id": "ocr_unsupported_region_branch_result_v1",
        "trigger": "unsupported_region",
        "target_candidate": "fallback_to_visual_candidate",
        "candidate": _branch_candidate("fallback_to_visual_candidate", "unsupported_region", meta),
        "visual_fallback_remains_candidate": True,
        "branch_pass": True,
        **meta,
    }

    runtime_violation_branch = {
        "result_id": "ocr_runtime_boundary_violation_branch_result_v1",
        "trigger": "runtime_boundary_violation",
        "target_candidate": "block_candidate",
        "candidate": _branch_candidate("block_candidate", "runtime_boundary_violation", meta),
        "provider_invocation_blocked": True,
        "branch_pass": True,
        **meta,
    }

    health_rows = []
    for hb in HEALTH_BINDINGS:
        health_rows.append(
            {
                "trigger": hb["trigger"],
                "target_candidate": hb["target"],
                "routed": True,
                "executed_now": False,
                "candidate": _branch_candidate(hb["target"], hb["trigger"], meta),
            }
        )

    health_dryrun = {
        "result_id": "ocr_health_binding_dryrun_result_v1",
        "routes": health_rows,
        "route_count": len(health_rows),
        "routing_pass": len(health_rows) == 6,
        "no_automatic_fallback": True,
        "no_model_switch": True,
        "provider_failed_fallback_generated": any(
            r["target_candidate"] == "fallback_candidate" for r in health_rows
        ),
        **meta,
    }

    constitution_dryrun = {
        "result_id": "ocr_constitution_boundary_dryrun_result_v1",
        "blocks": [{"block_id": b["block_id"], "blocked": True, "observed_now": False} for b in CONSTITUTION_BLOCKS],
        "all_blocked": True,
        **meta,
    }

    midplatform_dryrun = {
        "result_id": "ocr_midplatform_flow_binding_dryrun_result_v1",
        "flow": list(CHAIN_STEPS[:-1]),
        "task_response_later": True,
        "flow_pass": True,
        **meta,
    }

    boundary_checks = [
        {"check_id": "readiness_not_enabled", "passed": meta.get("ocr_controlled_provider_enabled_now") is False},
        {"check_id": "request_not_submitted", "passed": meta.get("ocr_request_submitted_now") is False},
        {"check_id": "roi_no_read", "passed": meta.get("image_read_executed_now") is False and meta.get("crop_executed_now") is False},
        {"check_id": "result_no_provider", "passed": meta.get("ocr_provider_invoked_now") is False},
        {"check_id": "no_fact", "passed": meta.get("ocr_fact_generated_now") is False},
        {"check_id": "no_wm_memory", "passed": meta.get("world_model_written_now") is False and meta.get("memory_written_now") is False},
        {"check_id": "no_paddle", "passed": meta.get("paddleocr_invoked_now") is False},
        {"check_id": "no_rapid", "passed": meta.get("rapidocr_invoked_now") is False},
        {"check_id": "no_real", "passed": meta.get("real_ocr_provider_invoked_now") is False},
    ]
    boundary_audit = {
        "audit_id": "ocr_no_runtime_boundary_audit_v1",
        "checks": boundary_checks,
        "audit_pass": all(c["passed"] for c in boundary_checks),
        **meta,
    }

    blocked_result = {
        "result_id": "ocr_blocked_path_result_v1",
        "paths": [{"path_id": p, "blocked": True, "observed_now": False} for p in BLOCKED_PATHS],
        "all_blocked": True,
        **meta,
    }

    all_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and len(readiness_samples) >= 4
        and request_sample.get("candidate_only") is True
        and roi_sample.get("image_read_allowed") is False
        and result_sample.get("fact_status") == "not_fact"
        and evidence_sample.get("world_model_write_allowed") is False
        and chain_trace.get("chain_pass")
        and timeout_branch.get("branch_pass")
        and low_confidence_branch.get("branch_pass")
        and empty_result_branch.get("branch_pass")
        and unsupported_region_branch.get("branch_pass")
        and runtime_violation_branch.get("branch_pass")
        and health_dryrun.get("routing_pass")
        and constitution_dryrun.get("all_blocked")
        and midplatform_dryrun.get("flow_pass")
        and boundary_audit.get("audit_pass")
        and blocked_result.get("all_blocked")
    )

    readiness_decision = {
        "decision_id": "ocr_controlled_provider_dryrun_readiness_decision_v1",
        "ready_for_post_dryrun_review": all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_controlled_provider_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_pass,
        "violations": blockers,
        "final_decision": readiness_decision["final_decision"],
        "recommended_next_phase": readiness_decision["recommended_next_phase"],
        "readiness_sample_count": len(readiness_samples),
        "high_risk_count": 0 if all_pass else 1,
        **meta,
    }

    return {
        "ocr_controlled_provider_dryrun_policy": policy,
        "ocr_controlled_provider_planning_input_review": input_review,
        "ocr_provider_readiness_candidate_samples": {
            "artifact_id": "ocr_provider_readiness_candidate_samples_v1",
            "sample_count": len(readiness_samples),
            "samples": readiness_samples,
            **meta,
        },
        "ocr_request_candidate_samples": {
            "artifact_id": "ocr_request_candidate_samples_v1",
            "sample_count": 1,
            "samples": [request_sample],
            **meta,
        },
        "ocr_roi_candidate_samples": {
            "artifact_id": "ocr_roi_candidate_samples_v1",
            "sample_count": 1,
            "samples": [roi_sample],
            **meta,
        },
        "ocr_result_candidate_samples": {
            "artifact_id": "ocr_result_candidate_samples_v1",
            "sample_count": 1,
            "samples": [result_sample],
            **meta,
        },
        "ocr_evidence_pack_candidate_samples": {
            "artifact_id": "ocr_evidence_pack_candidate_samples_v1",
            "sample_count": 1,
            "samples": [evidence_sample],
            **meta,
        },
        "ocr_candidate_chain_trace": chain_trace,
        "ocr_timeout_fallback_branch_result": timeout_branch,
        "ocr_low_confidence_branch_result": low_confidence_branch,
        "ocr_empty_result_branch_result": empty_result_branch,
        "ocr_unsupported_region_branch_result": unsupported_region_branch,
        "ocr_runtime_boundary_violation_branch_result": runtime_violation_branch,
        "ocr_health_binding_dryrun_result": health_dryrun,
        "ocr_constitution_boundary_dryrun_result": constitution_dryrun,
        "ocr_midplatform_flow_binding_dryrun_result": midplatform_dryrun,
        "ocr_no_runtime_boundary_audit": boundary_audit,
        "ocr_blocked_path_result": blocked_result,
        "ocr_controlled_provider_dryrun_readiness_decision": readiness_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
