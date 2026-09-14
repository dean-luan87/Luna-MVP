# -*- coding: utf-8 -*-
"""Vision / OCR / Voice Controlled Optimization DryRun v1 — readiness candidates only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.post_health_management_roadmap_decision_v1 import SELECTED_ROUTE
from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    CONSTITUTION_BLOCKS,
    CROSS_CHAIN_DEPS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    REGISTRY_BIND_MODELS,
    REGISTRY_VERSION,
    SCHEMA_VERSION,
)

PHASE_ID = "Phase-Vision-OCR-Voice-Controlled-Optimization-DryRun-v1-001"
SCOPE = "vision_ocr_voice_controlled_optimization_dryrun_only"
SOURCE_CHAIN = "vision_ocr_voice_controlled_optimization_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Voice-Controlled-Optimization-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-OCR-Voice-Controlled-Optimization-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "vision_readiness_to_vision_model_invocation",
    "vision_readiness_to_live_camera",
    "vision_readiness_to_image_read",
    "ocr_readiness_to_paddleocr",
    "ocr_readiness_to_rapidocr",
    "ocr_readiness_to_real_provider",
    "voice_readiness_to_asr_runtime",
    "voice_readiness_to_tts_runtime",
    "speech_response_to_voice_output",
    "transcript_to_task_commit",
    "provider_readiness_to_provider_call",
    "candidate_to_user_output",
    "candidate_to_memory_write",
    "candidate_to_world_model_write",
)

BOUNDARY_FALSE_DRYRUN: Tuple[str, ...] = (
    "controlled_provider_enabled_now",
    "controlled_provider_invoked_now",
    "real_runtime_enabled_now",
    "vision_model_invoked_now",
    "live_camera_enabled_now",
    "arbitrary_image_read_executed_now",
    "image_read_executed_now",
    "ocr_provider_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "real_ocr_provider_invoked_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "voice_output_generated_now",
    "user_facing_output_generated_now",
    "model_runtime_invoked_now",
    "provider_runtime_invoked_now",
    "model_switch_executed_now",
    "task_state_committed_now",
    "speech_response_candidate_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ controlled provider enabled",
    "readiness_candidate ≠ provider invocation",
    "ocr_controlled_provider_readiness_candidate ≠ PaddleOCR/RapidOCR called",
    "voice_boundary_readiness_candidate ≠ ASR/TTS runtime",
    "vision_readiness ≠ live camera or real vision model",
    "health binding dryrun pass ≠ fallback executed",
    "Post-DryRun Review next ≠ OCR provider trial started",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "vision_ocr_voice_controlled_optimization_dryrun_only": True,
        "simulated": True,
        "controlled_optimization_readiness_candidate_generated_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "selected_route": SELECTED_ROUTE,
        "ocr_p0_first": True,
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
        "user_facing_output_allowed": False,
        "write_allowed": False,
        "executed_now": False,
        "timestamp": "dryrun_simulated",
        "ttl": 300,
    }


def run_vision_ocr_voice_controlled_optimization_dryrun_v1(
    *,
    vision_ocr_voice_controlled_optimization_planning_root: str,
    post_health_management_roadmap_decision_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(vision_ocr_voice_controlled_optimization_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    registry_plan = _try_read_json(planning_root / "model_registry_binding_plan_v1.json") or {}

    roadmap_root = Path(
        post_health_management_roadmap_decision_root
        or plan_sm.get("upstream_roadmap_decision_root")
        or planning_root.parent / "post_health_management_roadmap_decision"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or roadmap_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or roadmap_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or roadmap_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    task_post_root = Path(
        task_response_candidate_midplatform_integration_post_dryrun_review_root
        or roadmap_root.parent / "task_response_candidate_midplatform_integration_post_dryrun_review"
    ).expanduser().resolve()
    factory_root = Path(
        luna_validation_factory_consolidation_root
        or roadmap_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "upstream_planning_root": str(planning_root), "output_root": str(out_root)}

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    mm_sm = _try_read_json(mm_post_root / "summary.json") or {}
    task_closure = _try_read_json(task_post_root / "post_dryrun_closure_decision_v1.json") or {}
    factory_sm = _try_read_json(factory_root / "summary.json") or {}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("ocr_p0_first") is not True:
        blockers.append("OCR must be P0 first")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route mismatch")

    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management integration must be closed")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    task_closed = task_closure.get("perception_to_task_response_candidate_hub_closed") is True
    if not task_closed:
        blockers.append("task_response_candidate integration must be closed")
    if factory_sm.get("boundary_ok") is not True:
        blockers.append("validation factory consolidation should be boundary_ok")

    plan_bindings = registry_plan.get("bindings") or []
    for binding in plan_bindings:
        if binding.get("invocation_allowed") is not False:
            blockers.append("planning registry invocation_allowed must be false")
        if binding.get("controlled_provider_entry_generated_now") is True:
            blockers.append("no controlled provider entry in planning")
        if binding.get("real_provider_entry_generated_now") is True:
            blockers.append("no real provider entry in planning")

    input_review = {
        "review_id": "controlled_optimization_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "health_integration_closed": health_sm.get("health_management_integration_dryrun_closed"),
        "b_lite_closed": canonical_sm.get("b_lite_canonical_v0_baseline_closed"),
        "task_response_closed": task_closed,
        "model_governance_consumable": mm_sm.get("governance_skeleton_consumable"),
        "validation_factory_ok": factory_sm.get("boundary_ok"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    vision_readiness = {
        **_candidate_defaults(),
        "result_id": "vision_readiness_candidate_result_v1",
        "candidate_type": "vision_controlled_optimization_readiness_candidate",
        "source_scope": "sample_or_controlled_frame_reference_only",
        "visual_observation_candidate_supported": True,
        "visual_evidence_formatting_ready": True,
        "task_response_linkage_ready": True,
        "controlled_provider_planning_allowed": True,
        "real_vision_model_allowed": False,
        "live_camera_allowed": False,
        "arbitrary_image_read_allowed": False,
        "visual_fact_write_allowed": False,
        "world_model_write_allowed": False,
        **meta,
    }

    ocr_readiness = {
        **_candidate_defaults(),
        "result_id": "ocr_readiness_candidate_result_v1",
        "candidate_type": "ocr_controlled_provider_readiness_candidate",
        "mock_to_controlled_provider_planning_ready": True,
        "ocr_request_candidate_supported": True,
        "roi_candidate_supported": True,
        "ocr_result_candidate_supported": True,
        "ocr_evidence_pack_candidate_supported": True,
        "provider_readiness_candidate_supported": True,
        "timeout_fallback_candidate_supported": True,
        "controlled_provider_planning_allowed": True,
        "p0_priority": 1,
        "paddleocr_allowed": False,
        "rapidocr_allowed": False,
        "real_ocr_provider_allowed": False,
        "ocr_fact_write_allowed": False,
        "user_output_allowed": False,
        **meta,
    }

    voice_readiness = {
        **_candidate_defaults(),
        "result_id": "voice_readiness_candidate_result_v1",
        "candidate_type": "voice_boundary_readiness_candidate",
        "speech_input_candidate_supported": True,
        "transcript_candidate_supported": True,
        "speech_response_candidate_contract_needed": True,
        "asr_tts_boundary_planned": True,
        "interruption_candidate_supported": True,
        "output_arbitration_required": True,
        "controlled_provider_planning_allowed": "partial",
        "real_asr_allowed": False,
        "real_tts_allowed": False,
        "voice_output_allowed": False,
        "user_output_allowed": False,
        **meta,
    }

    cross_chain_rows = [
        {
            "edge_id": edge["edge_id"],
            "from": edge["from"],
            "to": edge["to"],
            "routed": True,
            "executed_now": False,
            "commit_allowed": False,
        }
        for edge in CROSS_CHAIN_DEPS
    ]
    cross_chain = {
        "result_id": "cross_chain_dependency_dryrun_result_v1",
        "edges": cross_chain_rows,
        "edge_count": len(cross_chain_rows),
        "routing_pass": len(cross_chain_rows) == 6,
        **meta,
    }

    registry_rows = []
    registry_issues: List[str] = []
    for mid in REGISTRY_BIND_MODELS:
        plan_row = next((b for b in plan_bindings if b.get("model_id") == mid), None)
        row = {
            "model_id": mid,
            "invocation_allowed": False,
            "provider_type": "mock_or_fixture",
            "runtime_mode_upgraded": False,
            "controlled_provider_entry_generated_now": False,
            "real_provider_entry_generated_now": False,
            "binding_pass": plan_row is not None and plan_row.get("invocation_allowed") is False,
        }
        registry_rows.append(row)
        if not row["binding_pass"]:
            registry_issues.append(mid)

    registry_dryrun = {
        "result_id": "model_registry_binding_dryrun_result_v1",
        "registry_version": REGISTRY_VERSION,
        "bindings": registry_rows,
        "binding_pass": len(registry_issues) == 0,
        "issues": registry_issues,
        **meta,
    }

    health_rows = [
        {
            "trigger": hb["trigger"],
            "target_candidate": hb["target"],
            "routed": True,
            "executed_now": False,
            "automatic_execution": False,
            "health_signal_candidate_only": True,
        }
        for hb in HEALTH_BINDINGS
    ]
    health_dryrun = {
        "result_id": "health_management_binding_dryrun_result_v1",
        "routes": health_rows,
        "route_count": len(health_rows),
        "routing_pass": len(health_rows) == 6,
        "no_automatic_fallback": True,
        "no_model_switch_execution": True,
        **meta,
    }

    constitution_rows = [
        {"block_id": b["block_id"], "blocked": True, "observed_now": False}
        for b in CONSTITUTION_BLOCKS
    ]
    constitution_dryrun = {
        "result_id": "constitution_boundary_dryrun_result_v1",
        "blocks": constitution_rows,
        "all_blocked": True,
        **meta,
    }

    midplatform_dryrun = {
        "result_id": "midplatform_candidate_flow_dryrun_result_v1",
        "candidate_protocol": "candidate_only / not_fact / no_write / no_user_output",
        "task_response_hub": "task_response_candidate",
        "validation_factory_boundary_ok": factory_sm.get("boundary_ok"),
        "flow_pass": factory_sm.get("boundary_ok") is True,
        **meta,
    }

    readiness_matrix = {
        "matrix_id": "controlled_provider_readiness_dryrun_matrix_v1",
        "Vision": {
            "readiness_candidate": "vision_controlled_optimization_readiness_candidate",
            "generated": True,
            "controlled_provider_planning_allowed": True,
            "real_runtime_allowed": False,
        },
        "OCR": {
            "readiness_candidate": "ocr_controlled_provider_readiness_candidate",
            "generated": True,
            "p0_priority": 1,
            "controlled_provider_planning_allowed": True,
            "real_provider_allowed": False,
        },
        "Voice": {
            "readiness_candidate": "voice_boundary_readiness_candidate",
            "generated": True,
            "controlled_provider_planning_allowed": "partial",
            "real_asr_tts_allowed": False,
        },
        "all_three_generated": True,
        **meta,
    }

    boundary_checks = [
        {"check_id": row["check_id"], "field": row["field"], "passed": meta.get(row["field"]) is row["required"]}
        for row in (
            {"check_id": "no_vision_model", "field": "vision_model_invoked_now", "required": False},
            {"check_id": "no_live_camera", "field": "live_camera_enabled_now", "required": False},
            {"check_id": "no_arbitrary_read", "field": "arbitrary_image_read_executed_now", "required": False},
            {"check_id": "no_ocr_provider", "field": "ocr_provider_invoked_now", "required": False},
            {"check_id": "no_paddleocr", "field": "paddleocr_invoked_now", "required": False},
            {"check_id": "no_real_ocr", "field": "real_ocr_provider_invoked_now", "required": False},
            {"check_id": "no_asr", "field": "asr_runtime_invoked_now", "required": False},
            {"check_id": "no_tts", "field": "tts_runtime_invoked_now", "required": False},
            {"check_id": "no_provider_runtime", "field": "provider_runtime_invoked_now", "required": False},
        )
    ]
    boundary_audit = {
        "audit_id": "no_runtime_boundary_audit_v1",
        "checks": boundary_checks,
        "audit_pass": all(c["passed"] for c in boundary_checks),
        **meta,
    }

    blocked_result = {
        "result_id": "blocked_path_result_v1",
        "paths": [{"path_id": p, "blocked": True, "observed_now": False} for p in BLOCKED_PATHS],
        "all_blocked": True,
        **meta,
    }

    all_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and vision_readiness.get("controlled_provider_planning_allowed") is True
        and ocr_readiness.get("mock_to_controlled_provider_planning_ready") is True
        and voice_readiness.get("speech_input_candidate_supported") is True
        and cross_chain.get("routing_pass")
        and registry_dryrun.get("binding_pass")
        and health_dryrun.get("routing_pass")
        and constitution_dryrun.get("all_blocked")
        and midplatform_dryrun.get("flow_pass")
        and boundary_audit.get("audit_pass")
        and blocked_result.get("all_blocked")
        and readiness_matrix.get("all_three_generated")
    )

    readiness_decision = {
        "decision_id": "phased_optimization_readiness_decision_v1",
        "ready_for_post_dryrun_review": all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "ocr_p0_first": True,
        **meta,
    }

    policy = {
        "policy_id": "vision_ocr_voice_controlled_optimization_dryrun_policy_v1",
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
        "high_risk_count": 0 if all_pass else 1,
        **meta,
    }

    return {
        "vision_ocr_voice_controlled_optimization_dryrun_policy": policy,
        "controlled_optimization_planning_input_review": input_review,
        "vision_readiness_candidate_result": vision_readiness,
        "ocr_readiness_candidate_result": ocr_readiness,
        "voice_readiness_candidate_result": voice_readiness,
        "cross_chain_dependency_dryrun_result": cross_chain,
        "model_registry_binding_dryrun_result": registry_dryrun,
        "health_management_binding_dryrun_result": health_dryrun,
        "constitution_boundary_dryrun_result": constitution_dryrun,
        "midplatform_candidate_flow_dryrun_result": midplatform_dryrun,
        "controlled_provider_readiness_dryrun_matrix": readiness_matrix,
        "no_runtime_boundary_audit": boundary_audit,
        "blocked_path_result": blocked_result,
        "phased_optimization_readiness_decision": readiness_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
