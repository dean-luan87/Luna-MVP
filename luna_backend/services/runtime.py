"""
统一运行时容器 (RuntimeContainer) v1.2.0
替代原来 web_test_server.py 里的一堆全局变量
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List


@dataclass
class RuntimeContainer:
    """
    统一运行时容器
    
    集中管理所有全局单例服务实例
    所有原来的全局变量都从 rt.xxx 读/写
    """
    
    # ========== 视觉相关 ==========
    vision_engine: Any = None
    step_detector: Any = None
    signboard_detector: Any = None
    hazard_detector: Any = None
    facility_detector: Any = None
    traffic_light_detector: Any = None
    crowd_density_detector: Any = None
    queue_detector: Any = None
    doorplate_reader: Any = None
    saliency_roi: Any = None
    temporal_fusion: Any = None
    visual_language_fusion: Any = None
    scene_memory_system: Any = None
    local_map_generator: Any = None
    
    # ========== 导航相关 ==========
    navigation_manager: Any = None
    path_planner: Any = None
    local_map_service: Any = None  # 新的本地地图服务
    
    # ========== 语音 / TTS ==========
    whisper_recognizer: Any = None
    tts_manager: Any = None
    fast_tts_cache: Any = None
    
    # ========== 日志 / 降级 / 性能 ==========
    log_manager: Any = None
    graceful_degrader: Any = None
    performance_metrics: Dict[str, List[float]] = field(default_factory=dict)
    
    # ========== 任务系统（后台 TaskChain）==========
    task_engine: Any = None  # 比如后台版 TaskChainUnified


# 全局唯一 Runtime 实例
rt = RuntimeContainer()
