#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 上下文记忆缓存机制 (Context Store)
管理上下文指令记忆，支持追问识别和会话状态保持
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class ContextEntry:
    """上下文条目"""
    timestamp: str
    user_input: str
    intent: str
    system_response: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class ContextStore:
    """上下文存储器"""
    
    def __init__(self, max_entries: int = 5):
        """
        初始化上下文存储器
        
        Args:
            max_entries: 最大条目数
        """
        self.max_entries = max_entries
        self.entries = deque(maxlen=max_entries)
        
        # 持久化数据
        self.user_preferences = {}
        self.last_destination = None
        self.last_location = None
        
        logger.info(f"🧠 上下文存储器初始化 (最大条目: {max_entries})")
    
    def add_entry(self,
                  user_input: str,
                  intent: str,
                  system_response: str,
                  metadata: Optional[Dict[str, Any]] = None):
        """
        添加上下文条目
        
        Args:
            user_input: 用户输入
            intent: 意图
            system_response: 系统响应
            metadata: 额外元数据
        """
        entry = ContextEntry(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            intent=intent,
            system_response=system_response,
            metadata=metadata or {}
        )
        
        self.entries.append(entry)
        
        logger.debug(f"📝 添加上下文: {intent} - {user_input[:30]}")
        
        # 更新持久化数据
        self._update_persistent_data(intent, metadata)
    
    def _update_persistent_data(self, intent: str, metadata: Optional[Dict[str, Any]]):
        """更新持久化数据"""
        if not metadata:
            return
        
        # 更新目的地
        if "destination" in metadata:
            self.last_destination = metadata["destination"]
        
        # 更新位置
        if "location" in metadata:
            self.last_location = metadata["location"]
    
    def get_last_intent(self) -> Optional[str]:
        """获取上一次意图"""
        if self.entries:
            return self.entries[-1].intent
        return None
    
    def get_last_destination(self) -> Optional[str]:
        """获取上一次目的地"""
        if self.last_destination:
            return self.last_destination
        
        # 从条目中查找
        for entry in reversed(self.entries):
            if "destination" in entry.metadata:
                return entry.metadata["destination"]
        
        return None
    
    def get_last_location(self) -> Optional[str]:
        """获取上一次位置"""
        if self.last_location:
            return self.last_location
        
        # 从条目中查找
        for entry in reversed(self.entries):
            if "location" in entry.metadata:
                return entry.metadata["location"]
        
        return None
    
    def resolve_question(self, text: str) -> Optional[Any]:
        """
        解析追问
        
        Args:
            text: 用户输入文本
            
        Returns:
            解析结果或None
        """
        text_lower = text.lower()
        
        # 追问关键词
        question_keywords = ["上次", "刚才", "之前", "那个", "那里"]
        
        for keyword in question_keywords:
            if keyword in text_lower:
                return self._resolve_from_context(text_lower, keyword)
        
        return None
    
    def _resolve_from_context(self, text: str, keyword: str) -> Optional[Any]:
        """从上下文解析"""
        # "上次那个" -> 上一个目的地
        if keyword in ["上次", "刚才", "之前"] and "那个" in text:
            return self.get_last_destination()
        
        # "那个医院" -> 上一次的地点
        if "医院" in text or "地点" in text or "地方" in text:
            return self.get_last_location()
        
        # "刚才的" -> 上一个意图
        if keyword in ["刚才", "之前"]:
            return self.get_last_intent()
        
        return None
    
    def get_context_summary(self) -> Dict[str, Any]:
        """获取上下文摘要"""
        return {
            "total_entries": len(self.entries),
            "last_intent": self.get_last_intent(),
            "last_destination": self.get_last_destination(),
            "last_location": self.get_last_location(),
            "recent_entries": [entry.to_dict() for entry in list(self.entries)[-3:]]
        }
    
    def get_entries(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取条目列表"""
        entries = list(self.entries)
        
        if limit:
            entries = entries[-limit:]
        
        return [entry.to_dict() for entry in entries]
    
    def clear(self):
        """清空上下文"""
        self.entries.clear()
        self.last_destination = None
        self.last_location = None
        
        logger.info("🗑️ 上下文已清空")
    
    def is_question_follow_up(self, text: str) -> bool:
        """
        判断是否为追问
        
        Args:
            text: 用户输入文本
            
        Returns:
            是否为追问
        """
        question_keywords = ["上次", "刚才", "之前", "那个", "那里", "还是", "也是"]
        text_lower = text.lower()
        
        for keyword in question_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def extract_intent_with_context(self, text: str, base_intent: str) -> str:
        """
        结合上下文提取意图
        
        Args:
            text: 用户输入文本
            base_intent: 基础意图
            
        Returns:
            增强后的意图字符串
        """
        # 如果是追问
        if self.is_question_follow_up(text):
            resolved = self.resolve_question(text)
            
            if resolved:
                return f"{base_intent}:[context={resolved}]"
        
        return base_intent


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建上下文存储器
    context_store = ContextStore(max_entries=5)
    
    print("=" * 70)
    print("🧠 测试上下文记忆缓存机制")
    print("=" * 70)
    
    # 模拟对话
    print("\n💬 模拟对话序列:")
    print("-" * 70)
    
    # 第一轮
    print("\n1️⃣ 用户: '我要去虹口医院'")
    context_store.add_entry(
        user_input="我要去虹口医院",
        intent="find_destination",
        system_response="已开始导航至虹口医院",
        metadata={"destination": "虹口医院", "location": "虹口医院"}
    )
    print("   ✅ 已记录上下文")
    
    # 第二轮
    print("\n2️⃣ 用户: '上次那个' (追问)")
    is_followup = context_store.is_question_follow_up("上次那个")
    print(f"   是否追问: {is_followup}")
    
    if is_followup:
        resolved = context_store.resolve_question("上次那个")
        print(f"   🔍 解析结果: {resolved}")
    
    # 第三轮
    print("\n3️⃣ 用户: '去那个医院' (带上下文的意图)")
    enhanced_intent = context_store.extract_intent_with_context(
        "去那个医院",
        "find_destination"
    )
    print(f"   增强意图: {enhanced_intent}")
    
    # 第四轮
    print("\n4️⃣ 用户: '305号诊室'")
    context_store.add_entry(
        user_input="305号诊室",
        intent="find_destination",
        system_response="已开始导航至305号诊室",
        metadata={"destination": "305号诊室"}
    )
    print("   ✅ 已记录上下文")
    
    # 查看上下文摘要
    print("\n📊 上下文摘要:")
    print("-" * 70)
    summary = context_store.get_context_summary()
    for key, value in summary.items():
        if key != "recent_entries":
            print(f"   {key}: {value}")
    
    # 查看最近条目
    print("\n📝 最近条目:")
    entries = context_store.get_entries(limit=3)
    for i, entry in enumerate(entries, 1):
        print(f"   {i}. [{entry['intent']}] {entry['user_input']}")
    
    print("\n✅ 测试完成")

