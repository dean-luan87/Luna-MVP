"""
红绿灯通行增强模块
识别红绿灯状态和倒计时，提供实时播报
"""

import logging
import cv2
import numpy as np
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class TrafficLightState(Enum):
    """红绿灯状态"""
    RED = "red"           # 红灯
    GREEN = "green"       # 绿灯
    YELLOW = "yellow"     # 黄灯
    UNKNOWN = "unknown"   # 未知


@dataclass
class TrafficLightInfo:
    """红绿灯信息"""
    state: TrafficLightState
    countdown: Optional[int] = None  # 倒计时秒数
    confidence: float = 0.0
    bbox: Optional[Tuple[int, int, int, int]] = None  # (x, y, w, h)
    timestamp: float = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "state": self.state.value,
            "countdown": self.countdown,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "timestamp": self.timestamp
        }
    
    def get_broadcast_message(self) -> Optional[str]:
        """获取播报消息"""
        if self.state == TrafficLightState.RED and self.countdown:
            return f"红灯剩余{self.countdown}秒"
        elif self.state == TrafficLightState.GREEN and self.countdown:
            return f"绿灯亮起，请快速通过，剩余时间{self.countdown}秒。"
        elif self.state == TrafficLightState.RED:
            return "当前为红灯，请等待。"
        elif self.state == TrafficLightState.GREEN:
            return "当前为绿灯，请通过。"
        return None


