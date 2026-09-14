#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试日志管理器
统一管理所有行为记录和调试功能
"""

import logging
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

class EventType(Enum):
    """事件类型枚举"""
    SYSTEM = "SYSTEM"
    DETECTION = "DETECTION"
    TRACKING = "TRACKING"
    PREDICTION = "PREDICTION"
    SPEECH = "SPEECH"
    STATE = "STATE"
    COOLDOWN = "COOLDOWN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class DebugLogger:
    """调试日志管理器"""
    
    def __init__(self, name: str, debug_mode: bool = False):
        """
        初始化调试日志管理器
        
        Args:
            name: 日志记录器名称
            debug_mode: 是否启用调试模式
        """
        self.name = name
        self.debug_mode = debug_mode
        self.log_file = "logs/debug.log"
        self.logger = None
        self.event_history = []
        self.max_history_size = 1000
        
        # 初始化日志记录器
        self._setup_logger()
        
        # 记录初始化事件
        self.log_event(EventType.SYSTEM, LogLevel.INFO, "DebugLogger初始化完成", {
            "debug_mode": debug_mode,
            "log_file": self.log_file
        })
    
    def _setup_logger(self):
        """设置日志记录器"""
        try:
            # 创建日志记录器
            self.logger = logging.getLogger(f"{self.name}_debug")
            
            # 设置日志级别
            log_level = logging.DEBUG if self.debug_mode else logging.INFO
            self.logger.setLevel(log_level)
            
            # 避免重复添加处理器
            if self.logger.handlers:
                return
            
            # 创建格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # 创建文件处理器
            try:
                # 确保日志目录存在
                log_dir = os.path.dirname(self.log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
                
            except Exception as e:
                self.logger.warning(f"⚠️ 无法创建日志文件处理器: {e}")
            
        except Exception as e:
            print(f"❌ 日志记录器设置失败: {e}")
    
    def log_event(self, event_type: EventType, level: LogLevel, message: str, 
                  data: Optional[Dict[str, Any]] = None, status: Optional[str] = None):
        """
        记录事件日志
        
        Args:
            event_type: 事件类型
            level: 日志级别
            message: 日志消息
            data: 附加数据
            status: 状态信息
        """
        try:
            # 创建事件记录
            event_record = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type.value,
                "level": level.value,
                "message": message,
                "status": status,
                "data": data or {}
            }
            
            # 添加到历史记录
            self.event_history.append(event_record)
            
            # 限制历史记录大小
            if len(self.event_history) > self.max_history_size:
                self.event_history = self.event_history[-self.max_history_size:]
            
            # 记录到日志文件
            log_message = self._format_log_message(event_record)
            
            if self.logger:
                if level == LogLevel.DEBUG:
                    self.logger.debug(log_message)
                elif level == LogLevel.INFO:
                    self.logger.info(log_message)
                elif level == LogLevel.WARNING:
                    self.logger.warning(log_message)
                elif level == LogLevel.ERROR:
                    self.logger.error(log_message)
                elif level == LogLevel.CRITICAL:
                    self.logger.critical(log_message)
            
            # 调试模式下的额外输出
            if self.debug_mode:
                self._debug_output(event_record)
                
        except Exception as e:
            print(f"❌ 事件日志记录失败: {e}")
    
    def _format_log_message(self, event_record: Dict[str, Any]) -> str:
        """
        格式化日志消息
        
        Args:
            event_record: 事件记录
            
        Returns:
            str: 格式化后的日志消息
        """
        try:
            # 基础格式: [事件类型] 消息
            message = f"[{event_record['event_type']}] {event_record['message']}"
            
            # 添加状态信息
            if event_record.get('status'):
                message += f" | 状态: {event_record['status']}"
            
            # 添加数据信息
            if event_record.get('data'):
                data_str = json.dumps(event_record['data'], ensure_ascii=False)
                message += f" | 数据: {data_str}"
            
            return message
            
        except Exception as e:
            return f"日志格式化失败: {e}"
    
    def _debug_output(self, event_record: Dict[str, Any]):
        """
        调试模式下的额外输出
        
        Args:
            event_record: 事件记录
        """
        try:
            if self.debug_mode:
                print(f"🔍 [DEBUG] {event_record['event_type']}: {event_record['message']}")
                if event_record.get('data'):
                    print(f"   数据: {event_record['data']}")
                if event_record.get('status'):
                    print(f"   状态: {event_record['status']}")
                    
        except Exception as e:
            print(f"❌ 调试输出失败: {e}")
    
    def log_detection(self, detections: List[Dict[str, Any]], status: str = "success"):
        """
        记录检测事件
        
        Args:
            detections: 检测结果列表
            status: 状态信息
        """
        self.log_event(
            EventType.DETECTION,
            LogLevel.INFO,
            f"目标检测完成，检测到 {len(detections)} 个目标",
            {"detection_count": len(detections), "detections": detections},
            status
        )
    
    def log_tracking(self, tracks: List[Dict[str, Any]], status: str = "success"):
        """
        记录跟踪事件
        
        Args:
            tracks: 跟踪结果列表
            status: 状态信息
        """
        self.log_event(
            EventType.TRACKING,
            LogLevel.INFO,
            f"目标跟踪完成，跟踪 {len(tracks)} 个目标",
            {"track_count": len(tracks), "tracks": tracks},
            status
        )
    
    def log_prediction(self, prediction: Dict[str, Any], status: str = "success"):
        """
        记录预测事件
        
        Args:
            prediction: 预测结果
            status: 状态信息
        """
        self.log_event(
            EventType.PREDICTION,
            LogLevel.INFO,
            f"路径预测完成，路径状态: {prediction.get('obstructed', 'unknown')}",
            prediction,
            status
        )
    
    def log_speech(self, text: str, priority: int, status: str = "queued"):
        """
        记录语音事件
        
        Args:
            text: 语音文本
            priority: 优先级
            status: 状态信息
        """
        self.log_event(
            EventType.SPEECH,
            LogLevel.INFO,
            f"语音播报: {text}",
            {"text": text, "priority": priority},
            status
        )
    
    def log_state_change(self, key: str, old_value: Any, new_value: Any):
        """
        记录状态变化
        
        Args:
            key: 状态键名
            old_value: 旧值
            new_value: 新值
        """
        self.log_event(
            EventType.STATE,
            LogLevel.INFO,
            f"状态变化: {key}",
            {"key": key, "old_value": old_value, "new_value": new_value},
            "changed"
        )
    
    def log_cooldown(self, event_key: str, can_trigger: bool, remaining_time: float = 0.0):
        """
        记录冷却事件
        
        Args:
            event_key: 事件键名
            can_trigger: 是否可以触发
            remaining_time: 剩余冷却时间
        """
        self.log_event(
            EventType.COOLDOWN,
            LogLevel.DEBUG,
            f"冷却检查: {event_key}",
            {"event_key": event_key, "can_trigger": can_trigger, "remaining_time": remaining_time},
            "checked"
        )
    
    def log_error(self, error_message: str, error_data: Optional[Dict[str, Any]] = None):
        """
        记录错误事件
        
        Args:
            error_message: 错误消息
            error_data: 错误数据
        """
        self.log_event(
            EventType.ERROR,
            LogLevel.ERROR,
            error_message,
            error_data,
            "error"
        )
    
    def log_debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        记录调试事件
        
        Args:
            message: 调试消息
            data: 调试数据
        """
        self.log_event(
            EventType.DEBUG,
            LogLevel.DEBUG,
            message,
            data,
            "debug"
        )
    
    def get_event_history(self, event_type: Optional[EventType] = None, 
                         limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取事件历史记录
        
        Args:
            event_type: 事件类型过滤
            limit: 限制返回数量
            
        Returns:
            List[Dict[str, Any]]: 事件历史记录
        """
        try:
            history = self.event_history.copy()
            
            # 按事件类型过滤
            if event_type:
                history = [event for event in history if event['event_type'] == event_type.value]
            
            # 限制返回数量
            return history[-limit:]
            
        except Exception as e:
            self.log_error(f"获取事件历史记录失败: {e}")
            return []
    
    def export_logs(self, output_file: str, event_type: Optional[EventType] = None):
        """
        导出日志到文件
        
        Args:
            output_file: 输出文件路径
            event_type: 事件类型过滤
        """
        try:
            history = self.get_event_history(event_type)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            self.log_event(
                EventType.SYSTEM,
                LogLevel.INFO,
                f"日志导出完成: {output_file}",
                {"export_count": len(history)},
                "exported"
            )
            
        except Exception as e:
            self.log_error(f"日志导出失败: {e}")
    
    def clear_history(self):
        """清除历史记录"""
        self.event_history.clear()
        self.log_event(
            EventType.SYSTEM,
            LogLevel.INFO,
            "历史记录已清除",
            {},
            "cleared"
        )
    
    def set_debug_mode(self, debug_mode: bool):
        """
        设置调试模式
        
        Args:
            debug_mode: 是否启用调试模式
        """
        self.debug_mode = debug_mode
        self.log_event(
            EventType.SYSTEM,
            LogLevel.INFO,
            f"调试模式已{'启用' if debug_mode else '禁用'}",
            {"debug_mode": debug_mode},
            "changed"
        )

# 全局调试日志管理器实例
_global_debug_logger: Optional[DebugLogger] = None

def get_debug_logger(name: str = "LunaBadgeMVP", debug_mode: bool = False) -> DebugLogger:
    """获取全局调试日志管理器实例"""
    global _global_debug_logger
    if _global_debug_logger is None:
        _global_debug_logger = DebugLogger(name, debug_mode)
    return _global_debug_logger

def set_debug_mode(debug_mode: bool):
    """设置全局调试模式"""
    global _global_debug_logger
    if _global_debug_logger:
        _global_debug_logger.set_debug_mode(debug_mode)

# 使用示例
if __name__ == "__main__":
    # 创建调试日志管理器
    debug_logger = DebugLogger("test", debug_mode=True)
    
    # 测试各种事件记录
    debug_logger.log_detection([
        {"bbox": [100, 100, 200, 200], "confidence": 0.8, "class_name": "person"}
    ])
    
    debug_logger.log_tracking([
        {"track_id": 1, "bbox": [100, 100, 200, 200]}
    ])
    
    debug_logger.log_prediction({"obstructed": False, "path_width": 200})
    
    debug_logger.log_speech("前方路径畅通", priority=1)
    
    debug_logger.log_state_change("test_flag", False, True)
    
    debug_logger.log_cooldown("test_event", True, 0.0)
    
    debug_logger.log_error("测试错误", {"error_code": 1001})
    
    debug_logger.log_debug("调试信息", {"variable": "test_value"})
    
    # 导出日志
    debug_logger.export_logs("test_logs.json")
    
    print("✅ 调试日志管理器测试完成")
