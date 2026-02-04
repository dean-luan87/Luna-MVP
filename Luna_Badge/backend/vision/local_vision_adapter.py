#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地视觉适配器：封装现有 YOLO vision_engine + OCR 结果
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class LocalVisionAdapter:
    """
    本地视觉适配器：
    - 封装现有 YOLO vision_engine + OCR 结果
    - 输出结构化语义，供融合器使用
    """

    def __init__(self, vision_engine=None, ocr_engine=None):
        self.vision_engine = vision_engine
        self.ocr_engine = ocr_engine

    def is_available(self) -> bool:
        return self.vision_engine is not None

    def analyze_image(self, image_np) -> Dict[str, Any]:
        """
        返回统一结构：
        {
          "objects": [{"label": str, "confidence": float, "bbox": [x,y,w,h]}, ...],
          "texts": [str, ...],
          "raw": 原始结果
        }
        """
        if not self.vision_engine:
            return {"objects": [], "texts": [], "raw": None}

        try:
            vision_results = self.vision_engine.detect_and_recognize(image_np)
        except Exception as e:
            logger.warning(f"⚠️ LocalVisionAdapter: detect_and_recognize 失败: {e}")
            return {"objects": [], "texts": [], "raw": None}

        objects = []
        for det in vision_results.get("detections", []):
            label = det.get("class") or det.get("name") or ""
            conf = float(det.get("confidence", 0.0))
            bbox = det.get("bbox", None)
            objects.append({
                "label": label,
                "confidence": conf,
                "bbox": bbox
            })

        texts = [t.get("text", "") for t in vision_results.get("ocr_results", []) if t.get("text")]

        return {
            "objects": objects,
            "texts": texts,
            "raw": vision_results
        }


