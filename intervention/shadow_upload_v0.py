# -*- coding: utf-8 -*-
"""
M) Shadow 数据的「最小上传与聚合协议」v0

目标：少而准、可比较、不可反推个人行为
原则：只上传聚合统计，不上传事件序列；不上传内容、文本、task_id
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

# v0 固定
LOCAL_WINDOW_SEC = 300  # 5 分钟
UPLOAD_INTERVAL_SEC = 1800  # 30 分钟（6 个窗口合并）
VERSION = "A3.1.0"


def _sum_dwell_time(rows: List[Dict[str, Any]]) -> float:
    if len(rows) < 2:
        return 0.0
    ts_list = [r.get("ts") for r in rows if r.get("ts") is not None]
    if len(ts_list) < 2:
        return 0.0
    ts_list.sort()
    return ts_list[-1] - ts_list[0]


def compute_intervention_stats(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """A) 介入结构指标"""
    active_rows = [r for r in rows if r.get("intervention", {}).get("task_state") == "ACTIVE"]
    engaged_rows = [r for r in rows if r.get("rhythm", {}).get("state") == "ENGAGED"]
    active_time = _sum_dwell_time(active_rows) if active_rows else 0
    engaged_time = _sum_dwell_time(engaged_rows) if engaged_rows else 0
    engaged_ratio = engaged_time / active_time if active_time > 0 else 0.0

    level_counter: Counter = Counter()
    for r in engaged_rows:
        lev = r.get("engagement", {}).get("level", "L0")
        level_counter[lev] += 1
    level_dist = dict(level_counter)

    rhythm_seq = [r.get("rhythm", {}).get("state") for r in rows if r.get("rhythm")]
    switches = sum(1 for i in range(1, len(rhythm_seq)) if rhythm_seq[i] != rhythm_seq[i - 1])
    duration_min = _sum_dwell_time(rows) / 60.0 if rows else 1e-6
    avg_switches_per_min = switches / max(duration_min, 1e-6)

    return {
        "active_time_s": round(active_time, 1),
        "engaged_time_s": round(engaged_time, 1),
        "engaged_ratio": round(engaged_ratio, 3),
        "level_dist": level_dist,
        "avg_switches_per_min": round(avg_switches_per_min, 2),
    }


def compute_arbitration_stats(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """B) 仲裁与公平性"""
    arb_rows = [r for r in rows if "arbitration" in r]
    if not arb_rows:
        return {"winner_type_dist": {}, "fairness_boost_rate": 0.0}

    winner_counter: Counter = Counter()
    fairness_boost_used = 0
    fairness_boost_total = 0

    def _norm_type(t: Optional[str]) -> str:
        if not t:
            return "UNKNOWN"
        t = str(t).upper()
        if "NAVIGATION" in t or t == "NAV":
            return "NAV"
        if "ENV" in t or "AWARENESS" in t:
            return "ENV"
        if "TASK" in t:
            return "TASK"
        if "SAFETY" in t:
            return "SAFETY"
        return t[:8] if len(t) > 8 else t

    for r in arb_rows:
        arb = r.get("arbitration", {})
        wtype = arb.get("winner_type") or _norm_type(arb.get("winner"))
        if arb.get("winner"):
            winner_counter[_norm_type(wtype)] += 1
        for _, info in arb.get("fairness", {}).items():
            fairness_boost_total += 1
            if info.get("boost", 0) > 0:
                fairness_boost_used += 1

    total_wins = sum(winner_counter.values())
    winner_type_dist = {k: round(v / total_wins, 2) for k, v in winner_counter.items()} if total_wins else {}
    fairness_boost_rate = round(fairness_boost_used / fairness_boost_total, 2) if fairness_boost_total else 0.0

    return {
        "winner_type_dist": winner_type_dist,
        "fairness_boost_rate": fairness_boost_rate,
    }


# J→N 过渡：engaged_signal.block_stage 映射为 legacy reason，供 gate/统计兼容
_ENGAGED_SIGNAL_BLOCK_STAGE_TO_REASON = {
    "COOLDOWN": "FAIL_COOLDOWN_ACTIVE",
    "ARBITRATION": "FAIL_ARBITRATION_LOST",
    "RHYTHM": "FAIL_RHYTHM",
    "UNKNOWN": "FAIL_UNKNOWN",
}


def compute_failure_stats(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    """C) 失败与抑制原因（兼容 engaged_failure.reason 与 engaged_signal.block_stage）"""
    counter: Counter = Counter()
    for r in rows:
        if "engaged_failure" in r:
            reason = r.get("engaged_failure", {}).get("reason", "FAIL_UNKNOWN")
            counter[reason] += 1
        elif "engaged_signal" in r:
            sig = r.get("engaged_signal", {})
            if sig.get("blocked") and sig.get("block_stage"):
                reason = _ENGAGED_SIGNAL_BLOCK_STAGE_TO_REASON.get(
                    sig["block_stage"], "FAIL_UNKNOWN"
                )
                counter[reason] += 1
    if not counter:
        return {}
    total = sum(counter.values())
    return {k: round(v / total, 2) for k, v in counter.items()}


def compute_multimodal_stats(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """D) 多模态冲突概览"""
    mc_rows = [r for r in rows if "multimodal_conflict" in r]
    if not mc_rows:
        return {"conflict_rate": 0.0, "selected_source_dist": {}}

    total_ticks = len([r for r in rows if r.get("ts") is not None])
    conflict_count = len(mc_rows)
    conflict_rate = round(conflict_count / max(total_ticks, 1), 2)

    src_counter: Counter = Counter()
    for r in mc_rows:
        sel = r.get("multimodal_conflict", {}).get("selected_source")
        if sel:
            src_counter[sel] += 1
    total_sel = sum(src_counter.values())
    selected_source_dist = {k: round(v / total_sel, 2) for k, v in src_counter.items()} if total_sel else {}

    return {
        "conflict_rate": conflict_rate,
        "selected_source_dist": selected_source_dist,
    }


def build_upload_payload(
    rows: List[Dict[str, Any]],
    device_class: str = "OTHER",
    camera_fov_class: str = "MID",
    version: str = VERSION,
) -> Dict[str, Any]:
    """
    构建 M) 最小上传 payload（v0 冻结）。

    严格不上传：文本、task_id、时间戳序列、用户操作细节
    """
    return {
        "intervention_stats": compute_intervention_stats(rows),
        "arbitration_stats": compute_arbitration_stats(rows),
        "failure_stats": compute_failure_stats(rows),
        "multimodal_stats": compute_multimodal_stats(rows),
        "device_meta": {
            "device_class": device_class,  # PHONE | BADGE | OTHER
            "camera_fov_class": camera_fov_class,  # NARROW | MID | WIDE
            "version": version,
        },
        "window_sec": LOCAL_WINDOW_SEC,
        "row_count": len(rows),
    }
