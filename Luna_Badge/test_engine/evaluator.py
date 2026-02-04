#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则判断与标签匹配模块
判断检测结果是否正确、漏检、错检
"""

import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)


class Evaluator:
    """规则判断与标签匹配模块"""
    
    def evaluate(self, detection_labels: List[str], ground_truth: List[str], 
                 ocr_texts: List[str] = None) -> Dict[str, Any]:
        """
        评估检测结果
        
        Args:
            detection_labels: 检测到的标签列表，例如 ["person", "car"]
            ground_truth: 期望的标签列表，例如 ["person", "stairs"]
            ocr_texts: OCR 识别到的文字列表（可选），例如 ["电梯", "出口"]
        
        Returns:
            {
                "correct": ["person"],      # 正确识别的标签
                "incorrect": [],            # 错误识别的标签（检测到了但不在期望中）
                "missing": ["stairs"],       # 漏检的标签（期望但未检测到）
                "extra": ["car"],           # 额外检测到的标签（不在期望中）
                "accuracy": 0.5,            # 准确率
                "precision": 0.5,           # 精确率
                "recall": 0.5,              # 召回率
                "f1": 0.5                   # F1 分数
            }
        """
        detection_set = set(detection_labels)
        ground_truth_set = set(ground_truth)
        
        # 基础匹配
        correct = list(detection_set & ground_truth_set)  # 交集
        missing = list(ground_truth_set - detection_set)  # 期望但未检测到
        extra = list(detection_set - ground_truth_set)    # 检测到但不在期望中
        
        # OCR 辅助匹配（如果提供了 OCR 结果）
        if ocr_texts:
            ocr_text = " ".join(ocr_texts).lower()
            for gt in ground_truth:
                gt_lower = gt.lower()
                # 如果 OCR 文本中包含期望标签，也算作正确
                if gt_lower in ocr_text and gt not in correct:
                    correct.append(gt)
                    if gt in missing:
                        missing.remove(gt)
        
        # 计算指标
        total_expected = len(ground_truth_set)
        total_detected = len(detection_set)
        total_correct = len(correct)
        
        accuracy = total_correct / total_expected if total_expected > 0 else 0.0
        precision = total_correct / total_detected if total_detected > 0 else 0.0
        recall = total_correct / total_expected if total_expected > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            "correct": correct,
            "incorrect": extra,  # 这里 incorrect 和 extra 是同一个概念
            "missing": missing,
            "extra": extra,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "total_expected": total_expected,
            "total_detected": total_detected,
            "total_correct": total_correct
        }
    
    def evaluate_image(self, img_path: str, ground_truth: List[str], 
                       detector, ocr_reader=None) -> Dict[str, Any]:
        """
        评估单张图片
        
        Args:
            img_path: 图片路径
            ground_truth: 期望的标签列表
            detector: Detector 实例
            ocr_reader: OCRReader 实例（可选）
        
        Returns:
            评估结果字典
        """
        # 获取检测结果
        detections = detector.detect(img_path)
        detection_labels = [d["class"] for d in detections]
        
        # 获取 OCR 结果（如果提供了 OCR 读取器）
        ocr_texts = None
        if ocr_reader is not None:
            ocr_results = ocr_reader.read(img_path)
            ocr_texts = [r["text"] for r in ocr_results if r.get("text")]
        
        # 评估
        result = self.evaluate(detection_labels, ground_truth, ocr_texts)
        
        # 添加图片路径和原始检测结果
        result["img_path"] = img_path
        result["detections"] = detections
        result["ocr_texts"] = ocr_texts or []
        
        return result


