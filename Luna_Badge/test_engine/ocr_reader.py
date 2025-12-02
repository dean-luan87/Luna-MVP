#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 识别模块
使用 PaddleOCR（如果可用）或现有 OCR 引擎
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except (ImportError, ValueError, AttributeError) as e:
    PADDLEOCR_AVAILABLE = False
    logger.warning(f"PaddleOCR 不可用，OCR 功能将使用简化版本。原因: {type(e).__name__}")


class OCRReader:
    """OCR 识别模块"""
    
    def __init__(self, vision_engine=None):
        """
        初始化 OCR 读取器
        
        Args:
            vision_engine: 现有的 vision_engine 实例（如果为 None，则尝试从 web_test_server 获取）
        """
        self.vision_engine = vision_engine
        self.paddle_ocr = None
        self._init_ocr()
    
    def _init_ocr(self):
        """初始化 OCR 引擎"""
        if PADDLEOCR_AVAILABLE:
            try:
                self.paddle_ocr = PaddleOCR(use_angle_cls=True, lang="ch")
                logger.info("PaddleOCR 初始化成功")
            except Exception as e:
                logger.warning(f"PaddleOCR 初始化失败: {e}")
        
        if self.vision_engine is None:
            try:
                import sys
                if 'web_test_server' in sys.modules:
                    from web_test_server import vision_engine
                    self.vision_engine = vision_engine
            except Exception as e:
                logger.debug(f"无法获取 vision_engine: {e}")
    
    def read(self, img_path: str) -> List[Dict[str, Any]]:
        """
        读取图片中的文字
        
        Args:
            img_path: 图片路径
        
        Returns:
            OCR 结果列表，每个结果包含：
            {
                "text": "文字内容",
                "confidence": 0.95,
                "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            }
        """
        import cv2
        
        try:
            image_np = cv2.imread(img_path)
            if image_np is None:
                logger.warning(f"无法读取图片: {img_path}")
                return []
            
            # 优先使用 PaddleOCR
            if self.paddle_ocr is not None:
                try:
                    result = self.paddle_ocr.ocr(img_path, cls=True)
                    if result and len(result) > 0:
                        formatted = []
                        for line in result[0]:
                            if line:
                                formatted.append({
                                    "text": line[1][0],
                                    "confidence": line[1][1],
                                    "bbox": line[0]
                                })
                        return formatted
                except Exception as e:
                    logger.warning(f"PaddleOCR 识别失败: {e}")
            
            # 降级：使用现有的 vision_engine
            if self.vision_engine is not None:
                try:
                    result = self.vision_engine.detect_and_recognize(image_np)
                    ocr_results = result.get("ocr_results", []) or []
                    
                    # 转换为统一格式
                    formatted = []
                    for ocr in ocr_results:
                        formatted.append({
                            "text": ocr.get("text") or ocr.get("content") or "",
                            "confidence": ocr.get("confidence") or ocr.get("score") or 0.0,
                            "bbox": ocr.get("bbox") or ocr.get("box") or []
                        })
                    return formatted
                except Exception as e:
                    logger.warning(f"vision_engine OCR 失败: {e}")
            
            # 如果都不可用，返回空结果
            logger.warning("OCR 引擎不可用，返回空结果")
            return []
        except Exception as e:
            logger.error(f"OCR 识别失败 {img_path}: {e}")
            return []
    
    def get_texts(self, img_path: str) -> List[str]:
        """
        获取识别到的文字列表（简化版）
        
        Args:
            img_path: 图片路径
        
        Returns:
            文字列表，例如 ["电梯", "出口", "123"]
        """
        results = self.read(img_path)
        texts = [r["text"] for r in results if r.get("text")]
        return texts

