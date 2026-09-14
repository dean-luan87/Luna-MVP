#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qwen-plus 长语音任务拆解：Provider 配置 A/B 对照（同一终端、顺序执行）。

A 组（legacy）：不显式 `enable_thinking`、默认 max_output=4096、每次 HTTP 新建连接 — **仅对照/回归/排障，非主链默认**
B 组（optimized）：`enable_thinking=false`、默认 max_output=1024、`requests.Session` keep-alive — **主链默认**（`DEFAULT_QWEN_AB_PROFILE`）

通过环境变量 `LUNA_QWEN_AB_PROFILE` 切换；决策见 `docs/architecture/voice/LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md`。

前置：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...

用法：
  export LUNA_BENCH_ITERS=10
  python3 tools/ab_qwen_provider_long_input_compare.py

仅压测、不跑 smoke：
  python3 tools/ab_qwen_provider_long_input_compare.py --no-smoke
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser(description="qwen provider legacy vs optimized A/B")
    ap.add_argument(
        "--iters",
        default=os.getenv("LUNA_BENCH_ITERS", "10"),
        help="benchmark 轮数（默认 10 或环境变量 LUNA_BENCH_ITERS）",
    )
    ap.add_argument("--no-smoke", action="store_true", help="跳过 smoke，只跑 benchmark")
    args = ap.parse_args()
    iters = str(args.iters)

    key = (os.getenv("DASHSCOPE_API_KEY") or os.getenv("LUNA_DASHSCOPE_API_KEY") or "").strip()
    if not key:
        print("请先设置 DASHSCOPE_API_KEY（或 LUNA_DASHSCOPE_API_KEY）。", file=sys.stderr)
        sys.exit(2)

    # 预检：确认子进程会继承同一 Key（子进程 env 使用 {**os.environ}，勿在其它工具里清空）
    _mask = (key[:4] + "…") if len(key) > 4 else "(过短)"
    print(f"预检: DASHSCOPE_API_KEY 已加载（长度={len(key)}，前缀={_mask}）", file=sys.stderr)

    prov = (os.getenv("LUNA_EXTERNAL_LLM_PROVIDER") or "").strip().lower()
    if prov != "qwen":
        print("建议设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen。", file=sys.stderr)

    bench = ROOT / "tools" / "benchmark_qwen_plus_long_input_p95.py"
    smoke = ROOT / "tools" / "smoke_qwen_long_input_baseline.py"

    groups = [
        ("A 组 legacy（基线：无 thinking 字段 / max_out=4096 / 无 Session）", {"LUNA_QWEN_AB_PROFILE": "legacy"}),
        ("B 组 optimized（当前默认：thinking 关 / max_out=1024 / Session）", {"LUNA_QWEN_AB_PROFILE": "optimized"}),
    ]

    for title, extra in groups:
        env = {**os.environ, **extra}
        env.setdefault("LUNA_EXTERNAL_LLM_PROVIDER", "qwen")
        env["LUNA_SMOKE_QWEN_MODELS"] = "qwen-plus"
        env["LUNA_BENCH_ITERS"] = iters
        env.setdefault("LUNA_BENCH_MODEL", "qwen-plus")
        # 显式传入，避免个别环境下父进程未导出到子进程
        if os.getenv("DASHSCOPE_API_KEY"):
            env["DASHSCOPE_API_KEY"] = os.environ["DASHSCOPE_API_KEY"]
        if os.getenv("LUNA_DASHSCOPE_API_KEY"):
            env["LUNA_DASHSCOPE_API_KEY"] = os.environ["LUNA_DASHSCOPE_API_KEY"]

        print("")
        print("=" * 72)
        print(title)
        print("=" * 72)
        if not args.no_smoke:
            r = subprocess.run([sys.executable, str(smoke)], cwd=str(ROOT), env=env)
            if r.returncode != 0:
                sys.exit(r.returncode)
        r = subprocess.run([sys.executable, str(bench)], cwd=str(ROOT), env=env)
        if r.returncode != 0:
            sys.exit(r.returncode)

    print("")
    print("=" * 72)
    print("A/B 顺序跑完。请人工对比两组：avg_ms、p95_ms、json_rate、val_rate、fallback_rate、mixed_preserve_rate。")
    print("若任一组出现 json_rate=0 且日志含 401：Key 无效或过期，结果作废，请到百炼控制台核对后重跑。")
    print("=" * 72)


if __name__ == "__main__":
    main()
