#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Replay runner skeleton (v1.4.9 P0-2-A).

P0-2-A 目标：定义并实现 Replay 输入结构，使 Replay 路径不依赖实时输入。

本 runner 的职责：
- 读取 ReplayInput JSON
- 设置 deterministic seed
- 安装逻辑时钟（禁止 wall clock time）
- 逐 step 提供 vision/map/intent 的 SSOT 输入

注意：
- 本文件不修改任何业务逻辑
- 业务系统的“确定性一致性”在 P0-2-B 才会进一步收敛

Run:
    python3 luna_badge_v1_2/replay/replay_runner.py luna_badge_v1_2/replay/examples/case_nav_turn_001.json
"""

from __future__ import annotations

import json
import random
import os
import sys
from typing import Any, Dict

# 支持两种运行方式：
# 1) python3 -m luna_badge_v1_2.replay.replay_runner <file>
# 2) python3 luna_badge_v1_2/replay/replay_runner.py <file>
#
# 直接运行脚本时，相对导入会失败，因此这里做最小兼容处理（不影响业务逻辑）。
if __package__ is None or __package__ == "":
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from luna_badge_v1_2.replay.replay_models import ReplayInput  # type: ignore
    from luna_badge_v1_2.replay.replay_clock import ReplayClock, patch_time  # type: ignore
else:
    from .replay_models import ReplayInput
    from .replay_clock import ReplayClock, patch_time


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 replay_runner.py <replay_input.json>")
        return 2

    data = load_json(sys.argv[1])
    replay = ReplayInput.from_dict(data)
    errors = replay.validate()
    if errors:
        print("[REPLAY][INVALID INPUT]")
        for e in errors:
            print(" -", e)
        return 1

    random.seed(replay.seed)

    clock = ReplayClock(
        t0_ms=replay.time.t0,
        delta_ms=replay.time.delta_ms,
        steps=replay.time.steps,
    )

    print(f"[REPLAY] replay_id={replay.replay_id} seed={replay.seed}")
    print(f"[REPLAY] steps={replay.time.steps} delta_ms={replay.time.delta_ms}")
    print("[REPLAY] realtime dependencies blocked: time.time/time.sleep/monotonic")

    with patch_time(clock):
        for step in range(replay.time.steps):
            clock.step = step
            t_ms = replay.time_ms_at_step(step)
            vf = replay.vision_at_step(step)
            ms = replay.map_at_step(step)
            intents = replay.intents_at_step(step)

            # P0-2-A: only surface the SSOT inputs; do not call devices or online services.
            if intents or step == 0 or step == replay.time.steps - 1:
                print(f"\n[STEP {step:04d}] t_ms={t_ms} vision_state={vf.vision_state}")
                if ms is not None:
                    print(f"  map.route_state={ms.route_state} distance_to_turn={ms.distance_to_turn}")
                if intents:
                    for it in intents:
                        print(f"  intent={it.intent} payload={it.payload}")

    print("\n[REPLAY] P0-2-A input spec validated and replay timeline enumerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
