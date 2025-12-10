from core.logging import get_logger

# task_chain.py

log = get_logger("task_chain")
"""
任务链基类（占位实现）
具体任务链需要继承此类并实现相应方法
"""


class TaskChain:
    """
    任务链基类
    """
    
    def __init__(self, name):
        self.name = name
        self.state = "IDLE"
    
    def start(self):
        """启动任务链"""
        self.state = "RUNNING"
        log.info(f"[TaskChain] {self.name} started")
    
    def pause(self):
        """暂停任务链"""
        self.state = "PAUSED"
        log.info(f"[TaskChain] {self.name} paused")
    
    def resume(self):
        """恢复任务链"""
        self.state = "RUNNING"
        log.info(f"[TaskChain] {self.name} resumed")
    
    def cancel(self):
        """取消任务链"""
        self.state = "CANCELLED"
        log.info(f"[TaskChain] {self.name} cancelled")
    
    def complete(self):
        """完成任务链"""
        self.state = "COMPLETED"
        log.info(f"[TaskChain] {self.name} completed")














