"""
TtsManager: TTS 抽象门面

统一的 TTS 接口，支持同步和异步模式。
- 生产环境：对接实际 TTS 引擎（本地 / 远端）
- 测试环境：只记录 utterances，便于断言

设计目标：
- 提供简单的 speak() 接口，方便业务层追加播报任务；
- 提供 enqueue()/pop_all() 队列操作，供 RuntimeDriver 消费；
- 在 pop_all() 时按 priority 降序 + created_at 升序排序，
  实现"高优先级插队，但同优先级 FIFO"的行为。
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Queue & safety preemption semantics (contract)
#
# Frozen behaviors:
# - Safety queue exists and preempts main queue (via PriorityScheduler).
# - Safety de-duplication window: 2.0 seconds for identical safety text.
# - Safety utterance priority floor: at least 100 and interrupt=True.
# - RuntimeDriver consumes via pop_next(): one utterance per tick.
#
# Changing any of the above changes what/when the user hears.
# ======================================================================

from __future__ import annotations

import time
from typing import List, Any, Optional
from collections import deque

from .utterance import Utterance
from .priority_scheduler import PriorityScheduler


class TtsManager:
    """
    负责管理待播报的 Utterance 队列。

    设计目标：
    - 提供简单的 speak() 接口，方便业务层追加播报任务；
    - 提供 enqueue()/pop_all() 队列操作，供 RuntimeDriver 消费；
    - 在 pop_all() 时按 priority 降序 + created_at 升序排序，
      实现"高优先级插队，但同优先级 FIFO"的行为。
    """

    def __init__(self) -> None:
        """
        初始化 TTS 管理器。

        内部队列保持插入顺序，优先级排序在 pop_all() 时处理。
        
        Step 11: 添加安全播报队列（Preemptive Safety Queue）
        """
        # 内部队列保持插入顺序，优先级排序在 pop_all() 时处理
        self._queue: List[Utterance] = []
        
        # Step 11: 安全播报队列（最高优先级，可抢占主队列）
        self._safety_queue: deque = deque()
        self._last_safety_utter: Optional[str] = None
        self._last_safety_time: float = 0.0
        
        # Step 12: 优先级调度器
        self._scheduler = PriorityScheduler()

    def speak(
        self,
        text: str,
        level: str = "info",
        channel: str = "tts",
        priority: int = 50,
        interrupt: bool = False,
        **meta: Any,
    ) -> Utterance:
        """
        追加一条播报任务。

        Args:
            text: 文本内容
            level: 消息级别
            channel: 输出通道
            priority: 优先级（数值越大越优先，默认 50）
            interrupt: 是否期望打断当前播报（当前仅存储，不在本版本生效）
            **meta: 其他元数据

        Returns:
            Utterance: 创建的 Utterance 对象
        """
        utter = Utterance(
            text=text,
            level=level,
            channel=channel,
            priority=priority,
            interrupt=interrupt,
            meta=meta or {},
        )
        self.enqueue(utter)
        return utter

    def enqueue(self, utterance: Utterance) -> None:
        """
        将 Utterance 加入主队列。调用端通常使用 speak()，但也可直接 enqueue()。

        Args:
            utterance: Utterance 实例
        """
        if not isinstance(utterance, Utterance):
            # 容错：自动包装
            utterance = Utterance(text=str(utterance))
        self._queue.append(utterance)

    def push_safety(self, utterance: Utterance) -> bool:
        """
        Step 11: 高优先级安全播报，立即抢占主队列。

        Args:
            utterance: Utterance 实例

        Returns:
            bool: 是否成功加入安全队列（如果 2 秒内重复同一句，返回 False）
        """
        if not isinstance(utterance, Utterance):
            utterance = Utterance(text=str(utterance))

        now = time.time()

        # 限制 2 秒内重复同一句安全播报
        if utterance.text == self._last_safety_utter and (now - self._last_safety_time) < 2.0:
            return False

        # 确保安全播报具有最高优先级和 interrupt 标志
        utterance.priority = max(utterance.priority, 100)  # 安全播报至少 100 优先级
        utterance.interrupt = True
        utterance.meta = utterance.meta or {}
        utterance.meta["ttscategory"] = "SAFETY"
        utterance.meta["safety"] = True

        self._safety_queue.append(utterance)
        self._last_safety_utter = utterance.text
        self._last_safety_time = now
        return True

    def get_safety_queue(self) -> List[Utterance]:
        """
        Step 11: 返回当前安全队列的快照（不清空），主要用于调试与测试。

        Returns:
            List[Utterance]: 当前安全队列的副本
        """
        return list(self._safety_queue)

    def get_queue(self) -> List[Utterance]:
        """
        返回当前队列的快照（不清空，不排序），主要用于调试与测试。

        保持插入顺序。

        Returns:
            List[Utterance]: 当前队列的副本
        """
        return list(self._queue)

    def pop_all(self) -> List[Utterance]:
        """
        取出当前队列中的所有 Utterance，并清空队列。

        Step 11 + Step 12: 使用 PriorityScheduler 统一调度。

        返回结果按以下规则排序：
        - 安全队列优先（全部先于主队列）
        - 主队列内按 PriorityBand: P1 > P2 > P3
        - 同 band 内按 priority 降序，同 priority 按 created_at 升序

        Returns:
            List[Utterance]: 按优先级排序后的队列中的所有 Utterance
        """
        result: List[Utterance] = []

        # Step 12: 使用 PriorityScheduler 统一调度
        # 将主队列转换为 deque（临时，用于调度器）
        main_queue_deque = deque(self._queue)
        
        # 逐个选择并添加到结果
        while True:
            utter = self._scheduler.select_next(self._safety_queue, main_queue_deque)
            if utter is None:
                break
            result.append(utter)

        # 清空队列
        self._queue.clear()
        self._safety_queue.clear()

        return result

    def pop_next(self) -> Optional[Utterance]:
        """
        Step 12: 使用 PriorityScheduler 统一决定下一条播报。

        Returns:
            Optional[Utterance]: 下一条要播报的 Utterance，如果队列为空则返回 None
        """
        # 将主队列转换为 deque（临时，用于调度器）
        main_queue_deque = deque(self._queue)
        
        utter = self._scheduler.select_next(self._safety_queue, main_queue_deque)
        
        if utter is None:
            return None
        
        # 从原始队列中移除已选中的 Utterance
        if utter in self._queue:
            self._queue.remove(utter)
        
        return utter

    def clear(self) -> None:
        """清空所有队列（主队列 + 安全队列）"""
        self._queue.clear()
        self._safety_queue.clear()
        self._last_safety_utter = None
        self._last_safety_time = 0.0


# 简单的模块级单例，方便 TaskChainManager / Demo 直接使用
tts_manager = TtsManager()

