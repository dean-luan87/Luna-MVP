# backend/vision/scene_description_engine.py
import cv2
import time
from typing import Dict, List, Any, Optional


class SceneDescriptionEngine:
    """
    场景描述引擎
    负责：视觉 → 场景理解 → 结构化描述
    """

    def __init__(self, yolo_detector=None):
        self.detector = yolo_detector

    def describe(self, frame=None, detections=None, ocr_results=None, hazards=None, facilities=None, env_features=None):
        """
        输入一帧图像或检测结果 → 输出结构化描述
        
        支持两种调用方式：
        1. describe(frame) - 直接传入图像帧，内部调用detector
        2. describe(detections=..., ocr_results=...) - 传入已有检测结果
        """
        if frame is None and detections is None:
            return {
                "success": False,
                "error": "EMPTY_FRAME",
                "objects": [],
                "summary": "未提供图像或检测结果"
            }

        # 如果提供了frame但没有detections，尝试使用detector
        if frame is not None and detections is None and self.detector:
            try:
                if hasattr(self.detector, 'detect'):
                    detections = self.detector.detect(frame)
                elif hasattr(self.detector, 'detect_and_recognize'):
                    result = self.detector.detect_and_recognize(frame)
                    detections = result.get("detections", [])
                    ocr_results = result.get("ocr_results", [])
            except Exception as e:
                print(f"⚠️ 检测失败: {e}")
                detections = []

        # 处理检测结果
        objects = []
        if detections:
            for d in detections:
                if isinstance(d, dict):
                    objects.append({
                        "label": d.get("label") or d.get("class") or d.get("name", "unknown"),
                        "confidence": float(d.get("confidence", 0.0)),
                        "bbox": d.get("bbox") or d.get("box", [])
                    })
                else:
                    # 如果是对象，尝试获取属性
                    objects.append({
                        "label": getattr(d, "label", getattr(d, "class", "unknown")),
                        "confidence": float(getattr(d, "confidence", 0.0)),
                        "bbox": getattr(d, "bbox", getattr(d, "box", []))
                    })

        # 处理OCR结果
        texts = []
        if ocr_results:
            for ocr in ocr_results:
                if isinstance(ocr, dict):
                    texts.append(ocr.get("text", ""))
                else:
                    texts.append(getattr(ocr, "text", ""))

        # 处理危险检测
        hazard_summary = []
        if hazards:
            for h in hazards:
                if isinstance(h, dict):
                    hazard_summary.append({
                        "type": h.get("type", "unknown"),
                        "severity": h.get("severity", "medium")
                    })
                else:
                    hazard_summary.append({
                        "type": getattr(h, "type", "unknown"),
                        "severity": getattr(h, "severity", "medium")
                    })

        # 生成摘要
        summary = self._summarize(objects, texts, hazard_summary)

        return {
            "success": True,
            "timestamp": time.time(),
            "objects": objects,
            "texts": texts,
            "hazards": hazard_summary,
            "summary": summary,
            "scene_type": self._infer_scene_type(objects, texts),
            "environment": self._infer_environment(objects, texts, hazard_summary)
        }

    def _summarize(self, objects: List[Dict], texts: List[str], hazards: List[Dict]) -> str:
        """
        基于 objects、texts、hazards 输出自然语言摘要
        """
        parts = []

        # 物体描述
        if objects:
            names = [obj.get("label", "物体") for obj in objects]
            unique_names = list(set(names))

            if len(unique_names) == 1 and len(objects) == 1:
                parts.append(f"我看到一个{unique_names[0]}。")
            elif len(unique_names) <= 3:
                joined = "、".join(unique_names)
                parts.append(f"我看到周围有：{joined}。")
            else:
                parts.append(f"我看到多个物体，包括：{', '.join(unique_names[:4])} 等。")

        # 文字描述
        if texts:
            important_texts = [t for t in texts if len(t.strip()) > 2][:3]
            if important_texts:
                parts.append(f"识别到文字：{', '.join(important_texts)}。")

        # 危险描述
        if hazards:
            critical_hazards = [h for h in hazards if h.get("severity") == "critical"]
            if critical_hazards:
                parts.append("⚠️ 检测到严重危险，请小心！")
            else:
                parts.append("检测到一些潜在危险区域。")

        if not parts:
            return "周围很安静，我没有看到明显的物体或标识。"

        return " ".join(parts)

    def _infer_scene_type(self, objects: List[Dict], texts: List[str]) -> str:
        """推断场景类型"""
        all_text = " ".join(texts).lower()
        
        # 室内场景关键词
        indoor_keywords = ["电梯", "楼层", "科室", "诊室", "病房", "洗手间", "卫生间"]
        if any(kw in all_text for kw in indoor_keywords):
            return "indoor"
        
        # 室外场景关键词
        outdoor_keywords = ["路口", "红绿灯", "斑马线", "公交站"]
        if any(kw in all_text for kw in outdoor_keywords):
            return "outdoor"
        
        # 根据物体推断
        object_labels = [obj.get("label", "").lower() for obj in objects]
        if any("car" in label or "vehicle" in label for label in object_labels):
            return "outdoor"
        
        return "unknown"

    def _infer_environment(self, objects: List[Dict], texts: List[str], hazards: List[Dict]) -> Dict[str, Any]:
        """推断环境特征"""
        return {
            "lighting": "normal",  # TODO: 根据图像亮度推断
            "crowd_density": len(objects) // 5,  # 简单估算
            "has_hazards": len(hazards) > 0,
            "has_text": len(texts) > 0
        }



