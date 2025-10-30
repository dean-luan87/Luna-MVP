#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 本地增强记忆系统模块
构建支持用户主动输入和系统记忆的重要信息系统
"""

import logging
import json
import time
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """记忆类型"""
    MEDICATION = "medication"       # 服药
    PHONE = "phone"                  # 电话号码
    EVENT = "event"                  # 事件
    REMINDER = "reminder"           # 提醒
    NOTE = "note"                    # 笔记
    PERSONAL = "personal"           # 个人信息

class Priority(Enum):
    """优先级"""
    LOW = "low"                     # 低
    NORMAL = "normal"              # 正常
    HIGH = "high"                  # 高
    URGENT = "urgent"              # 紧急

class MemoryStatus(Enum):
    """记忆状态"""
    ACTIVE = "active"               # 正常提醒
    PAUSED = "paused"                # 暂停（用户主动取消）
    DELETED = "deleted"              # 彻底删除（可选，不推荐）

@dataclass
class FeedbackRecord:
    """反馈记录"""
    action: str                     # 动作（paused/resumed/modified）
    reason: str                     # 原因
    timestamp: str                  # 时间戳
    raw_input: str                  # 原始输入

@dataclass
class MemoryItem:
    """记忆项"""
    id: str                         # 唯一ID (如 "m_20251028_001")
    type: str                       # 记忆类型 (medication/reminder/event等)
    title: str                      # 标题
    content: str                     # 内容
    tags: List[str]                 # 标签
    priority: str                   # 优先级
    created_at: float               # 创建时间
    updated_at: float               # 最后修改时间
    trigger_time: Optional[str] = None    # 触发时间（如 "20:00"）
    repeat: Optional[str] = None          # 重复周期（daily/weekly/none）
    status: str = "active"               # 状态（active/paused/deleted）
    remind_at: Optional[float] = None    # 提醒时间
    reminder_method: str = "voice"       # 提醒方式
    category: str = ""                   # 分类
    feedback_history: List[Dict[str, Any]] = None  # 反馈历史记录
    
    def __post_init__(self):
        if self.feedback_history is None:
            self.feedback_history = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "trigger_time": self.trigger_time,
            "repeat": self.repeat,
            "status": self.status,
            "remind_at": self.remind_at,
            "reminder_method": self.reminder_method,
            "category": self.category,
            "feedback_history": self.feedback_history
        }

class MemoryStore:
    """记忆存储器"""
    
    def __init__(self, storage_file: str = "data/memory_store.json"):
        """
        初始化记忆存储器
        
        Args:
            storage_file: 存储文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        self.memories: Dict[str, MemoryItem] = {}
        
        # 导航状态（独立于记忆项的状态）
        self.navigation_status: str = "idle"  # idle/active/pending/cancelled
        
        self._load_data()
        self.logger.info("🧠 记忆存储器初始化完成")
    
    def add_memory(self, memory_type: MemoryType, 
                   title: str, 
                   content: str,
                   tags: List[str] = None,
                   priority: Priority = Priority.NORMAL,
                   remind_at: Optional[float] = None,
                   reminder_method: str = "voice",
                   category: str = "") -> MemoryItem:
        """
        添加记忆
        
        Args:
            memory_type: 记忆类型
            title: 标题
            content: 内容
            tags: 标签列表
            priority: 优先级
            remind_at: 提醒时间
            reminder_method: 提醒方式
            category: 类别
            
        Returns:
            MemoryItem: 创建的记忆项
        """
        memory_id = f"{memory_type.value}_{int(time.time())}"
        
        memory = MemoryItem(
            id=memory_id,
            type=memory_type.value,
            title=title,
            content=content,
            tags=tags or [],
            priority=priority.value,
            created_at=time.time(),
            updated_at=time.time(),
            remind_at=remind_at,
            reminder_method=reminder_method,
            category=category
        )
        
        self.memories[memory_id] = memory
        self._save_data()
        
        self.logger.info(f"📝 添加记忆: {memory_type.value} - {title}")
        
        return memory
    
    def search_memories(self, 
                       keyword: Union[str, List[str], None] = None,
                       memory_type: Optional[MemoryType] = None,
                       tags: Optional[List[str]] = None,
                       priority: Optional[Priority] = None) -> List[MemoryItem]:
        """
        搜索记忆
        
        Args:
            keyword: 关键词（字符串或列表，在标题和内容中搜索）
            memory_type: 记忆类型
            tags: 标签列表
            priority: 优先级
            
        Returns:
            List[MemoryItem]: 匹配的记忆列表
        """
        results = []
        
        for memory in self.memories.values():
            # 关键词搜索
            if keyword:
                if isinstance(keyword, list):
                    # 如果是列表，检查是否包含任一关键词
                    keyword_match = False
                    for kw in keyword:
                        if kw.lower() in memory.title.lower() or kw.lower() in memory.content.lower():
                            keyword_match = True
                            break
                    if not keyword_match:
                        continue
                else:
                    # 如果是字符串，直接搜索
                    if keyword.lower() not in memory.title.lower() and \
                       keyword.lower() not in memory.content.lower():
                        continue
            
            # 类型过滤
            if memory_type and memory.type != memory_type:
                continue
            
            # 标签过滤
            if tags and not any(tag in memory.tags for tag in tags):
                continue
            
            # 优先级过滤
            if priority and memory.priority != priority:
                continue
            
            results.append(memory)
        
        # 按优先级和创建时间排序
        results.sort(key=lambda m: (
            self._priority_weight(m.priority),
            -m.created_at
        ))
        
        return results
    
    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        """获取记忆"""
        return self.memories.get(memory_id)
    
    def update_memory(self, memory_id: str, **kwargs) -> bool:
        """
        更新记忆
        
        Args:
            memory_id: 记忆ID
            **kwargs: 要更新的字段
            
        Returns:
            bool: 是否成功
        """
        if memory_id not in self.memories:
            return False
        
        memory = self.memories[memory_id]
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        memory.updated_at = time.time()
        self._save_data()
        
        self.logger.info(f"📝 更新记忆: {memory_id}")
        
        return True
    
    def delete_memory(self, memory_id: str) -> bool:
        """删除记忆"""
        if memory_id not in self.memories:
            return False
        
        del self.memories[memory_id]
        self._save_data()
        
        self.logger.info(f"📝 删除记忆: {memory_id}")
        
        return True
    
    def get_upcoming_reminders(self) -> List[MemoryItem]:
        """获取即将到期的提醒"""
        now = time.time()
        upcoming = []
        
        for memory in self.memories.values():
            if memory.remind_at and memory.remind_at <= now:
                upcoming.append(memory)
        
        # 按提醒时间排序
        upcoming.sort(key=lambda m: m.remind_at or 0)
        
        return upcoming
    
    def _priority_weight(self, priority: Priority) -> int:
        """获取优先级权重"""
        weights = {
            Priority.LOW: 0,
            Priority.NORMAL: 1,
            Priority.HIGH: 2,
            Priority.URGENT: 3
        }
        return weights.get(priority, 1)
    
    def _load_data(self):
        """加载数据"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 加载导航状态
                    self.navigation_status = data.get('navigation_status', 'idle')
                    
                    for mem_data in data.get('memories', []):
                        memory = MemoryItem(
                            id=mem_data['id'],
                            type=MemoryType(mem_data['type']),
                            title=mem_data['title'],
                            content=mem_data['content'],
                            tags=mem_data['tags'],
                            priority=Priority(mem_data['priority']),
                            created_at=mem_data['created_at'],
                            updated_at=mem_data['updated_at'],
                            remind_at=mem_data.get('remind_at'),
                            reminder_method=mem_data['reminder_method'],
                            category=mem_data['category']
                        )
                        self.memories[memory.id] = memory
                    
                    self.logger.info(f"📂 加载了 {len(self.memories)} 条记忆")
        except Exception as e:
            self.logger.error(f"❌ 加载数据失败: {e}")
    
    def set_navigation_status(self, status: str):
        """
        设置导航状态
        
        Args:
            status: 导航状态 (idle/active/pending/cancelled)
        """
        self.navigation_status = status
        self.logger.info(f"🧭 导航状态已更新: {status}")
    
    def get_navigation_status(self) -> str:
        """获取导航状态"""
        return self.navigation_status
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                'memories': [mem.to_dict() for mem in self.memories.values()],
                'navigation_status': self.navigation_status
            }
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug("💾 记忆数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存数据失败: {e}")


# 全局存储器实例
global_memory_store = MemoryStore()

def add_memory(memory_type: MemoryType, title: str, content: str, **kwargs) -> MemoryItem:
    """添加记忆的便捷函数"""
    return global_memory_store.add_memory(memory_type, title, content, **kwargs)


if __name__ == "__main__":
    # 测试记忆存储器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    store = MemoryStore('data/test_memory.json')
    
    print("=" * 60)
    print("🧠 记忆存储器测试")
    print("=" * 60)
    
    # 添加服药记忆
    print("\n1. 添加服药记忆")
    med_memory = store.add_memory(
        MemoryType.MEDICATION,
        title="高血压药物",
        content="每天早晚各一次，每次一片",
        tags=["重要", "健康"],
        priority=Priority.URGENT,
        remind_at=time.time() + 3600,  # 1小时后提醒
        reminder_method="voice",
        category="health"
    )
    print(f"   ID: {med_memory.id}")
    print(f"   标题: {med_memory.title}")
    
    # 添加电话号码记忆
    print("\n2. 添加电话号码记忆")
    phone_memory = store.add_memory(
        MemoryType.PHONE,
        title="紧急联系人",
        content="13800138000",
        tags=["紧急", "联系人"],
        priority=Priority.HIGH,
        category="contact"
    )
    print(f"   ID: {phone_memory.id}")
    
    # 搜索记忆
    print("\n3. 搜索记忆")
    results = store.search_memories(keyword="重要")
    print(f"   找到 {len(results)} 条记忆")
    for memory in results:
        print(f"   - {memory.title}: {memory.content}")
    
    # 获取即将到期的提醒
    print("\n4. 获取即将到期的提醒")
    upcoming = store.get_upcoming_reminders()
    print(f"   即将到期: {len(upcoming)} 条")
    
    print("\n" + "=" * 60)


# 全局记忆存储实例
_global_memory_store: Optional[MemoryStore] = None

def get_memory_store() -> MemoryStore:
    """获取全局记忆存储实例"""
    global _global_memory_store
    if _global_memory_store is None:
        _global_memory_store = MemoryStore()
    return _global_memory_store
