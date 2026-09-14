#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线统一回归执行器（V1）

目标：把分散的 test 脚本收成“一条命令可跑”的固定入口。
约束（V1）：
- 串行执行（不并行）
- 不做复杂依赖图/跳过逻辑
- 不改变任何 test 脚本语义

输出：
- logs/run_mainline_regression_v1_<UTC>.json
- logs/run_mainline_regression_v1_<UTC>.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


# 以“当前工作目录”为仓库根（避免 __file__.resolve() 因工作区映射/软链导致跑到别的目录）
ROOT = Path.cwd().resolve()
LOGS_DIR = ROOT / "logs"


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _truncate(s: str, limit: int = 4000) -> str:
    s = s or ""
    if len(s) <= limit:
        return s
    return s[: limit - 40] + "\n...<truncated>...\n" + s[-20:]


def _run_cmd(cmd: Sequence[str], cwd: Path, env: Dict[str, str], timeout_s: Optional[int]) -> Tuple[int, float, str, str]:
    t0 = time.time()
    p = subprocess.run(
        list(cmd),
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout_s,
    )
    dur = time.time() - t0
    return p.returncode, dur, p.stdout or "", p.stderr or ""


@dataclass
class ScriptResult:
    group: str
    name: str
    command: List[str]
    cwd: str
    return_code: int
    duration_s: float
    stdout_excerpt: str
    stderr_excerpt: str


def _discover_risk_trace_inputs(root: Path) -> List[Path]:
    """
    V1.1：优先使用 risk 相关回归脚本写入的固定 trace 文件名。
    若文件不存在则跳过该输入。
    """
    candidates = [
        root / "logs" / "risk_interrupt_level2_pilot_v1_test.jsonl",
        root / "logs" / "risk_interrupt_cancel_replace_v1_test.jsonl",
        root / "logs" / "risk_interrupt_state_transition_v1_test.jsonl",
    ]
    return [p for p in candidates if p.exists()]


def _default_plan() -> List[Tuple[str, str]]:
    """
    返回 (group, script_path) 的固定执行顺序。
    """
    return [
        # smoke / output chain basics
        ("smoke", "tools/test_real_output_submit_v1.py"),
        ("smoke", "tools/test_request_runtime_source_v1.py"),
        ("smoke", "tools/test_playback_runtime_source_v1.py"),
        # output_chain (execution layer)
        ("output_chain", "tools/test_real_playback_execution_v1.py"),
        ("output_chain", "tools/test_interrupt_cancel_v1.py"),
        # cross-domain orchestrator
        ("cross_domain", "tools/test_cross_domain_orchestrator_v1.py"),
        # risk pilot
        ("risk_pilot", "tools/test_risk_interrupt_v1_level2_pilot.py"),
        ("risk_pilot", "tools/test_risk_interrupt_v1_cancel_replace_v1.py"),
        ("risk_pilot", "tools/test_risk_interrupt_v1_pilot_state_transition.py"),
    ]


