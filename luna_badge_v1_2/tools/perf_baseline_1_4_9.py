#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""P0-4: Performance & stability baseline collector (v1.4.9).

目标：
- 只做采集与记录，不做优化、不改业务逻辑
- 输出 perf_baseline_1_4_9.md（可审计，可一键复现）

说明：
- 建议在空闲机器上运行，避免背景负载污染 P95
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from typing import Any, Dict, List, Optional


PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../luna_badge_v1_2
WORKSPACE_ROOT = os.path.dirname(PKG_ROOT)


def _git_commit() -> str:
    try:
        import subprocess

        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKSPACE_ROOT)
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"


def _percentile(values: List[int], p: float) -> int:
    if not values:
        return 0
    xs = sorted(values)
    if p <= 0:
        return xs[0]
    if p >= 100:
        return xs[-1]
    k = (len(xs) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    if f == c:
        return xs[f]
    d0 = xs[f] * (c - k)
    d1 = xs[c] * (k - f)
    return int(round(d0 + d1))


def _ru_maxrss_bytes() -> Optional[int]:
    # ru_maxrss 在 macOS 为 bytes；在 Linux 常见为 KB
    try:
        import resource

        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if platform.system().lower() == "darwin":
            return int(r)
        return int(r) * 1024
    except Exception:
        return None


def main() -> int:
    case_path = os.path.join(PKG_ROOT, "replay", "examples", "case_nav_turn_001.json")
    out_md = os.path.join(PKG_ROOT, "perf_baseline_1_4_9.md")

    runs = int(os.environ.get("PERF_RUNS", "200"))

    # 以 replay_runner/build_event_stream 作为基线采集入口
    sys.path.insert(0, WORKSPACE_ROOT)
    sys.path.insert(0, PKG_ROOT)
    from replay.replay_models import ReplayInput
    from replay.replay_clock import ReplayClock, patch_time
    from replay.replay_runner import build_event_stream  # type: ignore

    with open(case_path, "r", encoding="utf-8") as f:
        replay = ReplayInput.from_dict(json.load(f))
    errs = replay.validate()
    if errs:
        print("[PERF][INVALID REPLAY INPUT]", errs)
        return 1

    step_wall_us_all: List[int] = []
    tts_enqueue_us_all: List[int] = []
    total_wall_us_runs: List[int] = []

    # 运行多次以获得 P95 稳定估计
    for _ in range(runs):
        clock = ReplayClock(t0_ms=replay.time.t0, delta_ms=replay.time.delta_ms, steps=replay.time.steps)
        perf: Dict[str, Any] = {"step_wall_us": [], "tts_enqueue_wall_us": []}

        t0 = time.perf_counter()
        with patch_time(clock):
            _ = build_event_stream(replay, clock, fault_config_path=None, perf=perf)
        t1 = time.perf_counter()

        total_wall_us_runs.append(int((t1 - t0) * 1_000_000))
        step_wall_us_all.extend([int(x) for x in perf["step_wall_us"]])
        tts_enqueue_us_all.extend([int(x) for x in perf["tts_enqueue_wall_us"]])

    # DecisionPipeline E2E latency：定义为“replay step 的 wall time”（输入→决策/调度→输出事件流）
    step_p50 = _percentile(step_wall_us_all, 50)
    step_p95 = _percentile(step_wall_us_all, 95)
    step_p99 = _percentile(step_wall_us_all, 99)

    # TTS 首帧延迟：定义为“调用 facade.emit → 入队/节流判定完成”的 wall time
    tts_p50 = _percentile(tts_enqueue_us_all, 50)
    tts_p95 = _percentile(tts_enqueue_us_all, 95)
    tts_p99 = _percentile(tts_enqueue_us_all, 99)

    total_us_p50 = _percentile(total_wall_us_runs, 50)
    total_us_p95 = _percentile(total_wall_us_runs, 95)

    rss_peak = _ru_maxrss_bytes()

    os_info = platform.platform()
    py_info = sys.version.replace("\n", " ")
    cpu = platform.processor() or platform.machine() or "unknown"
    mem_bytes: Optional[int] = None
    try:
        import psutil  # type: ignore

        mem_bytes = int(psutil.virtual_memory().total)
    except Exception:
        mem_bytes = None

    # 退化红线（仅定义，不做门禁接入）
    redline_step_p95 = int(step_p95 * 1.2)
    redline_tts_p95 = int(tts_p95 * 1.2)

    lines: List[str] = []
    lines.append("# perf_baseline_1_4_9.md")
    lines.append("")
    lines.append("## Test environment")
    lines.append(f"- **git_commit**: `{_git_commit()}`")
    lines.append(f"- **os**: `{os_info}`")
    lines.append(f"- **python**: `{py_info}`")
    lines.append(f"- **cpu**: `{cpu}`")
    if mem_bytes is not None:
        lines.append(f"- **ram_bytes**: `{mem_bytes}`")
    else:
        lines.append(f"- **ram_bytes**: `unknown`")
    if rss_peak is not None:
        lines.append(f"- **peak_rss_bytes (process ru_maxrss)**: `{rss_peak}`")
    lines.append("")
    lines.append("## Method")
    lines.append("- Baseline is collected by repeatedly running replay mode (no optimization).")
    lines.append("- Input case: `luna_badge_v1_2/replay/examples/case_nav_turn_001.json`")
    lines.append(f"- Runs: `{runs}` (set via env `PERF_RUNS`, default=200)")
    lines.append("")
    lines.append("### Metric definitions (auditable)")
    lines.append("- **DecisionPipeline E2E latency (replay-step)**: per-step wall time from step processing start → end (includes decision/scheduler/tts routing event generation).")
    lines.append("- **TTS first-frame latency (queue entry)**: wall time of `facade.emit(...)` call until enqueue/suppress decision completes (no real audio).")
    lines.append("- **RSS peak**: `resource.getrusage(...).ru_maxrss` converted to bytes (Darwin bytes, Linux KB×1024).")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("### DecisionPipeline E2E latency (replay-step, wall µs)")
    lines.append(f"- P50: `{step_p50}`")
    lines.append(f"- P95: `{step_p95}`")
    lines.append(f"- P99: `{step_p99}`")
    lines.append("")
    lines.append("### TTS first-frame latency (enqueue, wall µs)")
    lines.append(f"- P50: `{tts_p50}`")
    lines.append(f"- P95: `{tts_p95}`")
    lines.append(f"- P99: `{tts_p99}`")
    lines.append("")
    lines.append("### Replay run total time (wall ms)")
    lines.append(f"- P50: `{total_us_p50/1000.0:.3f}`")
    lines.append(f"- P95: `{total_us_p95/1000.0:.3f}`")
    lines.append("")
    lines.append("## Degradation redlines (definition only)")
    lines.append("- **Rule**: P95 must not exceed baseline +20%.")
    lines.append(f"- replay-step P95 redline (µs): `{redline_step_p95}`")
    lines.append(f"- tts enqueue P95 redline (µs): `{redline_tts_p95}`")
    lines.append("")
    lines.append("## How to reproduce")
    lines.append("")
    lines.append("### Collect baseline")
    lines.append("```bash")
    lines.append("PERF_RUNS=200 python3 luna_badge_v1_2/tools/perf_baseline_1_4_9.py")
    lines.append("```")
    lines.append("")
    lines.append("### Determinism regression gate (must stay green)")
    lines.append("```bash")
    lines.append("python3 luna_badge_v1_2/tools/replay_gate.py --cases luna_badge_v1_2/replay/examples/case_nav_turn_001.json --runs 5")
    lines.append("```")
    lines.append("")
    lines.append("## 30-minute stability (manual/assisted)")
    lines.append("- Recommended manual procedure (no automation guarantee in CI):")
    lines.append("  - Run the gate loop for >=30 minutes and keep logs as evidence.")
    lines.append("  - Suggested command (shell loop):")
    lines.append("```bash")
    lines.append("end=$((SECONDS+1800)); while [ $SECONDS -lt $end ]; do python3 luna_badge_v1_2/tools/replay_gate.py --cases luna_badge_v1_2/replay/examples/case_nav_turn_001.json --runs 1 || break; done")
    lines.append("```")
    lines.append("")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")

    print("[PERF] wrote", out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






