# -*- coding: utf-8 -*-
"""
主线 1.3A：视线/视觉连续性守护（View Guard）。

最小规则型判断：镜头是否对准该看的方向、当前视觉输入是否仍可靠。
不做复杂姿态估计、对象级几何、预测模型。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# 视觉退化判定阈值
_VIEW_CONFIDENCE_DEGRADED = 0.5
_OCCLUSION_RATIO_DEGRADED = 0.8
_BLUR_SCORE_DEGRADED = 0.6
_MOTION_INSTABILITY_SHAKE = 0.6
# 恢复时间估计（规则型，毫秒）
_ETA_GOOD_MS = 0.0
_ETA_DEGRADED_MS = 500.0
_ETA_INVALID_MS = 1000.0


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def evaluate(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据 ctx 中的视觉/质量信号输出 view_guard 字段。
    ctx 可包含（来自 pipeline / main）：
    - frame_quality: GOOD / DEGRADED / INVALID
    - view_confidence: float 0~1
    - occlusion_ratio: float 0~1
    - occlusion_state: CLEAR / OCCLUDED / UNKNOWN
    - perception_state: NORMAL / DEGRADED
    - motion_instability: float 0~1（抖动）
    - blur_score / metrics.blur_score
    - forward_view_valid: bool（可选，无则视线对齐保守为 assumed_ok）
    """
    frame_quality = ctx.get("frame_quality")
    if frame_quality is None and ctx.get("pipeline_result"):
        frame_quality = _get(ctx["pipeline_result"], "frame_quality")
    view_confidence = ctx.get("view_confidence")
    if view_confidence is None and ctx.get("pipeline_result"):
        view_confidence = _get(ctx["pipeline_result"], "view_confidence")
    occlusion_ratio = ctx.get("occlusion_ratio")
    if occlusion_ratio is None and ctx.get("pipeline_result"):
        occlusion_ratio = _get(ctx["pipeline_result"], "occlusion_ratio")
    occlusion_state = ctx.get("occlusion_state")
    if occlusion_state is not None and hasattr(occlusion_state, "value"):
        occlusion_state = occlusion_state.value
    perception_state = ctx.get("perception_state")
    motion_instability = ctx.get("motion_instability")
    if motion_instability is None and ctx.get("pipeline_result"):
        motion_instability = _get(ctx["pipeline_result"], "motion_instability")
    blur_score = ctx.get("blur_score")
    metrics = ctx.get("metrics") or (ctx.get("pipeline_result") or {}).get("metrics") if isinstance(ctx.get("pipeline_result"), dict) else {}
    if blur_score is None:
        blur_score = _get(metrics, "blur_score", 0.0)
    forward_view_valid = ctx.get("forward_view_valid")

    # ----- 视线对齐（A） -----
    view_alignment_state = "assumed_ok"
    view_alignment_score = 1.0
    view_misaligned = False
    view_correction_needed = False
    view_correction_hint = None
    if forward_view_valid is False:
        view_alignment_state = "misaligned"
        view_alignment_score = 0.0
        view_misaligned = True
        view_correction_needed = True
        view_correction_hint = "目标要求前向观察，但当前无前向有效信息，建议纠正镜头方向"
    elif forward_view_valid is True:
        view_alignment_state = "aligned"
        view_alignment_score = 1.0
    # 无 forward_view_valid 时保持 assumed_ok，不主动判偏航

    # ----- 视觉质量（B） -----
    vision_quality_state = "unknown"
    vision_reliability_score = 1.0
    vision_degraded = False
    vision_degrade_reason = None
    vision_recovery_eta_ms = _ETA_GOOD_MS

    fq = str(frame_quality).upper() if frame_quality else ""
    vc = float(view_confidence) if view_confidence is not None else 1.0
    occ_ratio = float(occlusion_ratio) if occlusion_ratio is not None else 0.0
    occ = str(occlusion_state).upper() if occlusion_state else ""
    blur = float(blur_score) if blur_score is not None else 0.0
    motion = float(motion_instability) if motion_instability is not None else 0.0

    if fq == "INVALID" or vc <= 0.0:
        vision_quality_state = "invalid"
        vision_reliability_score = 0.0
        vision_degraded = True
        vision_degrade_reason = "no_forward_view"  # 或无有效帧
        vision_recovery_eta_ms = _ETA_INVALID_MS
    elif fq == "DEGRADED" or vc < _VIEW_CONFIDENCE_DEGRADED or (str(perception_state or "").upper() == "DEGRADED"):
        vision_quality_state = "degraded"
        vision_reliability_score = max(0.0, min(1.0, vc))
        vision_degraded = True
        reasons = []
        if occ_ratio >= _OCCLUSION_RATIO_DEGRADED or occ == "OCCLUDED":
            reasons.append("occluded")
        if blur >= _BLUR_SCORE_DEGRADED:
            reasons.append("blur")
        if motion >= _MOTION_INSTABILITY_SHAKE:
            reasons.append("shake")
        vision_degrade_reason = "+".join(reasons) if reasons else "degraded_quality"
        vision_recovery_eta_ms = _ETA_DEGRADED_MS
    else:
        vision_quality_state = "good"
        vision_reliability_score = max(0.0, min(1.0, vc if vc else 1.0))
        vision_degraded = False
        vision_recovery_eta_ms = _ETA_GOOD_MS

    return {
        "view_alignment_state": view_alignment_state,
        "view_alignment_score": view_alignment_score,
        "view_misaligned": view_misaligned,
        "view_correction_needed": view_correction_needed,
        "view_correction_hint": view_correction_hint,
        "vision_quality_state": vision_quality_state,
        "vision_reliability_score": vision_reliability_score,
        "vision_degraded": vision_degraded,
        "vision_degrade_reason": vision_degrade_reason,
        "vision_recovery_eta_ms": vision_recovery_eta_ms,
    }
