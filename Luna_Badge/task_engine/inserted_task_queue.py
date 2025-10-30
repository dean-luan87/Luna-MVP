#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 插入任务管理器
管理主任务执行过程中的插入任务（如厕所、购物、接电话），确保插入任务执行完毕后恢复主任务
"""

import logging
import time
from typing import Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class InsertedTaskInfo:
    """插入任务信息"""
    parent_id: str                          # 主任务ID
    inserted_id: str                        # 插入任务ID
    resume_node_id: str                    # 主任务恢复点
    started_at: str                         # 开始时间
    status: str = "active"                  # active, completed, cancelled
    timeout: Optional[int] = 300            # 超时时间（秒）
    metadata: Dict[str, Any] = None         # 元数据
    
    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}


class InsertedTaskQueue:
    """插入任务管理器"""
    
    def __init__(self, state_manager=None):
        """
        初始化插入任务队列
        
        Args:
            state_manager: 状态管理器实例（可选）
        """
        self.active_tasks: Dict[str, InsertedTaskInfo] = {}  # inserted_id -> info
        self.state_manager = state_manager
        self.logger = logging.getLogger("InsertedTaskQueue")
        
        # 嵌套保护
        self.max_nesting_level = 1  # 不支持嵌套
        
        self.logger.info("🚀 InsertedTaskQueue 初始化完成")
    
    def register_inserted_task(self, parent_id: str, inserted_id: str, 
                               resume_node_id: str, timeout: int = 300) -> bool:
        """
        注册插入任务，并暂停主任务
        
        Args:
            parent_id: 主任务ID
            inserted_id: 插入任务ID
            resume_node_id: 主任务恢复点（节点ID）
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否成功注册
            
        Raises:
            ValueError: 如果已有插入任务在执行（嵌套保护）
        """
        # 检查是否已有插入任务在执行（嵌套保护）
        if self.is_inserted_task_active():
            active_task = list(self.active_tasks.values())[0]
            self.logger.warning(f"⚠️ 已有插入任务在执行: {active_task.inserted_id}")
            raise ValueError("不支持嵌套插入任务，请先完成当前插入任务")
        
        # 创建插入任务信息
        task_info = InsertedTaskInfo(
            parent_id=parent_id,
            inserted_id=inserted_id,
            resume_node_id=resume_node_id,
            started_at=datetime.now().isoformat(),
            status="active",
            timeout=timeout
        )
        
        self.active_tasks[inserted_id] = task_info
        
        # 与状态管理器联动
        if self.state_manager:
            try:
                pause_point = self.state_manager.pause_for_inserted_task(
                    parent_id, inserted_id, resume_node_id
                )
                self.logger.info(f"✅ 主任务已暂停: {parent_id} (恢复点: {pause_point})")
            except Exception as e:
                self.logger.error(f"❌ 状态管理器暂停失败: {e}")
        
        self.logger.info(f"💉 插入任务已注册: {inserted_id} (主任务: {parent_id})")
        return True
    
    def is_inserted_task_active(self) -> bool:
        """
        判断是否有插入任务正在执行
        
        Returns:
            bool: 是否有插入任务正在执行
        """
        # 清理超时的插入任务
        self._cleanup_timeout_tasks()
        
        active_count = sum(1 for task in self.active_tasks.values() 
                          if task.status == "active")
        
        return active_count > 0
    
    def get_inserted_task_info(self) -> Optional[Dict[str, Any]]:
        """
        获取当前插入任务的状态和信息
        
        Returns:
            Dict: 插入任务信息，如果没有活跃的插入任务返回None
        """
        if not self.is_inserted_task_active():
            return None
        
        # 返回第一个活跃的插入任务
        for task in self.active_tasks.values():
            if task.status == "active":
                return asdict(task)
        
        return None
    
    def complete_inserted_task(self, inserted_id: str) -> Optional[str]:
        """
        完成插入任务，返回主任务恢复点
        
        Args:
            inserted_id: 插入任务ID
            
        Returns:
            str: 主任务恢复点（节点ID），如果不存在返回None
        """
        if inserted_id not in self.active_tasks:
            self.logger.warning(f"⚠️ 插入任务不存在: {inserted_id}")
            return None
        
        task_info = self.active_tasks[inserted_id]
        
        if task_info.status != "active":
            self.logger.warning(f"⚠️ 插入任务状态异常: {task_info.status}")
            return None
        
        # 更新任务状态
        task_info.status = "completed"
        
        # 与状态管理器联动
        if self.state_manager:
            try:
                resume_point = self.state_manager.resume_from_inserted_task(task_info.parent_id)
                self.logger.info(f"✅ 主任务已恢复: {task_info.parent_id} (节点: {resume_point})")
                
                # 移除插入任务
                del self.active_tasks[inserted_id]
                
                return resume_point
                
            except Exception as e:
                self.logger.error(f"❌ 状态管理器恢复失败: {e}")
                return None
        
        # 如果没有状态管理器，直接返回恢复点
        resume_point = task_info.resume_node_id
        del self.active_tasks[inserted_id]
        
        self.logger.info(f"✅ 插入任务完成: {inserted_id}")
        return resume_point
    
    def cancel_inserted_task(self, inserted_id: str) -> Optional[str]:
        """
        用户主动取消插入任务，恢复主任务
        
        Args:
            inserted_id: 插入任务ID
            
        Returns:
            str: 主任务恢复点，如果不存在返回None
        """
        if inserted_id not in self.active_tasks:
            self.logger.warning(f"⚠️ 插入任务不存在: {inserted_id}")
            return None
        
        task_info = self.active_tasks[inserted_id]
        
        # 更新任务状态
        task_info.status = "cancelled"
        
        # 与状态管理器联动
        if self.state_manager:
            try:
                resume_point = self.state_manager.resume_from_inserted_task(task_info.parent_id)
                self.logger.info(f"✅ 主任务已恢复: {task_info.parent_id} (节点: {resume_point})")
                
                # 移除插入任务
                del self.active_tasks[inserted_id]
                
                return resume_point
                
            except Exception as e:
                self.logger.error(f"❌ 状态管理器恢复失败: {e}")
                return None
        
        # 如果没有状态管理器，直接返回恢复点
        resume_point = task_info.resume_node_id
        del self.active_tasks[inserted_id]
        
        self.logger.info(f"✅ 插入任务已取消: {inserted_id}")
        return resume_point
    
    def auto_expire_inserted_task(self, max_duration: int = 300) -> bool:
        """
        超时自动终止插入任务
        
        Args:
            max_duration: 最大执行时间（秒）
            
        Returns:
            bool: 是否终止了超时任务
        """
        current_time = time.time()
        expired_tasks = []
        
        for inserted_id, task_info in self.active_tasks.items():
            if task_info.status != "active":
                continue
            
            # 解析开始时间
            try:
                started_time = datetime.fromisoformat(task_info.started_at).timestamp()
                elapsed = current_time - started_time
                
                # 使用任务超时时间或最大持续时间
                timeout = task_info.timeout or max_duration
                
                if elapsed > timeout:
                    self.logger.warning(f"⏰ 插入任务超时: {inserted_id} (已执行{int(elapsed)}秒)")
                    expired_tasks.append(inserted_id)
                    
            except Exception as e:
                self.logger.error(f"❌ 时间解析失败: {e}")
                continue
        
        # 终止超时任务
        terminated = False
        for inserted_id in expired_tasks:
            resume_point = self.complete_inserted_task(inserted_id)
            if resume_point:
                self.logger.info(f"✅ 超时任务已自动终止: {inserted_id}")
                terminated = True
        
        return terminated
    
    def _cleanup_timeout_tasks(self):
        """清理超时任务"""
        self.auto_expire_inserted_task()
    
    def get_active_task_parent(self) -> Optional[str]:
        """
        获取当前活跃插入任务的主任务ID
        
        Returns:
            str: 主任务ID，如果没有活跃任务返回None
        """
        if not self.is_inserted_task_active():
            return None
        
        for task in self.active_tasks.values():
            if task.status == "active":
                return task.parent_id
        
        return None
    
    def get_active_task_id(self) -> Optional[str]:
        """
        获取当前活跃插入任务的ID
        
        Returns:
            str: 插入任务ID，如果没有活跃任务返回None
        """
        if not self.is_inserted_task_active():
            return None
        
        for task_id, task in self.active_tasks.items():
            if task.status == "active":
                return task_id
        
        return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        获取队列状态
        
        Returns:
            Dict: 队列状态信息
        """
        active_count = sum(1 for task in self.active_tasks.values() 
                          if task.status == "active")
        completed_count = sum(1 for task in self.active_tasks.values() 
                             if task.status == "completed")
        cancelled_count = sum(1 for task in self.active_tasks.values() 
                             if task.status == "cancelled")
        
        active_task = None
        if self.is_inserted_task_active():
            active_task = self.get_inserted_task_info()
        
        return {
            "total_tasks": len(self.active_tasks),
            "active": active_count,
            "completed": completed_count,
            "cancelled": cancelled_count,
            "current_task": active_task
        }
    
    def list_all_active_tasks(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有活跃的插入任务
        
        Returns:
            Dict: {inserted_id: task_info}
        """
        result = {}
        for inserted_id, task in self.active_tasks.items():
            if task.status == "active":
                result[inserted_id] = asdict(task)
        
        return result


# 向后兼容
InsertedTaskQueue.add_inserted_task = InsertedTaskQueue.register_inserted_task


if __name__ == "__main__":
    # 测试插入任务队列
    print("💉 InsertedTaskQueue测试")
    print("=" * 60)
    
    queue = InsertedTaskQueue()
    
    # 测试1: 注册插入任务
    print("\n1. 注册插入任务...")
    try:
        success = queue.register_inserted_task(
            parent_id="hospital_visit",
            inserted_id="toilet_task",
            resume_node_id="goto_department",
            timeout=300
        )
        print(f"   ✅ 插入任务已注册: toilet_task")
    except ValueError as e:
        print(f"   ❌ 注册失败: {e}")
    
    # 测试2: 检查是否有活跃任务
    print("\n2. 检查活跃任务...")
    is_active = queue.is_inserted_task_active()
    print(f"   是否有活跃任务: {is_active}")
    
    # 测试3: 获取任务信息
    if is_active:
        info = queue.get_inserted_task_info()
        print(f"   任务信息: {info}")
    
    # 测试4: 尝试嵌套插入任务（应该失败）
    print("\n3. 尝试嵌套插入任务...")
    try:
        queue.register_inserted_task(
            parent_id="hospital_visit",
            inserted_id="snack_task",
            resume_node_id="goto_department",
            timeout=300
        )
        print("   ❌ 应该失败但没有")
    except ValueError as e:
        print(f"   ✅ 嵌套保护生效: {e}")
    
    # 测试5: 完成插入任务
    print("\n4. 完成插入任务...")
    resume_point = queue.complete_inserted_task("toilet_task")
    print(f"   恢复点: {resume_point}")
    
    # 测试6: 检查活跃任务
    is_active = queue.is_inserted_task_active()
    print(f"   是否有活跃任务: {is_active}")
    
    # 测试7: 获取队列状态
    print("\n5. 队列状态...")
    status = queue.get_queue_status()
    print(f"   总任务数: {status['total_tasks']}")
    print(f"   活跃任务: {status['active']}")
    print(f"   已完成: {status['completed']}")
    print(f"   已取消: {status['cancelled']}")
    
    print("\n🎉 InsertedTaskQueue测试完成！")