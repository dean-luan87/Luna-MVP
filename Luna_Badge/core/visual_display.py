#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 可视化显示模块
用于调试阶段的可视化显示，包括目标人体框选、路径区域显示、判断结果标记等
"""

import cv2
import numpy as np
import threading
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import queue

logger = logging.getLogger(__name__)

class PathStatus(Enum):
    """路径状态枚举"""
    CLEAR = "clear"           # 路径畅通
    BLOCKED = "blocked"       # 路径被阻挡
    WARNING = "warning"       # 路径警告
    UNKNOWN = "unknown"       # 路径状态未知

@dataclass
class DetectionBox:
    """检测框数据类"""
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
    label: str
    color: Tuple[int, int, int] = (0, 255, 0)

@dataclass
class PathRegion:
    """路径区域数据类"""
    x1: int
    y1: int
    x2: int
    y2: int
    status: PathStatus
    color: Tuple[int, int, int] = (0, 255, 0)

@dataclass
class DisplayInfo:
    """显示信息数据类"""
    frame: np.ndarray
    detections: List[DetectionBox]
    path_regions: List[PathRegion]
    path_status: PathStatus
    broadcast_message: str
    performance_info: Dict[str, Any]
    timestamp: float

class VisualDisplayManager:
    """可视化显示管理器"""
    
    def __init__(self, window_name: str = "Luna Badge Debug Display", 
                 enable_display: bool = True, display_fps: int = 30):
        """
        初始化可视化显示管理器
        
        Args:
            window_name: 窗口名称
            enable_display: 是否启用显示
            display_fps: 显示帧率
        """
        self.window_name = window_name
        self.enable_display = enable_display
        self.display_fps = display_fps
        
        # 显示队列
        self.display_queue = queue.Queue(maxsize=10)
        self.is_running = False
        self.display_thread = None
        
        # 显示状态
        self.current_frame = None
        self.current_detections = []
        self.current_path_regions = []
        self.current_path_status = PathStatus.UNKNOWN
        self.current_broadcast_message = ""
        self.current_performance_info = {}
        
        # 显示配置
        self.display_config = {
            "show_detections": True,
            "show_path_regions": True,
            "show_path_status": True,
            "show_broadcast_message": True,
            "show_performance_info": True,
            "detection_box_thickness": 2,
            "path_region_thickness": 2,
            "text_font": cv2.FONT_HERSHEY_SIMPLEX,
            "text_scale": 0.7,
            "text_thickness": 2
        }
        
        # 颜色配置
        self.colors = {
            "clear": (0, 255, 0),      # 绿色 - 路径畅通
            "blocked": (0, 0, 255),    # 红色 - 路径被阻挡
            "warning": (0, 255, 255),  # 黄色 - 路径警告
            "unknown": (128, 128, 128), # 灰色 - 路径状态未知
            "person": (255, 0, 0),     # 蓝色 - 人体检测
            "vehicle": (255, 165, 0),  # 橙色 - 车辆检测
            "obstacle": (255, 0, 255), # 紫色 - 障碍物检测
            "text": (255, 255, 255),   # 白色 - 文本
            "background": (0, 0, 0)    # 黑色 - 背景
        }
        
        # 启动显示线程
        if self.enable_display:
            self.start()
        
        logger.info("🖥️ 可视化显示管理器初始化完成")
    
    def start(self):
        """启动显示管理器"""
        if not self.is_running and self.enable_display:
            self.is_running = True
            self.display_thread = threading.Thread(target=self._display_worker, daemon=True)
            self.display_thread.start()
            logger.info("✅ 可视化显示管理器启动")
    
    def stop(self):
        """停止显示管理器"""
        if self.is_running:
            self.is_running = False
            if self.display_thread:
                self.display_thread.join(timeout=2.0)
            cv2.destroyAllWindows()
            logger.info("⏹️ 可视化显示管理器停止")
    
    def _display_worker(self):
        """显示工作线程"""
        while self.is_running:
            try:
                # 从队列获取显示信息
                display_info = self.display_queue.get(timeout=1.0)
                
                # 更新当前显示信息
                self.current_frame = display_info.frame
                self.current_detections = display_info.detections
                self.current_path_regions = display_info.path_regions
                self.current_path_status = display_info.path_status
                self.current_broadcast_message = display_info.broadcast_message
                self.current_performance_info = display_info.performance_info
                
                # 绘制显示内容
                display_frame = self._draw_display_content(display_info)
                
                # 显示帧
                cv2.imshow(self.window_name, display_frame)
                
                # 处理键盘输入
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' 或 ESC 键退出
                    self.is_running = False
                    break
                elif key == ord('s'):  # 's' 键保存截图
                    self._save_screenshot(display_frame)
                
                # 标记任务完成
                self.display_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 显示工作线程异常: {e}")
    
    def _draw_display_content(self, display_info: DisplayInfo) -> np.ndarray:
        """绘制显示内容"""
        frame = display_info.frame.copy()
        
        # 绘制检测框
        if self.display_config["show_detections"]:
            frame = self._draw_detections(frame, display_info.detections)
        
        # 绘制路径区域
        if self.display_config["show_path_regions"]:
            frame = self._draw_path_regions(frame, display_info.path_regions)
        
        # 绘制路径状态
        if self.display_config["show_path_status"]:
            frame = self._draw_path_status(frame, display_info.path_status)
        
        # 绘制播报消息
        if self.display_config["show_broadcast_message"]:
            frame = self._draw_broadcast_message(frame, display_info.broadcast_message)
        
        # 绘制性能信息
        if self.display_config["show_performance_info"]:
            frame = self._draw_performance_info(frame, display_info.performance_info)
        
        # 绘制时间戳
        frame = self._draw_timestamp(frame, display_info.timestamp)
        
        return frame
    
    def _draw_detections(self, frame: np.ndarray, detections: List[DetectionBox]) -> np.ndarray:
        """绘制检测框"""
        for detection in detections:
            # 绘制检测框
            cv2.rectangle(frame, (detection.x1, detection.y1), (detection.x2, detection.y2), 
                         detection.color, self.display_config["detection_box_thickness"])
            
            # 绘制标签和置信度
            label_text = f"{detection.label}: {detection.confidence:.2f}"
            label_size = cv2.getTextSize(label_text, self.display_config["text_font"], 
                                       self.display_config["text_scale"], 
                                       self.display_config["text_thickness"])[0]
            
            # 绘制标签背景
            cv2.rectangle(frame, (detection.x1, detection.y1 - label_size[1] - 10), 
                         (detection.x1 + label_size[0], detection.y1), 
                         detection.color, -1)
            
            # 绘制标签文本
            cv2.putText(frame, label_text, (detection.x1, detection.y1 - 5), 
                       self.display_config["text_font"], self.display_config["text_scale"], 
                       self.colors["text"], self.display_config["text_thickness"])
        
        return frame
    
    def _draw_path_regions(self, frame: np.ndarray, path_regions: List[PathRegion]) -> np.ndarray:
        """绘制路径区域"""
        for region in path_regions:
            # 绘制路径区域框
            cv2.rectangle(frame, (region.x1, region.y1), (region.x2, region.y2), 
                         region.color, self.display_config["path_region_thickness"])
            
            # 绘制路径区域标签
            region_text = f"Path Region: {region.status.value}"
            cv2.putText(frame, region_text, (region.x1, region.y1 - 10), 
                       self.display_config["text_font"], self.display_config["text_scale"], 
                       region.color, self.display_config["text_thickness"])
        
        return frame
    
    def _draw_path_status(self, frame: np.ndarray, path_status: PathStatus) -> np.ndarray:
        """绘制路径状态"""
        status_text = f"Path Status: {path_status.value.upper()}"
        status_color = self.colors[path_status.value]
        
        # 绘制状态文本背景
        text_size = cv2.getTextSize(status_text, self.display_config["text_font"], 
                                   self.display_config["text_scale"] * 1.2, 
                                   self.display_config["text_thickness"] * 2)[0]
        
        cv2.rectangle(frame, (10, 10), (10 + text_size[0] + 20, 10 + text_size[1] + 20), 
                     self.colors["background"], -1)
        
        # 绘制状态文本
        cv2.putText(frame, status_text, (20, 30), 
                   self.display_config["text_font"], self.display_config["text_scale"] * 1.2, 
                   status_color, self.display_config["text_thickness"] * 2)
        
        return frame
    
    def _draw_broadcast_message(self, frame: np.ndarray, message: str) -> np.ndarray:
        """绘制播报消息"""
        if not message:
            return frame
        
        # 限制消息长度
        if len(message) > 50:
            message = message[:47] + "..."
        
        # 绘制消息背景
        text_size = cv2.getTextSize(message, self.display_config["text_font"], 
                                   self.display_config["text_scale"], 
                                   self.display_config["text_thickness"])[0]
        
        cv2.rectangle(frame, (10, frame.shape[0] - 60), 
                     (10 + text_size[0] + 20, frame.shape[0] - 10), 
                     self.colors["background"], -1)
        
        # 绘制消息文本
        cv2.putText(frame, message, (20, frame.shape[0] - 30), 
                   self.display_config["text_font"], self.display_config["text_scale"], 
                   self.colors["text"], self.display_config["text_thickness"])
        
        return frame
    
    def _draw_performance_info(self, frame: np.ndarray, performance_info: Dict[str, Any]) -> np.ndarray:
        """绘制性能信息"""
        if not performance_info:
            return frame
        
        y_offset = 60
        for key, value in performance_info.items():
            info_text = f"{key}: {value}"
            cv2.putText(frame, info_text, (10, y_offset), 
                       self.display_config["text_font"], self.display_config["text_scale"], 
                       self.colors["text"], self.display_config["text_thickness"])
            y_offset += 25
        
        return frame
    
    def _draw_timestamp(self, frame: np.ndarray, timestamp: float) -> np.ndarray:
        """绘制时间戳"""
        timestamp_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
        cv2.putText(frame, timestamp_str, (frame.shape[1] - 100, 30), 
                   self.display_config["text_font"], self.display_config["text_scale"], 
                   self.colors["text"], self.display_config["text_thickness"])
        
        return frame
    
    def _save_screenshot(self, frame: np.ndarray):
        """保存截图"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            logger.info(f"📸 截图已保存: {filename}")
        except Exception as e:
            logger.error(f"❌ 保存截图失败: {e}")
    
    def update_display(self, frame: np.ndarray, detections: List[DetectionBox] = None,
                      path_regions: List[PathRegion] = None, path_status: PathStatus = PathStatus.UNKNOWN,
                      broadcast_message: str = "", performance_info: Dict[str, Any] = None):
        """
        更新显示内容
        
        Args:
            frame: 视频帧
            detections: 检测结果列表
            path_regions: 路径区域列表
            path_status: 路径状态
            broadcast_message: 播报消息
            performance_info: 性能信息
        """
        if not self.enable_display or not self.is_running:
            return
        
        if detections is None:
            detections = []
        if path_regions is None:
            path_regions = []
        if performance_info is None:
            performance_info = {}
        
        # 创建显示信息
        display_info = DisplayInfo(
            frame=frame,
            detections=detections,
            path_regions=path_regions,
            path_status=path_status,
            broadcast_message=broadcast_message,
            performance_info=performance_info,
            timestamp=time.time()
        )
        
        # 添加到显示队列
        try:
            self.display_queue.put(display_info, timeout=0.1)
        except queue.Full:
            # 队列已满，丢弃旧帧
            try:
                self.display_queue.get_nowait()
                self.display_queue.put(display_info, timeout=0.1)
            except queue.Empty:
                pass
    
    def set_display_config(self, config: Dict[str, Any]):
        """设置显示配置"""
        self.display_config.update(config)
        logger.info(f"✅ 显示配置更新: {config}")
    
    def get_display_config(self) -> Dict[str, Any]:
        """获取显示配置"""
        return self.display_config.copy()
    
    def create_detection_box(self, x1: int, y1: int, x2: int, y2: int, 
                           confidence: float, label: str) -> DetectionBox:
        """创建检测框"""
        # 根据标签选择颜色
        if label.lower() in ["person", "人", "人体"]:
            color = self.colors["person"]
        elif label.lower() in ["car", "vehicle", "车", "车辆"]:
            color = self.colors["vehicle"]
        else:
            color = self.colors["obstacle"]
        
        return DetectionBox(x1, y1, x2, y2, confidence, label, color)
    
    def create_path_region(self, x1: int, y1: int, x2: int, y2: int, 
                          status: PathStatus) -> PathRegion:
        """创建路径区域"""
        color = self.colors[status.value]
        return PathRegion(x1, y1, x2, y2, status, color)
    
    def create_path_status(self, status: str) -> PathStatus:
        """创建路径状态"""
        status_mapping = {
            "clear": PathStatus.CLEAR,
            "blocked": PathStatus.BLOCKED,
            "warning": PathStatus.WARNING,
            "unknown": PathStatus.UNKNOWN
        }
        return status_mapping.get(status.lower(), PathStatus.UNKNOWN)


