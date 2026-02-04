#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一视觉引擎（规范要求）
封装所有视觉检测功能，提供统一入口
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VisionDetectionResult:
    """视觉检测结果"""
    objects: List[Dict[str, Any]] = None
    texts: List[Dict[str, Any]] = None
    hazards: List[Dict[str, Any]] = None
    steps: Optional[Dict[str, Any]] = None
    signboards: List[Dict[str, Any]] = None
    facilities: List[Dict[str, Any]] = None
    traffic_lights: Optional[Dict[str, Any]] = None
    crowd_density: Optional[Dict[str, Any]] = None
    queues: Optional[Dict[str, Any]] = None
    doorplates: List[Dict[str, Any]] = None
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "objects": self.objects or [],
            "texts": self.texts or [],
            "hazards": self.hazards or [],
            "steps": self.steps,
            "signboards": self.signboards or [],
            "facilities": self.facilities or [],
            "traffic_lights": self.traffic_lights,
            "crowd_density": self.crowd_density,
            "queues": self.queues,
            "doorplates": self.doorplates or [],
            "processing_time": self.processing_time
        }


class VisionEngine:
    """
    统一视觉引擎
    封装所有视觉检测功能，提供统一入口
    """
    
    def __init__(self, 
                 vision_ocr_engine=None,
                 step_detector=None,
                 signboard_detector=None,
                 hazard_detector=None,
                 facility_detector=None,
                 traffic_light_detector=None,
                 crowd_density_detector=None,
                 queue_detector=None,
                 doorplate_reader=None):
        """
        初始化视觉引擎
        
        Args:
            vision_ocr_engine: 视觉OCR引擎
            step_detector: 台阶检测器
            signboard_detector: 标识牌检测器
            hazard_detector: 危险检测器
            facility_detector: 公共设施检测器
            traffic_light_detector: 红绿灯检测器
            crowd_density_detector: 人群密度检测器
            queue_detector: 排队检测器
            doorplate_reader: 门牌号识别器
        """
        self.vision_ocr_engine = vision_ocr_engine
        self.step_detector = step_detector
        self.signboard_detector = signboard_detector
        self.hazard_detector = hazard_detector
        self.facility_detector = facility_detector
        self.traffic_light_detector = traffic_light_detector
        self.crowd_density_detector = crowd_density_detector
        self.queue_detector = queue_detector
        self.doorplate_reader = doorplate_reader
        
        logger.info("VisionEngine初始化完成", extra={"module": "vision", "meta": {"component": "vision_engine"}})
    
    def detect_hazard(self, image: np.ndarray, detected_objects: List[Dict] = None) -> List[Dict[str, Any]]:
        """
        检测危险区域
        
        Args:
            image: 输入图像
            detected_objects: 已检测的物体列表（用于过滤误报）
        
        Returns:
            List[Dict]: 危险区域列表
        """
        if not self.hazard_detector:
            logger.warning("危险检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return []
        
        try:
            hazards = self.hazard_detector.detect_hazards(image, detected_objects=detected_objects)
            return [h.to_dict() for h in hazards] if hazards else []
        except Exception as e:
            logger.error(f"危险检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return []
    
    def detect_step(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        检测台阶
        
        Args:
            image: 输入图像
        
        Returns:
            Optional[Dict]: 台阶检测结果
        """
        if not self.step_detector:
            logger.warning("台阶检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return None
        
        try:
            result = self.step_detector.detect_step(image)
            return result if result else None
        except Exception as e:
            logger.error(f"台阶检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return None
    
    def detect_signboard(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        检测标识牌
        
        Args:
            image: 输入图像
        
        Returns:
            List[Dict]: 标识牌列表
        """
        if not self.signboard_detector:
            logger.warning("标识牌检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return []
        
        try:
            results = self.signboard_detector.detect_signboards(image)
            return [r.to_dict() for r in results] if results else []
        except Exception as e:
            logger.error(f"标识牌检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return []
    
    def detect_facility(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        检测公共设施
        
        Args:
            image: 输入图像
        
        Returns:
            List[Dict]: 公共设施列表
        """
        if not self.facility_detector:
            logger.warning("公共设施检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return []
        
        try:
            results = self.facility_detector.detect_facility(image)
            return [r.to_dict() for r in results] if results else []
        except Exception as e:
            logger.error(f"公共设施检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return []
    
    def detect_traffic_light(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        检测红绿灯
        
        Args:
            image: 输入图像
        
        Returns:
            Optional[Dict]: 红绿灯检测结果
        """
        if not self.traffic_light_detector:
            logger.warning("红绿灯检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return None
        
        try:
            result = self.traffic_light_detector.detect_traffic_light(image)
            return result.to_dict() if result else None
        except Exception as e:
            logger.error(f"红绿灯检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return None
    
    def detect_crowd_density(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        检测人群密度
        
        Args:
            image: 输入图像
        
        Returns:
            Optional[Dict]: 人群密度检测结果
        """
        if not self.crowd_density_detector:
            logger.warning("人群密度检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return None
        
        try:
            result = self.crowd_density_detector.detect_density(image)
            return result.to_dict() if result else None
        except Exception as e:
            logger.error(f"人群密度检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return None
    
    def detect_queue(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        检测排队情况
        
        Args:
            image: 输入图像
        
        Returns:
            Optional[Dict]: 排队检测结果
        """
        if not self.queue_detector:
            logger.warning("排队检测器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return None
        
        try:
            result = self.queue_detector.detect_queue(image)
            return result.to_dict() if result else None
        except Exception as e:
            logger.error(f"排队检测失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return None
    
    def detect_doorplate(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        识别门牌号
        
        Args:
            image: 输入图像
        
        Returns:
            List[Dict]: 门牌号列表
        """
        if not self.doorplate_reader:
            logger.warning("门牌号识别器未初始化", extra={"module": "vision", "meta": {"component": "vision_engine"}})
            return []
        
        try:
            results = self.doorplate_reader.read_doorplate(image)
            return [r.to_dict() for r in results] if results else []
        except Exception as e:
            logger.error(f"门牌号识别失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
            return []
    
    def detect_all(self, image: np.ndarray) -> VisionDetectionResult:
        """
        执行所有视觉检测（统一入口）
        
        Args:
            image: 输入图像
        
        Returns:
            VisionDetectionResult: 所有检测结果
        """
        import time
        start_time = time.time()
        
        result = VisionDetectionResult()
        
        # 1. 基础视觉识别（物体+文字）
        if self.vision_ocr_engine:
            try:
                vision_results = self.vision_ocr_engine.detect_and_recognize(image)
                result.objects = vision_results.get('detections', [])
                result.texts = vision_results.get('ocr_results', [])
            except Exception as e:
                logger.error(f"基础视觉识别失败: {e}", extra={"module": "vision", "meta": {"component": "vision_engine", "error": str(e)}})
        
        # 2. 危险检测（需要物体检测结果用于过滤误报）
        detected_objects = result.objects or []
        result.hazards = self.detect_hazard(image, detected_objects=detected_objects)
        
        # 3. 台阶检测
        result.steps = self.detect_step(image)
        
        # 4. 标识牌检测
        result.signboards = self.detect_signboard(image)
        
        # 5. 公共设施检测
        result.facilities = self.detect_facility(image)
        
        # 6. 红绿灯检测
        result.traffic_lights = self.detect_traffic_light(image)
        
        # 7. 人群密度检测
        result.crowd_density = self.detect_crowd_density(image)
        
        # 8. 排队检测
        result.queues = self.detect_queue(image)
        
        # 9. 门牌号识别
        result.doorplates = self.detect_doorplate(image)
        
        result.processing_time = time.time() - start_time
        
        logger.info(f"视觉检测完成，耗时: {result.processing_time:.3f}秒", 
                   extra={"module": "vision", "meta": {
                       "component": "vision_engine",
                       "processing_time": result.processing_time,
                       "objects_count": len(result.objects or []),
                       "hazards_count": len(result.hazards or [])
                   }})
        
        return result


# 全局VisionEngine实例
_global_vision_engine: Optional[VisionEngine] = None


def get_vision_engine(vision_ocr_engine=None,
                      step_detector=None,
                      signboard_detector=None,
                      hazard_detector=None,
                      facility_detector=None,
                      traffic_light_detector=None,
                      crowd_density_detector=None,
                      queue_detector=None,
                      doorplate_reader=None) -> VisionEngine:
    """
    获取全局VisionEngine实例
    
    Args:
        各检测器实例（可选）
    
    Returns:
        VisionEngine: 视觉引擎实例
    """
    global _global_vision_engine
    
    if _global_vision_engine is None:
        _global_vision_engine = VisionEngine(
            vision_ocr_engine=vision_ocr_engine,
            step_detector=step_detector,
            signboard_detector=signboard_detector,
            hazard_detector=hazard_detector,
            facility_detector=facility_detector,
            traffic_light_detector=traffic_light_detector,
            crowd_density_detector=crowd_density_detector,
            queue_detector=queue_detector,
            doorplate_reader=doorplate_reader
        )
    
    return _global_vision_engine


if __name__ == "__main__":
    # 自检代码
    import cv2
    import numpy as np
    
    print("🧪 VisionEngine自检开始...")
    
    # 创建测试图像
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image, (100, 100), (200, 200), (255, 0, 0), 2)
    
    # 创建VisionEngine实例（使用None作为占位符）
    engine = VisionEngine()
    
    # 测试检测函数（会返回空结果，因为检测器未初始化）
    result = engine.detect_all(test_image)
    
    print(f"✅ VisionEngine自检完成")
    print(f"   处理时间: {result.processing_time:.3f}秒")
    print(f"   检测结果: {result.to_dict()}")


