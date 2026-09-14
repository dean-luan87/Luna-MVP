# -*- coding: utf-8 -*-
"""
MobileSAM → OCR route exploration smoke processor.

Exploratory only — no OCR runner, no OCR execution, no fact write.
"""

from __future__ import annotations

import copy
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_test_lens.human_correction.correction_midplatform_analyzer_v1 import (
    analyze_correction,
)
from capabilities.midplatform.model_test_lens.single_model_interaction_validation.result_to_midplatform_processor_v1 import (
    evaluate_text_likely_region,
)

PHASE_REF = "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Exploration-Smoke-v1-001"
SYSTEM_ID = "LunaMidplatformMobileSamOcrExplorationSmokeV1"

OCR_TEXT_INTENT_PATTERNS = (
    r"读文字", r"这里有文字", r"应该.*文字", r"需要.*读", r"想看.*字",
)

FORBIDDEN_OUTPUT_KEYS = frozenset({
    "type", "sign", "text", "confirmed_text", "fact_label", "object_name",
})


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _result_candidate_id(region_id: str) -> str:
    return f"rc_seg_{region_id}"


def _analysis_record_id(region_id: str) -> str:
    return f"mar_{region_id}"


def _map_route_reasons(signals: List[str]) -> List[str]:
    mapping = {
        "vertical_rect_geometry": "text_likely_geometry",
        "sign_like_aspect_ratio": "text_likely_geometry",
        "static_text_candidate_hint": "static_candidate",
        "ocr_required_hint_from_attention": "static_candidate",
        "street_navigation_context": "task_context_signal",
        "segmentation_confidence_ok": "confidence_ok",
    }
    reasons: List[str] = []
    for s in signals:
        reasons.append(mapping.get(s, s))
    if "static_candidate" not in reasons and any("static" in s for s in signals):
        reasons.append("static_candidate")
    if "text_likely_geometry" not in reasons and any("geometry" in s or "aspect" in s for s in signals):
        reasons.append("text_likely_geometry")
    return list(dict.fromkeys(reasons)) or ["needs_review"]


def process_segmentation_envelope_for_ocr_route(
    envelope: Dict[str, Any],
    attention_record: Optional[Dict[str, Any]] = None,
    *,
    task_context: str = "street_navigation_test",
) -> Dict[str, Any]:
    """
    Input: segmentation_result_envelope
    Output: result_candidate, midplatform_analysis_record, followup_model_route_candidate, ocr_task_candidate
    """
    region_id = envelope.get("region_id", "unknown_region")
    eval_out = evaluate_text_likely_region(envelope, attention_record, task_context=task_context)

    rc_id = _result_candidate_id(region_id)
    mar_id = _analysis_record_id(region_id)
    mask_ref = envelope.get("mask_ref") or f"mask_{region_id}"
    signals = (eval_out.get("observation_update_candidate") or {}).get("appearance_candidate_signals", [])

    result_candidate = {
        "result_candidate_id": rc_id,
        "result_candidate_type": "segmentation_mask_candidate",
        "source_model": envelope.get("source_model", "mobile_sam"),
        "source_region_id": region_id,
        "mask_ref": mask_ref,
        "confidence": envelope.get("confidence"),
        "model_provides": "region_geometry_only",
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
    }

    midplatform_analysis_record = {
        "analysis_record_id": mar_id,
        "source_result_candidate_id": rc_id,
        "source_region_id": region_id,
        "input_type": "segmentation_result_envelope",
        "judgment": "text_likely" if eval_out["text_likely"] else "no_ocr_route",
        "appearance_signals": signals,
        "midplatform_score": (eval_out.get("observation_update_candidate") or {}).get("midplatform_score"),
        "candidate_only": True,
        "not_fact": True,
        "midplatform_analysis_not_model_output": True,
        "no_text_fact_generation": True,
    }

    followup_model_route_candidate = None
    ocr_task_candidate = None
    trace_chain: List[Dict[str, str]] = [
        {"stage": "Image", "ref": envelope.get("image_ref", "input")},
        {"stage": "MobileSAM Execution", "ref": envelope.get("source_runner_execution_id", "")},
        {"stage": "Segmentation Result Envelope", "ref": mask_ref},
        {"stage": "Result Candidate", "ref": rc_id},
        {"stage": "Midplatform Analysis", "ref": mar_id},
    ]

    if eval_out["text_likely"]:
        route = eval_out["followup_model_route_candidate"] or {}
        followup_model_route_candidate = {
            **route,
            "route_type": "OCR",
            "reason": _map_route_reasons(signals),
            "source_result_candidate_id": rc_id,
            "source_analysis_record_id": mar_id,
            "candidate_only": True,
            "not_fact": True,
            "no_text_fact_generation": True,
        }
        task = eval_out["new_task_candidate"] or {}
        ocr_task_candidate = {
            **task,
            "task_type": "ocr_task_candidate",
            "source_region_id": region_id,
            "source_result_candidate_id": rc_id,
            "source_analysis_record_id": mar_id,
            "source_followup_model_route_candidate_id": route.get("followup_model_route_candidate_id"),
            "ocr_runner_forbidden": True,
            "not_runner_execution": True,
            "not_executed": True,
            "candidate_only": True,
            "not_fact": True,
        }
        trace_chain.extend([
            {"stage": "OCR Route Candidate", "ref": followup_model_route_candidate.get("followup_model_route_candidate_id", "")},
            {"stage": "OCR Task Candidate", "ref": ocr_task_candidate.get("task_candidate_id", "")},
        ])

    output = {
        "phase_ref": PHASE_REF,
        "system_id": SYSTEM_ID,
        "region_id": region_id,
        "text_likely": eval_out["text_likely"],
        "result_candidate": result_candidate,
        "midplatform_analysis_record": midplatform_analysis_record,
        "followup_model_route_candidate": followup_model_route_candidate,
        "ocr_task_candidate": ocr_task_candidate,
        "trace_chain": trace_chain,
        "ocr_runner_forbidden": True,
        "no_ocr_execution": True,
        "candidate_only": True,
        "not_fact": True,
    }
    _assert_no_forbidden_keys(output)
    return output


