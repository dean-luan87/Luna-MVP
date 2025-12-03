# task_manager.py

"""
任务管理器（兼容层）
用于 TaskChainRouter 调用，实际委托给 TaskEngine
"""

from core.task.task_engine import TaskEngine


class TaskManager:
    """
    任务管理器：管理任务链的执行、切换、插入等
    
    这是一个兼容层，实际功能由 TaskEngine 提供
    """
    
    def __init__(self, task_engine=None):
        """
        如果传入 TaskEngine，则使用它；否则创建新的
        """
        if task_engine:
            self.engine = task_engine
        else:
            self.engine = TaskEngine()
    
    def force_start(self, task_id, chain):
        """
        强制启动任务链（用于危险情况）
        """
        self.engine.force_start(task_id, chain)
    
    def switch_to(self, task_id, chain):
        """
        切换到新任务链（替换主任务）
        """
        self.engine.switch_to(task_id, chain)
    
    def insert_task(self, task_id, chain):
        """
        插入任务链（保留主任务）
        """
        self.engine.insert_task(task_id, chain)
    
    def append_contextual(self, task_id, chain):
        """
        追加上下文任务（继续主任务）
        """
        # 对于 continue 模式，可以简单地插入任务
        self.engine.insert_task(task_id, chain)

