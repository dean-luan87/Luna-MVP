# -*- coding: utf-8 -*-
"""Result envelope → midplatform processing → followup task candidates (Case 1)."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Sequence, Tuple

from capabilities.midplatform.model_test_lens.single_model_interaction_validation.single_model_interaction_validation_types_v1 import (
    CASE_1_ID,
    INTERACTION_LOOP_STAGES,
    PHASE_REF,
    SINGLE_MODEL_INTERACTION_VALIDATION_SYSTEM_ID,
)


def _aspect_ratio(bbox: Dict[str, float]) -> float:
    w = max(float(bbox.get("width", 0)), 1e-6)
    h = max(float(bbox.get("height", 0)), 1e-6)
    return h / w


def _text_likelihood_signals(
    envelope: Dict[str, Any],
    attention_record: Optional[Dict[str, Any]],
    *,
    task_context: str,
) -> Tuple[List[str], float]:
    """Heuristic appearance/geometry signals — not fact labels."""
    signals: List[str] = []
    score = 0.0

    bbox = envelope.get("bbox") or envelope.get("bbox_hint") or {}
    if bbox:
        ar = _aspect_ratio(bbox)
        if ar >= 1.2:
            signals.append("vertical_rect_geometry")
            score += 0.25
        if 1.5 <= ar <= 6.0:
            signals.append("sign_like_aspect_ratio")
            score += 0.25

    if attention_record:
        if attention_record.get("ocr_required"):
            signals.append("ocr_required_hint_from_attention")
            score += 0.35
        if attention_record.get("motion_state_candidate") == "static_text_candidate":
            signals.append("static_text_candidate_hint")
            score += 0.2

    if task_context == "street_navigation_test":
        signals.append("street_navigation_context")
        score += 0.1

    conf = float(envelope.get("confidence", 0.5))
    if conf >= 0.4:
        signals.append("segmentation_confidence_ok")
        score += min(conf * 0.2, 0.15)

    return signals, min(score, 1.0)


def evaluate_text_likely_region(
    envelope: Dict[str, Any],
    attention_record: Optional[Dict[str, Any]] = None,
    *,
    task_context: str = "street_navigation_test",
    policy_ref: str = "FollowupRouteFromResultPolicyV1",
    ocr_threshold: float = 0.45,
) -> Dict[str, Any]:
    """Midplatform decides OCR worthiness — MobileSAM does not assert labels."""
    signals, score = _text_likelihood_signals(envelope, attention_record, task_context=task_context)
    text_likely = score >= ocr_threshold

    region_id = envelope.get("region_id", "unknown_region")
    attn_id = (attention_record or {}).get("attention_record_id", f"attn_{region_id}")

    update_candidate = {
        "update_candidate_id": f"ouc_{region_id}",
        "envelope_type": "observation_update_candidate",
        "source_result_candidate_ref": envelope.get("mask_ref") or f"rc_{region_id}",
        "source_region_id": region_id,
        "source_attention_record_id": attn_id,
        "update_type": "text_likely_region_candidate" if text_likely else "needs_followup_review",
        "new_evidence_refs": [envelope.get("mask_ref") or f"mask_{region_id}"],
        "appearance_candidate_signals": signals,
        "midplatform_score": round(score, 4),
        "does_not_overwrite_attention_record": True,
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
    }

    route_candidate = None
    task_candidate = None
    if text_likely:
        route_candidate = {
            "followup_model_route_candidate_id": f"fmrc_ocr_{region_id}",
            "route_type": "ocr",
            "target_model_id": "ocr",
            "source_region_id": region_id,
            "source_update_candidate_id": update_candidate["update_candidate_id"],
            "route_reason": "疑似文字区域，建议 OCR 候选复核（中台调度，非 MobileSAM 断言）",
            "route_reason_key": "read_text",
            "decision_inputs": ["region_geometry", "appearance_candidate", "task_context", "policy_ref"],
            "forbidden_decision_inputs": ["mobilesam_fact_label", "confirmed_text"],
            "followup_model_route_candidate_only": True,
            "not_runner_execution": True,
            "not_executed": True,
            "candidate_only": True,
            "not_fact": True,
            "policy_ref": policy_ref,
        }
        task_candidate = {
            "task_candidate_id": f"T-ocr-{region_id}",
            "runner_task_candidate_id": f"rtc_ocr_{region_id}",
            "recommended_runner_type": "ocr",
            "target_model_id": "ocr",
            "source_region_id": region_id,
            "source_followup_route_ref": route_candidate["followup_model_route_candidate_id"],
            "route_reason": route_candidate["route_reason"],
            "trigger_mode": "manual_only",
            "runner_task_candidate_only": True,
            "not_runner_execution": True,
            "not_executed": True,
            "candidate_only": True,
            "not_fact": True,
            "ocr_runner_forbidden_this_phase": True,
        }

    return {
        "region_id": region_id,
        "text_likely": text_likely,
        "observation_update_candidate": update_candidate,
        "followup_model_route_candidate": route_candidate,
        "new_task_candidate": task_candidate,
    }


def process_segmentation_envelopes(
    envelopes: Sequence[Dict[str, Any]],
    attention_records: Optional[Sequence[Dict[str, Any]]] = None,
    *,
    task_context: str = "street_navigation_test",
    trace_prefix: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Case 1: MobileSAM envelopes → midplatform processing → OCR route/task candidates.
    Attention records are read-only; never mutated.
    """
    attn_by_region: Dict[str, Dict[str, Any]] = {}
    for rec in attention_records or []:
        rid = rec.get("region_id")
        if rid:
            attn_by_region[rid] = copy.deepcopy(rec)

    original_attention_snapshot = copy.deepcopy(list(attn_by_region.values()))
    per_region: List[Dict[str, Any]] = []
    ocr_routes: List[Dict[str, Any]] = []
    ocr_tasks: List[Dict[str, Any]] = []
    updates: List[Dict[str, Any]] = []

    for env in envelopes:
        rid = env.get("region_id", "")
        eval_out = evaluate_text_likely_region(
            env,
            attn_by_region.get(rid),
            task_context=task_context,
        )
        per_region.append(eval_out)
        updates.append(eval_out["observation_update_candidate"])
        if eval_out["followup_model_route_candidate"]:
            ocr_routes.append(eval_out["followup_model_route_candidate"])
        if eval_out["new_task_candidate"]:
            ocr_tasks.append(eval_out["new_task_candidate"])

    trace = list(trace_prefix or [])
    trace.extend(
        [
            {"stage": "result_candidate", "ref": "result_layer"},
            {"stage": "midplatform_processing", "ref": SINGLE_MODEL_INTERACTION_VALIDATION_SYSTEM_ID},
            {"stage": "observation_update_candidate", "ref": f"ouc_batch_{len(updates)}"},
        ]
    )
    if ocr_routes:
        trace.append({"stage": "followup_model_route_candidate", "ref": ocr_routes[0]["followup_model_route_candidate_id"]})
    if ocr_tasks:
        trace.append({"stage": "new_task_candidate", "ref": ocr_tasks[0]["task_candidate_id"]})

    attention_unchanged = original_attention_snapshot == list(attn_by_region.values())

    return {
        "system_id": SINGLE_MODEL_INTERACTION_VALIDATION_SYSTEM_ID,
        "phase_ref": PHASE_REF,
        "case_id": CASE_1_ID,
        "candidate_only": True,
        "not_fact": True,
        "not_runner_execution": True,
        "ocr_runner_forbidden": True,
        "midplatform_schedules_not_pipeline": True,
        "per_region_results": per_region,
        "observation_update_candidates": updates,
        "followup_model_route_candidates": ocr_routes,
        "new_task_candidates": ocr_tasks,
        "attention_records_read_only": True,
        "attention_records_not_overwritten": attention_unchanged,
        "original_attention_snapshot": original_attention_snapshot,
        "trace_chain": trace,
        "interaction_loop_stages": list(INTERACTION_LOOP_STAGES),
    }


