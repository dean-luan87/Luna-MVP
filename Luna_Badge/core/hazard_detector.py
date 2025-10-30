#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 危险环境识别模块
识别潜在危险环境，触发安全播报与状态警告
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)

class HazardType(Enum):
    """危险类型枚举"""
    WATER = "water"               # 水域（河边、喷泉）
    CONSTRUCTION = "construction" # 工地
    PIT = "pit"                   # 坑洞
    HIGH_PLATFORM = "high_platform"  # 无护栏高台
    ELECTRIC = "electric"         # 电力设施
    ROADWAY = "roadway"           # 车行道
    UNKNOWN = "unknown"           # 未知

class SeverityLevel(Enum):
    """严重程度"""
    LOW = "low"                   # 低风险
    MEDIUM = "medium"             # 中风险
    HIGH = "high"                 # 高风险
    CRITICAL = "critical"         # 极高风险

@dataclass
class HazardResult:
    """危险识别结果"""
    type: HazardType              # 危险类型
    severity: SeverityLevel       # 严重程度
    bbox: Tuple[int, int, int, int]  # 边界框 (x, y, w, h)
    center: Tuple[int, int]       # 中心点坐标
    confidence: float             # 置信度
    features: Dict[str, Any]      # 特征信息
    timestamp: float              # 检测时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "bbox": self.bbox,
            "center": self.center,
            "confidence": self.confidence,
            "features": self.features,
            "timestamp": self.timestamp
        }

