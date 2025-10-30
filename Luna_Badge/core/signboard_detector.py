#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 标识牌识别模块
支持识别洗手间、电梯、出口、导览图、安全出口、禁烟标识等
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger(__name__)

class SignboardType(Enum):
    """标识牌类型枚举"""
    TOILET = "toilet"           # 洗手间
    ELEVATOR = "elevator"       # 电梯
    EXIT = "exit"               # 出口
    MAP = "map"                 # 导览图
    SAFETY_EXIT = "safety_exit" # 安全出口
    NO_SMOKING = "no_smoking"   # 禁烟标识
    PLATFORM_DIRECTION = "platform_direction"  # 站台方向
    UNKNOWN = "unknown"         # 未知

@dataclass
class SignboardResult:
    """标识牌识别结果"""
    type: SignboardType        # 类型
    text: str                  # 文字内容
    confidence: float          # 置信度 (0-1)
    bbox: Tuple[int, int, int, int]  # 边界框 (x, y, w, h)
    center: Tuple[int, int]    # 中心点坐标
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "text": self.text,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "center": self.center
        }

class SignboardDetector:
    """标识牌检测器"""
    
    def __init__(self):
        """初始化标识牌检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 关键词字典 (中文 + 英文)
        self.keywords = {
            SignboardType.TOILET: [
                "洗手间", "卫生间", "厕所", "男厕", "女厕",
                "toilet", "restroom", "WC", "Men", "Women"
            ],
            SignboardType.ELEVATOR: [
                "电梯", "升降梯", "升降机",
                "elevator", "lift", "escalator"
            ],
            SignboardType.EXIT: [
                "出口", "安全出口", "疏散口",
                "exit", "way out", "eject"
            ],
            SignboardType.SAFETY_EXIT: [
                "安全出口", "紧急出口", "疏散通道",
                "safety exit", "emergency exit", "evacuation"
            ],
            SignboardType.MAP: [
                "导览图", "平面图", "地图", "示意图",
                "map", "guide", "floor plan", "directory"
            ],
            SignboardType.NO_SMOKING: [
                "禁止吸烟", "禁烟", "请勿吸烟",
                "no smoking", "smoking prohibited"
            ],
            SignboardType.PLATFORM_DIRECTION: [
                "往", "方向", "开往", "至",
                "towards", "to", "direction"
            ]
        }
        
        # 颜色特征 (HSV颜色空间)
        self.color_features = {
            SignboardType.TOILET: [
                (100, 150, 50, 130, 255, 255),  # 蓝色背景
                (0, 10, 200, 180, 30, 255)      # 白色背景
            ],
            SignboardType.SAFETY_EXIT: [
                (10, 20, 200, 50, 100, 255),    # 绿色背景
                (0, 10, 200, 180, 30, 255)      # 白色文字
            ],
            SignboardType.NO_SMOKING: [
                (0, 180, 0, 255, 100, 255),     # 红色圆形
                (0, 10, 200, 180, 30, 255)      # 白色背景
            ]
        }
        
        self.logger.info("🏷️ 标识牌检测器初始化完成")
    
    def detect_signboard(self, image: np.ndarray) -> List[SignboardResult]:
        """
        检测图像中的标识牌
        
        Args:
            image: 输入图像 (BGR格式)
            
        Returns:
            List[SignboardResult]: 检测结果列表
        """
        results = []
        
        try:
            # 转换为HSV颜色空间用于颜色特征检测
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 方法1: 基于OCR文字识别
            ocr_results = self._detect_by_ocr(image)
            results.extend(ocr_results)
            
            # 方法2: 基于颜色特征识别
            color_results = self._detect_by_color(hsv)
            results.extend(color_results)
            
            # 去重 - 合并位置相近的结果
            results = self._merge_nearby_results(results)
            
            # 按置信度排序
            results.sort(key=lambda x: x.confidence, reverse=True)
            
            self.logger.info(f"✅ 检测到 {len(results)} 个标识牌")
            
        except Exception as e:
            self.logger.error(f"❌ 标识牌检测失败: {e}")
        
        return results
    
    def _detect_by_ocr(self, image: np.ndarray) -> List[SignboardResult]:
        """
        基于OCR文字识别标识牌
        
        Args:
            image: 输入图像
            
        Returns:
            List[SignboardResult]: OCR识别结果
        """
        results = []
        
        try:
            # 图像预处理
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 二值化
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # 形态学操作，突出文字区域
            kernel = np.ones((3, 3), np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # 查找轮廓
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # 过滤太小的区域
                if area < 500:
                    continue
                
                # 获取边界框
                x, y, w, h = cv2.boundingRect(contour)
                
                # 提取文字区域
                text_roi = gray[y:y+h, x:x+w]
                
                # OCR识别 (使用tesseract或EasyOCR)
                # 这里简化处理，实际应该调用OCR库
                text = self._simple_text_recognition(text_roi)
                
                if not text:
                    continue
                
                # 匹配关键词
                sign_type, confidence = self._match_keywords(text)
                
                if sign_type != SignboardType.UNKNOWN:
                    result = SignboardResult(
                        type=sign_type,
                        text=text,
                        confidence=confidence,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2)
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"OCR检测失败: {e}")
        
        return results
    
    def _detect_by_color(self, hsv: np.ndarray) -> List[SignboardResult]:
        """
        基于颜色特征识别标识牌
        
        Args:
            hsv: HSV颜色空间图像
            
        Returns:
            List[SignboardResult]: 颜色检测结果
        """
        results = []
        
        try:
            for sign_type, color_ranges in self.color_features.items():
                for color_range in color_ranges:
                    # 创建颜色掩码
                    lower = np.array(color_range[:3])
                    upper = np.array(color_range[3:])
                    mask = cv2.inRange(hsv, lower, upper)
                    
                    # 形态学操作
                    kernel = np.ones((5, 5), np.uint8)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                    
                    # 查找轮廓
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    for contour in contours:
                        area = cv2.contourArea(contour)
                        
                        # 过滤太小的区域
                        if area < 1000:
                            continue
                        
                        # 获取边界框
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # 判断形状特征 (圆形/矩形)
                        aspect_ratio = w / h if h > 0 else 0
                        solidity = area / (w * h) if (w * h) > 0 else 0
                        
                        # 根据类型判断
                        confidence = 0.6  # 基础置信度
                        
                        if sign_type == SignboardType.NO_SMOKING:
                            # 禁烟标识通常是圆形
                            if 0.8 < aspect_ratio < 1.2 and solidity > 0.7:
                                confidence = 0.85
                        elif sign_type in [SignboardType.TOILET, SignboardType.SAFETY_EXIT]:
                            # 矩形标识
                            if 1.5 < aspect_ratio < 3.0 and solidity > 0.6:
                                confidence = 0.8
                        
                        if confidence > 0.6:
                            result = SignboardResult(
                                type=sign_type,
                                text=sign_type.value,
                                confidence=confidence,
                                bbox=(x, y, w, h),
                                center=(x + w // 2, y + h // 2)
                            )
                            results.append(result)
                            
        except Exception as e:
            self.logger.error(f"颜色检测失败: {e}")
        
        return results
    
    def _simple_text_recognition(self, text_roi: np.ndarray) -> str:
        """
        简单的文字识别 (模拟OCR)
        
        实际应该调用 tesseract 或 EasyOCR
        
        Args:
            text_roi: 文字区域图像
            
        Returns:
            str: 识别的文字
        """
        # 这里简化处理
        # 实际实现应该调用OCR库:
        # import pytesseract
        # text = pytesseract.image_to_string(text_roi, lang='chi_sim+eng')
        
        # 或者使用EasyOCR:
        # import easyocr
        # reader = easyocr.Reader(['ch_sim', 'en'])
        # result = reader.readtext(text_roi)
        # text = ' '.join([item[1] for item in result])
        
        # 暂时返回空字符串
        return ""
    
    def _match_keywords(self, text: str) -> Tuple[SignboardType, float]:
        """
        匹配关键词确定标识牌类型
        
        Args:
            text: 识别出的文字
            
        Returns:
            Tuple[SignboardType, float]: (类型, 置信度)
        """
        text_lower = text.lower()
        
        max_confidence = 0.0
        matched_type = SignboardType.UNKNOWN
        
        for sign_type, keywords in self.keywords.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    # 计算匹配度
                    match_ratio = len(keyword) / len(text) if text else 0
                    confidence = min(match_ratio * 1.5, 1.0)
                    
                    if confidence > max_confidence:
                        max_confidence = confidence
                        matched_type = sign_type
        
        return matched_type, max_confidence
    
    def _merge_nearby_results(self, results: List[SignboardResult], 
                            threshold: int = 50) -> List[SignboardResult]:
        """
        合并位置相近的检测结果
        
        Args:
            results: 检测结果列表
            threshold: 距离阈值（像素）
            
        Returns:
            List[SignboardResult]: 去重后的结果
        """
        if not results:
            return []
        
        merged = []
        used = set()
        
        for i, result in enumerate(results):
            if i in used:
                continue
            
            # 查找相近的结果
            nearby = [result]
            for j, other in enumerate(results):
                if i != j and j not in used:
                    # 计算中心点距离
                    dx = result.center[0] - other.center[0]
                    dy = result.center[1] - other.center[1]
                    distance = np.sqrt(dx*dx + dy*dy)
                    
                    if distance < threshold:
                        nearby.append(other)
                        used.add(j)
            
            # 合并相近结果（保留置信度最高的）
            if len(nearby) > 1:
                best = max(nearby, key=lambda x: x.confidence)
                merged.append(best)
            else:
                merged.append(nearby[0])
        
        return merged
    
    def get_detection_summary(self, results: List[SignboardResult]) -> Dict[str, Any]:
        """
        获取检测结果摘要
        
        Args:
            results: 检测结果列表
            
        Returns:
            Dict[str, Any]: 摘要信息
        """
        summary = {
            "total": len(results),
            "by_type": {}
        }
        
        for result in results:
            type_name = result.type.value
            if type_name not in summary["by_type"]:
                summary["by_type"][type_name] = 0
            summary["by_type"][type_name] += 1
        
        return summary
    
    def check_platform_direction(self,
                                detected_text: str,
                                target_station: str) -> Dict[str, Any]:
        """
        检查站台方向是否匹配目标
        
        Args:
            detected_text: OCR识别的站台标牌文字（如"往中山公园方向"）
            target_station: 目标站点名称
        
        Returns:
            Dict[str, Any]: 方向匹配结果
        """
        # 从文字中提取方向信息
        direction_text = self._extract_direction(detected_text)
        
        if not direction_text:
            return {
                "matched": False,
                "message": "无法识别站台方向信息",
                "detected_direction": None,
                "target_station": target_station
            }
        
        # 检查是否包含目标站点（简化匹配，实际可用更复杂的NLP）
        matched = target_station in detected_text or \
                  any(keyword in detected_text for keyword in [target_station[:2], target_station[:3]])
        
        if matched:
            message = None  # 方向正确，无需播报
        else:
            message = f"您当前站台方向为{direction_text}，与目标{target_station}不一致，请前往对面站台。"
        
        return {
            "matched": matched,
            "message": message,
            "detected_direction": direction_text,
            "target_station": target_station
        }
    
    def _extract_direction(self, text: str) -> Optional[str]:
        """
        从文字中提取方向信息
        
        Args:
            text: OCR识别的文字
        
        Returns:
            Optional[str]: 提取的方向信息
        """
        # 匹配"往XX方向"、"开往XX"等模式
        patterns = [
            r'往([^方向]+)方向',
            r'开往([^，,。]+)',
            r'至([^，,。]+)',
            r'方向：([^，,。]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None


# 全局检测器实例
global_signboard_detector = SignboardDetector()

def detect_signboards(image: np.ndarray) -> List[SignboardResult]:
    """检测标识牌的便捷函数"""
    return global_signboard_detector.detect_signboard(image)


if __name__ == "__main__":
    # 测试标识牌检测
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建测试图像
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 绘制一个模拟的标识牌（蓝色矩形）
    cv2.rectangle(test_image, (200, 150), (400, 250), (255, 100, 50), -1)
    cv2.putText(test_image, "洗手间", (230, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # 进行检测
    detector = SignboardDetector()
    results = detector.detect_signboard(test_image)
    
    print(f"检测结果: {len(results)} 个标识牌")
    for i, result in enumerate(results):
        print(f"\n标识牌 {i+1}:")
        print(f"  类型: {result.type.value}")
        print(f"  文字: {result.text}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  位置: {result.bbox}")
        print(f"  中心: {result.center}")
    
    # 获取摘要
    summary = detector.get_detection_summary(results)
    print(f"\n检测摘要: {summary}")
