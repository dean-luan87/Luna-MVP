# -*- coding: utf-8 -*-
"""
J) 仲裁结果 × Advice 类型节律「联动体检」v0

诊断层，不回馈实时系统。
统计：winner_type_dist, deferred_type_dist, fairness_boost_usage_rate
体检信号：TYPE_DOMINANCE, STRUCTURAL_STARVATION, BASE_SCORE_IMBALANCE
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

TYPE_DOMINANCE_THRESHOLD = 0.70  # 某一 task_type >70%
FAIRNESS_BOOST_HIGH_THRESHOLD = 0.50  # fairness_boost 触发率 >50%


def compute_arbitration_diagnosis(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    从 trace 行计算 arbitration_diagnosis（v0）。

    rows 需包含：arbitration（含 winner, deferred, scores, fairness）
    仅统计 ENGAGED 段内的 arbitration 事件。
    """
    if not rows:
        return _empty_diagnosis()

    arb_rows = [r for r in rows if "arbitration" in r]
    if not arb_rows:
        return _empty_diagnosis()

    # 仅 ENGAGED 段：arbitration 事件通常与 rhythm=ENGAGED 同 tick
    # 简化：arbitration 行即视为 ENGAGED 段内
    winner_type_counter: Counter = Counter()
    deferred_type_counter: Counter = Counter()
    win_count_by_type: Counter = Counter()
    defer_count_by_type: Counter = Counter()
    fairness_boost_used = 0
    fairness_boost_total = 0
    missed_by_type: Dict[str, List[int]] = defaultdict(list)

    def _infer_type(task_id: Optional[str]) -> str:
        """trace 无 type 时回退推断"""
        if not task_id:
            return "UNKNOWN"
        tid = str(task_id).lower()
        if "remind" in tid or "path" in tid:
            return "ENV_AWARENESS"
        if "wait" in tid or "adjust" in tid or "ask" in tid:
            return "TASK_STATE"
        if "nav" in tid or "nav_" in tid:
            return "NAVIGATION"
        return "TASK_STATE"

    for r in arb_rows:
        arb = r.get("arbitration", {})
        winner = arb.get("winner")
        winner_type = arb.get("winner_type")
        deferred = arb.get("deferred", [])
        deferred_types = arb.get("deferred_types", [])
        fairness = arb.get("fairness", {})

        if winner:
            wtype = winner_type or _infer_type(winner)
            winner_type_counter[wtype] += 1
            win_count_by_type[wtype] += 1

        for i, did in enumerate(deferred):
            dtype = deferred_types[i] if i < len(deferred_types) else _infer_type(did)
            deferred_type_counter[dtype] += 1
            defer_count_by_type[dtype] += 1

        for task_id, info in fairness.items():
            missed = info.get("missed", 0)
            boost = info.get("boost", 0)
            fairness_boost_total += 1
            if boost > 0:
                fairness_boost_used += 1
            ttype = _infer_type(task_id)
            missed_by_type[ttype].append(missed)

    total_arb = len(arb_rows)
    winner_type_dist = dict(winner_type_counter)
    deferred_type_dist = dict(deferred_type_counter)
    fairness_boost_usage_rate = fairness_boost_used / fairness_boost_total if fairness_boost_total else 0
    avg_missed_by_type = {k: round(sum(v) / len(v), 2) if v else 0 for k, v in missed_by_type.items()}

    # 体检信号
    tag = "ARBITRATION_OK"
    details: Dict[str, Any] = {}
    urgency = "LOW"

    # A) 类型偏置：某一 task_type >70%
    total_wins = sum(winner_type_counter.values())
    if total_wins > 0:
        for ttype, cnt in winner_type_counter.items():
            if cnt / total_wins >= TYPE_DOMINANCE_THRESHOLD:
                tag = "TYPE_DOMINANCE"
                details["dominant_type"] = ttype
                details["ratio"] = round(cnt / total_wins, 2)
                break

    # B) 结构性饿死：某 task_type 长期只 defer 不 win
    if tag == "ARBITRATION_OK":
        for ttype in set(win_count_by_type) | set(defer_count_by_type):
            wins = win_count_by_type.get(ttype, 0)
            defers = defer_count_by_type.get(ttype, 0)
            if defers >= 3 and wins == 0:
                tag = "STRUCTURAL_STARVATION"
                details["starved_type"] = ttype
                details["avg_missed"] = round(sum(missed_by_type.get(ttype, [0])) / max(len(missed_by_type.get(ttype, [1])), 1), 2)
                break

    # C) 补偿依赖过高：fairness_boost 触发率 >50%
    if tag == "ARBITRATION_OK" and fairness_boost_usage_rate >= FAIRNESS_BOOST_HIGH_THRESHOLD:
        tag = "BASE_SCORE_IMBALANCE"
        details["fairness_boost_usage_rate"] = round(fairness_boost_usage_rate, 2)

    return {
        "tag": tag,
        "details": details,
        "apply_now": False,
        "urgency": urgency,
        "signals": {
            "winner_type_dist": winner_type_dist,
            "deferred_type_dist": deferred_type_dist,
            "fairness_boost_usage_rate": round(fairness_boost_usage_rate, 2),
            "avg_missed_by_type": avg_missed_by_type,
            "total_arbitration_events": total_arb,
        },
    }


def _empty_diagnosis() -> Dict[str, Any]:
    return {
        "tag": "INSUFFICIENT_DATA",
        "details": {},
        "apply_now": False,
        "urgency": "LOW",
        "signals": {},
    }
