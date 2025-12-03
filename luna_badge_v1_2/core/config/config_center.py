"""
统一配置中心
提供统一的配置入口，支持按环境加载不同配置文件
"""
from pathlib import Path
from typing import Any, Optional

import yaml

from core.logging.log_manager import LogManager

logger = LogManager.get_logger(__name__)


class ConfigCenter:
    """统一配置中心（单例模式）"""
    
    _instance = None
    _config: dict = {}
    _initialized = False

    @classmethod
    def init(cls, env: str = "dev") -> None:
        """
        初始化配置中心
        
        Args:
            env: 环境名称（dev/prod），对应 config/{env}.yaml
        """
        if cls._initialized:
            logger.warning("ConfigCenter already initialized, skipping")
            return

        # 获取项目根目录（从 core/config/ 向上两级）
        base_dir = Path(__file__).resolve().parents[2]
        default_path = base_dir / "config" / "default.yaml"
        env_path = base_dir / "config" / f"{env}.yaml"

        config = {}

        # 加载默认配置
        if default_path.exists():
            with default_path.open("r", encoding="utf-8") as f:
                default_config = yaml.safe_load(f) or {}
                config.update(default_config)
                logger.info(f"Loaded default config from {default_path}")
        else:
            logger.warning(f"Default config not found: {default_path}")

        # 加载环境配置（覆盖默认配置）
        if env_path.exists():
            with env_path.open("r", encoding="utf-8") as f:
                env_cfg = yaml.safe_load(f) or {}
                # 深度合并（简单版本，只处理顶层）
                for key, value in env_cfg.items():
                    if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
                logger.info(f"Loaded env config from {env_path}")
        else:
            logger.warning(f"Env config not found: {env_path}")

        cls._config = config
        cls._instance = cls()
        cls._initialized = True
        logger.info(f"ConfigCenter initialized with env={env}")

    @classmethod
    def get(cls, key: str, default: Optional[Any] = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键（如 "logging.level"）
            default: 默认值，如果键不存在则返回此值
        
        Returns:
            配置值或默认值
        
        Examples:
            >>> ConfigCenter.get("logging.level")
            "INFO"
            >>> ConfigCenter.get("logging.max_bytes", 1024)
            1024
        """
        if not cls._initialized:
            raise RuntimeError(
                "ConfigCenter not initialized. Call ConfigCenter.init() first."
            )

        parts = key.split(".")
        cur = cls._config

        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return default

        return cur

    @classmethod
    def get_all(cls) -> dict:
        """
        获取所有配置
        
        Returns:
            完整的配置字典
        """
        if not cls._initialized:
            raise RuntimeError(
                "ConfigCenter not initialized. Call ConfigCenter.init() first."
            )
        return cls._config.copy()