class HazardDetector:
    """危险环境检测器"""
    
    def __init__(self):
        """初始化危险环境检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 颜色特征 (HSV颜色空间)
        self.color_features = {
            HazardType.WATER: [
                (100, 100, 100, 120, 255, 255),  # 蓝色水域
                (15, 0, 100, 25, 50, 255)       # 橙色告警标志
            ],
            HazardType.CONSTRUCTION: [
                (15, 0, 100, 25, 50, 255),       # 橙色警示
                (0, 0, 0, 180, 255, 50)          # 深色
            ],
            HazardType.ROADWAY: [
                (0, 0, 0, 180, 30, 80),          # 灰色路面
                (0, 0, 100, 180, 50, 255)        # 白色标线
            ],
            HazardType.ELECTRIC: [
                (15, 0, 200, 25, 100, 255),      # 黄色警告
                (100, 150, 50, 130, 255, 255)    # 蓝色电力标识
            ]
        }
        
        # 严重程度阈值
        self.severity_thresholds = {
            HazardType.WATER: {
                "area_min": 5000,    # 小水域
                "area_medium": 20000,  # 中水域
                "area_max": 50000,   # 大水域
                "distance_threshold": 50  # 像素距离
            },
            HazardType.CONSTRUCTION: {
                "area_min": 10000,
                "area_medium": 30000,
                "area_max": 60000,
                "confidence_threshold": 0.7
            },
            HazardType.PIT: {
                "area_min": 2000,
                "area_medium": 8000,
                "area_max": 20000,
                "depth_threshold": 0.3
            },
            HazardType.HIGH_PLATFORM: {
                "height_threshold": 100,  # 像素高度
                "edge_detection": True
            },
            HazardType.ELECTRIC: {
                "warning_sign_area": 1000,
                "confidence_threshold": 0.8
            },
            HazardType.ROADWAY: {
                "traffic_density": 0.5,
                "crossing_danger": True
            }
        }
        
        # 危险区域记录
        self.detected_hazards: List[HazardResult] = []
        
        self.logger.info("⚠️ 危险环境检测器初始化完成")
    
    def detect_hazards(self, image: np.ndarray) -> List[HazardResult]:
        """
        检测图像中的危险环境
        
        Args:
            image: 输入图像 (BGR格式)
            
        Returns:
            List[HazardResult]: 检测结果列表
        """
        results = []
        
        try:
            # 转换为HSV颜色空间
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 方法1: 颜色特征检测
            color_results = self._detect_by_color(hsv, image.shape)
            results.extend(color_results)
            
            # 方法2: 形状分析检测（坑洞、高台）
            shape_results = self._detect_by_shape(image)
            results.extend(shape_results)
            
            # 方法3: 纹理分析检测（工地、路面）
            texture_results = self._detect_by_texture(image)
            results.extend(texture_results)
            
            # 去重和排序
            results = self._filter_and_sort(results)
            
            # 评估严重程度
            results = self._assess_severity(results, image.shape)
            
            # 记录检测结果
            self.detected_hazards = results
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ 危险检测失败: {e}")
            return []
    
    def evaluate_construction_detour(self,
                                     construction_hazard: HazardResult,
                                     current_position: Tuple[float, float],
                                     detour_distance_meters: float = 10.0) -> Dict[str, Any]:
        """
        评估施工绕行方案
        
        Args:
            construction_hazard: 施工区域检测结果
            current_position: 当前位置 (lat, lng) 或 (x, y)
            detour_distance_meters: 预计绕行距离（米）
        
        Returns:
            Dict[str, Any]: 绕行评估结果
        """
        if construction_hazard.type != HazardType.CONSTRUCTION:
            return {
                "needs_detour": False,
                "message": None
            }
        
        # 计算到绕行点的距离（简化：假设10米）
        # 实际应该根据路径规划计算真实距离
        distance_to_detour = detour_distance_meters
        
        # 判断距离并生成播报消息
        messages = []
        
        if distance_to_detour > 10:
            messages.append(f"前方施工，预计{distance_to_detour:.0f}米后需绕行，请准备右转。")
        elif distance_to_detour > 5:
            messages.append("前方施工，即将到达绕行点，请准备右转。")
        else:
            messages.append("现在右转进入绕行通道。")
            messages.append("现在右转进入绕行通道。")  # 重复一次
        
        return {
            "needs_detour": True,
            "detour_distance": distance_to_detour,
            "messages": messages,
            "hazard_type": construction_hazard.type.value,
            "severity": construction_hazard.severity.value
        }
    
    def estimate_detour_distance(self,
                                 hazard_bbox: Tuple[int, int, int, int],
                                 image_shape: Tuple[int, int]) -> float:
        """
        估算绕行距离（像素转米）
        
        Args:
            hazard_bbox: 危险区域边界框
            image_shape: 图像尺寸
        
        Returns:
            float: 估算距离（米）
        """
        x, y, w, h = hazard_bbox
        
        # 假设图像中心为当前位置，危险区域中心为施工点
        # 简化的距离估算（实际应使用深度估计或GPS）
        center_x, center_y = image_shape[1] // 2, image_shape[0] // 2
        hazard_center_x = x + w // 2
        hazard_center_y = y + h // 2
        
        # 计算像素距离
        pixel_distance = np.sqrt((hazard_center_x - center_x)**2 + 
                                (hazard_center_y - center_y)**2)
        
        # 假设图像宽度640像素对应真实距离约20米（可根据实际调整）
        meters_per_pixel = 20.0 / image_shape[1]
        distance_meters = pixel_distance * meters_per_pixel
        
        return max(5.0, min(distance_meters, 50.0))  # 限制在5-50米之间
    
    def _detect_by_color(self, hsv: np.ndarray, img_shape: Tuple[int, int]) -> List[HazardResult]:
        """
        基于颜色特征检测危险
        
        Args:
            hsv: HSV颜色空间图像
            img_shape: 图像尺寸
            
        Returns:
            List[HazardResult]: 颜色检测结果
        """
        results = []
        
        try:
            for hazard_type, color_ranges in self.color_features.items():
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
                        
                        # 根据类型过滤面积
                        if hazard_type == HazardType.WATER and area < 5000:
                            continue
                        if hazard_type == HazardType.CONSTRUCTION and area < 5000:
                            continue
                        
                        # 获取边界框
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # 计算置信度
                        confidence = min(area / 10000.0, 1.0)
                        
                        result = HazardResult(
                            type=hazard_type,
                            severity=SeverityLevel.MEDIUM,  # 临时，后续会重新评估
                            bbox=(x, y, w, h),
                            center=(x + w // 2, y + h // 2),
                            confidence=confidence,
                            features={
                                "detection_method": "color",
                                "area": area
                            },
                            timestamp=time.time()
                        )
                        results.append(result)
                        
        except Exception as e:
            self.logger.error(f"颜色检测失败: {e}")
        
        return results
    
    def _detect_by_shape(self, image: np.ndarray) -> List[HazardResult]:
        """
        基于形状分析检测（坑洞、高台）
        
        Args:
            image: 输入图像
            
        Returns:
            List[HazardResult]: 形状检测结果
        """
        results = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 边缘检测
            edges = cv2.Canny(gray, 50, 150)
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # 过滤太小的区域
                if area < 500:
                    continue
                
                # 获取边界框
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # 检测坑洞特征（不规则形状、深色区域）
                solidity = area / (w * h) if (w * h) > 0 else 0
                
                if 0.3 < aspect_ratio < 3.0 and solidity < 0.7:
                    # 可能是坑洞
                    result = HazardResult(
                        type=HazardType.PIT,
                        severity=SeverityLevel.HIGH,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2),
                        confidence=0.7,
                        features={
                            "detection_method": "shape",
                            "area": area,
                            "aspect_ratio": aspect_ratio,
                            "solidity": solidity
                        },
                        timestamp=time.time()
                    )
                    results.append(result)
                
                # 检测高台特征（矩形、边缘明显）
                elif 1.5 < aspect_ratio < 4.0 and solidity > 0.6 and h > 100:
                    # 可能是高台
                    result = HazardResult(
                        type=HazardType.HIGH_PLATFORM,
                        severity=SeverityLevel.MEDIUM,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2),
                        confidence=0.65,
                        features={
                            "detection_method": "shape",
                            "area": area,
                            "height": h,
                            "aspect_ratio": aspect_ratio
                        },
                        timestamp=time.time()
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"形状检测失败: {e}")
        
        return results
    
    def _detect_by_texture(self, image: np.ndarray) -> List[HazardResult]:
        """
        基于纹理分析检测（工地、路面）
        
        Args:
            image: 输入图像
            
        Returns:
            List[HazardResult]: 纹理检测结果
        """
        results = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 计算纹理特征（方差）
            kernel_size = 5
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
            mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
            variance = cv2.filter2D((gray.astype(np.float32) - mean) ** 2, -1, kernel)
            
            # 工地区域通常纹理复杂（方差大）
            _, construction_mask = cv2.threshold(variance, 100, 255, cv2.THRESH_BINARY)
            construction_mask = construction_mask.astype(np.uint8)
            
            contours, _ = cv2.findContours(construction_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 10000:
                    continue
                
                x, y, w, h = cv2.boundingRect(contour)
                
                result = HazardResult(
                    type=HazardType.CONSTRUCTION,
                    severity=SeverityLevel.MEDIUM,
                    bbox=(x, y, w, h),
                    center=(x + w // 2, y + h // 2),
                    confidence=0.6,
                    features={
                        "detection_method": "texture",
                        "area": area,
                        "texture_variance": float(np.mean(variance[y:y+h, x:x+w]))
                    },
                    timestamp=time.time()
                )
                results.append(result)
            
            # 车行道检测（平整路面，纹理方差小）
            _, roadway_mask = cv2.threshold(variance, 30, 255, cv2.THRESH_BINARY_INV)
            roadway_mask = roadway_mask.astype(np.uint8)
            
            contours, _ = cv2.findContours(roadway_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 15000:
                    continue
                
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # 车行道通常较宽
                if aspect_ratio > 2.0:
                    result = HazardResult(
                        type=HazardType.ROADWAY,
                        severity=SeverityLevel.HIGH,
                        bbox=(x, y, w, h),
                        center=(x + w // 2, y + h // 2),
                        confidence=0.7,
                        features={
                            "detection_method": "texture",
                            "area": area,
                            "aspect_ratio": aspect_ratio
                        },
                        timestamp=time.time()
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"纹理检测失败: {e}")
        
        return results
    
    def _assess_severity(self, results: List[HazardResult], img_shape: Tuple[int, int]) -> List[HazardResult]:
        """
        评估危险的严重程度
        
        Args:
            results: 检测结果列表
            img_shape: 图像尺寸
            
        Returns:
            List[HazardResult]: 已评估严重程度的结果
        """
        img_area = img_shape[0] * img_shape[1]
        
        for result in results:
            hazard_type = result.type
            
            if hazard_type not in self.severity_thresholds:
                result.severity = SeverityLevel.MEDIUM
                continue
            
            thresholds = self.severity_thresholds[hazard_type]
            area = result.bbox[2] * result.bbox[3]
            area_ratio = area / img_area if img_area > 0 else 0
            
            # 根据面积比例评估严重程度
            if area_ratio > 0.3:
                result.severity = SeverityLevel.CRITICAL
            elif area_ratio > 0.15:
                result.severity = SeverityLevel.HIGH
            elif area_ratio > 0.05:
                result.severity = SeverityLevel.MEDIUM
            else:
                result.severity = SeverityLevel.LOW
            
            # 特殊规则
            if hazard_type == HazardType.WATER and area_ratio > 0.2:
                result.severity = SeverityLevel.CRITICAL
            
            if hazard_type == HazardType.ROADWAY:
                # 车行道通常风险较高
                if result.severity == SeverityLevel.LOW:
                    result.severity = SeverityLevel.MEDIUM
        
        return results
    
    def _filter_and_sort(self, results: List[HazardResult]) -> List[HazardResult]:
        """过滤和排序结果"""
        if not results:
            return []
        
        # 按置信度排序
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        # 去重（保留置信度最高的）
        filtered = []
        used_areas = set()
        
        for result in results:
            # 使用中心点作为唯一标识
            center_key = result.center
            
            # 检查是否已存在相似结果
            is_duplicate = False
            for used_center in used_areas:
                if abs(center_key[0] - used_center[0]) < 50 and \
                   abs(center_key[1] - used_center[1]) < 50:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered.append(result)
                used_areas.add(center_key)
        
        return filtered
    
    def get_detection_summary(self, results: List[HazardResult]) -> Dict[str, Any]:
        """
        获取检测结果摘要
        
        Args:
            results: 检测结果列表
            
        Returns:
            Dict[str, Any]: 摘要信息
        """
        summary = {
            "total": len(results),
            "by_type": {},
            "by_severity": {},
            "critical_count": 0
        }
        
        for result in results:
            # 按类型统计
            type_name = result.type.value
            if type_name not in summary["by_type"]:
                summary["by_type"][type_name] = 0
            summary["by_type"][type_name] += 1
            
            # 按严重程度统计
            severity_name = result.severity.value
            if severity_name not in summary["by_severity"]:
                summary["by_severity"][severity_name] = 0
            summary["by_severity"][severity_name] += 1
            
            # 统计高风险
            if result.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
                summary["critical_count"] += 1
        
        return summary
    
    def export_to_map(self, results: List[HazardResult]) -> List[Dict[str, Any]]:
        """
        导出危险区域供地图模块标注
        
        Args:
            results: 检测结果列表
            
        Returns:
            List[Dict[str, Any]]: 地图标注数据
        """
        map_annotations = []
        
        for result in results:
            annotation = {
                "type": result.type.value,
                "severity": result.severity.value,
                "position": result.center,
                "bbox": result.bbox,
                "confidence": result.confidence,
                "timestamp": result.timestamp
            }
            map_annotations.append(annotation)
        
        return map_annotations


# 全局检测器实例
global_hazard_detector = HazardDetector()

def detect_hazards(image: np.ndarray) -> List[HazardResult]:
    """检测危险环境的便捷函数"""
    return global_hazard_detector.detect_hazards(image)


if __name__ == "__main__":
    # 测试危险环境检测
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建测试图像 - 模拟多种危险
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    test_image.fill(200)  # 浅灰色背景
    
    # 绘制蓝色水域
    cv2.rectangle(test_image, (50, 50), (200, 200), (255, 150, 0), -1)
    
    # 绘制橙色工地区域
    cv2.rectangle(test_image, (250, 100), (450, 300), (0, 150, 255), -1)
    
    # 绘制灰色路面
    cv2.rectangle(test_image, (50, 350), (600, 430), (100, 100, 100), -1)
    
    # 进行检测
    detector = HazardDetector()
    results = detector.detect_hazards(test_image)
    
    print(f"检测结果: {len(results)} 个危险区域")
    for i, result in enumerate(results):
        print(f"\n危险区域 {i+1}:")
        print(f"  类型: {result.type.value}")
        print(f"  严重程度: {result.severity.value}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  位置: {result.bbox}")
        print(f"  中心: {result.center}")
        print(f"  特征: {result.features}")
    
    # 获取摘要
    summary = detector.get_detection_summary(results)
    print(f"\n检测摘要: {summary}")
    
    # 导出地图标注
    map_data = detector.export_to_map(results)
    print(f"\n地图标注数据: {len(map_data)} 个标注")
