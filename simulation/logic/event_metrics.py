# -*- coding: utf-8 -*-
"""
Phase 2: 事件级指标抽取。复用 Phase 1 的 control_mode 口径（不依赖 risk_raw）。
RISK_STATES = {CAUTION, GUARDED}；一个事件 = 进入风险态的连续段落直到退出。
"""
from typing import Any, Dict, List

RISK_STATES = frozenset({"CAUTION", "GUARDED"})


def _control_mode(frame: Dict[str, Any]) -> str:
    dec = frame.get("decision")
    if not dec or not isinstance(dec, dict):
        return "NONE"
    cm = dec.get("control_mode")
    if cm is None or (isinstance(cm, str) and not cm.strip()):
        return "NONE"
    return (cm if isinstance(cm, str) else str(cm)).strip().upper()


def _is_risk(mode: str) -> bool:
    return mode in RISK_STATES


def extract_risk_events(frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    从帧列表提取风险事件。帧需含 seq 与 decision.control_mode（缺失视为 NONE）。
    返回列表，每项：entry_seq, exit_seq, dwell_frames, enter_mode, max_mode, switch_count_within_event。
    """
    if not frames:
        return []
    # 按 seq 排序
    seq_mode: List[tuple] = []
    for f in frames:
        seq = f.get("seq")
        if seq is None:
            continue
        try:
            seq = int(seq)
        except (TypeError, ValueError):
            continue
        mode = _control_mode(f)
        seq_mode.append((seq, mode))
    seq_mode.sort(key=lambda x: x[0])
    events: List[Dict[str, Any]] = []
    in_risk = False
    entry_seq: int = 0
    enter_mode = ""
    modes_in_event: List[str] = []
    switch_count = 0
    prev_mode = ""
    for seq, mode in seq_mode:
        risk = _is_risk(mode)
        if not in_risk and risk:
            in_risk = True
            entry_seq = seq
            enter_mode = mode
            modes_in_event = [mode]
            switch_count = 0
            prev_mode = mode
        elif in_risk and not risk:
            in_risk = False
            dwell = max(0, seq - entry_seq)
            max_mode = "GUARDED" if "GUARDED" in modes_in_event else "CAUTION"
            events.append({
                "entry_seq": entry_seq,
                "exit_seq": seq,
                "dwell_frames": dwell,
                "enter_mode": enter_mode,
                "max_mode": max_mode,
                "switch_count_within_event": switch_count,
            })
            prev_mode = mode
        elif in_risk and risk:
            modes_in_event.append(mode)
            if mode != prev_mode:
                switch_count += 1
            prev_mode = mode
    if in_risk and seq_mode:
        last_seq = seq_mode[-1][0]
        dwell = max(0, last_seq - entry_seq + 1)
        max_mode = "GUARDED" if "GUARDED" in modes_in_event else "CAUTION"
        events.append({
            "entry_seq": entry_seq,
            "exit_seq": last_seq + 1,
            "dwell_frames": dwell,
            "enter_mode": enter_mode,
            "max_mode": max_mode,
            "switch_count_within_event": switch_count,
        })
    return events


def summarize_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    事件级汇总：p50/p95/max dwell, event_count, total_risk_frames 等。
    """
    if not events:
        return {
            "event_count": 0,
            "total_risk_frames": 0,
            "dwell_p50": 0,
            "dwell_p95": 0,
            "dwell_max": 0,
        }
    dwells = [e["dwell_frames"] for e in events]
    dwells_sorted = sorted(dwells)
    n = len(dwells_sorted)
    total_risk_frames = sum(dwells)
    return {
        "event_count": len(events),
        "total_risk_frames": total_risk_frames,
        "dwell_p50": dwells_sorted[int((n - 1) * 0.50)] if n else 0,
        "dwell_p95": dwells_sorted[int((n - 1) * 0.95)] if n else 0,
        "dwell_max": max(dwells) if dwells else 0,
    }
