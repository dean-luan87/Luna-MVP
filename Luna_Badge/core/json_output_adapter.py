#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge JSON输出适配器
统一所有模块的输出格式
"""

import json
import time
from typing import Dict, Any, Optional
from enum import Enum

class OutputLevel(Enum):
    """输出级别"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class JSONOutputAdapter:
    """JSON输出适配器"""
    
    @staticmethod
    def format_output(event: str, level: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化输出为统一JSON格式
        
        Args:
            event: 事件名称
            level: 级别 (low/medium/high)
            data: 数据
            
        Returns:
            Dict[str, Any]: 格式化的输出
        """
        return {
            "event": event,
            "level": level,
            "data": data,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    
    @staticmethod
    def output_to_json(output: Dict[str, Any], pretty: bool = False) -> str:
        """
        将输出转换为JSON字符串
        
        Args:
            output: 输出字典
            pretty: 是否美化输出
            
        Returns:
            str: JSON字符串
        """
        if pretty:
            return json.dumps(output, ensure_ascii=False, indent=2)
        else:
            return json.dumps(output, ensure_ascii=False)
    
    @staticmethod
    def vision_detection(objects: list, signboards: list, hazards: list) -> Dict[str, Any]:
        """视觉检测输出"""
        return JSONOutputAdapter.format_output(
            event="vision_detection",
            level="medium",
            data={
                "objects": objects,
                "signboards": signboards,
                "hazards": hazards
            }
        )
    
    @staticmethod
    def path_analysis(crowd_density: str, flow_direction: str, 
                      queue_detected: bool, hazards: list) -> Dict[str, Any]:
        """路径分析输出"""
        return JSONOutputAdapter.format_output(
            event="path_analysis",
            level="medium",
            data={
                "crowd_density": crowd_density,
                "flow_direction": flow_direction,
                "queue_detected": queue_detected,
                "hazards": hazards
            }
        )
    
    @staticmethod
    def speech_broadcast(text: str, style: str, voice: str, 
                        rate: float, pitch: float) -> Dict[str, Any]:
        """语音播报输出"""
        return JSONOutputAdapter.format_output(
            event="speech_broadcast",
            level="high",
            data={
                "text": text,
                "style": style,
                "voice": voice,
                "rate": rate,
                "pitch": pitch
            }
        )
    
    @staticmethod
    def user_interaction(interaction_type: str, intent: str, 
                        confidence: float, user_response: str) -> Dict[str, Any]:
        """用户交互输出"""
        return JSONOutputAdapter.format_output(
            event="user_interaction",
            level="medium",
            data={
                "type": interaction_type,
                "intent": intent,
                "confidence": confidence,
                "user_response": user_response
            }
        )


def format_output(event: str, level: str, data: Dict[str, Any]) -> str:
    """
    格式化输出为JSON字符串
    
    Args:
        event: 事件名称
        level: 级别
        data: 数据
        
    Returns:
        str: JSON字符串
    """
    adapter = JSONOutputAdapter()
    output = adapter.format_output(event, level, data)
    return adapter.output_to_json(output, pretty=True)


# 使用示例
if __name__ == "__main__":
    # 测试JSON输出适配器
    adapter = JSONOutputAdapter()
    
    # 视觉检测输出
    vision_output = adapter.vision_detection(
        objects=[{"type": "person", "position": [100, 200], "confidence": 0.9}],
        signboards=[{"type": "toilet", "text": "洗手间"}],
        hazards=[{"type": "water", "severity": "high"}]
    )
    print("视觉检测输出:")
    print(json.dumps(vision_output, ensure_ascii=False, indent=2))
    
    # 路径分析输出
    path_output = adapter.path_analysis(
        crowd_density="crowded",
        flow_direction="counter",
        queue_detected=True,
        hazards=[{"type": "water", "severity": "high"}]
    )
    print("\n路径分析输出:")
    print(json.dumps(path_output, ensure_ascii=False, indent=2))


