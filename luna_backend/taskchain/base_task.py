"""
任务基类 (BaseTask) v1.2.0
所有任务链任务的抽象基类：医院任务、导航任务、洗手间任务都继承它
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseTask(ABC):
    """
    所有任务链任务的抽象基类
    
    医院任务、导航任务、洗手间任务都继承它
    """
    
    def __init__(self, task_id: str, meta: Optional[Dict[str, Any]] = None):
        """
        初始化任务
        
        Args:
            task_id: 任务ID
            meta: 任务元数据
        """
        self.task_id = task_id
        self.meta = meta or {}
        self.state = "pending"  # pending / running / paused / completed / cancelled
    
    @abstractmethod
    def start(self):
        """
        任务开始时调用
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: Dict[str, Any]):
        """
        处理事件
        
        event = {"type": "...", "payload": {...}}
        例如: type=voice_intent / vision / nav_update / hospital_stage_update
        
        Args:
            event: 事件字典
        """
        pass
    
    def pause(self, reason: str = ""):
        """
        暂停任务
        
        Args:
            reason: 暂停原因
        """
        self.state = "paused"
    
    def resume(self):
        """恢复任务"""
        self.state = "running"
    
    def cancel(self, reason: str = ""):
        """
        取消任务
        
        Args:
            reason: 取消原因
        """
        self.state = "cancelled"
    
    def is_finished(self) -> bool:
        """
        检查任务是否完成
        
        Returns:
            是否完成
        """
        return self.state in ("completed", "cancelled")
    
    def get_state(self) -> str:
        """
        获取任务状态
        
        Returns:
            任务状态
        """
        return self.state



