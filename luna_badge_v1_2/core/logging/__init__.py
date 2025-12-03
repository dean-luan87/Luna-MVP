"""
统一日志系统
提供全局日志接口，支持异步写入、按天切割、全局开关
"""
from .logger import Logger, get_logger, close_all_loggers
from .log_config import LogConfig
from .log_writer import LogWriter
from .log_rotator import LogRotator

__all__ = [
    "Logger",
    "get_logger",
    "close_all_loggers",
    "LogConfig",
    "LogWriter",
    "LogRotator",
]

