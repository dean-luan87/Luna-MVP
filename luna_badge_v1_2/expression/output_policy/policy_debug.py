"""
Policy Debug (v1.4.8 Step 13)

调试与可视化
"""

from typing import Optional
from expression.output_policy.output_slot import OutputSlot
from expression.output_policy.output_queue import OutputQueue


def log_output_slot(slot: Optional[OutputSlot]) -> None:
    """
    记录 OutputSlot 日志
    
    Args:
        slot: 输出槽位（可选）
    """
    if not slot:
        return
    
    print(
        "[OUTPUT_POLICY]",
        f"approved={slot.approved}",
        f"priority={slot.priority}",
        f"interrupt={slot.can_interrupt}",
        f"ttl_ms={slot.ttl_ms}",
        f"reason={slot.reason}",
        f"intent_type={slot.intent.intent_type}",
        f"urgency={slot.intent.urgency}"
    )


def log_output_queue(queue: OutputQueue) -> None:
    """
    记录输出队列状态
    
    Args:
        queue: 输出队列
    """
    print(
        "[OUTPUT_QUEUE]",
        f"size={queue.size()}"
    )
    
    if queue.size() > 0:
        peek_slot = queue.peek()
        if peek_slot:
            print(
        "[OUTPUT_QUEUE]",
        f"next_priority={peek_slot.priority}",
        f"next_intent_type={peek_slot.intent.intent_type}"
    )
