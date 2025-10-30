#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆项构建器模块
用户语音输入 → 转换为结构化记忆项
"""

import logging
import re
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class IntentType(Enum):
    """意图类型"""
    CREATE_MEMORY = "create_memory"         # 新增记忆
    MODIFY_MEMORY = "modify_memory"         # 修改记忆
    PAUSE_MEMORY = "pause_memory"           # 暂停记忆
    RESUME_MEMORY = "resume_memory"         # 恢复记忆
    DELETE_MEMORY = "delete_memory"         # 删除记忆
    UNKNOWN = "unknown"                     # 未知

@dataclass
class ExtractedInfo:
    """提取的信息"""
    content: str                    # 内容
    trigger_time: Optional[str]    # 触发时间
    repeat: Optional[str]          # 重复周期
    tags: List[str]                # 标签
    intent: IntentType            # 意图
    confidence: float              # 置信度

class MemoryEntryBuilder:
    """记忆项构建器"""
    
    def __init__(self):
        """初始化记忆项构建器"""
        self.logger = logging.getLogger(__name__)
        
        # 时间关键词映射
        self.time_keywords = {
            "早上": "08:00", "上午": "09:00", "中午": "12:00",
            "下午": "14:00", "晚上": "20:00", "凌晨": "01:00",
            "早晨": "07:00", "傍晚": "18:00", "深夜": "23:00"
        }
        
        # 频率关键词映射
        self.repeat_keywords = {
            "每天": "daily", "每周": "weekly", "每月": "monthly",
            "工作日": "weekday", "周末": "weekend", "一次": "none",
            "不再": "none", "暂停": "paused"
        }
        
        # 行为类型关键词
        self.action_keywords = {
            "吃药": ["吃药", "服药", "用药"],
            "吃饭": ["吃饭", "用餐", "进食"],
            "喝水": ["喝水", "饮水"],
            "睡觉": ["睡觉", "休息"],
            "锻炼": ["锻炼", "运动", "健身"],
            "开会": ["开会", "会议"],
            "提醒": ["提醒", "记得"],
            "吃药": ["吃药", "降压药", "药"]
        }
        
        # 对象关键词（如"我妈"、"小张"）
        self.object_keywords = {
            "妈", "爸", "老", "小", "我"
        }
        
        self.logger.info("🏗️ 记忆项构建器初始化完成")
    
    def parse_voice_input(self, voice_text: str) -> Dict[str, Any]:
        """
        解析语音输入，构建记忆项
        
        Args:
            voice_text: 语音文本
            
        Returns:
            Dict[str, Any]: 结构化记忆项
        """
        # 识别意图
        intent = self._detect_intent(voice_text)
        
        # 提取关键信息
        info = self._extract_info(voice_text)
        
        # 构建记忆项
        memory_item = self._build_memory_item(intent, info, voice_text)
        
        self.logger.info(f"🏗️ 识别意图: {intent.value}, "
                        f"置信度: {info.confidence:.2f}")
        
        return memory_item
    
    def _detect_intent(self, voice_text: str) -> IntentType:
        """检测用户意图"""
        voice_text_lower = voice_text.lower()
        
        # 新增记忆
        if any(kw in voice_text_lower for kw in ["提醒我", "记得", "帮我记", "新增"]):
            return IntentType.CREATE_MEMORY
        
        # 修改记忆
        elif any(kw in voice_text_lower for kw in ["不是", "改成", "修改", "应该"]):
            return IntentType.MODIFY_MEMORY
        
        # 暂停记忆
        elif any(kw in voice_text_lower for kw in ["不用", "暂停", "取消", "不要提醒"]):
            return IntentType.PAUSE_MEMORY
        
        # 恢复记忆
        elif any(kw in voice_text_lower for kw in ["恢复", "继续提醒", "还是提醒"]):
            return IntentType.RESUME_MEMORY
        
        # 删除记忆
        elif any(kw in voice_text_lower for kw in ["删除", "忘记", "不要"]):
            return IntentType.DELETE_MEMORY
        
        else:
            return IntentType.UNKNOWN
    
    def _extract_info(self, voice_text: str) -> ExtractedInfo:
        """提取关键信息"""
        content = voice_text
        trigger_time = None
        repeat = None
        tags = []
        confidence = 0.0
        
        # 提取时间
        trigger_time = self._extract_time(voice_text)
        
        # 提取频率
        repeat = self._extract_repeat(voice_text)
        
        # 提取标签
        tags = self._extract_tags(voice_text)
        
        # 提取行为类型（用于内容优化）
        action_type = self._extract_action_type(voice_text)
        if action_type:
            if action_type not in tags:
                tags.insert(0, action_type)
        
        # 计算置信度
        confidence = self._calculate_confidence(voice_text, trigger_time, repeat, tags)
        
        return ExtractedInfo(
            content=content,
            trigger_time=trigger_time,
            repeat=repeat,
            tags=tags,
            intent=IntentType.UNKNOWN,
            confidence=confidence
        )
    
    def _extract_time(self, text: str) -> Optional[str]:
        """提取时间"""
        # 尝试提取具体时间（如 "20:00", "8点"）
        time_pattern = r'(\d{1,2}):(\d{2})|(\d{1,2})点'
        match = re.search(time_pattern, text)
        if match:
            if match.group(1):  # 20:00格式
                return match.group(0)
            else:  # 8点格式
                hour = int(match.group(3))
                return f"{hour:02d}:00"
        
        # 尝试关键词匹配
        for keyword, time_str in self.time_keywords.items():
            if keyword in text:
                return time_str
        
        return None
    
    def _extract_repeat(self, text: str) -> Optional[str]:
        """提取重复周期"""
        for keyword, repeat_str in self.repeat_keywords.items():
            if keyword in text:
                return repeat_str
        
        return None
    
    def _extract_tags(self, text: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 从行为关键词中提取
        for action_type, keywords in self.action_keywords.items():
            if any(kw in text for kw in keywords):
                if action_type not in tags:
                    tags.append(action_type)
        
        # 提取对象关键词
        for obj in self.object_keywords:
            if obj in text:
                tags.append(obj)
        
        # 提取情绪/健康相关
        health_keywords = ["健康", "治疗", "康复", "病情"]
        for kw in health_keywords:
            if kw in text:
                tags.append("健康")
                break
        
        return tags
    
    def _extract_action_type(self, text: str) -> Optional[str]:
        """提取行为类型"""
        for action_type, keywords in self.action_keywords.items():
            if any(kw in text for kw in keywords):
                return action_type
        
        return None
    
    def _calculate_confidence(self, text: str, time: Optional[str], 
                             repeat: Optional[str], tags: List[str]) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        if time:
            confidence += 0.2
        
        if repeat:
            confidence += 0.15
        
        if len(tags) > 0:
            confidence += 0.15
        
        # 检查是否包含明确的意图词
        if any(kw in text for kw in ["提醒", "记得", "吃药", "吃药"]):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _build_memory_item(self, intent: IntentType, info: ExtractedInfo, 
                          raw_input: str) -> Dict[str, Any]:
        """构建记忆项"""
        import uuid
        from datetime import datetime
        
        # 生成ID
        memory_id = f"m_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:3]}"
        
        # 当前时间戳
        now = datetime.now().isoformat()
        
        memory_item = {
            "id": memory_id,
            "type": "reminder",  # 默认类型
            "content": info.content,
            "trigger_time": info.trigger_time,
            "repeat": info.repeat or "none",
            "status": "active",
            "tags": info.tags,
            "created_at": now,
            "last_modified": now,
            "feedback_history": [],
            "intent": intent.value,
            "confidence": info.confidence
        }
        
        return memory_item


# 全局构建器实例
global_builder = MemoryEntryBuilder()

def parse_voice_input(voice_text: str) -> Dict[str, Any]:
    """解析语音输入，构建记忆项"""
    return global_builder.parse_voice_input(voice_text)


if __name__ == "__main__":
    # 测试记忆项构建器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    builder = MemoryEntryBuilder()
    
    print("=" * 70)
    print("🏗️ 记忆项构建器测试")
    print("=" * 70)
    
    test_cases = [
        "提醒我晚上8点吃降压药",
        "不是晚上，是早上8点吃药",
        "不用再提醒我吃药了",
        "还是提醒我吃药吧",
        "帮我记得明天要开会"
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试{i}: {test}")
        result = builder.parse_voice_input(test)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 70)