def _render_md(stamp: str, results: List[ScriptResult]) -> str:
    total = len(results)
    failed = [r for r in results if r.return_code != 0]
    ok = total - len(failed)

    lines: List[str] = []
    lines.append("# 主线统一回归执行器（V1）运行报告")
    lines.append("")
    lines.append(f"- generated_at_utc: `{stamp}`")
    lines.append(f"- total: `{total}`  ok: `{ok}`  failed: `{len(failed)}`")
    lines.append("")

    by_group: Dict[str, List[ScriptResult]] = {}
    for r in results:
        by_group.setdefault(r.group, []).append(r)

    for g in ("smoke", "output_chain", "cross_domain", "risk_pilot", "risk_analysis"):
        arr = by_group.get(g, [])
        if not arr:
            continue
        lines.append(f"## {g}")
        lines.append("")
        for r in arr:
            status = "OK" if r.return_code == 0 else f"FAIL({r.return_code})"
            lines.append(f"- **{r.name}**: `{status}`  duration=`{r.duration_s:.3f}s`")
            lines.append(f"  - command: `{ ' '.join(r.command) }`")
            if r.stdout_excerpt.strip():
                lines.append("  - stdout_excerpt:")
                lines.append("")
                lines.append("```")
                lines.append(_truncate(r.stdout_excerpt, 1200))
                lines.append("```")
            if r.stderr_excerpt.strip():
                lines.append("  - stderr_excerpt:")
                lines.append("")
                lines.append("```")
                lines.append(_truncate(r.stderr_excerpt, 1200))
                lines.append("```")
        lines.append("")

    if failed:
        lines.append("## 失败汇总（按出现顺序）")
        lines.append("")
        for r in failed:
            lines.append(f"- **{r.group}/{r.name}**: return_code=`{r.return_code}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout_s", type=int, default=120, help="per-script timeout seconds (default 120)")
    ap.add_argument("--analyzer_timeout_s", type=int, default=60, help="risk analyzer timeout seconds (default 60)")
    ap.add_argument("--stop_on_fail", action="store_true", help="stop immediately when a script fails")
    ap.add_argument("--out_dir", default=str(LOGS_DIR), help="output directory (default: logs)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_stamp()

    # 保持与直接运行 tools/test_*.py 一致的 import 行为
    env = dict(os.environ)
    env.setdefault("PYTHONPATH", str(ROOT))

    results: List[ScriptResult] = []
    plan = _default_plan()
    for group, script in plan:
        script_path = ROOT / script
        cmd = [sys.executable, str(script_path)]
        name = script_path.name

        try:
            rc, dur, out, err = _run_cmd(cmd, cwd=ROOT, env=env, timeout_s=args.timeout_s)
        except subprocess.TimeoutExpired as e:
            rc = 124
            dur = float(args.timeout_s)
            out = (e.stdout or "") if isinstance(e.stdout, str) else ""
            err = (e.stderr or "") if isinstance(e.stderr, str) else ""
            err = (err + "\n" if err else "") + f"TIMEOUT after {args.timeout_s}s"

        results.append(
            ScriptResult(
                group=group,
                name=name,
                command=cmd,
                cwd=str(ROOT),
                return_code=int(rc),
                duration_s=float(dur),
                stdout_excerpt=_truncate(out, 4000),
                stderr_excerpt=_truncate(err, 4000),
            )
        )

        if args.stop_on_fail and rc != 0:
            break

    # V1.1：risk_pilot 跑完后追加 analyzer（不改变 analyzer 行为）
    risk_inputs = _discover_risk_trace_inputs(ROOT)
    if risk_inputs:
        analyzer_path = ROOT / "tools" / "analyze_risk_interrupt_v1_pilot.py"
        cmd = [sys.executable, str(analyzer_path)]
        for p in risk_inputs:
            cmd += ["--input", str(p)]
        try:
            rc, dur, out, err = _run_cmd(cmd, cwd=ROOT, env=env, timeout_s=args.analyzer_timeout_s)
        except subprocess.TimeoutExpired as e:
            rc = 124
            dur = float(args.analyzer_timeout_s)
            out = (e.stdout or "") if isinstance(e.stdout, str) else ""
            err = (e.stderr or "") if isinstance(e.stderr, str) else ""
            err = (err + "\n" if err else "") + f"TIMEOUT after {args.analyzer_timeout_s}s"

        results.append(
            ScriptResult(
                group="risk_analysis",
                name=analyzer_path.name,
                command=cmd,
                cwd=str(ROOT),
                return_code=int(rc),
                duration_s=float(dur),
                stdout_excerpt=_truncate(out, 4000),
                stderr_excerpt=_truncate(err, 4000),
            )
        )
    else:
        results.append(
            ScriptResult(
                group="risk_analysis",
                name="analyze_risk_interrupt_v1_pilot.py",
                command=[sys.executable, str(ROOT / "tools" / "analyze_risk_interrupt_v1_pilot.py"), "--input", "<no_risk_trace_found>"],
                cwd=str(ROOT),
                return_code=0,
                duration_s=0.0,
                stdout_excerpt="SKIPPED: no risk trace inputs found (expected one of logs/risk_interrupt_*_test.jsonl).",
                stderr_excerpt="",
            )
        )

    out_json = out_dir / f"run_mainline_regression_v1_{stamp}.json"
    out_md = out_dir / f"run_mainline_regression_v1_{stamp}.md"

    payload = {
        "version": "v1",
        "generated_at_utc": stamp,
        "results": [asdict(r) for r in results],
        "summary": {
            "total": len(results),
            "failed": sum(1 for r in results if r.return_code != 0),
        },
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(_render_md(stamp, results), encoding="utf-8")

    print(str(out_md))
    # 以“是否有失败”作为执行器自身退出码
    sys.exit(0 if payload["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    main()

