#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 视觉OCR引擎
集成 PaddleOCR + YOLOv8n 实现多模态识别
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class OCRResult:
    """OCR识别结果"""
    text: str                    # 识别的文本
    confidence: float            # 置信度
    box: List[List[int]]         # 文本框坐标
    detected_class: str = None   # YOLO检测到的类别
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "text": self.text,
            "confidence": self.confidence,
            "box": self.box,
            "detected_class": self.detected_class
        }

class VisionOCREngine:
    """
    视觉OCR引擎
    组合YOLOv8物体检测 + PaddleOCR文字识别
    """
    
    def __init__(self, use_yolo: bool = True, use_ocr: bool = True, yolo_imgsz: int = 1280):
        """
        初始化视觉OCR引擎
        
        Args:
            use_yolo: 是否使用YOLO检测
            use_ocr: 是否使用OCR识别
            yolo_imgsz: YOLO输入图像尺寸（默认1280，支持1080P）
        """
        self.use_yolo = use_yolo
        self.use_ocr = use_ocr
        self.yolo_model = None
        self.ocr_model = None
        self.yolo_imgsz = yolo_imgsz  # 1080P使用1280，保持比例resize
        
        logger.info(f"🎯 视觉OCR引擎初始化 (YOLO={use_yolo}, OCR={use_ocr}, imgsz={yolo_imgsz})")
    
    def _init_yolo(self):
        """初始化YOLO模型"""
        if not self.use_yolo:
            return
        
        try:
            from ultralytics import YOLO
            
            logger.info(f"正在加载YOLOv8模型 (输入尺寸: {self.yolo_imgsz})...")
            self.yolo_model = YOLO('yolov8n.pt')  # nano版本，轻量级
            
            logger.info(f"✅ YOLOv8模型加载成功 (输入尺寸: {self.yolo_imgsz}，支持1080P)")
        except ImportError:
            logger.error("❌ 未安装ultralytics，请运行: pip install ultralytics")
        except Exception as e:
            logger.error(f"❌ YOLO模型加载失败: {e}")
    
    def _init_ocr(self):
        """初始化PaddleOCR模型"""
        if not self.use_ocr:
            return
        
        try:
            from paddleocr import PaddleOCR
            
            logger.info("正在加载PaddleOCR模型...")
            # 新版本PaddleOCR的初始化
            self.ocr_model = PaddleOCR(
                lang='ch'  # 中文识别
            )
            
            logger.info("✅ PaddleOCR模型加载成功")
        except ImportError:
            logger.error("❌ 未安装PaddleOCR，请运行: pip install paddleocr paddlepaddle")
        except Exception as e:
            logger.error(f"❌ PaddleOCR模型加载失败: {e}")
    
    def load_models(self) -> bool:
        """
        加载所有模型
        
        Returns:
            bool: 是否成功加载
        """
        try:
            self._init_yolo()
            self._init_ocr()
            return True
        except Exception as e:
            logger.error(f"❌ 模型加载失败: {e}")
            return False
    
    def detect_objects(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        使用YOLO检测物体
        
        Args:
            image: 输入图像
            
        Returns:
            List[Dict]: 检测结果列表
        """
        if not self.use_yolo or self.yolo_model is None:
            return []
        
        try:
            # 使用指定的输入尺寸进行推理（支持1080P）
            results = self.yolo_model(image, imgsz=self.yolo_imgsz, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    class_name = result.names[class_id]
                    
                    # 获取边界框坐标
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    detections.append({
                        "class": class_name,
                        "confidence": confidence,
                        "box": [int(x1), int(y1), int(x2), int(y2)],
                        "center": (int((x1 + x2) / 2), int((y1 + y2) / 2))
                    })
            
            return detections
        except Exception as e:
            logger.error(f"❌ YOLO检测失败: {e}")
            return []
    
    def recognize_text(self, image: np.ndarray, roi: List[int] = None) -> List[OCRResult]:
        """
        使用OCR识别文字
        
        Args:
            image: 输入图像
            roi: 感兴趣区域 [x1, y1, x2, y2]，如果为None则识别整个图像
            
        Returns:
            List[OCRResult]: 识别结果列表
        """
        if not self.use_ocr or self.ocr_model is None:
            return []
        
        try:
            # 如果指定了ROI，裁剪图像
            if roi is not None:
                x1, y1, x2, y2 = roi
                image = image[y1:y2, x1:x2]
            
            # OCR识别（新版本API - 使用.predict()方法）
            results = self.ocr_model.predict(image)
            
            ocr_results = []
            if results and len(results) > 0:
                result_obj = results[0]
                # 提取文字和分数
                rec_texts = result_obj.get('rec_texts', [])
                rec_scores = result_obj.get('rec_scores', [])
                rec_polys = result_obj.get('rec_polys', [])
                
                for i, text in enumerate(rec_texts):
                    if i < len(rec_scores) and i < len(rec_polys):
                        score = rec_scores[i]
                        box = rec_polys[i].tolist() if hasattr(rec_polys[i], 'tolist') else rec_polys[i]
                        
                        ocr_results.append(OCRResult(
                            text=text,
                            confidence=score,
                            box=box
                        ))
            
            return ocr_results
        except Exception as e:
            logger.error(f"❌ OCR识别失败: {e}")
            return []
    
    def detect_and_recognize(self, image: np.ndarray) -> Dict[str, Any]:
        """
        检测物体并识别文字（组合YOLO + OCR）
        
        Args:
            image: 输入图像
            
        Returns:
            Dict: 包含检测和识别结果的字典
        """
        start_time = time.time()
        
        # 1. YOLO物体检测
        detections = self.detect_objects(image) if self.use_yolo else []
        
        # 2. OCR文字识别
        ocr_results = self.recognize_text(image) if self.use_ocr else []
        
        # 3. 组合结果（将OCR结果与最近的物体关联）
        combined_results = self._combine_results(detections, ocr_results)
        
        processing_time = time.time() - start_time
        
        return {
            "detections": detections,
            "ocr_results": [r.to_dict() for r in ocr_results],
            "combined": combined_results,
            "processing_time": processing_time
        }
    
    def _combine_results(self, detections: List[Dict], ocr_results: List[OCRResult]) -> List[Dict]:
        """
        组合YOLO检测结果和OCR识别结果
        
        Args:
            detections: YOLO检测结果
            ocr_results: OCR识别结果
            
        Returns:
            List[Dict]: 组合后的结果
        """
        combined = []
        
        for ocr in ocr_results:
            # 找到最近的物体
            nearest_detection = self._find_nearest_detection(ocr.box, detections)
            
            combined.append({
                "text": ocr.text,
                "confidence": ocr.confidence,
                "box": ocr.box,
                "detected_class": nearest_detection["class"] if nearest_detection else None,
                "object_confidence": nearest_detection["confidence"] if nearest_detection else None
            })
        
        return combined
    
    def _find_nearest_detection(self, ocr_box: List[List[int]], detections: List[Dict]) -> Optional[Dict]:
        """
        找到与OCR框最近的物体检测结果
        
        Args:
            ocr_box: OCR边界框
            detections: 物体检测结果
            
        Returns:
            Optional[Dict]: 最近的物体检测结果
        """
        if not detections:
            return None
        
        # 计算OCR框的中心点
        ocr_center = np.array([
            (ocr_box[0][0] + ocr_box[2][0]) / 2,
            (ocr_box[0][1] + ocr_box[2][1]) / 2
        ])
        
        min_distance = float('inf')
        nearest = None
        
        for detection in detections:
            det_center = np.array(detection["center"])
            distance = np.linalg.norm(ocr_center - det_center)
            
            if distance < min_distance:
                min_distance = distance
                nearest = detection
        
        return nearest if min_distance < 100 else None  # 距离阈值100像素
    
    def recognize_roi(self, image: np.ndarray, roi: List[int]) -> List[OCRResult]:
        """
        在指定区域识别文字
        
        Args:
            image: 输入图像
            roi: 感兴趣区域 [x1, y1, x2, y2]
            
        Returns:
            List[OCRResult]: 识别结果
        """
        return self.recognize_text(image, roi)


# 全局引擎实例
_vision_ocr_engine: Optional[VisionOCREngine] = None

def get_vision_ocr_engine(use_yolo: bool = True, use_ocr: bool = True, yolo_imgsz: int = 1280) -> VisionOCREngine:
    """
    获取全局视觉OCR引擎实例
    
    Args:
        use_yolo: 是否使用YOLO
        use_ocr: 是否使用OCR
        yolo_imgsz: YOLO输入图像尺寸（默认1280，支持1080P）
        
    Returns:
        VisionOCREngine: 引擎实例
    """
    global _vision_ocr_engine
    
    if _vision_ocr_engine is None:
        _vision_ocr_engine = VisionOCREngine(use_yolo, use_ocr, yolo_imgsz=yolo_imgsz)
        _vision_ocr_engine.load_models()
    
    return _vision_ocr_engine


if __name__ == "__main__":
    # 测试视觉OCR引擎
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("=" * 60)
    print("🎯 视觉OCR引擎测试")
    print("=" * 60)
    
    engine = VisionOCREngine()
    
    # 加载模型
    if engine.load_models():
        print("✅ 模型加载成功")
        print(f"   YOLO: {engine.yolo_model is not None}")
        print(f"   OCR: {engine.ocr_model is not None}")
    else:
        print("❌ 模型加载失败")
    
    print("\n" + "=" * 60)
