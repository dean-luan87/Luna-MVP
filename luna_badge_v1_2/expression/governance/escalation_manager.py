"""
Escalation Manager (C-4.4)

升级机制

职责：
"现在是不是已经危险到必须打断用户？"

这是安全系统的最后一道防线。

升级等级（一期）：
1. 正常播报
2. 重复一次
3. 加强语气
4. 打断一切，强提醒
5. 连续播报 + 硬件配合
"""

from typing import Dict, Any


class EscalationManager:
    """
    升级管理器
    
    职责：
    - 判断表达紧急程度
    - 决定是否需要打断
    - 一期：规则驱动
    - 二期：可接入风险评估模型
    """
    
    def level(self, context: Dict[str, Any]) -> int:
        """
        获取升级等级
        
        升级等级（一期）：
        1. 正常播报
        2. 重复一次
        3. 加强语气
        4. 打断一切，强提醒
        5. 连续播报 + 硬件配合
        
        Args:
            context: 上下文（包含 collision_risk, high_urgency, urgency_level 等）
            
        Returns:
            int: 升级等级（1-5）
        """
        # 5. 碰撞风险（最高等级）
        if context.get("collision_risk", False):
            return 5
        
        # 4. 高紧急度
        if context.get("high_urgency", False):
            return 4
        
        # 根据 urgency_level 判断
        urgency_level = context.get("urgency_level", 1)
        if urgency_level >= 5:
            return 5
        elif urgency_level >= 4:
            return 4
        elif urgency_level >= 3:
            return 3
        elif urgency_level >= 2:
            return 2
        else:
            return 1
    
    def should_interrupt(self, level: int) -> bool:
        """
        判断是否需要打断
        
        Args:
            level: 升级等级
            
        Returns:
            bool: True 表示需要打断
        """
        return level >= 4
    
    def should_repeat(self, level: int) -> bool:
        """
        判断是否需要重复
        
        Args:
            level: 升级等级
            
        Returns:
            bool: True 表示需要重复
        """
        return level >= 2
