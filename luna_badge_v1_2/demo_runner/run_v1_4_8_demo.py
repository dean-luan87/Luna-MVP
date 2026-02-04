#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
v1.4.8 Behavior Contract Demo

Purpose:
- Verify that Luna Badge v1.4.8 strictly follows the Vision-Driven behavior contract.
- This script is NOT a feature demo. It is a behavior proof.

Run:
    python3 demo_runner/run_v1_4_8_demo.py

Expected result:
    [DEMO RESULT] v1.4.8 behavior contract VERIFIED
"""

import os
import sys
import time
import random

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.scheduler.c5_scheduler import C5Scheduler
from expression.scheduler.c5_types import VisionRhythmContext, ExpressionCandidate


# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------

def banner(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def assert_in(value, candidates, msg):
    assert value in candidates, f"{msg}: {value} not in {candidates}"


# ----------------------------------------------------------------------
# Demo Entry
# ----------------------------------------------------------------------

def main():
    random.seed(42)

    banner("PHASE 0 · INIT")

    vision = VisionRhythmContext(
        vision_state="STABLE",
        speed_mps=0.8,
        last_vision_ts=time.time()
    )
    scheduler = C5Scheduler()
    queue = scheduler.queue

    print(f"[INIT] vision_state={vision.vision_state}, speed={vision.speed_mps:.2f} m/s")

    # 用于捕获输出的回调
    emitted_expressions = []
    emitted_delays = []

    def emit_callback(expr: ExpressionCandidate, delay_ms: int):
        """输出回调（用于捕获）"""
        emitted_expressions.append(expr.contract_id)
        emitted_delays.append(delay_ms)
        print(f"    🎤 [TTS] {expr.contract_id} (延迟: {delay_ms}ms)")

    # ------------------------------------------------------------------
    # PHASE 1: STABLE + normal → EMIT (with delay)
    # ------------------------------------------------------------------
    banner("PHASE 1 · STABLE + normal → EMIT")

    expr_1 = ExpressionCandidate(
        contract_id="nav_forward",
        duplicate_key="forward_1",
        urgency="normal",
        is_critical=False
    )

    decision_1 = scheduler.schedule(expr_1, vision, emit_callback)

    assert decision_1 == "EMIT", f"PHASE 1 failed: should EMIT, got {decision_1}"
    assert len(emitted_expressions) == 1, "PHASE 1 failed: should emit once"
    assert_in(emitted_delays[0], {100, 200, 300}, "PHASE 1 delay invalid")

    print(f"[PASS] PHASE 1: {decision_1}, delay={emitted_delays[0]}ms")

    # ------------------------------------------------------------------
    # PHASE 2: STABLE + low → QUEUE + REPLACE
    # ------------------------------------------------------------------
    banner("PHASE 2 · STABLE + low → QUEUE + REPLACE")

    # 清空之前的输出
    emitted_expressions.clear()
    emitted_delays.clear()

    expr_2a = ExpressionCandidate(
        contract_id="nav_hint",
        duplicate_key="hint_1",
        urgency="low",
        is_critical=False
    )

    expr_2b = ExpressionCandidate(
        contract_id="nav_hint",
        duplicate_key="hint_1",  # 相同的 duplicate_key
        urgency="low",
        is_critical=False
    )

    d2a = scheduler.schedule(expr_2a, vision, emit_callback)
    d2b = scheduler.schedule(expr_2b, vision, emit_callback)

    assert d2a == "QUEUE", f"PHASE 2a failed: should QUEUE, got {d2a}"
    assert d2b == "QUEUE", f"PHASE 2b failed: should REPLACE via QUEUE, got {d2b}"
    assert queue.size() <= 1, f"PHASE 2 failed: queue overflow, size={queue.size()}"

    print(f"[PASS] PHASE 2: 2a={d2a}, 2b={d2b}, queue_size={queue.size()}")

    # ------------------------------------------------------------------
    # PHASE 3: TURNING + normal → DROP
    # ------------------------------------------------------------------
    banner("PHASE 3 · TURNING + normal → DROP")

    vision.vision_state = "TURNING"
    vision.last_vision_ts = time.time()

    # 清空之前的输出
    emitted_expressions.clear()
    emitted_delays.clear()

    expr_3 = ExpressionCandidate(
        contract_id="nav_turn",
        duplicate_key="turn_1",
        urgency="normal",
        is_critical=False
    )

    d3 = scheduler.schedule(expr_3, vision, emit_callback)

    assert d3 == "DROP", f"PHASE 3 failed: normal must DROP during TURNING, got {d3}"
    assert len(emitted_expressions) == 0, "PHASE 3 failed: should not emit"

    print(f"[PASS] PHASE 3: {d3}")

    # ------------------------------------------------------------------
    # PHASE 4: TURNING + critical → EMIT (override)
    # ------------------------------------------------------------------
    banner("PHASE 4 · TURNING + critical → EMIT")

    # 清空之前的输出
    emitted_expressions.clear()
    emitted_delays.clear()

    expr_4 = ExpressionCandidate(
        contract_id="nav_turn_critical",
        duplicate_key="turn_critical",
        urgency="high",
        is_critical=True  # 关键表达
    )

    d4 = scheduler.schedule(expr_4, vision, emit_callback)

    assert d4 == "EMIT", f"PHASE 4 failed: critical must EMIT, got {d4}"
    assert len(emitted_expressions) == 1, "PHASE 4 failed: should emit once"
    assert emitted_delays[0] == 0, f"PHASE 4 failed: critical delay must be 0, got {emitted_delays[0]}"

    print(f"[PASS] PHASE 4: {d4}, delay={emitted_delays[0]}ms")

    # ------------------------------------------------------------------
    # PHASE 5: Vision change → queue flush
    # ------------------------------------------------------------------
    banner("PHASE 5 · Vision change → QUEUE FLUSH")

    # 先入队一些内容
    vision.vision_state = "STABLE"
    vision.last_vision_ts = time.time()

    expr_5 = ExpressionCandidate(
        contract_id="nav_queue_test",
        duplicate_key="queue_test",
        urgency="low",
        is_critical=False
    )

    scheduler.schedule(expr_5, vision, emit_callback)
    assert queue.size() == 1, f"PHASE 5 setup failed: queue size should be 1, got {queue.size()}"

    # 改变视觉状态（这会触发 flush）
    vision.vision_state = "TURNING"
    vision.last_vision_ts = time.time()

    # 再次调度（会触发状态变化检测和 flush）
    expr_5b = ExpressionCandidate(
        contract_id="nav_queue_test_2",
        duplicate_key="queue_test_2",
        urgency="normal",
        is_critical=False
    )
    scheduler.schedule(expr_5b, vision, emit_callback)

    assert queue.size() == 0, f"PHASE 5 failed: queue not flushed on vision change, size={queue.size()}"

    print(f"[PASS] PHASE 5: queue flushed, size={queue.size()}")

    # ------------------------------------------------------------------
    # DONE
    # ------------------------------------------------------------------
    banner("DEMO RESULT")
    print("[DEMO RESULT] v1.4.8 behavior contract VERIFIED")
    print("\n✅ All phases passed:")
    print("   - PHASE 1: STABLE + normal → EMIT (with delay)")
    print("   - PHASE 2: STABLE + low → QUEUE + REPLACE")
    print("   - PHASE 3: TURNING + normal → DROP")
    print("   - PHASE 4: TURNING + critical → EMIT (override)")
    print("   - PHASE 5: Vision change → QUEUE FLUSH")


if __name__ == "__main__":
    main()
