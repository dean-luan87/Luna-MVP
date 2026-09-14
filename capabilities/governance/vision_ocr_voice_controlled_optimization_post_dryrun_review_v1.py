# -*- coding: utf-8 -*-
"""Vision / OCR / Voice Controlled Optimization Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_ocr_voice_controlled_optimization_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    CONSTITUTION_BLOCKS,
    CROSS_CHAIN_DEPS,
    HEALTH_BINDINGS,
    REGISTRY_BIND_MODELS,
)

PHASE_ID = "Phase-Vision-OCR-Voice-Controlled-Optimization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "vision_ocr_voice_controlled_optimization_post_dryrun_review_only"
SOURCE_CHAIN = "vision_ocr_voice_controlled_optimization_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_OCR_CONTROLLED_PROVIDER_PLANNING"
)
FINAL_DECISION_HOLD = "VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Controlled-Provider-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-OCR-Voice-Controlled-Optimization-Issue-Review-v1-001"

OUT_OF_SCOPE: Tuple[str, ...] = (
    "scene_intent_candidate",
    "visual_context_governance",
    "world_model",
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_readiness_candidate_generated_now",
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
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ provider enabled",
    "OCR readiness ≠ OCR provider invoked",
    "Vision readiness ≠ live camera enabled",
    "Voice readiness ≠ ASR/TTS runtime enabled",
    "controlled optimization closure ≠ limited runtime allowed",
    "next OCR planning readiness ≠ PaddleOCR/RapidOCR invocation allowed",
    "scene_intent / visual_context_governance / world_model not in scope for this review",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "vision_ocr_voice_controlled_optimization_post_dryrun_review_only": True,
        "review_only": True,
        "new_readiness_candidate_generated_now": False,
        "out_of_scope_not_included": list(OUT_OF_SCOPE),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "ocr_p0_next": True,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _vision_checks(vision: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    expected = {
        "candidate_type": "vision_controlled_optimization_readiness_candidate",
        "source_scope": "sample_or_controlled_frame_reference_only",
        "visual_observation_candidate_supported": True,
        "task_response_linkage_ready": True,
        "live_camera_allowed": False,
        "real_vision_model_allowed": False,
        "visual_fact_write_allowed": False,
        "world_model_write_allowed": False,
        "candidate_only": True,
    }
    for key, val in expected.items():
        if vision.get(key) != val:
            issues.append({"issue_id": key, "detail": f"expected {val}"})
    return issues


def _ocr_checks(ocr: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    flags = {
        "candidate_type": "ocr_controlled_provider_readiness_candidate",
        "mock_to_controlled_provider_planning_ready": True,
        "ocr_request_candidate_supported": True,
        "roi_candidate_supported": True,
        "ocr_result_candidate_supported": True,
        "ocr_evidence_pack_candidate_supported": True,
        "provider_readiness_candidate_supported": True,
        "controlled_provider_planning_allowed": True,
        "paddleocr_allowed": False,
        "rapidocr_allowed": False,
        "real_ocr_provider_allowed": False,
        "ocr_fact_write_allowed": False,
        "user_output_allowed": False,
        "candidate_only": True,
    }
    for key, val in flags.items():
        if ocr.get(key) != val:
            issues.append({"issue_id": key, "detail": f"expected {val}"})
    return issues


def _voice_checks(voice: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    flags = {
        "candidate_type": "voice_boundary_readiness_candidate",
        "speech_input_candidate_supported": True,
        "transcript_candidate_supported": True,
        "asr_tts_boundary_planned": True,
        "interruption_candidate_supported": True,
        "output_arbitration_required": True,
        "real_asr_allowed": False,
        "real_tts_allowed": False,
        "voice_output_allowed": False,
        "user_output_allowed": False,
        "candidate_only": True,
    }
    for key, val in flags.items():
        if voice.get(key) != val:
            issues.append({"issue_id": key, "detail": f"expected {val}"})
    return issues


def run_vision_ocr_voice_controlled_optimization_post_dryrun_review_v1(
    *,
    vision_ocr_voice_controlled_optimization_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(vision_ocr_voice_controlled_optimization_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "vision_ocr_voice_controlled_optimization_post_dryrun_review"
    )
    meta = {
        **_review_meta(),
        "upstream_dryrun_root": str(dryrun_root),
        "review_output_root": str(out_root),
    }

    vision = _try_read_json(dryrun_root / "vision_readiness_candidate_result_v1.json") or {}
    ocr = _try_read_json(dryrun_root / "ocr_readiness_candidate_result_v1.json") or {}
    voice = _try_read_json(dryrun_root / "voice_readiness_candidate_result_v1.json") or {}
    cross = _try_read_json(dryrun_root / "cross_chain_dependency_dryrun_result_v1.json") or {}
    registry = _try_read_json(dryrun_root / "model_registry_binding_dryrun_result_v1.json") or {}
    health = _try_read_json(dryrun_root / "health_management_binding_dryrun_result_v1.json") or {}
    constitution = _try_read_json(dryrun_root / "constitution_boundary_dryrun_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "no_runtime_boundary_audit_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "blocked_path_result_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "controlled_optimization_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "readiness_candidates_present": {
            "vision": vision.get("candidate_type") == "vision_controlled_optimization_readiness_candidate",
            "ocr": ocr.get("candidate_type") == "ocr_controlled_provider_readiness_candidate",
            "voice": voice.get("candidate_type") == "voice_boundary_readiness_candidate",
        },
        "out_of_scope_confirmed": list(OUT_OF_SCOPE),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    vision_issues = _vision_checks(vision)
    vision_review = {
        "review_id": "vision_readiness_candidate_review_v1",
        "candidate_type": vision.get("candidate_type"),
        "issues": vision_issues,
        "review_pass": len(vision_issues) == 0,
        **meta,
    }

    ocr_issues = _ocr_checks(ocr)
    ocr_review = {
        "review_id": "ocr_readiness_candidate_review_v1",
        "candidate_type": ocr.get("candidate_type"),
        "p0_priority": ocr.get("p0_priority"),
        "issues": ocr_issues,
        "review_pass": len(ocr_issues) == 0,
        **meta,
    }

    voice_issues = _voice_checks(voice)
    voice_review = {
        "review_id": "voice_readiness_candidate_review_v1",
        "candidate_type": voice.get("candidate_type"),
        "issues": voice_issues,
        "review_pass": len(voice_issues) == 0,
        **meta,
    }

    cross_issues: List[Dict[str, Any]] = []
    edges = cross.get("edges") or []
    if cross.get("routing_pass") is not True or len(edges) != 6:
        cross_issues.append({"issue_id": "routing_pass", "detail": "must be 6 edges pass"})
    for edge in edges:
        if edge.get("routed") is not True:
            cross_issues.append({"issue_id": edge.get("edge_id"), "detail": "not routed"})
        if edge.get("executed_now") is True:
            cross_issues.append({"issue_id": edge.get("edge_id"), "detail": "executed_now true"})

    cross_review = {
        "review_id": "cross_chain_dependency_review_v1",
        "edge_count": len(edges),
        "issues": cross_issues,
        "review_pass": len(cross_issues) == 0,
        **meta,
    }

    registry_issues: List[Dict[str, Any]] = []
    binds = registry.get("bindings") or []
    if registry.get("binding_pass") is not True or len(binds) != 4:
        registry_issues.append({"issue_id": "binding_pass", "detail": "4 mock models required"})
    for mid in REGISTRY_BIND_MODELS:
        row = next((b for b in binds if b.get("model_id") == mid), None)
        if not row or row.get("invocation_allowed") is not False:
            registry_issues.append({"issue_id": mid, "detail": "invocation_allowed must be false"})
        if row and row.get("controlled_provider_entry_generated_now") is True:
            registry_issues.append({"issue_id": mid, "detail": "no controlled entry"})
        if row and row.get("real_provider_entry_generated_now") is True:
            registry_issues.append({"issue_id": mid, "detail": "no real entry"})

    registry_review = {
        "review_id": "model_registry_binding_review_v1",
        "model_ids": list(REGISTRY_BIND_MODELS),
        "issues": registry_issues,
        "review_pass": len(registry_issues) == 0,
        **meta,
    }

    health_issues: List[Dict[str, Any]] = []
    routes = health.get("routes") or []
    if health.get("routing_pass") is not True or len(routes) != 6:
        health_issues.append({"issue_id": "routing", "detail": "6 routes required"})
    if health.get("no_automatic_fallback") is not True:
        health_issues.append({"issue_id": "fallback", "detail": "no automatic fallback"})
    if health.get("no_model_switch_execution") is not True:
        health_issues.append({"issue_id": "switch", "detail": "no model switch"})
    for route in routes:
        if route.get("executed_now") is True or route.get("automatic_execution") is True:
            health_issues.append({"issue_id": route.get("trigger"), "detail": "must not execute"})

    health_review = {
        "review_id": "health_management_binding_review_v1",
        "route_count": len(routes),
        "issues": health_issues,
        "review_pass": len(health_issues) == 0,
        **meta,
    }

    constitution_issues: List[Dict[str, Any]] = []
    blocks = constitution.get("blocks") or []
    if constitution.get("all_blocked") is not True or len(blocks) != 7:
        constitution_issues.append({"issue_id": "count", "detail": "7 blocks required"})
    for block in CONSTITUTION_BLOCKS:
        row = next((b for b in blocks if b.get("block_id") == block["block_id"]), None)
        if not row or row.get("blocked") is not True:
            constitution_issues.append({"issue_id": block["block_id"], "detail": "must be blocked"})

    constitution_review = {
        "review_id": "constitution_boundary_review_v1",
        "issues": constitution_issues,
        "review_pass": len(constitution_issues) == 0,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    if audit.get("audit_pass") is not True:
        runtime_issues.append({"issue_id": "audit_pass", "detail": "must pass"})
    for check in audit.get("checks") or []:
        if check.get("passed") is not True:
            runtime_issues.append({"issue_id": check.get("check_id"), "detail": "failed"})

    runtime_review = {
        "review_id": "no_runtime_boundary_review_v1",
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    if blocked.get("all_blocked") is not True or len(paths) != 14:
        blocked_issues.append({"issue_id": "count", "detail": "14 paths required"})
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked=true"})
        if row and row.get("observed_now") is True:
            blocked_issues.append({"issue_id": pid, "detail": "observed_now must be false"})

    blocked_review = {
        "review_id": "blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and vision_review.get("review_pass")
        and ocr_review.get("review_pass")
        and voice_review.get("review_pass")
        and cross_review.get("review_pass")
        and registry_review.get("review_pass")
        and health_review.get("review_pass")
        and constitution_review.get("review_pass")
        and runtime_review.get("review_pass")
        and blocked_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "controlled_optimization_closure_decision_v1",
        "controlled_optimization_dryrun_closed": boundary_ok,
        "three_chain_readiness_trusted": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_controlled_provider_planning": boundary_ok,
        "preferred_next_chain": "OCR",
        "rationale": "OCR is best suited for first controlled provider planning among Vision/OCR/Voice",
        "do_not_invoke_paddleocr_or_rapidocr": True,
        "do_not_enable_provider_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers
        + [i["issue_id"] for i in vision_issues + ocr_issues + voice_issues + blocked_issues],
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "controlled_optimization_dryrun_closed": boundary_ok,
        "three_chain_readiness_trusted": boundary_ok,
        **meta,
    }

    return {
        "controlled_optimization_dryrun_input_review": input_review,
        "vision_readiness_candidate_review": vision_review,
        "ocr_readiness_candidate_review": ocr_review,
        "voice_readiness_candidate_review": voice_review,
        "cross_chain_dependency_review": cross_review,
        "model_registry_binding_review": registry_review,
        "health_management_binding_review": health_review,
        "constitution_boundary_review": constitution_review,
        "no_runtime_boundary_review": runtime_review,
        "blocked_path_review": blocked_review,
        "controlled_optimization_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
