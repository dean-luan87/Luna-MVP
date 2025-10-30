#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务引擎入口模块
调度任务图、加载执行器、控制状态、执行节点
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# 导入模块
from .task_graph_loader import TaskGraph, get_graph_loader, TaskGraphLoader
from .task_node_executor import TaskNodeExecutor
from .task_state_manager import TaskStateManager
from .task_cache_manager import TaskCacheManager
from .inserted_task_queue import InsertedTaskQueue
from .task_cleanup import TaskCleanup
from .task_report_uploader import get_report_uploader

class TaskStatus:
    """任务状态（与枚举兼容）"""
    IDLE = "idle"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

class TaskEngine:
    """任务引擎核心类"""
    
    def __init__(self):
        """初始化任务引擎"""
        self.active_tasks: Dict[str, TaskGraph] = {}      # 活动任务
        self.completed_tasks: Dict[str, TaskGraph] = {}   # 已完成任务
        self.task_states: Dict[str, TaskStatus] = {}      # 任务状态
        self.task_progress: Dict[str, int] = {}           # 任务进度
        
        self.lock = threading.Lock()
        self.logger = logging.getLogger("TaskEngine")
        
        # 初始化各个模块
        self.graph_loader = get_graph_loader("task_graphs")
        self.state_manager = TaskStateManager()
        self.node_executor = TaskNodeExecutor()
        self.cache_manager = TaskCacheManager()
        self.inserted_queue = InsertedTaskQueue()
        self.cleanup = TaskCleanup(self)
        self.report_uploader = get_report_uploader()
        
        # 启动清理线程
        self.cleanup.start()
        
        self.logger.info("🚀 TaskEngine初始化完成")
    
    def load_task_graph(self, graph_file: str) -> TaskGraph:
        """
        加载任务图
        
        Args:
            graph_file: 任务图JSON文件路径
            
        Returns:
            TaskGraph: 任务图对象
        """
        return self.graph_loader.load_from_file(graph_file)
    
    def register_task(self, task_graph: TaskGraph) -> str:
        """
        注册任务链
        
        Args:
            task_graph: 任务图对象
            
        Returns:
            str: 任务ID
        """
        with self.lock:
            # 检查主任务数量限制
            if self._is_main_task(task_graph.graph_id) and self._count_main_tasks() >= 1:
                self.logger.warning("⚠️ 主任务已存在，无法注册新的主任务")
                raise ValueError("已有一个活跃的主任务")
            
            # 检查插入任务数量限制
            if self._is_inserted_task(task_graph.graph_id) and self._count_inserted_tasks() >= 2:
                self.logger.warning("⚠️ 插入任务数量已达上限(2个)")
                raise ValueError("插入任务数量已达上限")
            
            self.active_tasks[task_graph.graph_id] = task_graph
            self.task_states[task_graph.graph_id] = TaskStatus.IDLE
            self.task_progress[task_graph.graph_id] = 0
            
            self.logger.info(f"✅ 任务注册成功: {task_graph.graph_id}")
            return task_graph.graph_id
    
    def start_task(self, graph_id: str) -> bool:
        """
        启动任务
        
        Args:
            graph_id: 任务ID
            
        Returns:
            bool: 是否成功启动
        """
        with self.lock:
            if graph_id not in self.active_tasks:
                self.logger.error(f"❌ 任务不存在: {graph_id}")
                return False
            
            self.task_states[graph_id] = TaskStatus.ACTIVE
            self.logger.info(f"🚀 任务启动: {graph_id}")
            
            # 调用状态管理器
            self.state_manager.task_started(graph_id)
            
            # 开始执行任务
            self._execute_task(graph_id)
            
            return True
    
    def pause_task(self, graph_id: str) -> bool:
        """暂停任务"""
        with self.lock:
            if graph_id not in self.active_tasks:
                return False
            
            if self.task_states[graph_id] != TaskStatus.ACTIVE:
                return False
            
            self.task_states[graph_id] = TaskStatus.PAUSED
            self.state_manager.task_paused(graph_id)
            
            self.logger.info(f"⏸️ 任务暂停: {graph_id}")
            return True
    
    def resume_task(self, graph_id: str) -> bool:
        """恢复任务"""
        with self.lock:
            if graph_id not in self.active_tasks:
                return False
            
            if self.task_states[graph_id] != TaskStatus.PAUSED:
                return False
            
            self.task_states[graph_id] = TaskStatus.ACTIVE
            self.state_manager.task_resumed(graph_id)
            
            # 继续执行
            self._execute_task(graph_id)
            
            self.logger.info(f"▶️ 任务恢复: {graph_id}")
            return True
    
    def complete_task(self, graph_id: str) -> bool:
        """完成任务"""
        with self.lock:
            if graph_id not in self.active_tasks:
                return False
            
            task_graph = self.active_tasks.pop(graph_id)
            self.task_states[graph_id] = TaskStatus.COMPLETED
            self.completed_tasks[graph_id] = task_graph
            
            self.state_manager.task_completed(graph_id)
            
            # 生成并上传执行报告
            self._upload_task_report(graph_id, task_graph)
            
            self.logger.info(f"✅ 任务完成: {graph_id}")
            
            # 触发清理（延迟释放）
            self.cleanup.schedule_cleanup(graph_id)
            
            return True
    
    def cancel_task(self, graph_id: str) -> bool:
        """取消任务"""
        with self.lock:
            if graph_id not in self.active_tasks:
                return False
            
            self.active_tasks.pop(graph_id)
            self.task_states[graph_id] = TaskStatus.CANCELLED
            self.state_manager.task_cancelled(graph_id)
            
            self.logger.info(f"❌ 任务取消: {graph_id}")
            
            # 立即清理
            self.cleanup.immediate_cleanup(graph_id)
            
            return True
    
    def get_task_status(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        with self.lock:
            if graph_id not in self.active_tasks and graph_id not in self.completed_tasks:
                return None
            
            task_graph = self.active_tasks.get(graph_id) or self.completed_tasks.get(graph_id)
            state = self.task_states.get(graph_id, TaskStatus.IDLE)
            progress = self.task_progress.get(graph_id, 0)
            
            return {
                "graph_id": graph_id,
                "name": task_graph.name or task_graph.goal if task_graph else "Unknown",
                "status": state if isinstance(state, str) else str(state),
                "progress": progress,
                "current_node": self.state_manager.get_current_node(graph_id),
                "metadata": task_graph.metadata if task_graph else {}
            }
    
    def list_active_tasks(self) -> List[Dict[str, Any]]:
        """列出活动任务"""
        with self.lock:
            return [
                self.get_task_status(graph_id)
                for graph_id in self.active_tasks.keys()
            ]
    
    def insert_task(self, graph_id: str, inserted_graph: TaskGraph, return_point: str = None) -> bool:
        """
        插入任务
        
        Args:
            graph_id: 当前任务ID
            inserted_graph: 插入的任务图
            return_point: 返回点
            
        Returns:
            bool: 是否成功插入
        """
        try:
            # 暂停当前任务
            self.pause_task(graph_id)
            
            # 注册插入任务
            inserted_id = self.register_task(inserted_graph)
            
            # 记录插入关系
            self.inserted_queue.add_inserted_task(graph_id, inserted_id, return_point)
            
            # 启动插入任务
            self.start_task(inserted_id)
            
            self.logger.info(f"💉 插入任务成功: {inserted_id} -> {graph_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 插入任务失败: {e}")
            return False
    
    def _execute_task(self, graph_id: str):
        """执行任务（异步）"""
        def execute():
            try:
                task_graph = self.active_tasks[graph_id]
                
                # 执行每个节点
                for i, node in enumerate(task_graph.nodes):
                    if self.task_states[graph_id] != TaskStatus.ACTIVE:
                        break
                    
                    # 更新当前节点
                    node_id = node.get("id", f"node_{i}")
                    self.state_manager.update_current_node(graph_id, node_id)
                    
                    # 执行节点
                    result = self.node_executor.execute(node, self.state_manager.get_context(graph_id))
                    
                    # 更新进度
                    progress = int((i + 1) / len(task_graph.nodes) * 100)
                    self.task_progress[graph_id] = progress
                    self.state_manager.update_progress(graph_id, progress)
                    
                    # 记录上下文
                    self.state_manager.update_context(graph_id, result)
                    
                    # 检查节点执行结果
                    if not result.get("success", True):
                        # 节点执行失败
                        self.logger.warning(f"⚠️ 节点执行失败: {node_id}")
                        # 可以选择继续或中止任务
                    
                    self.logger.info(f"📝 节点执行完成: {node_id}")
                
                # 任务完成
                if self.task_states[graph_id] == TaskStatus.ACTIVE:
                    self.complete_task(graph_id)
                    
                    # 检查是否有需要恢复的插入任务
                    self._handle_inserted_task_return(graph_id)
                    
            except Exception as e:
                self.logger.error(f"❌ 任务执行失败: {e}")
                self.task_states[graph_id] = TaskStatus.FAILED
        
        # 在新线程中执行
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
    
    def _handle_inserted_task_return(self, inserted_graph_id: str):
        """处理插入任务返回"""
        parent_id = self.inserted_queue.get_parent_task(inserted_graph_id)
        if parent_id:
            # 恢复父任务
            self.resume_task(parent_id)
            self.logger.info(f"🔄 返回主任务: {parent_id}")
    
    def _is_main_task(self, graph_id: str) -> bool:
        """判断是否为主任务"""
        return not graph_id.startswith("inserted_")
    
    def _is_inserted_task(self, graph_id: str) -> bool:
        """判断是否为插入任务"""
        return graph_id.startswith("inserted_")
    
    def _upload_task_report(self, graph_id: str, task_graph: TaskGraph):
        """
        上传任务执行报告
        
        Args:
            graph_id: 任务ID
            task_graph: 任务图对象
        """
        try:
            task_state = self.state_manager.get_state(graph_id)
            if not task_state:
                return
            
            # 计算执行时长
            duration = 0
            if task_state.started_at:
                end_time = task_state.completed_at or time.time()
                duration = int(end_time - task_state.started_at)
            
            # 获取执行路径
            execution_path = task_state.context.get("execution_path", self.state_manager.get_context(graph_id).get("execution_path", []))
            if not execution_path and task_state.current_node:
                execution_path = [task_state.current_node]
            
            # 收集失败节点
            failed_nodes = []
            for node in task_graph.nodes:
                node_id = node.get("id")
                node_result = self.state_manager.get_context(graph_id).get(f"node_{node_id}_result")
                if node_result and not node_result.get("success", True):
                    failed_nodes.append(node_id)
            
            # 构建报告数据
            report_data = {
                "task_id": graph_id,
                "user_id": "default_user",  # 可从配置或用户管理器获取
                "graph_name": task_graph.goal or task_graph.graph_id,
                "scene": task_graph.scene,
                "execution_path": execution_path,
                "failed_nodes": failed_nodes,
                "corrections": task_state.context.get("corrections", []),
                "duration": duration,
                "status": self.task_states.get(graph_id, TaskStatus.COMPLETED),
                "progress": self.task_progress.get(graph_id, 100),
                "nodes_total": len(task_graph.nodes),
                "nodes_completed": len(execution_path)
            }
            
            # 上传报告
            self.report_uploader.upload_task_report(report_data)
            
        except Exception as e:
            self.logger.error(f"❌ 上传任务报告失败: {e}")
    
    def _count_main_tasks(self) -> int:
        """统计主任务数量"""
        return sum(1 for gid in self.active_tasks.keys() if self._is_main_task(gid))
    
    def _count_inserted_tasks(self) -> int:
        """统计插入任务数量"""
        return sum(1 for gid in self.active_tasks.keys() if self._is_inserted_task(gid))
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        return {
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "main_tasks": self._count_main_tasks(),
            "inserted_tasks": self._count_inserted_tasks(),
            "cache_usage": self.cache_manager.get_usage()
        }


# 全局任务引擎实例
_global_task_engine: Optional[TaskEngine] = None

def get_task_engine() -> TaskEngine:
    """获取全局任务引擎实例"""
    global _global_task_engine
    if _global_task_engine is None:
        _global_task_engine = TaskEngine()
    return _global_task_engine


if __name__ == "__main__":
    # 测试任务引擎
    print("🚀 TaskEngine测试")
    print("=" * 60)
    
    engine = get_task_engine()
    
    # 测试1: 加载任务图
    print("\n1. 加载任务图...")
    try:
        graph = engine.load_task_graph("task_graphs/hospital_visit.json")
        print(f"   ✅ 任务图加载成功: {graph.graph_id}")
    except FileNotFoundError:
        print("   ⚠️ 任务图文件不存在，跳过测试")
    
    print("\n2. 任务状态检查...")
    info = engine.get_cache_info()
    print(f"   📊 {info}")
    
    print("\n🎉 TaskEngine测试完成！")
