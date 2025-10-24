#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 日志管理器
将关键事件写入 logs/runlog.txt，用于回放与测试追踪
"""

import os
import json
import logging
import threading
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import queue

logger = logging.getLogger(__name__)

class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class EventType(Enum):
    """事件类型枚举"""
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    VOICE_BROADCAST = "voice_broadcast"
    PATH_BLOCKED = "path_blocked"
    PATH_CLEAR = "path_clear"
    CAMERA_START = "camera_start"
    CAMERA_STOP = "camera_stop"
    AI_DETECTION = "ai_detection"
    FAULT_OCCURRED = "fault_occurred"
    FAULT_RESOLVED = "fault_resolved"
    USER_INTERACTION = "user_interaction"
    CONFIG_CHANGE = "config_change"
    PERFORMANCE_METRIC = "performance_metric"

@dataclass
class LogEntry:
    """日志条目数据类"""
    timestamp: float
    level: LogLevel
    event_type: EventType
    module_name: str
    message: str
    data: Dict[str, Any]
    thread_id: str
    process_id: int

class LogManager:
    """日志管理器"""
    
    def __init__(self, log_dir: str = "logs", max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 max_files: int = 5, enable_console_log: bool = True):
        """
        初始化日志管理器
        
        Args:
            log_dir: 日志目录
            max_file_size: 最大文件大小（字节）
            max_files: 最大文件数量
            enable_console_log: 是否启用控制台日志
        """
        self.log_dir = log_dir
        self.max_file_size = max_file_size
        self.max_files = max_files
        self.enable_console_log = enable_console_log
        
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 日志文件路径
        self.log_file = os.path.join(self.log_dir, "runlog.txt")
        self.backup_log_file = os.path.join(self.log_dir, "runlog_backup.txt")
        
        # 日志队列
        self.log_queue = queue.Queue()
        self.is_running = False
        self.log_thread = None
        
        # 日志统计
        self.log_stats = {
            "total_entries": 0,
            "entries_by_level": {},
            "entries_by_event_type": {},
            "entries_by_module": {},
            "last_log_time": None
        }
        
        # 启动日志线程
        self.start()
        
        logger.info("📝 日志管理器初始化完成")
    
    def start(self):
        """启动日志管理器"""
        if not self.is_running:
            self.is_running = True
            self.log_thread = threading.Thread(target=self._log_worker, daemon=True)
            self.log_thread.start()
            logger.info("✅ 日志管理器启动")
    
    def stop(self):
        """停止日志管理器"""
        if self.is_running:
            self.is_running = False
            # 等待日志队列清空
            while not self.log_queue.empty():
                time.sleep(0.1)
            logger.info("⏹️ 日志管理器停止")
    
    def _log_worker(self):
        """日志工作线程"""
        while self.is_running:
            try:
                # 从队列获取日志条目
                log_entry = self.log_queue.get(timeout=1.0)
                
                # 写入日志文件
                self._write_log_entry(log_entry)
                
                # 更新统计信息
                self._update_log_stats(log_entry)
                
                # 标记任务完成
                self.log_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 日志工作线程异常: {e}")
    
    def _write_log_entry(self, log_entry: LogEntry):
        """写入日志条目"""
        try:
            # 格式化日志条目
            log_line = self._format_log_entry(log_entry)
            
            # 检查文件大小
            if os.path.exists(self.log_file):
                file_size = os.path.getsize(self.log_file)
                if file_size > self.max_file_size:
                    self._rotate_log_file()
            
            # 写入日志文件
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
            
            # 同时写入控制台
            if self.enable_console_log:
                self._write_console_log(log_entry)
                
        except Exception as e:
            logger.error(f"❌ 写入日志条目失败: {e}")
    
    def _format_log_entry(self, log_entry: LogEntry) -> str:
        """格式化日志条目"""
        timestamp_str = datetime.fromtimestamp(log_entry.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # 基础格式
        log_line = f"[{timestamp_str}] [{log_entry.level.value}] [{log_entry.event_type.value}] [{log_entry.module_name}] {log_entry.message}"
        
        # 添加数据信息
        if log_entry.data:
            data_str = json.dumps(log_entry.data, ensure_ascii=False)
            log_line += f" | DATA: {data_str}"
        
        # 添加线程和进程信息
        log_line += f" | THREAD: {log_entry.thread_id} | PROCESS: {log_entry.process_id}"
        
        return log_line
    
    def _write_console_log(self, log_entry: LogEntry):
        """写入控制台日志"""
        if log_entry.level == LogLevel.DEBUG:
            logger.debug(f"[{log_entry.event_type.value}] {log_entry.message}")
        elif log_entry.level == LogLevel.INFO:
            logger.info(f"[{log_entry.event_type.value}] {log_entry.message}")
        elif log_entry.level == LogLevel.WARNING:
            logger.warning(f"[{log_entry.event_type.value}] {log_entry.message}")
        elif log_entry.level == LogLevel.ERROR:
            logger.error(f"[{log_entry.event_type.value}] {log_entry.message}")
        elif log_entry.level == LogLevel.CRITICAL:
            logger.critical(f"[{log_entry.event_type.value}] {log_entry.message}")
    
    def _rotate_log_file(self):
        """轮转日志文件"""
        try:
            # 备份当前日志文件
            if os.path.exists(self.log_file):
                os.rename(self.log_file, self.backup_log_file)
            
            # 清理旧日志文件
            self._cleanup_old_logs()
            
            logger.info("🔄 日志文件轮转完成")
        except Exception as e:
            logger.error(f"❌ 日志文件轮转失败: {e}")
    
    def _cleanup_old_logs(self):
        """清理旧日志文件"""
        try:
            log_files = []
            for filename in os.listdir(self.log_dir):
                if filename.startswith("runlog") and filename.endswith(".txt"):
                    filepath = os.path.join(self.log_dir, filename)
                    log_files.append((filepath, os.path.getmtime(filepath)))
            
            # 按修改时间排序
            log_files.sort(key=lambda x: x[1], reverse=True)
            
            # 删除多余的日志文件
            if len(log_files) > self.max_files:
                for filepath, _ in log_files[self.max_files:]:
                    os.remove(filepath)
                    logger.info(f"🗑️ 删除旧日志文件: {filepath}")
                    
        except Exception as e:
            logger.error(f"❌ 清理旧日志文件失败: {e}")
    
    def _update_log_stats(self, log_entry: LogEntry):
        """更新日志统计信息"""
        self.log_stats["total_entries"] += 1
        self.log_stats["last_log_time"] = log_entry.timestamp
        
        # 按级别统计
        level = log_entry.level.value
        if level not in self.log_stats["entries_by_level"]:
            self.log_stats["entries_by_level"][level] = 0
        self.log_stats["entries_by_level"][level] += 1
        
        # 按事件类型统计
        event_type = log_entry.event_type.value
        if event_type not in self.log_stats["entries_by_event_type"]:
            self.log_stats["entries_by_event_type"][event_type] = 0
        self.log_stats["entries_by_event_type"][event_type] += 1
        
        # 按模块统计
        module_name = log_entry.module_name
        if module_name not in self.log_stats["entries_by_module"]:
            self.log_stats["entries_by_module"][module_name] = 0
        self.log_stats["entries_by_module"][module_name] += 1
    
    def log(self, level: LogLevel, event_type: EventType, module_name: str, 
            message: str, data: Dict[str, Any] = None):
        """
        记录日志
        
        Args:
            level: 日志级别
            event_type: 事件类型
            module_name: 模块名称
            message: 消息内容
            data: 附加数据
        """
        if data is None:
            data = {}
        
        # 创建日志条目
        log_entry = LogEntry(
            timestamp=time.time(),
            level=level,
            event_type=event_type,
            module_name=module_name,
            message=message,
            data=data,
            thread_id=threading.current_thread().name,
            process_id=os.getpid()
        )
        
        # 添加到日志队列
        try:
            self.log_queue.put(log_entry, timeout=1.0)
        except queue.Full:
            logger.error("❌ 日志队列已满，丢弃日志条目")
    
    def log_voice_broadcast(self, message: str, voice_type: str = "tts", 
                          success: bool = True, duration: float = 0.0):
        """记录语音播报日志"""
        data = {
            "voice_type": voice_type,
            "success": success,
            "duration": duration,
            "message_length": len(message)
        }
        
        level = LogLevel.INFO if success else LogLevel.ERROR
        self.log(level, EventType.VOICE_BROADCAST, "Voice", f"语音播报: {message}", data)
    
    def log_path_status(self, status: str, blocked_count: int = 0, 
                       clear_count: int = 0, obstacles: List[str] = None):
        """记录路径状态日志"""
        if obstacles is None:
            obstacles = []
        
        data = {
            "blocked_count": blocked_count,
            "clear_count": clear_count,
            "obstacles": obstacles
        }
        
        if status == "blocked":
            self.log(LogLevel.WARNING, EventType.PATH_BLOCKED, "Path", 
                    f"路径被阻挡，障碍物: {obstacles}", data)
        else:
            self.log(LogLevel.INFO, EventType.PATH_CLEAR, "Path", 
                    f"路径畅通，障碍物: {obstacles}", data)
    
    def log_ai_detection(self, detection_type: str, objects: List[Dict[str, Any]], 
                        confidence: float, processing_time: float):
        """记录AI检测日志"""
        data = {
            "detection_type": detection_type,
            "object_count": len(objects),
            "confidence": confidence,
            "processing_time": processing_time,
            "objects": objects
        }
        
        self.log(LogLevel.INFO, EventType.AI_DETECTION, "AI", 
                f"AI检测: {detection_type}, 对象数量: {len(objects)}", data)
    
    def log_fault(self, fault_type: str, fault_id: str, severity: str, 
                  error_message: str, recovery_attempts: int = 0):
        """记录故障日志"""
        data = {
            "fault_type": fault_type,
            "fault_id": fault_id,
            "severity": severity,
            "recovery_attempts": recovery_attempts
        }
        
        level = LogLevel.CRITICAL if severity == "critical" else LogLevel.ERROR
        self.log(level, EventType.FAULT_OCCURRED, "Fault", 
                f"故障发生: {fault_type} - {error_message}", data)
    
    def log_performance(self, metric_name: str, value: float, unit: str = "", 
                       context: Dict[str, Any] = None):
        """记录性能指标日志"""
        if context is None:
            context = {}
        
        data = {
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "context": context
        }
        
        self.log(LogLevel.INFO, EventType.PERFORMANCE_METRIC, "Performance", 
                f"性能指标: {metric_name} = {value}{unit}", data)
    
    def get_log_stats(self) -> Dict[str, Any]:
        """获取日志统计信息"""
        return self.log_stats.copy()
    
    def export_logs(self, start_time: Optional[float] = None, 
                   end_time: Optional[float] = None, 
                   event_types: Optional[List[EventType]] = None) -> List[Dict[str, Any]]:
        """
        导出日志
        
        Args:
            start_time: 开始时间戳
            end_time: 结束时间戳
            event_types: 事件类型过滤
            
        Returns:
            List[Dict[str, Any]]: 日志条目列表
        """
        logs = []
        
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            # 解析日志行
                            log_entry = self._parse_log_line(line)
                            if log_entry:
                                # 时间过滤
                                if start_time and log_entry['timestamp'] < start_time:
                                    continue
                                if end_time and log_entry['timestamp'] > end_time:
                                    continue
                                
                                # 事件类型过滤
                                if event_types and log_entry['event_type'] not in [et.value for et in event_types]:
                                    continue
                                
                                logs.append(log_entry)
                        except Exception as e:
                            logger.error(f"❌ 解析日志行失败: {e}")
                            
        except Exception as e:
            logger.error(f"❌ 导出日志失败: {e}")
        
        return logs
    
    def _parse_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """解析日志行"""
        try:
            # 简单的日志行解析
            # 格式: [timestamp] [level] [event_type] [module] message | DATA: {...} | THREAD: ... | PROCESS: ...
            
            parts = line.strip().split(' | ')
            if len(parts) < 4:
                return None
            
            # 解析基础信息
            basic_info = parts[0]
            basic_parts = basic_info.split('] [')
            if len(basic_parts) < 4:
                return None
            
            timestamp_str = basic_parts[0][1:]  # 移除开头的 [
            level = basic_parts[1]
            event_type = basic_parts[2]
            module_and_message = basic_parts[3][:-1]  # 移除结尾的 ]
            
            # 分离模块和消息
            module_parts = module_and_message.split('] ', 1)
            if len(module_parts) < 2:
                return None
            
            module_name = module_parts[0]
            message = module_parts[1]
            
            # 解析数据
            data = {}
            for part in parts[1:]:
                if part.startswith('DATA: '):
                    try:
                        data_str = part[6:]  # 移除 'DATA: '
                        data = json.loads(data_str)
                    except:
                        pass
                elif part.startswith('THREAD: '):
                    thread_id = part[8:]
                elif part.startswith('PROCESS: '):
                    process_id = int(part[9:])
            
            return {
                'timestamp': time.mktime(datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f').timetuple()),
                'level': level,
                'event_type': event_type,
                'module_name': module_name,
                'message': message,
                'data': data
            }
            
        except Exception as e:
            logger.error(f"❌ 解析日志行异常: {e}")
            return None
    
    def clear_logs(self):
        """清空日志文件"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            if os.path.exists(self.backup_log_file):
                os.remove(self.backup_log_file)
            logger.info("🗑️ 日志文件已清空")
        except Exception as e:
            logger.error(f"❌ 清空日志文件失败: {e}")


