#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆调用与提醒机制模块
根据上下文主动提醒用户或被动调用信息
"""

import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime, timedelta

try:
    from .memory_store import MemoryStore, MemoryItem, MemoryType, Priority, MemoryStatus
except ImportError:
    from memory_store import MemoryStore, MemoryItem, MemoryType, Priority, MemoryStatus

logger = logging.getLogger(__name__)

class ReminderFormat(Enum):
    """提醒格式"""
    NORMAL = "normal"            # 正常
    URGENT = "urgent"           # 紧急
    GENTLE = "gentle"           # 温和
    REPEAT = "repeat"           # 重复

@dataclass
class ReminderMessage:
    """提醒消息"""
    title: str                   # 标题
    content: str                 # 内容
    format: ReminderFormat       # 格式
    priority: Priority           # 优先级
    repeat_count: int            # 重复次数
    
    def to_tts(self) -> str:
        """转换为TTS文本"""
        priority_prefix = {
            Priority.URGENT: "紧急",
            Priority.HIGH: "重要",
            Priority.NORMAL: "",
            Priority.LOW: ""
        }.get(self.priority, "")
        
        prefix = f"{priority_prefix}，" if priority_prefix else ""
        
        return f"{prefix}{self.title}：{self.content}"

class MemoryCaller:
    """记忆调用器"""
    
    def __init__(self, memory_store: MemoryStore):
        """
        初始化记忆调用器
        
        Args:
            memory_store: 记忆存储器
        """
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        self.last_reminder_time = {}
        
        self.logger.info("🔔 记忆调用器初始化完成")
    
    def check_reminders(self) -> List[ReminderMessage]:
        """
        检查并生成提醒消息
        
        Returns:
            List[ReminderMessage]: 提醒消息列表
        """
        reminders = []
        
        # 获取即将到期的提醒
        upcoming = self.memory_store.get_upcoming_reminders()
        
        for memory in upcoming:
            # 检查是否应该提醒
            if self._should_remind(memory):
                reminder = self._create_reminder_message(memory)
                reminders.append(reminder)
                
                # 更新最后提醒时间
                self.last_reminder_time[memory.id] = time.time()
        
        return reminders
    
    def search_fuzzy(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """
        模糊搜索记忆
        
        Args:
            query: 查询字符串
            limit: 结果数量限制
            
        Returns:
            List[MemoryItem]: 匹配的记忆列表
        """
        all_memories = list(self.memory_store.memories.values())
        
        # 计算相似度
        scored_memories = []
        for memory in all_memories:
            # 计算标题和内容的相似度
            title_score = self._calculate_similarity(query, memory.title)
            content_score = self._calculate_similarity(query, memory.content)
            tag_score = max([
                self._calculate_similarity(query, tag) 
                for tag in memory.tags
            ] + [0])
            
            # 综合评分
            score = max(title_score, content_score * 0.5, tag_score)
            
            if score > 0.3:  # 相似度阈值
                scored_memories.append((score, memory))
        
        # 按相似度排序
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # 返回前limit个结果
        return [mem for _, mem in scored_memories[:limit]]
    
    def search_by_keyword(self, keywords: List[str]) -> List[MemoryItem]:
        """
        关键词搜索
        
        Args:
            keywords: 关键词列表
            
        Returns:
            List[MemoryItem]: 匹配的记忆列表
        """
        results = []
        
        for memory in self.memory_store.memories.values():
            # 检查是否包含任何关键词
            if any(
                keyword in memory.title or 
                keyword in memory.content or 
                keyword in memory.category
                for keyword in keywords
            ):
                results.append(memory)
        
        return results
    
    def get_contextual_reminders(self, context: Dict[str, Any]) -> List[ReminderMessage]:
        """
        根据上下文生成提醒
        
        Args:
            context: 上下文信息（如时间、位置等）
            
        Returns:
            List[ReminderMessage]: 提醒消息列表
        """
        reminders = []
        
        # 检查当前时间
        current_hour = time.localtime().tm_hour
        
        # 早晨提醒（7-9点）
        if 7 <= current_hour <= 9:
            # 检查是否有早晨服药提醒
            med_memories = self.memory_store.search_memories(
                memory_type=MemoryType.MEDICATION
            )
            for memory in med_memories:
                if "早" in memory.content or "morning" in memory.content.lower():
                    reminder = self._create_reminder_message(
                        memory, 
                        custom_title="早晨服药提醒"
                    )
                    reminders.append(reminder)
        
        # 中午提醒（11-13点）
        if 11 <= current_hour <= 13:
            # 检查是否有事件提醒
            event_memories = self.memory_store.search_memories(
                memory_type=MemoryType.EVENT
            )
            for memory in event_memories:
                if memory.priority in [Priority.HIGH, Priority.URGENT]:
                    reminder = self._create_reminder_message(memory)
                    reminders.append(reminder)
        
        # 晚上提醒（18-20点）
        if 18 <= current_hour <= 20:
            # 检查是否有晚上服药提醒
            med_memories = self.memory_store.search_memories(
                memory_type=MemoryType.MEDICATION
            )
            for memory in med_memories:
                if "晚" in memory.content or "night" in memory.content.lower():
                    reminder = self._create_reminder_message(
                        memory,
                        custom_title="晚上服药提醒"
                    )
                    reminders.append(reminder)
        
        return reminders
    
    def _should_remind(self, memory: MemoryItem) -> bool:
        """判断是否应该提醒"""
        if not memory.remind_at:
            return False
        
        # 检查提醒时间
        now = time.time()
        if now < memory.remind_at:
            return False
        
        # 检查重复间隔
        last_time = self.last_reminder_time.get(memory.id, 0)
        
        # 根据优先级设置重复间隔
        intervals = {
            Priority.URGENT: 300,      # 5分钟
            Priority.HIGH: 1800,       # 30分钟
            Priority.NORMAL: 3600,     # 1小时
            Priority.LOW: 7200         # 2小时
        }
        
        interval = intervals.get(memory.priority, 3600)
        
        if now - last_time < interval:
            return False
        
        return True
    
    def _create_reminder_message(self, 
                                 memory: MemoryItem,
                                 custom_title: Optional[str] = None) -> ReminderMessage:
        """
        创建提醒消息
        
        Args:
            memory: 记忆项
            custom_title: 自定义标题
            
        Returns:
            ReminderMessage: 提醒消息
        """
        # 确定提醒格式
        format_map = {
            Priority.URGENT: ReminderFormat.URGENT,
            Priority.HIGH: ReminderFormat.NORMAL,
            Priority.NORMAL: ReminderFormat.GENTLE,
            Priority.LOW: ReminderFormat.GENTLE
        }
        
        format_type = format_map.get(memory.priority, ReminderFormat.NORMAL)
        
        return ReminderMessage(
            title=custom_title or memory.title,
            content=memory.content,
            format=format_type,
            priority=memory.priority,
            repeat_count=1 if memory.priority in [Priority.URGENT, Priority.HIGH] else 0
        )
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """
        计算两个字符串的相似度
        
        Args:
            s1: 字符串1
            s2: 字符串2
            
        Returns:
            float: 相似度 (0-1)
        """
        s1_lower = s1.lower()
        s2_lower = s2.lower()
        
        # 使用SequenceMatcher计算相似度
        matcher = difflib.SequenceMatcher(None, s1_lower, s2_lower)
        return matcher.ratio()


def check_reminders(memory_store: MemoryStore) -> List[ReminderMessage]:
    """检查提醒的便捷函数"""
    caller = MemoryCaller(memory_store)
    return caller.check_reminders()


if __name__ == "__main__":
    # 测试记忆调用器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from memory_store import MemoryStore
    
    store = MemoryStore('data/test_memory.json')
    caller = MemoryCaller(store)
    
    print("=" * 60)
    print("🔔 记忆调用器测试")
    print("=" * 60)
    
    # 测试模糊搜索
    print("\n1. 模糊搜索测试")
    query = "服药"
    results = caller.search_fuzzy(query)
    print(f"   查询: '{query}'")
    print(f"   找到 {len(results)} 条记忆")
    for memory in results:
        print(f"   - {memory.title}: {memory.content}")
    
    # 测试关键词搜索
    print("\n2. 关键词搜索测试")
    keywords = ["紧急", "重要"]
    results = caller.search_by_keyword(keywords)
    print(f"   关键词: {keywords}")
    print(f"   找到 {len(results)} 条记忆")
    
    # 测试提醒检查
    print("\n3. 提醒检查测试")
    reminders = caller.check_reminders()
    print(f"   检查到 {len(reminders)} 个提醒")
    for reminder in reminders:
        print(f"   - {reminder.to_tts()}")
    
    # 测试上下文提醒
    print("\n4. 上下文提醒测试")
    context = {"time": time.time()}
    reminders = caller.get_contextual_reminders(context)
    print(f"   上下文提醒: {len(reminders)} 个")
    for reminder in reminders:
        print(f"   - {reminder.to_tts()}")
    
    print("\n" + "=" * 60)
