"""
统一日志接口
提供全局日志管理器，所有模块使用此接口记录日志
"""
import sys
from typing import Optional
from datetime import datetime
from .log_config import LogConfig
from .log_writer import LogWriter


class Logger:
    """统一日志类"""
    
    _loggers: dict = {}
    _config: Optional[LogConfig] = None
    
    def __init__(self, name: str, test_mode: bool = False):
        """
        初始化日志器
        
        Args:
            name: 日志器名称（通常是模块名）
            test_mode: 是否为测试模式
        """
        self.name = name
        self.test_mode = test_mode
        
        if Logger._config is None:
            Logger._config = LogConfig()
        
        self.config = Logger._config
        self.writer = LogWriter(name, test_mode)
        
        # 日志级别映射
        self.level_map = {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 2,
            "ERROR": 3,
        }
        self.current_level = self.level_map.get(self.config.get_level(), 1)
    
    def _should_log(self, level: str) -> bool:
        """检查是否应该记录此级别的日志"""
        if not self.config.is_enabled():
            return False
        
        level_num = self.level_map.get(level, 1)
        return level_num >= self.current_level
    
    def _format_message(self, level: str, message: str) -> str:
        """格式化日志消息"""
        timestamp = datetime.now().strftime(self.config.get_date_format())
        return f"{timestamp} [{level}] {self.name}: {message}"
    
    def _log(self, level: str, message: str):
        """内部日志方法"""
        if not self._should_log(level):
            return
        
        log_entry = self._format_message(level, message)
        
        # 写入文件
        self.writer.write(log_entry)
        
        # 同时输出到控制台（可选）
        if level in ["WARNING", "ERROR"]:
            log.info("log_entry, file=sys.stderr")
        elif self.current_level <= self.level_map.get("DEBUG", 0):
            log.info("log_entry")
    
    def debug(self, message: str):
        """记录 DEBUG 级别日志"""
        self._log("DEBUG", message)
    
    def info(self, message: str):
        """记录 INFO 级别日志"""
        self._log("INFO", message)
    
    def warning(self, message: str):
        """记录 WARNING 级别日志"""
        self._log("WARNING", message)
    
    def error(self, message: str):
        """记录 ERROR 级别日志"""
        self._log("ERROR", message)
    
    def exception(self, message: str, exc_info=None):
        """记录异常信息"""
        import traceback
        error_msg = f"{message}\n{traceback.format_exc()}"
        self._log("ERROR", error_msg)
    
    def flush(self):
        """刷新日志缓冲区"""
        self.writer.flush()
    
    def close(self):
        """关闭日志器"""
        self.writer.close()


def get_logger(name: str, test_mode: bool = False) -> Logger:
    """
    获取日志器实例（单例模式）
    
    Args:
        name: 日志器名称（通常是模块名）
        test_mode: 是否为测试模式
    
    Returns:
        Logger: 日志器实例
    """
    key = f"{name}_{test_mode}"
    if key not in Logger._loggers:
        Logger._loggers[key] = Logger(name, test_mode)
    return Logger._loggers[key]


def close_all_loggers():
    """关闭所有日志器"""
    for logger in Logger._loggers.values():
        logger.close()
    Logger._loggers.clear()

