from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple


_VISUAL_HINT_TO_CLASS: Dict[str, str] = {
    # Task vs supporting
    "task_sign": "task_relevant_text",
    "task_exit": "task_relevant_text",
    "task_office": "task_relevant_text",
    "task_warning": "task_relevant_text",
    "task_door": "task_relevant_text",
    "task_platform": "task_relevant_text",
    "task_counternow": "context_relevant_text",
    "task_elevator_hall": "context_relevant_text",
    "task_queue_entrance": "context_relevant_text",
    "task_floor_guide": "context_relevant_text",
    "task_business_hours": "context_relevant_text",

    # World context (scene environment)
    "storefront_brand": "world_context_text",
    "place_public_info": "world_context_text",
    "public_slogan": "world_context_text",

    # Commercial / ambient
    "commercial_activity": "commercial_context_text",
    "promo_activity": "promotional_text",
    "advertisement_poster": "advertisement_like_text",
    "advertisement_screen": "advertisement_like_text",

    # Ambient derived (for completeness)
    "ambient_context": "ambient_context_text",
    "experience_enrichment": "experience_enrichment_text",
    "decorative": "decorative_text",

    # Noise / uncertainty
    "uncertain": "uncertain_relevance_text",
    "irrelevant": "irrelevant_or_noise_text",

    # Low-value / uncertain visual text
    "illegible": "illegible_text",
    "unreadable": "illegible_text",
    "blurred": "blurred_text",
    "low_quality": "blurred_text",
    "graffiti": "scribble_or_graffiti_text",
    "scribble": "scribble_or_graffiti_text",
    "stylized": "decorative_or_stylized_text",
    "decorative_stylized": "decorative_or_stylized_text",
    "fragmented": "fragmented_text",
    "non_actionable": "non_actionable_text",
    "meaning_uncertain": "meaning_uncertain_text",
}


