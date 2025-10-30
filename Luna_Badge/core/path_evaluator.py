#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 路径判断引擎模块
聚合多个感知模块输出，判断当前路径是否安全通行
"""

import logging
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

# 导入播报风格管理器（延迟导入，避免循环依赖）
def get_speech_style_manager():
    """获取播报风格管理器实例"""
    try:
        from core.speech_style_manager import get_speech_style
        return get_speech_style
    except ImportError:
        logger.warning("⚠️ 无法导入speech_style_manager，将跳过播报风格调用")
        return None

class PathStatus(Enum):
    """路径状态"""
    NORMAL = "normal"           # 正常
    CAUTION = "caution"         # 谨慎
    REROUTE = "reroute"         # 需要改道
    STOP = "stop"              # 停止

class ReasonType(Enum):
    """原因类型"""
    CROWD_HIGH = "crowd_high"                  # 人群密度高
    CROWD_VERY_HIGH = "crowd_very_high"       # 人群非常密集
    DIRECTION_OPPOSITE = "direction_opposite"  # 逆向人流
    DIRECTION_COUNTER = "direction_counter"    # 逆向人流
    DOORPLATE_REVERSED = "doorplate_reversed"  # 门牌反序
    HAZARD_DETECTED = "hazard_detected"       # 检测到危险
    HAZARD_CRITICAL = "hazard_critical"       # 危险极高
    QUEUE_DETECTED = "queue_detected"         # 检测到排队
    UNKNOWN = "unknown"                       # 未知

@dataclass
class PathEvaluation:
    """路径评估结果"""
    status: PathStatus                  # 路径状态
    reasons: List[ReasonType]          # 原因列表
    confidence: float                   # 置信度
    recommendations: List[str]         # 建议
    timestamp: float                    # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status.value,
            "reasons": [r.value for r in self.reasons],
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        output = {
            "event": "path_status_update",
            "status": self.status.value,
            "reason": [r.value for r in self.reasons],
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp))
        }
        return json.dumps(output, ensure_ascii=False, indent=2)

class PathEvaluator:
    """路径判断引擎"""
    
    def __init__(self):
        """初始化路径判断引擎"""
        self.logger = logging.getLogger(__name__)
        
        # 评估阈值
        self.thresholds = {
            "caution": {
                "crowd_density": "crowded",
                "flow_opposite_percentage": 0.5,
                "hazard_severity": "medium"
            },
            "reroute": {
                "crowd_density": "very_crowded",
                "flow_opposite_percentage": 0.7,
                "hazard_severity": "high",
                "doorplate_reversed": True
            },
            "stop": {
                "crowd_density": "very_crowded",
                "hazard_severity": "critical",
                "queue_length": 20
            }
        }
        
        # 偏航检测相关
        self.planned_route: List[Dict[str, float]] = []  # 预定路径 [{lat, lng}, ...]
        self.deviation_count = 0  # 连续偏离次数
        self.deviation_threshold = 5.0  # 偏离阈值（米）
        self.max_deviation_count = 2  # 最大连续偏离次数
        
        self.logger.info("🛤️ 路径判断引擎初始化完成")
    
    def evaluate_path(self, 
                     crowd_density: Dict[str, Any] = None,
                     flow_direction: Dict[str, Any] = None,
                     doorplate_info: Dict[str, Any] = None,
                     hazards: List[Dict[str, Any]] = None,
                     queue_status: Dict[str, Any] = None) -> PathEvaluation:
        """
        评估路径状态
        
        Args:
            crowd_density: 人群密度检测结果
            flow_direction: 人流方向检测结果
            doorplate_info: 门牌推理结果
            hazards: 危险环境检测结果
            queue_status: 排队状态
            
        Returns:
            PathEvaluation: 路径评估结果
        """
        status = PathStatus.NORMAL
        reasons = []
        recommendations = []
        confidence = 1.0
        
        # 1. 检查人群密度
        if crowd_density:
            density_level = crowd_density.get("level", "normal")
            if density_level == "very_crowded":
                status = PathStatus.REROUTE
                reasons.append(ReasonType.CROWD_VERY_HIGH)
                recommendations.append("人群过于密集，建议改道或等待")
                confidence = 0.95
            elif density_level == "crowded":
                if status == PathStatus.NORMAL:
                    status = PathStatus.CAUTION
                reasons.append(ReasonType.CROWD_HIGH)
                recommendations.append("人群较多，请注意安全")
                confidence = 0.85
        
        # 2. 检查人流方向
        if flow_direction:
            flow_status = flow_direction.get("flow_direction", "same")
            counterflow_percentage = flow_direction.get("counterflow_percentage", 0.0)
            
            if flow_status == "counter" or counterflow_percentage > 0.7:
                if status in [PathStatus.NORMAL, PathStatus.CAUTION]:
                    status = PathStatus.REROUTE
                reasons.append(ReasonType.DIRECTION_COUNTER)
                recommendations.append("存在大量逆向人流，建议靠边或改道")
                confidence = 0.9
            elif counterflow_percentage > 0.5:
                if status == PathStatus.NORMAL:
                    status = PathStatus.CAUTION
                reasons.append(ReasonType.DIRECTION_OPPOSITE)
                recommendations.append("存在逆向人流，请注意")
                confidence = 0.75
        
        # 3. 检查门牌方向
        if doorplate_info:
            doorplate_status = doorplate_info.get("status", "unknown")
            if doorplate_status == "backward":
                if status in [PathStatus.NORMAL, PathStatus.CAUTION]:
                    status = PathStatus.REROUTE
                reasons.append(ReasonType.DOORPLATE_REVERSED)
                recommendations.append("门牌号反序，可能走错方向")
                confidence = 0.85
        
        # 4. 检查危险环境
        if hazards:
            for hazard in hazards:
                severity = hazard.get("severity", "low")
                if severity == "critical":
                    status = PathStatus.STOP
                    reasons.append(ReasonType.HAZARD_CRITICAL)
                    recommendations.append("检测到严重危险，请立即停止")
                    confidence = 1.0
                    break
                elif severity == "high":
                    if status == PathStatus.NORMAL:
                        status = PathStatus.CAUTION
                    if status not in [PathStatus.REROUTE, PathStatus.STOP]:
                        reasons.append(ReasonType.HAZARD_DETECTED)
                        recommendations.append("检测到危险环境，请小心通过")
                        confidence = 0.9
        
        # 5. 检查排队状态
        if queue_status:
            queue_detected = queue_status.get("detected", False)
            if queue_detected:
                queue_length = queue_status.get("queue_length", 0)
                if queue_length > 15:
                    status = PathStatus.STOP
                    reasons.append(ReasonType.QUEUE_DETECTED)
                    recommendations.append("前方排队较长，建议等待或绕行")
                    confidence = 0.8
        
        # 如果没有具体原因，但需要谨慎
        if not reasons and status == PathStatus.CAUTION:
            reasons.append(ReasonType.UNKNOWN)
        
        result = PathEvaluation(
            status=status,
            reasons=reasons,
            confidence=confidence,
            recommendations=recommendations,
            timestamp=time.time()
        )
        
        self.logger.info(f"🛤️ 路径评估: {status.value}, "
                        f"原因={len(reasons)}, 置信度={confidence:.2f}")
        
        return result
    
    def set_planned_route(self, route: List[Dict[str, float]]):
        """
        设置预定路径
        
        Args:
            route: 路径点列表 [{lat, lng}, ...]
        """
        self.planned_route = route
        self.deviation_count = 0
        self.logger.info(f"🛤️ 已设置预定路径，包含 {len(route)} 个路径点")
    
    def check_route_deviation(self, current_lat: float, current_lng: float) -> Dict[str, Any]:
        """
        检查路径偏离
        
        Args:
            current_lat: 当前纬度
            current_lng: 当前经度
        
        Returns:
            Dict[str, Any]: 偏离检测结果
        """
        if not self.planned_route:
            return {
                "deviated": False,
                "deviation_distance": 0.0,
                "message": None
            }
        
        # 找到最近的路径点
        min_distance = float('inf')
        nearest_point = None
        
        for point in self.planned_route:
            distance = self._calculate_distance(
                current_lat, current_lng,
                point["lat"], point["lng"]
            )
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
        
        # 判断是否偏离
        deviated = min_distance > self.deviation_threshold
        
        if deviated:
            self.deviation_count += 1
            self.logger.warning(f"⚠️ 检测到路径偏离: {min_distance:.1f}米 (连续{self.deviation_count}次)")
            
            # 连续2次偏离，触发纠正
            if self.deviation_count >= self.max_deviation_count:
                # 优先判断是否可以调头
                turnaround_check = self._check_turnaround_feasibility(
                    current_lat, current_lng, nearest_point
                )
                
                if turnaround_check["can_turnaround"]:
                    # 调头建议优先
                    message = "您刚才走错了，建议您在前方安全位置原地调头，返回右转方向。"
                    self.logger.info("🔄 建议调头恢复路线")
                    
                    self.deviation_count = 0  # 重置计数，避免重复播报
                    
                    return {
                        "deviated": True,
                        "deviation_distance": min_distance,
                        "message": message,
                        "trigger_reroute": False,
                        "suggest_turnaround": True,
                        "turnaround_reason": turnaround_check["reason"]
                    }
                else:
                    # 无法调头，执行路径重规划
                    message = "您可能走错方向了，我来帮您重新规划。"
                    self.logger.warning("🔄 触发路径重规划")
                    
                    self.deviation_count = 0
                    
                    return {
                        "deviated": True,
                        "deviation_distance": min_distance,
                        "message": message,
                        "trigger_reroute": True,
                        "suggest_turnaround": False,
                        "turnaround_reason": turnaround_check["reason"]
                    }
        else:
            # 未偏离，重置计数
            self.deviation_count = 0
        
        return {
            "deviated": deviated,
            "deviation_distance": min_distance,
            "message": None
        }
    
    def _check_turnaround_feasibility(self,
                                     current_lat: float,
                                     current_lng: float,
                                     nearest_point: Dict[str, float]) -> Dict[str, Any]:
        """
        检查调头可行性
        
        Args:
            current_lat: 当前纬度
            current_lng: 当前经度
            nearest_point: 最近的路径点
        
        Returns:
            Dict[str, Any]: 调头可行性评估
        """
        # TODO: 实际应该结合视觉检测（单行道标识、墙体、障碍物）或地图数据
        # 目前简化判断：基于偏离距离和角度
        
        # 计算偏离角度
        import math
        
        # 简化：假设偏离距离较近（<20米）且方向偏差不大时可以调头
        distance = self._calculate_distance(
            current_lat, current_lng,
            nearest_point["lat"], nearest_point["lng"]
        )
        
        # 判断条件
        can_turnaround = True
        reason = "可以调头"
        
        # 条件1: 偏离距离过远（>50米），不适合调头
        if distance > 50:
            can_turnaround = False
            reason = "偏离距离过远，不适合调头"
        
        # 条件2: TODO - 结合视觉检测判断前方是否有单行道标识、墙体、障碍物
        # 这里可以预留接口，后续集成视觉模块
        
        return {
            "can_turnaround": can_turnaround,
            "reason": reason,
            "deviation_distance": distance
        }
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """计算两点间距离（米）- Haversine公式"""
        from math import radians, cos, sin, asin, sqrt
        
        R = 6371000  # 地球半径（米）
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lng = radians(lng2 - lng1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        return R * c
    
    def get_speech_style_for_evaluation(self, danger_level: str = None) -> Optional[Dict[str, Any]]:
        """
        为当前评估结果获取播报风格
        
        Args:
            danger_level: 危险等级
            
        Returns:
            Optional[Dict[str, Any]]: 播报风格配置，如果无法调用返回None
        """
        get_style = get_speech_style_manager()
        if not get_style:
            return None
        
        try:
            # 调用播报风格管理器
            style_output = get_style(
                path_status=self.status.value if hasattr(self, 'status') else "normal",
                danger_level=danger_level
            )
            
            return {
                "speech_style": style_output.speech_style.value,
                "tts_config": style_output.tts_config.to_dict()
            }
        except Exception as e:
            self.logger.error(f"⚠️ 获取播报风格失败: {e}")
            return None
    
    status: Optional[PathStatus] = None  # 用于存储当前评估的状态
    
    def evaluate_path_from_modules(self,
                                  crowd_detector=None,
                                  flow_analyzer=None,
                                  doorplate_engine=None,
                                  hazard_detector=None,
                                  queue_detector=None) -> PathEvaluation:
        """
        从模块实例获取数据进行评估
        
        Args:
            crowd_detector: 人群密度检测器实例
            flow_analyzer: 人流方向分析器实例
            doorplate_engine: 门牌推理引擎实例
            hazard_detector: 危险检测器实例
            queue_detector: 排队检测器实例
            
        Returns:
            PathEvaluation: 路径评估结果
        """
        # 模拟数据（实际应该从各模块获取）
        crowd_density = None
        flow_direction = None
        doorplate_info = None
        hazards = []
        queue_status = None
        
        # TODO: 从各模块获取实际数据
        # 这里使用模拟数据进行演示
        
        return self.evaluate_path(
            crowd_density=crowd_density,
            flow_direction=flow_direction,
            doorplate_info=doorplate_info,
            hazards=hazards,
            queue_status=queue_status
        )


# 全局评估器实例
global_path_evaluator = PathEvaluator()

def evaluate_path(**kwargs) -> PathEvaluation:
    """评估路径的便捷函数"""
    return global_path_evaluator.evaluate_path(**kwargs)


if __name__ == "__main__":
    # 测试路径判断引擎
    import logging
    logging.basicConfig(level=logging.INFO)
    
    evaluator = PathEvaluator()
    
    print("=" * 70)
    print("🛤️ 路径判断引擎测试")
    print("=" * 70)
    
    # 测试案例1: 正常路径
    print("\n测试1: 正常路径")
    result = evaluator.evaluate_path()
    print(result.to_json())
    
    # 测试案例2: 人群密集
    print("\n测试2: 人群密集")
    result = evaluator.evaluate_path(
        crowd_density={"level": "crowded"}
    )
    print(result.to_json())
    
    # 测试案例3: 逆向人流
    print("\n测试3: 逆向人流")
    result = evaluator.evaluate_path(
        flow_direction={
            "flow_direction": "counter",
            "counterflow_percentage": 0.8
        }
    )
    print(result.to_json())
    
    # 测试案例4: 门牌反序
    print("\n测试4: 门牌反序")
    result = evaluator.evaluate_path(
        doorplate_info={"status": "backward"}
    )
    print(result.to_json())
    
    # 测试案例5: 严重危险
    print("\n测试5: 严重危险")
    result = evaluator.evaluate_path(
        hazards=[{"severity": "critical"}]
    )
    print(result.to_json())
    
    # 测试案例6: 综合复杂场景
    print("\n测试6: 综合场景")
    result = evaluator.evaluate_path(
        crowd_density={"level": "very_crowded"},
        flow_direction={"flow_direction": "counter", "counterflow_percentage": 0.6},
        hazards=[{"severity": "high"}]
    )
    print(result.to_json())
    
    print("\n" + "=" * 70)
