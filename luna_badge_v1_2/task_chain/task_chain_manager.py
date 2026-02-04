"""
Task Chain Manager

任务链管理器（稳定版骨架）。

v1.5 设计原则：
- TaskChain 不是流程控制器，而是「任务状态主权者」
- 模型、控制器、PlanB 全都必须服从 TaskChain 的状态机
- 与 MOC / Fallback 解耦
"""

from typing import Dict, Any, Optional
from .task_state import TaskState
from .task_node import TaskNode
from .task_context import TaskContext


class TaskChainManager:
    """
    任务链管理器
    
    职责：
    - 管理任务链的生命周期（启动、暂停、恢复、中止）
    - 维护任务链状态
    - 协调任务节点执行
    - 接收 MOC 决策结果并处理
    - 与 FallbackExecutor 对接
    
    v1.5 定位：
    - TaskChain 是"任务状态主权者"
    - 解决"我现在在哪一步"、"是否允许中断"、"中断后能否继续"
    """
    
    def __init__(self, fallback_executor=None, metrics_collector=None, trace_id=None):
        """
        初始化任务链管理器
        
        Args:
            fallback_executor: FallbackExecutor 实例（可选，用于 PlanB）
            metrics_collector: 指标收集器（可选）
            trace_id: 跟踪 ID（可选）
        """
        self.current_node: Optional[TaskNode] = None
        self.state = TaskState.PENDING
        self.context = TaskContext()
        self.fallback_executor = fallback_executor
        self.metrics_collector = metrics_collector
        self.trace_id = trace_id or (metrics_collector.new_trace_id() if metrics_collector else None)
        
        # 记录启动事件
        self.context.record({
            "type": "task_chain_initialized",
            "state": self.state.value
        })
    
    def start(self, task_node: TaskNode):
        """
        启动任务链
        
        Args:
            task_node: 任务节点
        """
        if self.state != TaskState.PENDING:
            raise RuntimeError(f"Cannot start task chain in state {self.state}")
        
        self.current_node = task_node
        self.state = TaskState.RUNNING
        
        # 记录启动事件
        self.context.record({
            "type": "task_chain_started",
            "node_id": task_node.node_id,
            "domain": task_node.domain,
            "state": self.state.value
        })
        
        # 记录 node_start 事件（打点）
        if self.metrics_collector and self.trace_id:
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=task_node.domain,
                node_id=task_node.node_id,
                event="node_start",
                payload={"state": self.state.value}
            )
    
    def pause(self):
        """
        暂停任务链执行
        
        v1.5: 暂停后状态变为 PAUSED，可以恢复
        """
        if not self.state.can_pause():
            raise RuntimeError(f"Cannot pause task chain in state {self.state}")
        
        self.state = TaskState.PAUSED
        if self.current_node:
            self.current_node.pause()
        
        # 记录暂停事件
        self.context.record({
            "type": "task_chain_paused",
            "state": self.state.value
        })
    
    def resume(self):
        """
        恢复任务链执行
        
        v1.5: 从 PAUSED 恢复，状态变为 RUNNING
        """
        if not self.state.can_resume():
            raise RuntimeError(f"Cannot resume task chain in state {self.state}")
        
        self.state = TaskState.RUNNING
        if self.current_node:
            self.current_node.resume()
        
        # 记录恢复事件
        self.context.record({
            "type": "task_chain_resumed",
            "state": self.state.value
        })
    
    def abort(self, reason: str):
        """
        中止任务链
        
        Args:
            reason: 中止原因
            
        v1.5: 中止后状态变为 ABORTED，不可恢复
        """
        self.state = TaskState.ABORTED
        if self.current_node:
            self.current_node.abort(reason)
        
        # 记录中止事件
        self.context.record({
            "type": "task_chain_aborted",
            "reason": reason,
            "state": self.state.value
        })
        
        # 记录 node_end 事件（打点）
        if self.metrics_collector and self.trace_id and self.current_node:
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=self.current_node.domain,
                node_id=self.current_node.node_id,
                event="node_end",
                payload={"state": self.state.value, "reason": reason}
            )
    
    def handle_result(self, result: Dict[str, Any]):
        """
        接收 Model Output Controller 的决策结果
        
        Args:
            result: MOC 返回的决策结果（符合 decision_schema.json）
            
        v1.5: 这是 TaskChain × MOC × PlanB 的最小闭环入口
        """
        if self.state.is_terminal():
            raise RuntimeError(f"Cannot handle result in terminal state {self.state}")
        
        decision = result.get("decision")
        
        if decision == "commit":
            self._complete_node(result)
        
        elif decision == "fallback":
            self._handle_fallback(result)
        
        elif decision == "abort":
            self.abort(result.get("reason", "MOC requested abort"))
        
        else:
            # 未知决策，标记为失败
            self._mark_node_failed(f"Unknown decision: {decision}")
    
    def _complete_node(self, result: Dict[str, Any]):
        """
        完成当前节点
        
        Args:
            result: MOC 返回的决策结果
        """
        if self.current_node:
            self.current_node.mark_completed()
        
        # 记录完成事件
        self.context.record({
            "type": "node_completed",
            "node_id": self.current_node.node_id if self.current_node else None,
            "decision": result.get("decision"),
            "used_model": result.get("used_model")
        })
        
        # v1.5: 节点完成后，任务链状态变为 COMPLETED
        # 实际应用中，这里可能会启动下一个节点
        self.state = TaskState.COMPLETED
        
        # 记录 node_end 事件（打点）
        if self.metrics_collector and self.trace_id and self.current_node:
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=self.current_node.domain,
                node_id=self.current_node.node_id,
                event="node_end",
                payload={"state": self.state.value, "decision": result.get("decision")}
            )
    
    def _handle_fallback(self, decision: Dict[str, Any]):
        """
        处理 fallback 决策
        
        将 fallback 行为交给 FallbackExecutor
        
        Args:
            decision: MOC 返回的 fallback 决策结果
        """
        if not self.fallback_executor:
            # 没有 FallbackExecutor，直接标记为失败
            self._mark_node_failed("No fallback executor available")
            return
        
        if not self.current_node:
            self.abort("No current node for fallback")
            return
        
        # 1. 更新 attempts
        domain = self.current_node.domain
        self.context.increment_attempt(domain)
        
        # 2. 调用 FallbackExecutor
        reason = decision.get("reason", "unknown")
        fallback_action = self.fallback_executor.execute(
            task_domain=domain,
            reason=reason,
            context={
                "attempt": self.context.get_attempt_count(domain),
                "node_id": self.current_node.node_id
            }
        )
        
        # 3. 根据返回 action 调整执行路径
        action = fallback_action.get("action")
        
        if action == "abort":
            # FallbackExecutor 决定中止
            self.abort(fallback_action.get("reason", "Fallback executor requested abort"))
        
        elif action == "wait":
            # 处于冷却期，标记为暂停
            self.pause()
            # 记录等待事件
            self.context.record({
                "type": "fallback_cooldown",
                "cooldown_ms": fallback_action.get("cooldown_remaining_ms", 0),
                "reason": reason
            })
        
        else:
            # switch_model / degrade_capability / cross_domain
            # v1.5: 标记为失败，允许 PlanB 恢复
            self._mark_node_failed(f"Fallback triggered: {action}")
            
            # 记录 fallback 事件
            self.context.record({
                "type": "fallback_triggered",
                "action": action,
                "target": fallback_action.get("target"),
                "plan": fallback_action.get("plan"),
                "attempt": fallback_action.get("attempt"),
                "reason": reason
            })
    
    def _mark_node_failed(self, reason: str):
        """
        标记当前节点失败
        
        Args:
            reason: 失败原因
            
        v1.5: 失败后状态变为 FAILED，可以恢复（通过 PlanB）
        """
        if self.current_node:
            self.current_node.mark_failed(reason)
        
        self.state = TaskState.FAILED
        
        # 记录失败事件
        self.context.record({
            "type": "node_failed",
            "node_id": self.current_node.node_id if self.current_node else None,
            "reason": reason,
            "state": self.state.value
        })
    
    def handle_fallback(self, fallback_action: Dict[str, Any]):
        """
        处理 FallbackExecutor 返回的行动描述
        
        v1.5: TaskChain 不理解"为什么 fallback"，只理解"接下来要干什么"
        
        Args:
            fallback_action: FallbackExecutor 返回的行动描述
        """
        action = fallback_action.get("action")
        
        if action == "abort":
            self.abort(fallback_action.get("reason", "Fallback requested abort"))
        
        elif action == "wait":
            # 处于冷却期，暂停任务链
            if self.state == TaskState.RUNNING:
                self.pause()
        
        else:
            # switch_model / degrade_capability / cross_domain
            # v1.5: 这些 action 由外部系统（如 TaskChainManager 的调用者）处理
            # TaskChain 只记录事件
            self.context.record({
                "type": "fallback_action_received",
                "action": action,
                "target": fallback_action.get("target"),
                "plan": fallback_action.get("plan"),
                "attempt": fallback_action.get("attempt")
            })
