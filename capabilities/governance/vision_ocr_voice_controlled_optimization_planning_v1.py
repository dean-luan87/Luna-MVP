# -*- coding: utf-8 -*-
"""Vision / OCR / Voice Controlled Optimization Planning v1 — planning-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    REGISTRY_VERSION,
    SCHEMA_VERSION,
    V0_MODEL_IDS,
)
from capabilities.governance.post_health_management_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Vision-OCR-Voice-Controlled-Optimization-Planning-v1-001"
SCOPE = "vision_ocr_voice_controlled_optimization_planning_only"
SOURCE_CHAIN = "vision_ocr_voice_controlled_optimization_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Voice-Controlled-Optimization-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-OCR-Voice-Controlled-Optimization-Issue-Review-v1-001"

REGISTRY_BIND_MODELS: Tuple[str, ...] = (
    "vision_perspective_model_mock",
    "ocr_model_mock",
    "voice_asr_model_mock",
    "voice_tts_model_mock",
)

VISION_ALLOWED: Tuple[str, ...] = (
    "sample_frame_reference",
    "controlled_frame_reference",
    "visual_observation_candidate",
    "visual_candidate_quality_review",
    "visual_evidence_formatting",
    "visual_candidate_to_task_response_candidate_linkage",
)

VISION_FORBIDDEN: Tuple[str, ...] = (
    "live_camera",
    "arbitrary_image_read",
    "real_vision_model_invocation",
    "visual_fact_write",
    "world_model_write",
)

OCR_ALLOWED: Tuple[str, ...] = (
    "ocr_mock_to_controlled_provider_planning",
    "ocr_request_candidate",
    "roi_candidate",
    "ocr_result_candidate",
    "ocr_evidence_pack_candidate",
    "provider_readiness_candidate",
    "timeout_fallback_candidate",
)

OCR_FORBIDDEN: Tuple[str, ...] = (
    "paddleocr_invocation",
    "rapidocr_invocation",
    "real_ocr_provider_invocation",
    "ocr_fact_write",
    "direct_world_model_write",
    "direct_user_output",
)

VOICE_ALLOWED: Tuple[str, ...] = (
    "speech_input_candidate",
    "transcript_candidate",
    "speech_response_candidate",
    "asr_tts_boundary",
    "voice_interruption_candidate",
    "voice_output_arbitration_plan",
    "tts_readiness_candidate",
)

VOICE_FORBIDDEN: Tuple[str, ...] = (
    "asr_runtime",
    "tts_runtime",
    "real_voice_output",
    "user_facing_output",
    "direct_emotional_expression_output",
)

CROSS_CHAIN_DEPS: Tuple[Dict[str, str], ...] = (
    {
        "edge_id": "vision_to_ocr",
        "from": "Vision",
        "to": "OCR",
        "rule": "visual_observation_candidate triggers OCRRequest candidate",
    },
    {
        "edge_id": "ocr_to_task",
        "from": "OCR",
        "to": "Task",
        "rule": "ocr_result_candidate enters task_response_candidate",
    },
    {
        "edge_id": "nav_task_to_voice",
        "from": "Navigation/Task",
        "to": "Voice",
        "rule": "speech_response_candidate later only — no TTS now",
    },
    {
        "edge_id": "voice_to_task",
        "from": "Voice",
        "to": "Task",
        "rule": "transcript_candidate may enter task layer — no commit",
    },
    {
        "edge_id": "health_to_all",
        "from": "Health",
        "to": "Vision/OCR/Voice",
        "rule": "provider timeout / model degraded / runtime disabled → fallback/hold/degradation candidate",
    },
    {
        "edge_id": "constitution_to_all",
        "from": "Constitution",
        "to": "all",
        "rule": "candidate must not escalate to fact/action/TTS/write",
    },
)

HEALTH_BINDINGS: Tuple[Dict[str, str], ...] = (
    {"trigger": "vision_model_timeout", "target": "fallback_candidate"},
    {"trigger": "ocr_provider_timeout", "target": "hold_candidate"},
    {"trigger": "voice_asr_failed", "target": "clarification_or_hold_candidate"},
    {"trigger": "voice_tts_disabled", "target": "no_voice_output_candidate"},
    {"trigger": "low_resource", "target": "lower_cost_model_candidate"},
    {"trigger": "runtime_boundary_violation", "target": "block_candidate"},
)

CONSTITUTION_BLOCKS: Tuple[Dict[str, str], ...] = (
    {"block_id": "visual_candidate_to_fact", "blocked": True},
    {"block_id": "ocr_candidate_to_fact", "blocked": True},
    {"block_id": "transcript_candidate_to_task_commit", "blocked": True},
    {"block_id": "speech_response_candidate_to_tts", "blocked": True},
    {"block_id": "any_candidate_to_user_output", "blocked": True},
    {"block_id": "any_candidate_to_memory_world_write", "blocked": True},
    {"block_id": "provider_ready_candidate_to_provider_call", "blocked": True},
)

NO_RUNTIME_BOUNDARY: Tuple[Dict[str, Any], ...] = (
    {"check_id": "no_vision_model", "field": "vision_model_invoked_now", "required": False},
    {"check_id": "no_live_camera", "field": "live_camera_enabled_now", "required": False},
    {"check_id": "no_image_read", "field": "image_read_executed_now", "required": False},
    {"check_id": "no_ocr_provider", "field": "ocr_provider_invoked_now", "required": False},
    {"check_id": "no_paddleocr", "field": "paddleocr_invoked_now", "required": False},
    {"check_id": "no_rapidocr", "field": "rapidocr_invoked_now", "required": False},
    {"check_id": "no_asr", "field": "asr_runtime_invoked_now", "required": False},
    {"check_id": "no_tts", "field": "tts_runtime_invoked_now", "required": False},
    {"check_id": "no_voice_output", "field": "voice_output_generated_now", "required": False},
    {"check_id": "no_user_output", "field": "user_facing_output_generated_now", "required": False},
    {"check_id": "no_model_runtime", "field": "model_runtime_invoked_now", "required": False},
    {"check_id": "no_provider_runtime", "field": "provider_runtime_invoked_now", "required": False},
)

PHASED_ROADMAP: Tuple[Dict[str, Any], ...] = (
    {
        "phase_id": "P0",
        "priority_order": 1,
        "items": [
            "OCR controlled provider planning (P0 first — easiest controlled validation, candidate-only output)",
            "Vision sample/controlled frame quality planning",
            "Voice speech candidate boundary planning",
        ],
    },
    {
        "phase_id": "P1",
        "items": [
            "OCR controlled provider dryrun",
            "Vision controlled sample dryrun",
            "Voice ASR transcript candidate dryrun",
        ],
    },
    {
        "phase_id": "P2",
        "items": [
            "OCR provider controlled trial",
            "Vision provider controlled trial",
            "Voice interruption / TTS candidate dryrun",
        ],
    },
    {
        "phase_id": "P3",
        "items": ["limited runtime planning"],
    },
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "controlled_optimization_started_now",
    "real_runtime_enabled_now",
    "vision_model_invoked_now",
    "live_camera_enabled_now",
    "image_read_executed_now",
    "ocr_provider_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "voice_output_generated_now",
    "user_facing_output_generated_now",
    "model_runtime_invoked_now",
    "provider_runtime_invoked_now",
    "model_switch_executed_now",
    "task_state_committed_now",
    "memory_written_now",
    "world_model_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ Vision/OCR/Voice optimization started",
    "Controlled optimization planning ≠ controlled provider enabled",
    "Provider readiness candidate ≠ provider invocation",
    "speech_response_candidate ≠ TTS",
    "transcript_candidate ≠ task commit",
    "visual_observation_candidate ≠ visual fact",
    "ocr_result_candidate ≠ OCR fact",
    "health binding planned ≠ fallback executed",
    "model registry binding planned ≠ model invocation allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/vision_ocr_voice_controlled_optimization_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "vision_ocr_voice_controlled_optimization_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "defer_health_metric_baseline_planning": True,
        "defer_hardware_lifespan_alert_planning": True,
        "defer_robustness_baseline_planning": True,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_vision_ocr_voice_controlled_optimization_planning_v1(
    *,
    post_health_management_roadmap_decision_root: str,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: Optional[str] = None,
    midplatform_minimal_backbone_post_dryrun_review_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roadmap_root = Path(post_health_management_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}

    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or roadmap_sm.get("upstream_post_dryrun_review_root")
        or roadmap_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or roadmap_sm.get("upstream_canonical_post_review_root")
        or roadmap_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or roadmap_sm.get("upstream_model_management_post_review_root")
        or roadmap_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    task_post_root = Path(
        task_response_candidate_midplatform_integration_post_dryrun_review_root
        or roadmap_root.parent / "task_response_candidate_midplatform_integration_post_dryrun_review"
    ).expanduser().resolve()
    backbone_post_root = Path(
        midplatform_minimal_backbone_post_dryrun_review_root
        or roadmap_root.parent / "midplatform_minimal_backbone_post_dryrun_review"
    ).expanduser().resolve()
    factory_root = Path(
        luna_validation_factory_consolidation_root
        or roadmap_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else Path(DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    )
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "output_root": str(out_root),
    }

    health_sm = _try_read_json(health_post_root / "summary.json") or {}
    health_vr = _try_read_json(health_post_root / "verifier_report.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    mm_sm = _try_read_json(mm_post_root / "summary.json") or {}
    task_closure = _try_read_json(task_post_root / "post_dryrun_closure_decision_v1.json") or {}
    task_sm = _try_read_json(task_post_root / "summary.json") or {}
    backbone_sm = _try_read_json(backbone_post_root / "summary.json") or {}
    factory_sm = _try_read_json(factory_root / "summary.json") or {}

    roadmap_go = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    if not roadmap_go:
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if roadmap_sm.get("defer_health_metric_baseline_planning") is not True:
        blockers.append("health metric baseline must remain deferred")

    if health_vr.get("verifier") != "GO":
        blockers.append("health post-dryrun review verifier must be GO")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management integration must be closed")
    if health_sm.get("health_signal_and_drive_candidates_consumable") is not True:
        blockers.append("health_signal_and_drive_candidates_consumable required")

    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 baseline must be closed")
    if mm_sm.get("governance_skeleton_consumable") is not True:
        blockers.append("model governance skeleton must be consumable")

    task_closed = (
        task_closure.get("perception_to_task_response_candidate_hub_closed") is True
        or task_sm.get("boundary_ok") is True
    )
    if not task_closed:
        blockers.append("task_response_candidate integration must be closed")

    backbone_closed = (
        backbone_sm.get("minimal_backbone_dryrun_closed") is True
        or backbone_sm.get("boundary_ok") is True
    )
    if not backbone_closed:
        blockers.append("midplatform minimal backbone must be closed")

    if factory_sm.get("boundary_ok") is not True:
        blockers.append("luna_validation_factory_consolidation should be boundary_ok")

    input_review = {
        "review_id": "post_health_roadmap_input_review_v1",
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_verifier_go": roadmap_go,
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "health_integration_closed": health_sm.get("health_management_integration_dryrun_closed"),
        "health_candidates_consumable": health_sm.get("health_signal_and_drive_candidates_consumable"),
        "b_lite_closed": canonical_sm.get("b_lite_canonical_v0_baseline_closed"),
        "model_governance_consumable": mm_sm.get("governance_skeleton_consumable"),
        "task_response_closed": task_closed,
        "backbone_closed": backbone_closed,
        "validation_factory_ok": factory_sm.get("boundary_ok"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    vision_scope = {
        "scope_id": "vision_controlled_optimization_scope_v1",
        "chain": "Vision",
        "focus": "controlled frame / sample frame / visual candidate optimization",
        "allowed_now": list(VISION_ALLOWED),
        "forbidden_now": list(VISION_FORBIDDEN),
        "p0_note": "sample and controlled frame quality planning before any provider trial",
        **meta,
    }

    ocr_scope = {
        "scope_id": "ocr_controlled_optimization_scope_v1",
        "chain": "OCR",
        "focus": "mock OCR → controlled OCR provider planning",
        "allowed_now": list(OCR_ALLOWED),
        "forbidden_now": list(OCR_FORBIDDEN),
        "p0_priority": 1,
        "p0_rationale": "OCR provider easiest controlled validation; outputs stay candidate-only",
        **meta,
    }

    voice_scope = {
        "scope_id": "voice_controlled_optimization_scope_v1",
        "chain": "Voice",
        "focus": "speech candidate / ASR-TTS boundary / interruption planning",
        "allowed_now": list(VOICE_ALLOWED),
        "forbidden_now": list(VOICE_FORBIDDEN),
        "do_not_open_real_provider": True,
        **meta,
    }

    cross_chain = {
        "matrix_id": "cross_chain_dependency_matrix_v1",
        "edges": list(CROSS_CHAIN_DEPS),
        "edge_count": len(CROSS_CHAIN_DEPS),
        **meta,
    }

    registry_bindings = [
        {
            "model_id": mid,
            "registry_version": REGISTRY_VERSION,
            "invocation_allowed": False,
            "provider_type": "mock_or_fixture",
            "runtime_mode_upgrade_now": False,
            "controlled_provider_entry_generated_now": False,
            "real_provider_entry_generated_now": False,
        }
        for mid in REGISTRY_BIND_MODELS
        if mid in V0_MODEL_IDS
    ]
    if len(registry_bindings) != 4:
        blockers.append("registry binding must cover 4 vision/ocr/voice models")

    registry_plan = {
        "plan_id": "model_registry_binding_plan_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "bindings": registry_bindings,
        "constraints": [
            "invocation_allowed=false",
            "provider_type=mock_or_fixture",
            "no runtime_mode upgrade in planning",
            "no controlled or real provider entry generated now",
        ],
        **meta,
    }

    health_plan = {
        "plan_id": "health_management_binding_plan_v1",
        "bindings": list(HEALTH_BINDINGS),
        "constraints": [
            "health_signal only candidate",
            "no automatic fallback execution",
            "no model switching execution",
        ],
        **meta,
    }

    constitution_plan = {
        "plan_id": "constitution_boundary_plan_v1",
        "blocks": list(CONSTITUTION_BLOCKS),
        "all_blocked_in_planning": True,
        **meta,
    }

    midplatform_flow = {
        "plan_id": "midplatform_candidate_flow_binding_plan_v1",
        "layers": ["Perception", "ModelManagement", "HealthManagement", "Task", "Constitution"],
        "candidate_protocol": "candidate_only / not_fact / no_write / no_user_output",
        "task_response_hub": "task_response_candidate",
        "ocr_p0_first": True,
        **meta,
    }

    readiness_matrix = {
        "matrix_id": "controlled_provider_readiness_matrix_v1",
        "chains": {
            "Vision": {
                "current_status": "sample_frame_candidate_ready",
                "controlled_provider_planning_allowed": True,
                "real_runtime_allowed": False,
            },
            "OCR": {
                "current_status": "mock_result_candidate_ready",
                "controlled_provider_planning_allowed": True,
                "real_provider_allowed": False,
                "p0_priority": 1,
            },
            "Voice": {
                "current_status": "speech_candidate_contract_needed",
                "controlled_provider_planning_allowed": "partial",
                "real_asr_tts_allowed": False,
            },
        },
        "do_not_open_all_real_providers_simultaneously": True,
        **meta,
    }

    vision_provider_plan = {
        "plan_id": "vision_controlled_provider_planning_v1",
        "steps": [
            "define controlled_frame_reference contract",
            "link visual_observation_candidate to task_response_candidate",
            "plan visual evidence formatting candidate",
            "defer real vision provider until P2 dryrun/trial",
        ],
        "real_provider_invoked_now": False,
        **meta,
    }

    ocr_provider_plan = {
        "plan_id": "ocr_controlled_provider_planning_v1",
        "steps": [
            "OCR mock → controlled provider readiness candidate",
            "OCRRequest / ROI / result / evidence pack candidate chain",
            "provider_readiness_candidate without PaddleOCR/RapidOCR call",
            "timeout / fallback candidate linkage to health hold",
        ],
        "p0_first": True,
        "real_provider_invoked_now": False,
        **meta,
    }

    voice_provider_plan = {
        "plan_id": "voice_controlled_provider_planning_v1",
        "steps": [
            "speech_input_candidate contract",
            "transcript_candidate without task commit",
            "speech_response_candidate without TTS",
            "voice_interruption_candidate and output arbitration plan",
            "tts_readiness_candidate only",
        ],
        "real_asr_tts_invoked_now": False,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "no_runtime_boundary_matrix_v1",
        "checks": [
            {**row, "passed": meta.get(row["field"]) is row["required"]}
            for row in NO_RUNTIME_BOUNDARY
        ],
        "all_pass": all(meta.get(row["field"]) is row["required"] for row in NO_RUNTIME_BOUNDARY),
        **meta,
    }

    phased = {
        "roadmap_id": "phased_optimization_roadmap_v1",
        "phases": list(PHASED_ROADMAP),
        "recommended_next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "no real provider invocation",
            "generate controlled_provider_readiness_candidate",
            "generate OCR provider readiness candidate",
            "generate voice boundary readiness candidate",
            "verify no-runtime boundary",
        ],
        **meta,
    }

    planning_ok = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and boundary_matrix.get("all_pass")
        and len(registry_bindings) == 4
    )

    decision = {
        "decision_id": "vision_ocr_voice_planning_decision_v1",
        "planning_pass": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        "ocr_p0_first": True,
        **meta,
    }

    non_claims = {
        "register_id": "vision_ocr_voice_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    policy = {
        "policy_id": "vision_ocr_voice_controlled_optimization_planning_policy_v1",
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
        "selected_route": SELECTED_ROUTE,
        "ocr_p0_first": True,
        "high_risk_count": 0 if planning_ok else 1,
        **meta,
    }

    return {
        "vision_ocr_voice_controlled_optimization_planning_policy": policy,
        "post_health_roadmap_input_review": input_review,
        "vision_controlled_optimization_scope": vision_scope,
        "ocr_controlled_optimization_scope": ocr_scope,
        "voice_controlled_optimization_scope": voice_scope,
        "cross_chain_dependency_matrix": cross_chain,
        "model_registry_binding_plan": registry_plan,
        "health_management_binding_plan": health_plan,
        "constitution_boundary_plan": constitution_plan,
        "midplatform_candidate_flow_binding_plan": midplatform_flow,
        "controlled_provider_readiness_matrix": readiness_matrix,
        "vision_controlled_provider_planning": vision_provider_plan,
        "ocr_controlled_provider_planning": ocr_provider_plan,
        "voice_controlled_provider_planning": voice_provider_plan,
        "no_runtime_boundary_matrix": boundary_matrix,
        "phased_optimization_roadmap": phased,
        "vision_ocr_voice_non_claims_register": non_claims,
        "vision_ocr_voice_planning_decision": decision,
        "summary": summary,
    }
