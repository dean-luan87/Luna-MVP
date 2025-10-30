#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 任务中心系统
支持多种任务链、用户对话修改、长期记忆调用
"""

import logging
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import os
import threading

from .memory_store import MemoryStore, get_memory_store, MemoryType, Priority

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"           # 待执行
    ACTIVE = "active"             # 执行中
    WAITING = "waiting"           # 等待用户输入
    PAUSED = "paused"             # 暂停
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    CANCELLED = "cancelled"       # 已取消

class TaskType(Enum):
    """任务类型"""
    NAVIGATION = "navigation"           # 导航任务
    REGISTRATION = "registration"       # 挂号任务
    WAITING = "waiting"                # 候诊任务
    PAYMENT = "payment"                 # 缴费任务
    EXAMINATION = "examination"         # 检查任务
    MEDICATION = "medication"          # 取药任务
    SHOPPING = "shopping"              # 购物任务
    TRANSPORT = "transport"            # 交通任务
    MEETING = "meeting"                # 会议任务
    CUSTOM = "custom"                   # 自定义任务

class TaskChainStatus(Enum):
    """任务链状态"""
    DRAFT = "draft"                 # 草稿
    ACTIVE = "active"               # 激活
    PAUSED = "paused"               # 暂停
    COMPLETED = "completed"         # 完成
    ARCHIVED = "archived"           # 归档

@dataclass
class Task:
    """任务定义"""
    task_id: str
    task_type: TaskType
    title: str
    description: str
    data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = 0.0
    updated_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    dependencies: List[str] = None  # 依赖任务ID列表
    next_tasks: List[str] = None    # 后续任务ID列表
    estimated_duration: int = 0     # 预计时长（分钟）
    priority: int = 1               # 优先级（1-5）
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.updated_at == 0.0:
            self.updated_at = time.time()
        if self.dependencies is None:
            self.dependencies = []
        if self.next_tasks is None:
            self.next_tasks = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "title": self.title,
            "description": self.description,
            "data": self.data,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "dependencies": self.dependencies,
            "next_tasks": self.next_tasks,
            "estimated_duration": self.estimated_duration,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建任务"""
        return cls(
            task_id=data["task_id"],
            task_type=TaskType(data["task_type"]),
            title=data["title"],
            description=data["description"],
            data=data["data"],
            status=TaskStatus(data["status"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            dependencies=data.get("dependencies", []),
            next_tasks=data.get("next_tasks", []),
            estimated_duration=data.get("estimated_duration", 0),
            priority=data.get("priority", 1)
        )

@dataclass
class TaskChain:
    """任务链定义"""
    chain_id: str
    name: str
    description: str
    tasks: List[Task]
    status: TaskChainStatus = TaskChainStatus.DRAFT
    created_at: float = 0.0
    updated_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    current_task_id: Optional[str] = None
    template_id: Optional[str] = None  # 模板ID
    user_customizations: Dict[str, Any] = None  # 用户自定义配置
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.updated_at == 0.0:
            self.updated_at = time.time()
        if self.user_customizations is None:
            self.user_customizations = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "chain_id": self.chain_id,
            "name": self.name,
            "description": self.description,
            "tasks": [task.to_dict() for task in self.tasks],
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "current_task_id": self.current_task_id,
            "template_id": self.template_id,
            "user_customizations": self.user_customizations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskChain':
        """从字典创建任务链"""
        tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]
        return cls(
            chain_id=data["chain_id"],
            name=data["name"],
            description=data["description"],
            tasks=tasks,
            status=TaskChainStatus(data["status"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            current_task_id=data.get("current_task_id"),
            template_id=data.get("template_id"),
            user_customizations=data.get("user_customizations", {})
        )

class TaskCenter:
    """任务中心系统"""
    
    def __init__(self, storage_file: str = "data/task_center.json"):
        """
        初始化任务中心
        
        Args:
            storage_file: 存储文件路径
        """
        self.storage_file = storage_file
        self.task_chains: Dict[str, TaskChain] = {}
        self.task_templates: Dict[str, TaskChain] = {}
        self.active_chain_id: Optional[str] = None
        
        # 回调函数
        self.on_task_start: Optional[Callable] = None
        self.on_task_complete: Optional[Callable] = None
        self.on_chain_start: Optional[Callable] = None
        self.on_chain_complete: Optional[Callable] = None
        self.on_user_input: Optional[Callable] = None
        
        # 长期记忆系统
        self.memory_store = get_memory_store()
        
        # 线程锁
        self.lock = threading.Lock()
        
        # 加载数据
        self._load_data()
        
        # 初始化模板
        self._initialize_templates()
        
        logger.info("🎯 任务中心系统初始化完成")
    
    def _load_data(self):
        """加载数据"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 加载任务链
                for chain_data in data.get("task_chains", []):
                    chain = TaskChain.from_dict(chain_data)
                    self.task_chains[chain.chain_id] = chain
                
                # 加载模板
                for template_data in data.get("templates", []):
                    template = TaskChain.from_dict(template_data)
                    self.task_templates[template.chain_id] = template
                
                logger.info(f"✅ 已加载 {len(self.task_chains)} 个任务链和 {len(self.task_templates)} 个模板")
            else:
                logger.info("📝 存储文件不存在，将创建新文件")
        except Exception as e:
            logger.error(f"❌ 加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            
            data = {
                "task_chains": [chain.to_dict() for chain in self.task_chains.values()],
                "templates": [template.to_dict() for template in self.task_templates.values()],
                "last_updated": time.time()
            }
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug("💾 任务中心数据已保存")
        except Exception as e:
            logger.error(f"❌ 保存数据失败: {e}")
    
    def _initialize_templates(self):
        """初始化任务链模板"""
        # 医院流程模板
        hospital_template = self._create_hospital_template()
        self.task_templates["hospital_workflow"] = hospital_template
        
        # 购物流程模板
        shopping_template = self._create_shopping_template()
        self.task_templates["shopping_workflow"] = shopping_template
        
        # 出行流程模板
        transport_template = self._create_transport_template()
        self.task_templates["transport_workflow"] = transport_template
        
        logger.info(f"✅ 已初始化 {len(self.task_templates)} 个任务链模板")
    
    def _create_hospital_template(self) -> TaskChain:
        """创建医院流程模板"""
        tasks = [
            Task(
                task_id="nav_to_hospital",
                task_type=TaskType.NAVIGATION,
                title="导航到医院",
                description="使用导航系统引导用户到达目标医院",
                data={"destination": "医院", "transport_mode": "auto"},
                estimated_duration=30,
                priority=3
            ),
            Task(
                task_id="registration",
                task_type=TaskType.REGISTRATION,
                title="挂号",
                description="在医院挂号处完成挂号流程",
                data={"department": "", "doctor": "", "time": ""},
                dependencies=["nav_to_hospital"],
                estimated_duration=15,
                priority=4
            ),
            Task(
                task_id="waiting",
                task_type=TaskType.WAITING,
                title="候诊",
                description="在候诊区等待叫号",
                data={"queue_number": "", "estimated_wait": 0},
                dependencies=["registration"],
                estimated_duration=60,
                priority=2
            ),
            Task(
                task_id="examination",
                task_type=TaskType.EXAMINATION,
                title="就诊",
                description="与医生进行诊疗",
                data={"doctor": "", "department": ""},
                dependencies=["waiting"],
                estimated_duration=30,
                priority=5
            ),
            Task(
                task_id="payment",
                task_type=TaskType.PAYMENT,
                title="缴费",
                description="完成医疗费用支付",
                data={"amount": 0, "payment_method": ""},
                dependencies=["examination"],
                estimated_duration=10,
                priority=3
            ),
            Task(
                task_id="medication",
                task_type=TaskType.MEDICATION,
                title="取药",
                description="在药房取药",
                data={"prescription": "", "pharmacy_location": ""},
                dependencies=["payment"],
                estimated_duration=20,
                priority=3
            )
        ]
        
        # 设置任务链关系
        for i, task in enumerate(tasks):
            if i < len(tasks) - 1:
                task.next_tasks = [tasks[i + 1].task_id]
        
        return TaskChain(
            chain_id="hospital_workflow",
            name="医院就诊流程",
            description="完整的医院就诊流程，包括导航、挂号、候诊、就诊、缴费、取药",
            tasks=tasks,
            template_id="hospital_workflow"
        )
    
    def _create_shopping_template(self) -> TaskChain:
        """创建购物流程模板"""
        tasks = [
            Task(
                task_id="nav_to_mall",
                task_type=TaskType.NAVIGATION,
                title="导航到商场",
                description="导航到目标购物中心",
                data={"destination": "商场", "transport_mode": "auto"},
                estimated_duration=20,
                priority=3
            ),
            Task(
                task_id="shopping",
                task_type=TaskType.SHOPPING,
                title="购物",
                description="在商场内进行购物",
                data={"shopping_list": [], "budget": 0},
                dependencies=["nav_to_mall"],
                estimated_duration=120,
                priority=4
            ),
            Task(
                task_id="payment_shopping",
                task_type=TaskType.PAYMENT,
                title="结账",
                description="完成购物结账",
                data={"items": [], "total_amount": 0},
                dependencies=["shopping"],
                estimated_duration=15,
                priority=3
            )
        ]
        
        # 设置任务链关系
        for i, task in enumerate(tasks):
            if i < len(tasks) - 1:
                task.next_tasks = [tasks[i + 1].task_id]
        
        return TaskChain(
            chain_id="shopping_workflow",
            name="购物流程",
            description="完整的购物流程，包括导航、购物、结账",
            tasks=tasks,
            template_id="shopping_workflow"
        )
    
    def _create_transport_template(self) -> TaskChain:
        """创建出行流程模板"""
        tasks = [
            Task(
                task_id="plan_route",
                task_type=TaskType.NAVIGATION,
                title="规划路线",
                description="规划出行路线",
                data={"destination": "", "transport_mode": "auto"},
                estimated_duration=5,
                priority=3
            ),
            Task(
                task_id="transport",
                task_type=TaskType.TRANSPORT,
                title="出行",
                description="执行出行计划",
                data={"route": "", "estimated_time": 0},
                dependencies=["plan_route"],
                estimated_duration=60,
                priority=4
            )
        ]
        
        # 设置任务链关系
        tasks[0].next_tasks = [tasks[1].task_id]
        
        return TaskChain(
            chain_id="transport_workflow",
            name="出行流程",
            description="出行路线规划和执行",
            tasks=tasks,
            template_id="transport_workflow"
        )
    
    def create_task_chain_from_template(self, template_id: str, customizations: Dict[str, Any] = None) -> str:
        """
        从模板创建任务链
        
        Args:
            template_id: 模板ID
            customizations: 用户自定义配置
            
        Returns:
            str: 新任务链ID
        """
        if template_id not in self.task_templates:
            raise ValueError(f"模板不存在: {template_id}")
        
        template = self.task_templates[template_id]
        chain_id = f"{template_id}_{int(time.time() * 1000)}"
        
        # 创建新任务
        new_tasks = []
        for task in template.tasks:
            new_task = Task(
                task_id=f"{task.task_id}_{int(time.time() * 1000)}",
                task_type=task.task_type,
                title=task.title,
                description=task.description,
                data=task.data.copy(),
                dependencies=task.dependencies.copy() if task.dependencies else [],
                next_tasks=task.next_tasks.copy() if task.next_tasks else [],
                estimated_duration=task.estimated_duration,
                priority=task.priority
            )
            new_tasks.append(new_task)
        
        # 更新任务关系
        task_id_mapping = {}
        for i, (old_task, new_task) in enumerate(zip(template.tasks, new_tasks)):
            task_id_mapping[old_task.task_id] = new_task.task_id
        
        for new_task in new_tasks:
            new_task.dependencies = [task_id_mapping[dep] for dep in new_task.dependencies if dep in task_id_mapping]
            new_task.next_tasks = [task_id_mapping[next_id] for next_id in new_task.next_tasks if next_id in task_id_mapping]
        
        # 创建任务链
        chain = TaskChain(
            chain_id=chain_id,
            name=template.name,
            description=template.description,
            tasks=new_tasks,
            template_id=template_id,
            user_customizations=customizations or {}
        )
        
        with self.lock:
            self.task_chains[chain_id] = chain
            self._save_data()
        
        # 保存到长期记忆
        self._save_chain_to_memory(chain)
        
        logger.info(f"🔗 从模板 {template_id} 创建任务链: {chain_id}")
        return chain_id
    
    def start_task_chain(self, chain_id: str) -> bool:
        """
        启动任务链
        
        Args:
            chain_id: 任务链ID
            
        Returns:
            bool: 是否成功启动
        """
        if chain_id not in self.task_chains:
            logger.error(f"❌ 任务链不存在: {chain_id}")
            return False
        
        chain = self.task_chains[chain_id]
        
        if chain.status != TaskChainStatus.DRAFT:
            logger.warning(f"⚠️ 任务链状态不允许启动: {chain.status}")
            return False
        
        with self.lock:
            chain.status = TaskChainStatus.ACTIVE
            chain.started_at = time.time()
            chain.updated_at = time.time()
            
            # 找到第一个任务
            first_task = None
            for task in chain.tasks:
                if not task.dependencies:
                    first_task = task
                    break
            
            if first_task:
                chain.current_task_id = first_task.task_id
                first_task.status = TaskStatus.ACTIVE
                first_task.started_at = time.time()
                first_task.updated_at = time.time()
            
            self.active_chain_id = chain_id
            self._save_data()
        
        # 保存到长期记忆
        self._save_chain_event_to_memory(chain_id, "started", "任务链已启动")
        
        logger.info(f"🚀 任务链已启动: {chain_id}")
        
        # 触发回调
        if self.on_chain_start:
            self.on_chain_start(chain)
        
        return True
    
    def pause_task_chain(self, chain_id: str, reason: str = "用户暂停") -> bool:
        """
        暂停任务链
        
        Args:
            chain_id: 任务链ID
            reason: 暂停原因
            
        Returns:
            bool: 是否成功暂停
        """
        if chain_id not in self.task_chains:
            logger.error(f"❌ 任务链不存在: {chain_id}")
            return False
        
        chain = self.task_chains[chain_id]
        
        if chain.status != TaskChainStatus.ACTIVE:
            logger.warning(f"⚠️ 任务链状态不允许暂停: {chain.status}")
            return False
        
        with self.lock:
            chain.status = TaskChainStatus.PAUSED
            chain.updated_at = time.time()
            
            # 暂停当前任务
            if chain.current_task_id:
                current_task = self._get_task_by_id(chain_id, chain.current_task_id)
                if current_task:
                    current_task.status = TaskStatus.PAUSED
                    current_task.updated_at = time.time()
            
            self._save_data()
        
        logger.info(f"⏸️ 任务链已暂停: {chain_id} - {reason}")
        return True
    
    def resume_task_chain(self, chain_id: str) -> bool:
        """
        恢复任务链
        
        Args:
            chain_id: 任务链ID
            
        Returns:
            bool: 是否成功恢复
        """
        if chain_id not in self.task_chains:
            logger.error(f"❌ 任务链不存在: {chain_id}")
            return False
        
        chain = self.task_chains[chain_id]
        
        if chain.status != TaskChainStatus.PAUSED:
            logger.warning(f"⚠️ 任务链状态不允许恢复: {chain.status}")
            return False
        
        with self.lock:
            chain.status = TaskChainStatus.ACTIVE
            chain.updated_at = time.time()
            
            # 恢复当前任务
            if chain.current_task_id:
                current_task = self._get_task_by_id(chain_id, chain.current_task_id)
                if current_task:
                    current_task.status = TaskStatus.ACTIVE
                    current_task.updated_at = time.time()
            
            self._save_data()
        
        logger.info(f"▶️ 任务链已恢复: {chain_id}")
        return True
    
    def complete_task(self, chain_id: str, task_id: str, result: Dict[str, Any] = None) -> bool:
        """
        完成任务
        
        Args:
            chain_id: 任务链ID
            task_id: 任务ID
            result: 任务结果
            
        Returns:
            bool: 是否成功完成
        """
        if chain_id not in self.task_chains:
            logger.error(f"❌ 任务链不存在: {chain_id}")
            return False
        
        task = self._get_task_by_id(chain_id, task_id)
        if not task:
            logger.error(f"❌ 任务不存在: {task_id}")
            return False
        
        with self.lock:
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            task.updated_at = time.time()
            
            if result:
                task.data.update(result)
            
            # 检查是否有下一个任务
            chain = self.task_chains[chain_id]
            next_task_id = self._get_next_task_id(chain_id, task_id)
            
            if next_task_id:
                # 启动下一个任务
                next_task = self._get_task_by_id(chain_id, next_task_id)
                if next_task and next_task.status == TaskStatus.PENDING:
                    next_task.status = TaskStatus.ACTIVE
                    next_task.started_at = time.time()
                    next_task.updated_at = time.time()
                    chain.current_task_id = next_task_id
                else:
                    chain.current_task_id = None
            else:
                # 任务链完成
                chain.status = TaskChainStatus.COMPLETED
                chain.completed_at = time.time()
                chain.current_task_id = None
                self.active_chain_id = None
            
            chain.updated_at = time.time()
            self._save_data()
        
        # 保存到长期记忆
        self._save_task_event_to_memory(chain_id, task_id, "completed", f"任务已完成: {task.title}")
        
        logger.info(f"✅ 任务已完成: {task_id}")
        
        # 触发回调
        if self.on_task_complete:
            self.on_task_complete(chain, task, result)
        
        return True
    
    def modify_task_chain(self, chain_id: str, modifications: Dict[str, Any]) -> bool:
        """
        修改任务链
        
        Args:
            chain_id: 任务链ID
            modifications: 修改内容
            
        Returns:
            bool: 是否成功修改
        """
        if chain_id not in self.task_chains:
            logger.error(f"❌ 任务链不存在: {chain_id}")
            return False
        
        chain = self.task_chains[chain_id]
        
        with self.lock:
            # 更新任务链信息
            if "name" in modifications:
                chain.name = modifications["name"]
            if "description" in modifications:
                chain.description = modifications["description"]
            if "user_customizations" in modifications:
                chain.user_customizations.update(modifications["user_customizations"])
            
            # 更新任务信息
            if "tasks" in modifications:
                for task_mod in modifications["tasks"]:
                    task_id = task_mod.get("task_id")
                    if task_id:
                        task = self._get_task_by_id(chain_id, task_id)
                        if task:
                            if "title" in task_mod:
                                task.title = task_mod["title"]
                            if "description" in task_mod:
                                task.description = task_mod["description"]
                            if "data" in task_mod:
                                task.data.update(task_mod["data"])
                            if "priority" in task_mod:
                                task.priority = task_mod["priority"]
                            if "estimated_duration" in task_mod:
                                task.estimated_duration = task_mod["estimated_duration"]
                            task.updated_at = time.time()
            
            chain.updated_at = time.time()
            self._save_data()
        
        logger.info(f"✏️ 任务链已修改: {chain_id}")
        return True
    
    def get_task_chain_status(self, chain_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务链状态
        
        Args:
            chain_id: 任务链ID
            
        Returns:
            Dict[str, Any]: 任务链状态信息
        """
        if chain_id not in self.task_chains:
            return None
        
        chain = self.task_chains[chain_id]
        
        # 统计任务状态
        task_stats = {}
        for status in TaskStatus:
            task_stats[status.value] = 0
        
        for task in chain.tasks:
            task_stats[task.status.value] += 1
        
        return {
            "chain_id": chain_id,
            "name": chain.name,
            "status": chain.status.value,
            "current_task_id": chain.current_task_id,
            "task_stats": task_stats,
            "progress": self._calculate_progress(chain),
            "created_at": chain.created_at,
            "updated_at": chain.updated_at,
            "started_at": chain.started_at,
            "completed_at": chain.completed_at
        }
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """
        获取可用模板列表
        
        Returns:
            List[Dict[str, Any]]: 模板列表
        """
        templates = []
        for template in self.task_templates.values():
            templates.append({
                "template_id": template.chain_id,
                "name": template.name,
                "description": template.description,
                "task_count": len(template.tasks),
                "estimated_duration": sum(task.estimated_duration for task in template.tasks)
            })
        return templates
    
    def _get_task_by_id(self, chain_id: str, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        if chain_id not in self.task_chains:
            return None
        
        chain = self.task_chains[chain_id]
        for task in chain.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def _get_next_task_id(self, chain_id: str, current_task_id: str) -> Optional[str]:
        """获取下一个任务ID"""
        current_task = self._get_task_by_id(chain_id, current_task_id)
        if not current_task or not current_task.next_tasks:
            return None
        
        # 检查依赖是否满足
        for next_task_id in current_task.next_tasks:
            next_task = self._get_task_by_id(chain_id, next_task_id)
            if next_task:
                # 检查所有依赖是否完成
                dependencies_met = True
                for dep_id in next_task.dependencies:
                    dep_task = self._get_task_by_id(chain_id, dep_id)
                    if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                        dependencies_met = False
                        break
                
                if dependencies_met:
                    return next_task_id
        
        return None
    
    def _calculate_progress(self, chain: TaskChain) -> float:
        """计算任务链进度"""
        if not chain.tasks:
            return 0.0
        
        completed_count = sum(1 for task in chain.tasks if task.status == TaskStatus.COMPLETED)
        return completed_count / len(chain.tasks) * 100.0
    
    def _save_chain_to_memory(self, chain: TaskChain):
        """保存任务链到长期记忆"""
        try:
            memory_content = f"创建任务链: {chain.name} - {chain.description}"
            self.memory_store.add_memory(
                title=f"任务链: {chain.name}",
                content=memory_content,
                memory_type=MemoryType.NOTE,
                tags=["task_chain", "created", chain.template_id or "custom"],
                priority=Priority.NORMAL
            )
        except Exception as e:
            logger.error(f"❌ 保存任务链到记忆失败: {e}")
    
    def _save_chain_event_to_memory(self, chain_id: str, event: str, description: str):
        """保存任务链事件到长期记忆"""
        try:
            chain = self.task_chains.get(chain_id)
            if chain:
                memory_content = f"任务链事件: {chain.name} - {event} - {description}"
                self.memory_store.add_memory(
                    title=f"任务链事件: {event}",
                    content=memory_content,
                    memory_type=MemoryType.NOTE,
                    tags=["task_chain", "event", event, chain_id],
                    priority=Priority.NORMAL
                )
        except Exception as e:
            logger.error(f"❌ 保存任务链事件到记忆失败: {e}")
    
    def _save_task_event_to_memory(self, chain_id: str, task_id: str, event: str, description: str):
        """保存任务事件到长期记忆"""
        try:
            chain = self.task_chains.get(chain_id)
            task = self._get_task_by_id(chain_id, task_id)
            if chain and task:
                memory_content = f"任务事件: {chain.name} - {task.title} - {event} - {description}"
                self.memory_store.add_memory(
                    title=f"任务事件: {event}",
                    content=memory_content,
                    memory_type=MemoryType.NOTE,
                    tags=["task", "event", event, chain_id, task_id],
                    priority=Priority.NORMAL
                )
        except Exception as e:
            logger.error(f"❌ 保存任务事件到记忆失败: {e}")
    
    def get_chain_from_memory(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """从长期记忆中搜索任务链"""
        try:
            memories = self.memory_store.search_memories(keywords, memory_type="note")
            chains = []
            
            for memory in memories:
                if "task_chain" in memory.tags:
                    # 提取任务链信息
                    chain_info = {
                        "memory_id": memory.id,
                        "content": memory.content,
                        "created_at": memory.created_at,
                        "tags": memory.tags
                    }
                    chains.append(chain_info)
            
            return chains
        except Exception as e:
            logger.error(f"❌ 从记忆搜索任务链失败: {e}")
            return []
    
    def create_chain_from_memory(self, memory_id: str) -> Optional[str]:
        """从记忆中的信息创建任务链"""
        try:
            memory = self.memory_store.get_memory_by_id(memory_id)
            if not memory or "task_chain" not in memory.tags:
                return None
            
            # 从标签中提取模板信息
            template_id = None
            for tag in memory.tags:
                if tag in ["hospital_workflow", "shopping_workflow", "transport_workflow"]:
                    template_id = tag
                    break
            
            if template_id:
                # 从记忆内容中提取自定义信息
                customizations = self._extract_customizations_from_memory(memory.content)
                return self.create_task_chain_from_template(template_id, customizations)
            
            return None
        except Exception as e:
            logger.error(f"❌ 从记忆创建任务链失败: {e}")
            return None
    
    def _extract_customizations_from_memory(self, content: str) -> Dict[str, Any]:
        """从记忆内容中提取自定义信息"""
        customizations = {}
        
        # 简单的信息提取逻辑
        if "医院" in content:
            customizations["type"] = "hospital"
        if "购物" in content:
            customizations["type"] = "shopping"
        if "出行" in content:
            customizations["type"] = "transport"
        
        return customizations


# 全局任务中心实例
_global_task_center: Optional[TaskCenter] = None

def get_task_center() -> TaskCenter:
    """获取全局任务中心实例"""
    global _global_task_center
    if _global_task_center is None:
        _global_task_center = TaskCenter()
    return _global_task_center


if __name__ == "__main__":
    # 测试任务中心
    print("🎯 任务中心系统测试")
    print("=" * 50)
    
    task_center = get_task_center()
    
    # 测试1: 获取可用模板
    print("\n1. 获取可用模板...")
    templates = task_center.get_available_templates()
    for template in templates:
        print(f"   📋 {template['name']}: {template['description']}")
    
    # 测试2: 从模板创建任务链
    print("\n2. 从模板创建任务链...")
    chain_id = task_center.create_task_chain_from_template(
        "hospital_workflow",
        {"hospital_name": "虹口医院", "department": "内科"}
    )
    print(f"   ✅ 创建任务链: {chain_id}")
    
    # 测试3: 启动任务链
    print("\n3. 启动任务链...")
    success = task_center.start_task_chain(chain_id)
    print(f"   启动成功: {success}")
    
    # 测试4: 获取任务链状态
    print("\n4. 获取任务链状态...")
    status = task_center.get_task_chain_status(chain_id)
    if status:
        print(f"   状态: {status['status']}")
        print(f"   进度: {status['progress']:.1f}%")
        print(f"   当前任务: {status['current_task_id']}")
    
    print("\n🎉 任务中心系统测试完成！")
