#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务状态管理器
统一管理任务图中所有节点的执行状态、任务整体状态、插入任务记录与恢复点信息
"""

import logging
import time
import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class NodeState:
    """节点状态"""
    node_id: str
    status: str = "pending"  # pending, running, complete, failed, skipped
    output: Optional[Dict[str, Any]] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if self.output is None:
            self.output = {}


@dataclass
class InsertedTaskInfo:
    """插入任务信息"""
    is_active: bool = False
    paused_main_node: Optional[str] = None
    inserted_task_id: Optional[str] = None
    pause_time: Optional[str] = None


@dataclass
class TaskState:
    """任务状态"""
    task_id: str
    graph_status: str = "pending"  # pending, running, complete, paused, error
    current_node_id: Optional[str] = None
    nodes: Dict[str, NodeState] = None
    inserted_task: InsertedTaskInfo = None
    progress: int = 0
    started_at: Optional[float] = None
    paused_at: Optional[float] = None
    completed_at: Optional[float] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = {}
        if self.inserted_task is None:
            self.inserted_task = InsertedTaskInfo()
        if self.context is None:
            self.context = {}


class TaskStateManager:
    """任务状态管理器"""
    
    def __init__(self, storage_dir: str = "data/task_states"):
        """
        初始化状态管理器
        
        Args:
            storage_dir: 状态文件存储目录
        """
        self.task_states: Dict[str, TaskState] = {}
        self.storage_dir = storage_dir
        self.logger = logging.getLogger("TaskStateManager")
        
        # 确保存储目录存在
        os.makedirs(storage_dir, exist_ok=True)
    
    def init_task_state(self, task_id: str, node_ids: List[str]) -> None:
        """
        初始化任务状态
        
        Args:
            task_id: 任务ID
            node_ids: 所有节点ID列表
        """
        if task_id not in self.task_states:
            self.task_states[task_id] = TaskState(task_id=task_id)
        
        task_state = self.task_states[task_id]
        task_state.graph_status = "pending"
        task_state.started_at = time.time()
        
        # 初始化所有节点状态
        for node_id in node_ids:
            task_state.nodes[node_id] = NodeState(node_id=node_id, status="pending")
        
        self.logger.info(f"🎬 任务状态初始化: {task_id} ({len(node_ids)}个节点)")
    
    def update_node_status(self, task_id: str, node_id: str, status: str, 
                           output: Optional[Dict[str, Any]] = None) -> None:
        """
        更新节点状态
        
        Args:
            task_id: 任务ID
            node_id: 节点ID
            status: 新状态（pending/running/complete/failed/skipped）
            output: 节点输出数据（可选）
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return
        
        task_state = self.task_states[task_id]
        
        if node_id not in task_state.nodes:
            task_state.nodes[node_id] = NodeState(node_id=node_id)
        
        node_state = task_state.nodes[node_id]
        node_state.status = status
        node_state.timestamp = datetime.now().isoformat()
        
        if output is not None:
            node_state.output = output
        
        # 更新任务整体状态
        if status == "running":
            task_state.graph_status = "running"
            task_state.current_node_id = node_id
        elif status == "complete":
            # 检查是否所有节点都完成
            if all(n.status in ["complete", "skipped"] for n in task_state.nodes.values()):
                task_state.graph_status = "complete"
                task_state.completed_at = time.time()
        elif status == "failed":
            task_state.graph_status = "error"
        
        # 更新进度
        completed_count = sum(1 for n in task_state.nodes.values() 
                            if n.status == "complete")
        total_count = len(task_state.nodes)
        if total_count > 0:
            task_state.progress = int((completed_count / total_count) * 100)
        
        self.logger.debug(f"📊 节点状态更新: {task_id}.{node_id} -> {status}")
    
    def get_node_status(self, task_id: str, node_id: str) -> Optional[str]:
        """
        查询节点状态
        
        Args:
            task_id: 任务ID
            node_id: 节点ID
            
        Returns:
            节点状态，如果不存在返回None
        """
        if task_id not in self.task_states:
            return None
        
        task_state = self.task_states[task_id]
        if node_id not in task_state.nodes:
            return None
        
        return task_state.nodes[node_id].status
    
    def record_node_output(self, task_id: str, node_id: str, output: Dict[str, Any]) -> None:
        """
        写入节点输出数据
        
        Args:
            task_id: 任务ID
            node_id: 节点ID
            output: 输出数据
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return
        
        task_state = self.task_states[task_id]
        
        if node_id not in task_state.nodes:
            task_state.nodes[node_id] = NodeState(node_id=node_id)
        
        task_state.nodes[node_id].output = output
        self.logger.debug(f"💾 记录节点输出: {task_id}.{node_id}")
    
    def get_node_output(self, task_id: str, node_id: str) -> Optional[Dict[str, Any]]:
        """
        获取节点输出数据
        
        Args:
            task_id: 任务ID
            node_id: 节点ID
            
        Returns:
            节点输出数据，如果不存在返回None
        """
        if task_id not in self.task_states:
            return None
        
        task_state = self.task_states[task_id]
        if node_id not in task_state.nodes:
            return None
        
        return task_state.nodes[node_id].output
    
    def set_task_status(self, task_id: str, status: str) -> None:
        """
        设置任务整体状态
        
        Args:
            task_id: 任务ID
            status: 状态（pending/running/complete/paused/error）
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return
        
        self.task_states[task_id].graph_status = status
        
        if status == "paused":
            self.task_states[task_id].paused_at = time.time()
        elif status == "complete":
            self.task_states[task_id].completed_at = time.time()
        
        self.logger.info(f"📊 任务状态更新: {task_id} -> {status}")
    
    def get_task_status(self, task_id: str) -> Optional[str]:
        """
        获取任务整体状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态，如果不存在返回None
        """
        if task_id not in self.task_states:
            return None
        
        return self.task_states[task_id].graph_status
    
    def pause_for_inserted_task(self, task_id: str, inserted_task_id: str, 
                                current_node: str) -> str:
        """
        暂停当前任务以执行插入任务
        
        Args:
            task_id: 主任务ID
            inserted_task_id: 插入任务ID
            current_node: 当前节点ID
            
        Returns:
            恢复点（当前节点ID）
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return current_node
        
        task_state = self.task_states[task_id]
        
        # 暂停主任务
        task_state.graph_status = "paused"
        task_state.paused_at = time.time()
        
        # 记录插入任务信息
        task_state.inserted_task.is_active = True
        task_state.inserted_task.paused_main_node = current_node
        task_state.inserted_task.inserted_task_id = inserted_task_id
        task_state.inserted_task.pause_time = datetime.now().isoformat()
        
        self.logger.info(f"⏸️ 主任务暂停: {task_id} (节点: {current_node}), 插入任务: {inserted_task_id}")
        
        return current_node
    
    def resume_from_inserted_task(self, task_id: str) -> Optional[str]:
        """
        插入任务结束后恢复主任务
        
        Args:
            task_id: 主任务ID
            
        Returns:
            恢复点（节点ID），如果不存在返回None
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return None
        
        task_state = self.task_states[task_id]
        inserted_info = task_state.inserted_task
        
        if not inserted_info.is_active:
            self.logger.warning(f"⚠️ 没有活跃的插入任务: {task_id}")
            return None
        
        # 恢复主任务
        resume_point = inserted_info.paused_main_node
        
        # 清除插入任务信息
        inserted_info.is_active = False
        inserted_info.paused_main_node = None
        inserted_info.inserted_task_id = None
        
        # 恢复任务状态
        task_state.graph_status = "running"
        task_state.paused_at = None
        
        self.logger.info(f"▶️ 主任务恢复: {task_id} (节点: {resume_point})")
        
        return resume_point
    
    def persist_state_to_file(self, task_id: str) -> str:
        """
        持久化任务状态到文件
        
        Args:
            task_id: 任务ID
            
        Returns:
            文件路径
        """
        if task_id not in self.task_states:
            self.logger.warning(f"⚠️ 任务状态不存在: {task_id}")
            return ""
        
        task_state = self.task_states[task_id]
        
        # 转换为可序列化的字典
        state_dict = {
            "task_id": task_state.task_id,
            "graph_status": task_state.graph_status,
            "current_node_id": task_state.current_node_id,
            "nodes": {
                node_id: asdict(node_state)
                for node_id, node_state in task_state.nodes.items()
            },
            "inserted_task": asdict(task_state.inserted_task),
            "progress": task_state.progress,
            "started_at": task_state.started_at,
            "paused_at": task_state.paused_at,
            "completed_at": task_state.completed_at,
            "context": task_state.context,
            "timestamp": datetime.now().isoformat()
        }
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        filename = f"{task_id}_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        # 保存到文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state_dict, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 状态已持久化: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ 状态持久化失败: {e}")
            return ""
    
    def load_state_from_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        从文件加载任务状态
        
        Args:
            filepath: 文件路径
            
        Returns:
            任务状态字典，如果加载失败返回None
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state_dict = json.load(f)
            
            task_id = state_dict.get("task_id")
            if not task_id:
                self.logger.error("状态文件缺少task_id字段")
                return None
            
            # 恢复任务状态
            task_state = TaskState(task_id=task_id)
            task_state.graph_status = state_dict.get("graph_status", "pending")
            task_state.current_node_id = state_dict.get("current_node_id")
            task_state.progress = state_dict.get("progress", 0)
            task_state.started_at = state_dict.get("started_at")
            task_state.paused_at = state_dict.get("paused_at")
            task_state.completed_at = state_dict.get("completed_at")
            task_state.context = state_dict.get("context", {})
            
            # 恢复节点状态
            for node_id, node_data in state_dict.get("nodes", {}).items():
                node_state = NodeState(
                    node_id=node_data.get("node_id", node_id),
                    status=node_data.get("status", "pending"),
                    output=node_data.get("output"),
                    timestamp=node_data.get("timestamp", "")
                )
                task_state.nodes[node_id] = node_state
            
            # 恢复插入任务信息
            inserted_data = state_dict.get("inserted_task", {})
            task_state.inserted_task = InsertedTaskInfo(
                is_active=inserted_data.get("is_active", False),
                paused_main_node=inserted_data.get("paused_main_node"),
                inserted_task_id=inserted_data.get("inserted_task_id"),
                pause_time=inserted_data.get("pause_time")
            )
            
            self.task_states[task_id] = task_state
            self.logger.info(f"✅ 状态已加载: {filepath}")
            
            return state_dict
            
        except Exception as e:
            self.logger.error(f"❌ 状态加载失败: {filepath}: {e}")
            return None
    
    def get_state_summary(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务状态摘要（用于日志上报）
        
        Args:
            task_id: 任务ID
            
        Returns:
            状态摘要字典
        """
        if task_id not in self.task_states:
            return {}
        
        task_state = self.task_states[task_id]
        
        # 统计已完成和失败的节点
        completed_nodes = [node_id for node_id, node_state in task_state.nodes.items()
                          if node_state.status == "complete"]
        failed_nodes = [node_id for node_id, node_state in task_state.nodes.items()
                       if node_state.status == "failed"]
        
        return {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "graph_status": task_state.graph_status,
            "completed_nodes": completed_nodes,
            "failed_nodes": failed_nodes,
            "current_node": task_state.current_node_id,
            "inserted_task_active": task_state.inserted_task.is_active,
            "progress": task_state.progress,
            "nodes_total": len(task_state.nodes)
        }
    
    # ========== 向后兼容方法 ==========
    
    def update_current_node(self, task_id: str, node_id: str):
        """向后兼容：更新当前节点"""
        self.update_node_status(task_id, node_id, "running")
    
    def task_started(self, task_id: str):
        """向后兼容：任务开始"""
        if task_id in self.task_states:
            self.task_states[task_id].started_at = time.time()
    
    def task_paused(self, task_id: str):
        """向后兼容：任务暂停"""
        self.set_task_status(task_id, "paused")
    
    def task_resumed(self, task_id: str):
        """向后兼容：任务恢复"""
        self.set_task_status(task_id, "running")
    
    def task_completed(self, task_id: str):
        """向后兼容：任务完成"""
        self.set_task_status(task_id, "complete")
    
    def task_cancelled(self, task_id: str):
        """向后兼容：任务取消"""
        self.set_task_status(task_id, "error")
    
    def update_progress(self, task_id: str, progress: int):
        """向后兼容：更新进度"""
        if task_id in self.task_states:
            self.task_states[task_id].progress = progress
    
    def update_context(self, task_id: str, data: Dict[str, Any]):
        """向后兼容：更新上下文"""
        if task_id in self.task_states:
            self.task_states[task_id].context.update(data)
    
    def get_context(self, task_id: str) -> Dict[str, Any]:
        """向后兼容：获取上下文"""
        if task_id in self.task_states:
            return self.task_states[task_id].context
        return {}
    
    def get_current_node(self, task_id: str) -> Optional[str]:
        """向后兼容：获取当前节点"""
        if task_id in self.task_states:
            return self.task_states[task_id].current_node_id
        return None
    
    def get_state(self, task_id: str) -> Optional[TaskState]:
        """向后兼容：获取任务状态对象"""
        return self.task_states.get(task_id)
    
    def remove_state(self, task_id: str):
        """向后兼容：移除任务状态"""
        if task_id in self.task_states:
            del self.task_states[task_id]
    
    def save_all_to_directory(self, directory: Optional[str] = None):
        """向后兼容：保存所有状态到目录"""
        if directory is None:
            directory = self.storage_dir
        
        for task_id in self.task_states:
            self.persist_state_to_file(task_id)
    
    def load_all_from_directory(self, directory: Optional[str] = None):
        """向后兼容：从目录加载所有状态"""
        if directory is None:
            directory = self.storage_dir
        
        if not os.path.exists(directory):
            return
        
        count = 0
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                if self.load_state_from_file(filepath):
                    count += 1
        
        self.logger.info(f"✅ 从 {directory} 加载了 {count} 个任务状态")


if __name__ == "__main__":
    # 测试状态管理器
    print("📊 TaskStateManager测试")
    print("=" * 60)
    
    manager = TaskStateManager()
    
    # 测试1: 初始化任务状态
    print("\n1. 初始化任务状态...")
    node_ids = ["plan_route", "goto_department", "wait_for_call"]
    manager.init_task_state("test_task", node_ids)
    print(f"   ✅ 初始化了3个节点")
    
    # 测试2: 更新节点状态
    print("\n2. 更新节点状态...")
    manager.update_node_status("test_task", "plan_route", "running")
    manager.update_node_status("test_task", "plan_route", "complete", 
                               {"destination": "虹口医院", "eta": "30min"})
    print(f"   ✅ 节点状态已更新")
    
    # 测试3: 查询节点状态
    print("\n3. 查询节点状态...")
    status = manager.get_node_status("test_task", "plan_route")
    print(f"   节点状态: {status}")
    
    # 测试4: 暂停和恢复
    print("\n4. 测试插入任务...")
    pause_point = manager.pause_for_inserted_task("test_task", "toilet_task", "goto_department")
    print(f"   暂停点: {pause_point}")
    
    resume_point = manager.resume_from_inserted_task("test_task")
    print(f"   恢复点: {resume_point}")
    
    # 测试5: 持久化
    print("\n5. 持久化状态...")
    filepath = manager.persist_state_to_file("test_task")
    print(f"   文件路径: {filepath}")
    
    # 测试6: 加载状态
    print("\n6. 加载状态...")
    loaded = manager.load_state_from_file(filepath)
    print(f"   加载成功: {loaded is not None}")
    
    # 测试7: 获取状态摘要
    print("\n7. 获取状态摘要...")
    summary = manager.get_state_summary("test_task")
    print(f"   摘要: {summary}")
    
    print("\n🎉 TaskStateManager测试完成！")