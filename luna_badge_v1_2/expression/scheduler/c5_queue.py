"""
C-5 Expression Queue

极简候选队列（非 FIFO）

队列约束（必须实现）：
- 最大长度：2
- 非 FIFO
- 只支持 3 个操作：enqueue, flush, replace

行为规则：
1. 视觉状态变化 → 任何 vision_state 改变 → flush()
2. 同 contract / duplicate_key → 新的直接 replace()
3. 队列满 → 丢弃低优先级
"""

from typing import List, Optional
from .c5_types import ExpressionCandidate


class C5ExpressionQueue:
    """
    极简表达式队列（候选池）
    
    最大长度：2
    非 FIFO
    """
    
    MAX_SIZE = 2
    
    def __init__(self):
        """初始化队列"""
        self._queue: List[ExpressionCandidate] = []
    
    def enqueue(self, expr: ExpressionCandidate) -> bool:
        """
        入队
        
        Args:
            expr: 表达式候选
            
        Returns:
            bool: True 表示成功入队
        """
        # 如果队列满，丢弃低优先级
        if len(self._queue) >= self.MAX_SIZE:
            # 找到最低优先级的项
            lowest_idx = -1
            lowest_urgency = "high"
            
            for i, item in enumerate(self._queue):
                urgency_map = {"high": 3, "normal": 2, "low": 1}
                if urgency_map.get(item.urgency, 0) < urgency_map.get(lowest_urgency, 0):
                    lowest_idx = i
                    lowest_urgency = item.urgency
            
            if lowest_idx >= 0:
                self._queue.pop(lowest_idx)
            else:
                # 如果都是高优先级，丢弃最旧的
                self._queue.pop(0)
        
        self._queue.append(expr)
        return True
    
    def flush(self, reason: str = "state_change"):
        """
        清空队列
        
        Args:
            reason: 清空原因
        """
        self._queue.clear()
    
    def replace(self, expr: ExpressionCandidate) -> bool:
        """
        替换（如果存在相同 contract_id 或 duplicate_key）
        
        Args:
            expr: 表达式候选
            
        Returns:
            bool: True 表示已替换
        """
        # 查找相同 contract_id 或 duplicate_key 的项
        for i, item in enumerate(self._queue):
            if (item.contract_id == expr.contract_id or
                (item.duplicate_key and expr.duplicate_key and
                 item.duplicate_key == expr.duplicate_key)):
                # 替换
                self._queue[i] = expr
                return True
        
        return False
    
    def peek(self) -> Optional[ExpressionCandidate]:
        """
        查看队列头（不删除）
        
        Returns:
            Optional[ExpressionCandidate]: 队列头项，如果为空则返回 None
        """
        if not self._queue:
            return None
        return self._queue[0]
    
    def dequeue(self) -> Optional[ExpressionCandidate]:
        """
        出队
        
        Returns:
            Optional[ExpressionCandidate]: 队列头项，如果为空则返回 None
        """
        if not self._queue:
            return None
        return self._queue.pop(0)
    
    def size(self) -> int:
        """
        获取队列大小
        
        Returns:
            int: 队列大小
        """
        return len(self._queue)
    
    def is_empty(self) -> bool:
        """
        判断队列是否为空
        
        Returns:
            bool: True 表示队列为空
        """
        return len(self._queue) == 0
