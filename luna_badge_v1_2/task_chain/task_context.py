"""
Task Context

任务上下文定义。

v1.5 设计原则：
- TaskContext 是任务唯一事实源
- attempts 用于 PlanB 次数统计
- history 用于复盘（与 logs 对齐）
"""

from typing import Dict, Any, List, Optional


class TaskContext:
    """
    任务上下文
    
    职责：
    - 封装任务执行过程中的上下文信息
    - 传递状态和数据给任务节点
    - 记录任务历史（用于复盘）
    - 追踪 PlanB 尝试次数
    
    v1.5 要求：
    - TaskContext 是任务唯一事实源
    - attempts 用于 PlanB 次数统计
    - history 用于复盘（与 logs 对齐）
    """
    
    def __init__(self):
        """初始化任务上下文"""
        # 数据存储
        self.data: Dict[str, Any] = {}
        
        # PlanB 尝试次数统计（key: domain, value: count）
        self.attempts: Dict[str, int] = {}
        
        # 事件历史（用于复盘）
        self.history: List[Dict[str, Any]] = []
    
    def get(self, key: str, default=None) -> Any:
        """
        获取上下文值
        
        Args:
            key: 键名
            default: 默认值
            
        Returns:
            上下文值
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        设置上下文值
        
        Args:
            key: 键名
            value: 值
        """
        self.data[key] = value
    
    def record(self, event: Dict[str, Any]):
        """
        记录事件到历史
        
        Args:
            event: 事件字典，必须包含至少 "type" 和 "timestamp"
            
        v1.5: 所有重要事件都应该记录到 history
        """
        import time
        if "timestamp" not in event:
            event["timestamp"] = time.time()
        self.history.append(event)
    
    def increment_attempt(self, domain: str):
        """
        增加 PlanB 尝试次数
        
        Args:
            domain: 任务领域
        """
        if domain not in self.attempts:
            self.attempts[domain] = 0
        self.attempts[domain] += 1
    
    def get_attempt_count(self, domain: str) -> int:
        """
        获取 PlanB 尝试次数
        
        Args:
            domain: 任务领域
            
        Returns:
            尝试次数
        """
        return self.attempts.get(domain, 0)
    
    def reset_attempts(self, domain: Optional[str] = None):
        """
        重置尝试次数
        
        Args:
            domain: 任务领域（如果为 None，重置所有）
        """
        if domain is None:
            self.attempts.clear()
        elif domain in self.attempts:
            del self.attempts[domain]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        序列化为字典（用于快照/恢复）
        
        Returns:
            上下文字典
        """
        return {
            "data": self.data.copy(),
            "attempts": self.attempts.copy(),
            "history": self.history.copy()
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """
        从字典恢复（用于快照/恢复）
        
        Args:
            data: 上下文字典
        """
        self.data = data.get("data", {}).copy()
        self.attempts = data.get("attempts", {}).copy()
        self.history = data.get("history", []).copy()





