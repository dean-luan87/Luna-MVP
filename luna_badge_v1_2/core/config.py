"""
Config (v1.3.0)

配置中心

将散落在代码中的"魔法数字 & 路径 & 行为开关"收拢到一个可配置的系统中
"""

import json
import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


DEFAULT_CONFIG: Dict[str, Any] = {
    "env": "dev",  # dev / test / prod
    "models": {
        "l1_model_name": "Qwen/Qwen2.5-0.5B-Instruct",
        "l2_model_name": "Qwen/Qwen2.5-3B-Instruct",
        "enable_l1": True,
        "enable_l2": True,
    },
    "features": {
        "enable_task_chain": True,
        "enable_replay": True,
    },
    "logging": {
        "level": "DEBUG",  # DEBUG / INFO / WARN / ERROR
        "event_log_file": "logs/luna_events.log",
        "trace_log_file": "logs/trace_events.log",
        "max_file_size_mb": 10,
        "trace_sampling_rate": 1.0,  # 1.0 = 全量记录；0.5 = 50% 采样
    },
}


class Config:
    """
    配置类

    一个简单的全局配置对象：
    - 先用 DEFAULT_CONFIG
    - 再叠加 config/luna_config.json（如果存在）
    - 再叠加环境变量（可选，预留）
    """

    def __init__(self, config_path: str = "config/luna_config.json"):
        """
        初始化配置

        Args:
            config_path: 配置文件路径
        """
        self._data = DEFAULT_CONFIG.copy()
        self._load_from_file(config_path)
        self._apply_env_overrides()

    def _load_from_file(self, path: str):
        """从文件加载配置"""
        if not os.path.exists(path):
            # 没有配置文件就用默认，不报错
            logger.debug(f"配置文件不存在，使用默认配置: {path}")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._deep_update(self._data, data)
            logger.info(f"已加载配置文件: {path}")
        except json.JSONDecodeError as e:
            logger.warning(f"配置文件 JSON 格式错误，使用默认配置: {e}")
        except Exception as e:
            # 读取失败就当这个文件不存在，不阻塞运行
            logger.warning(f"加载配置文件失败，使用默认配置: {e}")

    def _apply_env_overrides(self):
        """应用环境变量覆盖（预留）"""
        # 将来可以用环境变量覆盖某些 key，比如 L1/L2 模型名
        env = os.getenv("LUNA_ENV")
        if env:
            self._data["env"] = env
            logger.info(f"环境变量 LUNA_ENV={env} 覆盖配置")

    def _deep_update(self, base: Dict[str, Any], updates: Dict[str, Any]):
        """深度更新字典"""
        for k, v in updates.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                self._deep_update(base[k], v)
            else:
                base[k] = v

    # ---- 对外访问方法 ----

    @property
    def env(self) -> str:
        """环境（dev / test / prod）"""
        return self._data.get("env", "dev")

    @property
    def models(self) -> Dict[str, Any]:
        """模型配置"""
        return self._data.get("models", {})

    @property
    def features(self) -> Dict[str, Any]:
        """功能开关"""
        return self._data.get("features", {})

    @property
    def logging(self) -> Dict[str, Any]:
        """日志配置"""
        return self._data.get("logging", {})

    def get(self, path: str, default=None):
        """
        支持类似 "logging.level" 的路径访问

        Args:
            path: 配置路径，例如 "logging.level"
            default: 默认值

        Returns:
            配置值或默认值
        """
        parts = path.split(".")
        cur = self._data
        for p in parts:
            if not isinstance(cur, dict):
                return default
            cur = cur.get(p, default)
            if cur is default:
                return default
        return cur

    def __repr__(self):
        return f"Config(env={self.env})"


# 全局单例
CONFIG = Config()
