# tools/stress_v2/trace_reader.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional

@dataclass
class TraceFrame:
    seq: int
    ts_ms: Optional[int]
    weighted_sum: float
    complexity_raw: float
    motion_instability: float
    path_instability: float
    branch_load: float


def _get(d: Dict[str, Any], path: str, default=None):
    cur: Any = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def _norm_record(r: Dict[str, Any]) -> Dict[str, Any]:
    """
    兼容两类结构：
    A) {"view": {...}, "a3": {...}}
    B) {"obs": {...}, "decision": {...}}  (当前 trace：ts/seq/obs/decision，decision 含 debug)
    只关心风险相关字段。
    """
    if "view" in r or "a3" in r:
        view = r.get("view") or {}
        a3 = r.get("a3") or {}
        return {"view": view, "a3": a3, "raw": r}

    obs = r.get("obs") or {}
    decision = r.get("decision") or {}
    # 把 obs/decision 映射成 view/a3 的概念空间
    view = {
        "complexity_raw": obs.get("complexity_raw", obs.get("complexity", 0.0)) or 0.0,
        "motion_instability": obs.get("motion_instability", obs.get("motion", 0.0)) or 0.0,
        "path_instability": obs.get("path_instability", obs.get("path", 0.0)) or 0.0,
        "branch_load": obs.get("branch_load", obs.get("branch", 0.0)) or 0.0,
    }
    # weighted_sum：优先 decision.debug.weighted_sum_before_clamp（当前 a3_logger 写入），再 decision.risk.weighted_sum，再 obs
    ws = _get(decision, "risk.weighted_sum", None)
    if ws is None and isinstance(decision.get("debug"), dict):
        ws = decision["debug"].get("weighted_sum_before_clamp")
    if ws is None:
        ws = obs.get("weighted_sum", obs.get("risk_weighted_sum", 0.0)) or 0.0
    a3 = {"risk": {"weighted_sum": ws}, "debug": decision.get("debug") or {}}
    return {"view": view, "a3": a3, "raw": r}


def iter_trace_frames(trace_jsonl_path: str) -> Iterator[TraceFrame]:
    with open(trace_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            nr = _norm_record(r)

            seq = nr["raw"].get("seq")
            if seq is None:
                seq = nr["raw"].get("frame_seq")
            if seq is None:
                continue
            seq = int(seq)

            ts_ms = nr["raw"].get("ts_ms")
            if ts_ms is None:
                ts = nr["raw"].get("ts", nr["raw"].get("timestamp"))
                if isinstance(ts, (int, float)):
                    ts_ms = int(ts * 1000) if ts < 1e11 else int(ts)

            weighted_sum = float(_get(nr, "a3.risk.weighted_sum", 0.0) or 0.0)
            view = nr["view"]
            yield TraceFrame(
                seq=seq,
                ts_ms=ts_ms,
                weighted_sum=weighted_sum,
                complexity_raw=float(view.get("complexity_raw", 0.0) or 0.0),
                motion_instability=float(view.get("motion_instability", 0.0) or 0.0),
                path_instability=float(view.get("path_instability", 0.0) or 0.0),
                branch_load=float(view.get("branch_load", 0.0) or 0.0),
            )
