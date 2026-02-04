"""
Fail-Safe Trigger

失效保护触发器。

v1.5 设计原则：
- 发现异常 → 判断级别 → 选择 Fail-Safe 行为
- 不直接重启，而是根据异常类型选择合适的行为
- 4 级 Fail-Safe 行为：FS-1 软干预、FS-2 任务重置、FS-3 系统暂停、FS-4 终止并恢复
"""

from typing import Dict, Any, Optional
from enum import Enum
from .watchdog_monitor import AnomalyType


class FailSafeLevel(Enum):
    """Fail-Safe 等级"""
    FS_1_SOFT_INTERVENTION = "FS-1"      # 软干预：暂停当前 TaskNode，重新评估环境，触发 PlanB
    FS_2_TASK_RESET = "FS-2"            # 任务重置：中止当前 node，回到上一个安全节点，保留 TaskContext
    FS_3_SYSTEM_PAUSE = "FS-3"          # 系统暂停：停止所有自动执行，明确告知用户，等待指令
    FS_4_ABORT_RECOVER = "FS-4"         # 终止并恢复：终止任务链，写入错误原因，提供恢复入口


class FailSafeTrigger:
    """
    失效保护触发器
    
    职责：
    - 接收 anomaly
    - 判定 Fail-Safe 等级
    - 下发行为指令
    
    v1.5: 触发即"决策点"，不是直接重启
    """
    
    def __init__(self, task_chain_manager=None, metrics_collector=None, trace_id=None):
        """
        初始化失效保护触发器
        
        Args:
            task_chain_manager: TaskChainManager 实例（可选）
            metrics_collector: 指标收集器（可选）
            trace_id: 跟踪 ID（可选）
        """
        self.task_chain = task_chain_manager
        self.metrics_collector = metrics_collector
        self.trace_id = trace_id
        
        # Fail-Safe 行为映射（anomaly_type -> FS level）
        self.anomaly_to_failsafe = {
            AnomalyType.MODEL_TIMEOUT: FailSafeLevel.FS_1_SOFT_INTERVENTION,
            AnomalyType.MODEL_NO_RETURN: FailSafeLevel.FS_1_SOFT_INTERVENTION,
            AnomalyType.MODEL_LOW_CONFIDENCE: FailSafeLevel.FS_1_SOFT_INTERVENTION,
            AnomalyType.NODE_TIMEOUT: FailSafeLevel.FS_2_TASK_RESET,
            AnomalyType.STATE_INCONSISTENT: FailSafeLevel.FS_2_TASK_RESET,
            AnomalyType.FALLBACK_LOOP: FailSafeLevel.FS_4_ABORT_RECOVER,
            AnomalyType.ENV_MUTATION: FailSafeLevel.FS_3_SYSTEM_PAUSE,
        }
    
    def decide(self, anomaly: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据异常类型返回 Fail-Safe 行为
        
        Args:
            anomaly: WatchdogMonitor 返回的异常描述
            
        Returns:
            Fail-Safe 行为指令：
            {
                "level": FailSafeLevel,
                "action": str,
                "reason": str,
                "context": Dict
            }
        """
        anomaly_type = anomaly.get("type")
        severity = anomaly.get("severity", "medium")
        description = anomaly.get("description", "")
        context = anomaly.get("context", {})
        
        # 根据异常类型映射到 Fail-Safe 等级
        fs_level = self.anomaly_to_failsafe.get(anomaly_type, FailSafeLevel.FS_2_TASK_RESET)
        
        # 根据等级生成行为指令
        if fs_level == FailSafeLevel.FS_1_SOFT_INTERVENTION:
            return {
                "level": fs_level.value,
                "action": "pause_node_and_trigger_planb",
                "reason": description,
                "context": context,
                "steps": [
                    "暂停当前 TaskNode",
                    "重新评估环境",
                    "触发 PlanB"
                ]
            }
        
        elif fs_level == FailSafeLevel.FS_2_TASK_RESET:
            return {
                "level": fs_level.value,
                "action": "reset_task_node",
                "reason": description,
                "context": context,
                "steps": [
                    "中止当前 node",
                    "回到上一个安全节点",
                    "保留 TaskContext"
                ]
            }
        
        elif fs_level == FailSafeLevel.FS_3_SYSTEM_PAUSE:
            return {
                "level": fs_level.value,
                "action": "pause_system_and_notify_user",
                "reason": description,
                "context": context,
                "steps": [
                    "停止所有自动执行",
                    "明确告知用户",
                    "等待指令"
                ]
            }
        
        elif fs_level == FailSafeLevel.FS_4_ABORT_RECOVER:
            return {
                "level": fs_level.value,
                "action": "abort_task_and_provide_recovery",
                "reason": description,
                "context": context,
                "steps": [
                    "终止任务链",
                    "写入错误原因",
                    "提供恢复入口"
                ]
            }
        
        # 默认行为
        return {
            "level": FailSafeLevel.FS_2_TASK_RESET.value,
            "action": "reset_task_node",
            "reason": description,
            "context": context
        }
    
    def execute(self, failsafe_action: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Fail-Safe 行为
        
        Args:
            failsafe_action: decide() 返回的行为指令
            
        Returns:
            执行结果：
            {
                "success": bool,
                "action_taken": str,
                "context_snapshot": str
            }
        """
        if not self.task_chain:
            return {
                "success": False,
                "action_taken": "no_task_chain",
                "error": "No task chain manager available"
            }
        
        level = failsafe_action.get("level")
        action = failsafe_action.get("action")
        reason = failsafe_action.get("reason", "")
        
        # 生成上下文快照（用于审计）
        context_snapshot = self._create_context_snapshot()
        
        # 记录 watchdog 事件（打点）
        if self.metrics_collector and self.trace_id:
            task_domain = "unknown"
            node_id = "unknown"
            if self.task_chain and self.task_chain.current_node:
                task_domain = self.task_chain.current_node.domain
                node_id = self.task_chain.current_node.node_id
            
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=task_domain,
                node_id=node_id,
                event="watchdog",
                payload={
                    "anomaly": failsafe_action.get("reason", ""),
                    "failsafe_level": level,
                    "action": action,
                    "context_snapshot": context_snapshot
                }
            )
            
            # 记录错误日志
            self.metrics_collector.error(
                error_type="watchdog_triggered",
                severity="high",
                context={
                    "failsafe_level": level,
                    "action": action,
                    "reason": failsafe_action.get("reason", "")
                }
            )
        
        # 根据 action 执行相应行为
        if action == "pause_node_and_trigger_planb":
            # FS-1: 软干预
            if self.task_chain.state.value == "running":
                self.task_chain.pause()
            return {
                "success": True,
                "action_taken": "paused_node",
                "context_snapshot": context_snapshot,
                "next_step": "trigger_planb"
            }
        
        elif action == "reset_task_node":
            # FS-2: 任务重置
            if self.task_chain.current_node:
                self.task_chain.current_node.abort(reason)
            # 保留 TaskContext，但重置节点
            return {
                "success": True,
                "action_taken": "reset_node",
                "context_snapshot": context_snapshot,
                "next_step": "restore_safe_node"
            }
        
        elif action == "pause_system_and_notify_user":
            # FS-3: 系统暂停
            if self.task_chain.state.value == "running":
                self.task_chain.pause()
            return {
                "success": True,
                "action_taken": "paused_system",
                "context_snapshot": context_snapshot,
                "user_notification": f"系统已暂停：{reason}",
                "next_step": "wait_user_instruction"
            }
        
        elif action == "abort_task_and_provide_recovery":
            # FS-4: 终止并恢复
            self.task_chain.abort(reason)
            return {
                "success": True,
                "action_taken": "aborted_task",
                "context_snapshot": context_snapshot,
                "recovery_available": True,
                "next_step": "provide_recovery_entry"
            }
        
        return {
            "success": False,
            "action_taken": "unknown_action",
            "error": f"Unknown action: {action}"
        }
    
    def _create_context_snapshot(self) -> str:
        """
        创建上下文快照（用于审计）
        
        Returns:
            快照 ID（简化版，实际应该保存到文件/数据库）
        """
        import hashlib
        import json
        
        if not self.task_chain:
            return "no_context"
        
        snapshot_data = {
            "task_state": self.task_chain.state.value,
            "node_id": self.task_chain.current_node.node_id if self.task_chain.current_node else None,
            "context": self.task_chain.context.to_dict()
        }
        
        snapshot_str = json.dumps(snapshot_data, sort_keys=True)
        snapshot_id = hashlib.md5(snapshot_str.encode()).hexdigest()[:8]
        
        return snapshot_id





