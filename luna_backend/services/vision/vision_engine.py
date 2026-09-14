"""
视觉引擎服务层 (v1.2.0)
封装VisionOCREngine，提供统一的视觉服务接口
"""

import base64
import time
import cv2
import numpy as np
from typing import Dict, Any, Optional, List
from PIL import Image
import io
import sys
import os

# 添加Luna_Badge路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "Luna_Badge"))

from core.logger import logger
from core.vision_ocr_engine import VisionOCREngine, get_vision_ocr_engine


class VisionEngine:
    """视觉引擎服务类"""
    
    def __init__(self):
        """初始化视觉引擎"""
        self.engine: Optional[VisionOCREngine] = None
        self.model_name = "yolov8n"
        self._init_time = None
        self._metrics = {
            "total_inferences": 0,
            "total_time_ms": 0,
            "last_inference_time_ms": 0,
            "fps": 0.0,
            "errors": 0
        }
        self._load_engine()
    
    def _load_engine(self):
        """加载视觉引擎"""
        try:
            logger.info("正在初始化视觉引擎...", module="Vision")
            self.engine = get_vision_ocr_engine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
            if self.engine and self.engine.yolo_model:
                self._init_time = time.time()
                logger.info("✅ 视觉引擎初始化成功", module="Vision")
            else:
                logger.error("视觉引擎初始化失败", module="Vision")
        except Exception as e:
            logger.error("视觉引擎初始化异常", details={"error": str(e)}, module="Vision")
            self.engine = None
    
    def is_ready(self) -> bool:
        """检查引擎是否就绪"""
        return self.engine is not None and self.engine.yolo_model is not None
    
    def detect_image(self, image_bytes: bytes) -> Optional[Dict[str, Any]]:
        """
        检测图片（multipart/form-data）
        
        Args:
            image_bytes: 图片字节数据
        
        Returns:
            检测结果字典
        """
        if not self.is_ready():
            logger.error("视觉引擎未就绪", module="Vision")
            return None
        
        try:
            start_time = time.time()
            
            # 转换为numpy数组
            image_np = self._bytes_to_numpy(image_bytes)
            if image_np is None:
                logger.error("图片格式转换失败", module="Vision")
                return None
            
            # 执行检测
            detections = self.engine.detect_objects(image_np)
            ocr_results = self.engine.recognize_text(image_np)
            
            # 计算耗时
            inference_time = (time.time() - start_time) * 1000
            
            # 更新指标
            self._update_metrics(inference_time)
            
            result = {
                "detections": detections,
                "ocr_results": [ocr.to_dict() for ocr in ocr_results],
                "processing_time_ms": round(inference_time, 2),
                "detections_count": len(detections),
                "ocr_count": len(ocr_results)
            }
            
            logger.info("视觉检测完成", details={
                "detections_count": len(detections),
                "ocr_count": len(ocr_results),
                "time_ms": inference_time
            }, module="Vision")
            
            return result
            
        except Exception as e:
            self._metrics["errors"] += 1
            logger.error("视觉检测失败", details={"error": str(e)}, module="Vision")
            return None
    
    def detect_base64(self, base64_str: str) -> Optional[Dict[str, Any]]:
        """
        检测base64图片（适合实时模式）
        
        Args:
            base64_str: base64编码的图片字符串
        
        Returns:
            检测结果字典
        """
        if not self.is_ready():
            logger.error("视觉引擎未就绪", module="Vision")
            return None
        
        try:
            # 解码base64
            if ',' in base64_str:
                base64_str = base64_str.split(',')[-1]
            
            image_bytes = base64.b64decode(base64_str)
            return self.detect_image(image_bytes)
            
        except Exception as e:
            self._metrics["errors"] += 1
            logger.error("base64图片检测失败", details={"error": str(e)}, module="Vision")
            return None
    
    def reload(self) -> bool:
        """重新加载YOLO模型（热重载）"""
        try:
            logger.info("开始重新加载视觉引擎...", module="Vision")
            
            # 释放旧模型
            if self.engine:
                self.engine.yolo_model = None
                self.engine = None
            
            # 重新加载
            self._load_engine()
            
            if self.is_ready():
                logger.info("✅ 视觉引擎重载成功", module="Vision")
                return True
            else:
                logger.error("视觉引擎重载失败", module="Vision")
                return False
                
        except Exception as e:
            logger.error("视觉引擎重载异常", details={"error": str(e)}, module="Vision")
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取视觉性能指标"""
        return {
            "model": self.model_name,
            "ready": self.is_ready(),
            "total_inferences": self._metrics["total_inferences"],
            "total_time_ms": round(self._metrics["total_time_ms"], 2),
            "avg_time_ms": round(
                self._metrics["total_time_ms"] / self._metrics["total_inferences"]
                if self._metrics["total_inferences"] > 0 else 0,
                2
            ),
            "last_inference_time_ms": round(self._metrics["last_inference_time_ms"], 2),
            "fps": round(self._metrics["fps"], 2),
            "errors": self._metrics["errors"],
            "uptime_seconds": round(time.time() - self._init_time, 2) if self._init_time else 0
        }
    
    def _bytes_to_numpy(self, image_bytes: bytes) -> Optional[np.ndarray]:
        """将图片字节转换为numpy数组"""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                # 尝试用PIL
                img_pil = Image.open(io.BytesIO(image_bytes))
                img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            return img
        except Exception as e:
            logger.error("图片转换失败", details={"error": str(e)}, module="Vision")
            return None
    
    def _update_metrics(self, inference_time_ms: float):
        """更新性能指标"""
        self._metrics["total_inferences"] += 1
        self._metrics["total_time_ms"] += inference_time_ms
        self._metrics["last_inference_time_ms"] = inference_time_ms
        
        # 计算FPS（基于最近一次推理时间）
        if inference_time_ms > 0:
            self._metrics["fps"] = 1000.0 / inference_time_ms


# 全局实例
_vision_engine: Optional[VisionEngine] = None

def get_vision_engine() -> VisionEngine:
    """获取全局视觉引擎实例"""
    global _vision_engine
    if _vision_engine is None:
        _vision_engine = VisionEngine()
    return _vision_engine



