"""
Luna Badge 配置校验模块
用于在系统启动时自动检查配置文件是否存在，若不存在则自动生成默认模板
"""

import os
import logging
from typing import Dict, Any
import yaml

logger = logging.getLogger(__name__)

# 必需配置文件列表
REQUIRED_CONFIG_FILES = {
    "system_config.yaml": {
        "device_id": "luna_badge_dev_001",
        "startup_mode": "active",
        "log_level": "info",
        "language": "zh-CN",
        "wake_word_engine": "porcupine",
        "audio_input_device": "default",
        "camera_device": 0,
        "auto_update": False
    },
    "tts_config.yaml": {
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
    "modules_enabled.yaml": {
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
    "safety_policy.yaml": {
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
    }
}


def validate_configs(force_overwrite: bool = False) -> Dict[str, str]:
    """
    校验配置文件是否存在，若不存在则自动生成默认模板
    
    Args:
        force_overwrite: 是否强制覆盖已存在的配置文件
    
    Returns:
        Dict[str, str]: 记录各配置文件的加载状态
            - "created": 新创建的配置文件
            - "loaded": 成功加载已有配置文件
            - "overwritten": 强制覆盖的配置文件
    """
    logger.info("🔍 开始校验配置文件...")
    
    # 确保config目录存在
    config_dir = "config"
    os.makedirs(config_dir, exist_ok=True)
    
    status = {}
    
    for file_name, default_config in REQUIRED_CONFIG_FILES.items():
        file_path = os.path.join(config_dir, file_name)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 创建配置文件
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)
                status[file_name] = "created"
                logger.info(f"✅ 配置缺失：已创建 {file_name}")
            except Exception as e:
                status[file_name] = "error"
                logger.error(f"❌ 创建配置文件失败 {file_name}: {e}")
        
        elif force_overwrite:
            # 强制覆盖
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)
                status[file_name] = "overwritten"
                logger.info(f"🔄 强制覆盖配置文件 {file_name}")
            except Exception as e:
                status[file_name] = "error"
                logger.error(f"❌ 强制覆盖配置文件失败 {file_name}: {e}")
        
        else:
            # 配置文件已存在且不强制覆盖
            status[file_name] = "loaded"
            logger.info(f"✅ 配置加载成功：{file_name}")
    
    logger.info(f"📋 配置文件校验完成，共处理 {len(status)} 个文件")
    return status


def load_config(file_name: str) -> Dict[str, Any]:
    """
    加载指定配置文件
    
    Args:
        file_name: 配置文件名称
    
    Returns:
        Dict[str, Any]: 配置字典
    
    Raises:
        FileNotFoundError: 配置文件不存在
        yaml.YAMLError: YAML解析错误
    """
    file_path = os.path.join("config", file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件不存在: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.debug(f"📂 成功加载配置文件: {file_name}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"❌ YAML解析错误 {file_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ 加载配置文件失败 {file_name}: {e}")
        raise


def get_config_value(config_name: str, key_path: str, default: Any = None) -> Any:
    """
    获取配置项的值（支持嵌套路径，如 "system_config.yaml:startup_mode"）
    
    Args:
        config_name: 配置文件名
        key_path: 键路径，使用点号分隔（如 "vision.crowd_detector"）
        default: 默认值
    
    Returns:
        Any: 配置值
    
    Example:
        >>> get_config_value("modules_enabled.yaml", "vision.crowd_detector")
        True
    """
    try:
        config = load_config(config_name)
        
        # 按点号分割路径
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.warning(f"⚠️ 配置项不存在: {config_name}:{key_path}，使用默认值")
                return default
        
        return value
    
    except FileNotFoundError:
        logger.warning(f"⚠️ 配置文件不存在: {config_name}，使用默认值")
        return default
    except Exception as e:
        logger.error(f"❌ 读取配置项失败 {config_name}:{key_path}: {e}")
        return default


def update_config(file_name: str, updates: Dict[str, Any]) -> bool:
    """
    更新配置文件
    
    Args:
        file_name: 配置文件名称
        updates: 更新的配置字典
    
    Returns:
        bool: 是否更新成功
    """
    file_path = os.path.join("config", file_name)
    
    try:
        # 加载现有配置
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}
        
        # 更新配置
        config.update(updates)
        
        # 保存配置
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        logger.info(f"✅ 配置文件已更新: {file_name}")
        return True
    
    except Exception as e:
        logger.error(f"❌ 更新配置文件失败 {file_name}: {e}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🔍 Luna Badge 配置校验模块测试")
    print("=" * 70)
    
    # 测试配置校验
    print("\n1. 测试配置校验...")
    status = validate_configs(force_overwrite=False)
    print(f"   配置文件状态:")
    for file_name, file_status in status.items():
        print(f"   - {file_name}: {file_status}")
    
    # 测试加载配置
    print("\n2. 测试加载配置...")
    try:
        system_config = load_config("system_config.yaml")
        print(f"   系统配置: {system_config.get('startup_mode', 'unknown')}")
        
        tts_config = load_config("tts_config.yaml")
        print(f"   TTS配置: {tts_config.get('default_voice', 'unknown')}")
        
        modules_config = load_config("modules_enabled.yaml")
        print(f"   模块配置: {modules_config.get('vision', {}).get('crowd_detector', False)}")
        
        safety_config = load_config("safety_policy.yaml")
        print(f"   安全策略: {safety_config.get('privacy_zones', {}).get('toilet', {}).get('camera_lock', False)}")
    
    except Exception as e:
        print(f"   ❌ 加载配置失败: {e}")
    
    # 测试获取配置值
    print("\n3. 测试获取配置值...")
    crowd_detector = get_config_value("modules_enabled.yaml", "vision.crowd_detector", default=False)
    print(f"   人群检测模块: {crowd_detector}")
    
    speech_speed = get_config_value("tts_config.yaml", "speech_speed", default=1.0)
    print(f"   语音速度: {speech_speed}")
    
    # 测试更新配置
    print("\n4. 测试更新配置...")
    success = update_config("system_config.yaml", {"auto_update": True})
    print(f"   更新配置: {'成功' if success else '失败'}")
    
    print("\n" + "=" * 70)

