# -*- coding: utf-8 -*-
"""
F) ENGAGED「跨段稳定性体检」v0

体检层，不反馈到实时系统。
统计窗口：短期 5min / 中期 30min / 长期 1天（可离线）
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

# 期望区间
ENGAGED_RATIO_WALK_COMPLEX = (0.05, 0.20)  # 徒步复杂环境
ENGAGED_RATIO_STABLE = (0.0, 0.05)  # 稳定直行
L3_RATIO_MAX = 0.05  # L3 长期 >5% → 过度强介入
ADVICE_TYPE_SKEW_THRESHOLD = 0.70  # 单一类型 >70% → 内容单调


def compute_long_term_diagnosis(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    从 trace 行计算 long_term_diagnosis（v0 最小）。

    rows 需包含：ts, rhythm, engagement, engaged_failure 或 engaged_signal, advice_rhythm
    """
    if not rows:
        return _empty_diagnosis()

    ts_min = min(r.get("ts", 0) for r in rows)
    ts_max = max(r.get("ts", 0) for r in rows)
    duration_sec = ts_max - ts_min if ts_max > ts_min else 0

    # ① ENGAGED 密度：engaged_ratio = ENGAGED_time / ACTIVE_time
    active_rows = [r for r in rows if r.get("intervention", {}).get("task_state") == "ACTIVE"]
    engaged_rows = [r for r in rows if r.get("rhythm", {}).get("state") == "ENGAGED"]
    active_time = _sum_dwell_time(active_rows) if active_rows else 0
    engaged_time = _sum_dwell_time(engaged_rows) if engaged_rows else 0
    engaged_ratio = engaged_time / active_time if active_time > 0 else 0.0

    # ② Level 分布稳定性：P(L1), P(L2), P(L3)
    level_counter = Counter()
    for r in engaged_rows:
        lev = r.get("engagement", {}).get("level", "L0")
        level_counter[lev] += 1
    total_eng = len(engaged_rows)
    l1_ratio = level_counter.get("L1", 0) / total_eng if total_eng else 0
    l2_ratio = level_counter.get("L2", 0) / total_eng if total_eng else 0
    l3_ratio = level_counter.get("L3", 0) / total_eng if total_eng else 0

    # ③ 失败/阻断结构健康度：兼容 engaged_failure.reason 与 engaged_signal.block_stage
    _block_stage_to_reason = {
        "COOLDOWN": "FAIL_COOLDOWN_ACTIVE",
        "ARBITRATION": "FAIL_ARBITRATION_LOST",
        "RHYTHM": "FAIL_RHYTHM",
        "UNKNOWN": "FAIL_UNKNOWN",
    }
    fail_counter: Counter = Counter()
    for r in rows:
        if "engaged_failure" in r:
            fail_counter[r.get("engaged_failure", {}).get("reason", "FAIL_UNKNOWN")] += 1
        elif "engaged_signal" in r:
            sig = r.get("engaged_signal", {})
            if sig.get("blocked") and sig.get("block_stage"):
                fail_counter[_block_stage_to_reason.get(sig["block_stage"], "FAIL_UNKNOWN")] += 1
    dominant_failure = fail_counter.most_common(1)[0][0] if fail_counter else "NONE"

    # ④ 内容类型偏置：AdviceType 分布 / ENGAGED
    advice_rhythm_rows = [r for r in rows if "advice_rhythm" in r]
    advice_type_counter = Counter()
    for r in advice_rhythm_rows:
        t = r.get("advice_rhythm", {}).get("type")
        if t and r.get("advice_rhythm", {}).get("allowed", False):
            advice_type_counter[t] += 1
    total_advice = sum(advice_type_counter.values())
    advice_type_skew = "BALANCED"
    if total_advice > 0:
        max_ratio = max(advice_type_counter.values()) / total_advice
        if max_ratio >= ADVICE_TYPE_SKEW_THRESHOLD:
            dominant_type = advice_type_counter.most_common(1)[0][0]
            advice_type_skew = f"SKEW_{dominant_type}"

    # 诊断 tag
    tag = "ENGAGED_STABILITY_OK"
    urgency = "LOW"
    if l3_ratio > L3_RATIO_MAX:
        tag = "L3_OVER_INTERVENTION"
        urgency = "MEDIUM"
    elif engaged_ratio > ENGAGED_RATIO_WALK_COMPLEX[1]:
        tag = "ENGAGED_DENSITY_HIGH"
        urgency = "LOW"
    elif engaged_ratio < ENGAGED_RATIO_STABLE[0] and total_eng == 0 and active_time > 60:
        tag = "ENGAGED_NEVER"
        urgency = "LOW"
    elif dominant_failure == "FAIL_COOLDOWN_ACTIVE" and fail_counter[dominant_failure] > 10:
        tag = "RHYTHM_TOO_TIGHT"
        urgency = "LOW"
    elif dominant_failure == "FAIL_NO_ADVICE_MATCH":
        tag = "ADVICE_COVERAGE_LOW"
        urgency = "LOW"
    elif advice_type_skew.startswith("SKEW_"):
        tag = "ADVICE_TYPE_MONOTONE"
        urgency = "LOW"

    return {
        "tag": tag,
        "signals": {
            "engaged_ratio": round(engaged_ratio, 3),
            "L1_ratio": round(l1_ratio, 3),
            "L2_ratio": round(l2_ratio, 3),
            "L3_ratio": round(l3_ratio, 3),
            "dominant_failure": dominant_failure,
            "advice_type_skew": advice_type_skew,
            "duration_sec": round(duration_sec, 1),
        },
        "apply_now": False,
        "urgency": urgency,
    }


def _sum_dwell_time(rows: List[Dict[str, Any]]) -> float:
    """估算驻留总时长（按采样间隔 × 行数）。"""
    if len(rows) < 2:
        return 0.0
    ts_list = [r.get("ts") for r in rows if r.get("ts") is not None]
    if len(ts_list) < 2:
        return 0.0
    ts_list.sort()
    return ts_list[-1] - ts_list[0]


def _empty_diagnosis() -> Dict[str, Any]:
    return {
        "tag": "INSUFFICIENT_DATA",
        "signals": {},
        "apply_now": False,
        "urgency": "LOW",
    }