def _assert_no_forbidden_keys(obj: Any, path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_OUTPUT_KEYS and v not in (None, False, ""):
                raise ValueError(f"forbidden_output_key={k} at {path}")
            if k == "text" and isinstance(v, str) and v not in ("", "read_text"):
                raise ValueError(f"forbidden_text_fact at {path}")
        for k, v in obj.items():
            _assert_no_forbidden_keys(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _assert_no_forbidden_keys(item, f"{path}[{i}]")


def process_correction_ocr_priority_signal(
    correction: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Case C: Human correction with text-read intent → OCR priority signal → task candidate only.
    No OCR execution.
    """
    note = str(correction.get("manual_annotation") or correction.get("user_note") or "")
    region_id = (
        (correction.get("correction_target") or {}).get("source_object_id")
        or (correction.get("correction_target") or {}).get("target_id")
        or "unknown_region"
    )
    has_text_intent = any(re.search(p, note) for p in OCR_TEXT_INTENT_PATTERNS)
    analysis = analyze_correction(correction)

    ocr_priority_signal = None
    ocr_task_candidate = None
    if has_text_intent:
        mar_id = f"mar_corr_{correction.get('correction_id', 'unknown')}"
        rc_id = _result_candidate_id(region_id)
        route_id = f"fmrc_ocr_corr_{region_id}"
        ocr_priority_signal = {
            "signal_type": "ocr_priority_signal",
            "source_correction_id": correction.get("correction_id"),
            "source_region_id": region_id,
            "attribution_id": analysis.get("attribution_id"),
            "reason": "human_correction_text_read_intent",
            "candidate_only": True,
            "not_fact": True,
            "human_correction_not_ground_truth": True,
            "no_ocr_execution": True,
        }
        ocr_task_candidate = {
            "task_candidate_id": f"T-ocr-corr-{region_id}",
            "runner_task_candidate_id": f"rtc_ocr_corr_{region_id}",
            "task_type": "ocr_task_candidate",
            "recommended_runner_type": "ocr",
            "source_region_id": region_id,
            "source_result_candidate_id": rc_id,
            "source_analysis_record_id": mar_id,
            "source_followup_model_route_candidate_id": route_id,
            "source_correction_id": correction.get("correction_id"),
            "trigger_mode": "manual_only",
            "ocr_runner_forbidden": True,
            "not_runner_execution": True,
            "candidate_only": True,
            "not_fact": True,
        }

    trace_chain = [
        {"stage": "User Correction", "ref": correction.get("correction_id", "")},
        {"stage": "Correction Record", "ref": note[:40]},
        {"stage": "Attribution", "ref": analysis.get("attribution_id", "")},
    ]
    if ocr_priority_signal:
        trace_chain.append({"stage": "OCR Priority Signal", "ref": ocr_priority_signal["signal_type"]})
        trace_chain.append({"stage": "OCR Task Candidate", "ref": ocr_task_candidate["task_candidate_id"]})  # type: ignore[index]

    return {
        "phase_ref": PHASE_REF,
        "case_id": "Case-C-Correction-OCR-Priority",
        "correction_analysis": analysis,
        "ocr_priority_signal": ocr_priority_signal,
        "ocr_task_candidate": ocr_task_candidate,
        "ocr_executed": False,
        "no_ocr_execution": True,
        "trace_chain": trace_chain,
        "candidate_only": True,
    }


def fixture_envelope_region_002() -> Dict[str, Any]:
    return {
        "envelope_type": "segmentation_result_envelope",
        "source_model": "mobile_sam",
        "source_runner_execution_id": "rex_mobile_sam_explore_a",
        "source_execution_candidate_id": "crec_explore_a",
        "region_id": "region_002",
        "mask_ref": "mask_region_002",
        "confidence": 0.91,
        "bbox_hint": {"width": 45, "height": 180},
        "candidate_only": True,
        "not_fact": True,
    }


def fixture_attention_region_002() -> Dict[str, Any]:
    return {
        "attention_record_id": "attn_region_002",
        "region_id": "region_002",
        "ocr_required": True,
        "motion_state_candidate": "static_text_candidate",
        "candidate_only": True,
    }


def fixture_envelope_building() -> Dict[str, Any]:
    return {
        "envelope_type": "segmentation_result_envelope",
        "source_model": "mobile_sam",
        "source_runner_execution_id": "rex_mobile_sam_explore_b",
        "region_id": "region_building_001",
        "mask_ref": "mask_building_001",
        "confidence": 0.88,
        "bbox_hint": {"width": 220, "height": 140},
        "candidate_only": True,
        "not_fact": True,
    }


def fixture_correction_text_intent() -> Dict[str, Any]:
    return {
        "correction_id": "correction_explore_c_text",
        "source_model_id": "mobile_sam",
        "manual_annotation": "这个区域应该读文字",
        "user_note": "这个区域应该读文字",
        "correction_target": {
            "target_id": "region_002",
            "source_object_id": "region_002",
            "target_type": "segmentation_mask",
        },
        "candidate_only": True,
        "not_fact": True,
    }


def run_smoke_cases() -> Dict[str, Any]:
    case_a = process_segmentation_envelope_for_ocr_route(
        fixture_envelope_region_002(),
        fixture_attention_region_002(),
    )
    case_b = process_segmentation_envelope_for_ocr_route(fixture_envelope_building())
    case_c = process_correction_ocr_priority_signal(fixture_correction_text_intent())

    checks = {
        "case_a_ocr_route": case_a["followup_model_route_candidate"] is not None,
        "case_a_ocr_task": case_a["ocr_task_candidate"] is not None,
        "case_a_trace_complete": len(case_a["trace_chain"]) >= 7,
        "case_a_task_traceable": (
            case_a["ocr_task_candidate"] is not None
            and case_a["ocr_task_candidate"].get("source_region_id") == "region_002"
            and case_a["ocr_task_candidate"].get("source_result_candidate_id")
            and case_a["ocr_task_candidate"].get("source_analysis_record_id")
        ),
        "case_b_no_ocr_task": case_b["ocr_task_candidate"] is None,
        "case_b_no_ocr_route": case_b["followup_model_route_candidate"] is None,
        "case_c_priority_signal": case_c["ocr_priority_signal"] is not None,
        "case_c_ocr_task_not_execution": (
            case_c["ocr_task_candidate"] is not None
            and case_c["ocr_task_candidate"].get("not_runner_execution") is True
            and case_c["no_ocr_execution"] is True
        ),
        "no_ocr_runner_call": (
            case_a.get("ocr_runner_forbidden") is True
            and case_c.get("no_ocr_execution") is True
        ),
        "candidate_only_preserved": all(
            x.get("candidate_only", True) for x in (case_a, case_b, case_c)
        ),
    }
    failed = [k for k, v in checks.items() if not v]

    return {
        "smoke_id": "mobile_sam_ocr_interaction_exploration_smoke_v1",
        "phase_ref": PHASE_REF,
        "case_a": case_a,
        "case_b": case_b,
        "case_c": case_c,
        "checks": checks,
        "failed_checks": failed,
        "final_decision": "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO"
        if not failed
        else "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_BLOCKED",
        "reviewed_at": _now_iso(),
    }
