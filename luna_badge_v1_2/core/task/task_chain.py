# task_chain.py

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
        print(f"[TaskChain] {self.name} started")
    
    def pause(self):
        """暂停任务链"""
        self.state = "PAUSED"
        print(f"[TaskChain] {self.name} paused")
    
    def resume(self):
        """恢复任务链"""
        self.state = "RUNNING"
        print(f"[TaskChain] {self.name} resumed")
    
    def cancel(self):
        """取消任务链"""
        self.state = "CANCELLED"
        print(f"[TaskChain] {self.name} cancelled")
    
    def complete(self):
        """完成任务链"""
        self.state = "COMPLETED"
        print(f"[TaskChain] {self.name} completed")










