"""
Task Node

任务节点定义。

v1.5 设计原则：
- 一个 Node 执行一次"意图明确的动作"
- Node 不保存模型细节
- Node 的失败原因必须可记录
- Node 是可恢复的最小执行单元
"""

from typing import Dict, Any, Optional
from .task_state import TaskState


class TaskNode:
    """
    任务节点
    
    职责：
    - 表示任务链中的一个执行单元
    - 封装节点状态和转换逻辑
    - 一个 Node 执行一次"意图明确的动作"
    
    v1.5 要求：
    - Node 不保存模型细节
    - Node 的失败原因必须可记录
    - Node 必须支持 pause/resume/abort
    """
    
    def __init__(self, node_id: str, domain: str):
        """
        初始化任务节点
        
        Args:
            node_id: 节点标识符
            domain: 任务领域（如 "navigation", "safety", "inquiry"）
        """
        self.node_id = node_id
        self.domain = domain
        self.state = TaskState.PENDING
        self.failure_reason: Optional[str] = None
        self.execution_context: Dict[str, Any] = {}
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行节点逻辑
        
        Args:
            context: 执行上下文（来自 TaskContext）
            
        Returns:
            执行结果：
            {
                "success": bool,
                "data": Any,
                "error": Optional[str]
            }
        """
        if self.state != TaskState.PENDING and self.state != TaskState.PAUSED:
            raise RuntimeError(f"Cannot execute node {self.node_id} in state {self.state}")
        
        self.state = TaskState.RUNNING
        self.execution_context = context.copy()
        
        # v1.5: Node 不直接调用模型，只返回执行结果
        # 实际执行由 TaskChainManager 协调模型 Adapter 完成
        # 这里只做状态管理
        
        return {
            "success": True,
            "data": None,
            "error": None
        }
    
    def pause(self):
        """
        暂停节点执行
        
        v1.5: 暂停后状态变为 PAUSED，可以恢复
        """
        if self.state == TaskState.RUNNING or self.state == TaskState.PENDING:
            self.state = TaskState.PAUSED
    
    def resume(self):
        """
        恢复节点执行
        
        v1.5: 从 PAUSED 恢复，状态变为 RUNNING
        """
        if self.state == TaskState.PAUSED:
            self.state = TaskState.RUNNING
    
    def abort(self, reason: str):
        """
        中止节点执行
        
        Args:
            reason: 中止原因
            
        v1.5: 中止后状态变为 ABORTED，不可恢复
        """
        self.state = TaskState.ABORTED
        self.failure_reason = reason
    
    def mark_failed(self, reason: str):
        """
        标记节点失败
        
        Args:
            reason: 失败原因
            
        v1.5: 失败后状态变为 FAILED，可以恢复（通过 PlanB）
        """
        self.state = TaskState.FAILED
        self.failure_reason = reason
    
    def mark_completed(self):
        """
        标记节点完成
        
        v1.5: 完成后状态变为 COMPLETED
        """
        self.state = TaskState.COMPLETED