class TrafficLightDetector:
    """红绿灯检测器"""
    
    def __init__(self):
        """初始化红绿灯检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 颜色阈值（HSV）
        self.red_lower1 = np.array([0, 50, 50])
        self.red_upper1 = np.array([10, 255, 255])
        self.red_lower2 = np.array([170, 50, 50])
        self.red_upper2 = np.array([180, 255, 255])
        
        self.green_lower = np.array([40, 50, 50])
        self.green_upper = np.array([80, 255, 255])
        
        self.yellow_lower = np.array([15, 50, 50])
        self.yellow_upper = np.array([35, 255, 255])
        
        # 检测历史（用于过滤抖动）
        self.detection_history = []
        self.history_size = 5
        
        self.logger.info("🚦 红绿灯检测器初始化完成")
    
    def detect_traffic_light(self, image: np.ndarray) -> Optional[TrafficLightInfo]:
        """
        检测红绿灯
        
        Args:
            image: 输入图像（BGR格式）
        
        Returns:
            Optional[TrafficLightInfo]: 红绿灯信息
        """
        try:
            # 转换到HSV色彩空间
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 检测红色、绿色、黄色
            red_mask1 = cv2.inRange(hsv, self.red_lower1, self.red_upper1)
            red_mask2 = cv2.inRange(hsv, self.red_lower2, self.red_upper2)
            red_mask = cv2.bitwise_or(red_mask1, red_mask2)
            
            green_mask = cv2.inRange(hsv, self.green_lower, self.green_upper)
            yellow_mask = cv2.inRange(hsv, self.yellow_lower, self.yellow_upper)
            
            # 计算各颜色的面积
            red_area = np.sum(red_mask > 0)
            green_area = np.sum(green_mask > 0)
            yellow_area = np.sum(yellow_mask > 0)
            
            # 判断状态
            max_area = max(red_area, green_area, yellow_area)
            
            if max_area < 100:  # 阈值，太小则忽略
                return None
            
            state = TrafficLightState.UNKNOWN
            confidence = 0.0
            bbox = None
            
            if red_area == max_area:
                state = TrafficLightState.RED
                confidence = red_area / (image.shape[0] * image.shape[1])
                # 查找红色区域边界框
                bbox = self._find_bbox(red_mask)
            elif green_area == max_area:
                state = TrafficLightState.GREEN
                confidence = green_area / (image.shape[0] * image.shape[1])
                bbox = self._find_bbox(green_mask)
            elif yellow_area == max_area:
                state = TrafficLightState.YELLOW
                confidence = yellow_area / (image.shape[0] * image.shape[1])
                bbox = self._find_bbox(yellow_mask)
            
            # 识别倒计时（OCR）
            countdown = None
            if bbox and state != TrafficLightState.UNKNOWN:
                countdown = self._detect_countdown(image, bbox, state)
            
            info = TrafficLightInfo(
                state=state,
                countdown=countdown,
                confidence=confidence,
                bbox=bbox,
                timestamp=time.time()
            )
            
            # 添加到历史记录
            self.detection_history.append(info)
            if len(self.detection_history) > self.history_size:
                self.detection_history.pop(0)
            
            # 过滤抖动（使用历史记录中最稳定的状态）
            stable_info = self._get_stable_state()
            
            if stable_info:
                self.logger.debug(f"🚦 检测到红绿灯: {stable_info.state.value}, "
                                f"倒计时={stable_info.countdown}秒, "
                                f"置信度={stable_info.confidence:.2f}")
            
            return stable_info
            
        except Exception as e:
            self.logger.error(f"❌ 红绿灯检测失败: {e}")
            return None
    
    def _find_bbox(self, mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """查找边界框"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # 找到最大的轮廓
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            return (x, y, w, h)
        return None
    
    def _detect_countdown(self, 
                         image: np.ndarray, 
                         bbox: Tuple[int, int, int, int],
                         state: TrafficLightState) -> Optional[int]:
        """
        检测倒计时数字
        
        Args:
            image: 输入图像
            bbox: 红绿灯边界框
            state: 红绿灯状态
        
        Returns:
            Optional[int]: 倒计时秒数
        """
        try:
            x, y, w, h = bbox
            
            # 提取红绿灯区域（扩大一点以包含倒计时）
            roi = image[max(0, y-h//2):min(image.shape[0], y+h*2), 
                       max(0, x-w//2):min(image.shape[1], x+w*2)]
            
            if roi.size == 0:
                return None
            
            # 转为灰度图
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # TODO: 这里应该使用OCR识别数字
            # 目前简化处理：返回None，实际应调用OCR模块
            # countdown = ocr_module.read_countdown(gray)
            
            return None  # 暂时返回None，后续可集成OCR
            
        except Exception as e:
            self.logger.debug(f"倒计时识别失败: {e}")
            return None
    
    def _get_stable_state(self) -> Optional[TrafficLightInfo]:
        """从历史记录中获取最稳定的状态"""
        if not self.detection_history:
            return None
        
        # 统计最近几次检测中最常见的状态
        recent = self.detection_history[-self.history_size:]
        
        state_counts = {}
        for info in recent:
            state = info.state.value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # 找到最常见的状态
        if state_counts:
            most_common_state = max(state_counts, key=state_counts.get)
            
            # 返回最后一次检测到该状态的信息
            for info in reversed(recent):
                if info.state.value == most_common_state:
                    return info
        
        return self.detection_history[-1] if self.detection_history else None


# 全局红绿灯检测器实例
_global_traffic_light_detector: Optional[TrafficLightDetector] = None


def get_traffic_light_detector() -> TrafficLightDetector:
    """获取全局红绿灯检测器实例"""
    global _global_traffic_light_detector
    if _global_traffic_light_detector is None:
        _global_traffic_light_detector = TrafficLightDetector()
    return _global_traffic_light_detector


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🚦 红绿灯检测器测试")
    print("=" * 70)
    
    detector = TrafficLightDetector()
    
    # 创建测试图像（模拟红绿灯）
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 绘制红色圆形（模拟红灯）
    cv2.circle(test_image, (320, 200), 30, (0, 0, 255), -1)
    
    # 测试检测
    result = detector.detect_traffic_light(test_image)
    if result:
        print(f"\n检测结果:")
        print(f"  状态: {result.state.value}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  倒计时: {result.countdown}秒")
        print(f"  播报消息: {result.get_broadcast_message()}")
    
    print("\n" + "=" * 70)