def build_sample_case1_envelopes() -> List[Dict[str, Any]]:
    """Fixture envelopes for Case 1 smoke — geometry hints only, no fact labels."""
    return [
        {
            "envelope_type": "segmentation_result_envelope",
            "source_model": "mobile_sam",
            "source_runner_execution_id": "rex_mobile_sam_case1_001",
            "source_execution_candidate_id": "crec_case1_001",
            "region_id": "region_001",
            "mask_ref": "mask_region_001",
            "confidence": 0.72,
            "bbox_hint": {"width": 120, "height": 40},
            "candidate_only": True,
            "not_fact": True,
            "needs_fact_admission": True,
        },
        {
            "envelope_type": "segmentation_result_envelope",
            "source_model": "mobile_sam",
            "source_runner_execution_id": "rex_mobile_sam_case1_001",
            "source_execution_candidate_id": "crec_case1_001",
            "region_id": "region_002",
            "mask_ref": "mask_region_002",
            "confidence": 0.81,
            "bbox_hint": {"width": 45, "height": 180},
            "candidate_only": True,
            "not_fact": True,
            "needs_fact_admission": True,
        },
        {
            "envelope_type": "segmentation_result_envelope",
            "source_model": "mobile_sam",
            "source_runner_execution_id": "rex_mobile_sam_case1_001",
            "source_execution_candidate_id": "crec_case1_001",
            "region_id": "region_003",
            "mask_ref": "mask_region_003",
            "confidence": 0.65,
            "bbox_hint": {"width": 200, "height": 120},
            "candidate_only": True,
            "not_fact": True,
            "needs_fact_admission": True,
        },
    ]


def build_sample_attention_records() -> List[Dict[str, Any]]:
    return [
        {
            "attention_record_id": "attn_region_001",
            "region_id": "region_001",
            "priority_level": "P2_medium_attention",
            "ocr_required": False,
            "motion_state_candidate": "scene_structure_candidate",
            "candidate_only": True,
        },
        {
            "attention_record_id": "attn_region_002",
            "region_id": "region_002",
            "priority_level": "P1_high_attention",
            "ocr_required": True,
            "motion_state_candidate": "static_text_candidate",
            "candidate_only": True,
        },
        {
            "attention_record_id": "attn_region_003",
            "region_id": "region_003",
            "priority_level": "P3_low_attention",
            "ocr_required": False,
            "motion_state_candidate": "scene_structure_candidate",
            "candidate_only": True,
        },
    ]
