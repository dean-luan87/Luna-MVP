"""
Expression Queue

表达式队列（候选池，不是 FIFO）

队列必须支持的操作：
1. enqueue(expr)
2. flush(reason)
3. replace_if_same_contract(expr)
4. drop_if_outdated(ctx)
"""

from typing import List, Optional, Dict
import time
from ..calibration.expression_params import ExpressionParams
from .vision_rhythm_context import VisionRhythmContext


class ExpressionQueue:
    """
    表达式队列（候选池）
    
    关键触发规则（必须实现）：
    1. 视觉状态变化 → STABLE → TURNING → flush()
    2. 视觉锁定增强 → visual_confidence ↑ → drop 低优先级
    3. 新表达更贴近当前视觉 → replace old expression
    """
    
    def __init__(self):
        """初始化队列"""
        self._queue: List[ExpressionParams] = []
        self._timestamps: Dict[int, float] = {}
        self._counter = 0
    
    def enqueue(self, expr: ExpressionParams) -> int:
        """
        入队
        
        Args:
            expr: 表达参数
            
        Returns:
            int: 队列项 ID
        """
        self._counter += 1
        item_id = self._counter
        self._queue.append(expr)
        self._timestamps[item_id] = time.time()
        return item_id
    
    def flush(self, reason: str = "state_change"):
        """
        清空队列
        
        Args:
            reason: 清空原因
        """
        self._queue.clear()
        self._timestamps.clear()
    
    def replace_if_same_contract(
        self,
        expr: ExpressionParams,
        contract_id: Optional[str] = None
    ) -> bool:
        """
        如果是相同合约，替换
        
        Args:
            expr: 新表达参数
            contract_id: 合约 ID（可选）
            
        Returns:
            bool: True 表示已替换
        """
        if contract_id is None:
            contract_id = getattr(expr, 'contract_id', expr.action)
        
        # 查找相同合约的项
        for i, item in enumerate(self._queue):
            item_contract_id = getattr(item, 'contract_id', item.action)
            if item_contract_id == contract_id:
                # 替换
                self._queue[i] = expr
                return True
        
        return False
    
    def drop_if_outdated(self, ctx: VisionRhythmContext, max_age_ms: int = 1000):
        """
        丢弃过期的项
        
        Args:
            ctx: 视角节奏上下文
            max_age_ms: 最大年龄（毫秒）
        """
        now = time.time()
        max_age_s = max_age_ms / 1000.0
        
        # 移除过期的项
        to_remove = []
        for i, item in enumerate(self._queue):
            item_id = len(self._queue) - i  # 简化：使用索引作为 ID
            if item_id in self._timestamps:
                age = now - self._timestamps[item_id]
                if age > max_age_s:
                    to_remove.append(i)
        
        # 从后往前删除，避免索引错乱
        for i in reversed(to_remove):
            if i < len(self._queue):
                self._queue.pop(i)
    
    def peek(self) -> Optional[ExpressionParams]:
        """
        查看队列头（不删除）
        
        Returns:
            Optional[ExpressionParams]: 队列头项，如果为空则返回 None
        """
        if not self._queue:
            return None
        return self._queue[0]
    
    def dequeue(self) -> Optional[ExpressionParams]:
        """
        出队
        
        Returns:
            Optional[ExpressionParams]: 队列头项，如果为空则返回 None
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
