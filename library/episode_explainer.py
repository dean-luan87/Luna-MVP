# -*- coding: utf-8 -*-
"""
Phase 3.2-Explain Core: OBS_V1 + decision -> structured_explain.
不接 LLM、不 import runtime/intervention/a3、不读外部感知字段。
"""
from typing import Any, Dict, List, Optional

EXPLAIN_VERSION = "v1.0.0"
ENGINE_VERSION = "runtime_v1.1"

OBS_NUMERIC = ("motion", "path", "branch", "roi", "pal", "complexity", "vc")
OBS_ENUM = ("frame_quality", "control_mode")
DECISION_FIELDS = ("safety_level", "control_mode", "complexity_score", "advice_budget_scale", "pal_lookahead_m")

# 固定顺序：先 decision 关键枚举，再 obs 关键，再 decision 数值
FOCUS_ORDER = [
    "decision.safety_level",
    "decision.control_mode",
    "obs.frame_quality",
    "obs.pal",
    "obs.complexity",
    "obs.vc",
    "decision.pal_lookahead_m",
]


def _safe_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _get_obs(rec: Dict[str, Any], key: str) -> Any:
    if key in ("ocr_text", "map_hint", "speech_event") or "_produced_ts" in key:
        return None
    obs = rec.get("obs") or {}
    return obs.get(key)


def _get_decision(rec: Dict[str, Any], key: str) -> Any:
    dec = rec.get("decision") or {}
    return dec.get(key)


def _filter_obs_v1(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for r in records if (r.get("record_type") or "").strip() == "OBS_V1"]


def _build_field_deltas(records: List[Dict[str, Any]]) -> Dict[str, Optional[float]]:
    """center - pre；若 pre 不存在则 delta=0.0。至少包含 complexity_delta, pal_delta。"""
    out = {}
    for key in OBS_NUMERIC:
        out[f"{key}_delta"] = None
    if not records:
        out["complexity_delta"] = 0.0
        out["pal_delta"] = 0.0
        return out
    idx = len(records) // 2
    center = records[idx]
    pre = records[idx - 1] if idx >= 1 else None
    for key in OBS_NUMERIC:
        c_val = _safe_float(_get_obs(center, key))
        p_val = _safe_float(_get_obs(pre, key)) if pre else None
        if c_val is not None and p_val is not None:
            out[f"{key}_delta"] = c_val - p_val
        elif c_val is not None:
            out[f"{key}_delta"] = c_val - 0.0
        else:
            out[f"{key}_delta"] = 0.0 if key in ("complexity", "pal") else None
    if out.get("complexity_delta") is None:
        out["complexity_delta"] = 0.0
    if out.get("pal_delta") is None:
        out["pal_delta"] = 0.0
    return out


def _detect_pre_danger(structured_explain: Dict[str, Any]) -> Dict[str, Any]:
    """
    PRE-DANGER 识别：纯规则，不读外部字段，不改变 safety_level/枚举。
    满足任一即 pre_danger_flag=True。
    输出 {"pre_danger_flag": bool, "pre_danger_reason": str}。
    """
    risk = structured_explain.get("risk_analysis") or {}
    decision = structured_explain.get("decision_analysis") or {}
    control_mode = (decision.get("control_mode") or "").strip().upper()
    complexity_delta = risk.get("complexity_delta")
    pal_delta = risk.get("pal_delta")
    pal_lookahead_m = decision.get("pal_lookahead_m")
    # 明显缩短：存在且 < 1.5 视为提前收缩
    pal_lookahead_short = pal_lookahead_m is not None and _safe_float(pal_lookahead_m) is not None and _safe_float(pal_lookahead_m) < 1.5
    if control_mode == "GUARDED":
        return {"pre_danger_flag": True, "pre_danger_reason": "control_mode shifted to GUARDED before danger"}
    if complexity_delta is not None and _safe_float(complexity_delta) is not None and _safe_float(complexity_delta) > 0:
        return {"pre_danger_flag": True, "pre_danger_reason": "risk_analysis.complexity_delta > 0"}
    if pal_delta is not None and _safe_float(pal_delta) is not None and _safe_float(pal_delta) < 0:
        return {"pre_danger_flag": True, "pre_danger_reason": "risk_analysis.pal_delta < 0"}
    if pal_lookahead_short:
        return {"pre_danger_flag": True, "pre_danger_reason": "decision.pal_lookahead_m shortened"}
    return {"pre_danger_flag": False, "pre_danger_reason": ""}