def _sha_short(s: str, n: int = 16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _avg_conf(cands: Any) -> float:
    if not isinstance(cands, list):
        return 0.0
    vals: List[float] = []
    for c in cands:
        if isinstance(c, dict):
            conf = c.get("confidence", None)
            if conf is not None:
                vals.append(_as_float(conf, 0.0))
    return float(sum(vals) / len(vals)) if vals else 0.0


def _joined_text(evidence_input: Dict[str, Any]) -> str:
    t = evidence_input.get("raw_text_joined")
    if isinstance(t, str):
        return t
    # fallback: rebuild from candidates order
    cands = evidence_input.get("raw_text_candidates") or []
    if isinstance(cands, list):
        pairs: List[Tuple[int, str]] = []
        for c in cands:
            if not isinstance(c, dict):
                continue
            ln = c.get("line_order")
            order = int(ln) if isinstance(ln, (int, float, str)) and str(ln).isdigit() else 0
            text = str(c.get("text") or c.get("normalized_text") or "")
            if text:
                pairs.append((order, text))
        pairs.sort(key=lambda x: x[0])
        return "\n".join([p[1] for p in pairs])
    return ""


def classify_visual_text_relevance_v0(evidence_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Contract-only placeholder classifier.

    - If `visual_source_hint` exists, we treat it as the authoritative classification hint.
    - Otherwise we apply conservative keyword triggers on the joined raw text.
    """

    hint = evidence_input.get("visual_source_hint")
    if isinstance(hint, str):
        cls = _VISUAL_HINT_TO_CLASS.get(hint.strip().lower())
        if cls:
            # Support user override by upgrading to user_requested_text,
            # while keeping the base class for uncertainty marking.
            base_cls = cls
            if evidence_input.get("user_requested_override"):
                return {
                    "visual_text_relevance_class": "user_requested_text",
                    "why": f"user_requested_override_from:{hint}",
                    "base_visual_text_relevance_class": base_cls,
                }
            return {"visual_text_relevance_class": cls, "why": f"visual_source_hint:{hint}"}

    joined = _joined_text(evidence_input).lower()
    avg_conf = _avg_conf(evidence_input.get("raw_text_candidates"))

    # Low-value / uncertain boundary (very conservative)
    if avg_conf > 0 and avg_conf < 0.35:
        base_cls = "meaning_uncertain_text"
        if avg_conf < 0.15:
            base_cls = "illegible_text"
        elif avg_conf < 0.25:
            base_cls = "blurred_text"
        if evidence_input.get("user_requested_override"):
            return {
                "visual_text_relevance_class": "user_requested_text",
                "why": f"user_requested_override_from:{base_cls}",
                "base_visual_text_relevance_class": base_cls,
            }
        return {"visual_text_relevance_class": base_cls, "why": "avg_conf_low"}

    # Task vs supporting: actionability-ish keywords
    task_kw = ["出口", "科室", "门牌", "警示", "站台", "窗口", "路线", "楼层", "挂号", "收费", "服务台", "电梯", "电梯厅", "排队入口"]
    support_kw = ["服务台", "电梯厅", "营业时间", "排队入口", "楼层导视", "排队", "指引"]
    if any(k in joined for k in task_kw):
        if any(k in joined for k in support_kw):
            cls = "context_relevant_text"
        else:
            cls = "task_relevant_text"
        if evidence_input.get("user_requested_override"):
            return {
                "visual_text_relevance_class": "user_requested_text",
                "why": f"user_requested_override_from:{cls}",
                "base_visual_text_relevance_class": cls,
            }
        return {"visual_text_relevance_class": cls, "why": "task_keyword_match"}

    # Commercial / promo / ad-like
    promo_kw = ["扫码", "领券", "限时", "秒杀", "满", "减", "立减", "抢购", "优惠购", "特价"]
    commercial_kw = ["折扣", "优惠", "会员", "第二杯", "新品", "活动", "营业时间", "促销", "价"]
    ad_like_kw = ["海报", "广告", "灯箱", "轮播", "屏幕", "banner", "二维码", "扫码"]

    if any(k in joined for k in promo_kw):
        cls = "promotional_text"
    elif any(k in joined for k in commercial_kw):
        cls = "commercial_context_text"
    elif any(k in joined for k in ad_like_kw):
        cls = "advertisement_like_text"
    else:
        cls = None

    if cls:
        if evidence_input.get("user_requested_override"):
            return {
                "visual_text_relevance_class": "user_requested_text",
                "why": f"user_requested_override_from:{cls}",
                "base_visual_text_relevance_class": cls,
            }
        return {"visual_text_relevance_class": cls, "why": "commercial_keyword_match"}

    # World context (store/brand/public info)
    world_kw = ["银行", "商场", "超市", "便利店", "药店", "医院", "店", "品牌", "营业", "基业", "有限公司"]
    if any(k in joined for k in world_kw):
        cls = "world_context_text"
        if evidence_input.get("user_requested_override"):
            return {
                "visual_text_relevance_class": "user_requested_text",
                "why": f"user_requested_override_from:{cls}",
                "base_visual_text_relevance_class": cls,
            }
        return {"visual_text_relevance_class": cls, "why": "world_keyword_match"}

    # Decorative / stylized (OCR might be wrong; treat conservatively)
    deco_markers = ["欢迎", "祝", "艺术", "口号", "logo"]
    if any(m in joined for m in deco_markers):
        cls = "decorative_or_stylized_text" if avg_conf < 0.6 else "decorative_text"
        if evidence_input.get("user_requested_override"):
            return {
                "visual_text_relevance_class": "user_requested_text",
                "why": f"user_requested_override_from:{cls}",
                "base_visual_text_relevance_class": cls,
            }
        return {"visual_text_relevance_class": cls, "why": "decorative_marker_match"}

    if evidence_input.get("user_requested_override"):
        return {
            "visual_text_relevance_class": "user_requested_text",
            "why": "user_requested_override_default_irrelevant",
            "base_visual_text_relevance_class": "irrelevant_or_noise_text",
        }

    return {"visual_text_relevance_class": "irrelevant_or_noise_text", "why": "default_irrelevant"}


def _pick_primary_bbox(raw_text_candidates: Any) -> Optional[Dict[str, float]]:
    if not isinstance(raw_text_candidates, list):
        return None
    for c in raw_text_candidates:
        if not isinstance(c, dict):
            continue
        bbox = c.get("bbox")
        if isinstance(bbox, list) and len(bbox) == 4:
            try:
                x1, y1, x2, y2 = [float(v) for v in bbox]
                if x2 > x1 and y2 > y1:
                    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            except Exception:
                continue
    return None


def build_midplatform_ocr_evidence_input_v0(
    *,
    evidence_id: str,
    raw_text_candidates: List[Dict[str, Any]],
    raw_text_joined: str,
    reading_direction_candidate: str,
    line_order_status: str,
    timestamp_ms: int = 0,
    frame_id: Optional[str] = None,
    source_evidence_id: Optional[str] = None,
    user_requested_override: bool = False,
    visual_source_hint: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Skeleton evidence input for MidPlatform.
    Candidate-only, semantic disabled, no execution allowed.
    """

    cands = raw_text_candidates if isinstance(raw_text_candidates, list) else []
    avg_conf = _avg_conf(cands)
    bbox = _pick_primary_bbox(cands)

    evidence: Dict[str, Any] = {
        "evidence_id": evidence_id,
        "source_modalities": ["ocr"],
        "source_evidence_id": source_evidence_id or evidence_id,
        "frame_id": frame_id,
        "timestamp_ms": int(timestamp_ms),

        "raw_text_candidates": cands,
        "raw_text_joined": raw_text_joined,
        "reading_direction_candidate": reading_direction_candidate,
        "line_order_status": line_order_status,

        # Governance boundary placeholders (must remain non-runtime)
        "candidate_only": True,
        "semantic_interpretation_enabled": False,
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "downstream_invocation_count": 0,

        # Optional skeleton routing hints
        "visual_source_hint": visual_source_hint,
        "user_requested_override": bool(user_requested_override),
        "evidence_confidence_hint": avg_conf,

        # Observability refs (placeholders; verifier checks existence)
        "trace_ref": "midplatform_ocr_bridge_trace.jsonl",
        "replay_ref": "midplatform_ocr_bridge_replay.jsonl",
        "whitebox_ref": "midplatform_ocr_bridge_whitebox.jsonl",

        # A small crop region approximation to support signature stability
        "primary_bbox": bbox,
    }
    return evidence


def run_midplatform_ocr_delta_control_v0(
    *,
    evidence_inputs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Skeleton delta control:
    - uses text_signature similarity (exact match) and confidence thresholds
    - no runtime and no external state
    """

    prev_text_sig: Optional[str] = None
    prev_layout_sig: Optional[str] = None
    prev_delta_control_id: Optional[str] = None

    out: List[Dict[str, Any]] = []

    for idx, ev in enumerate(evidence_inputs):
        evidence_id = str(ev.get("evidence_id"))
        joined = _joined_text(ev).strip()

        raw_cands = ev.get("raw_text_candidates") or []
        avg_conf = _avg_conf(raw_cands)

        bbox = _pick_primary_bbox(raw_cands) or {"x1": 0.0, "y1": 0.0, "x2": 1.0, "y2": 1.0}
        frame_id = str(ev.get("frame_id") or evidence_id)

        crop_signature = _sha_short(f"{frame_id}:{bbox['x1']},{bbox['y1']},{bbox['x2']},{bbox['y2']}")
        text_signature = _sha_short(f"text:{joined}:{ev.get('line_order_status')}")
        layout_signature = _sha_short(f"layout:{ev.get('reading_direction_candidate')}:{len(raw_cands)}:{ev.get('line_order_status')}")
        object_signature = _sha_short(f"object:{frame_id}:ocr_text_only")

        delta_control_id = f"scene_delta_{idx:03d}"
        delta_status: str
        delta_decision: str
        previous_result_ref: Optional[str] = prev_delta_control_id

        if prev_text_sig is not None and text_signature == prev_text_sig:
            # reuse previous if only text signature identical
            delta_status = "unchanged"
            delta_decision = "reuse_previous"
        else:
            if avg_conf and avg_conf < 0.35:
                delta_status = "uncertain"
                delta_decision = "hold_uncertain"
            else:
                delta_status = "changed"
                delta_decision = "full_reprocess"

        # change summary is required by contract; keep conservative fields
        text_changed = prev_text_sig is None or text_signature != prev_text_sig
        layout_changed = prev_layout_sig is None or layout_signature != prev_layout_sig

        change_summary = {
            "text_changed": bool(text_changed),
            "layout_changed": bool(layout_changed),
            "crop_shift_ratio": 0.0,
            "confidence_delta": float(avg_conf - _as_float(ev.get("evidence_confidence_hint_prev"), avg_conf)),
            "line_order_changed": False,
        }

        out.append(
            {
                "delta_control_id": delta_control_id,
                "evidence_id": evidence_id,
                "previous_result_ref": previous_result_ref,
                "crop_signature": crop_signature,
                "text_signature": text_signature,
                "layout_signature": layout_signature,
                "object_signature": object_signature,
                "comparison_window_ms": 3000,
                "delta_status": delta_status,
                "delta_decision": delta_decision,
                "change_summary": change_summary,
                "reason": "skeleton_delta_placeholder",
            }
        )

        prev_text_sig = text_signature
        prev_layout_sig = layout_signature
        prev_delta_control_id = delta_control_id

    return out


def apply_ocr_evidence_filtering_v0(
    *,
    evidence_input: Dict[str, Any],
    visual_text_relevance_class: str,
    delta_control_result: Optional[Dict[str, Any]] = None,
    classification_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    evidence_id = str(evidence_input.get("evidence_id"))
    trace_ref = str(evidence_input.get("trace_ref") or "midplatform_ocr_bridge_trace.jsonl")
    whitebox_ref = str(evidence_input.get("whitebox_ref") or "midplatform_ocr_bridge_whitebox.jsonl")

    filter_result_id = f"ocr_filter_{evidence_id}"
    retained_evidence_ref = f"retained_{evidence_id}"

    base_cls = None
    if classification_meta and isinstance(classification_meta, dict):
        base_cls = classification_meta.get("base_visual_text_relevance_class")

    # Defaults: conservative fail-closed for taskchain; ambient/world can be retained.
    block_applied = False
    block_level = "soft_block"
    block_reason: Optional[str] = None

    allowed_to_task_candidate = False
    allowed_for_primary_task_decision = False
    allowed_for_ambient_context_candidate = False
    allowed_for_world_context_candidate = False
    ambient_context_candidate_context_type: Optional[str] = None
    speech_priority = "silent_by_default"
    requires_human_or_later_review = False
    eligible_for_recheck = True

    # Uncertainty fields (for low-value visual text)
    readability_status = "unknown"  # readable | partially_readable | illegible | blurred | fragmented | uncertain
    meaning_status = "unknown"  # meaningful | non_actionable | uncertain | decorative | unknown
    requires_better_frame = False
    uncertainty_reason: Optional[str] = None
    allowed_for_user_requested_readout = bool(evidence_input.get("user_requested_override") or False)

    if visual_text_relevance_class == "task_relevant_text":
        allowed_to_task_candidate = True
        allowed_for_primary_task_decision = True
        allowed_for_world_context_candidate = False
        block_applied = False
        block_reason = None
        speech_priority = "low_priority_hint"
    elif visual_text_relevance_class == "context_relevant_text":
        allowed_to_task_candidate = True
        allowed_for_primary_task_decision = True
        requires_human_or_later_review = True
        block_applied = False
        speech_priority = "low_priority_hint"
    elif visual_text_relevance_class == "world_context_text":
        allowed_for_world_context_candidate = True
        block_applied = True
        block_level = "soft_block"
        block_reason = "irrelevant_to_current_task"
        allowed_for_ambient_context_candidate = False
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class == "commercial_context_text":
        allowed_for_ambient_context_candidate = True
        ambient_context_candidate_context_type = "commercial_context_text"
        block_applied = True
        block_level = "soft_block"
        block_reason = "irrelevant_to_current_task"
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class == "promotional_text":
        allowed_for_ambient_context_candidate = True
        ambient_context_candidate_context_type = "commercial_context_text"
        block_applied = True
        block_level = "soft_block"
        block_reason = "promotional_text"
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class == "advertisement_like_text":
        allowed_for_ambient_context_candidate = True
        ambient_context_candidate_context_type = "ambient_context_text"
        block_applied = True
        block_level = "soft_block"
        block_reason = "advertisement_like_text"
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class == "user_requested_text":
        # user-requested readout: allow a readout candidate, but still block primary task decision and world persistence by default.
        allowed_to_task_candidate = True
        block_applied = False
        allowed_for_primary_task_decision = False
        allowed_for_world_context_candidate = False
        allowed_for_ambient_context_candidate = False
        ambient_context_candidate_context_type = None
        speech_priority = "user_requested_only"

        # If the base class is low-value/uncertain, preserve uncertainty metadata.
        low_value = {
            "illegible_text",
            "blurred_text",
            "scribble_or_graffiti_text",
            "decorative_or_stylized_text",
            "fragmented_text",
            "non_actionable_text",
            "meaning_uncertain_text",
        }
        if base_cls in low_value:
            requires_human_or_later_review = True
            requires_better_frame = base_cls in ("illegible_text", "blurred_text", "fragmented_text", "meaning_uncertain_text")
            block_level = "hold_uncertain"
            uncertainty_reason = f"user_requested_from_uncertain_base:{base_cls}"
            if base_cls == "illegible_text":
                readability_status = "illegible"
                meaning_status = "unknown"
                block_reason = "illegible_or_unreadable"
            elif base_cls == "blurred_text":
                readability_status = "blurred"
                meaning_status = "unknown"
                block_reason = "blurred_or_low_quality"
            elif base_cls == "scribble_or_graffiti_text":
                readability_status = "uncertain"
                meaning_status = "unknown"
                block_reason = "scribble_or_graffiti"
            elif base_cls == "decorative_or_stylized_text":
                readability_status = "uncertain"
                meaning_status = "decorative"
                block_reason = "decorative_or_stylized"
            elif base_cls == "fragmented_text":
                readability_status = "fragmented"
                meaning_status = "unknown"
                block_reason = "fragmented_text"
            elif base_cls == "non_actionable_text":
                readability_status = "unknown"
                meaning_status = "non_actionable"
                block_reason = "non_actionable_text"
            elif base_cls == "meaning_uncertain_text":
                readability_status = "uncertain"
                meaning_status = "uncertain"
                block_reason = "meaning_uncertain"
    elif visual_text_relevance_class in ("illegible_text", "blurred_text", "scribble_or_graffiti_text", "decorative_or_stylized_text", "fragmented_text", "non_actionable_text", "meaning_uncertain_text"):
        # Low-value / uncertain visual text handling.
        allowed_to_task_candidate = False
        allowed_for_primary_task_decision = False
        allowed_for_world_context_candidate = False
        allowed_for_ambient_context_candidate = False
        ambient_context_candidate_context_type = None

        if visual_text_relevance_class == "illegible_text":
            block_applied = True
            block_level = "hold_uncertain"
            block_reason = "illegible_or_unreadable"
            readability_status = "illegible"
            meaning_status = "unknown"
            requires_human_or_later_review = True
            requires_better_frame = True
            uncertainty_reason = "illegible_or_unreadable"
        elif visual_text_relevance_class == "blurred_text":
            block_applied = True
            block_level = "hold_uncertain"
            block_reason = "blurred_or_low_quality"
            readability_status = "blurred"
            meaning_status = "unknown"
            requires_human_or_later_review = True
            requires_better_frame = True
            uncertainty_reason = "blurred_or_low_quality"
        elif visual_text_relevance_class == "scribble_or_graffiti_text":
            block_applied = True
            block_level = "soft_block"
            block_reason = "scribble_or_graffiti"
            readability_status = "uncertain"
            meaning_status = "unknown"
            requires_human_or_later_review = False
            requires_better_frame = False
            uncertainty_reason = "scribble_or_graffiti"
        elif visual_text_relevance_class == "decorative_or_stylized_text":
            block_applied = True
            block_level = "hold_uncertain"
            block_reason = "decorative_or_stylized"
            readability_status = "uncertain"
            meaning_status = "decorative"
            requires_human_or_later_review = True
            requires_better_frame = True
            uncertainty_reason = "decorative_or_stylized"
        elif visual_text_relevance_class == "fragmented_text":
            block_applied = True
            block_level = "hold_uncertain"
            block_reason = "fragmented_text"
            readability_status = "fragmented"
            meaning_status = "unknown"
            requires_human_or_later_review = True
            requires_better_frame = True
            uncertainty_reason = "fragmented_text"
        elif visual_text_relevance_class == "non_actionable_text":
            block_applied = True
            block_level = "soft_block"
            block_reason = "non_actionable_text"
            readability_status = "unknown"
            meaning_status = "non_actionable"
            requires_human_or_later_review = False
            requires_better_frame = False
            uncertainty_reason = "non_actionable_text"
        elif visual_text_relevance_class == "meaning_uncertain_text":
            block_applied = True
            block_level = "hold_uncertain"
            block_reason = "meaning_uncertain"
            readability_status = "uncertain"
            meaning_status = "uncertain"
            requires_human_or_later_review = True
            requires_better_frame = True
            uncertainty_reason = "meaning_uncertain"
        speech_priority = "silent_by_default"

    elif visual_text_relevance_class in ("decorative_text", "irrelevant_or_noise_text"):
        block_applied = True
        block_level = "soft_block" if visual_text_relevance_class == "decorative_text" else "hard_block"
        block_reason = "repeated_non_task_text"
        allowed_to_task_candidate = False
        allowed_for_primary_task_decision = False
        allowed_for_ambient_context_candidate = False
        allowed_for_world_context_candidate = False
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class == "uncertain_relevance_text":
        block_applied = True
        block_level = "hold_uncertain"
        block_reason = "low_confidence_text"
        allowed_to_task_candidate = False
        allowed_for_primary_task_decision = False
        allowed_for_ambient_context_candidate = False
        allowed_for_world_context_candidate = False
        requires_human_or_later_review = True
        speech_priority = "silent_by_default"
    elif visual_text_relevance_class in ("ambient_context_text", "experience_enrichment_text"):
        allowed_for_ambient_context_candidate = True
        ambient_context_candidate_context_type = "ambient_context_text"
        block_applied = True
        block_level = "soft_block"
        block_reason = "irrelevant_to_current_task"
        speech_priority = "low_priority_hint"
    else:
        block_applied = True
        block_level = "soft_block"
        block_reason = "irrelevant_to_current_task"

    return {
        "filter_result_id": filter_result_id,
        "evidence_id": evidence_id,
        "visual_text_relevance_class": visual_text_relevance_class,
        "block_applied": bool(block_applied),
        "block_level": block_level,
        "block_reason": block_reason,
        "retained_evidence_ref": retained_evidence_ref,
        "evidence_retention_policy": "keep_for_recheck",
        "eligible_for_recheck": bool(eligible_for_recheck),

        "allowed_to_task_candidate": bool(allowed_to_task_candidate),
        "allowed_for_primary_task_decision": bool(allowed_for_primary_task_decision),
        "allowed_for_world_context_candidate": bool(allowed_for_world_context_candidate),
        "allowed_for_ambient_context_candidate": bool(allowed_for_ambient_context_candidate),
        "ambient_context_candidate_context_type": ambient_context_candidate_context_type,
        "speech_priority": speech_priority,
        "requires_human_or_later_review": bool(requires_human_or_later_review),

        # Low-value / uncertainty fields (for contract completeness)
        "readability_status": readability_status,
        "meaning_status": meaning_status,
        "requires_better_frame": bool(requires_better_frame),
        "uncertainty_reason": uncertainty_reason,
        "allowed_for_user_requested_readout": bool(allowed_for_user_requested_readout),

        "trace_ref": trace_ref,
        "whitebox_ref": whitebox_ref,
        # keep a stable signature reference for auditability if needed
        "delta_control_deferred": True if delta_control_result else False,
        "delta_control_id": (delta_control_result or {}).get("delta_control_id"),
    }


def build_midplatform_text_extraction_candidate_v0(
    *,
    evidence_input: Dict[str, Any],
    delta_control_result: Dict[str, Any],
    filter_result: Dict[str, Any],
    visual_text_relevance_class: str,
    seq: int,
) -> Optional[Dict[str, Any]]:
    evidence_id = str(evidence_input.get("evidence_id"))
    if not filter_result.get("allowed_to_task_candidate"):
        return None

    raw_text_joined = str(evidence_input.get("raw_text_joined") or "")
    cands = evidence_input.get("raw_text_candidates") or []
    avg_conf = _avg_conf(cands)
    seg_refs: List[str] = []
    if isinstance(cands, list):
        for c in cands:
            if isinstance(c, dict):
                tid = c.get("text_id")
                if tid:
                    seg_refs.append(str(tid))

    return {
        "text_candidate_id": f"mid_text_{seq:03d}",
        "source_evidence_id": evidence_id,
        "delta_control_id": delta_control_result.get("delta_control_id"),

        "raw_text_ref": evidence_id,
        "segment_refs": seg_refs,
        "extraction_scope": "joined_preview",
        "text": raw_text_joined,
        "confidence": float(avg_conf),

        "task_relevance_status": "potentially_relevant" if visual_text_relevance_class in ("task_relevant_text", "context_relevant_text") else "blocked",
        "reason_for_relevance": (
            filter_result.get("block_reason")
            or (filter_result.get("uncertainty_reason") if visual_text_relevance_class == "user_requested_text" else None)
            or "keyword_match_skeleton"
        ),
        "semantic_summary": None,

        "navigation_action": None,
        "candidate_only": True,
        "requires_further_validation": True,
        "allows_execute_now": False,
    }


def build_world_context_evidence_candidate_v0(
    *,
    evidence_input: Dict[str, Any],
    filter_result: Dict[str, Any],
    seq: int,
    visual_text_relevance_class: str,
) -> Optional[Dict[str, Any]]:
    evidence_id = str(evidence_input.get("evidence_id"))

    # world evidence route: world_context_text and commercial/promotional/advertisement as low-priority context
    if visual_text_relevance_class not in ("world_context_text", "commercial_context_text", "promotional_text", "advertisement_like_text"):
        return None

    raw_text_joined = str(evidence_input.get("raw_text_joined") or "")
    avg_conf = _avg_conf(evidence_input.get("raw_text_candidates") or [])
    now = int(evidence_input.get("timestamp_ms") or 0)
    time_source = "midplatform_clock"

    if visual_text_relevance_class == "world_context_text":
        ttl_policy = "scene_local_ttl"
        write_policy = "scene_local_candidate"
        entity_type = "place_public_info"
        requires_user_confirmation = False
    else:
        ttl_policy = "short_ttl"
        write_policy = "low_priority_candidate"
        entity_type = "store_promotion"
        requires_user_confirmation = False

    return {
        "world_context_evidence_id": f"world_ctx_{seq:03d}",
        "source_modalities": ["ocr"],
        "source_evidence_refs": [evidence_id],
        "observed_at": {
            "timestamp_ms": now,
            "time_source": time_source,
            "date_confidence": "system_confirmed",
        },
        "observed_where": {
            "geo_location": {"lat": None, "lng": None, "accuracy_m": None},
            "place_hint": "unknown",
            "spatial_anchor_type": "unknown",
            "relative_position": {"distance_estimate_m": None, "direction_hint": None},
        },
        "content": {
            "text": raw_text_joined,
            "entity_type": entity_type,
            "entity_name": None,
            "details": raw_text_joined,
            "valid_time_text": None,
            "extracted_from": "ocr_raw_text",
        },
        "trust": {
            "source_confidence": 1.0,
            "ocr_confidence": float(avg_conf),
            "yolo_confidence": 0.0,
            "cross_validation_status": "single_source",
            "trust_score": float(min(1.0, max(0.0, avg_conf * 0.75))),
            "fraud_risk_status": "unknown",
        },
        "lifecycle": {
            "evidence_status": "active",
            "ttl_policy": ttl_policy,
            "expires_at": None,
            "requires_revalidation": True,
            "last_seen_at": now,
            "seen_count": 1,
        },
        "world_model_policy": {
            "write_policy": write_policy,
            "task_planning_impact": "none",
            "shareable_to_hive": False,
            "requires_user_confirmation": requires_user_confirmation,
        },
        "trace_ref": str(evidence_input.get("trace_ref") or "midplatform_ocr_bridge_trace.jsonl"),
        "whitebox_ref": str(evidence_input.get("whitebox_ref") or "midplatform_ocr_bridge_whitebox.jsonl"),
    }


def build_ambient_context_candidate_v0(
    *,
    evidence_input: Dict[str, Any],
    filter_result: Dict[str, Any],
    seq: int,
    visual_text_relevance_class: str,
) -> Optional[Dict[str, Any]]:
    evidence_id = str(evidence_input.get("evidence_id"))
    if not filter_result.get("allowed_for_ambient_context_candidate"):
        return None

    if visual_text_relevance_class == "promotional_text":
        context_type = "commercial_context_text"
    elif visual_text_relevance_class == "advertisement_like_text":
        context_type = "ambient_context_text"
    elif visual_text_relevance_class in ("commercial_context_text",):
        context_type = "commercial_context_text"
    else:
        context_type = "ambient_context_text"

    speech_priority = "silent_by_default"
    if visual_text_relevance_class == "user_requested_text" or evidence_input.get("user_requested_override"):
        speech_priority = "user_requested_only"

    return {
        "ambient_context_candidate_id": f"ambient_ctx_{seq:03d}",
        "source_evidence_id": evidence_id,
        "text": str(evidence_input.get("raw_text_joined") or ""),
        "context_type": context_type,
        "task_relevance_status": "supplementary",

        "allowed_for_primary_task_decision": False,
        "allowed_for_experience_enrichment": True,
        "allowed_when_user_requested": bool(evidence_input.get("user_requested_override") or False),
        "requires_user_context_match": True,

        "expiry_policy": "short_ttl",
        "requires_revalidation": True,

        "navigation_action": None,
        "speech_priority": speech_priority,

        "trace_ref": str(evidence_input.get("trace_ref") or "midplatform_ocr_bridge_trace.jsonl"),
        "whitebox_ref": str(evidence_input.get("whitebox_ref") or "midplatform_ocr_bridge_whitebox.jsonl"),
    }


def run_midplatform_ocr_text_extraction_bridge_v0(
    *,
    evidence_inputs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Offline skeleton: OCR raw text -> MidPlatform evidence layer candidates.
    No runtime calls; no semantic interpretation; no navigation; no world model write.
    """

    # 1) delta control
    delta_results = run_midplatform_ocr_delta_control_v0(evidence_inputs=evidence_inputs)

    # 2) filtering and candidates
    filter_results: List[Dict[str, Any]] = []
    text_candidates: List[Dict[str, Any]] = []
    world_candidates: List[Dict[str, Any]] = []
    ambient_candidates: List[Dict[str, Any]] = []

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    whitebox_rows: List[Dict[str, Any]] = []

    for i, ev in enumerate(evidence_inputs):
        delta = delta_results[i]
        ev_id = str(ev.get("evidence_id"))

        cls_info = classify_visual_text_relevance_v0(ev)
        visual_cls = str(cls_info.get("visual_text_relevance_class"))
        why = str(cls_info.get("why"))

        fr = apply_ocr_evidence_filtering_v0(
            evidence_input=ev,
            visual_text_relevance_class=visual_cls,
            delta_control_result=delta,
            classification_meta=cls_info,
        )
        filter_results.append(fr)

        # Candidates
        tc = build_midplatform_text_extraction_candidate_v0(
            evidence_input=ev,
            delta_control_result=delta,
            filter_result=fr,
            visual_text_relevance_class=visual_cls,
            seq=len(text_candidates) + 1,
        )
        if tc is not None:
            text_candidates.append(tc)

        wc = build_world_context_evidence_candidate_v0(
            evidence_input=ev,
            filter_result=fr,
            seq=len(world_candidates) + 1,
            visual_text_relevance_class=visual_cls,
        )
        if wc is not None:
            world_candidates.append(wc)

        ac = build_ambient_context_candidate_v0(
            evidence_input=ev,
            filter_result=fr,
            seq=len(ambient_candidates) + 1,
            visual_text_relevance_class=visual_cls,
        )
        if ac is not None:
            ambient_candidates.append(ac)

        # Trace / replay / whitebox
        world_context_candidate_created = wc is not None
        ambient_context_candidate_created = ac is not None

        trace_rows.append(
            {
                "event_type": "trace",
                "evidence_id": ev_id,
                "delta_control_id": delta.get("delta_control_id"),
                "text_signature": delta.get("text_signature"),
                "layout_signature": delta.get("layout_signature"),
                "visual_text_relevance_class": visual_cls,
                "delta_status": delta.get("delta_status"),
                "delta_decision": delta.get("delta_decision"),
                "filter_result_id": fr.get("filter_result_id"),
                "block_applied": fr.get("block_applied"),
                "block_reason": fr.get("block_reason"),
                "block_level": fr.get("block_level"),
                "candidate_generated": tc is not None,
                "task_candidate_allowed": fr.get("allowed_to_task_candidate"),
                "readability_status": fr.get("readability_status"),
                "meaning_status": fr.get("meaning_status"),
                "requires_better_frame": fr.get("requires_better_frame"),
                "uncertainty_reason": fr.get("uncertainty_reason"),
                "world_context_candidate_created": world_context_candidate_created,
                "world_context_evidence_id": (wc or {}).get("world_context_evidence_id"),
                "world_model_write_policy": (wc or {}).get("world_model_policy", {}).get("write_policy"),
                "expiry_policy": (wc or {}).get("lifecycle", {}).get("ttl_policy"),
                "requires_revalidation": (wc or {}).get("lifecycle", {}).get("requires_revalidation"),
                "allowed_when_user_requested": bool(ev.get("user_requested_override") or False),

                "ambient_context_candidate_created": ambient_context_candidate_created,
                "ambient_context_candidate_id": (ac or {}).get("ambient_context_candidate_id"),
                "ambient_context_candidate_context_type": (ac or {}).get("context_type"),
                "allowed_for_primary_task_decision": False,
                "speech_priority": (ac or {}).get("speech_priority"),
            }
        )

        replay_rows.append(
            {
                "event_type": "replay",
                "raw_evidence_ref": ev_id,
                "previous_result_ref": delta.get("previous_result_ref"),
                "signature_inputs_ref": {
                    "crop_signature": delta.get("crop_signature"),
                    "text_signature": delta.get("text_signature"),
                    "layout_signature": delta.get("layout_signature"),
                },
                "delta_decision_ref": delta.get("delta_decision"),
                "filter_result_ref": fr.get("filter_result_id"),
                "world_context_policy_decision_ref": (wc or {}).get("world_context_evidence_id"),
                "ambient_context_policy_decision_ref": (ac or {}).get("ambient_context_candidate_id"),
            }
        )

        whitebox_rows.append(
            {
                "event_type": "whitebox",
                "why_reused": "reuse_previous" if delta.get("delta_decision") == "reuse_previous" else None,
                "why_blocked": why if fr.get("block_applied") else None,
                "why_relevance_class": why,
                "why_reprocessed": "full_reprocess" if delta.get("delta_decision") == "full_reprocess" else None,
                "why_world_context_written": "world_context_candidate_from_filter" if wc is not None else None,
                "why_ambient_context_created": "ambient_context_candidate_from_filter" if ac is not None else None,
                "confidence_thresholds": {"avg_conf_uncertain_threshold": 0.35},
                "reading_order_status": ev.get("line_order_status"),
                "uncertainty_reason": fr.get("uncertainty_reason"),
                "task_context_snapshot_ref": "task_context_placeholder",
                "governance_boundary_status": "boundary_contract_only",
            }
        )

    return {
        "midplatform_text_extraction_candidates": text_candidates,
        "world_context_evidence_candidates": world_candidates,
        "ambient_context_candidates": ambient_candidates,
        "scene_delta_control_results": delta_results,
        "filter_results": filter_results,
        "trace_rows": trace_rows,
        "replay_rows": replay_rows,
        "whitebox_rows": whitebox_rows,
    }

