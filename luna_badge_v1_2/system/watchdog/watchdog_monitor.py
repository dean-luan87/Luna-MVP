"""
Watchdog Monitor

看门狗监控器。

v1.5 设计原则：
- Watchdog 的职责不是"修好一切"，而是及时止损，把控制权交还给系统与用户
- 任何情况下，系统都不能"无声失败、卡死、失控"
- 不做决策，只上报异常
"""

import time
from typing import Dict, Any, Optional, List
from enum import Enum


class AnomalyType(Enum):
    """异常类型枚举"""
    NODE_TIMEOUT = "node_timeout"              # 执行卡死：TaskNode 长时间无进展
    MODEL_TIMEOUT = "model_timeout"            # 模型异常：超时
    MODEL_NO_RETURN = "model_no_return"        # 模型异常：无返回
    MODEL_LOW_CONFIDENCE = "model_low_confidence"  # 模型异常：置信度异常
    STATE_INCONSISTENT = "state_inconsistent"  # 状态不一致：TaskChain state 与 node 行为冲突
    FALLBACK_LOOP = "fallback_loop"            # PlanB 循环：fallback 重复触发
    ENV_MUTATION = "env_mutation"              # 环境突变：视角世界发生明显变化


class WatchdogMonitor:
    """
    看门狗监控器
    
    职责：
    - 定期检查系统健康
    - 检测异常和死锁
    - 不做决策，只上报异常
    
    v1.5 必须覆盖的异常类型：
    1. 执行卡死（TaskNode 长时间无进展）
    2. 模型异常（超时/无返回/置信度异常）
    3. 状态不一致（TaskChain state 与 node 行为冲突）
    4. PlanB 循环（fallback 重复触发）
    5. 环境突变（视角世界发生明显变化）
    """
    
    def __init__(self, task_chain_manager=None):
        """
        初始化看门狗监控器
        
        Args:
            task_chain_manager: TaskChainManager 实例（可选）
        """
        self.task_chain = task_chain_manager
        
        # 监控配置
        self.node_timeout_seconds = 30.0  # TaskNode 超时阈值
        self.model_timeout_seconds = 10.0  # 模型超时阈值
        self.fallback_loop_threshold = 5  # PlanB 循环阈值
        
        # 运行时状态
        self.node_start_times: Dict[str, float] = {}  # node_id -> start_time
        self.last_check_time: float = time.time()
        self.anomaly_history: List[Dict[str, Any]] = []
    
    def start(self):
        """启动监控"""
        self.last_check_time = time.time()
    
    def check(self) -> Optional[Dict[str, Any]]:
        """
        周期性调用，检查系统健康
        
        Returns:
            异常描述（如果发现异常），否则返回 None：
            {
                "type": AnomalyType,
                "severity": "high" | "medium" | "low",
                "description": str,
                "context": Dict
            }
        """
        if not self.task_chain:
            return None
        
        current_time = time.time()
        anomalies = []
        
        # 1. 检查当前 TaskState
        state_anomaly = self._check_task_state()
        if state_anomaly:
            anomalies.append(state_anomaly)
        
        # 2. 检查 TaskNode 是否超时
        timeout_anomaly = self._check_node_timeout(current_time)
        if timeout_anomaly:
            anomalies.append(timeout_anomaly)
        
        # 3. 检查 attempts 是否异常（PlanB 循环）
        loop_anomaly = self._check_fallback_loop()
        if loop_anomaly:
            anomalies.append(loop_anomaly)
        
        # 4. 检查状态一致性
        consistency_anomaly = self._check_state_consistency()
        if consistency_anomaly:
            anomalies.append(consistency_anomaly)
        
        # 返回最严重的异常（如果有）
        if anomalies:
            # 按优先级排序：high > medium > low
            severity_order = {"high": 3, "medium": 2, "low": 1}
            anomalies.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 0), reverse=True)
            anomaly = anomalies[0]
            
            # 记录到历史
            self.anomaly_history.append({
                "timestamp": current_time,
                "anomaly": anomaly
            })
            
            return anomaly
        
        self.last_check_time = current_time
        return None
    
    def _check_task_state(self) -> Optional[Dict[str, Any]]:
        """检查 TaskState 是否合法"""
        if not self.task_chain:
            return None
        
        state = self.task_chain.state
        
        # v1.5: 如果状态是 RUNNING 但没有 current_node，这是异常
        if state.value == "running" and not self.task_chain.current_node:
            return {
                "type": AnomalyType.STATE_INCONSISTENT,
                "severity": "high",
                "description": "TaskChain is RUNNING but has no current_node",
                "context": {"state": state.value}
            }
        
        return None
    
    def _check_node_timeout(self, current_time: float) -> Optional[Dict[str, Any]]:
        """检查 TaskNode 是否超时"""
        if not self.task_chain or not self.task_chain.current_node:
            return None
        
        node = self.task_chain.current_node
        node_id = node.node_id
        
        # 如果节点刚启动，记录启动时间
        if node_id not in self.node_start_times:
            if node.state.value == "running":
                self.node_start_times[node_id] = current_time
            return None
        
        # 检查是否超时
        elapsed = current_time - self.node_start_times[node_id]
        if elapsed > self.node_timeout_seconds:
            return {
                "type": AnomalyType.NODE_TIMEOUT,
                "severity": "high",
                "description": f"TaskNode {node_id} has been running for {elapsed:.1f}s (timeout: {self.node_timeout_seconds}s)",
                "context": {
                    "node_id": node_id,
                    "elapsed_seconds": elapsed,
                    "timeout_seconds": self.node_timeout_seconds
                }
            }
        
        return None
    
    def _check_fallback_loop(self) -> Optional[Dict[str, Any]]:
        """检查 PlanB 循环"""
        if not self.task_chain:
            return None
        
        # 检查各域的 attempts
        for domain, count in self.task_chain.context.attempts.items():
            if count >= self.fallback_loop_threshold:
                return {
                    "type": AnomalyType.FALLBACK_LOOP,
                    "severity": "high",
                    "description": f"Fallback loop detected in domain {domain}: {count} attempts",
                    "context": {
                        "domain": domain,
                        "attempts": count,
                        "threshold": self.fallback_loop_threshold
                    }
                }
        
        return None
    
    def _check_state_consistency(self) -> Optional[Dict[str, Any]]:
        """检查状态一致性"""
        if not self.task_chain or not self.task_chain.current_node:
            return None
        
        chain_state = self.task_chain.state
        node_state = self.task_chain.current_node.state
        
        # v1.5: 如果 chain 是 RUNNING 但 node 不是 RUNNING/PAUSED，这是不一致
        if chain_state.value == "running":
            if node_state.value not in ["running", "paused"]:
                return {
                    "type": AnomalyType.STATE_INCONSISTENT,
                    "severity": "high",
                    "description": f"State inconsistency: chain={chain_state.value}, node={node_state.value}",
                    "context": {
                        "chain_state": chain_state.value,
                        "node_state": node_state.value
                    }
                }
        
        return None
    
    def record_model_anomaly(self, anomaly_type: AnomalyType, description: str, context: Dict[str, Any] = None):
        """
        记录模型异常（由外部调用）
        
        Args:
            anomaly_type: 异常类型
            description: 异常描述
            context: 上下文信息
        """
        self.anomaly_history.append({
            "timestamp": time.time(),
            "anomaly": {
                "type": anomaly_type,
                "severity": "high" if anomaly_type in [AnomalyType.MODEL_TIMEOUT, AnomalyType.MODEL_NO_RETURN] else "medium",
                "description": description,
                "context": context or {}
            }
        })
    
    def record_env_mutation(self, description: str, context: Dict[str, Any] = None):
        """
        记录环境突变（由外部调用）
        
        Args:
            description: 突变描述
            context: 上下文信息
            
        v1.5: 视角优先 - 当视角状态发生剧烈变化时，所有基于旧地图/POI 的任务立即暂停
        """
        self.anomaly_history.append({
            "timestamp": time.time(),
            "anomaly": {
                "type": AnomalyType.ENV_MUTATION,
                "severity": "high",
                "description": description,
                "context": context or {}
            }
        })
    
    def stop(self):
        """停止监控"""
        self.node_start_times.clear()
    
    def get_anomaly_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取异常历史
        
        Args:
            limit: 返回数量限制
            
        Returns:
            异常历史列表
        """
        return self.anomaly_history[-limit:]





