#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 门牌视觉识别模块
识别房门/房号/楼层门牌等文字信息
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import time

logger = logging.getLogger(__name__)

class DoorplateType(Enum):
    """门牌类型"""
    ROOM = "room"              # 房间号
    FLOOR = "floor"            # 楼层
    BUILDING = "building"     # 楼栋
    AREA = "area"              # 区域
    UNKNOWN = "unknown"       # 未知

@dataclass
class DoorplateInfo:
    """门牌信息"""
    text: str                  # 门牌文字
    type: DoorplateType       # 门牌类型
    bbox: Tuple[int, int, int, int]  # 边界框
    confidence: float          # 置信度
    direction: Optional[str]   # 方向（东/西/南/北）
    number: Optional[int]      # 数字编号
    timestamp: float           # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "text": self.text,
            "type": self.type.value,
            "bbox": self.bbox,
            "confidence": self.confidence,
            "direction": self.direction,
            "number": self.number,
            "timestamp": self.timestamp
        }

class DoorplateReader:
    """门牌识别器"""
    
    def __init__(self):
        """初始化门牌识别器"""
        self.logger = logging.getLogger(__name__)
        
        # 门牌识别模式
        self.patterns = {
            DoorplateType.ROOM: [
                r'^(\d+)室$',                    # 501室
                r'^(\d+)$',                      # 501
                r'^第?(\d+)号$',                  # 第501号
                r'^R(\d+)$',                     # R501
            ],
            DoorplateType.FLOOR: [
                r'^(\d+)层$',                    # 5层
                r'^(\d+)F$',                     # 5F
                r'^(\d+)楼$',                    # 5楼
            ],
            DoorplateType.BUILDING: [
                r'^(\d+)栋$',                    # 8栋
                r'^(\d+)号楼$',                  # 8号楼
                r'^(\d+)幢$',                    # 8幢
            ],
            DoorplateType.AREA: [
                r'^东区(\d+)栋$',                # 东区8栋
                r'^西区(\d+)栋$',                # 西区8栋
                r'^南区(\d+)栋$',                # 南区8栋
                r'^北区(\d+)栋$',                # 北区8栋
            ]
        }
        
        # 方向关键词
        self.direction_keywords = {
            "东": "east",
            "西": "west",
            "南": "south",
            "北": "north"
        }
        
        self.logger.info("🚪 门牌识别器初始化完成")
    
    def detect_doorplates(self, image: np.ndarray) -> List[DoorplateInfo]:
        """
        检测图像中的门牌
        
        Args:
            image: 输入图像
            
        Returns:
            List[DoorplateInfo]: 门牌信息列表
        """
        # 模拟OCR识别（实际应使用Tesseract或PaddleOCR）
        detected_texts = self._simulate_doorplate_ocr(image)
        
        results = []
        
        for text, bbox in detected_texts:
            # 解析门牌信息
            info = self._parse_doorplate(text, bbox)
            if info:
                results.append(info)
        
        self.logger.info(f"🚪 检测到 {len(results)} 个门牌")
        
        return results
    
    def detect_doorplates_enhanced(self, image: np.ndarray) -> Dict[str, Any]:
        """
        增强版门牌检测，输出结构化信息
        
        Args:
            image: 输入图像
            
        Returns:
            Dict[str, Any]: 结构化门牌信息
        """
        doorplates = self.detect_doorplates(image)
        
        if not doorplates:
            return {
                "event": "doorplate_detected",
                "room_number": None,
                "area": None,
                "floor": None,
                "bbox": None,
                "confidence": 0.0,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        
        # 选择置信度最高的门牌
        best_doorplate = doorplates[0]
        
        # 提取结构化信息
        room_number = None
        area = None
        floor = None
        
        if best_doorplate.type == DoorplateType.ROOM:
            room_number = str(best_doorplate.number) if best_doorplate.number else None
        elif best_doorplate.type == DoorplateType.FLOOR:
            floor = str(best_doorplate.number) if best_doorplate.number else None
        elif best_doorplate.type == DoorplateType.AREA:
            area = best_doorplate.direction
        
        # 检查异常（楼层跨越）
        anomaly_detected = self._check_floor_anomaly(doorplates)
        
        result = {
            "event": "doorplate_detected",
            "room_number": room_number,
            "area": area,
            "floor": floor,
            "bbox": list(best_doorplate.bbox),
            "confidence": best_doorplate.confidence,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "anomaly_detected": anomaly_detected,
            "raw_text": best_doorplate.text
        }
        
        return result
    
    def _check_floor_anomaly(self, doorplates: List[DoorplateInfo]) -> bool:
        """检查楼层跨越异常"""
        floor_numbers = []
        
        for doorplate in doorplates:
            if doorplate.type == DoorplateType.FLOOR and doorplate.number:
                floor_numbers.append(doorplate.number)
        
        if len(floor_numbers) >= 2:
            # 检查是否有楼层跳跃（如5楼跳到8楼）
            floor_numbers.sort()
            for i in range(1, len(floor_numbers)):
                if floor_numbers[i] - floor_numbers[i-1] > 2:
                    return True
        
        return False
    
    def _simulate_doorplate_ocr(self, image: np.ndarray) -> List[Tuple[str, Tuple]]:
        """
        模拟OCR识别门牌（占位符实现）
        
        Args:
            image: 输入图像
            
        Returns:
            List[Tuple[str, Tuple]]: (文字, 边界框) 列表
        """
        # 实际的OCR实现应该使用pytesseract或PaddleOCR
        # 这里返回模拟数据用于测试
        
        # 模拟检测结果
        simulated_results = [
            ("501室", (100, 50, 150, 100)),
            ("5层", (200, 50, 240, 90)),
            ("东区8栋", (300, 50, 380, 100)),
        ]
        
        return simulated_results
    
    def _parse_doorplate(self, text: str, bbox: Tuple) -> Optional[DoorplateInfo]:
        """
        解析门牌信息
        
        Args:
            text: 识别到的文字
            bbox: 边界框
            
        Returns:
            Optional[DoorplateInfo]: 门牌信息
        """
        # 检测方向
        direction = None
        for key, value in self.direction_keywords.items():
            if key in text:
                direction = value
                break
        
        # 检测门牌类型
        doorplate_type = self._detect_type(text)
        
        # 提取数字
        number = self._extract_number(text)
        
        return DoorplateInfo(
            text=text,
            type=doorplate_type,
            bbox=bbox,
            confidence=0.9,  # 模拟置信度
            direction=direction,
            number=number,
            timestamp=time.time()
        )
    
    def _detect_type(self, text: str) -> DoorplateType:
        """检测门牌类型"""
        # 检查房间号
        if any(re.match(pattern, text) for pattern in self.patterns[DoorplateType.ROOM]):
            return DoorplateType.ROOM
        
        # 检查楼层
        if any(re.match(pattern, text) for pattern in self.patterns[DoorplateType.FLOOR]):
            return DoorplateType.FLOOR
        
        # 检查楼栋
        if any(re.match(pattern, text) for pattern in self.patterns[DoorplateType.BUILDING]):
            return DoorplateType.BUILDING
        
        # 检查区域
        if any(re.match(pattern, text) for pattern in self.patterns[DoorplateType.AREA]):
            return DoorplateType.AREA
        
        return DoorplateType.UNKNOWN
    
    def _extract_number(self, text: str) -> Optional[int]:
        """提取数字编号"""
        # 提取第一个数字
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None


# 全局识别器实例
global_doorplate_reader = DoorplateReader()

def detect_doorplates(image: np.ndarray) -> List[DoorplateInfo]:
    """检测门牌的便捷函数"""
    return global_doorplate_reader.detect_doorplates(image)


if __name__ == "__main__":
    # 测试门牌识别
    import logging
    logging.basicConfig(level=logging.INFO)
    
    reader = DoorplateReader()
    
    # 创建测试图像
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # 检测门牌
    results = reader.detect_doorplates(test_image)
    
    print("\n" + "=" * 60)
    print("🚪 门牌识别测试")
    print("=" * 60)
    
    print(f"\n检测到 {len(results)} 个门牌:")
    for i, doorplate in enumerate(results, 1):
        print(f"\n{i}. {doorplate.text}")
        print(f"   类型: {doorplate.type.value}")
        print(f"   方向: {doorplate.direction or '无'}")
        print(f"   编号: {doorplate.number or '无'}")
        print(f"   位置: {doorplate.bbox}")
        print(f"   置信度: {doorplate.confidence:.2f}")
    
    print("\n" + "=" * 60)

