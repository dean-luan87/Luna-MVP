#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 任务链打断机制 (Task Interrupt Handler)
支持导航过程中临时中断主任务，插入子任务，并在子任务完成后恢复主任务
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    ACTIVE = "active"         # 活跃中
    PAUSED = "paused"         # 已暂停
    SUBTASK = "subtask"       # 子任务
    RESUMED = "resumed"       # 已恢复
    COMPLETED = "completed"   # 已完成
    CANCELLED = "cancelled"   # 已取消


@dataclass
class Task:
    """任务"""
    task_id: str
    task_type: str
    description: str
    intent: str
    destination: Optional[str] = None
    status: TaskStatus = TaskStatus.ACTIVE
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    paused_at: Optional[str] = None
    resumed_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data["status"] = self.status.value
        return data


class TaskInterruptor:
    """任务打断管理器"""
    
    def __init__(self):
        """初始化任务打断管理器"""
        # 任务栈
        self.main_task_stack: List[Task] = []
        self.subtask_stack: List[Task] = []
        
        # 当前任务
        self.current_task: Optional[Task] = None
        
        # 任务计数器
        self.task_counter = 0
        
        logger.info("🧭 任务打断管理器初始化完成")
    
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        self.task_counter += 1
        return f"task_{self.task_counter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def start_main_task(self,
                       task_type: str,
                       description: str,
                       intent: str,
                       destination: Optional[str] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        启动主任务
        
        Args:
            task_type: 任务类型
            description: 任务描述
            intent: 意图
            destination: 目的地
            metadata: 额外元数据
            
        Returns:
            任务ID
        """
        task = Task(
            task_id=self._generate_task_id(),
            task_type=task_type,
            description=description,
            intent=intent,
            destination=destination,
            status=TaskStatus.ACTIVE,
            metadata=metadata or {}
        )
        
        self.main_task_stack.append(task)
        self.current_task = task
        
        logger.info(f"✅ 启动主任务: {task.task_id} - {description}")
        
        return task.task_id
    
    def interrupt_with_subtask(self,
                               subtask_type: str,
                               description: str,
                               intent: str,
                               destination: Optional[str] = None,
                               metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        插入子任务（打断主任务）
        
        Args:
            subtask_type: 子任务类型
            description: 任务描述
            intent: 意图
            destination: 目的地
            metadata: 额外元数据
            
        Returns:
            任务ID
        """
        # 如果当前有主任务，暂停它
        if self.current_task and self.current_task.status == TaskStatus.ACTIVE:
            self.current_task.status = TaskStatus.PAUSED
            self.current_task.paused_at = datetime.now().isoformat()
            logger.info(f"⏸️ 暂停主任务: {self.current_task.task_id}")
        
        # 创建子任务
        subtask = Task(
            task_id=self._generate_task_id(),
            task_type=subtask_type,
            description=description,
            intent=intent,
            destination=destination,
            status=TaskStatus.SUBTASK,
            metadata=metadata or {}
        )
        
        self.subtask_stack.append(subtask)
        self.current_task = subtask
        
        logger.info(f"✅ 启动子任务: {subtask.task_id} - {description}")
        
        return subtask.task_id
    
    def complete_current_task(self) -> Optional[str]:
        """
        完成当前任务
        
        Returns:
            恢复的任务ID（如果有）
        """
        if not self.current_task:
            logger.warning("⚠️ 没有当前任务")
            return None
        
        # 保存当前任务
        completed_task = self.current_task
        
        # 标记当前任务为已完成
        completed_task.status = TaskStatus.COMPLETED
        
        logger.info(f"✅ 完成任务: {completed_task.task_id}")
        
        # 如果是子任务，从子任务栈移除并尝试恢复主任务
        if completed_task in self.subtask_stack:
            self.subtask_stack.remove(completed_task)
            
            # 恢复主任务
            if self.main_task_stack:
                main_task = self.main_task_stack[-1]
                if main_task.status == TaskStatus.PAUSED:
                    main_task.status = TaskStatus.RESUMED
                    main_task.resumed_at = datetime.now().isoformat()
                    self.current_task = main_task
                    
                    logger.info(f"▶️ 恢复主任务: {main_task.task_id}")
                    return main_task.task_id
        
        # 如果是主任务，从主任务栈移除
        elif completed_task in self.main_task_stack:
            self.main_task_stack.remove(completed_task)
        
        # 检查是否还有待处理的任务
        if self.main_task_stack:
            self.current_task = self.main_task_stack[-1]
        else:
            self.current_task = None
        
        return None
    
    def get_current_task(self) -> Optional[Dict[str, Any]]:
        """获取当前任务"""
        if self.current_task:
            return self.current_task.to_dict()
        return None
    
    def get_task_status(self) -> Dict[str, Any]:
        """获取任务状态"""
        return {
            "current_task": self.get_current_task(),
            "main_task_count": len(self.main_task_stack),
            "subtask_count": len(self.subtask_stack),
            "main_tasks": [task.to_dict() for task in self.main_task_stack],
            "subtasks": [task.to_dict() for task in self.subtask_stack]
        }
    
    def cancel_current_task(self):
        """取消当前任务"""
        if self.current_task:
            self.current_task.status = TaskStatus.CANCELLED
            logger.info(f"❌ 取消任务: {self.current_task.task_id}")
            
            # 如果取消子任务，恢复主任务
            if self.current_task in self.subtask_stack:
                self.subtask_stack.remove(self.current_task)
                if self.main_task_stack:
                    main_task = self.main_task_stack[-1]
                    main_task.status = TaskStatus.RESUMED
                    self.current_task = main_task
    
    def clear_all_tasks(self):
        """清空所有任务"""
        self.main_task_stack.clear()
        self.subtask_stack.clear()
        self.current_task = None
        
        logger.info("🗑️ 已清空所有任务")
    
    def get_resume_prompt(self) -> Optional[str]:
        """
        获取恢复提示
        
        Returns:
            恢复提示文本
        """
        if self.main_task_stack:
            main_task = self.main_task_stack[-1]
            if main_task.status == TaskStatus.PAUSED:
                if main_task.destination:
                    return f"是否继续前往{main_task.destination}？"
                else:
                    return f"是否继续{main_task.description}？"
        
        return None


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建任务打断管理器
    task_interruptor = TaskInterruptor()
    
    print("=" * 70)
    print("🧭 测试任务链打断机制")
    print("=" * 70)
    
    # 启动主任务
    print("\n1️⃣ 启动主任务: 去医院305号诊室")
    main_task_id = task_interruptor.start_main_task(
        task_type="navigation",
        description="去医院305号诊室",
        intent="find_destination",
        destination="305号诊室"
    )
    print(f"   主任务ID: {main_task_id}")
    
    # 查看状态
    status = task_interruptor.get_task_status()
    print(f"\n   当前任务: {status['current_task']['description']}")
    
    # 打断并插入子任务
    print("\n2️⃣ 用户临时说: '我想先上厕所'")
    subtask_id = task_interruptor.interrupt_with_subtask(
        subtask_type="find_facility",
        description="找洗手间",
        intent="find_toilet",
        destination="洗手间"
    )
    print(f"   子任务ID: {subtask_id}")
    
    # 查看状态
    status = task_interruptor.get_task_status()
    print(f"\n   当前任务: {status['current_task']['description']}")
    print(f"   主任务数: {status['main_task_count']}")
    print(f"   子任务数: {status['subtask_count']}")
    
    # 完成子任务
    print("\n3️⃣ 子任务完成")
    restored_task_id = task_interruptor.complete_current_task()
    
    if restored_task_id:
        print(f"   已恢复主任务: {restored_task_id}")
    
    # 获取恢复提示
    resume_prompt = task_interruptor.get_resume_prompt()
    if resume_prompt:
        print(f"\n   🔊 系统提示: {resume_prompt}")
    
    # 查看最终状态
    print("\n4️⃣ 最终状态:")
    status = task_interruptor.get_task_status()
    print(f"   当前任务: {status['current_task']['description'] if status['current_task'] else 'None'}")
    print(f"   主任务数: {status['main_task_count']}")
    print(f"   子任务数: {status['subtask_count']}")
    
    print("\n✅ 测试完成")

