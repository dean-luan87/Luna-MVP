#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Narrative-Trace Support (nt) tightening analysis — M17

只读分析（以“构帧”为准，不以 pack JSON 为准）：
- 读取 `tools/real_scenario_pack.default_real_cases()`（包含 R1..R100）
- 对每个 ctx_json case 用 `DecisionMonitorBuilder().build(ctx)` 构建 frame
- 统计 tightening 前后 nt 分布，并提取“关键证据锚点”特征（timeline high/medium 事件等）

输出 JSON 用于文档对比，避免陷入“感觉更响/更乱”的主观争论。

本脚本不改 benchmark/triage，不修改任何运行逻辑。
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

import sys as _sys

# 允许以 `python3 tools/...py` 直接运行
if str(ROOT) not in _sys.path:
    _sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from tools.real_scenario_pack import default_real_cases  # noqa: E402


def _to_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if obj is not None and hasattr(obj, "to_dict"):
        d = obj.to_dict()
        return d if isinstance(d, dict) else {}
    return {}


def _s(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def _net(frame_d: Dict[str, Any]) -> Dict[str, Any]:
    n = frame_d.get("narrative_evidence_tension_review")
    if n is not None and hasattr(n, "to_dict"):
        n = n.to_dict()
    return n if isinstance(n, dict) else {}


def _extract_frame_features(case_id: str, frame_d: Dict[str, Any]) -> Dict[str, Any]:
    rsr = frame_d.get("run_summary_reference")
    if rsr is not None and hasattr(rsr, "to_dict"):
        rsr = rsr.to_dict()
    rsr = rsr if isinstance(rsr, dict) else {}
    ev = rsr.get("structured_event_layer_snapshot") if isinstance(rsr.get("structured_event_layer_snapshot"), dict) else {}
    event_count = ev.get("event_count") if isinstance(ev.get("event_count"), int) else 0

    # narrative 文本：优先 rsr.mainline_narrative_brief；若无则落到 mna / summary_brief
    nar = _s(rsr.get("mainline_narrative_brief"))
    mna = frame_d.get("mainline_narrative_alignment")
    if not nar and mna is not None:
        mna = mna.to_dict() if hasattr(mna, "to_dict") else mna
        if isinstance(mna, dict) and mna.get("narrative_brief"):
            nar = _s(mna.get("narrative_brief"))
    nar = nar or _s(rsr.get("summary_brief"))
    narr_len = len(nar)

    tv = frame_d.get("reasoning_timeline_view")
    tvd = _to_dict(tv)
    events = tvd.get("events") or []
    if not isinstance(events, list):
        events = []
    hi = [e for e in events if isinstance(e, dict) and e.get("event_importance") in ("high", "medium")]
    hi_types = [e.get("event_type") for e in hi if e.get("event_type")]

    return {
        "case_id": case_id,
        "nt": _net(frame_d).get("narrative_trace_support_tension") or "unknown",
        "nt_reason": (_net(frame_d).get("tension_reason_summaries") or {}).get("narrative_trace_support"),
        "narr_len": narr_len,
        "structured_event_count": event_count,
        "timeline_event_count": len(events),
        "timeline_hi_event_count": len(hi),
        "timeline_hi_type_count": len(set(hi_types)),
        "key_transition_count": tvd.get("key_transition_count"),
        "key_transition_summary": _s(tvd.get("key_transition_summary"))[:220],
    }


def _thin_evidence_score(f: Dict[str, Any]) -> float:
    """
    证据偏薄候选排序：叙事越长、关键事件锚点（hi）越少，得分越高。
    用于人工挑代表 case；不是规则。
    """
    narr = float(f.get("narr_len") or 0)
    hi = float(f.get("timeline_hi_event_count") or 0)
    types = float(f.get("timeline_hi_type_count") or 0)
    # 避免除 0；types 作为弱加权（类型越少越可疑）
    denom = max(1.0, hi + 0.6 * types)
    return narr / denom


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=str,
        default=str(ROOT / "logs" / "real_scenario_pack_m17.json"),
        help="Path to real_scenario_pack_m17.json",
    )
    ap.add_argument(
        "--out",
        type=str,
        default=str(ROOT / "logs" / "narrative_trace_tightening_analysis_m17.json"),
        help="Output analysis JSON",
    )
    ap.add_argument("--label", type=str, required=True, help="Snapshot label: before|after")
    ap.add_argument("--top-k", type=int, default=12)
    args = ap.parse_args()

    # 以 default_real_cases() 为准，确保 tightening 前后对比跑的是同一批 case
    cases_with_ref = default_real_cases()
    builder = DecisionMonitorBuilder()

    feats: List[Dict[str, Any]] = []
    for case, ref in cases_with_ref:
        if not isinstance(ref, dict) or ref.get("input_mode") != "ctx_json":
            continue
        p = ROOT / ref.get("input_ref")
        if not p.is_file():
            continue
        ctx = json.loads(p.read_text(encoding="utf-8"))
        frame = builder.build(ctx)
        frame_d = frame.to_dict() if hasattr(frame, "to_dict") else (frame or {})
        feats.append(_extract_frame_features(case.case_id, frame_d if isinstance(frame_d, dict) else {}))

    nt_dist = Counter([f.get("nt") or "unknown" for f in feats])

    hi_dist = Counter([int(f.get("timeline_hi_event_count") or 0) for f in feats])
    type_dist = Counter([int(f.get("timeline_hi_type_count") or 0) for f in feats])

    scored = []
    for f in feats:
        f2 = dict(f)
        f2["thin_evidence_score"] = round(_thin_evidence_score(f2), 3)
        scored.append(f2)
    scored.sort(key=lambda x: float(x.get("thin_evidence_score") or 0), reverse=True)

    out_path = Path(args.out)
    existing: Dict[str, Any] = {}
    if out_path.is_file():
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        if not isinstance(existing, dict):
            existing = {}

    existing[args.label] = {
        "input": "DecisionMonitorBuilder().build(ctx_json) over default_real_cases()",
        "summary": {
            "total_cases": len(feats),
            "nt_distribution": dict(nt_dist),
            "timeline_hi_event_count_distribution": dict(sorted(hi_dist.items(), key=lambda x: x[0])),
            "timeline_hi_type_count_distribution": dict(sorted(type_dist.items(), key=lambda x: x[0])),
        },
        "top_thin_evidence_candidates": scored[: int(args.top_k)],
    }

    out_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