# 全局日志管理器实例
global_log_manager = LogManager()

# 便捷函数
def log(level: LogLevel, event_type: EventType, module_name: str, 
        message: str, data: Dict[str, Any] = None):
    """记录日志的便捷函数"""
    global_log_manager.log(level, event_type, module_name, message, data)

def log_voice_broadcast(message: str, voice_type: str = "tts", 
                       success: bool = True, duration: float = 0.0):
    """记录语音播报日志的便捷函数"""
    global_log_manager.log_voice_broadcast(message, voice_type, success, duration)

def log_path_status(status: str, blocked_count: int = 0, 
                   clear_count: int = 0, obstacles: List[str] = None):
    """记录路径状态日志的便捷函数"""
    global_log_manager.log_path_status(status, blocked_count, clear_count, obstacles)

def log_ai_detection(detection_type: str, objects: List[Dict[str, Any]], 
                    confidence: float, processing_time: float):
    """记录AI检测日志的便捷函数"""
    global_log_manager.log_ai_detection(detection_type, objects, confidence, processing_time)

def log_fault(fault_type: str, fault_id: str, severity: str, 
              error_message: str, recovery_attempts: int = 0):
    """记录故障日志的便捷函数"""
    global_log_manager.log_fault(fault_type, fault_id, severity, error_message, recovery_attempts)

