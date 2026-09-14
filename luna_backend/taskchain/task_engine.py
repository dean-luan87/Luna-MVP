"""
任务引擎 (TaskEngine) v1.2.0
后台任务调度器：管理HospitalTask、NavigationTask等任务
"""

from typing import Dict, Any, Optional, List
from .base_task import BaseTask

# 延迟导入
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class TaskEngine:
    """
    任务引擎
    
    管理所有任务的生命周期：enqueue / get_task / tick
    """
    
    def __init__(self):
        """初始化任务引擎"""
        self._tasks: Dict[str, BaseTask] = {}  # task_id -> task
        self._running_tasks: List[str] = []  # 正在运行的任务ID列表
    
    def enqueue(self, task: BaseTask):
        """
        入队任务
        
        Args:
            task: 任务实例
        """
        if not isinstance(task, BaseTask):
            system_log = _get_logger()
            system_log("TASK_ENQUEUE_INVALID", {"error": "task is not BaseTask instance"})
            return
        
        self._tasks[task.task_id] = task
        self._running_tasks.append(task.task_id)
        
        # 启动任务
        try:
            task.start()
        except Exception as e:
            system_log = _get_logger()
            system_log("TASK_START_ERROR", {
                "task_id": task.task_id,
                "error": str(e)
            })
    
    def get_task(self, task_id: str) -> Optional[BaseTask]:
        """
        获取任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务实例，如果不存在则返回None
        """
        return self._tasks.get(task_id)
    
    def tick(self):
        """
        任务引擎tick（可选，用于定期检查任务状态）
        """
        # TODO: 实现任务状态检查、超时处理等
        pass
    
    def remove_task(self, task_id: str) -> bool:
        """
        移除任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功移除
        """
        if task_id in self._tasks:
            task = self._tasks[task_id]
            task.cancel("任务被移除")
            del self._tasks[task_id]
            if task_id in self._running_tasks:
                self._running_tasks.remove(task_id)
            return True
        return False
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """
        列出所有任务
        
        Returns:
            任务列表
        """
        return [
            {
                "task_id": task.task_id,
                "state": task.get_state(),
                "meta": task.meta
            }
            for task in self._tasks.values()
        ]