def _build_structured_explain(
    records: List[Dict[str, Any]],
    field_deltas: Dict[str, Optional[float]],
) -> Dict[str, Any]:
    """四块结构，键与清单一致。"""
    if not records:
        return {
            "environment": {},
            "risk_analysis": {},
            "engagement_analysis": {},
            "decision_analysis": {},
        }
    idx = len(records) // 2
    rec = records[idx]
    obs = rec.get("obs") or {}
    dec = rec.get("decision") or {}

    def o(k: str):
        return obs.get(k) if k in OBS_NUMERIC or k in OBS_ENUM else None

    def d(k: str):
        return dec.get(k) if k in DECISION_FIELDS else None

    risk_analysis: Dict[str, Any] = {
        "pal": o("pal"),
        "complexity": o("complexity"),
        "complexity_delta": field_deltas.get("complexity_delta"),
        "pal_delta": field_deltas.get("pal_delta"),
        "frame_quality": o("frame_quality"),
    }
    structured = {
        "environment": {
            "motion": o("motion"),
            "path": o("path"),
            "branch": o("branch"),
            "roi": o("roi"),
        },
        "risk_analysis": risk_analysis,
        "engagement_analysis": {
            "control_mode": o("control_mode") or d("control_mode"),
            "vc": o("vc"),
        },
        "decision_analysis": {
            "safety_level": d("safety_level"),
            "control_mode": d("control_mode"),
            "advice_budget_scale": d("advice_budget_scale"),
            "pal_lookahead_m": d("pal_lookahead_m"),
            "complexity_score": d("complexity_score"),
        },
    }
    pre_danger = _detect_pre_danger(structured)
    risk_analysis["pre_danger_flag"] = pre_danger["pre_danger_flag"]
    risk_analysis["pre_danger_reason"] = pre_danger["pre_danger_reason"]
    return structured


def _compute_focus_fields(records: List[Dict[str, Any]]) -> List[str]:
    """固定顺序输出关键字段列表，保证包含 decision.safety_level 等。"""
    if not records:
        return list(FOCUS_ORDER)
    return list(FOCUS_ORDER)


def _calculate_completeness(structured: Dict[str, Any]) -> float:
    """非 null 关键字段数量 / 关键字段总数。"""
    env = structured.get("environment") or {}
    risk = structured.get("risk_analysis") or {}
    engagement = structured.get("engagement_analysis") or {}
    decision = structured.get("decision_analysis") or {}
    keys = [
        env.get("motion"),
        env.get("path"),
        env.get("branch"),
        env.get("roi"),
        risk.get("pal"),
        risk.get("complexity"),
        risk.get("frame_quality"),
        engagement.get("vc"),
        decision.get("safety_level"),
        decision.get("control_mode"),
    ]
    total = len(keys)
    non_null = sum(1 for v in keys if v is not None)
    return round(non_null / total, 3) if total else 0.0


class EpisodeExplainer:
    """离线 Explain Core：只读 OBS_V1 + decision 白名单，输出 structured_explain。"""

    def explain_episode(
        self,
        episode_id: str,
        trigger_type: str,
        records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        只处理 record_type == "OBS_V1" 的记录。
        center = records[len(records)//2]，pre/post 为前后一条。
        """
        filtered = _filter_obs_v1(records or [])
        if not filtered:
            structured_empty = {
                "environment": {},
                "risk_analysis": {},
                "engagement_analysis": {},
                "decision_analysis": {},
            }
            return {
                "episode_id": episode_id,
                "trigger_type": trigger_type,
                "structured_explain": structured_empty,
                "focus_fields": list(FOCUS_ORDER),
                "field_deltas": {"complexity_delta": 0.0, "pal_delta": 0.0},
                "completeness_score": _calculate_completeness(structured_empty),
                "explain_version": EXPLAIN_VERSION,
                "engine_version": ENGINE_VERSION,
                "model_name": "template",
            }

        field_deltas = _build_field_deltas(filtered)
        structured_explain = _build_structured_explain(filtered, field_deltas)
        focus_fields = _compute_focus_fields(filtered)
        completeness_score = _calculate_completeness(structured_explain)

        return {
            "episode_id": episode_id,
            "trigger_type": trigger_type,
            "structured_explain": structured_explain,
            "focus_fields": focus_fields,
            "field_deltas": field_deltas,
            "completeness_score": completeness_score,
            "explain_version": EXPLAIN_VERSION,
            "engine_version": ENGINE_VERSION,
            "model_name": "template",
        }
