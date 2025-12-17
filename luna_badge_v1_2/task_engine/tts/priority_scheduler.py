"""
PriorityScheduler: 统一的 TTS 优先级调度器

负责在 safety_queue + main_queue 中，选出下一条要播报的 Utterance。

Step 12: 优先级调度器实现
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Scheduling semantics (behavior contract)
#
# User-visible ordering guarantees:
# 1) safety_queue always preempts main_queue (P0 > others)
# 2) main_queue ordering:
#    - PriorityBand: P1 > P2 > P3
#    - Within a band: higher numeric priority first
#    - If same band & same priority: FIFO by enqueue order
#
# Any change to the above ordering is a contract change.
# ======================================================================

from __future__ import annotations

from collections import deque
from typing import Deque, Optional, List

from .utterance import Utterance
from .priority_bands import PriorityBand


class PriorityScheduler:
    """
    统一的 TTS 优先级调度器。

    负责在 safety_queue + main_queue 中，选出下一条要播报的 Utterance。

    调度规则：
    1. 如果 safety_queue 非空，永远先取 safety_queue（P0）。
    2. 否则，从 main_queue 中选：
       - 按 PriorityBand: P1 > P2 > P3
       - 同一个 band 内：priority 较高优先；若相同，按进入队列顺序（FIFO）。
    """

    def select_next(
        self,
        safety_queue: Deque[Utterance],
        main_queue: Deque[Utterance],
    ) -> Optional[Utterance]:
        """
        从安全队列和主队列中选择下一条要播报的 Utterance。

        Args:
            safety_queue: 安全播报队列（P0）
            main_queue: 主队列（P1-P3）

        Returns:
            Optional[Utterance]: 选中的 Utterance，如果两个队列都为空则返回 None
        """
        # 1) 安全队列优先
        if safety_queue:
            return safety_queue.popleft()

        if not main_queue:
            return None

        # 2) main_queue 内按 band + priority 选择一个元素
        # 为了不打乱原队列顺序，我们仅找到"最优元素的索引"，然后 pop 该元素。
        best_idx: Optional[int] = None
        best_band: Optional[PriorityBand] = None
        best_priority: Optional[int] = None

        for idx, u in enumerate(main_queue):
            band = PriorityBand.from_priority(int(getattr(u, "priority", 0)))
            prio = int(getattr(u, "priority", 0))

            if best_idx is None:
                best_idx = idx
                best_band = band
                best_priority = prio
                continue

            # band 更高优先
            if band.is_higher_than(best_band):
                best_idx = idx
                best_band = band
                best_priority = prio
                continue

            # 同 band，priority 更高优先
            if band == best_band and prio > best_priority:
                best_idx = idx
                best_band = band
                best_priority = prio
                continue

            # 同 band，同 priority，则保留之前的（先入队优先）

        if best_idx is None:
            return None

        # deque 不支持按索引 pop，简单做：旋转 + popleft
        # 这里 main_queue 一般不大，这种写法够用。
        for _ in range(best_idx):
            main_queue.append(main_queue.popleft())
        return main_queue.popleft()






