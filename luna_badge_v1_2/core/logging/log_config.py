# 日志配置模块，不使用 logger 避免循环导入
"""
日志配置管理
支持全局开关、日志级别、输出目录等配置
"""
from pathlib import Path
from typing import Optional, Dict, Any
import json
import yaml


class LogConfig:
    """日志配置类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "enabled": True,
        "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
        "log_dir": "logs/system",
        "test_log_dir": "logs/tests",
        "async_write": True,
        "rotate_daily": True,
        "max_file_size_mb": 100,
        "backup_count": 30,  # 保留30天的日志
        "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "date_format": "%Y-%m-%d %H:%M:%S",
    }
    
    _instance: Optional['LogConfig'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """加载配置"""
        # 尝试从配置文件加载
        config_paths = [
            Path("config/logging.yaml"),
            Path("config/logging.json"),
            Path("configs/logging.yaml"),
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    if config_path.suffix == '.yaml':
                        with open(config_path, 'r', encoding='utf-8') as f:
                            file_config = yaml.safe_load(f) or {}
                    else:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            file_config = json.load(f)
                    
                    self._config = {**self.DEFAULT_CONFIG, **file_config}
                    return
                except Exception as e:
                    log.error(f"Warning: Failed to load log config from {config_path}: {e}")
        
        # 使用默认配置
        self._config = self.DEFAULT_CONFIG.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(key, default)
    
    def is_enabled(self) -> bool:
        """检查日志是否启用"""
        return self._config.get("enabled", True)
    
    def get_level(self) -> str:
        """获取日志级别"""
        return self._config.get("level", "INFO")
    
    def get_log_dir(self, test_mode: bool = False) -> Path:
        """获取日志目录"""
        if test_mode:
            dir_str = self._config.get("test_log_dir", "logs/tests")
        else:
            dir_str = self._config.get("log_dir", "logs/system")
        
        log_dir = Path(dir_str)
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    
    def should_rotate_daily(self) -> bool:
        """是否按天切割日志"""
        return self._config.get("rotate_daily", True)
    
    def is_async(self) -> bool:
        """是否异步写入"""
        return self._config.get("async_write", True)
    
    def get_format(self) -> str:
        """获取日志格式"""
        return self._config.get("format", "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    def get_date_format(self) -> str:
        """获取日期格式"""
        return self._config.get("date_format", "%Y-%m-%d %H:%M:%S")

