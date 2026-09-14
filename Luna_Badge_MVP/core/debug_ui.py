#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试界面管理器
提供可视化的调试信息显示功能
"""

import cv2
import numpy as np
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from .debug_logger import DebugLogger, EventType

class DebugUI:
    """调试界面管理器"""
    
    def __init__(self, debug_logger: DebugLogger):
        """
        初始化调试界面管理器
        
        Args:
            debug_logger: 调试日志管理器
        """
        self.debug_logger = debug_logger
        self.window_name = "Luna Badge MVP - Debug Mode"
        self.debug_info = {}
        self.show_debug = False
        self.debug_font = cv2.FONT_HERSHEY_SIMPLEX
        self.debug_font_scale = 0.6
        self.debug_font_thickness = 1
        self.debug_line_height = 25
        self.debug_margin = 10
        
        # 调试颜色配置
        self.colors = {
            'background': (0, 0, 0),
            'text': (255, 255, 255),
            'success': (0, 255, 0),
            'warning': (0, 255, 255),
            'error': (0, 0, 255),
            'info': (255, 255, 0),
            'debug': (255, 0, 255)
        }
        
        self.debug_logger.log_debug("DebugUI初始化完成")
    
    def set_debug_mode(self, enabled: bool):
        """
        设置调试模式
        
        Args:
            enabled: 是否启用调试模式
        """
        self.show_debug = enabled
        self.debug_logger.log_debug(f"调试界面模式已{'启用' if enabled else '禁用'}")
    
    def update_debug_info(self, info: Dict[str, Any]):
        """
        更新调试信息
        
        Args:
            info: 调试信息字典
        """
        self.debug_info.update(info)
        self.debug_logger.log_debug("调试信息已更新", info)
    
    def draw_debug_overlay(self, frame: np.ndarray, 
                          detections: List[Dict[str, Any]] = None,
                          tracks: List[Dict[str, Any]] = None,
                          prediction: Dict[str, Any] = None) -> np.ndarray:
        """
        在图像上绘制调试信息覆盖层
        
        Args:
            frame: 输入图像帧
            detections: 检测结果列表
            tracks: 跟踪结果列表
            prediction: 预测结果
            
        Returns:
            np.ndarray: 带有调试信息的图像帧
        """
        try:
            if not self.show_debug:
                return frame
            
            # 创建调试信息覆盖层
            debug_frame = frame.copy()
            
            # 绘制检测结果
            if detections:
                self._draw_detections(debug_frame, detections)
            
            # 绘制跟踪结果
            if tracks:
                self._draw_tracks(debug_frame, tracks)
            
            # 绘制预测结果
            if prediction:
                self._draw_prediction(debug_frame, prediction)
            
            # 绘制系统信息
            self._draw_system_info(debug_frame)
            
            # 绘制事件历史
            self._draw_event_history(debug_frame)
            
            return debug_frame
            
        except Exception as e:
            self.debug_logger.log_error(f"调试覆盖层绘制失败: {e}")
            return frame
    
    def _draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]):
        """
        绘制检测结果
        
        Args:
            frame: 图像帧
            detections: 检测结果列表
        """
        try:
            for i, detection in enumerate(detections):
                bbox = detection.get('bbox', [0, 0, 0, 0])
                confidence = detection.get('confidence', 0.0)
                class_name = detection.get('class_name', 'unknown')
                
                # 绘制边界框
                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), self.colors['success'], 2)
                
                # 绘制标签
                label = f"{class_name}: {confidence:.2f}"
                label_size = cv2.getTextSize(label, self.debug_font, self.debug_font_scale, self.debug_font_thickness)[0]
                cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), self.colors['success'], -1)
                cv2.putText(frame, label, (x1, y1 - 5), self.debug_font, self.debug_font_scale, self.colors['text'], self.debug_font_thickness)
                
        except Exception as e:
            self.debug_logger.log_error(f"检测结果绘制失败: {e}")
    
    def _draw_tracks(self, frame: np.ndarray, tracks: List[Dict[str, Any]]):
        """
        绘制跟踪结果
        
        Args:
            frame: 图像帧
            tracks: 跟踪结果列表
        """
        try:
            for track in tracks:
                track_id = track.get('track_id', 0)
                bbox = track.get('bbox', [0, 0, 0, 0])
                
                # 绘制跟踪ID
                x1, y1, x2, y2 = bbox
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                cv2.circle(frame, (center_x, center_y), 5, self.colors['info'], -1)
                cv2.putText(frame, f"ID:{track_id}", (center_x + 10, center_y), 
                           self.debug_font, self.debug_font_scale, self.colors['info'], self.debug_font_thickness)
                
        except Exception as e:
            self.debug_logger.log_error(f"跟踪结果绘制失败: {e}")
    
    def _draw_prediction(self, frame: np.ndarray, prediction: Dict[str, Any]):
        """
        绘制预测结果
        
        Args:
            frame: 图像帧
            prediction: 预测结果
        """
        try:
            obstructed = prediction.get('obstructed', False)
            path_width = prediction.get('path_width', 0)
            
            # 绘制路径状态
            status_text = "路径阻塞" if obstructed else "路径畅通"
            status_color = self.colors['error'] if obstructed else self.colors['success']
            
            cv2.putText(frame, f"路径状态: {status_text}", 
                       (self.debug_margin, 30), self.debug_font, self.debug_font_scale, status_color, self.debug_font_thickness)
            cv2.putText(frame, f"路径宽度: {path_width:.1f}", 
                       (self.debug_margin, 60), self.debug_font, self.debug_font_scale, self.colors['info'], self.debug_font_thickness)
                
        except Exception as e:
            self.debug_logger.log_error(f"预测结果绘制失败: {e}")
    
    def _draw_system_info(self, frame: np.ndarray):
        """
        绘制系统信息
        
        Args:
            frame: 图像帧
        """
        try:
            y_offset = 90
            
            # 绘制系统信息
            for key, value in self.debug_info.items():
                if isinstance(value, (int, float)):
                    text = f"{key}: {value:.2f}"
                else:
                    text = f"{key}: {value}"
                
                cv2.putText(frame, text, (self.debug_margin, y_offset), 
                           self.debug_font, self.debug_font_scale, self.colors['text'], self.debug_font_thickness)
                y_offset += self.debug_line_height
                
        except Exception as e:
            self.debug_logger.log_error(f"系统信息绘制失败: {e}")
    
    def _draw_event_history(self, frame: np.ndarray):
        """
        绘制事件历史
        
        Args:
            frame: 图像帧
        """
        try:
            # 获取最近的事件历史
            recent_events = self.debug_logger.get_event_history(limit=5)
            
            if recent_events:
                y_offset = frame.shape[0] - 150
                
                cv2.putText(frame, "最近事件:", (self.debug_margin, y_offset), 
                           self.debug_font, self.debug_font_scale, self.colors['debug'], self.debug_font_thickness)
                y_offset += self.debug_line_height
                
                for event in recent_events[-3:]:  # 只显示最近3个事件
                    event_text = f"[{event['event_type']}] {event['message'][:30]}..."
                    cv2.putText(frame, event_text, (self.debug_margin, y_offset), 
                               self.debug_font, self.debug_font_scale * 0.8, self.colors['text'], self.debug_font_thickness)
                    y_offset += self.debug_line_height - 5
                
        except Exception as e:
            self.debug_logger.log_error(f"事件历史绘制失败: {e}")
    
    def show_debug_window(self, frame: np.ndarray):
        """
        显示调试窗口
        
        Args:
            frame: 图像帧
        """
        try:
            if self.show_debug:
                cv2.imshow(self.window_name, frame)
                
                # 处理键盘输入
                key = cv2.waitKey(1) & 0xFF
                if key == ord('d'):
                    self.set_debug_mode(not self.show_debug)
                    self.debug_logger.log_debug(f"调试模式切换: {self.show_debug}")
                elif key == ord('l'):
                    self._export_debug_logs()
                elif key == ord('c'):
                    self._clear_debug_info()
                    
        except Exception as e:
            self.debug_logger.log_error(f"调试窗口显示失败: {e}")
    
    def _export_debug_logs(self):
        """导出调试日志"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"logs/debug_export_{timestamp}.json"
            self.debug_logger.export_logs(log_file)
            self.debug_logger.log_debug(f"调试日志已导出: {log_file}")
            
        except Exception as e:
            self.debug_logger.log_error(f"调试日志导出失败: {e}")
    
    def _clear_debug_info(self):
        """清除调试信息"""
        try:
            self.debug_info.clear()
            self.debug_logger.clear_history()
            self.debug_logger.log_debug("调试信息已清除")
            
        except Exception as e:
            self.debug_logger.log_error(f"调试信息清除失败: {e}")
    
    def get_debug_stats(self) -> Dict[str, Any]:
        """
        获取调试统计信息
        
        Returns:
            Dict[str, Any]: 调试统计信息
        """
        try:
            stats = {
                "debug_mode": self.show_debug,
                "event_count": len(self.debug_logger.event_history),
                "debug_info_count": len(self.debug_info),
                "recent_events": self.debug_logger.get_event_history(limit=10)
            }
            
            return stats
            
        except Exception as e:
            self.debug_logger.log_error(f"调试统计信息获取失败: {e}")
            return {}

# 使用示例
if __name__ == "__main__":
    from .debug_logger import DebugLogger
    
    # 创建调试日志管理器
    debug_logger = DebugLogger("test", debug_mode=True)
    
    # 创建调试界面管理器
    debug_ui = DebugUI(debug_logger)
    
    # 启用调试模式
    debug_ui.set_debug_mode(True)
    
    # 更新调试信息
    debug_ui.update_debug_info({
        "fps": 30.0,
        "detection_count": 5,
        "track_count": 3
    })
    
    # 创建测试图像
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 绘制调试信息
    debug_frame = debug_ui.draw_debug_overlay(test_frame)
    
    print("✅ 调试界面管理器测试完成")
