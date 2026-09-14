"""
视觉服务聚合入口 (v1.2.0)
把所有"图片进来 → 调用不同detector → 返回结构化结果"的逻辑集中到一个类里
"""

import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from core.runtime import (
    vision_engine,
    step_detector,
    signboard_detector,
    hazard_detector,
    facility_detector,
    traffic_light_detector,
    crowd_density_detector,
    queue_detector,
    doorplate_reader,
    local_map_generator,
    scene_memory_system,
)
from utils.image_utils import image_to_numpy
from utils.logger import vision_log
from config.error_codes import ERR


class VisualService:
    """
    视觉服务聚合入口：
    - 基础识别 / 台阶 / 危险 / 公共设施 / 红绿灯 / 人群 / 排队 / 门牌 / 本地地图
    - 综合检测 / 视觉导航
    """
    
    def __init__(self):
        """初始化视觉服务"""
        pass
    
    # ======== 基础工具 ========
    
    def _to_np(self, file_storage) -> np.ndarray:
        """统一把上传图片转成 np.ndarray"""
        data = file_storage.read()
        img = image_to_numpy(data)
        if img is None:
            raise ValueError(f"无法解析图片 (错误码: {ERR.IMAGE_FORMAT_INVALID})")
        return img
    
    # ======== 单一能力 ========
    
    def recognize_basic(self, file_storage) -> Dict[str, Any]:
        """基础视觉识别"""
        img = self._to_np(file_storage)
        
        if vision_engine is None:
            raise RuntimeError(f"视觉引擎未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        t0 = time.time()
        res = vision_engine.detect_and_recognize(img)
        cost = time.time() - t0
        
        vision_log("RECOGNIZE", {
            "detections": len(res.get("detections", [])),
            "ocr": len(res.get("ocr_results", [])),
            "latency_ms": round(cost * 1000, 2),
        })
        
        return {
            "detections": res.get("detections", []),
            "ocr_results": res.get("ocr_results", []),
            "processing_time": res.get("processing_time", cost),
        }
    
    def detect_step(self, file_storage) -> Dict[str, Any]:
        """台阶检测"""
        img = self._to_np(file_storage)
        
        if step_detector is None:
            raise RuntimeError(f"台阶检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        result = step_detector.detect_step(img)
        
        vision_log("STEP", {
            "detected": bool(result),
            "result": result or {},
        })
        
        return result or {"detected": False, "message": "未检测到台阶"}
    
    def detect_signboard(self, file_storage) -> List[Dict[str, Any]]:
        """标识牌检测"""
        img = self._to_np(file_storage)
        
        if signboard_detector is None:
            raise RuntimeError(f"标识牌检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        # 兼容不同的方法名
        if hasattr(signboard_detector, 'detect_signboards'):
            results = signboard_detector.detect_signboards(img) or []
        elif hasattr(signboard_detector, 'detect_signboard'):
            result = signboard_detector.detect_signboard(img)
            results = [result] if result else []
        else:
            results = []
        
        # 转换为字典
        if results:
            if hasattr(results[0], 'to_dict'):
                return [r.to_dict() for r in results]
            elif isinstance(results[0], dict):
                return results
            else:
                return [{"result": str(r)} for r in results]
        
        return []
    
    def detect_hazard(self, file_storage) -> Dict[str, Any]:
        """危险检测"""
        img = self._to_np(file_storage)
        
        if hazard_detector is None:
            raise RuntimeError(f"危险检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        # 获取YOLO检测结果用于过滤误报
        detected_objects = []
        if vision_engine:
            try:
                vr = vision_engine.detect_and_recognize(img)
                detected_objects = vr.get("detections", [])
            except Exception:
                pass
        
        # 检测危险
        if hasattr(hazard_detector, 'detect_hazards'):
            hazards = hazard_detector.detect_hazards(img, detected_objects=detected_objects) or []
        elif hasattr(hazard_detector, 'detect_hazard'):
            hazard = hazard_detector.detect_hazard(img)
            hazards = [hazard] if hazard else []
        else:
            hazards = []
        
        # 转换为字典
        hazards_dict = []
        for h in hazards:
            if hasattr(h, 'to_dict'):
                hazards_dict.append(h.to_dict())
            elif isinstance(h, dict):
                hazards_dict.append(h)
            else:
                hazards_dict.append({"hazard": str(h)})
        
        # 获取摘要（如果有）
        summary = {}
        if hasattr(hazard_detector, "get_detection_summary"):
            try:
                summary = hazard_detector.get_detection_summary(hazards)
            except:
                pass
        
        vision_log("HAZARD", {
            "count": len(hazards_dict),
        })
        
        return {
            "hazards": hazards_dict,
            "summary": summary,
        }
    
    def detect_facility(self, file_storage) -> List[Dict[str, Any]]:
        """公共设施检测"""
        img = self._to_np(file_storage)
        
        if facility_detector is None:
            raise RuntimeError(f"公共设施检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        res = facility_detector.detect_facility(img) or []
        
        # 转换为字典
        if res:
            if hasattr(res[0], 'to_dict'):
                return [r.to_dict() for r in res]
            elif isinstance(res[0], dict):
                return res
            else:
                return [{"facility": str(r)} for r in res]
        
        return []
    
    def detect_traffic_light(self, file_storage) -> Dict[str, Any]:
        """红绿灯检测"""
        img = self._to_np(file_storage)
        
        if traffic_light_detector is None:
            raise RuntimeError(f"红绿灯检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        result = traffic_light_detector.detect_traffic_light(img)
        
        if not result:
            return {"traffic_light": None, "broadcast_message": None}
        
        # 转换为字典
        if hasattr(result, 'to_dict'):
            result_dict = result.to_dict()
        elif isinstance(result, dict):
            result_dict = result
        else:
            result_dict = {"traffic_light": str(result)}
        
        # 获取播报消息（如果有）
        broadcast_message = None
        if hasattr(result, "get_broadcast_message"):
            try:
                broadcast_message = result.get_broadcast_message()
            except:
                pass
        
        return {
            "traffic_light": result_dict,
            "broadcast_message": broadcast_message,
        }
    
    def detect_crowd_density(self, file_storage) -> Optional[Dict[str, Any]]:
        """人群密度检测"""
        img = self._to_np(file_storage)
        
        if crowd_density_detector is None:
            raise RuntimeError(f"人群密度检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        result = crowd_density_detector.detect_density(img)
        
        if not result:
            return None
        
        if hasattr(result, 'to_dict'):
            return result.to_dict()
        elif isinstance(result, dict):
            return result
        else:
            return {"density": str(result)}
    
    def detect_queue(self, file_storage) -> Optional[Dict[str, Any]]:
        """排队检测"""
        img = self._to_np(file_storage)
        
        if queue_detector is None:
            raise RuntimeError(f"排队检测器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        result = queue_detector.detect_queue(img)
        
        if not result:
            return None
        
        if hasattr(result, 'to_dict'):
            return result.to_dict()
        elif isinstance(result, dict):
            return result
        else:
            return {"queue": str(result)}
    
    def detect_doorplate(self, file_storage) -> List[Dict[str, Any]]:
        """门牌号识别"""
        img = self._to_np(file_storage)
        
        if doorplate_reader is None:
            raise RuntimeError(f"门牌号识别器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        res = doorplate_reader.read_doorplate(img) or []
        
        # 转换为字典
        if res:
            if hasattr(res[0], 'to_dict'):
                return [r.to_dict() for r in res]
            elif isinstance(res[0], dict):
                return res
            else:
                return [{"doorplate": str(r)} for r in res]
        
        return []
    
    # ======== 本地地图 / 场景记忆 ========
    
    def update_local_map(self, dx: float, dy: float, angle_delta: float, file_storage=None) -> Dict[str, Any]:
        """更新本地地图"""
        if local_map_generator is None:
            raise RuntimeError(f"本地地图生成器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        local_map_generator.update_position(dx, dy, angle_delta)
        
        if file_storage and facility_detector:
            try:
                img = self._to_np(file_storage)
                facilities = facility_detector.detect_facility(img) or []
                
                for f in facilities:
                    if hasattr(f, 'type') and hasattr(f, 'label') and hasattr(f, 'confidence'):
                        local_map_generator.add_landmark(
                            f.type.value if hasattr(f.type, 'value') else str(f.type),
                            (0, 0),  # TODO: 根据实际计算位置
                            f.label if hasattr(f, 'label') else "",
                            f.confidence if hasattr(f, 'confidence') else 0.0
                        )
            except Exception as e:
                vision_log("MAP_UPDATE_ERROR", {"error": str(e)})
        
        local_map = local_map_generator.get_map()
        if local_map:
            if hasattr(local_map, 'to_dict'):
                return local_map.to_dict()
            elif isinstance(local_map, dict):
                return local_map
            else:
                return {"map": str(local_map)}
        
        return {}
    
    # ======== 综合检测 ========
    
    def comprehensive(self, file_storage) -> Dict[str, Any]:
        """综合检测（所有检测器）"""
        img = self._to_np(file_storage)
        t0 = time.time()
        
        results: Dict[str, Any] = {}
        
        # 1) vision
        if vision_engine:
            try:
                vr = vision_engine.detect_and_recognize(img)
                results["vision"] = {
                    "detections": vr.get("detections", []),
                    "ocr_results": vr.get("ocr_results", []),
                }
            except Exception as e:
                results["vision"] = {"error": str(e)}
        
        # 2) step
        if step_detector:
            try:
                step_res = step_detector.detect_step(img)
                results["step"] = step_res or {"detected": False}
            except Exception as e:
                results["step"] = {"error": str(e)}
        
        # 3) signboard
        if signboard_detector:
            try:
                if hasattr(signboard_detector, 'detect_signboards'):
                    sb = signboard_detector.detect_signboards(img) or []
                else:
                    sb = []
                results["signboard"] = [r.to_dict() if hasattr(r, 'to_dict') else str(r) for r in sb]
            except Exception as e:
                results["signboard"] = {"error": str(e)}
        
        # 4) hazard
        if hazard_detector:
            try:
                detected_objects = results.get("vision", {}).get("detections", [])
                if hasattr(hazard_detector, 'detect_hazards'):
                    hz = hazard_detector.detect_hazards(img, detected_objects=detected_objects) or []
                else:
                    hz = []
                results["hazard"] = [h.to_dict() if hasattr(h, 'to_dict') else str(h) for h in hz]
            except Exception as e:
                results["hazard"] = {"error": str(e)}
        
        # 5) facility
        if facility_detector:
            try:
                fa = facility_detector.detect_facility(img) or []
                results["facility"] = [f.to_dict() if hasattr(f, 'to_dict') else str(f) for f in fa]
            except Exception as e:
                results["facility"] = {"error": str(e)}
        
        # 6) traffic light
        if traffic_light_detector:
            try:
                tl = traffic_light_detector.detect_traffic_light(img)
                results["traffic_light"] = tl.to_dict() if tl and hasattr(tl, 'to_dict') else (tl if tl else None)
            except Exception as e:
                results["traffic_light"] = {"error": str(e)}
        
        # 7) crowd
        if crowd_density_detector:
            try:
                cd = crowd_density_detector.detect_density(img)
                results["crowd_density"] = cd.to_dict() if cd and hasattr(cd, 'to_dict') else (cd if cd else None)
            except Exception as e:
                results["crowd_density"] = {"error": str(e)}
        
        # 8) queue
        if queue_detector:
            try:
                q = queue_detector.detect_queue(img)
                results["queue"] = q.to_dict() if q and hasattr(q, 'to_dict') else (q if q else None)
            except Exception as e:
                results["queue"] = {"error": str(e)}
        
        # 9) doorplate
        if doorplate_reader:
            try:
                dp = doorplate_reader.read_doorplate(img) or []
                results["doorplate"] = [d.to_dict() if hasattr(d, 'to_dict') else str(d) for d in dp]
            except Exception as e:
                results["doorplate"] = {"error": str(e)}
        
        vision_log("COMPREHENSIVE", {
            "latency_ms": round((time.time() - t0) * 1000, 2),
        })
        
        return results
    
    # ======== 视觉导航（保留高级逻辑，待迁移） ========
    
    def visual_guidance(self, file_storage, voice_command: str = "") -> Dict[str, Any]:
        """
        视觉导航引导
        把你原来 /api/navigation/visual_guidance 里的逻辑迁到这里
        （ROI + 时序融合 + 视觉语言融合）
        """
        img = self._to_np(file_storage)
        
        if vision_engine is None or scene_memory_system is None:
            raise RuntimeError(f"视觉导航模块未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        # TODO: 这里复制你原来 web_test_server.py 里 visual_guidance 的主体逻辑
        # 目前先返回一个占位结构
        return {
            "direction": "forward",
            "messages": ["视觉导航模块待迁移"],
            "debug": {},
        }


# 单例
visual_service = None

def get_visual_service():
    """获取视觉服务单例"""
    global visual_service
    if visual_service is None:
        visual_service = VisualService()
    return visual_service



