#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 公共设施识别模块
支持识别椅子、公交站、地铁入口、医院、公园、学校、导览牌等公共设施
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger(__name__)

class FacilityType(Enum):
    """公共设施类型枚举"""
    CHAIR = "chair"               # 椅子
    BUS_STOP = "bus_stop"         # 公交站
    SUBWAY = "subway"             # 地铁入口
    HOSPITAL = "hospital"         # 医院
    PARK = "park"                 # 公园
    SCHOOL = "school"             # 学校
    INFO_BOARD = "info_board"     # 导览牌
    UNKNOWN = "unknown"           # 未知

@dataclass
class FacilityResult:
    """公共设施识别结果"""
    type: FacilityType                   # 类型
    label: str                           # 标签文字（如具体名称）
    confidence: float                    # 置信度 (0-1)
    bbox: Tuple[int, int, int, int]      # 边界框 (x, y, w, h)
    center: Tuple[int, int]              # 中心点坐标
    features: Dict[str, Any]             # 特征信息
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "label": self.label,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "center": self.center,
            "features": self.features
        }

class FacilityDetector:
    """公共设施检测器"""
    
    def __init__(self):
        """初始化公共设施检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 关键词字典 (中文 + 英文)
        self.keywords = {
            FacilityType.CHAIR: [
                "椅子", "座椅", "长椅",
                "chair", "bench", "seat"
            ],
            FacilityType.BUS_STOP: [
                "公交站", "公交车站", "巴士站", "公交站台",
                "bus stop", "bus station", "bus shelter"
            ],
            FacilityType.SUBWAY: [
                "地铁", "地铁站", "地铁入口", "轨道交通",
                "subway", "metro", "underground", "train station"
            ],
            FacilityType.HOSPITAL: [
                "医院", "诊所", "卫生院", "医疗中心",
                "hospital", "clinic", "medical center"
            ],
            FacilityType.PARK: [
                "公园", "花园", "绿地", "广场",
                "park", "garden", "plaza", "square"
            ],
            FacilityType.SCHOOL: [
                "学校", "幼儿园", "小学", "中学", "大学",
                "school", "kindergarten", "college", "university"
            ],
            FacilityType.INFO_BOARD: [
                "导览牌", "信息牌", "指示牌", "公告牌",
                "info board", "guide board", "information board"
            ]
        }
        
        # 特征模式（用于提取具体名称）
        self.name_patterns = {
            FacilityType.HOSPITAL: [
                r'([\u4e00-\u9fa5]+医院)',
                r'([\u4e00-\u9fa5]+诊所)',
                r'([A-Za-z]+Hospital)',
                r'([A-Za-z]+Clinic)'
            ],
            FacilityType.PARK: [
                r'([\u4e00-\u9fa5]+公园)',
                r'([\u4e00-\u9fa5]+广场)',
                r'([A-Za-z]+Park)',
                r'([A-Za-z]+Square)'
            ],
            FacilityType.BUS_STOP: [
                r'([\u4e00-\u9fa5]+公交站)',
                r'([\u4e00-\u9fa5]+站)',
                r'([A-Za-z]+Bus Stop)',
                r'([A-Za-z]+Stop)'
            ],
            FacilityType.SCHOOL: [
                r'([\u4e00-\u9fa5]+学校)',
                r'([\u4e00-\u9fa5]+小学)',
                r'([\u4e00-\u9fa5]+中学)',
                r'([A-Za-z]+School)',
                r'([A-Za-z]+University)'
            ]
        }
        
        # 颜色特征 (HSV颜色空间)
        self.color_features = {
            FacilityType.BUS_STOP: [
                (15, 0, 100, 25, 50, 255),   # 黄色站牌
                (100, 150, 50, 130, 255, 255)  # 蓝色站台
            ],
            FacilityType.SUBWAY: [
                (100, 150, 50, 130, 255, 255),  # 蓝色标识
                (0, 10, 200, 180, 30, 255)      # 白色背景
            ],
            FacilityType.HOSPITAL: [
                (100, 150, 50, 130, 255, 255),  # 蓝色十字
                (0, 10, 200, 180, 30, 255)      # 白色背景
            ],
            FacilityType.PARK: [
                (50, 50, 100, 80, 255, 255),    # 绿色植被
                (20, 50, 100, 40, 255, 255)     # 棕色长椅
            ]
        }
        
        # 形状特征（宽高比范围）
        self.shape_features = {
            FacilityType.CHAIR: (2.0, 5.0),      # 长条形
            FacilityType.BUS_STOP: (1.5, 3.0),  # 矩形站牌
            FacilityType.INFO_BOARD: (1.0, 2.0), # 方形牌
            FacilityType.SUBWAY: (0.8, 1.2),     # 圆形标识
        }
        
        self.logger.info("🏛️ 公共设施检测器初始化完成")
    
    def detect_facility(self, image: np.ndarray) -> List[FacilityResult]:
        """
        检测图像中的公共设施
        
        Args:
            image: 输入图像 (BGR格式)
            
        Returns:
            List[FacilityResult]: 检测结果列表
        """
        results = []
        
        try:
            # 转换为HSV颜色空间用于颜色特征检测
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 方法1: 基于文字识别
            text_results = self._detect_by_text(image)
            results.extend(text_results)
            
            # 方法2: 基于颜色和形状特征
            feature_results = self._detect_by_features(hsv, image.shape)
            results.extend(feature_results)
            
            # 方法3: 基于形状检测（椅子、长椅等）
            shape_results = self._detect_by_shape(image)
            results.extend(shape_results)
            
            # 去重 - 合并位置相近的结果
            results = self._merge_nearby_results(results)
            
            # 按置信度排序
            results.sort(key=lambda x: x.confidence, reverse=True)
            
            self.logger.info(f"✅ 检测到 {len(results)} 个公共设施")
            
        except Exception as e:
            self.logger.error(f"❌ 公共设施检测失败: {e}")
        
        return results
    
    def _detect_by_text(self, image: np.ndarray) -> List[FacilityResult]:
        """
        基于文字识别公共设施
        
        Args:
            image: 输入图像
            
        Returns:
            List[FacilityResult]: 文字识别结果
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
                
                # OCR识别 (简化版)
                text = self._simple_text_recognition(text_roi)
                
                if not text:
                    continue
                
                # 匹配关键词
                facility_type, confidence = self._match_keywords(text)
                
                # 提取具体名称
                label = self._extract_name(text, facility_type)
                
                if facility_type != FacilityType.UNKNOWN:
                    result = FacilityResult(
                        type=facility_type,
                        label=label,
                        confidence=confidence,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2),
                        features={"detection_method": "text", "original_text": text}
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"文字检测失败: {e}")
        
        return results
    
    def _detect_by_features(self, hsv: np.ndarray, img_shape: Tuple[int, int]) -> List[FacilityResult]:
        """
        基于颜色和形状特征识别
        
        Args:
            hsv: HSV颜色空间图像
            img_shape: 图像尺寸
            
        Returns:
            List[FacilityResult]: 特征检测结果
        """
        results = []
        
        try:
            for facility_type, color_ranges in self.color_features.items():
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
                        
                        # 判断形状特征
                        aspect_ratio = w / h if h > 0 else 0
                        confidence = 0.6  # 基础置信度
                        
                        # 根据形状特征调整置信度
                        if facility_type in self.shape_features:
                            min_ratio, max_ratio = self.shape_features[facility_type]
                            if min_ratio <= aspect_ratio <= max_ratio:
                                confidence = 0.8
                        
                        if confidence > 0.6:
                            result = FacilityResult(
                                type=facility_type,
                                label=facility_type.value,
                                confidence=confidence,
                                bbox=(x, y, w, h),
                                center=(x + w // 2, y + h // 2),
                                features={
                                    "detection_method": "color_shape",
                                    "aspect_ratio": aspect_ratio,
                                    "area": area
                                }
                            )
                            results.append(result)
                            
        except Exception as e:
            self.logger.error(f"特征检测失败: {e}")
        
        return results
    
    def _detect_by_shape(self, image: np.ndarray) -> List[FacilityResult]:
        """
        基于形状检测（如长椅、椅子）
        
        Args:
            image: 输入图像
            
        Returns:
            List[FacilityResult]: 形状检测结果
        """
        results = []
        
        try:
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 边缘检测
            edges = cv2.Canny(gray, 50, 150)
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # 过滤太小的区域
                if area < 2000:
                    continue
                
                # 获取边界框
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # 检测长条形物体（可能是长椅）
                if 3.0 <= aspect_ratio <= 10.0:
                    result = FacilityResult(
                        type=FacilityType.CHAIR,
                        label="长椅",
                        confidence=0.75,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2),
                        features={
                            "detection_method": "shape",
                            "aspect_ratio": aspect_ratio,
                            "area": area
                        }
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"形状检测失败: {e}")
        
        return results
    
    def _simple_text_recognition(self, text_roi: np.ndarray) -> str:
        """
        简单的文字识别 (模拟OCR)
        
        Args:
            text_roi: 文字区域图像
            
        Returns:
            str: 识别的文字
        """
        # 这里简化处理
        # 实际实现应该调用OCR库
        return ""
    
    def _match_keywords(self, text: str) -> Tuple[FacilityType, float]:
        """
        匹配关键词确定设施类型
        
        Args:
            text: 识别出的文字
            
        Returns:
            Tuple[FacilityType, float]: (类型, 置信度)
        """
        text_lower = text.lower()
        
        max_confidence = 0.0
        matched_type = FacilityType.UNKNOWN
        
        for facility_type, keywords in self.keywords.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    # 计算匹配度
                    match_ratio = len(keyword) / len(text) if text else 0
                    confidence = min(match_ratio * 1.5, 1.0)
                    
                    if confidence > max_confidence:
                        max_confidence = confidence
                        matched_type = facility_type
        
        return matched_type, max_confidence
    
    def _extract_name(self, text: str, facility_type: FacilityType) -> str:
        """
        提取具体名称（如"仁爱医院"、"人民公园公交站"）
        
        Args:
            text: 识别出的文字
            facility_type: 设施类型
            
        Returns:
            str: 提取的名称
        """
        if facility_type not in self.name_patterns:
            return facility_type.value
        
        # 使用正则表达式提取名称
        for pattern in self.name_patterns[facility_type]:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return facility_type.value
    
    def _merge_nearby_results(self, results: List[FacilityResult],
                              threshold: int = 50) -> List[FacilityResult]:
        """
        合并位置相近的检测结果
        
        Args:
            results: 检测结果列表
            threshold: 距离阈值（像素）
            
        Returns:
            List[FacilityResult]: 去重后的结果
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
    
    def get_detection_summary(self, results: List[FacilityResult]) -> Dict[str, Any]:
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


# 全局检测器实例
global_facility_detector = FacilityDetector()

def detect_facilities(image: np.ndarray) -> List[FacilityResult]:
    """检测公共设施的便捷函数"""
    return global_facility_detector.detect_facility(image)


if __name__ == "__main__":
    # 测试公共设施检测
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建测试图像 - 公交站
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 绘制一个模拟的公交站牌（黄色矩形）
    cv2.rectangle(test_image, (150, 100), (350, 200), (0, 200, 255), -1)
    cv2.putText(test_image, "人民公园公交站", (165, 160),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # 绘制一个长椅（棕色矩形）
    cv2.rectangle(test_image, (400, 300), (550, 330), (42, 42, 165), -1)
    
    # 进行检测
    detector = FacilityDetector()
    results = detector.detect_facility(test_image)
    
    print(f"检测结果: {len(results)} 个公共设施")
    for i, result in enumerate(results):
        print(f"\n公共设施 {i+1}:")
        print(f"  类型: {result.type.value}")
        print(f"  标签: {result.label}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  位置: {result.bbox}")
        print(f"  中心: {result.center}")
        print(f"  特征: {result.features}")
    
    # 获取摘要
    summary = detector.get_detection_summary(results)
    print(f"\n检测摘要: {summary}")
