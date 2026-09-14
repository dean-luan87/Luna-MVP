"""
视觉输出 → 全局事件系统（如 unified_event_bridge）(v1.2.0)
"""

from typing import List, Dict, Any, Optional
from utils.logger import vision_log


class VisualEventMapper:
    """视觉事件映射器"""
    
    def __init__(self):
        """初始化视觉事件映射器"""
        pass
    
    def map(self, visual_bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        将视觉结果包映射为事件列表
        
        Args:
            visual_bundle: 视觉结果包
        
        Returns:
            事件列表
        """
        mapped_events = []
        
        # 映射台阶事件
        steps = visual_bundle.get("steps", [])
        if steps:
            if not isinstance(steps, list):
                steps = [steps]
            
            for step in steps:
                step_dict = step.to_dict() if hasattr(step, 'to_dict') else step
                mapped_events.append({
                    "type": "step_detected",
                    "data": step_dict,
                    "timestamp": visual_bundle.get("timestamp")
                })
        
        # 映射障碍物事件
        obstacles = visual_bundle.get("obstacles", [])
        if obstacles:
            for obs in obstacles:
                obs_dict = obs.to_dict() if hasattr(obs, 'to_dict') else obs
                mapped_events.append({
                    "type": "obstacle_detected",
                    "data": obs_dict,
                    "timestamp": visual_bundle.get("timestamp")
                })
        
        # 映射危险事件
        hazards = visual_bundle.get("hazards", [])
        if hazards:
            for hazard in hazards:
                hazard_dict = hazard.to_dict() if hasattr(hazard, 'to_dict') else hazard
                mapped_events.append({
                    "type": "hazard_detected",
                    "data": hazard_dict,
                    "timestamp": visual_bundle.get("timestamp"),
                    "priority": "high"
                })
        
        # 映射标识牌事件
        signs = visual_bundle.get("signs", [])
        signboards = visual_bundle.get("signboards", [])
        all_signs = signs + signboards
        
        if all_signs:
            for sign in all_signs:
                sign_dict = sign.to_dict() if hasattr(sign, 'to_dict') else sign
                mapped_events.append({
                    "type": "sign_detected",
                    "data": sign_dict,
                    "timestamp": visual_bundle.get("timestamp")
                })
        
        # 映射公共设施事件
        facilities = visual_bundle.get("facilities", [])
        if facilities:
            for facility in facilities:
                facility_dict = facility.to_dict() if hasattr(facility, 'to_dict') else facility
                mapped_events.append({
                    "type": "facility_detected",
                    "data": facility_dict,
                    "timestamp": visual_bundle.get("timestamp")
                })
        
        # 映射红绿灯事件
        traffic_light = visual_bundle.get("traffic_light")
        if traffic_light:
            traffic_dict = traffic_light.to_dict() if hasattr(traffic_light, 'to_dict') else traffic_light
            mapped_events.append({
                "type": "traffic_light_detected",
                "data": traffic_dict,
                "timestamp": visual_bundle.get("timestamp")
            })
        
        vision_log("EVENTS_MAPPED", {"event_count": len(mapped_events)})
        
        return mapped_events
    
    def map_to_unified_events(self, visual_bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        映射为统一事件格式（兼容unified_event_bridge）
        
        Args:
            visual_bundle: 视觉结果包
        
        Returns:
            统一格式事件列表
        """
        events = self.map(visual_bundle)
        
        # 转换为统一事件格式
        unified_events = []
        for event in events:
            unified_event = {
                "event_type": event["type"],
                "payload": event["data"],
                "timestamp": event.get("timestamp"),
                "source": "vision",
                "priority": event.get("priority", "normal")
            }
            unified_events.append(unified_event)
        
        return unified_events



