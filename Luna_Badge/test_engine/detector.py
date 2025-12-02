#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO 视觉检测模块
集成到现有 Luna Badge vision_engine
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class Detector:
    """YOLO 视觉检测模块"""
    
    def __init__(self, vision_engine=None):
        """
        初始化检测器
        
        Args:
            vision_engine: 现有的 vision_engine 实例（如果为 None，则尝试从 web_test_server 获取）
        """
        self.vision_engine = vision_engine
        self._init_engine()
    
    def _init_engine(self):
        """尝试初始化 vision_engine"""
        if self.vision_engine is not None:
            return
        
        try:
            # 尝试从 web_test_server 导入全局 vision_engine
            import sys
            if 'web_test_server' in sys.modules:
                from web_test_server import vision_engine
                self.vision_engine = vision_engine
        except Exception as e:
            logger.warning(f"无法获取 vision_engine: {e}")
    
    def detect(self, img_path: str) -> List[Dict[str, Any]]:
        """
        对图片执行 YOLO 检测
        
        Args:
            img_path: 图片路径
        
        Returns:
            检测结果列表，每个结果包含：
            {
                "class": "person",
                "confidence": 0.95,
                "bbox": [x1, y1, x2, y2]
            }
        """
        import cv2
        
        try:
            image_np = cv2.imread(img_path)
            if image_np is None:
                logger.warning(f"无法读取图片: {img_path}")
                return []
            
            # 使用现有的 vision_engine
            if self.vision_engine is not None:
                try:
                    result = self.vision_engine.detect_and_recognize(image_np)
                    detections = result.get("detections", []) or []
                    
                    # 转换为统一格式
                    formatted = []
                    for det in detections:
                        formatted.append({
                            "class": det.get("class") or det.get("label") or "unknown",
                            "confidence": det.get("confidence") or det.get("score") or 0.0,
                            "bbox": det.get("bbox") or det.get("box") or []
                        })
                    return formatted
                except Exception as e:
                    logger.warning(f"vision_engine 检测失败: {e}")
            
            # 降级：如果没有 vision_engine，返回空结果
            logger.warning("vision_engine 不可用，返回空检测结果")
            return []
        except Exception as e:
            logger.error(f"检测图片失败 {img_path}: {e}")
            return []
    
    def get_labels(self, img_path: str) -> List[str]:
        """
        获取检测到的标签列表（简化版）
        
        Args:
            img_path: 图片路径
        
        Returns:
            标签列表，例如 ["person", "car", "bicycle"]
        """
        detections = self.detect(img_path)
        labels = [d["class"] for d in detections]
        return labels


