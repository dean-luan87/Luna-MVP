#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 统一配置管理器 v1.0
P1-1: 配置管理统一化

功能:
- 统一配置文件格式为YAML
- 单一配置入口
- 配置验证机制
- 环境变量支持
- 热加载支持
"""

import os
import yaml
import logging
import platform
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class PlatformType(Enum):
    """平台类型"""
    MAC = "mac"
    EMBEDDED = "embedded"
    LINUX = "linux"
    WINDOWS = "windows"


@dataclass
class ConfigValidationResult:
    """配置验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class UnifiedConfigManager:
    """
    统一配置管理器
    
    功能:
    1. 统一YAML格式
    2. 单一入口加载
    3. 配置验证
    4. 环境变量覆盖
    5. 配置热加载
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置目录路径
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # 平台检测
        self.platform_type = self._detect_platform()
        
        # 配置缓存
        self._config_cache: Dict[str, Any] = {}
        
        # 配置文件列表
        self.config_files = {
            "system": "system_config.yaml",
            "modules": "modules_enabled.yaml",
            "tts": "tts_config.yaml",
            "safety": "safety_policy.yaml",
            "ai_models": "ai_models.yaml",
            "navigation": "navigation.yaml",
            "hardware": "hardware.yaml",
            "memory": "memory_schema.yaml"
        }
        
        logger.info("📝 统一配置管理器初始化完成")
    
    def _detect_platform(self) -> PlatformType:
        """检测当前平台"""
        system = platform.system().lower()
        if system == "darwin":
            return PlatformType.MAC
        elif system == "linux":
            return PlatformType.LINUX
        elif system == "windows":
            return PlatformType.WINDOWS
        else:
            return PlatformType.EMBEDDED
    
    def load_all_configs(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        加载所有配置文件
        
        Args:
            force_reload: 是否强制重新加载
            
        Returns:
            所有配置的字典
        """
        if not force_reload and self._config_cache:
            logger.debug("使用配置缓存")
            return self._config_cache
        
        logger.info("📂 加载所有配置文件...")
        
        all_configs = {}
        
        for config_name, file_name in self.config_files.items():
            file_path = self.config_dir / file_name
            
            if file_path.exists():
                try:
                    config = self._load_yaml_file(file_path)
                    all_configs[config_name] = config
                    logger.debug(f"✅ 加载: {file_name}")
                except Exception as e:
                    logger.error(f"❌ 加载失败 {file_name}: {e}")
                    all_configs[config_name] = self._get_default_config(config_name)
            else:
                logger.warning(f"⚠️ 配置文件不存在: {file_name}，使用默认配置")
                all_configs[config_name] = self._get_default_config(config_name)
                self._save_config_file(config_name, all_configs[config_name])
        
        # 环境变量覆盖
        all_configs = self._override_from_env(all_configs)
        
        # 验证配置
        validation_result = self.validate_configs(all_configs)
        if not validation_result.is_valid:
            logger.error(f"❌ 配置验证失败: {validation_result.errors}")
        if validation_result.warnings:
            for warning in validation_result.warnings:
                logger.warning(f"⚠️ 配置警告: {warning}")
        
        # 缓存配置
        self._config_cache = all_configs
        
        logger.info(f"✅ 配置加载完成，共 {len(all_configs)} 个配置模块")
        return all_configs
    
    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """加载YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _save_config_file(self, config_name: str, config: Dict[str, Any]) -> bool:
        """保存配置文件"""
        try:
            file_name = self.config_files.get(config_name, f"{config_name}.yaml")
            file_path = self.config_dir / file_name
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            logger.debug(f"💾 保存: {file_name}")
            return True
        except Exception as e:
            logger.error(f"❌ 保存失败 {file_name}: {e}")
            return False
    
    def _get_default_config(self, config_name: str) -> Dict[str, Any]:
        """获取默认配置"""
        defaults = {
            "system": {
                "device_id": "luna_badge_dev_001",
                "platform": self.platform_type.value,
                "startup_mode": "active",
                "log_level": "info",
                "language": "zh-CN",
                "wake_word_engine": "porcupine",
                "audio_input_device": "default",
                "camera_device": 0,
                "auto_update": False
            },
            "modules": {
                "vision": {
                    "signboard_detector": True,
                    "hazard_detector": True,
                    "crowd_detector": True
                },
                "navigation": {
                    "path_evaluator": True,
                    "doorplate_inference": True
                },
                "memory": {
                    "memory_store": True,
                    "memory_caller": True
                },
                "communication": {
                    "tts": True,
                    "whisper": True,
                    "wakeup": True
                },
                "other": {
                    "debug_mode": False
                }
            },
            "tts": {
                "default_voice": "zh-CN-XiaoxiaoNeural",
                "default_style": "default",
                "speech_speed": 1.0,
                "speech_pitch": 1.0,
                "style_mapping": {
                    "normal": "cheerful",
                    "caution": "calm",
                    "reroute": "empathetic",
                    "stop": "serious"
                }
            },
            "safety": {
                "privacy_zones": {
                    "toilet": {
                        "camera_lock": True,
                        "gps_radius": 5,
                        "lock_duration": 300,
                        "manual_unlock_allowed": False
                    },
                    "hospital": {
                        "camera_lock": False
                    }
                },
                "failover_behavior": {
                    "gps_unavailable": "allow_with_warning",
                    "config_file_missing": "auto_generate_defaults"
                }
            },
            "ai_models": {
                "yolo": {
                    "model_path": "models/yolov8n.pt",
                    "confidence_threshold": 0.5,
                    "device": "cpu"
                },
                "whisper": {
                    "model_size": "base",
                    "language": "zh",
                    "device": "cpu"
                },
                "ocr": {
                    "engine": "paddleocr",
                    "language": "ch",
                    "use_gpu": False
                }
            },
            "navigation": {
                "environment_detection": True,
                "weather_fail_safe": True,
                "signboard_navigation": True,
                "speech_route_understand": True,
                "max_path_length": 1000,
                "path_cache_size": 100
            },
            "hardware": {
                "camera": {
                    "enabled": True,
                    "resolution": "640x480",
                    "fps": 30,
                    "format": "rgb"
                },
                "microphone": {
                    "enabled": True,
                    "sample_rate": 16000,
                    "channels": 1,
                    "format": "pcm"
                },
                "speaker": {
                    "enabled": True,
                    "volume": 0.8
                }
            },
            "memory": {
                "cache_size": 100,
                "auto_save": True,
                "save_interval": 300,
                "max_history": 1000
            }
        }
        return defaults.get(config_name, {})
    
    def _override_from_env(self, configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        从环境变量覆盖配置
        
        环境变量格式: LUNA_CONFIG_{MODULE}_{KEY}
        例如: LUNA_CONFIG_SYSTEM_LOG_LEVEL=debug
        """
        logger.debug("🔧 检查环境变量覆盖...")
        
        env_prefix = "LUNA_CONFIG_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                # 解析环境变量
                # LUNA_CONFIG_SYSTEM_LOG_LEVEL -> system.log_level
                key_part = key[len(env_prefix):].lower()
                parts = key_part.split('_', 1)
                
                if len(parts) == 2:
                    config_name, config_key = parts
                    
                    # 查找配置模块
                    if config_name in configs:
                        # 支持嵌套key (用点号分隔)
                        config_keys = config_key.replace('_', '.').split('.')
                        config_target = configs[config_name]
                        
                        # 设置嵌套值
                        for k in config_keys[:-1]:
                            if k not in config_target:
                                config_target[k] = {}
                            config_target = config_target[k]
                        
                        config_target[config_keys[-1]] = self._parse_env_value(value)
                        logger.debug(f"   {key} = {value}")
        
        return configs
    
    def _parse_env_value(self, value: str) -> Any:
        """解析环境变量值"""
        # 尝试解析为布尔值
        if value.lower() in ('true', '1', 'yes'):
            return True
        if value.lower() in ('false', '0', 'no'):
            return False
        
        # 尝试解析为数字
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # 返回字符串
        return value
    
    def validate_configs(self, configs: Optional[Dict[str, Any]] = None) -> ConfigValidationResult:
        """
        验证配置
        
        Args:
            configs: 配置字典，如果为None则验证缓存
            
        Returns:
            验证结果
        """
        if configs is None:
            configs = self._config_cache
        
        errors = []
        warnings = []
        
        # 验证必需配置
        required_configs = ["system", "modules", "tts"]
        for req_config in required_configs:
            if req_config not in configs:
                errors.append(f"缺少必需配置: {req_config}")
        
        # 验证系统配置
        if "system" in configs:
            system = configs["system"]
            if "device_id" not in system:
                errors.append("system.device_id 必需")
            if "startup_mode" not in system:
                warnings.append("system.startup_mode 未设置，使用默认值")
        
        # 验证AI模型配置
        if "ai_models" in configs:
            ai_models = configs["ai_models"]
            if "yolo" in ai_models:
                yolo_model_path = ai_models["yolo"].get("model_path")
                if yolo_model_path and not os.path.exists(yolo_model_path):
                    warnings.append(f"YOLO模型文件不存在: {yolo_model_path}")
        
        # 验证硬件配置
        if "hardware" in configs:
            hardware = configs["hardware"]
            if hardware.get("camera", {}).get("enabled"):
                camera_device = hardware.get("camera", {}).get("device", 0)
                warnings.append(f"摄像头设备: {camera_device}")
        
        is_valid = len(errors) == 0
        
        return ConfigValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def get_config(self, module: str, key: Optional[str] = None, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            module: 配置模块名（如 "system", "tts"）
            key: 配置键，支持点号分隔的嵌套键（如 "log_level" 或 "vision.signboard_detector"）
            default: 默认值
            
        Returns:
            配置值
            
        Examples:
            >>> config_manager.get_config("system")
            {...}
            
            >>> config_manager.get_config("system", "log_level")
            "info"
            
            >>> config_manager.get_config("modules", "vision.signboard_detector")
            True
        """
        if module not in self._config_cache:
            self.load_all_configs()
        
        if module not in self._config_cache:
            logger.warning(f"⚠️ 配置模块不存在: {module}")
            return default
        
        config = self._config_cache[module]
        
        # 如果未指定key，返回整个模块
        if key is None:
            return config
        
        # 支持嵌套key
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                logger.debug(f"⚠️ 配置项不存在: {module}.{key}，使用默认值")
                return default
        
        return value
    
    def set_config(self, module: str, key: str, value: Any, save: bool = True) -> bool:
        """
        设置配置值
        
        Args:
            module: 配置模块名
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
            save: 是否立即保存到文件
            
        Returns:
            是否设置成功
        """
        # 确保模块存在
        if module not in self._config_cache:
            self._config_cache[module] = {}
        
        # 设置嵌套值
        keys = key.split('.')
        config = self._config_cache[module]
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        
        # 保存到文件
        if save:
            return self.save_config(module)
        
        return True
    
    def save_config(self, module: Optional[str] = None) -> bool:
        """
        保存配置到文件
        
        Args:
            module: 配置模块名，如果为None则保存所有模块
            
        Returns:
            是否保存成功
        """
        if module:
            if module not in self._config_cache:
                logger.error(f"❌ 配置模块不存在: {module}")
                return False
            return self._save_config_file(module, self._config_cache[module])
        else:
            # 保存所有配置
            success = True
            for mod_name in self._config_cache:
                if not self._save_config_file(mod_name, self._config_cache[mod_name]):
                    success = False
            return success
    
    def reload_config(self, module: Optional[str] = None) -> bool:
        """
        重新加载配置
        
        Args:
            module: 配置模块名，如果为None则重新加载所有
            
        Returns:
            是否加载成功
        """
        if module:
            # 重新加载单个模块
            file_name = self.config_files.get(module)
            if not file_name:
                logger.error(f"❌ 未知配置模块: {module}")
                return False
            
            file_path = self.config_dir / file_name
            if file_path.exists():
                try:
                    config = self._load_yaml_file(file_path)
                    self._config_cache[module] = config
                    logger.info(f"✅ 重新加载: {module}")
                    return True
                except Exception as e:
                    logger.error(f"❌ 重新加载失败 {module}: {e}")
                    return False
            else:
                logger.error(f"❌ 配置文件不存在: {file_name}")
                return False
        else:
            # 重新加载所有
            self.load_all_configs(force_reload=True)
            return True
    
    def list_configs(self) -> List[str]:
        """列出所有配置模块"""
        return list(self._config_cache.keys())
    
    def get_config_info(self) -> Dict[str, Any]:
        """获取配置信息"""
        return {
            "config_dir": str(self.config_dir),
            "platform": self.platform_type.value,
            "modules": list(self._config_cache.keys()),
            "cache_size": len(str(self._config_cache))
        }


# 全局配置管理器实例
unified_config_manager = UnifiedConfigManager()


# 向后兼容接口
def get_config(module: str, key: Optional[str] = None, default: Any = None) -> Any:
    """向后兼容的配置获取接口"""
    return unified_config_manager.get_config(module, key, default)


def set_config(module: str, key: str, value: Any, save: bool = True) -> bool:
    """向后兼容的配置设置接口"""
    return unified_config_manager.set_config(module, key, value, save)


# 参数中心接口
def get_all_runtime_params() -> Dict[str, Dict[str, Any]]:
    """
    获取所有可调参数的当前值，用于参数中心页面。
    
    返回格式：
    {
        "navigation.max_deviation": {"value": 1.5, "description": "允许偏航距离（米）"},
        "vision.yolo_conf": {"value": 0.65, "description": "YOLO 置信度阈值"},
        ...
    }
    """
    params = {}
    
    # 从配置文件中读取可调参数
    # 这里先做一个简单的实现，后续可以根据实际配置文件扩展
    
    # 导航参数
    nav_config = unified_config_manager.get_config("navigation", None, {})
    if isinstance(nav_config, dict):
        if "max_deviation" in nav_config:
            params["navigation.max_deviation"] = {
                "value": nav_config.get("max_deviation", 1.5),
                "description": "允许偏航距离（米）"
            }
        if "step_distance_threshold" in nav_config:
            params["navigation.step_distance_threshold"] = {
                "value": nav_config.get("step_distance_threshold", 2.0),
                "description": "台阶检测距离阈值（米）"
            }
    
    # 视觉参数
    vision_config = unified_config_manager.get_config("vision", None, {})
    if isinstance(vision_config, dict):
        if "yolo_conf" in vision_config:
            params["vision.yolo_conf"] = {
                "value": vision_config.get("yolo_conf", 0.65),
                "description": "YOLO 置信度阈值"
            }
        if "ocr_enabled" in vision_config:
            params["vision.ocr_enabled"] = {
                "value": vision_config.get("ocr_enabled", True),
                "description": "是否启用OCR识别"
            }
    
    # 危险检测参数
    hazard_config = unified_config_manager.get_config("hazard", None, {})
    if isinstance(hazard_config, dict):
        if "human_filter_zone" in hazard_config:
            params["hazard.human_filter_zone"] = {
                "value": hazard_config.get("human_filter_zone", 0.3),
                "description": "人像过滤中心区域半径（米）"
            }
    
    # 系统参数
    system_config = unified_config_manager.get_config("system", None, {})
    if isinstance(system_config, dict):
        if "log_level" in system_config:
            params["system.log_level"] = {
                "value": system_config.get("log_level", "info"),
                "description": "日志级别（debug/info/warning/error）"
            }
    
    return params


def update_runtime_params(updates: Dict[str, Any]) -> Dict[str, str]:
    """
    更新部分参数。
    
    Args:
        updates: 要更新的参数，格式如 {"navigation.max_deviation": 1.5, "vision.yolo_conf": 0.65}
    
    Returns:
        成功更新的参数列表
    """
    updated = {}
    
    for key, value in updates.items():
        try:
            # 解析键名：module.key
            parts = key.split(".", 1)
            if len(parts) != 2:
                continue
            
            module, param_key = parts
            
            # 更新配置
            success = unified_config_manager.set_config(module, param_key, value, save=True)
            if success:
                updated[key] = str(value)
        except Exception as e:
            logger.warning(f"Failed to update parameter {key}: {e}")
            continue
    
    return updated


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📝 Luna Badge 统一配置管理器测试")
    print("=" * 70)
    
    # 创建管理器
    config_manager = UnifiedConfigManager()
    
    # 加载配置
    print("\n1️⃣ 加载所有配置...")
    configs = config_manager.load_all_configs()
    print(f"   加载了 {len(configs)} 个配置模块")
    
    # 获取配置
    print("\n2️⃣ 获取配置值...")
    log_level = config_manager.get_config("system", "log_level")
    print(f"   system.log_level: {log_level}")
    
    wakeup_enabled = config_manager.get_config("modules", "communication.wakeup")
    print(f"   modules.communication.wakeup: {wakeup_enabled}")
    
    # 设置配置
    print("\n3️⃣ 设置配置值...")
    success = config_manager.set_config("system", "log_level", "debug", save=False)
    print(f"   设置 system.log_level = debug: {'成功' if success else '失败'}")
    
    new_value = config_manager.get_config("system", "log_level")
    print(f"   验证新值: {new_value}")
    
    # 列表配置
    print("\n4️⃣ 列出所有配置模块...")
    modules = config_manager.list_configs()
    for mod in modules:
        print(f"   - {mod}")
    
    # 配置信息
    print("\n5️⃣ 配置信息...")
    info = config_manager.get_config_info()
    print(f"   配置目录: {info['config_dir']}")
    print(f"   平台: {info['platform']}")
    print(f"   配置模块数: {len(info['modules'])}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")

