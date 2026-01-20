"""
Restart Recovery Flow

重启恢复流程。

v1.5 设计原则：
- 系统重启/任务终止后，决定是否恢复、如何恢复
- 提供明确的恢复入口和用户提示
"""

from typing import Dict, Any, Optional
import time


class RestartRecoveryFlow:
    """
    重启恢复流程
    
    职责：
    - 系统重启/任务终止后
    - 决定是否恢复、如何恢复
    - 生成用户提示
    """
    
    def __init__(self, task_cache_manager=None):
        """
        初始化恢复流程
        
        Args:
            task_cache_manager: TaskCacheManager 实例（可选，用于加载快照）
        """
        self.task_cache = task_cache_manager
    
    def start(self, last_snapshot: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        系统启动时调用
        
        Args:
            last_snapshot: 上次任务的快照（如果存在）
            
        Returns:
            恢复决策：
            {
                "has_unfinished_task": bool,
                "can_recover": bool,
                "recovery_action": str,
                "user_prompt": str,
                "snapshot_id": str
            }
        """
        if not last_snapshot:
            # 没有快照，正常启动
            return {
                "has_unfinished_task": False,
                "can_recover": False,
                "recovery_action": "normal_start",
                "user_prompt": None,
                "snapshot_id": None
            }
        
        # 检查快照中的任务状态
        task_state = last_snapshot.get("task_state")
        snapshot_id = last_snapshot.get("snapshot_id", "unknown")
        
        # v1.5: 只有非终止状态的任务才需要恢复
        terminal_states = ["completed", "aborted"]
        has_unfinished = task_state not in terminal_states if task_state else False
        
        if not has_unfinished:
            return {
                "has_unfinished_task": False,
                "can_recover": False,
                "recovery_action": "normal_start",
                "user_prompt": None,
                "snapshot_id": snapshot_id
            }
        
        # 判断是否可以恢复
        can_recover = self._can_recover_from_snapshot(last_snapshot)
        
        if can_recover:
            return {
                "has_unfinished_task": True,
                "can_recover": True,
                "recovery_action": "restore_from_snapshot",
                "user_prompt": f"检测到未完成的任务（状态：{task_state}），是否恢复？",
                "snapshot_id": snapshot_id,
                "snapshot": last_snapshot
            }
        else:
            return {
                "has_unfinished_task": True,
                "can_recover": False,
                "recovery_action": "abandon_task",
                "user_prompt": f"检测到未完成的任务（状态：{task_state}），但无法恢复。任务已中止。",
                "snapshot_id": snapshot_id
            }
    
    def _can_recover_from_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """
        判断是否可以从快照恢复
        
        Args:
            snapshot: 任务快照
            
        Returns:
            是否可以恢复
        """
        # v1.5: 简单判断规则
        # 如果快照包含完整的 context 和 node 信息，可以恢复
        if "context" not in snapshot:
            return False
        
        if "node_id" not in snapshot and "current_node" not in snapshot:
            return False
        
        # 检查快照是否过期（例如超过 1 小时）
        snapshot_time = snapshot.get("timestamp", 0)
        if snapshot_time > 0:
            elapsed = time.time() - snapshot_time
            if elapsed > 3600:  # 1 小时
                return False
        
        return True
    
    def recover(self, snapshot: Dict[str, Any], task_chain_manager) -> Dict[str, Any]:
        """
        执行恢复流程
        
        Args:
            snapshot: 任务快照
            task_chain_manager: TaskChainManager 实例
            
        Returns:
            恢复结果：
            {
                "success": bool,
                "restored_state": str,
                "restored_node_id": str,
                "error": Optional[str]
            }
        """
        try:
            # 1. 恢复 TaskContext
            context_data = snapshot.get("context", {})
            task_chain_manager.context.from_dict(context_data)
            
            # 2. 恢复 TaskNode（简化版，实际应该从快照重建 node）
            node_id = snapshot.get("node_id")
            domain = snapshot.get("domain", "unknown")
            
            # v1.5: 这里简化处理，实际应该重建完整的 TaskNode
            # 暂时只恢复 context
            
            return {
                "success": True,
                "restored_state": snapshot.get("task_state", "unknown"),
                "restored_node_id": node_id,
                "restored_context": True,
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "restored_state": None,
                "restored_node_id": None,
                "error": str(e)
            }
    
    def create_snapshot(self, task_chain_manager) -> Dict[str, Any]:
        """
        创建任务快照（用于恢复）
        
        Args:
            task_chain_manager: TaskChainManager 实例
            
        Returns:
            任务快照：
            {
                "timestamp": float,
                "task_state": str,
                "node_id": str,
                "domain": str,
                "context": Dict,
                "snapshot_id": str
            }
        """
        import hashlib
        import json
        
        snapshot_data = {
            "timestamp": time.time(),
            "task_state": task_chain_manager.state.value,
            "node_id": task_chain_manager.current_node.node_id if task_chain_manager.current_node else None,
            "domain": task_chain_manager.current_node.domain if task_chain_manager.current_node else None,
            "context": task_chain_manager.context.to_dict()
        }
        
        snapshot_str = json.dumps(snapshot_data, sort_keys=True)
        snapshot_id = hashlib.md5(snapshot_str.encode()).hexdigest()[:8]
        snapshot_data["snapshot_id"] = snapshot_id
        
        return snapshot_data





