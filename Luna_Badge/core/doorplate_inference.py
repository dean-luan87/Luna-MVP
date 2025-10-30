#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 门牌推理引擎模块
根据连续门牌信息判断用户行进方向是否正确
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
try:
    from .doorplate_reader import DoorplateInfo
except ImportError:
    from doorplate_reader import DoorplateInfo
import time

logger = logging.getLogger(__name__)

class MovementStatus(Enum):
    """运动状态"""
    FORWARD = "forward"            # 向前
    BACKWARD = "backward"          # 向后
    CORRECT = "correct"            # 正确方向
    WRONG = "wrong"               # 错误方向
    UNKNOWN = "unknown"           # 未知

@dataclass
class DirectionInference:
    """方向推理结果"""
    status: MovementStatus         # 运动状态
    message: str                   # 提示消息
    confidence: float              # 置信度
    expected_next: Optional[int]   # 期望的下一个门牌号
    timestamp: float               # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status.value,
            "message": self.message,
            "confidence": self.confidence,
            "expected_next": self.expected_next,
            "timestamp": self.timestamp
        }

class DoorplateInferenceEngine:
    """门牌推理引擎"""
    
    def __init__(self):
        """初始化推理引擎"""
        self.logger = logging.getLogger(__name__)
        
        # 历史记录
        self.history: List[DoorplateInfo] = []
        
        # 配置
        self.max_history = 10
        self.expected_step = 2  # 期望的门牌号步进
        
        self.logger.info("🧭 门牌推理引擎初始化完成")
    
    def infer_direction_enhanced(self, current_doorplate: DoorplateInfo, 
                                target_room: Optional[int] = None) -> Dict[str, Any]:
        """
        增强版方向推理，输出结构化信息
        
        Args:
            current_doorplate: 当前门牌信息
            target_room: 目标房间号（可选）
            
        Returns:
            Dict[str, Any]: 结构化推理结果
        """
        # 添加到历史
        self.history.append(current_doorplate)
        
        # 保留最近的历史
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # 如果历史不足，返回未知状态
        if len(self.history) < 2:
            return {
                "event": "doorplate_direction_analysis",
                "trend": "unknown",
                "confidence": 0.0,
                "is_approaching_target": False,
                "recommendation": "continue",
                "last_seen": None,
                "current_seen": str(current_doorplate.number) if current_doorplate.number else None,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        
        # 分析运动方向
        prev = self.history[-2]
        current = self.history[-1]
        
        # 判断趋势
        trend = self._determine_trend(prev, current)
        
        # 判断是否接近目标
        is_approaching_target = False
        if target_room and current.number:
            is_approaching_target = self._is_approaching_target(prev.number, current.number, target_room)
        
        # 生成建议
        recommendation = self._generate_recommendation(trend, is_approaching_target)
        
        # 计算置信度
        confidence = self._calculate_confidence(prev, current)
        
        result = {
            "event": "doorplate_direction_analysis",
            "trend": trend,
            "confidence": confidence,
            "is_approaching_target": is_approaching_target,
            "recommendation": recommendation,
            "last_seen": str(prev.number) if prev.number else None,
            "current_seen": str(current.number) if current.number else None,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        self.logger.info(f"🧭 方向推理: {trend}, 建议={recommendation}")
        
        return result
    
    def _determine_trend(self, prev: DoorplateInfo, current: DoorplateInfo) -> str:
        """判断趋势"""
        if not prev.number or not current.number:
            return "unknown"
        
        diff = current.number - prev.number
        
        if diff > 0:
            return "increasing"
        elif diff < 0:
            return "decreasing"
        else:
            return "stable"
    
    def _is_approaching_target(self, prev_num: Optional[int], current_num: Optional[int], 
                              target: int) -> bool:
        """判断是否接近目标"""
        if not prev_num or not current_num:
            return False
        
        prev_dist = abs(prev_num - target)
        current_dist = abs(current_num - target)
        
        return current_dist < prev_dist
    
    def _generate_recommendation(self, trend: str, is_approaching_target: bool) -> str:
        """生成建议"""
        if trend == "increasing" and is_approaching_target:
            return "continue"
        elif trend == "decreasing" and not is_approaching_target:
            return "turn_back"
        elif trend == "anomalous":
            return "check_direction"
        else:
            return "continue"
    
    def _calculate_confidence(self, prev: DoorplateInfo, current: DoorplateInfo) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        # 基于门牌号变化的合理性
        if prev.number and current.number:
            diff = abs(current.number - prev.number)
            if diff <= 2:  # 合理步进
                confidence += 0.3
            elif diff <= 5:  # 较大步进
                confidence += 0.1
            else:  # 异常跳跃
                confidence -= 0.2
        
        # 基于识别置信度
        avg_confidence = (prev.confidence + current.confidence) / 2
        confidence += avg_confidence * 0.2
        
        return max(0.0, min(1.0, confidence))
    
    def _analyze_movement(self) -> DirectionInference:
        """分析运动方向"""
        # 获取最近的两个门牌
        prev = self.history[-2]
        current = self.history[-1]
        
        # 只分析相同类型的门牌
        if prev.type != current.type:
            return DirectionInference(
                status=MovementStatus.UNKNOWN,
                message="门牌类型不同，无法推理方向",
                confidence=0.0,
                expected_next=None,
                timestamp=time.time()
            )
        
        # 检查是否有数字编号
        if prev.number is None or current.number is None:
            return DirectionInference(
                status=MovementStatus.UNKNOWN,
                message="门牌无数字编号，无法推理方向",
                confidence=0.0,
                expected_next=None,
                timestamp=time.time()
            )
        
        # 计算方向
        number_diff = current.number - prev.number
        
        if number_diff > 0:
            # 门牌号增加
            status = MovementStatus.FORWARD
            message = f"向前推进中（{prev.number} → {current.number}）"
            expected_next = current.number + self.expected_step
            confidence = 1.0 if abs(number_diff) <= 10 else 0.7
            
        elif number_diff < 0:
            # 门牌号减少
            status = MovementStatus.BACKWARD
            message = f"方向错误：门牌变小（{prev.number} → {current.number}），可能走错方向"
            expected_next = current.number - abs(number_diff)
            confidence = 0.9
            
        else:
            # 门牌号不变
            status = MovementStatus.UNKNOWN
            message = "门牌号未变化，请确认行进方向"
            expected_next = current.number + self.expected_step
            confidence = 0.3
        
        return DirectionInference(
            status=status,
            message=message,
            confidence=confidence,
            expected_next=expected_next,
            timestamp=time.time()
        )
    
    def get_movement_sequence(self) -> List[int]:
        """
        获取运动序列
        
        Returns:
            List[int]: 门牌号序列
        """
        sequence = []
        for doorplate in self.history:
            if doorplate.number is not None:
                sequence.append(doorplate.number)
        return sequence
    
    def reset(self):
        """重置引擎"""
        self.history = []
        self.logger.info("🔄 门牌推理引擎已重置")


# 全局推理引擎实例
global_inference_engine = DoorplateInferenceEngine()

def infer_direction(doorplate: DoorplateInfo) -> DirectionInference:
    """推理方向的便捷函数"""
    return global_inference_engine.infer_direction(doorplate)


if __name__ == "__main__":
    # 测试门牌推理引擎
    import logging
    logging.basicConfig(level=logging.INFO)
    
    engine = DoorplateInferenceEngine()
    
    print("=" * 60)
    print("🧭 门牌推理引擎测试")
    print("=" * 60)
    
    # 模拟向前走
    print("\n测试1: 向前走（501 → 509）")
    doorplate1 = DoorplateInfo("501室", None, (100, 50, 150, 100), 0.9, None, 501, time.time())
    doorplate2 = DoorplateInfo("509室", None, (100, 50, 150, 100), 0.9, None, 509, time.time())
    
    result1 = engine.infer_direction(doorplate1)
    result2 = engine.infer_direction(doorplate2)
    print(f"  状态: {result2.status.value}")
    print(f"  消息: {result2.message}")
    print(f"  期望下一个门牌: {result2.expected_next}")
    
    # 模拟走错方向
    print("\n测试2: 走错方向（509 → 501）")
    engine.reset()
    doorplate3 = DoorplateInfo("509室", None, (100, 50, 150, 100), 0.9, None, 509, time.time())
    doorplate4 = DoorplateInfo("501室", None, (100, 50, 150, 100), 0.9, None, 501, time.time())
    
    result3 = engine.infer_direction(doorplate3)
    result4 = engine.infer_direction(doorplate4)
    print(f"  状态: {result4.status.value}")
    print(f"  消息: {result4.message}")
    print(f"  置信度: {result4.confidence:.2f}")
    
    # 显示运动序列
    sequence = engine.get_movement_sequence()
    print(f"\n运动序列: {sequence}")
    
    print("\n" + "=" * 60)
