# -*- coding: utf-8 -*-
"""
Smoke: Advisory Observation Integration M0

- 构帧成功
- advisory_review_observation 可读
- JSONL 可写
- reasoning_console_aggregator 可聚合（Console/Viewer 可见的前置）

不跑长 trace。
"""

from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.logger import DecisionMonitorLogger  # noqa: E402
from tools.reasoning_console_aggregator import aggregate_frame  # noqa: E402


def _load_ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    out = ROOT / "logs" / "smoke_advisory_observation_integration.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    ctx = _load_ctx("R89_advisory_candidate_resume_fragility_global_stall_real_ctx.json")
    frame = DecisionMonitorBuilder().build(ctx)

    # JSONL 落地
    DecisionMonitorLogger(jsonl_path=str(out), emit_console_summary=False).write(frame)

    snap = aggregate_frame(frame.to_dict())
    assert snap.advisory_soft_fail_candidate_observed in (True, False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

