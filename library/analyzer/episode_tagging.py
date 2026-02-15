# -*- coding: utf-8 -*-
"""
Phase 3.2: EpisodeTagger — 派生标签，只写新文件（outputs/），不回写 meta/records。
禁止 import: runtime / a3 / intervention / external / main
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List

HIGH_COMPLEXITY_THRESHOLD = 0.8
LOW_VC_THRESHOLD = 0.5


def _has_speech_event(records: List[Dict[str, Any]]) -> bool:
    for rec in records:
        obs = rec.get("obs") or {}
        ev = obs.get("speech_event") or ""
        if ev and str(ev).strip():
            return True
    return False


def _safety_sequence_from_records(records: List[Dict[str, Any]]) -> List[Any]:
    out = []
    for rec in records:
        dec = rec.get("decision") or {}
        s = dec.get("safety_level")
        if s is not None:
            out.append(s)
    return out


def _safety_oscillation(seq: List[Any]) -> bool:
    """A→B→A 回跳"""
    if len(seq) < 3:
        return False
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 2] and seq[i] != seq[i + 1]:
            return True
    return False


def _has_caution(records: List[Dict[str, Any]]) -> bool:
    """任一帧 decision.safety_level == CAUTION（PRE-DANGER 高价值样本）。"""
    for rec in records:
        sl = (rec.get("decision") or {}).get("safety_level") or ""
        if str(sl).strip().upper() == "CAUTION":
            return True
    return False


def _has_control_mode_switch(records: List[Dict[str, Any]]) -> bool:
    """control_mode 在帧间发生过切换。"""
    modes = []
    for rec in records:
        m = (rec.get("decision") or {}).get("control_mode")
        if m is not None:
            modes.append(str(m).strip())
    if len(modes) <= 1:
        return False
    return any(modes[i] != modes[i - 1] for i in range(1, len(modes)))


def _has_negative_pal_trend(records: List[Dict[str, Any]]) -> bool:
    """obs.pal 在相邻帧中明显下降（pal_delta 为负的代理）。"""
    pals = []
    for rec in records:
        obs = rec.get("obs") or {}
        p = obs.get("pal")
        if p is not None:
            try:
                pals.append(float(p))
            except (TypeError, ValueError):
                pass
    if len(pals) < 2:
        return False
    return any(pals[i] < pals[i - 1] for i in range(1, len(pals)))


def compute_tags(summary: Dict[str, Any], records: List[Dict[str, Any]]) -> List[str]:
    tags: List[str] = []
    if _has_speech_event(records):
        tags.append("HAS_SPEECH_EVENT")

    if _safety_oscillation(_safety_sequence_from_records(records)):
        tags.append("SAFETY_OSCILLATION")

    vc_min = summary.get("vc_min")
    if vc_min is not None and vc_min > 0 and vc_min < LOW_VC_THRESHOLD:
        tags.append("LOW_VC_PRESENT")

    comp_max = summary.get("complexity_max")
    if comp_max is not None and comp_max >= HIGH_COMPLEXITY_THRESHOLD:
        tags.append("HIGH_COMPLEXITY")

    if _has_caution(records):
        tags.append("HAS_CAUTION")
    if _has_control_mode_switch(records):
        tags.append("CONTROL_MODE_SWITCH")
    if _has_negative_pal_trend(records):
        tags.append("NEGATIVE_PAL_TREND")

    return tags


def write_episode_tags(rows: List[Dict[str, Any]], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            line = {
                "version_tag": row.get("version_tag"),
                "session_id": row.get("session_id"),
                "episode_id": row.get("episode_id"),
                "tags": row.get("tags", []),
                "created_at": created_at,
            }
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

