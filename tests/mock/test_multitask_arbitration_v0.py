# -*- coding: utf-8 -*-
"""
Test 4 · 多任务并行仲裁 v0（Mock 脚本）

覆盖并验证：
- G：多任务并行仲裁（只选一个）
- I：跨 tick 公平性（长期不饿死）
- J：失败诊断是否完整（本 mock 不测，需 trace）
- O：trace 自洽（本 mock 不测，需 trace）

不测：视觉、PAL 计算、VC —— 全部 mock。
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

# 确保项目根在 path 中
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from intervention.arbitrator_v0 import (
    ArbitratorV0,
    CandidateTask,
    NAVIGATION,
    ENV_AWARENESS,
    TASK_STATE,
    SAFETY,
)


def _make_candidate(
    task_id: str,
    task_type: str,
    engagement_level: str,
    pal: float,
    complexity: float,
    last_spoken_ts: float,
) -> CandidateTask:
    """构造 CandidateTask（mock 用）"""
    urgency_map = {
        NAVIGATION: 0.8,
        ENV_AWARENESS: 0.6,
        TASK_STATE: 0.4,
        SAFETY: 1.0,
    }
    return CandidateTask(
        task_id=task_id,
        task_type=task_type,
        engagement_level=engagement_level,
        pal=pal,
        complexity=complexity,
        urgency=urgency_map.get(task_type, 0.4),
        last_spoken_ts=last_spoken_ts,
        decision={},
    )


def run_multitask_mock(duration: int = 60, tick_s: float = 1.0):
    """
    模拟 60 秒 ENGAGED 段，每秒注入多个候选任务。
    每 20 秒插入一次 SAFETY。
    """
    arbitrator = ArbitratorV0()

    now = 0.0
    last_spoken: dict[str, float] = {}  # task_id -> ts

    winner_log: list[str] = []
    deferred_log: list[list[str]] = []
    fairness_log: dict[str, list[int]] = defaultdict(list)

    for t in range(duration):
        now += tick_s

        # 固定候选：NAV / ENV / TASK
        candidates = [
            _make_candidate(
                "nav_1", NAVIGATION, "L2", 0.4, 0.6,
                last_spoken.get("nav_1", -999.0),
            ),
            _make_candidate(
                "env_1", ENV_AWARENESS, "L2", 0.4, 0.6,
                last_spoken.get("env_1", -999.0),
            ),
            _make_candidate(
                "task_1", TASK_STATE, "L2", 0.4, 0.6,
                last_spoken.get("task_1", -999.0),
            ),
        ]

        # 每 20 秒插入 SAFETY
        if t % 20 == 0:
            candidates.append(
                _make_candidate(
                    "safety_1", SAFETY, "L2", 0.4, 0.6,
                    last_spoken.get("safety_1", -999.0),
                )
            )

        winner, deferred, scores, fairness = arbitrator.pick(
            candidates,
            now=now,
            control_mode="ASSISTED",
        )

        if winner:
            last_spoken[winner.task_id] = now
            winner_log.append(winner.task_type)
        else:
            winner_log.append("NONE")

        deferred_log.append([d.task_type for d in deferred])

        for d in deferred:
            fairness_log[d.task_type].append(1)

    return winner_log, deferred_log, fairness_log


# -------- 通过 / 不通过判定 --------

def assert_safety_always_wins(winner_log: list[str], safety_ticks: list[int]) -> None:
    """SAFETY 出现时必然赢"""
    for i in safety_ticks:
        assert winner_log[i] == SAFETY, f"tick {i}: SAFETY 出现但 winner={winner_log[i]}"


def assert_single_winner_per_tick(winner_log: list[str]) -> None:
    """每 tick 只有一个 winner（NONE 或单一类型）"""
    for i, w in enumerate(winner_log):
        assert w in ("NONE", NAVIGATION, ENV_AWARENESS, TASK_STATE, SAFETY), (
            f"tick {i}: 非法 winner={w}"
        )


def assert_task_wins_at_least_once(winner_log: list[str]) -> None:
    """TASK 在 60s 内至少赢 1 次（Fairness 生效）"""
    assert TASK_STATE in winner_log, "TASK 60s 内一次都没赢 → 不通过"


def assert_not_mono_winner(winner_log: list[str]) -> None:
    """winner 不全为同一类型"""
    cnt = Counter(winner_log)
    non_none = {k: v for k, v in cnt.items() if k != "NONE"}
    assert len(non_none) >= 2, f"winner 全是同一类型: {cnt}"


# -------- pytest --------

def test_multitask_arbitration_safety_wins():
    """SAFETY 出现必胜"""
    winners, _, _ = run_multitask_mock(duration=60)
    safety_ticks = [0, 20, 40]  # t % 20 == 0
    assert_safety_always_wins(winners, safety_ticks)


def test_multitask_arbitration_single_winner():
    """每 tick 只有一个 winner"""
    winners, _, _ = run_multitask_mock(duration=60)
    assert_single_winner_per_tick(winners)


def test_multitask_arbitration_task_fairness():
    """TASK 至少赢 1 次（Fairness 生效）"""
    winners, _, _ = run_multitask_mock(duration=60)
    assert_task_wins_at_least_once(winners)


def test_multitask_arbitration_not_mono():
    """winner 不全为同一类型"""
    winners, _, _ = run_multitask_mock(duration=60)
    assert_not_mono_winner(winners)


def test_multitask_arbitration_full_run():
    """全量运行 + 人工可读输出"""
    winners, deferred, fairness = run_multitask_mock(duration=60)

    # 硬标准断言
    assert_safety_always_wins(winners, [0, 20, 40])
    assert_single_winner_per_tick(winners)
    assert_task_wins_at_least_once(winners)
    assert_not_mono_winner(winners)

    # 可读输出（pytest -s 可见）
    print("\n=== Winner distribution ===")
    print(Counter(winners))
    print("\n=== Fairness (deferred counts) ===")
    for k, v in fairness.items():
        print(f"  {k}: {sum(v)}")


# -------- 直接运行 --------

if __name__ == "__main__":
    winners, deferred, fairness = run_multitask_mock()

    print("=== Winner distribution ===")
    print(Counter(winners))

    print("\n=== Fairness (deferred counts) ===")
    for k, v in fairness.items():
        print(f"  {k}: {sum(v)}")

    # 硬标准检查
    print("\n=== 通过/不通过 ===")
    try:
        assert_safety_always_wins(winners, [0, 20, 40])
        print("  ✓ SAFETY 出现必胜")
    except AssertionError as e:
        print(f"  ✗ {e}")

    try:
        assert_task_wins_at_least_once(winners)
        print("  ✓ TASK 至少赢 1 次")
    except AssertionError as e:
        print(f"  ✗ {e}")

    try:
        assert_not_mono_winner(winners)
        print("  ✓ winner 不全为同一类型")
    except AssertionError as e:
        print(f"  ✗ {e}")
