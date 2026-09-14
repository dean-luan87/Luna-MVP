"""
视觉相关日志管理 (v1.2.0)
"""

import logging
from typing import Optional, Dict, Any
from utils.logger import vision_log as system_vision_log


class VisionLogger:
    """视觉日志记录器"""
    
    def __init__(self, name: str = "vision"):
        """
        初始化视觉日志记录器
        
        Args:
            name: 日志记录器名称
        """
        self.logger = logging.getLogger(name)
        self.name = name
    
    def info(self, msg: str, details: Optional[Dict[str, Any]] = None):
        """
        记录信息日志
        
        Args:
            msg: 日志消息
            details: 详细信息
        """
        self.logger.info(msg, extra={"details": details} if details else {})
        system_vision_log("INFO", {"message": msg, "details": details or {}})
    
    def warn(self, msg: str, details: Optional[Dict[str, Any]] = None):
        """
        记录警告日志
        
        Args:
            msg: 日志消息
            details: 详细信息
        """
        self.logger.warning(msg, extra={"details": details} if details else {})
        system_vision_log("WARN", {"message": msg, "details": details or {}})
    
    def error(self, msg: str, details: Optional[Dict[str, Any]] = None, error_code: Optional[int] = None):
        """
        记录错误日志
        
        Args:
            msg: 日志消息
            details: 详细信息
            error_code: 错误码
        """
        self.logger.error(msg, extra={"details": details} if details else {})
        system_vision_log("ERROR", {"message": msg, "details": details or {}}, error_code=error_code)
    
    def debug(self, msg: str, details: Optional[Dict[str, Any]] = None):
        """
        记录调试日志
        
        Args:
            msg: 日志消息
            details: 详细信息
        """
        self.logger.debug(msg, extra={"details": details} if details else {})
        system_vision_log("DEBUG", {"message": msg, "details": details or {}})



