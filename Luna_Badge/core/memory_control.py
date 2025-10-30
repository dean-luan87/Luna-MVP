#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆控制模块
记忆修改与暂停管理
"""

import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ControlAction(Enum):
    """控制动作"""
    MODIFY = "modify"           # 修改
    PAUSE = "pause"            # 暂停
    RESUME = "resume"           # 恢复
    DELETE = "delete"          # 删除
    UPDATE_TAGS = "update_tags"  # 更新标签

@dataclass
class ControlResult:
    """控制结果"""
    action: ControlAction
    memory_id: str
    success: bool
    message: str
    updated_memory: Optional[Dict[str, Any]] = None

class MemoryControl:
    """记忆控制器"""
    
    def __init__(self, memory_store):
        """
        初始化记忆控制器
        
        Args:
            memory_store: 记忆存储器实例
        """
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        
        self.logger.info("🎛️ 记忆控制器初始化完成")
    
    def modify_memory(self, memory_id: str, updates: Dict[str, Any], 
                     raw_input: str) -> ControlResult:
        """
        修改记忆项
        
        Args:
            memory_id: 记忆ID
            updates: 更新内容
            raw_input: 原始输入
            
        Returns:
            ControlResult: 控制结果
        """
        try:
            memory = self.memory_store.get_memory(memory_id)
            
            if not memory:
                return ControlResult(
                    action=ControlAction.MODIFY,
                    memory_id=memory_id,
                    success=False,
                    message=f"记忆项 {memory_id} 不存在"
                )
            
            # 记录反馈历史
            feedback_record = {
                "action": "modified",
                "reason": "用户语音修改",
                "timestamp": datetime.now().isoformat(),
                "raw_input": raw_input,
                "changes": updates
            }
            
            # 更新记忆项
            memory["last_modified"] = datetime.now().isoformat()
            
            # 应用更新
            for key, value in updates.items():
                if key in memory:
                    memory[key] = value
            
            # 添加反馈记录
            if "feedback_history" not in memory:
                memory["feedback_history"] = []
            memory["feedback_history"].append(feedback_record)
            
            # 保存
            self.memory_store.save_memory(memory_id, memory)
            
            self.logger.info(f"🎛️ 记忆项 {memory_id} 已修改: {updates}")
            
            return ControlResult(
                action=ControlAction.MODIFY,
                memory_id=memory_id,
                success=True,
                message="修改成功",
                updated_memory=memory
            )
            
        except Exception as e:
            self.logger.error(f"⚠️ 修改记忆失败: {e}")
            return ControlResult(
                action=ControlAction.MODIFY,
                memory_id=memory_id,
                success=False,
                message=f"修改失败: {str(e)}"
            )
    
    def pause_memory(self, memory_id: str, reason: str, raw_input: str) -> ControlResult:
        """
        暂停记忆提醒
        
        Args:
            memory_id: 记忆ID
            reason: 暂停原因
            raw_input: 原始输入
            
        Returns:
            ControlResult: 控制结果
        """
        try:
            memory = self.memory_store.get_memory(memory_id)
            
            if not memory:
                return ControlResult(
                    action=ControlAction.PAUSE,
                    memory_id=memory_id,
                    success=False,
                    message=f"记忆项 {memory_id} 不存在"
                )
            
            # 更新状态
            memory["status"] = "paused"
            memory["last_modified"] = datetime.now().isoformat()
            
            # 记录反馈历史
            feedback_record = {
                "action": "paused",
                "reason": reason or "用户主动取消",
                "timestamp": datetime.now().isoformat(),
                "raw_input": raw_input
            }
            
            if "feedback_history" not in memory:
                memory["feedback_history"] = []
            memory["feedback_history"].append(feedback_record)
            
            # 保存
            self.memory_store.save_memory(memory_id, memory)
            
            self.logger.info(f"🎛️ 记忆项 {memory_id} 已暂停")
            
            return ControlResult(
                action=ControlAction.PAUSE,
                memory_id=memory_id,
                success=True,
                message="暂停成功",
                updated_memory=memory
            )
            
        except Exception as e:
            self.logger.error(f"⚠️ 暂停记忆失败: {e}")
            return ControlResult(
                action=ControlAction.PAUSE,
                memory_id=memory_id,
                success=False,
                message=f"暂停失败: {str(e)}"
            )
    
    def resume_memory(self, memory_id: str, reason: str, raw_input: str) -> ControlResult:
        """
        恢复记忆提醒
        
        Args:
            memory_id: 记忆ID
            reason: 恢复原因
            raw_input: 原始输入
            
        Returns:
            ControlResult: 控制结果
        """
        try:
            memory = self.memory_store.get_memory(memory_id)
            
            if not memory:
                return ControlResult(
                    action=ControlAction.RESUME,
                    memory_id=memory_id,
                    success=False,
                    message=f"记忆项 {memory_id} 不存在"
                )
            
            # 更新状态
            memory["status"] = "active"
            memory["last_modified"] = datetime.now().isoformat()
            
            # 记录反馈历史
            feedback_record = {
                "action": "resumed",
                "reason": reason or "用户主动恢复",
                "timestamp": datetime.now().isoformat(),
                "raw_input": raw_input
            }
            
            if "feedback_history" not in memory:
                memory["feedback_history"] = []
            memory["feedback_history"].append(feedback_record)
            
            # 保存
            self.memory_store.save_memory(memory_id, memory)
            
            self.logger.info(f"🎛️ 记忆项 {memory_id} 已恢复")
            
            return ControlResult(
                action=ControlAction.RESUME,
                memory_id=memory_id,
                success=True,
                message="恢复成功",
                updated_memory=memory
            )
            
        except Exception as e:
            self.logger.error(f"⚠️ 恢复记忆失败: {e}")
            return ControlResult(
                action=ControlAction.RESUME,
                memory_id=memory_id,
                success=False,
                message=f"恢复失败: {str(e)}"
            )
    
    def update_tags(self, memory_id: str, tags: List[str], raw_input: str) -> ControlResult:
        """
        更新标签
        
        Args:
            memory_id: 记忆ID
            tags: 新标签列表
            raw_input: 原始输入
            
        Returns:
            ControlResult: 控制结果
        """
        try:
            memory = self.memory_store.get_memory(memory_id)
            
            if not memory:
                return ControlResult(
                    action=ControlAction.UPDATE_TAGS,
                    memory_id=memory_id,
                    success=False,
                    message=f"记忆项 {memory_id} 不存在"
                )
            
            # 更新标签
            memory["tags"] = tags
            memory["last_modified"] = datetime.now().isoformat()
            
            # 记录反馈历史
            feedback_record = {
                "action": "tags_updated",
                "reason": "用户修改标签",
                "timestamp": datetime.now().isoformat(),
                "raw_input": raw_input,
                "new_tags": tags
            }
            
            if "feedback_history" not in memory:
                memory["feedback_history"] = []
            memory["feedback_history"].append(feedback_record)
            
            # 保存
            self.memory_store.save_memory(memory_id, memory)
            
            self.logger.info(f"🎛️ 记忆项 {memory_id} 标签已更新: {tags}")
            
            return ControlResult(
                action=ControlAction.UPDATE_TAGS,
                memory_id=memory_id,
                success=True,
                message="标签更新成功",
                updated_memory=memory
            )
            
        except Exception as e:
            self.logger.error(f"⚠️ 更新标签失败: {e}")
            return ControlResult(
                action=ControlAction.UPDATE_TAGS,
                memory_id=memory_id,
                success=False,
                message=f"更新标签失败: {str(e)}"
            )


# 全局控制器实例（需要传入memory_store）
global_memory_control = None

def get_memory_control(memory_store):
    """获取记忆控制器实例"""
    global global_memory_control
    if global_memory_control is None:
        global_memory_control = MemoryControl(memory_store)
    return global_memory_control


if __name__ == "__main__":
    # 测试记忆控制器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建模拟的记忆存储器
    class MockMemoryStore:
        def __init__(self):
            self.memories = {
                "m_001": {
                    "id": "m_001",
                    "type": "reminder",
                    "content": "晚上8点吃药",
                    "trigger_time": "20:00",
                    "repeat": "daily",
                    "status": "active",
                    "tags": ["吃药", "健康"],
                    "created_at": "2025-10-27T00:00:00",
                    "last_modified": "2025-10-27T00:00:00",
                    "feedback_history": []
                }
            }
        
        def get_memory(self, memory_id):
            return self.memories.get(memory_id)
        
        def save_memory(self, memory_id, memory):
            self.memories[memory_id] = memory
    
    store = MockMemoryStore()
    controller = MemoryControl(store)
    
    print("=" * 70)
    print("🎛️ 记忆控制器测试")
    print("=" * 70)
    
    # 测试1: 修改记忆
    print("\n测试1: 修改记忆")
    result = controller.modify_memory(
        "m_001",
        {"trigger_time": "08:00"},
        "不是晚上，是早上8点吃药"
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    
    # 测试2: 暂停记忆
    print("\n测试2: 暂停记忆")
    result = controller.pause_memory(
        "m_001",
        "用户语音取消",
        "不用再提醒我吃药了"
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    
    # 测试3: 恢复记忆
    print("\n测试3: 恢复记忆")
    result = controller.resume_memory(
        "m_001",
        "用户主动恢复",
        "还是提醒我吃药吧"
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    
    # 测试4: 更新标签
    print("\n测试4: 更新标签")
    result = controller.update_tags(
        "m_001",
        ["吃药", "降压药", "健康"],
        "添加新标签"
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    
    print("\n" + "=" * 70)

