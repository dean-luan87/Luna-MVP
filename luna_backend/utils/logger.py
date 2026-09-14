"""
系统级日志统一入口 (v1.2.0)
统一日志：导航、视觉、TTS、错误码全部走这里
支持写入日志文件和后台上传（预留接口）
"""

import time
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime

# 日志文件路径
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_PATH = os.path.join(LOG_DIR, "system.log")
ERROR_LOG_PATH = os.path.join(LOG_DIR, "errors.log")

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)


def system_log(event_type: str, payload: Optional[Dict[str, Any]] = None, error_code: Optional[int] = None):
    """
    统一日志：导航、视觉、TTS、错误码全部走这里
    
    Args:
        event_type: 事件类型（如 "NAV_START", "TTS_ERROR", "VISION_DETECT"）
        payload: 事件数据
        error_code: 错误码（如果有）
    """
    log_entry = {
        "timestamp": int(time.time() * 1000),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "error_code": error_code,
        "payload": payload or {}
    }
    
    log_line = json.dumps(log_entry, ensure_ascii=False)
    
    # 写入系统日志
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"⚠️ 写入日志失败: {e}")
    
    # 如果是错误，同时写入错误日志
    if error_code is not None:
        try:
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"⚠️ 写入错误日志失败: {e}")
    
    # TODO: 后台上传（预留接口）
    # _upload_to_backend(log_entry)


def _upload_to_backend(log_entry: Dict[str, Any]):
    """
    后台上传日志（预留接口）
    
    Args:
        log_entry: 日志条目
    """
    # TODO: 实现后台上传逻辑
    # 例如：发送到日志收集服务、数据库等
    pass


def log_error(error_code: int, message: str, details: Optional[Dict[str, Any]] = None):
    """
    记录错误日志
    
    Args:
        error_code: 错误码
        message: 错误消息
        details: 错误详情
    """
    system_log("ERROR", {
        "message": message,
        "details": details or {}
    }, error_code=error_code)


def log_navigation(event: str, details: Optional[Dict[str, Any]] = None):
    """
    记录导航事件
    
    Args:
        event: 事件名称（如 "NAV_START", "NAV_UPDATE"）
        details: 事件详情
    """
    system_log(f"NAV_{event}", details)


def log_vision(event: str, details: Optional[Dict[str, Any]] = None):
    """
    记录视觉事件
    
    Args:
        event: 事件名称（如 "DETECT", "RELOAD"）
        details: 事件详情
    """
    system_log(f"VISION_{event}", details)


def vision_log(event: str, details: Optional[Dict[str, Any]] = None):
    """
    记录视觉事件（别名）
    
    Args:
        event: 事件名称
        details: 事件详情
    """
    log_vision(event, details)


def log_tts(event: str, details: Optional[Dict[str, Any]] = None, error_code: Optional[int] = None):
    """
    记录TTS事件
    
    Args:
        event: 事件名称（如 "SYNTH", "CACHE_HIT"）
        details: 事件详情
        error_code: 错误码（如果有）
    """
    system_log(f"TTS_{event}", details, error_code)


def task_log(event: str, details: Optional[Dict[str, Any]] = None, error_code: Optional[int] = None):
    """
    记录任务链事件
    
    Args:
        event: 事件名称（如 "ENQUEUE", "ERROR"）
        details: 事件详情
        error_code: 错误码（如果有）
    """
    system_log(f"TASK_{event}", details, error_code)


def scene_log(event: str, details: Optional[Dict[str, Any]] = None):
    """
    记录场景记忆事件
    
    Args:
        event: 事件名称（如 "ADD_NODE", "UPDATE"）
        details: 事件详情
    """
    system_log(f"SCENE_{event}", details)
