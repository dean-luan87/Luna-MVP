"""
Output Queue (v1.4.8 Step 13)

输出队列（不执行，只排队）
"""

from typing import List, Optional
from expression.output_policy.output_slot import OutputSlot


class OutputQueue:
    """
    输出队列（不执行，只排队）
    """
    
    def __init__(self):
        """初始化队列"""
        self.queue: List[OutputSlot] = []
    
    def push(self, slot: OutputSlot) -> None:
        """
        添加 OutputSlot 到队列（按优先级排序）
        
        Args:
            slot: 输出槽位
        """
        self.queue.append(slot)
        # 按优先级降序排序（优先级高的在前）
        self.queue.sort(key=lambda s: s.priority, reverse=True)
    
    def pop(self) -> Optional[OutputSlot]:
        """
        从队列中取出优先级最高的 OutputSlot
        
        Returns:
            OutputSlot: 如果队列不为空，返回优先级最高的槽位；否则返回 None
        """
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def peek(self) -> Optional[OutputSlot]:
        """
        查看队列中优先级最高的 OutputSlot（不移除）
        
        Returns:
            OutputSlot: 如果队列不为空，返回优先级最高的槽位；否则返回 None
        """
        if not self.queue:
            return None
        return self.queue[0]
    
    def size(self) -> int:
        """获取队列大小"""
        return len(self.queue)
    
    def clear(self) -> None:
        """清空队列"""
        self.queue.clear()
