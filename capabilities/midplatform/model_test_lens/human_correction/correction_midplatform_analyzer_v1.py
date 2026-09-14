# -*- coding: utf-8 -*-
"""Midplatform Human Correction analyzer — classify, attribute, route. No direct training."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

MODEL_ERROR_TYPES = frozenset({
    "false_positive", "false_negative", "wrong_label", "boundary_inaccurate",
    "confidence_mismatch", "duplicate_detection",
})
TASK_STRATEGY_TYPES = frozenset({"task_relevance_error", "recommendation_error"})
ATTENTION_TYPES = frozenset({"priority_wrong"})
ENVIRONMENT_TYPES = frozenset({
    "low_light", "occlusion", "motion_blur", "reflective_glare", "crowded_scene",
    "small_or_far_target", "background_interference", "image_quality_poor",
})

PREFERENCE_PATTERNS = (
    r"更关注", r"想看", r"偏好", r"优先看", r"我关心", r"我主要",
)
ATTENTION_IGNORE_PATTERNS = (
    r"不用看", r"不重要", r"忽略", r"别关注", r"优先级.*不对", r"不用管",
)
TASK_MISMATCH_PATTERNS = (
    r"不是我要", r"任务.*错", r"找错", r"应该看", r"我想看",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _note_text(correction: Dict[str, Any]) -> str:
    return str(correction.get("manual_annotation") or correction.get("user_note") or "")


def _correction_types(correction: Dict[str, Any]) -> List[str]:
    types = correction.get("correction_types") or []
    if not types and correction.get("correction_type"):
        types = [correction["correction_type"]]
    return list(types)


def _target_region_id(correction: Dict[str, Any]) -> str:
    target = correction.get("correction_target") or {}
    return (
        target.get("source_object_id")
        or target.get("target_id")
        or correction.get("target_region_id")
        or ""
    )


def _match_any(text: str, patterns: Sequence[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def classify_attribution(correction: Dict[str, Any]) -> Dict[str, str]:
    """Return attribution_id and human-readable reason."""
    note = _note_text(correction)
    types = set(_correction_types(correction))

    if _match_any(note, PREFERENCE_PATTERNS):
        return {
            "attribution_id": "user_preference",
            "attribution_label_zh": "用户偏好",
            "attribution_reason": "用户表达个体关注偏好，非模型错误断言",
        }

    if types & ATTENTION_TYPES or _match_any(note, ATTENTION_IGNORE_PATTERNS):
        return {
            "attribution_id": "attention_priority_error",
            "attribution_label_zh": "关注度/优先级问题",
            "attribution_reason": "纠错指向关注度或优先级，非分割/识别本身",
        }

    if types & TASK_STRATEGY_TYPES or _match_any(note, TASK_MISMATCH_PATTERNS):
        return {
            "attribution_id": "task_strategy_error",
            "attribution_label_zh": "任务/策略问题",
            "attribution_reason": "纠错指向任务目标或路由策略",
        }

    if types & ENVIRONMENT_TYPES and not (types & MODEL_ERROR_TYPES):
        return {
            "attribution_id": "environment_limitation",
            "attribution_label_zh": "环境/成像限制",
            "attribution_reason": "环境因素为主，不直接作为模型训练标签",
        }

    if types & MODEL_ERROR_TYPES:
        primary = sorted(types & MODEL_ERROR_TYPES)[0]
        return {
            "attribution_id": "model_error",
            "attribution_label_zh": "模型问题",
            "attribution_reason": f"纠错类型 {primary} 指向模型输出问题",
        }

    return {
        "attribution_id": "attention_priority_error",
        "attribution_label_zh": "关注度/优先级问题",
        "attribution_reason": "未明确模型错误，默认作为 priority/context 信号",
    }


def route_destinations(attribution_id: str, correction: Dict[str, Any]) -> List[str]:
    routes: Dict[str, List[str]] = {
        "model_error": [
            "model_training_data_candidate",
            "model_rerun_candidate",
            "new_task_candidate",
        ],
        "task_strategy_error": [
            "routing_policy_update_candidate",
            "decision_layer_review_candidate",
        ],
        "attention_priority_error": [
            "attention_policy_update_candidate",
            "priority_update_signal",
            "new_task_candidate",
        ],
        "user_preference": [
            "user_preference_update_candidate",
            "knowledge_memory_update_candidate",
        ],
        "environment_limitation": [
            "attention_policy_update_candidate",
            "human_review_candidate",
        ],
    }
    dest = list(routes.get(attribution_id, ["human_review_candidate"]))
    types = set(_correction_types(correction))
    if attribution_id == "model_error" and "boundary_inaccurate" in types:
        if "model_rerun_candidate" not in dest:
            dest.append("model_rerun_candidate")
    return dest


def training_candidate_status(attribution_id: str) -> str:
    if attribution_id == "model_error":
        return "pending_review"
    return "not_applicable"


def impact_for_attribution(attribution_id: str) -> str:
    mapping = {
        "model_error": "training_signal_pending_review",
        "task_strategy_error": "task_routing_signal",
        "attention_priority_error": "priority_signal",
        "user_preference": "preference_signal",
        "environment_limitation": "context_signal",
    }
    return mapping.get(attribution_id, "priority_signal")


def build_purified_training_signal(
    correction: Dict[str, Any],
    attribution: Dict[str, str],
) -> Optional[Dict[str, Any]]:
    if attribution["attribution_id"] != "model_error":
        return None
    types = _correction_types(correction)
    target = correction.get("correction_target") or {}
    return {
        "signal_id": f"training_signal_{correction.get('correction_id', 'unknown')}",
        "correction_ref": correction.get("correction_id"),
        "correction_type": types[0] if types else "unknown",
        "target_region_id": _target_region_id(correction),
        "source_model": correction.get("source_model_id"),
        "source_model_category": correction.get("source_model_category"),
        "confidence": correction.get("source_confidence"),
        "confirmed_by": "human",
        "training_candidate": True,
        "needs_owner_review": True,
        "not_auto_training_data": True,
        "not_ground_truth": True,
        "user_feedback": _note_text(correction),
        "target_display_name": target.get("target_display_name"),
    }


def analyze_correction(correction: Dict[str, Any]) -> Dict[str, Any]:
    """Midplatform entry: raw correction → analysis record + optional purified signal."""
    attribution = classify_attribution(correction)
    attr_id = attribution["attribution_id"]
    destinations = route_destinations(attr_id, correction)
    training_status = training_candidate_status(attr_id)
    impact = impact_for_attribution(attr_id)

    analysis = {
        "analysis_id": f"cma_{correction.get('correction_id', 'unknown')}",
        "correction_ref": correction.get("correction_id"),
        "source_model_id": correction.get("source_model_id"),
        "target_region_id": _target_region_id(correction),
        "attribution_id": attr_id,
        "attribution_label_zh": attribution["attribution_label_zh"],
        "attribution_reason": attribution["attribution_reason"],
        "routing_destinations": destinations,
        "impact": impact,
        "training_candidate": training_status,
        "model_rerun_candidate": (
            attr_id == "model_error"
            and ("boundary_inaccurate" in _correction_types(correction)
                 or "false_negative" in _correction_types(correction))
        ),
        "new_task_candidate_refs": [],
        "candidate_only": True,
        "not_fact": True,
        "not_ground_truth": True,
        "not_auto_training_data": True,
        "must_not_modify_model_output": True,
        "analyzed_at": _now_iso(),
    }

    purified = build_purified_training_signal(correction, attribution)
    if purified:
        analysis["purified_training_signal"] = purified

    return analysis


def decide_post_correction_actions(
    analysis: Dict[str, Any],
    *,
    source_result_envelope: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Case 2: MobileSAM result + user correction → rerun vs training vs reschedule.
    """
    attr_id = analysis.get("attribution_id")
    region_id = analysis.get("target_region_id") or (source_result_envelope or {}).get("region_id")
    actions: List[Dict[str, Any]] = []

    if analysis.get("model_rerun_candidate"):
        actions.append({
            "action_type": "model_rerun_candidate",
            "target_model_id": analysis.get("source_model_id") or "mobile_sam",
            "source_region_id": region_id,
            "reason": "模型边界/漏识别纠错 — 中台建议 MobileSAM 复跑候选",
            "not_modify_mask": True,
            "candidate_only": True,
        })

    if attr_id == "attention_priority_error":
        actions.append({
            "action_type": "priority_update_signal",
            "source_region_id": region_id,
            "priority_direction": "downgrade",
            "reason": "用户指示区域不必关注 — 调整 attention 策略",
            "candidate_only": True,
        })

    if attr_id == "task_strategy_error":
        actions.append({
            "action_type": "routing_policy_update_candidate",
            "reason": "任务理解偏差 — 调整路由策略",
            "candidate_only": True,
        })

    if attr_id == "user_preference":
        actions.append({
            "action_type": "user_preference_update_candidate",
            "reason": "用户偏好信号 — 进入 Preference Memory 候选",
            "candidate_only": True,
        })

    if training_status := analysis.get("training_candidate"):
        if training_status == "pending_review":
            actions.append({
                "action_type": "model_training_data_candidate",
                "status": "pending_review",
                "not_direct_training": True,
                "candidate_only": True,
            })

    new_tasks = []
    if attr_id in ("model_error", "attention_priority_error"):
        if "new_task_candidate" in (analysis.get("routing_destinations") or []):
            new_tasks.append({
                "task_candidate_id": f"T-rerun-{region_id or 'scene'}",
                "recommended_runner_type": analysis.get("source_model_id") or "mobile_sam",
                "source_region_id": region_id,
                "trigger_mode": "manual_only",
                "runner_task_candidate_only": True,
                "candidate_only": True,
            })

    return {
        "analysis_ref": analysis.get("analysis_id"),
        "post_correction_actions": actions,
        "new_task_candidates": new_tasks,
        "forbidden": ["modify_mask", "direct_training_pipeline", "write_fact"],
        "candidate_only": True,
    }
