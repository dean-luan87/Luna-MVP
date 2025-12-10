# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - TaskChainManager 实现

任务链管理器，支持主任务 + 子任务栈 + 恢复机制。
"""

import time
from typing import List, Dict, Optional, Any
from core.decision_output import DecisionOutput
from core.decision_actions import DecisionAction
from core.task_result import TaskResult


class TaskChainManager:
    """
    任务链管理器
    
    支持：
    - 主任务（Main Task）
    - 子任务栈（Sub Task Stack）
    - 自动恢复主任务
    - 任务替换
    """
    
    def __init__(self):
        """初始化任务链管理器"""
        self.main_task: Optional[Dict] = None
        self.sub_task_stack: List[Dict] = []
        self.active_task: Optional[Dict] = None
        self.active_node: Optional[Dict] = None
        self.main_task_state: Optional[Dict] = None
    
    def start_main_task(self, task_spec: Dict) -> None:
        """
        启动主任务
        
        Args:
            task_spec: 任务规格字典
        """
        self.main_task = task_spec
        self.active_task = task_spec
        self.main_task_state = None
        
        # 初始化第一个节点
        if task_spec.get("nodes") and len(task_spec["nodes"]) > 0:
            self.active_node = task_spec["nodes"][0]
        else:
            self.active_node = None
    
    def advance(self) -> None:
        """
        推进到下一节点
        
        将当前活动任务的 active_node 推进到下一个节点。
        如果已经是最后一个节点，则 active_node 设为 None。
        """
        if not self.active_task or not self.active_task.get("nodes"):
            return
        
        nodes = self.active_task["nodes"]
        if not self.active_node:
            # 如果没有当前节点，设置为第一个节点
            if len(nodes) > 0:
                self.active_node = nodes[0]
            return
        
        # 查找当前节点在列表中的位置
        current_index = -1
        for i, node in enumerate(nodes):
            if node.get("id") == self.active_node.get("id"):
                current_index = i
                break
        
        # 推进到下一个节点
        if current_index >= 0 and current_index + 1 < len(nodes):
            self.active_node = nodes[current_index + 1]
        else:
            # 已经是最后一个节点，任务完成
            self.active_node = None
    
    def complete_active_node(self) -> TaskResult:
        """
        完成当前节点
        
        Returns:
            TaskResult: 任务结果
        """
        if not self.active_task:
            return TaskResult(
                status="failed",
                reason="no_active_task",
                task_id="",
                task_type=""
            )
        
        # 检查是否所有节点都已完成
        if not self.active_node:
            # 所有节点已完成，任务完成
            return TaskResult(
                status="ok",
                reason="all_nodes_completed",
                task_id=self.active_task.get("task_id", ""),
                task_type=self.active_task.get("type", "")
            )
        
        # 节点完成，推进到下一个节点
        self.advance()
        
        return TaskResult(
            status="ok",
            reason="node_completed",
            task_id=self.active_task.get("task_id", ""),
            task_type=self.active_task.get("type", "")
        )
    
    def insert_task(self, task_spec: Dict, resume_strategy: str = "auto") -> Dict[str, Any]:
        """
        插入子任务
        
        保存当前主任务状态，将子任务压入栈，并切换活动任务。
        
        Args:
            task_spec: 子任务规格
            resume_strategy: 恢复策略，"auto" 或 "ask"
        
        Returns:
            Dict: 操作结果
        """
        # 1. 如果当前是主任务，保存主任务状态
        if self.main_task and self.active_task == self.main_task:
            self.main_task_state = {
                "task": self.main_task,
                "node": self.active_node,
                "timestamp": time.time()
            }
        
        # 2. 将子任务压入栈
        self.sub_task_stack.append({
            "task": task_spec,
            "resume_strategy": resume_strategy
        })
        
        # 3. 切换活动任务
        self.active_task = task_spec
        
        # 4. 初始化子任务的第一个节点
        if task_spec.get("nodes") and len(task_spec["nodes"]) > 0:
            self.active_node = task_spec["nodes"][0]
        else:
            self.active_node = None
        
        return {"status": "ok", "task": task_spec}
    
    def _replace_task(self, new_task_spec: Dict) -> Dict[str, Any]:
        """
        替换任务（内部方法）
        
        清空子任务栈，替换主任务，重置状态。
        
        Args:
            new_task_spec: 新任务规格
        
        Returns:
            Dict: 操作结果
        """
        # 1. 清空子任务栈
        self.sub_task_stack.clear()
        
        # 2. 替换主任务
        self.main_task = new_task_spec
        self.active_task = new_task_spec
        self.main_task_state = None
        
        # 3. 重置节点
        if new_task_spec.get("nodes") and len(new_task_spec["nodes"]) > 0:
            self.active_node = new_task_spec["nodes"][0]
        else:
            self.active_node = None
        
        return {"status": "replaced", "task": new_task_spec}
    
    def replace_task(self, old_task_id: str, new_task_spec: Dict) -> Dict[str, Any]:
        """
        替换任务（公开方法，兼容测试）
        
        Args:
            old_task_id: 旧任务 ID（用于验证）
            new_task_spec: 新任务规格
        
        Returns:
            Dict: 操作结果
        """
        return self._replace_task(new_task_spec)
    
    def complete_active_task(self) -> Dict[str, Any]:
        """
        完成当前活动任务
        
        如果当前是子任务，从栈中弹出。
        如果栈中还有其他子任务，切换到栈顶的子任务。
        如果栈为空，根据恢复策略恢复主任务或询问用户。
        如果当前是主任务，返回主任务完成状态。
        
        Returns:
            Dict: 操作结果
        """
        if not self.sub_task_stack:
            # 没有子任务栈，说明当前是主任务
            return {
                "status": "main_task_complete",
                "task": self.main_task
            }
        
        # 弹出完成的子任务
        finished = self.sub_task_stack.pop()
        
        # 如果栈中还有其他子任务，切换到栈顶的子任务
        if self.sub_task_stack:
            # 切换到栈顶的子任务
            next_task = self.sub_task_stack[-1]["task"]
            self.active_task = next_task
            
            # 初始化子任务的第一个节点
            if next_task.get("nodes") and len(next_task["nodes"]) > 0:
                self.active_node = next_task["nodes"][0]
            else:
                self.active_node = None
            
            return {
                "status": "switched_to_subtask",
                "task": next_task
            }
        
        # 栈为空，需要恢复主任务
        if finished["resume_strategy"] == "auto":
            # 自动恢复主任务
            return self.resume_main_task()
        elif finished["resume_strategy"] == "ask":
            # 询问用户是否恢复
            return {
                "action": "ASK_USER",
                "question": "是否继续之前的任务？",
                "resume_context": self.main_task_state
            }
        else:
            # 未知策略，默认恢复
            return self.resume_main_task()
    
    def resume_main_task(self) -> Dict[str, Any]:
        """
        恢复主任务
        
        从 main_task_state 恢复主任务状态。
        
        Returns:
            Dict: 操作结果
        """
        if not self.main_task:
            return {
                "status": "error",
                "reason": "no_main_task"
            }
        
        if not self.main_task_state:
            return {
                "status": "error",
                "reason": "no_main_task_state"
            }
        
        # 恢复主任务状态
        self.active_task = self.main_task
        self.active_node = self.main_task_state.get("node")
        
        # 可选：清理状态（保留以便调试）
        # self.main_task_state = None
        
        return {
            "status": "resumed",
            "task": self.main_task,
            "node": self.active_node
        }
    
    def apply_decision(self, decision_output: DecisionOutput) -> None:
        """
        应用决策输出
        
        根据 DecisionOutput 的 action 执行相应的操作。
        
        Args:
            decision_output: 决策输出
        """
        if decision_output.action == DecisionAction.CONTINUE_TASK:
            self.advance()
        elif decision_output.action == DecisionAction.INSERT_TASK:
            insert_task_spec = decision_output.params.get("insert_task_spec")
            if insert_task_spec:
                resume_strategy = decision_output.params.get("resume_strategy", "auto")
                self.insert_task(insert_task_spec, resume_strategy)
        elif decision_output.action == DecisionAction.REPLACE_TASK:
            new_task_spec = decision_output.params.get("new_task_spec")
            if new_task_spec:
                self._replace_task(new_task_spec)
        elif decision_output.action == DecisionAction.RESUME_MAIN_TASK:
            self.resume_main_task()
        # ASK_USER / TRIGGER_PLANB / NO_OP 由上层处理
    
    def pause_for_planb(self) -> Dict[str, Any]:
        """
        为 PlanB 暂停任务链
        
        保存当前状态，用于 PlanB 降级后恢复。
        
        Returns:
            Dict: 暂停状态快照
        """
        return {
            "status": "paused",
            "active_task_state": {
                "task": self.active_task,
                "node": self.active_node
            },
            "sub_task_stack": self.sub_task_stack.copy(),
            "main_task_state": self.main_task_state
        }
    
    def get_active_task(self) -> Optional[Dict]:
        """
        获取当前活动任务
        
        Returns:
            Optional[Dict]: 当前活动任务，如果没有则返回 None
        """
        return self.active_task
    
    def is_main_task_active(self) -> bool:
        """
        判断主任务是否活动
        
        Returns:
            bool: 如果当前活动任务是主任务，返回 True
        """
        return self.main_task is not None and self.active_task == self.main_task

