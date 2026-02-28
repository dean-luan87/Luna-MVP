#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单线程、冻结输入的 deterministic replay 模式（算法闭环验证）。

- 输入：trace 中的 quantized obs（整数）
- 输出：decision + advice_rhythm（只写 decision_trace.jsonl）
- 不启动视觉、multimodal、后台线程；不写原始 trace。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# 必须在 import a3 之前设置，保证定点路径
os.environ["A3_FIXEDPOINT"] = "1"

from a3.config import A3Config
from a3.engine import A3Engine
from a3.types import A3Signals
from intervention.advice_rhythm_v0 import AdviceRhythmV0
from runtime.a3_fixedpoint import SCORE_SCALE, dq, q


def _obs_quantized_to_signals(obs_q: dict, obs_float: dict) -> A3Signals:
    """从 trace 的 obs_quantized（及 obs 中的 frame_quality）构建 A3Signals。"""
    def get_q(key: str, default: int = 0) -> int:
        v = obs_q.get(key, default)
        return int(v) if v is not None else default

    complexity_q = get_q("complexity_q")
    path_q = get_q("path_q")
    motion_q = get_q("motion_q")
    branch_q = get_q("branch_q")
    roi = min(max(get_q("roi"), 0), 24)
    vc_q = get_q("vc_q", SCORE_SCALE)

    risk_density = dq(complexity_q)
    path_stability = 1.0 - dq(path_q)
    path_stability = max(0.0, min(1.0, path_stability))
    motion_instability = dq(motion_q)
    branch_count = min(max(int(branch_q), 0), 32)
    branch_load_val = dq(branch_q)
    branch_load = branch_load_val if 0 <= branch_load_val <= 1.0 else None
    view_confidence = dq(vc_q)
    view_confidence = max(0.0, min(1.0, view_confidence))
    frame_quality = str(obs_float.get("frame_quality", "GOOD") or "GOOD")

    return A3Signals(
        risk_density=risk_density,
        redline_hit=False,
        path_stability=path_stability,
        path_instability=1.0 - path_stability,
        branch_count=branch_count,
        branch_load=branch_load,
        roi_count=roi,
        occlusion_ratio=0.0,
        recent_speak_rate=0.0,
        rejected_rate=0.0,
        has_goal=True,
        view_confidence=view_confidence,
        frame_quality=frame_quality,
        motion_instability=motion_instability,
    )


def _serialize_mode(mode) -> dict:
    """与 runtime.a3_logger._serialize_mode 一致，仅用于 replay 输出。"""
    if mode is None:
        return {}
    out = {
        "complexity_score": round(getattr(mode, "complexity_score", 0), 3),
        "safety_level": getattr(getattr(mode, "safety_level", None), "value", None),
        "control_mode": getattr(getattr(mode, "control_mode", None), "value", None),
        "advice_budget_scale": round(getattr(mode, "advice_budget_scale", 0), 2),
        "pal_lookahead_m": round(getattr(mode, "pal_lookahead_m", 0), 1),
    }
    debug = getattr(mode, "debug", None) or {}
    out["debug"] = {
        k: (v if isinstance(v, (int, bool)) else round(v, 3))
        for k, v in debug.items()
    }
    return out


def _is_observation_row(row: dict) -> bool:
    """是否为 v1 观测行（含 obs + decision + ts）。"""
    if row.get("type") == "a3_input" and "obs_quantized" in row:
        return True
    if row.get("trace_schema_version") and "obs" in row and "decision" in row and "ts" in row:
        return True
    return False


def _get_obs_quantized(row: dict) -> dict:
    """从行中取量化 obs；若无则从 obs 现场 q() 得到。"""
    if "obs_quantized" in row:
        return row["obs_quantized"]
    obs = row.get("obs") or {}
    return {
        "motion_q": q(float(obs.get("motion", 0) or 0)),
        "path_q": q(float(obs.get("path", 0) or 0)),
        "branch_q": q(float(obs.get("branch", 0) or 0)),
        "roi": int(obs.get("roi", 0) or 0),
        "pal_q": q(float(obs.get("pal", 0) or 0)),
        "complexity_q": q(float(obs.get("complexity", 0) or 0)),
        "vc_q": q(float(obs.get("vc", 1.0) or 1.0)),
    }


def _get_ts(row: dict) -> float:
    return float(row["ts"])


def replay(input_trace_path: str, output_path: str) -> None:
    engine = A3Engine(A3Config(enabled=True))
    rhythm = AdviceRhythmV0()

    with open(input_trace_path, "r", encoding="utf-8") as f:
        lines = [json.loads(x) for x in f if x.strip()]

    with open(output_path, "w", encoding="utf-8") as out:
        for row in lines:
            if not _is_observation_row(row):
                continue

            obs_q = _get_obs_quantized(row)
            obs_float = row.get("obs") or {}
            signals = _obs_quantized_to_signals(obs_q, obs_float)

            ts = _get_ts(row)
            now_ms = int(ts * 1000)
            decision = engine.tick(signals, now_ms=now_ms)

            allowed, reason, _advice_type, _trace = rhythm.check(
                advice_category="ENV_AWARENESS",
                is_safety=False,
                now=ts,
            )

            out.write(
                json.dumps(
                    {
                        "ts": ts,
                        "decision": _serialize_mode(decision),
                        "allowed": allowed,
                        "reason": reason,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 tools/replay_freeze_a3.py <input_trace.jsonl> <output_freeze.jsonl>", file=sys.stderr)
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    replay(input_path, output_path)


if __name__ == "__main__":
    main()
