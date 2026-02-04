"""
统一打包视觉输出，提供给 route 层使用 (v1.2.0)
"""

from typing import Dict, Any, Optional
from utils.logger import vision_log


class VisualPackager:
    """视觉输出打包器"""
    
    def __init__(self):
        """初始化视觉打包器"""
        pass
    
    def package(self, runtime_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        打包视觉运行时状态为返回格式
        
        Args:
            runtime_state: 视觉运行时状态字典
        
        Returns:
            打包后的视觉输出字典
        """
        result = {
            "timestamp": runtime_state.get("timestamp"),
            "fps": runtime_state.get("fps", 0),
            "detections": [],
            "ocr_results": [],
            "steps": [],
            "obstacles": [],
            "hazards": [],
            "signs": [],
            "signboards": [],
            "facilities": [],
            "traffic_light": None,
            "crowd_density": None,
            "queue": None,
            "doorplates": []
        }
        
        # 处理检测结果
        detections = runtime_state.get("detections", [])
        if detections:
            result["detections"] = [
                d.to_dict() if hasattr(d, 'to_dict') else d
                for d in detections
                if d is not None
            ]
        
        # 处理OCR结果
        ocr_results = runtime_state.get("ocr_results", [])
        if ocr_results:
            result["ocr_results"] = [
                o.to_dict() if hasattr(o, 'to_dict') else o
                for o in ocr_results
                if o is not None
            ]
        
        # 处理台阶
        steps = runtime_state.get("steps", [])
        if steps:
            if isinstance(steps, list):
                result["steps"] = [
                    s.to_dict() if hasattr(s, 'to_dict') else s
                    for s in steps
                    if s is not None
                ]
            else:
                result["steps"] = [steps.to_dict() if hasattr(steps, 'to_dict') else steps]
        
        # 处理障碍物
        obstacles = runtime_state.get("obstacles", [])
        if obstacles:
            result["obstacles"] = [
                o.to_dict() if hasattr(o, 'to_dict') else o
                for o in obstacles
                if o is not None
            ]
        
        # 处理危险
        hazards = runtime_state.get("hazards", [])
        if hazards:
            result["hazards"] = [
                h.to_dict() if hasattr(h, 'to_dict') else h
                for h in hazards
                if h is not None
            ]
        
        # 处理标识牌
        signs = runtime_state.get("signs", [])
        signboards = runtime_state.get("signboards", [])
        all_signs = signs + signboards
        
        if all_signs:
            result["signs"] = [
                s.to_dict() if hasattr(s, 'to_dict') else s
                for s in all_signs
                if s is not None
            ]
        
        # 处理公共设施
        facilities = runtime_state.get("facilities", [])
        if facilities:
            result["facilities"] = [
                f.to_dict() if hasattr(f, 'to_dict') else f
                for f in facilities
                if f is not None
            ]
        
        # 处理红绿灯
        traffic_light = runtime_state.get("traffic_light")
        if traffic_light:
            result["traffic_light"] = (
                traffic_light.to_dict() if hasattr(traffic_light, 'to_dict') else traffic_light
            )
        
        # 处理人群密度
        crowd_density = runtime_state.get("crowd_density")
        if crowd_density:
            result["crowd_density"] = (
                crowd_density.to_dict() if hasattr(crowd_density, 'to_dict') else crowd_density
            )
        
        # 处理排队
        queue = runtime_state.get("queue")
        if queue:
            result["queue"] = (
                queue.to_dict() if hasattr(queue, 'to_dict') else queue
            )
        
        # 处理门牌号
        doorplates = runtime_state.get("doorplates", [])
        if doorplates:
            result["doorplates"] = [
                d.to_dict() if hasattr(d, 'to_dict') else d
                for d in doorplates
                if d is not None
            ]
        
        vision_log("PACKAGED", {
            "detection_count": len(result["detections"]),
            "ocr_count": len(result["ocr_results"]),
            "step_count": len(result["steps"]),
            "hazard_count": len(result["hazards"])
        })
        
        return result
    
    def package_comprehensive(self, comprehensive_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        打包综合检测结果
        
        Args:
            comprehensive_result: 综合检测结果字典
        
        Returns:
            打包后的综合检测输出字典
        """
        return {
            "timestamp": comprehensive_result.get("timestamp"),
            "results": comprehensive_result,
            "summary": {
                "has_vision": "vision" in comprehensive_result,
                "has_step": "step" in comprehensive_result,
                "has_hazard": "hazard" in comprehensive_result,
                "has_facility": "facility" in comprehensive_result,
                "has_traffic_light": "traffic_light" in comprehensive_result
            }
        }



