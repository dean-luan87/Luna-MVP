#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""P0-2-D Replay determinism gate (v1.4.9).

目标：
- 将 P0-2-C 的确定性验证固化为“可一键运行的门禁入口”
- 支持指定 replay case 列表
- 快/慢执行都验证（通过子进程，覆盖“重启进程后 hash 一致”）

说明：
- 本脚本不修改业务逻辑，不改阈值
- Replay 阶段会跳过机器相关随机源（例如 psutil CPU/MEM 探测不纳入口径）

用法示例：
  python3 luna_badge_v1_2/tools/replay_gate.py \\
    --cases luna_badge_v1_2/replay/examples/case_nav_turn_001.json \\
    --runs 5
"""

from __future__ import annotations

import os
import sys
import subprocess
from typing import List


def _parse_args(argv: List[str]) -> dict:
    args = {
        "cases": [],
        "runs": 5,
        "report_dir": "luna_badge_v1_2/replay",
    }
    it = iter(argv)
    for tok in it:
        if tok == "--cases":
            args["cases"].append(str(next(it)))
        elif tok == "--runs":
            args["runs"] = int(next(it))
        elif tok == "--report-dir":
            args["report_dir"] = str(next(it))
        elif tok in ("-h", "--help"):
            args["help"] = True
        else:
            args["help"] = True
            args["error"] = f"Unknown arg: {tok}"
    return args


def _runner_path(repo_root: str) -> str:
    return os.path.join(repo_root, "luna_badge_v1_2", "replay", "replay_runner.py")


def _run_case(runner: str, case_path: str, runs: int, report_path: str) -> int:
    cmd = [
        sys.executable,
        runner,
        case_path,
        "--validate",
        str(runs),
        "--report",
        report_path,
    ]
    return subprocess.call(cmd)


def main() -> int:
    # __file__ = <repo>/luna_badge_v1_2/tools/replay_gate.py
    # repo_root = <repo>
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = _parse_args(sys.argv[1:])
    if args.get("help") or not args.get("cases"):
        if args.get("error"):
            print("[REPLAY_GATE][ERROR]", args["error"])
        print("Usage:")
        print("  python3 luna_badge_v1_2/tools/replay_gate.py --cases <case.json> [--cases <case2.json>] [--runs 5]")
        print("  Optional: --report-dir luna_badge_v1_2/replay")
        return 2

    report_dir = os.path.join(repo_root, args["report_dir"])
    os.makedirs(report_dir, exist_ok=True)
    runner = _runner_path(repo_root)

    cases: List[str] = args["cases"]
    runs: int = int(args["runs"])

    failed: List[str] = []
    for case_path in cases:
        base = os.path.basename(case_path).replace(".json", "")
        report_path = os.path.join(report_dir, f"replay_validation_report__{base}.md")
        code = _run_case(runner, case_path, runs, report_path)
        if code != 0:
            failed.append(case_path)
            print(f"[REPLAY_GATE][FAIL] case={case_path} report={report_path}")
        else:
            print(f"[REPLAY_GATE][PASS] case={case_path} report={report_path}")

    if failed:
        print("\n[REPLAY_GATE] FAILED cases:")
        for c in failed:
            print(" -", c)
        return 1

    print("\n[REPLAY_GATE] ALL PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

