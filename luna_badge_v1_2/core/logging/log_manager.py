"""
统一日志管理器 v2.0
提供统一的日志入口，支持控制台和文件输出
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from core.config.config_center import ConfigCenter

# 注意：这里不能使用 LogManager.get_logger，因为 LogManager 还没初始化
# 使用标准 logging 作为临时方案
_temp_logger = logging.getLogger(__name__)


class LogManager:
    """统一日志管理器（单例模式）"""
    
    _initialized = False

    @classmethod
    def init(cls) -> None:
        """
        初始化日志管理器
        
        从 ConfigCenter 读取配置并设置日志系统
        """
        if cls._initialized:
            _temp_logger.warning("LogManager already initialized, skipping")
            return

        # 从配置中心读取日志配置
        level_str = ConfigCenter.get("logging.level", "INFO")
        level = getattr(logging, level_str.upper(), logging.INFO)
        log_file = ConfigCenter.get("logging.file_path", "logs/runtime.log")
        max_bytes = ConfigCenter.get("logging.max_bytes", 5 * 1024 * 1024)
        backup_count = ConfigCenter.get("logging.backup_count", 5)

        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 配置根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.handlers.clear()

        # 日志格式
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        root_logger.addHandler(console_handler)

        # 文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root_logger.addHandler(file_handler)

        cls._initialized = True
        _temp_logger.info(f"LogManager initialized: level={level_str}, file={log_file}")

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        """
        获取日志器实例
        
        Args:
            name: 日志器名称（通常是模块名），如果为 None 则返回根日志器
        
        Returns:
            logging.Logger 实例
        
        Examples:
            >>> logger = LogManager.get_logger(__name__)
            >>> logger.info("This is a log message")
        """
        if not cls._initialized:
            raise RuntimeError(
                "LogManager not initialized. Call LogManager.init() first."
            )
        return logging.getLogger(name)