def log_performance(metric_name: str, value: float, unit: str = "", 
                   context: Dict[str, Any] = None):
    """记录性能指标日志的便捷函数"""
    global_log_manager.log_performance(metric_name, value, unit, context)


if __name__ == "__main__":
    # 测试日志管理器
    logging.basicConfig(level=logging.INFO)
    
    def test_log_manager():
        """测试日志管理器"""
        log_manager = LogManager()
        
        # 测试不同类型的日志
        log_manager.log(LogLevel.INFO, EventType.SYSTEM_START, "System", "系统启动")
        log_manager.log_voice_broadcast("你好，我是Luna", "tts", True, 1.5)
        log_manager.log_path_status("blocked", 3, 0, ["行人", "车辆", "障碍物"])
        log_manager.log_ai_detection("person", [{"type": "person", "confidence": 0.95}], 0.95, 0.1)
        log_manager.log_fault("camera", "fault_001", "high", "摄像头初始化失败")
        log_manager.log_performance("fps", 30.0, "fps", {"resolution": "1920x1080"})
        
        # 等待日志写入
        time.sleep(2)
        
        # 显示统计信息
        stats = log_manager.get_log_stats()
        print(f"📊 日志统计: {stats}")
        
        # 导出日志
        logs = log_manager.export_logs()
        print(f"📝 导出日志数量: {len(logs)}")
        
        # 停止日志管理器
        log_manager.stop()
    
    # 运行测试
    test_log_manager()
