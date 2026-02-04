# vision_pipeline/b2/v03/evidence_pack.py
from __future__ import annotations
from typing import Dict, Any, List, Optional, Optional


def summarize_factors(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    从记录级证据中提取"主导变化因子"
    """
    summary: Dict[str, float] = {}

    for r in records:
        for k, v in r["confidence"].items():
            summary[k] = max(summary.get(k, 0.0), v)

    # 只保留变化明显的
    return {
        k: round(v, 2)
        for k, v in sorted(summary.items(), key=lambda x: x[1], reverse=True)
        if v >= 0.2
    }


def build_evidence_pack(
    window: Dict[str, Any],
    decision: str,
    main_factor: str,
    confidence: float,
    keyframes: Dict[str, int],
    param_vector: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    表达级证据包（人类可读）
    """

    records = window.get("records", [])

    pack = {
        "decision": decision,
        "main_factor": main_factor,
        "confidence": round(confidence, 2),

        "window": {
            "start_t": window.get("start_t"),
            "end_t": window.get("end_t"),
            "record_count": window.get("count"),
        },

        "dominant_factors": summarize_factors(records),

        "keyframes": {
            "before": keyframes.get("before"),
            "at": keyframes.get("at"),
            "after": keyframes.get("after"),
        },
    }

    # 附加 param_vector（可选，不污染主体结构）
    if param_vector is not None:
        pack["param_vector"] = param_vector

    return pack

