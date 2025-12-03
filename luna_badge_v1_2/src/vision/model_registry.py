#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型注册表 - 统一管理多个 YOLO 模型

功能：
- 模型配置管理
- 模型信息查询
- 支持主模型和快速回退模型
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def _find_config_path() -> Path:
    """查找配置文件路径（支持从不同目录运行）"""
    # 尝试多个可能的路径
    possible_paths = [
        Path("configs/model_registry.yaml"),  # 项目根目录
        Path(__file__).parent.parent / "configs" / "model_registry.yaml",  # 从 core/ 目录
        Path.cwd() / "configs" / "model_registry.yaml",  # 当前工作目录
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # 如果都找不到，返回默认路径
    return Path("configs/model_registry.yaml")


CONFIG_PATH = _find_config_path()


class ModelRegistry:
    """模型注册表（单例模式）"""
    
    _config: Dict[str, Any] = {}
    _loaded: bool = False

    @classmethod
    def _load(cls) -> None:
        """加载配置文件"""
        if cls._loaded:
            return
        
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(f"Model registry config not found: {CONFIG_PATH}")
        
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cls._config = yaml.safe_load(f) or {}
        
        cls._loaded = True

    @classmethod
    def get_current_nav_model(cls) -> str:
        """获取当前导航模型名称"""
        cls._load()
        return cls._config.get("current_nav_model", "yolo11_nav_tiny_v1")

    @classmethod
    def get_current_fast_model(cls) -> Optional[str]:
        """获取当前快速模型名称（可选）"""
        cls._load()
        return cls._config.get("current_fast_model")

    @classmethod
    def get_model_info(cls, name: str) -> Dict[str, Any]:
        """获取指定模型的详细信息"""
        cls._load()
        models = cls._config.get("models") or {}
        
        if name not in models:
            raise KeyError(f"Model '{name}' not found in registry")
        
        return models[name]

    @classmethod
    def list_models(cls) -> Dict[str, Any]:
        """列出所有已注册的模型"""
        cls._load()
        return cls._config.get("models") or {}

    @classmethod
    def get_model_path(cls, name: str) -> Path:
        """获取模型文件路径"""
        info = cls.get_model_info(name)
        return Path(info["path"])

    @classmethod
    def model_exists(cls, name: str) -> bool:
        """检查模型文件是否存在"""
        try:
            path = cls.get_model_path(name)
            return path.exists()
        except (KeyError, FileNotFoundError):
            return False