# 全局可视化显示管理器实例
global_visual_display = VisualDisplayManager()

# 便捷函数
def update_display(frame: np.ndarray, detections: List[DetectionBox] = None,
                  path_regions: List[PathRegion] = None, path_status: PathStatus = PathStatus.UNKNOWN,
                  broadcast_message: str = "", performance_info: Dict[str, Any] = None):
    """更新显示内容的便捷函数"""
    global_visual_display.update_display(frame, detections, path_regions, 
                                       path_status, broadcast_message, performance_info)

def create_detection_box(x1: int, y1: int, x2: int, y2: int, 
                        confidence: float, label: str) -> DetectionBox:
    """创建检测框的便捷函数"""
    return global_visual_display.create_detection_box(x1, y1, x2, y2, confidence, label)

def create_path_region(x1: int, y1: int, x2: int, y2: int, 
                      status: PathStatus) -> PathRegion:
    """创建路径区域的便捷函数"""
    return global_visual_display.create_path_region(x1, y1, x2, y2, status)

def create_path_status(status: str) -> PathStatus:
    """创建路径状态的便捷函数"""
    return global_visual_display.create_path_status(status)


if __name__ == "__main__":
    # 测试可视化显示管理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    def test_visual_display():
        """测试可视化显示管理器"""
        display_manager = VisualDisplayManager()
        
        # 创建测试帧
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 创建测试检测框
        detections = [
            display_manager.create_detection_box(100, 100, 200, 300, 0.95, "person"),
            display_manager.create_detection_box(300, 150, 400, 250, 0.87, "car")
        ]
        
        # 创建测试路径区域
        path_regions = [
            display_manager.create_path_region(50, 400, 590, 470, PathStatus.CLEAR),
            display_manager.create_path_region(100, 200, 200, 400, PathStatus.BLOCKED)
        ]
        
        # 创建测试性能信息
        performance_info = {
            "FPS": 30,
            "Detection Time": "0.05s",
            "Memory Usage": "256MB"
        }
        
        # 更新显示
        display_manager.update_display(
            frame=frame,
            detections=detections,
            path_regions=path_regions,
            path_status=PathStatus.WARNING,
            broadcast_message="前方检测到行人，请注意安全",
            performance_info=performance_info
        )
        
        # 等待显示
        time.sleep(5)
        
        # 停止显示管理器
        display_manager.stop()
    
    # 运行测试
    test_visual_display()
