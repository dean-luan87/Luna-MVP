"""
任务链管理器
支持"等待-挂号-用户唤醒"机制
"""

import logging
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    ACTIVE = "active"           # 活跃执行
    WAITING = "waiting"         # 等待用户操作
    SUSPENDED = "suspended"     # 暂停
    COMPLETED = "completed"     # 完成
    FAILED = "failed"           # 失败


class TaskType(Enum):
    """任务类型"""
    NAVIGATION = "navigation"           # 导航任务
    REGISTRATION = "registration"       # 挂号任务
    WAITING_FOR_USER = "waiting_for_user"  # 等待用户
    OCR_SCAN = "ocr_scan"              # OCR扫描
    ROUTE_MAPPING = "route_mapping"    # 路径映射


@dataclass
class Task:
    """任务定义"""
    task_id: str
    task_type: TaskType
    description: str
    status: TaskStatus
    created_at: float
    updated_at: float
    data: Dict[str, Any]
    next_tasks: List[str] = None  # 后续任务ID列表
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "data": self.data,
            "next_tasks": self.next_tasks or []
        }


class TaskChainManager:
    """任务链管理器"""
    
    def __init__(self):
        """初始化任务链管理器"""
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, Task] = {}
        self.current_task_id: Optional[str] = None
        self.task_history: List[str] = []
        
        # 唤醒词检测
        self.wake_words = ["Luna", "我挂号好了", "我办完了", "继续", "下一步"]
        
        self.logger.info("🔗 任务链管理器初始化完成")
    
    def create_task(self,
                    task_type: TaskType,
                    description: str,
                    data: Dict[str, Any] = None,
                    next_tasks: List[str] = None) -> str:
        """
        创建任务
        
        Args:
            task_type: 任务类型
            description: 任务描述
            data: 任务数据
            next_tasks: 后续任务ID列表
        
        Returns:
            str: 任务ID
        """
        task_id = f"{task_type.value}_{int(time.time() * 1000)}"
        
        task = Task(
            task_id=task_id,
            task_type=task_type,
            description=description,
            status=TaskStatus.ACTIVE,
            created_at=time.time(),
            updated_at=time.time(),
            data=data or {},
            next_tasks=next_tasks or []
        )
        
        self.tasks[task_id] = task
        self.current_task_id = task_id
        self.task_history.append(task_id)
        
        self.logger.info(f"🔗 创建任务: {task_id} - {description}")
        return task_id
    
    def set_task_waiting(self, task_id: str, reason: str = "等待用户操作"):
        """
        设置任务为等待状态
        
        Args:
            task_id: 任务ID
            reason: 等待原因
        """
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.WAITING
            self.tasks[task_id].updated_at = time.time()
            self.tasks[task_id].data["waiting_reason"] = reason
            
            self.logger.info(f"⏳ 任务进入等待状态: {task_id} - {reason}")
    
    def resume_task(self, task_id: str, user_input: str = "") -> bool:
        """
        恢复任务
        
        Args:
            task_id: 任务ID
            user_input: 用户输入
        
        Returns:
            bool: 是否成功恢复
        """
        if task_id not in self.tasks:
            self.logger.warning(f"⚠️ 任务不存在: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.WAITING:
            self.logger.warning(f"⚠️ 任务不在等待状态: {task_id}")
            return False
        
        # 检查唤醒词
        if not self._check_wake_words(user_input):
            self.logger.info(f"🔍 未检测到唤醒词: {user_input}")
            return False
        
        # 恢复任务
        task.status = TaskStatus.ACTIVE
        task.updated_at = time.time()
        task.data["resumed_at"] = time.time()
        task.data["user_input"] = user_input
        
        self.current_task_id = task_id
        
        self.logger.info(f"▶️ 任务已恢复: {task_id}")
        return True
    
    def complete_task(self, task_id: str, result: Dict[str, Any] = None):
        """
        完成任务
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].updated_at = time.time()
            if result:
                self.tasks[task_id].data["result"] = result
            
            self.logger.info(f"✅ 任务已完成: {task_id}")
            
            # 自动启动后续任务
            self._start_next_tasks(task_id)
    
    def get_current_task(self) -> Optional[Task]:
        """获取当前任务"""
        if self.current_task_id and self.current_task_id in self.tasks:
            return self.tasks[self.current_task_id]
        return None
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态"""
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None
    
    def _check_wake_words(self, user_input: str) -> bool:
        """检查唤醒词"""
        user_input_lower = user_input.lower()
        return any(wake_word.lower() in user_input_lower for wake_word in self.wake_words)
    
    def _start_next_tasks(self, completed_task_id: str):
        """启动后续任务"""
        if completed_task_id not in self.tasks:
            return
        
        completed_task = self.tasks[completed_task_id]
        next_task_ids = completed_task.next_tasks
        
        for next_task_id in next_task_ids:
            if next_task_id in self.tasks:
                next_task = self.tasks[next_task_id]
                if next_task.status == TaskStatus.WAITING:
                    next_task.status = TaskStatus.ACTIVE
                    next_task.updated_at = time.time()
                    self.current_task_id = next_task_id
                    self.logger.info(f"🚀 启动后续任务: {next_task_id}")


# 全局任务链管理器实例
_global_task_chain: Optional[TaskChainManager] = None


def get_task_chain_manager() -> TaskChainManager:
    """获取全局任务链管理器实例"""
    global _global_task_chain
    if _global_task_chain is None:
        _global_task_chain = TaskChainManager()
    return _global_task_chain


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🔗 任务链管理器测试")
    print("=" * 70)
    
    manager = get_task_chain_manager()
    
    # 测试1: 创建任务
    print("\n1. 创建任务...")
    task1_id = manager.create_task(
        TaskType.NAVIGATION,
        "导航到挂号处",
        {"destination": "挂号处"}
    )
    print(f"   任务ID: {task1_id}")
    
    # 测试2: 设置等待状态
    print("\n2. 设置等待状态...")
    manager.set_task_waiting(task1_id, "等待用户挂号完成")
    
    # 测试3: 检查唤醒词
    print("\n3. 测试唤醒词检测...")
    wake_result = manager.resume_task(task1_id, "Luna，我挂号好了")
    print(f"   唤醒成功: {wake_result}")
    
    # 测试4: 完成任务
    print("\n4. 完成任务...")
    manager.complete_task(task1_id, {"success": True})
    
    # 测试5: 获取当前任务
    print("\n5. 获取当前任务...")
    current_task = manager.get_current_task()
    if current_task:
        print(f"   当前任务: {current_task.description}")
    else:
        print("   无当前任务")
    
    print("\n" + "=" * 70)
