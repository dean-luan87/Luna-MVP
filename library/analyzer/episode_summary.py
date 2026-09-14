# -*- coding: utf-8 -*-
"""
Phase 3.2: EpisodeSummary — 描述性统计（不输出结论、不引入随机性）。
禁止使用 produced_ts 做任何逻辑判断。
"""
from typing import Any, Dict, List, Optional


def _unique_order(xs: List[Any]) -> List[Any]:
    out = []
    seen = set()
    for x in xs:
        key = str(x)
        if key in seen:
            continue
        seen.add(key)
        out.append(x)
    return out


def _as_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def build_summary(meta: Dict[str, Any], records: List[Dict[str, Any]], parse_errors: int = 0) -> Dict[str, Any]:
    # 基础字段
    version_tag = meta.get("version_tag")
    session_id = meta.get("session_id")
    episode_id = meta.get("episode_id")
    trigger_type = meta.get("trigger_type")
    trigger_seq = meta.get("trigger_seq")

    # record_count / ts / duration
    record_count = len(records)
    ts_values = []
    for rec in records:
        t = _as_float(rec.get("ts"))
        if t is not None:
            ts_values.append(t)
    ts_first = min(ts_values) if ts_values else None
    ts_last = max(ts_values) if ts_values else None
    duration_sec = (ts_last - ts_first) if (ts_first is not None and ts_last is not None) else None
    if duration_sec is not None and duration_sec < 0:
        duration_sec = 0.0

    # paths
    safety_seq = []
    control_seq = []
    complexities = []
    vc_values = []
    frame_quality_bad = 0
    for rec in records:
        dec = rec.get("decision") or {}
        obs = rec.get("obs") or {}

        if "safety_level" in dec and dec.get("safety_level") is not None:
            safety_seq.append(dec.get("safety_level"))
        if "control_mode" in dec and dec.get("control_mode") is not None:
            control_seq.append(dec.get("control_mode"))

        c = _as_float(dec.get("complexity_score"))
        if c is not None:
            complexities.append(c)

        vc = _as_float(obs.get("vc"))
        if vc is not None:
            vc_values.append(vc)

        fq = obs.get("frame_quality")
        if fq is not None and str(fq).upper() != "GOOD":
            frame_quality_bad += 1

    safety_level_path = _unique_order(safety_seq)
    control_mode_path = _unique_order(control_seq)

    complexity_max = max(complexities) if complexities else None
    complexity_avg = (sum(complexities) / len(complexities)) if complexities else None
    vc_min = min(vc_values) if vc_values else None

    return {
        "version_tag": version_tag,
        "session_id": session_id,
        "episode_id": episode_id,
        "trigger_type": trigger_type,
        "trigger_seq": trigger_seq,
        "record_count": record_count,
        "ts_first": ts_first,
        "ts_last": ts_last,
        "duration_sec": duration_sec,
        "safety_level_path": safety_level_path,
        "control_mode_path": control_mode_path,
        "complexity_max": complexity_max,
        "complexity_avg": complexity_avg,
        "vc_min": vc_min,
        "frame_quality_bad_count": frame_quality_bad,
        "parse_errors": int(parse_errors or 0),
    }

