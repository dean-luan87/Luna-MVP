#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 完整功能测试服务器
支持所有核心功能的手机端测试
"""

import os
import sys
import logging
import base64
import io
import tempfile
import time
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, render_template, send_file
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List, Optional

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# 注册统一API Gateway
try:
    from backend.api_gateway import api_v1
    app.register_blueprint(api_v1)
    logger.info("✅ API Gateway已注册")
except Exception as e:
    logger.warning(f"⚠️ API Gateway注册失败: {e}")

# 导入场景描述相关模块（延迟导入，避免初始化失败）
try:
    from backend.vision.scene_description_engine import SceneDescriptionEngine
    from backend.services.scene_describe_service import SceneDescribeService
except ImportError:
    # 不在这里报错，后面 init_all_modules 时再处理
    SceneDescriptionEngine = None
    SceneDescribeService = None

# 全局模块
vision_engine = None
step_detector = None
signboard_detector = None
hazard_detector = None
whisper_recognizer = None
# 快速TTS缓存系统
fast_tts_cache = None

def init_fast_tts_cache():
    """初始化快速TTS缓存系统"""
    global fast_tts_cache
    try:
        from core.fast_tts_cache import FastTTSCache
        fast_tts_cache = FastTTSCache(cache_dir="tts_cache")
        logger.info("✅ 快速TTS缓存系统初始化成功", extra={"module_name": "tts", "meta": {"component": "fast_tts_cache"}})
        
        # 后台预生成常用短语（不阻塞）
        import threading
        import asyncio
        def pregenerate():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(fast_tts_cache.pregenerate_common_phrases())
                loop.close()
            except Exception as e:
                logger.warning(f"⚠️ 预生成常用短语失败: {e}", extra={"module_name": "tts", "meta": {"component": "fast_tts_cache", "operation": "pregenerate"}})
        
        thread = threading.Thread(target=pregenerate, daemon=True)
        thread.start()
        logger.info("🔄 后台预生成常用短语已启动", extra={"module_name": "tts", "meta": {"component": "fast_tts_cache"}})
        
    except Exception as e:
        logger.warning(f"⚠️ 快速TTS缓存系统初始化失败: {e}", extra={"module_name": "tts", "meta": {"component": "fast_tts_cache", "error": str(e)}})
        fast_tts_cache = None
path_planner = None
navigation_manager = None
scene_memory_system = None
facility_detector = None
traffic_light_detector = None
crowd_density_detector = None
queue_detector = None
doorplate_reader = None
local_map_generator = None
log_manager = None  # 日志管理器

# ✅ 新增：场景描述引擎和服务
scene_description_engine = None
scene_describe_service = None

# 实时响应系统
time_sync_bus = None
rt_scheduler = None
policy_graph = None
vision_state_estimator = None
audio_state_estimator = None
graceful_degrader = None
performance_metrics = {
    'vision_latency': [],
    'audio_latency': [],
    'memory_usage': [],
    'fps': []
}

# 可借鉴代码模块（视角+语音导航优化）
saliency_roi = None  # 显著性ROI提取（STAViS）
temporal_fusion = None  # 时序融合（BEVFormer）
visual_language_fusion = None  # 视觉-语言融合（Talk2Nav）
visual_localization = None  # 视觉定位（ORB-SLAM2）

# 新导航链路模块
navigation_runtime = None  # NavigationRuntime 导航运行时
environment_scanner = None  # EnvironmentScanner 环境扫描器

def init_all_modules():
    """初始化所有模块"""
    global vision_engine, step_detector, signboard_detector, hazard_detector
    global whisper_recognizer, tts_manager
    global path_planner, navigation_manager, scene_memory_system
    global facility_detector, traffic_light_detector, crowd_density_detector
    global queue_detector, doorplate_reader, local_map_generator
    global log_manager
    global saliency_roi, temporal_fusion, visual_language_fusion, visual_localization
    global unified_vision_engine
    global navigation_runtime, environment_scanner
    global scene_description_engine, scene_describe_service  # ✅ 新增：场景描述引擎和服务
    
    success_count = 0
    
    # 1. 视觉OCR引擎
    try:
        from core.vision_ocr_engine import VisionOCREngine
        logger.info("正在初始化视觉OCR引擎...", extra={"module_name": "vision", "meta": {"component": "vision_ocr_engine"}})
        vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if vision_engine.load_models():
            logger.info("✅ 视觉OCR引擎初始化成功", extra={"module_name": "vision", "meta": {"component": "vision_ocr_engine"}})
            success_count += 1
        else:
            logger.warning("⚠️ 视觉OCR引擎初始化失败", extra={"module_name": "vision", "meta": {"component": "vision_ocr_engine"}})
    except Exception as e:
        logger.warning(f"⚠️ 视觉OCR引擎初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "vision_ocr_engine", "error": str(e)}})
    
    # 2. 台阶检测器
    try:
        from core.step_detector import StepDetector
        logger.info("正在初始化台阶检测器...", extra={"module_name": "vision", "meta": {"component": "step_detector"}})
        step_detector = StepDetector()
        logger.info("✅ 台阶检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "step_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 台阶检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "step_detector", "error": str(e)}})
    
    # 3. 标识牌检测器
    try:
        from core.signboard_detector import SignboardDetector
        logger.info("正在初始化标识牌检测器...", extra={"module_name": "vision", "meta": {"component": "signboard_detector"}})
        signboard_detector = SignboardDetector()
        logger.info("✅ 标识牌检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "signboard_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 标识牌检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "signboard_detector", "error": str(e)}})
    
    # 4. 危险检测器
    try:
        from core.hazard_detector import HazardDetector
        logger.info("正在初始化危险检测器...", extra={"module_name": "vision", "meta": {"component": "hazard_detector"}})
        hazard_detector = HazardDetector()
        logger.info("✅ 危险检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "hazard_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 危险检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "hazard_detector", "error": str(e)}})
    
    # 5. 语音识别器（延迟加载）
    try:
        from core.whisper_recognizer import WhisperRecognizer
        logger.info("语音识别器将在首次使用时加载...")
        whisper_recognizer = WhisperRecognizer(model_name="base", language="zh")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 语音识别器初始化异常: {e}")
    
    # 6. TTS管理器
    try:
        from core.tts_manager import TTSManager
        logger.info("正在初始化TTS管理器...", extra={"module_name": "tts", "meta": {"component": "tts_manager"}})
        tts_manager = TTSManager()
        logger.info("✅ TTS管理器初始化成功", extra={"module_name": "tts", "meta": {"component": "tts_manager"}})
        
        # 设置全局TTS管理器（规范要求）
        try:
            from backend.tts.unified_tts import set_tts_manager
            set_tts_manager(tts_manager)
            logger.info("✅ 统一TTS接口已设置", extra={"module_name": "tts", "meta": {"component": "unified_tts"}})
        except Exception as e:
            logger.warning(f"⚠️ 统一TTS接口设置失败: {e}", extra={"module_name": "tts", "meta": {"component": "unified_tts", "error": str(e)}})
        
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ TTS管理器初始化异常: {e}", extra={"module_name": "tts", "meta": {"component": "tts_manager", "error": str(e)}})
    
    # 7. 场景记忆系统（导航基础）
    try:
        from core.scene_memory_system import get_scene_memory_system
        logger.info("正在初始化场景记忆系统...", extra={"module_name": "navigation", "meta": {"component": "scene_memory_system"}})
        scene_memory_system = get_scene_memory_system()
        logger.info("✅ 场景记忆系统初始化成功", extra={"module_name": "navigation", "meta": {"component": "scene_memory_system"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 场景记忆系统初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "scene_memory_system", "error": str(e)}})
    
    # 8. 路径规划器
    try:
        from core.path_planner import PathPlanner
        logger.info("正在初始化路径规划器...", extra={"module_name": "navigation", "meta": {"component": "path_planner"}})
        if scene_memory_system:
            path_planner = PathPlanner(scene_memory_system)
            logger.info("✅ 路径规划器初始化成功", extra={"module_name": "navigation", "meta": {"component": "path_planner"}})
            success_count += 1
        else:
            logger.warning("⚠️ 场景记忆系统未初始化，跳过路径规划器", extra={"module_name": "navigation", "meta": {"component": "path_planner"}})
    except Exception as e:
        logger.warning(f"⚠️ 路径规划器初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "path_planner", "error": str(e)}})
    
    # 初始化快速TTS缓存系统
    init_fast_tts_cache()
    try:
        from core.navigation_manager import NavigationManager
        logger.info("正在初始化导航管理器...", extra={"module_name": "navigation", "meta": {"component": "navigation_manager"}})
        
        # 定义TTS播报回调函数
        def tts_broadcast_callback(text: str, style: str = "calm"):
            """TTS播报回调"""
            if tts_manager:
                try:
                    # 异步播报，不阻塞导航
                    import threading
                    def async_speak():
                        try:
                            tts_manager.speak(text, style)
                        except Exception as e:
                            logger.warning(f"⚠️ TTS播报失败: {e}", extra={"module_name": "tts", "meta": {"component": "tts_broadcast", "error": str(e)}})
                    thread = threading.Thread(target=async_speak)
                    thread.daemon = True
                    thread.start()
                except Exception as e:
                    logger.warning(f"⚠️ TTS播报线程启动失败: {e}", extra={"module_name": "tts", "meta": {"component": "tts_broadcast", "error": str(e)}})
            else:
                logger.info(f"🔊 [模拟播报] {text} (风格: {style})", extra={"module_name": "tts", "meta": {"component": "tts_broadcast", "style": style}})
        
        navigation_manager = NavigationManager(tts_callback=tts_broadcast_callback)
        logger.info("✅ 导航管理器初始化成功（已启用语音播报）", extra={"module_name": "navigation", "meta": {"component": "navigation_manager"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 导航管理器初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "navigation_manager", "error": str(e)}})
    
    # 10. 公共设施检测器
    try:
        from core.facility_detector import FacilityDetector
        logger.info("正在初始化公共设施检测器...", extra={"module_name": "vision", "meta": {"component": "facility_detector"}})
        facility_detector = FacilityDetector()
        logger.info("✅ 公共设施检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "facility_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 公共设施检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "facility_detector", "error": str(e)}})
    
    # 11. 红绿灯检测器
    try:
        from core.traffic_light_detector import TrafficLightDetector
        logger.info("正在初始化红绿灯检测器...", extra={"module_name": "vision", "meta": {"component": "traffic_light_detector"}})
        traffic_light_detector = TrafficLightDetector()
        logger.info("✅ 红绿灯检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "traffic_light_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 红绿灯检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "traffic_light_detector", "error": str(e)}})
    
    # 12. 人群密度检测器
    try:
        from core.crowd_density_detector import CrowdDensityDetector
        logger.info("正在初始化人群密度检测器...", extra={"module_name": "vision", "meta": {"component": "crowd_density_detector"}})
        crowd_density_detector = CrowdDensityDetector()
        logger.info("✅ 人群密度检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "crowd_density_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 人群密度检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "crowd_density_detector", "error": str(e)}})
    
    # 13. 排队检测器
    try:
        from core.queue_detector import QueueDetector
        logger.info("正在初始化排队检测器...", extra={"module_name": "vision", "meta": {"component": "queue_detector"}})
        queue_detector = QueueDetector()
        logger.info("✅ 排队检测器初始化成功", extra={"module_name": "vision", "meta": {"component": "queue_detector"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 排队检测器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "queue_detector", "error": str(e)}})
    
    # 14. 门牌号识别器
    try:
        from core.doorplate_reader import DoorplateReader
        logger.info("正在初始化门牌号识别器...", extra={"module_name": "vision", "meta": {"component": "doorplate_reader"}})
        doorplate_reader = DoorplateReader()
        logger.info("✅ 门牌号识别器初始化成功", extra={"module_name": "vision", "meta": {"component": "doorplate_reader"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 门牌号识别器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "doorplate_reader", "error": str(e)}})
    
    # 15. 本地地图生成器
    try:
        from core.local_map_generator import LocalMapGenerator
        logger.info("正在初始化本地地图生成器...", extra={"module_name": "navigation", "meta": {"component": "local_map_generator"}})
        local_map_generator = LocalMapGenerator()
        logger.info("✅ 本地地图生成器初始化成功", extra={"module_name": "navigation", "meta": {"component": "local_map_generator"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 本地地图生成器初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "local_map_generator", "error": str(e)}})
    
    # 16. 日志管理器
    try:
        from core.log_manager import LogManager
        logger.info("正在初始化日志管理器...", extra={"module_name": "system", "meta": {"component": "log_manager"}})
        log_manager = LogManager(user_id="web_test_user", log_dir="logs/web_test")
        logger.info("✅ 日志管理器初始化成功", extra={"module_name": "system", "meta": {"component": "log_manager"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 日志管理器初始化异常: {e}", extra={"module_name": "system", "meta": {"component": "log_manager", "error": str(e)}})
    
    # =====================
    # ✅ 场景描述引擎和服务初始化
    # =====================
    try:
        if SceneDescriptionEngine is not None and vision_engine is not None:
            scene_description_engine = SceneDescriptionEngine(
                vision_engine=vision_engine,
                signboard_detector=signboard_detector,
                facility_detector=facility_detector,
                hazard_detector=hazard_detector,
                step_detector=step_detector,
                crowd_density_detector=crowd_density_detector,
            )
            logger.info("✅ SceneDescriptionEngine 初始化成功", extra={"module_name": "vision", "meta": {"component": "scene_description_engine"}})
            success_count += 1
        else:
            logger.warning("⚠️ SceneDescriptionEngine 未初始化：缺少 SceneDescriptionEngine 类或 vision_engine", extra={"module_name": "vision", "meta": {"component": "scene_description_engine"}})
            scene_description_engine = None

        if SceneDescribeService is not None and scene_description_engine is not None:
            scene_describe_service = SceneDescribeService(scene_description_engine)
            logger.info("✅ SceneDescribeService 初始化成功", extra={"module_name": "vision", "meta": {"component": "scene_describe_service"}})
            success_count += 1
        else:
            logger.warning("⚠️ SceneDescribeService 未初始化：缺少 SceneDescribeService 类或 scene_description_engine", extra={"module_name": "vision", "meta": {"component": "scene_describe_service"}})
            scene_describe_service = None
    except Exception as e:
        logger.warning(f"⚠️ SceneDescription 相关模块初始化失败: {e}", extra={"module_name": "vision", "meta": {"component": "scene_description", "error": str(e)}})
        scene_description_engine = None
        scene_describe_service = None
    
    # 17. 实时响应系统
    try:
        from core.realtime_system import (
            get_time_sync_bus, get_rt_scheduler, get_policy_graph,
            StateEstimator, GracefulDegrader
        )
        from core.realtime_policies import DEFAULT_POLICY_RULES
        
        logger.info("正在初始化实时响应系统...")
        time_sync_bus = get_time_sync_bus()
        rt_scheduler = get_rt_scheduler()
        policy_graph = get_policy_graph()
        policy_graph.load_rules(DEFAULT_POLICY_RULES)
        
        # 注册策略动作
        def tts_action(text: str = None):
            """TTS播报动作"""
            if text and tts_manager:
                rt_scheduler.enqueue_high(lambda: tts_manager.speak_sync(text))
        
        def nav_start_action():
            """导航启动动作"""
            logger.info("策略触发：启动导航")
            # 这里可以添加导航启动逻辑
        
        policy_graph.register_actions({
            'tts': tts_action,
            'nav.start': nav_start_action
        })
        
        # 状态估计器
        vision_state_estimator = StateEstimator(alpha=0.7)  # 视觉状态平滑
        audio_state_estimator = StateEstimator(alpha=0.8)   # 音频状态平滑
        
        # 优雅降级器
        def monitor_performance():
            """性能监控回调"""
            try:
                import psutil
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
            except:
                memory_mb = 0
            
            # 从调度器获取延迟p95
            scheduler_metrics = rt_scheduler.get_metrics()
            p95 = scheduler_metrics.get('p95', 0)
            
            # 计算FPS
            fps_history = performance_metrics.get('fps', [])
            fps = fps_history[-1] if fps_history else 30
            
            return {'p95': p95, 'heap': memory_mb, 'fps': fps}
        
        def apply_degrade(level):
            """应用降级级别"""
            logger.info(f"📉 应用降级级别: {level.value}")
            # 这里可以根据级别调整检测频率、分辨率等
            # 暂时只记录日志
        
        graceful_degrader = GracefulDegrader(monitor_performance, apply_degrade)
        
        logger.info("✅ 实时响应系统初始化成功", extra={"module_name": "system", "meta": {"component": "realtime_system"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 实时响应系统初始化异常: {e}", extra={"module_name": "system", "meta": {"component": "realtime_system", "error": str(e)}})
    
    # 18. 可借鉴代码模块（视角+语音导航优化）
    try:
        from core.saliency_roi import SaliencyROI
        logger.info("正在初始化显著性ROI提取器（STAViS）...", extra={"module_name": "vision", "meta": {"component": "saliency_roi"}})
        saliency_roi = SaliencyROI()
        logger.info("✅ 显著性ROI提取器初始化成功", extra={"module_name": "vision", "meta": {"component": "saliency_roi"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 显著性ROI提取器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "saliency_roi", "error": str(e)}})
    
    try:
        from core.temporal_fusion import TemporalFusion
        logger.info("正在初始化时序融合器（BEVFormer）...", extra={"module_name": "vision", "meta": {"component": "temporal_fusion"}})
        temporal_fusion = TemporalFusion(window_size=3, vote_threshold=2)
        logger.info("✅ 时序融合器初始化成功", extra={"module_name": "vision", "meta": {"component": "temporal_fusion"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 时序融合器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "temporal_fusion", "error": str(e)}})
    
    try:
        from core.visual_language_fusion import VisualLanguageFusion
        logger.info("正在初始化视觉-语言融合器（Talk2Nav）...", extra={"module_name": "vision", "meta": {"component": "visual_language_fusion"}})
        visual_language_fusion = VisualLanguageFusion()
        logger.info("✅ 视觉-语言融合器初始化成功", extra={"module_name": "vision", "meta": {"component": "visual_language_fusion"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 视觉-语言融合器初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "visual_language_fusion", "error": str(e)}})
    
    try:
        from core.visual_localization import VisualLocalization
        logger.info("正在初始化视觉定位系统（ORB-SLAM2）...")
        visual_localization = VisualLocalization()
        logger.info("✅ 视觉定位系统初始化成功")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 视觉定位系统初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "visual_localization", "error": str(e)}})
    
    # ========== 初始化统一视觉引擎（规范要求）==========
    try:
        from backend.engines.vision_engine import get_vision_engine
        unified_vision_engine = get_vision_engine(
            vision_ocr_engine=vision_engine,
            step_detector=step_detector,
            signboard_detector=signboard_detector,
            hazard_detector=hazard_detector,
            facility_detector=facility_detector,
            traffic_light_detector=traffic_light_detector,
            crowd_density_detector=crowd_density_detector,
            queue_detector=queue_detector,
            doorplate_reader=doorplate_reader
        )
        logger.info("✅ 统一视觉引擎初始化成功", extra={"module_name": "vision", "meta": {"component": "unified_vision_engine"}})
    except Exception as e:
        logger.warning(f"⚠️ 统一视觉引擎初始化异常: {e}", extra={"module_name": "vision", "meta": {"component": "unified_vision_engine", "error": str(e)}})
    
    # ========== 初始化新导航链路模块 ==========
    # 22. EnvironmentScanner（环境扫描器）
    try:
        from core.navigation import EnvironmentScanner
        logger.info("正在初始化环境扫描器（EnvironmentScanner）...", extra={"module_name": "navigation", "meta": {"component": "environment_scanner"}})
        environment_scanner = EnvironmentScanner()
        logger.info("✅ 环境扫描器初始化成功", extra={"module_name": "navigation", "meta": {"component": "environment_scanner"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 环境扫描器初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "environment_scanner", "error": str(e)}})
    
    # 23. NavigationRuntime（导航运行时）
    try:
        from core.navigation import NavigationRuntime
        logger.info("正在初始化导航运行时（NavigationRuntime）...", extra={"module_name": "navigation", "meta": {"component": "navigation_runtime"}})
        
        # 定义结果回调函数（用于触发事件和TTS）
        def on_navigation_result(result: Dict[str, Any]):
            """导航结果回调：触发事件和TTS播报"""
            try:
                # 记录日志
                if log_manager:
                    log_manager.log_visual_event(
                        event_type="navigation_runtime_result",
                        detection_result=result
                    )
                
                # 触发危险事件
                if result.get("environment_hint"):
                    hint = result["environment_hint"]
                    if "台阶" in hint or "危险" in hint:
                        # 这里可以触发 UnifiedEventManager 的 emitHazardEvent
                        logger.info(f"[NavigationRuntime] 检测到危险提示: {hint}")
                
                # 触发导航事件
                direction = result.get("primary_direction", "forward")
                if direction != "forward":
                    logger.info(f"[NavigationRuntime] 导航方向: {direction}")
                
                # TTS播报（如果有推荐动作）
                if result.get("recommended_action") and tts_manager:
                    try:
                        tts_manager.speak(result["recommended_action"])
                    except Exception as e:
                        logger.warning(f"TTS播报失败: {e}")
            except Exception as e:
                logger.error(f"[NavigationRuntime] 结果回调错误: {e}")
        
        navigation_runtime = NavigationRuntime(
            ideal_heading_deg=None,  # 可以从路径规划动态设置
            on_result=on_navigation_result
        )
        logger.info("✅ 导航运行时初始化成功", extra={"module_name": "navigation", "meta": {"component": "navigation_runtime"}})
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 导航运行时初始化异常: {e}", extra={"module_name": "navigation", "meta": {"component": "navigation_runtime", "error": str(e)}})
    
    logger.info(f"✅ 模块初始化完成: {success_count}/23 个模块成功", extra={"module_name": "system", "meta": {"success_count": success_count, "total_modules": 23}})
    return success_count > 0

def image_to_numpy(image_data):
    """将图片数据转换为numpy数组"""
    try:
        # 处理不同类型的输入
        if isinstance(image_data, str):
            # 如果是base64字符串
            image_data = base64.b64decode(image_data)
        elif hasattr(image_data, 'read'):
            # 如果是文件对象
            image_data = image_data.read()
        
        # 检查数据是否为空
        if not image_data or len(image_data) == 0:
            logger.error("图片数据为空")
            return None
        
        # 尝试打开图片
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            logger.error(f"PIL打开图片失败: {e}, 数据长度: {len(image_data)}")
            # 尝试使用cv2直接读取
            try:
                nparr = np.frombuffer(image_data, np.uint8)
                img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img_bgr is not None:
                    logger.info("使用cv2.imdecode成功读取图片")
                    return img_bgr
            except Exception as e2:
                logger.error(f"cv2.imdecode也失败: {e2}")
            return None
        
        # 转换颜色模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        logger.debug(f"图片转换成功: 尺寸={img_bgr.shape}")
        return img_bgr
    except Exception as e:
        logger.error(f"图片转换失败: {e}", exc_info=True)
        return None

# HTML模板（完整版）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Luna 完整功能测试</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 { text-align: center; color: #333; margin-bottom: 20px; font-size: 28px; }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            background: #f5f5f5;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .tab.active {
            background: #667eea;
            color: white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        video { width: 100%; border-radius: 15px; background: #000; }
        canvas { display: none; }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.3s;
        }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-secondary { background: #f0f0f0; color: #333; }
        .btn-danger { background: #ff6b6b; color: white; }
        .btn-success { background: #51cf66; color: white; }
        .btn:active { transform: scale(0.98); opacity: 0.9; }
        .file-input { display: none; }
        .result-section {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .result-section.active { display: block; }
        .result-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .result-item {
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .result-text { font-size: 15px; color: #333; margin-bottom: 5px; }
        .result-confidence { font-size: 13px; color: #666; }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }
        .badge-success { background: #51cf66; color: white; }
        .badge-warning { background: #ffd43b; color: #333; }
        .badge-danger { background: #ff6b6b; color: white; }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .loading.active { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            display: none;
        }
        .error.active { display: block; }
        .audio-controls {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .audio-controls button {
            flex: 1;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Luna 完整功能测试</h1>
        
        <!-- 测试按钮 - 用于验证JavaScript是否工作 -->
        <div id="testButton" style="padding:10px; margin-bottom:10px; background:#fff3cd; border-radius:5px; text-align:center; border:2px solid #ffc107;">
            <button id="testJsButton" style="padding:10px 20px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer; font-size:16px;">
                🧪 点击测试JavaScript是否工作
            </button>
        </div>
        
        <div class="tabs">
            <button class="tab active" data-tab="product">🌟 完整产品模式</button>
            <button class="tab" data-tab="vision">👁️ 视觉识别</button>
            <button class="tab" data-tab="voice">🎤 语音功能</button>
            <button class="tab" data-tab="comprehensive">🔍 综合检测</button>
            <button class="tab" data-tab="navigation">🧭 离线导航</button>
            <button class="tab" data-tab="logs">📊 日志管理</button>
        </div>
        
        <!-- 完整产品模式标签页 -->
        <div id="product-tab" class="tab-content active">
            <div style="background:#e8f5e9; border:2px solid #4CAF50; border-radius:8px; padding:20px; margin-bottom:20px;">
                <h2 style="margin:0 0 15px 0; color:#2E7D32;">🌟 Luna 完整产品模式</h2>
                <div style="font-size:14px; line-height:1.8; color:#1B5E20;">
                    <strong>💡 产品模式说明：</strong><br>
                    • 开启摄像头后自动进入完整模式<br>
                    • 自动视觉识别 + 实时语音播报<br>
                    • 持续语音监听 + 语音对话交互<br>
                    • 自动检测障碍并播报警告<br>
                    • 模拟真实产品使用体验
                </div>
            </div>
            
            <!-- 视频显示区域 -->
            <div style="margin-bottom:20px; text-align:center;">
                <video id="productVideo" autoplay playsinline webkit-playsinline style="width:100%; max-width:640px; border-radius:8px; background:#000;"></video>
                <canvas id="productCanvas" style="display:none;"></canvas>
            </div>
            
            <div style="text-align:center; margin-bottom:20px;">
                <button id="startProductModeBtn" class="btn btn-success" style="width:100%; padding:20px; font-size:20px; font-weight:bold;">
                    🚀 启动完整产品模式
                </button>
                <button id="stopProductModeBtn" class="btn btn-danger" style="width:100%; padding:20px; margin-top:15px; font-size:18px; display:none;">
                    ⏹️ 停止产品模式
                </button>
            </div>
            
            <div id="productModeStatus" style="padding:15px; background:#f5f5f5; border-radius:8px; margin-bottom:15px; display:none;">
                <div style="font-size:16px; font-weight:bold; margin-bottom:10px; color:#4CAF50;">✅ 产品模式运行中</div>
                <div id="productStatusDetails" style="font-size:14px; color:#666;"></div>
                <!-- 调试信息显示区域（iPhone Safari无法使用控制台） -->
                <div id="debugInfo" style="margin-top:15px; padding:10px; background:#fff; border:1px solid #ddd; border-radius:5px; font-size:12px; font-family:monospace; max-height:200px; overflow-y:auto; display:none;">
                    <div style="font-weight:bold; margin-bottom:5px; color:#666;">🔍 调试信息：</div>
                    <div id="debugLog" style="line-height:1.6; color:#333;"></div>
                </div>
            </div>
            
            <div id="productGuidance" style="padding:15px; background:white; border:2px solid #4CAF50; border-radius:8px; margin-bottom:15px; display:none;">
                <div style="font-size:18px; text-align:center; margin-bottom:15px; font-weight:bold;" id="guidanceDirection">⬆️ FORWARD</div>
                <div id="guidanceMessages" style="font-size:14px; line-height:1.8;"></div>
            </div>
            
            <div id="productVoiceStatus" style="padding:15px; background:#e3f2fd; border-radius:8px; margin-bottom:15px; display:none;">
                <div style="font-size:14px; font-weight:bold; margin-bottom:8px;">🎤 语音状态</div>
                <div id="voiceStatusText" style="font-size:13px; color:#1976D2;">正在监听...</div>
                <div id="voiceRecognitionResult" style="margin-top:10px; padding:10px; background:white; border-radius:5px; font-size:13px; display:none;"></div>
                <div id="voicePlaybackStatus" style="margin-top:10px; padding:10px; background:#fff3cd; border-radius:5px; font-size:13px; display:none;">
                    <div style="color:#856404;">🔊 正在播放语音...</div>
                    <div id="playbackText" style="margin-top:5px; color:#666;"></div>
                </div>
            </div>
        </div>
        
        <!-- 视觉识别标签页 -->
        <div id="vision-tab" class="tab-content">
            <div style="background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:12px; margin-bottom:15px; font-size:14px; color:#856404;">
                <strong>💡 Safari浏览器提示：</strong><br>
                如果摄像头无法使用，请使用"选择图片"功能上传照片进行识别。
            </div>
            <video id="video" autoplay playsinline webkit-playsinline></video>
            <canvas id="canvas"></canvas>
            
            <button id="startCameraBtn" class="btn btn-primary">📷 打开摄像头</button>
            <button class="btn btn-primary" id="captureBtn" style="display:none;">📸 拍照识别</button>
            <button class="btn btn-secondary" id="stopBtn" style="display:none;">⏹️ 关闭摄像头</button>
            
            <label for="fileInput" class="btn btn-secondary" style="background:#28a745; color:white;">
                📁 选择图片（推荐Safari使用）
            </label>
            <input type="file" id="fileInput" class="file-input" accept="image/*" capture="environment">
            
            <button id="testStepBtn" class="btn btn-success">🪜 台阶检测</button>
            <button id="testSignboardBtn" class="btn btn-success">🚏 标识牌检测</button>
            <button id="testHazardBtn" class="btn btn-danger">⚠️ 危险检测</button>
            <button id="testFacilityBtn" class="btn btn-success">🏛️ 公共设施</button>
            <button id="testTrafficLightBtn" class="btn btn-success">🚦 红绿灯</button>
            <button id="testCrowdDensityBtn" class="btn btn-success">👥 人群密度</button>
            <button id="testQueueBtn" class="btn btn-success">📋 排队检测</button>
            <button id="testDoorplateBtn" class="btn btn-success">🚪 门牌号</button>
        </div>
        
        <!-- 实时视觉导航 -->
        <div style="margin-top: 20px; padding: 15px; background: #f0f8ff; border-radius: 8px; border: 2px solid #4CAF50;">
            <h3 style="margin-bottom: 15px; color: #2E7D32;">🎥 实时视觉导航</h3>
            <div style="background:#e8f5e9; border:1px solid #4CAF50; border-radius:8px; padding:12px; margin-bottom:15px; font-size:14px; color:#1B5E20;">
                <strong>💡 功能说明：</strong><br>
                • 开启摄像头后，实时分析画面<br>
                • 自动识别方向标识、门牌号、标识牌<br>
                • 提供前进路线指引（直行/左转/右转）<br>
                • 检测台阶和危险并自动警告<br>
                • 适合小范围内导航（如医院走廊、商场）
            </div>
            <button id="startVisualNavBtn" class="btn btn-success" style="width:100%; padding:15px; font-size:16px; font-weight:bold;">
                🎥 开始实时视觉导航
            </button>
            <button id="stopVisualNavBtn" class="btn btn-secondary" style="width:100%; padding:15px; margin-top:10px; font-size:16px;">
                ⏹️ 停止视觉导航
            </button>
            <div id="visualGuidanceResult" style="margin-top:15px; padding:10px; background:white; border-radius:8px; display:none;">
                <div id="guidanceMessages" style="font-size:14px; line-height:1.8;"></div>
            </div>
        </div>
        
        <!-- 语音功能标签页 -->
        <div id="voice-tab" class="tab-content">
            <h3 style="margin-bottom: 15px;">语音识别</h3>
            <button id="startRecordBtn" class="btn btn-primary">🎤 开始录音</button>
            <button class="btn btn-secondary" id="stopRecordBtn" style="display:none;">⏹️ 停止录音</button>
            
            <div id="recordingStatus" style="text-align:center; margin:15px 0; color:#667eea; font-weight:bold; display:none;">
                🔴 正在录音...
            </div>
            
            <h3 style="margin-top: 30px; margin-bottom: 15px;">语音合成</h3>
            <textarea id="ttsText" placeholder="输入要合成的文字（最多5000字符，超过将自动分段）" 
                maxlength="5000" 
                style="width:100%; padding:12px; border:2px solid #eee; border-radius:8px; margin-bottom:5px; font-size:16px; min-height:100px; resize:vertical; font-family:inherit;"></textarea>
            <div style="text-align:right; color:#666; font-size:12px; margin-bottom:10px;">
                <span id="charCount">0</span> / 5000 字符
            </div>
            
            <!-- 音量控制 -->
            <div style="margin:15px 0; padding:15px; background:#f8f9fa; border-radius:8px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span style="font-weight:bold; color:#333;">🔊 音量控制：</span>
                    <span id="volumeDisplay" style="font-weight:bold; color:#667eea; min-width:50px;">100%</span>
                </div>
                <div style="display:flex; gap:5px;">
                    <button id="volumeDownBtn" class="btn btn-secondary" style="flex:1; padding:10px; font-size:14px;">🔉 降低</button>
                    <button id="volumeUpBtn" class="btn btn-secondary" style="flex:1; padding:10px; font-size:14px;">🔊 提高</button>
                </div>
                <div style="margin-top:10px; font-size:12px; color:#666;">
                    💡 提示：也可以使用手机音量键控制（部分浏览器支持）
                </div>
            </div>
            
            <div class="audio-controls">
                <button id="ttsCheerfulBtn" class="btn btn-success">😊 欢快</button>
                <button id="ttsCalmBtn" class="btn btn-success">😌 平静</button>
                <button id="ttsUrgentBtn" class="btn btn-success">⚡ 紧急</button>
            </div>
        </div>
        
        <!-- 综合检测标签页 -->
        <div id="comprehensive-tab" class="tab-content">
            <div style="background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:15px; margin-bottom:15px; font-size:14px; color:#856404;">
                <strong>🔍 综合检测功能：</strong><br>
                同时运行所有视觉检测模块，包括：<br>
                • 基础视觉识别（YOLO + OCR）<br>
                • 台阶检测、标识牌检测、危险检测<br>
                • 公共设施检测、红绿灯检测<br>
                • 人群密度检测、排队检测、门牌号识别<br>
                生成完整的分析报告
            </div>
            <button id="comprehensiveDetectionBtn" class="btn btn-primary">🔍 综合检测</button>
            <p style="margin-top: 15px; color: #666; font-size: 14px;">
                点击按钮后，将对当前图片进行所有检测模块的分析
            </p>
            
            <!-- 自动百度抓图测试 -->
            <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">🤖 自动百度抓图测试</h3>
            <div style="background:#e8f5e9; border:1px solid #4CAF50; border-radius:8px; padding:15px; margin-bottom:15px;">
                <p style="font-size:14px; color:#2E7D32; margin-bottom:10px;">
                    <strong>💡 功能说明：</strong><br>
                    自动从百度图片搜索抓取测试图片，并自动调用 Luna 场景描述功能进行测试
                </p>
                <button id="btnShowKeywords" class="btn btn-secondary" style="width:100%; margin-bottom:10px;">📋 加载关键词列表</button>
                <select id="keywordList" class="form-select" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px; font-size:14px;">
                    <option value="">请先加载关键词列表</option>
                </select>
                <button id="btnAutoFetchTest" class="btn btn-primary" style="width:100%; margin-bottom:10px;">🚀 自动抓图并测试</button>
                <img id="autoTestImagePreview" style="margin-top:10px; max-width:100%; border:1px solid #ccc; border-radius:8px; display:none;" />
                <div id="autoTestResult" style="margin-top:15px; padding:15px; background:#f8f9fa; border-radius:8px; display:none;">
                    <div style="font-weight:bold; margin-bottom:10px; color:#333;">📝 场景描述结果：</div>
                    <div id="autoTestResultContent" style="font-size:14px; line-height:1.8; color:#666;"></div>
                </div>
            </div>
            
            <!-- 自动测试结果分类 -->
            <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">📊 自动测试结果</h3>
            <div class="row mt-2" style="display:flex; gap:15px; margin-bottom:20px;">
                <div class="col" style="flex:1; background:#e8f5e9; padding:15px; border-radius:8px;">
                    <h5 style="color:#2E7D32; margin-bottom:10px;">✅ 匹配成功</h5>
                    <ul id="matchList" class="list-group" style="list-style:none; padding:0; max-height:300px; overflow-y:auto;"></ul>
                </div>
                <div class="col" style="flex:1; background:#fff3cd; padding:15px; border-radius:8px;">
                    <h5 style="color:#856404; margin-bottom:10px;">⚠️ 匹配失败（待人工校正）</h5>
                    <ul id="failList" class="list-group" style="list-style:none; padding:0; max-height:300px; overflow-y:auto;"></ul>
                </div>
            </div>
            
            <!-- 人工审批区域 -->
            <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">👤 人工校对</h3>
            <div id="reviewBox" style="display:none; background:#f8f9fa; padding:20px; border-radius:8px; margin-bottom:15px;">
                <img id="reviewImg" style="max-width:60%; border:1px solid #ccc; border-radius:8px; margin-bottom:15px;" />
                <p id="reviewDesc" class="mt-2" style="font-size:14px; color:#333; margin-bottom:15px;"></p>
                
                <!-- 新增：错误类型 / 场景标签 -->
                <input id="clusterInput" type="text" placeholder="错误类型/场景标签（可选，如：台阶漏检、入口识别错）" 
                       style="width:100%; padding:10px; border:1px solid #ddd; border-radius:4px; margin-bottom:15px; font-size:14px;" />
                
                <div style="display:flex; gap:10px;">
                    <button id="btnMarkCorrect" class="btn btn-success" style="flex:1;">✅ AI判断正确</button>
                    <button id="btnMarkWrong" class="btn btn-danger" style="flex:1;">❌ AI判断错误（加入训练集）</button>
                </div>
            </div>
            
            <!-- CSV 导出 -->
            <button id="btnExportCSV" class="btn btn-dark mt-3" style="width:100%; padding:15px; font-size:16px;">📥 导出 CSV</button>
            
            <!-- V6.1：自动搜图 + 错误聚类 -->
            <hr style="margin-top:40px; margin-bottom:20px; border-top:2px solid #ddd;" />
            <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">🔍 V6.1：自动搜图 + 错误聚类</h3>
            <div style="background:#e7f3ff; border:1px solid #2196F3; border-radius:8px; padding:20px; margin-bottom:20px;">
                <p style="font-size:14px; color:#1976D2; margin-bottom:15px;">
                    <strong>💡 功能说明：</strong><br>
                    自动从 DuckDuckGo 搜索并下载真实生活场景图片，批量测试后自动进行错误聚类分析，并生成训练数据。
                </p>
                
                <div style="margin-bottom:15px;">
                    <label style="display:block; font-weight:bold; margin-bottom:8px; color:#333;">关键词列表（每行一个）：</label>
                    <textarea id="autoSearchKeywords" placeholder="电梯&#10;斑马线&#10;公交站牌&#10;危险施工区&#10;公园入口&#10;人行道" 
                              style="width:100%; padding:10px; border:1px solid #ddd; border-radius:4px; min-height:100px; font-size:14px;"></textarea>
                </div>
                
                <div style="margin-bottom:15px;">
                    <label for="autoSearchCount" style="display:block; font-weight:bold; margin-bottom:8px; color:#333;">每个关键词下载数量：</label>
                    <input id="autoSearchCount" type="number" value="10" min="1" max="50" 
                           style="max-width:200px; padding:8px; border:1px solid #ddd; border-radius:4px;">
                </div>
                
                <div style="display:flex; gap:10px; margin-bottom:15px;">
                    <button id="btnAutoSearchImages" class="btn btn-primary" style="flex:1; padding:12px; font-size:14px;">🔍 自动搜索并下载图片</button>
                    <button id="btnRunBatchWithClustering" class="btn btn-success" style="flex:1; padding:12px; font-size:14px;">🚀 批量测试 + 错误聚类</button>
                </div>
                
                <div id="autoSearchProgress" style="margin-top:15px; color:#666; font-size:14px;"></div>
                <div id="autoSearchResults" style="margin-top:15px; display:none;">
                    <h5 style="margin-bottom:10px; color:#333;">📊 搜索结果：</h5>
                    <div id="autoSearchResultsContent" style="font-size:13px; color:#495057;"></div>
                </div>
            </div>
            
            <!-- 批量自动测试（v3 / v4 / v5） -->
            <hr style="margin-top:40px; margin-bottom:20px; border-top:2px solid #ddd;" />
            <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">📊 批量自动测试（v3 / v4 / v5）</h3>
            <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:8px; padding:20px; margin-bottom:20px;">
                <p style="font-size:14px; color:#495057; margin-bottom:15px;">
                    说明：从本地 <code style="background:#e9ecef; padding:2px 6px; border-radius:3px;">test_images/&lt;keyword&gt;/</code> 读取图片，批量调用 Luna 场景描述，自动统计准确率，并聚类错误样本。
                </p>
                
                <div style="margin-bottom:15px;">
                    <label style="display:block; font-weight:bold; margin-bottom:8px; color:#333;">选择要测试的关键词：</label>
                    <div id="batchKeywordList" style="display:flex; flex-wrap:wrap; gap:8px;">
                        <!-- 由 JS 动态填充 -->
                    </div>
                </div>
                
                <div style="margin-bottom:15px;">
                    <label for="batchCount" style="display:block; font-weight:bold; margin-bottom:8px; color:#333;">每类测试张数（空=全部）：</label>
                    <input id="batchCount" type="number" style="max-width:200px; padding:8px; border:1px solid #ddd; border-radius:4px;" min="1" placeholder="例如 20">
                </div>
                
                <button id="btnRunBatchTest" class="btn btn-primary" style="width:100%; padding:15px; font-size:16px; margin-bottom:15px;">🚀 开始批量测试</button>
                
                <div id="batchProgress" style="margin-top:15px; color:#666; font-size:14px;"></div>
                
                <div id="batchSummary" style="margin-top:20px; display:none;">
                    <h4 style="margin-bottom:15px; color:#333;">📈 整体指标</h4>
                    <p id="batchSummaryText" style="font-size:14px; color:#495057; margin-bottom:20px;"></p>
                    
                    <h5 style="margin-bottom:10px; color:#333;">按关键词统计</h5>
                    <table style="width:100%; border-collapse:collapse; margin-bottom:20px;">
                        <thead>
                            <tr style="background:#e9ecef;">
                                <th style="padding:10px; text-align:left; border:1px solid #dee2e6;">关键词</th>
                                <th style="padding:10px; text-align:center; border:1px solid #dee2e6;">样本数</th>
                                <th style="padding:10px; text-align:center; border:1px solid #dee2e6;">命中数</th>
                                <th style="padding:10px; text-align:center; border:1px solid #dee2e6;">准确率</th>
                            </tr>
                        </thead>
                        <tbody id="batchPerKeywordBody"></tbody>
                    </table>
                    
                    <h5 style="margin-bottom:10px; color:#333;">🔍 错误聚类（v5）</h5>
                    <div id="batchErrorClusters" style="background:#fff3cd; border:1px solid #ffc107; border-radius:5px; padding:15px;"></div>
                </div>
            </div>
        </div>
        
        <!-- v1.1 + v1.2 + v1.3: 浏览器 UI 自动测试面板 -->
        <hr style="margin-top:40px; margin-bottom:20px; border-top:2px solid #ddd;" />
        <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">🎯 自动场景测试 v1.1</h3>
        <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:8px; padding:20px; margin-bottom:20px;">
            <div class="mb-2">
                <label class="form-label" style="display:block; font-weight:bold; margin-bottom:8px;">测试关键词</label>
                <input id="autoTestKeyword" class="form-control" placeholder="例如：斑马线 / 电梯入口 / 商场入口" style="padding:10px; border:1px solid #ddd; border-radius:4px;">
            </div>
            <div class="mb-2">
                <label class="form-label" style="display:block; font-weight:bold; margin-bottom:8px;">上传测试图片</label>
                <input id="autoTestImage" type="file" accept="image/*" class="form-control" style="padding:10px; border:1px solid #ddd; border-radius:4px;">
            </div>
            <button id="btnRunAutoTest" class="btn btn-primary mt-2" style="width:100%; padding:12px; font-size:16px;">运行自动测试</button>
            
            <div class="row mt-3">
                <div class="col">
                    <h5 style="font-size:16px; margin-bottom:10px;">匹配成功（AI判断正确）</h5>
                    <ul id="matchList" class="list-group" style="max-height:240px;overflow:auto; list-style:none; padding:0;"></ul>
                </div>
                <div class="col">
                    <h5 style="font-size:16px; margin-bottom:10px;">匹配失败（AI可能错误，需要人工校对）</h5>
                    <ul id="failList" class="list-group" style="max-height:240px;overflow:auto; list-style:none; padding:0;"></ul>
                </div>
            </div>
            
            <h4 class="mt-3" style="font-size:18px; margin-top:20px;">人工校对区</h4>
            <div id="reviewBox" style="display:none; margin-top:15px; padding:15px; background:#fff; border:1px solid #ddd; border-radius:8px;">
                <img id="reviewImg" style="max-width:60%;border:1px solid #ccc; border-radius:4px;" />
                <p id="reviewDesc" class="mt-2" style="margin-top:10px; font-size:14px;"></p>
                <p id="reviewMeta" class="text-muted" style="font-size:12px; color:#666; margin-top:5px;"></p>
                <button id="btnMarkCorrect" class="btn btn-success me-2" style="margin-top:10px; padding:8px 16px;">AI判断正确</button>
                <button id="btnMarkWrong" class="btn btn-danger" style="margin-top:10px; padding:8px 16px;">AI判断错误（加入训练集）</button>
            </div>
            <button id="btnExportCSV" class="btn btn-dark mt-3" style="width:100%; padding:12px; font-size:16px;">导出 CSV（当前结果）</button>
        </div>
        
        <!-- v1.2: 视频自动测试 -->
        <hr style="margin-top:40px; margin-bottom:20px; border-top:2px solid #ddd;" />
        <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">🎬 视频自动测试 v1.2</h3>
        <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:8px; padding:20px; margin-bottom:20px;">
            <div class="mb-2">
                <label style="display:block; font-weight:bold; margin-bottom:8px;">测试关键词（例如：斑马线 / 电梯入口）</label>
                <input id="videoTestKeyword" class="form-control" style="padding:10px; border:1px solid #ddd; border-radius:4px;">
            </div>
            <div class="mb-2">
                <label style="display:block; font-weight:bold; margin-bottom:8px;">上传测试视频（短视频即可）</label>
                <input id="videoTestFile" type="file" accept="video/*" class="form-control" style="padding:10px; border:1px solid #ddd; border-radius:4px;">
            </div>
            <button id="btnRunVideoTest" class="btn btn-secondary mt-2" style="width:100%; padding:12px; font-size:16px;">运行视频自动测试</button>
            <div id="videoTestResult" class="mt-3 small text-muted" style="margin-top:15px; font-size:14px; color:#666;"></div>
        </div>
        
        <!-- v1.3: 场景 Playlist 自动测试 -->
        <hr style="margin-top:40px; margin-bottom:20px; border-top:2px solid #ddd;" />
        <h3 class="mt-4" style="margin-top: 30px; margin-bottom: 15px;">📋 场景 Playlist 自动测试 v1.3</h3>
        <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:8px; padding:20px; margin-bottom:20px;">
            <div class="mb-2">
                <label style="display:block; font-weight:bold; margin-bottom:8px;">场景列表（逗号分隔）</label>
                <textarea id="playlistKeywords" class="form-control" rows="3" style="padding:10px; border:1px solid #ddd; border-radius:4px;">斑马线,红绿灯,人行道,盲道,道路施工,台阶,坡道,公交站牌,地铁入口,自动扶梯,电梯入口,商场入口,医院挂号大厅,医院科室门牌,小区大门,小区停车场,小区道路</textarea>
            </div>
            <div class="mb-2">
                <label style="display:block; font-weight:bold; margin-bottom:8px;">每个场景测试次数（使用当前上传的图片）</label>
                <input id="playlistCount" type="number" value="3" class="form-control" style="max-width:200px; padding:10px; border:1px solid #ddd; border-radius:4px;">
            </div>
            <button id="btnRunPlaylist" class="btn btn-warning mt-2" style="width:100%; padding:12px; font-size:16px;">运行 Playlist 测试（基于当前图片）</button>
            <div id="playlistResult" class="mt-3 small" style="margin-top:15px; font-size:14px;"></div>
        </div>
        
        <!-- 离线导航标签页 -->
        <div id="navigation-tab" class="tab-content">
            <div style="background:#e7f3ff; border:1px solid #2196F3; border-radius:8px; padding:15px; margin-bottom:15px; font-size:14px; color:#1976D2;">
                <strong>🧭 离线导航功能：</strong><br>
                • 完全离线工作，无需WiFi连接<br>
                • 基于本地地图数据和场景记忆<br>
                • 支持路径规划、导航控制、位置更新<br>
                <strong style="color:#d32f2f; margin-top:8px; display:block;">🔊 实时语音播报：</strong><br>
                • 自动播报转弯提示（"前方XX米到达XX"）<br>
                • 检测到障碍时自动播报警告（"请注意，前方有台阶"）<br>
                • 到达目的地时播报完成提示<br>
                • 建议：先规划路径，再开始导航，然后定期更新位置
            </div>
            
            <h3 style="margin-bottom: 15px;">路径规划</h3>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">起点：</label>
                <input type="text" id="navStart" placeholder="例如：挂号处" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">目的地（多个用逗号分隔）：</label>
                <input type="text" id="navDestinations" placeholder="例如：检查室,报告领取" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <button id="planRouteBtn" class="btn btn-primary">🗺️ 规划路径</button>
            <button id="loadPathsBtn" class="btn btn-secondary">📋 查看可用路径</button>
            
            <h3 style="margin-top: 30px; margin-bottom: 15px;">导航控制</h3>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">目的地：</label>
                <input type="text" id="navDestination" placeholder="例如：检查室" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <button id="startNavBtn" class="btn btn-success" style="flex:1;">▶️ 开始导航</button>
                <button id="pauseNavBtn" class="btn btn-secondary" style="flex:1;">⏸️ 暂停</button>
            </div>
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <button id="resumeNavBtn" class="btn btn-secondary" style="flex:1;">▶️ 恢复</button>
                <button id="cancelNavBtn" class="btn btn-danger" style="flex:1;">❌ 取消</button>
            </div>
            <button id="completeNavBtn" class="btn btn-success">✅ 完成导航</button>
            <button id="getNavStatusBtn" class="btn btn-secondary">📊 查看状态</button>
            
            <h3 style="margin-top: 30px; margin-bottom: 15px;">位置更新（GPS模拟）</h3>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">纬度：</label>
                <input type="number" id="navLat" placeholder="例如：31.2304" step="0.0001" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">经度：</label>
                <input type="number" id="navLng" placeholder="例如：121.4737" step="0.0001" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <button id="updatePositionBtn" class="btn btn-primary">📍 更新位置</button>
            <button id="getCurrentLocationBtn" class="btn btn-secondary">🌍 获取当前位置（需要GPS权限）</button>
        </div>
        
        <!-- 日志管理标签页 -->
        <div id="logs-tab" class="tab-content">
            <div style="background:#e7f3ff; border:1px solid #2196F3; border-radius:8px; padding:15px; margin-bottom:15px; font-size:14px; color:#1976D2;">
                <strong>📊 日志管理功能：</strong><br>
                • 自动记录所有API调用和功能使用情况<br>
                • 实时查看最新日志（自动刷新）<br>
                • 查看日志统计信息（按来源、级别、意图分类）<br>
                • 上传日志到后台进行分析<br>
                • 下载日志文件（JSON格式）
            </div>
            
            <h3 style="margin-bottom: 15px;">实时日志</h3>
            <div style="margin-bottom: 15px;">
                <button class="btn btn-success" id="startRealtimeLogsBtn" style="width:100%; margin-bottom:10px;">▶️ 开始实时日志</button>
                <button class="btn btn-danger" id="stopRealtimeLogsBtn" style="width:100%; margin-bottom:10px; display:none;">⏹️ 停止实时日志</button>
                <div id="realtimeLogsContainer" style="display:none; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:15px; max-height:400px; overflow-y:auto; font-family:monospace; font-size:12px;">
                    <div id="realtimeLogsContent" style="line-height:1.6;"></div>
                </div>
            </div>
            
            <h3 style="margin-bottom: 15px;">日志操作</h3>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:8px; font-weight:bold;">日期（可选，格式：YYYY-MM-DD）：</label>
                <input type="date" id="logDate" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            </div>
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <button id="viewLogsBtn" class="btn btn-primary" style="flex:1;">📋 查看日志</button>
                <button id="getLogStatsBtn" class="btn btn-success" style="flex:1;">📊 统计信息</button>
            </div>
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <button id="uploadLogsBtn" class="btn btn-success" style="flex:1;">📤 上传日志</button>
                <button id="downloadLogsBtn" class="btn btn-secondary" style="flex:1;">💾 下载日志</button>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px;">正在处理中...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result-section" id="resultSection">
            <div class="result-title">检测结果</div>
            <div id="results"></div>
        </div>
    </div>

    <script>
        // 全局错误处理 - 确保错误不会阻止页面运行
        window.addEventListener('error', function(e) {
            console.error('全局JavaScript错误:', e.error, e.message, e.filename, e.lineno);
            // 显示错误到页面
            try {
                const errorDiv = document.getElementById('error');
                if (errorDiv) {
                    errorDiv.textContent = 'JavaScript错误: ' + (e.message || '未知错误');
                    errorDiv.classList.add('active');
                }
            } catch (err) {
                console.error('无法显示错误:', err);
            }
            
            // 记录到统一日志（如果存在）
            if (window.lunaLog) {
                window.lunaLog('error', 'JavaScript错误', {
                    message: e.message,
                    filename: e.filename,
                    lineno: e.lineno,
                    error: e.error ? e.error.toString() : '未知错误'
                });
            }
            
            // 触发情绪事件（如果存在）
            if (window.emotion_event) {
                window.emotion_event('system_error', 'high', {
                    type: 'javascript_error',
                    message: e.message,
                    filename: e.filename,
                    lineno: e.lineno
                });
            }
        });
        
        // Promise未捕获错误处理（规范要求）
        window.addEventListener('unhandledrejection', function(e) {
            console.error('未捕获的Promise错误:', e.reason);
            // 显示错误到页面
            try {
                const errorDiv = document.getElementById('error');
                if (errorDiv) {
                    errorDiv.textContent = 'Promise错误: ' + (e.reason?.message || e.reason || '未知错误');
                    errorDiv.classList.add('active');
                }
            } catch (err) {
                console.error('无法显示错误:', err);
            }
            
            // 记录到统一日志（如果存在）
            if (window.lunaLog) {
                window.lunaLog('error', '未捕获的Promise错误', {
                    reason: e.reason?.message || String(e.reason),
                    error: e.reason
                });
            }
            
            // 触发情绪事件（如果存在）
            if (window.emotion_event) {
                window.emotion_event('system_error', 'high', {
                    type: 'unhandled_promise_rejection',
                    reason: e.reason?.message || String(e.reason)
                });
            }
            
            // 阻止默认行为（避免在控制台显示）
            e.preventDefault();
        });
        
        // 确保页面加载完成
        console.log('✅ JavaScript开始执行');
        
        let stream = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let currentImageBlob = null;
        let productModeActive = false;  // 产品模式状态
        // ✅ 完整产品模式状态变量
        let isWelcomePlayed = false;  // 欢迎语音是否已播放
        let hasStartedOnce = false;   // 是否已启动过一次
        let isProductModeRunning = false;  // 产品模式是否正在运行
        
        // ========== 全局定时器管理（规范要求）==========
        window.__intervals = window.__intervals || {};
        
        // 清理所有定时器的函数
        function clearAllIntervals() {
            Object.keys(window.__intervals).forEach(key => {
                if (window.__intervals[key]) {
                    clearInterval(window.__intervals[key]);
                    delete window.__intervals[key];
                }
            });
        }
        
        // 页面卸载时清理所有定时器
        window.addEventListener('beforeunload', () => {
            clearAllIntervals();
        });
        
        // ========== 统一事件绑定系统（规范要求：移除HTML内联onclick）==========
        /**
         * 统一的事件绑定函数
         * 在DOMContentLoaded时绑定所有事件，替代HTML内联onclick
         */
        function setupEventListeners() {
            // 测试按钮
            const testJsButton = document.getElementById('testJsButton');
            if (testJsButton) {
                testJsButton.addEventListener('click', () => {
                    alert('✅ JavaScript工作正常！');
                    console.log('测试按钮被点击');
                });
            }
            
            // Tab切换按钮（使用data-tab属性）
            document.querySelectorAll('.tab[data-tab]').forEach(btn => {
                const tabId = btn.getAttribute('data-tab');
                if (tabId) {
                    btn.addEventListener('click', (e) => {
                        switchTab(tabId, e);
                    });
                }
            });
            
            // 产品模式按钮
            const startProductModeBtn = document.getElementById('startProductModeBtn');
            if (startProductModeBtn) {
                startProductModeBtn.addEventListener('click', () => {
                    startProductMode();
                });
            }
            
            const stopProductModeBtn = document.getElementById('stopProductModeBtn');
            if (stopProductModeBtn) {
                stopProductModeBtn.addEventListener('click', () => {
                    stopProductMode();
                });
            }
            
            // 视觉识别按钮
            const startCameraBtn = document.getElementById('startCameraBtn');
            if (startCameraBtn) {
                startCameraBtn.addEventListener('click', () => {
                    startCamera();
                });
            }
            
            const captureBtn = document.getElementById('captureBtn');
            if (captureBtn) {
                captureBtn.addEventListener('click', () => {
                    capturePhoto();
                });
            }
            
            const stopBtn = document.getElementById('stopBtn');
            if (stopBtn) {
                stopBtn.addEventListener('click', () => {
                    stopCamera();
                });
            }
            
            // 文件选择
            const fileInput = document.getElementById('fileInput');
            if (fileInput) {
                fileInput.addEventListener('change', (e) => {
                    handleFileSelect(e);
                });
            }
            
            // 检测功能按钮
            const testButtonMap = {
                'testStepBtn': testStepDetection,
                'testSignboardBtn': testSignboardDetection,
                'testHazardBtn': testHazardDetection,
                'testFacilityBtn': testFacilityDetection,
                'testTrafficLightBtn': testTrafficLightDetection,
                'testCrowdDensityBtn': testCrowdDensityDetection,
                'testQueueBtn': testQueueDetection,
                'testDoorplateBtn': testDoorplateDetection
            };
            
            Object.keys(testButtonMap).forEach(btnId => {
                const btn = document.getElementById(btnId);
                if (btn && typeof testButtonMap[btnId] === 'function') {
                    btn.addEventListener('click', () => {
                        testButtonMap[btnId]();
                    });
                }
            });
            
            // 视觉导航按钮
            const startVisualNavBtn = document.getElementById('startVisualNavBtn');
            if (startVisualNavBtn) {
                startVisualNavBtn.addEventListener('click', () => {
                    startVisualNavigation();
                });
            }
            
            const stopVisualNavBtn = document.getElementById('stopVisualNavBtn');
            if (stopVisualNavBtn) {
                stopVisualNavBtn.addEventListener('click', () => {
                    stopVisualNavigation();
                });
            }
            
            // 语音功能按钮
            const startRecordBtn = document.getElementById('startRecordBtn');
            if (startRecordBtn) {
                startRecordBtn.addEventListener('click', () => {
                    startRecording();
                });
            }
            
            const stopRecordBtn = document.getElementById('stopRecordBtn');
            if (stopRecordBtn) {
                stopRecordBtn.addEventListener('click', () => {
                    stopRecording();
                });
            }
            
            // 音量控制按钮
            const volumeDownBtn = document.getElementById('volumeDownBtn');
            if (volumeDownBtn) {
                volumeDownBtn.addEventListener('click', () => {
                    adjustVolume(-0.1);
                });
            }
            
            const volumeUpBtn = document.getElementById('volumeUpBtn');
            if (volumeUpBtn) {
                volumeUpBtn.addEventListener('click', () => {
                    adjustVolume(0.1);
                });
            }
            
            // TTS测试按钮
            const ttsCheerfulBtn = document.getElementById('ttsCheerfulBtn');
            if (ttsCheerfulBtn) {
                ttsCheerfulBtn.addEventListener('click', () => {
                    testTTS('cheerful');
                });
            }
            
            const ttsCalmBtn = document.getElementById('ttsCalmBtn');
            if (ttsCalmBtn) {
                ttsCalmBtn.addEventListener('click', () => {
                    testTTS('calm');
                });
            }
            
            const ttsUrgentBtn = document.getElementById('ttsUrgentBtn');
            if (ttsUrgentBtn) {
                ttsUrgentBtn.addEventListener('click', () => {
                    testTTS('urgent');
                });
            }
            
            // 综合检测按钮
            // 自动百度抓图测试功能
            const btnShowKeywords = document.getElementById('btnShowKeywords');
            const keywordList = document.getElementById('keywordList');
            const btnAutoFetchTest = document.getElementById('btnAutoFetchTest');
            const autoTestImagePreview = document.getElementById('autoTestImagePreview');
            const autoTestResult = document.getElementById('autoTestResult');
            const autoTestResultContent = document.getElementById('autoTestResultContent');
            
            if (btnShowKeywords) {
                btnShowKeywords.onclick = async () => {
                    try {
                        const resp = await fetch("/api/auto/keyword_list");
                        const data = await resp.json();
                        if (data.success && keywordList) {
                            keywordList.innerHTML = "";
                            data.keywords.forEach(k => {
                                const o = document.createElement('option');
                                o.value = k;
                                o.textContent = k;
                                keywordList.appendChild(o);
                            });
                            alert("✅ 已加载 " + data.keywords.length + " 个关键词");
                        } else {
                            alert("❌ 加载关键词失败");
                        }
                    } catch (e) {
                        alert("❌ 加载关键词出错: " + e.message);
                        console.error("加载关键词错误:", e);
                    }
                };
            }
            
            if (btnAutoFetchTest) {
                btnAutoFetchTest.onclick = async () => {
                    if (!keywordList || !keywordList.value) {
                        alert("⚠️ 请先选择关键词！");
                        return;
                    }
                    
                    const kw = keywordList.value;
                    btnAutoFetchTest.disabled = true;
                    btnAutoFetchTest.textContent = "⏳ 正在抓取图片...";
                    
                    try {
                        // 1. 抓取图片
                        const resp = await fetch(`/api/auto/fetch_and_test/${encodeURIComponent(kw)}`);
                        const data = await resp.json();
                        
                        if (!data.success) {
                            alert("❌ 抓图失败：" + (data.error || "未知错误"));
                            btnAutoFetchTest.disabled = false;
                            btnAutoFetchTest.textContent = "🚀 自动抓图并测试";
                            return;
                        }
                        
                        // 2. 显示抓取的图片
                        if (autoTestImagePreview) {
                            autoTestImagePreview.src = "data:image/jpeg;base64," + data.image_base64;
                            autoTestImagePreview.style.display = "block";
                        }
                        
                        btnAutoFetchTest.textContent = "⏳ 正在测试场景描述...";
                        
                        // 3. 调用 Luna 场景描述
                        const descResp = await fetch("/api/navigation/describe_scene", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ image_base64: data.image_base64 }),
                        });
                        
                        const desc = await descResp.json();
                        console.log("场景描述结果：", desc);
                        
                        // 4. 显示结果
                        if (autoTestResult && autoTestResultContent) {
                            if (desc.success && desc.data) {
                                const result = desc.data;
                                let html = `<div style="margin-bottom:10px;"><strong>关键词：</strong>${kw}</div>`;
                                html += `<div style="margin-bottom:10px;"><strong>场景类型：</strong>${result.scene_type || "unknown"}</div>`;
                                html += `<div style="margin-bottom:10px;"><strong>场景标签：</strong>${(result.scene_tags || []).join(", ") || "无"}</div>`;
                                html += `<div style="margin-bottom:10px;"><strong>简短描述：</strong>${result.short_description || "无描述"}</div>`;
                                if (result.details && result.details.length > 0) {
                                    html += `<div style="margin-top:10px;"><strong>详细信息：</strong><ul style="margin-top:5px; padding-left:20px;">`;
                                    result.details.forEach(d => {
                                        html += `<li style="margin-bottom:5px;">${d}</li>`;
                                    });
                                    html += `</ul></div>`;
                                }
                                autoTestResultContent.innerHTML = html;
                                autoTestResult.style.display = "block";
                            } else {
                                autoTestResultContent.innerHTML = `<div style="color:#d32f2f;">❌ 场景描述失败：${desc.message || "未知错误"}</div>`;
                                autoTestResult.style.display = "block";
                            }
                        }
                        
                        btnAutoFetchTest.disabled = false;
                        btnAutoFetchTest.textContent = "🚀 自动抓图并测试";
                        
                    } catch (e) {
                        alert("❌ 测试出错: " + e.message);
                        console.error("自动测试错误:", e);
                        btnAutoFetchTest.disabled = false;
                        btnAutoFetchTest.textContent = "🚀 自动抓图并测试";
                    }
                };
            }
            
            // 自动测试结果分类功能
            async function runFullTest(keyword) {
                try {
                    const resp = await fetch(`/api/auto/run_full_test/${encodeURIComponent(keyword)}`);
                    const data = await resp.json();
                    
                    if (!data.success) {
                        alert("测试失败：" + (data.error || "未知错误"));
                        return;
                    }
                    
                    const li = document.createElement("li");
                    li.className = "list-group-item";
                    li.style.cssText = "padding:10px; margin-bottom:5px; background:white; border-radius:5px; cursor:pointer; border:1px solid #ddd; transition:background 0.2s;";
                    li.textContent = `${keyword} → ${data.description || "无描述"}`;
                    
                    // 把整个数据挂到 li 上也可以备用（V6）
                    li._autoData = data;
                    
                    // 鼠标悬停效果
                    li.onmouseenter = () => { li.style.background = "#f0f0f0"; };
                    li.onmouseleave = () => { li.style.background = "white"; };
                    
                    // 点击进入人工校对界面
                    li.onclick = () => {
                        const reviewData = li._autoData || data;
                        const reviewImg = document.getElementById("reviewImg");
                        const reviewDesc = document.getElementById("reviewDesc");
                        const reviewBox = document.getElementById("reviewBox");
                        const clusterInput = document.getElementById("clusterInput");
                        
                        if (reviewImg) {
                            reviewImg.src = "data:image/jpeg;base64," + reviewData.image_base64;
                        }
                        if (reviewDesc) {
                            reviewDesc.textContent = `关键词：${keyword}\n描述：${reviewData.description || "无描述"}\n匹配状态：${reviewData.match ? "✅ 匹配" : "❌ 不匹配"}\n命中词：${reviewData.hit || "无"}`;
                        }
                        if (clusterInput) {
                            clusterInput.value = "";  // 清空之前的输入
                        }
                        if (reviewBox) {
                            reviewBox.style.display = "block";
                            // 滚动到校对区域
                            reviewBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
                        }
                        
                        window.currentReview = reviewData;
                    };
                    
                    // 添加到对应的列表
                    if (data.match) {
                        const matchList = document.getElementById("matchList");
                        if (matchList) {
                            matchList.appendChild(li);
                        }
                    } else {
                        const failList = document.getElementById("failList");
                        if (failList) {
                            failList.appendChild(li);
                        }
                    }
                } catch (e) {
                    alert("运行测试出错: " + e.message);
                    console.error("runFullTest 错误:", e);
                }
            }
            
            // 修改 btnAutoFetchTest 按钮，使其调用 runFullTest
            if (btnAutoFetchTest) {
                btnAutoFetchTest.onclick = async () => {
                    if (!keywordList || !keywordList.value) {
                        alert("⚠️ 请先选择关键词！");
                        return;
                    }
                    
                    const kw = keywordList.value;
                    btnAutoFetchTest.disabled = true;
                    btnAutoFetchTest.textContent = "⏳ 正在测试...";
                    
                    await runFullTest(kw);
                    
                    btnAutoFetchTest.disabled = false;
                    btnAutoFetchTest.textContent = "🚀 自动抓图并测试";
                };
            }
            
            // 人工校对按钮逻辑（V6：统一封装保存训练样本）
            async function saveTrainingSample(humanLabel) {
                const d = window.currentReview;
                if (!d) {
                    alert("⚠️ 当前没有选中的样本");
                    return;
                }

                const clusterInput = document.getElementById("clusterInput");
                const cluster = clusterInput ? clusterInput.value || "" : "";

                const payload = {
                    keyword: d.keyword,
                    description: d.description || "",
                    match_auto: d.match || false,       // 自动判断是否匹配
                    human_label: humanLabel,   // "correct" / "wrong"
                    image_base64: d.image_base64 || "",
                    hit: d.hit || null,
                    cluster: cluster,
                    note: ""                   // 如有需要，后面可以加一个 textarea
                };

                try {
                    const resp = await fetch("/api/auto/training_samples/add", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(payload)
                    });
                    const res = await resp.json();

                    if (!res.success) {
                        alert("❌ 保存失败：" + (res.error || "未知错误"));
                        return;
                    }

                    if (humanLabel === "correct") {
                        alert("✅ 已记录：AI判断正确（用于统计对的比例）");
                    } else {
                        alert("✅ 已记录：AI判断错误（已加入训练样本）");
                    }
                    
                    // 清空输入框
                    if (clusterInput) clusterInput.value = "";
                } catch (e) {
                    console.error(e);
                    alert("❌ 网络或服务器错误，保存失败");
                }
            }

            const btnMarkCorrect = document.getElementById("btnMarkCorrect");
            const btnMarkWrong = document.getElementById("btnMarkWrong");
            
            if (btnMarkCorrect) {
                btnMarkCorrect.onclick = () => {
                    saveTrainingSample("correct");
                };
            }
            
            if (btnMarkWrong) {
                btnMarkWrong.onclick = () => {
                    saveTrainingSample("wrong");
                };
            }
            
            // CSV 导出功能（V6：调用后端统一导出训练样本）
            const btnExportCSV = document.getElementById("btnExportCSV");
            if (btnExportCSV) {
                btnExportCSV.onclick = async () => {
                    try {
                        const resp = await fetch("/api/auto/training_samples/export?format=csv");
                        if (!resp.ok) {
                            alert("❌ 导出失败：" + resp.status);
                            return;
                        }
                        const csvText = await resp.text();

                        const blob = new Blob([csvText], {type: "text/csv;charset=utf-8;"});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "luna_training_samples.csv";
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(url);
                        
                        alert("✅ 训练样本已导出到 CSV");
                    } catch (e) {
                        console.error(e);
                        alert("❌ 导出失败：" + e.message);
                    }
                };
            }
            
            // ====== 批量自动测试：加载可用关键词 ======
            async function loadBatchKeywords() {
                try {
                    const resp = await fetch('/api/auto/keywords');
                    const data = await resp.json();
                    if (!data.success) return;

                    const container = document.getElementById('batchKeywordList');
                    if (!container) return;
                    container.innerHTML = '';

                    data.keywords.forEach(kw => {
                        const label = document.createElement('label');
                        label.style.cssText = "display:inline-flex; align-items:center; padding:6px 12px; margin:4px; background:#e9ecef; border:1px solid #ced4da; border-radius:4px; cursor:pointer; font-size:14px;";
                        
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.value = kw;
                        checkbox.style.cssText = "margin-right:6px; cursor:pointer;";
                        
                        label.appendChild(checkbox);
                        label.appendChild(document.createTextNode(kw));
                        container.appendChild(label);
                    });
                } catch (e) {
                    console.error('加载关键词失败', e);
                }
            }

            // 页面初始化时加载一次
            if (document.getElementById('batchKeywordList')) {
                loadBatchKeywords();
            }

            // ====== 批量自动测试：执行 ======
            const btnRunBatchTest = document.getElementById('btnRunBatchTest');
            if (btnRunBatchTest) {
                btnRunBatchTest.onclick = async () => {
                    const container = document.getElementById('batchKeywordList');
                    if (!container) return;
                    
                    const checked = Array.from(container.querySelectorAll('input[type=checkbox]:checked'))
                        .map(c => c.value);

                    if (checked.length === 0) {
                        alert('⚠️ 请至少选择一个关键词');
                        return;
                    }

                    const countInput = document.getElementById('batchCount');
                    const maxPerKeyword = countInput && countInput.value ? parseInt(countInput.value, 10) : null;

                    const progressEl = document.getElementById('batchProgress');
                    const summaryEl = document.getElementById('batchSummary');
                    
                    if (progressEl) progressEl.textContent = '⏳ 批量测试进行中...';
                    if (summaryEl) summaryEl.style.display = 'none';
                    
                    btnRunBatchTest.disabled = true;
                    btnRunBatchTest.textContent = "⏳ 测试中...";

                    try {
                        const resp = await fetch('/api/auto/run_batch_test', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                keywords: checked,
                                max_per_keyword: maxPerKeyword
                            })
                        });
                        const data = await resp.json();
                        if (!data.success) {
                            if (progressEl) progressEl.textContent = '❌ 批量测试失败：' + (data.error || '未知错误');
                            btnRunBatchTest.disabled = false;
                            btnRunBatchTest.textContent = "🚀 开始批量测试";
                            return;
                        }

                        renderBatchSummary(data.summary, data.error_clusters);
                    } catch (e) {
                        console.error(e);
                        if (progressEl) progressEl.textContent = '❌ 批量测试异常：' + e.message;
                    } finally {
                        btnRunBatchTest.disabled = false;
                        btnRunBatchTest.textContent = "🚀 开始批量测试";
                    }
                };
            }

            function renderBatchSummary(summary, clusters) {
                const progress = document.getElementById('batchProgress');
                const box = document.getElementById('batchSummary');
                const text = document.getElementById('batchSummaryText');
                const tbody = document.getElementById('batchPerKeywordBody');
                const clusterBox = document.getElementById('batchErrorClusters');

                if (!summary || summary.total === 0) {
                    if (progress) progress.textContent = '⚠️ 没有可用的测试样本，请确认本地 test_images 目录。';
                    if (box) box.style.display = 'none';
                    return;
                }

                if (progress) progress.textContent = '✅ 批量测试完成';
                if (box) box.style.display = 'block';

                const acc = (summary.accuracy * 100).toFixed(1);
                const prec = (summary.precision * 100).toFixed(1);
                const rec = (summary.recall * 100).toFixed(1);
                const f1 = (summary.f1 * 100).toFixed(1);

                if (text) {
                    text.textContent =
                        `总样本数：${summary.total}，命中数：${summary.matched}，` +
                        `准确率：${acc}% ，Precision：${prec}% ，Recall：${rec}% ，F1：${f1}%`;
                }

                // per keyword
                if (tbody) {
                    tbody.innerHTML = '';
                    Object.entries(summary.per_keyword || {}).forEach(([kw, v]) => {
                        const tr = document.createElement('tr');
                        const accKw = ((v.accuracy || 0) * 100).toFixed(1);
                        tr.innerHTML = `
                            <td style="padding:8px; border:1px solid #dee2e6;">${kw}</td>
                            <td style="padding:8px; text-align:center; border:1px solid #dee2e6;">${v.total}</td>
                            <td style="padding:8px; text-align:center; border:1px solid #dee2e6;">${v.matched}</td>
                            <td style="padding:8px; text-align:center; border:1px solid #dee2e6;">${accKw}%</td>
                        `;
                        tbody.appendChild(tr);
                    });
                }

                // error clusters
                if (clusterBox) {
                    clusterBox.innerHTML = '';
                    if (!clusters || clusters.length === 0) {
                        clusterBox.textContent = '✅ 暂时没有错误样本，Luna 在这些关键词上全部命中。';
                        return;
                    }

                    clusters.forEach(c => {
                        const div = document.createElement('div');
                        div.style.cssText = "margin-bottom:15px; padding:10px; background:white; border-radius:4px;";

                        const title = document.createElement('h6');
                        title.style.cssText = "margin-bottom:8px; color:#856404; font-size:14px; font-weight:bold;";
                        title.textContent = `${c.keyword}：${c.count} 个错误样本`;
                        div.appendChild(title);

                        const ul = document.createElement('ul');
                        ul.style.cssText = "margin:0; padding-left:20px; font-size:13px; color:#495057;";
                        (c.examples || []).forEach(ex => {
                            const li = document.createElement('li');
                            li.style.cssText = "margin-bottom:5px;";
                            li.textContent = `${ex.file} → ${ex.description || '（无描述）'}`;
                            ul.appendChild(li);
                        });
                        div.appendChild(ul);

                        clusterBox.appendChild(div);
                    });
                }
            }
            
            // ====== V6.1：自动搜图 + 错误聚类 ======
            const btnAutoSearchImages = document.getElementById('btnAutoSearchImages');
            const btnRunBatchWithClustering = document.getElementById('btnRunBatchWithClustering');
            const autoSearchKeywords = document.getElementById('autoSearchKeywords');
            const autoSearchCount = document.getElementById('autoSearchCount');
            const autoSearchProgress = document.getElementById('autoSearchProgress');
            const autoSearchResults = document.getElementById('autoSearchResults');
            const autoSearchResultsContent = document.getElementById('autoSearchResultsContent');
            
            if (btnAutoSearchImages) {
                btnAutoSearchImages.onclick = async () => {
                    if (!autoSearchKeywords || !autoSearchKeywords.value.trim()) {
                        alert('⚠️ 请输入关键词列表');
                        return;
                    }
                    
                    const keywords = autoSearchKeywords.value.split('\n')
                        .map(k => k.trim())
                        .filter(k => k.length > 0);
                    
                    if (keywords.length === 0) {
                        alert('⚠️ 请输入至少一个关键词');
                        return;
                    }
                    
                    const maxPerKeyword = parseInt(autoSearchCount?.value || '10', 10);
                    
                    btnAutoSearchImages.disabled = true;
                    btnAutoSearchImages.textContent = '⏳ 正在搜索并下载图片...';
                    if (autoSearchProgress) autoSearchProgress.textContent = `正在处理 ${keywords.length} 个关键词...`;
                    
                    try {
                        const resp = await fetch('/api/auto/auto_search_images', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                keywords: keywords,
                                max_per_keyword: maxPerKeyword
                            })
                        });
                        
                        const data = await resp.json();
                        
                        if (!data.success) {
                            alert('❌ 搜索失败：' + (data.error || '未知错误'));
                            return;
                        }
                        
                        if (autoSearchProgress) {
                            autoSearchProgress.textContent = `✅ 成功下载 ${data.total_downloaded} 张图片`;
                        }
                        
                        if (autoSearchResults && autoSearchResultsContent) {
                            let html = `<div style="margin-bottom:10px;"><strong>总计下载：</strong>${data.total_downloaded} 张</div>`;
                            html += '<ul style="margin:0; padding-left:20px;">';
                            Object.entries(data.results || {}).forEach(([kw, info]) => {
                                html += `<li style="margin-bottom:5px;">${kw}：${info.count} 张</li>`;
                            });
                            html += '</ul>';
                            autoSearchResultsContent.innerHTML = html;
                            autoSearchResults.style.display = 'block';
                        }
                    } catch (e) {
                        console.error(e);
                        alert('❌ 搜索出错：' + e.message);
                    } finally {
                        btnAutoSearchImages.disabled = false;
                        btnAutoSearchImages.textContent = '🔍 自动搜索并下载图片';
                    }
                };
            }
            
            if (btnRunBatchWithClustering) {
                btnRunBatchWithClustering.onclick = async () => {
                    if (!autoSearchKeywords || !autoSearchKeywords.value.trim()) {
                        alert('⚠️ 请先搜索并下载图片');
                        return;
                    }
                    
                    const keywords = autoSearchKeywords.value.split('\n')
                        .map(k => k.trim())
                        .filter(k => k.length > 0);
                    
                    if (keywords.length === 0) {
                        alert('⚠️ 请输入至少一个关键词');
                        return;
                    }
                    
                    const maxPerKeyword = parseInt(autoSearchCount?.value || '10', 10);
                    
                    btnRunBatchWithClustering.disabled = true;
                    btnRunBatchWithClustering.textContent = '⏳ 正在批量测试并聚类...';
                    if (autoSearchProgress) autoSearchProgress.textContent = '正在批量测试、聚类分析、生成训练数据...';
                    
                    try {
                        const resp = await fetch('/api/auto/run_batch_with_clustering', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                keywords: keywords,
                                max_per_keyword: maxPerKeyword,
                                n_clusters: 3
                            })
                        });
                        
                        const data = await resp.json();
                        
                        if (!data.success) {
                            alert('❌ 批量测试失败：' + (data.error || '未知错误'));
                            return;
                        }
                        
                        if (autoSearchProgress) {
                            autoSearchProgress.textContent = `✅ 批量测试完成，已自动保存 ${data.auto_saved_samples || 0} 个错误样本到训练数据`;
                        }
                        
                        if (autoSearchResults && autoSearchResultsContent) {
                            let html = `<div style="margin-bottom:10px;"><strong>测试结果：</strong></div>`;
                            html += `<div style="margin-bottom:10px;">总样本数：${data.summary?.total || 0}，命中数：${data.summary?.matched || 0}，准确率：${((data.summary?.accuracy || 0) * 100).toFixed(1)}%</div>`;
                            html += `<div style="margin-bottom:10px;"><strong>错误聚类摘要：</strong></div>`;
                            
                            const clusters = data.clustering_summary?.clusters || [];
                            if (clusters.length > 0) {
                                html += '<ul style="margin:0; padding-left:20px;">';
                                clusters.forEach(c => {
                                    html += `<li style="margin-bottom:5px;">Cluster ${c.cluster_id}：${c.count} 个样本，关键词：${c.keywords.join(', ')}</li>`;
                                });
                                html += '</ul>';
                            } else {
                                html += '<div>暂无错误样本</div>';
                            }
                            
                            autoSearchResultsContent.innerHTML = html;
                            autoSearchResults.style.display = 'block';
                        }
                    } catch (e) {
                        console.error(e);
                        alert('❌ 批量测试出错：' + e.message);
                    } finally {
                        btnRunBatchWithClustering.disabled = false;
                        btnRunBatchWithClustering.textContent = '🚀 批量测试 + 错误聚类';
                    }
                };
            }
            
            // ====== v1.1: 浏览器 UI 自动测试面板 ======
            (function () {
                "use strict";
                
                const elKeyword = document.getElementById("autoTestKeyword");
                const elImage = document.getElementById("autoTestImage");
                const elBtnRun = document.getElementById("btnRunAutoTest");
                const elMatchList = document.getElementById("matchList");
                const elFailList = document.getElementById("failList");
                const elReviewBox = document.getElementById("reviewBox");
                const elReviewImg = document.getElementById("reviewImg");
                const elReviewDesc = document.getElementById("reviewDesc");
                const elReviewMeta = document.getElementById("reviewMeta");
                const btnMarkCorrect = document.getElementById("btnMarkCorrect");
                const btnMarkWrong = document.getElementById("btnMarkWrong");
                const btnExportCSV = document.getElementById("btnExportCSV");
                
                if (!elKeyword || !elImage || !elBtnRun) {
                    console.warn("[AutoTest] v1.1 元素未找到，跳过初始化");
                    return;
                }
                
                let reviewState = {
                    current: null,
                    records: []  // {keyword, description, match, human_review, ts}
                };
                
                function fileToBase64(file) {
                    return new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onload = () => resolve(reader.result);
                        reader.onerror = reject;
                        reader.readAsDataURL(file);
                    });
                }
                
                async function runAutoTestOnce() {
                    const kw = elKeyword.value.trim();
                    const file = elImage.files[0];
                    
                    if (!kw) {
                        alert("请输入测试关键词");
                        return;
                    }
                    if (!file) {
                        alert("请上传测试图片");
                        return;
                    }
                    
                    elBtnRun.disabled = true;
                    elBtnRun.textContent = "⏳ 测试中...";
                    
                    try {
                        const b64 = await fileToBase64(file);
                        
                        const resp = await fetch("/api/auto/run_full_test", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({
                                keyword: kw,
                                image_base64: b64
                            })
                        });
                        
                        const data = await resp.json();
                        if (!data.success) {
                            alert("自动测试失败: " + (data.error || "未知错误"));
                            return;
                        }
                        
                        const { keyword, description, match, hit_word } = data.data;
                        const li = document.createElement("li");
                        li.className = "list-group-item list-group-item-action";
                        li.style.cssText = "padding:10px; margin-bottom:5px; border:1px solid #ddd; border-radius:4px; cursor:pointer; background:#fff;";
                        li.textContent = `${keyword} → ${description || "(无描述)"}`;
                        
                        const record = {
                            keyword,
                            description,
                            match,
                            hit_word,
                            human_review: "pending",
                            ts: Date.now(),
                            image_base64: b64
                        };
                        
                        li.onclick = () => {
                            reviewState.current = record;
                            
                            elReviewImg.src = b64;
                            elReviewDesc.textContent = `描述：${description || "(无)"}`;
                            elReviewMeta.textContent = `关键词：${keyword} | 自动判断：${match ? "匹配" : "不匹配"} | 命中词：${hit_word || "无"}`;
                            elReviewBox.style.display = "block";
                        };
                        
                        reviewState.records.push(record);
                        
                        if (match) {
                            if (elMatchList) elMatchList.appendChild(li);
                        } else {
                            if (elFailList) elFailList.appendChild(li);
                        }
                        
                    } catch (e) {
                        console.error(e);
                        alert("运行自动测试时出错：" + e.message);
                    } finally {
                        elBtnRun.disabled = false;
                        elBtnRun.textContent = "运行自动测试";
                    }
                }
                
                elBtnRun.onclick = runAutoTestOnce;
                
                if (btnMarkCorrect) {
                    btnMarkCorrect.onclick = () => {
                        if (!reviewState.current) return;
                        reviewState.current.human_review = "correct";
                        alert("已标记：AI判断正确");
                    };
                }
                
                if (btnMarkWrong) {
                    btnMarkWrong.onclick = () => {
                        if (!reviewState.current) return;
                        reviewState.current.human_review = "wrong";
                        alert("已标记：AI判断错误，将加入训练集（后续导出 JSON/CSV 使用）");
                    };
                }
                
                if (btnExportCSV) {
                    btnExportCSV.onclick = () => {
                        const rows = [];
                        rows.push("keyword,description,match,human_review,timestamp");
                        reviewState.records.forEach(r => {
                            const line = [
                                (r.keyword || "").replace(/,/g, "；"),
                                (r.description || "").replace(/,/g, "；"),
                                r.match ? "match" : "fail",
                                r.human_review,
                                new Date(r.ts).toISOString()
                            ].join(",");
                            rows.push(line);
                        });
                        
                        const csv = rows.join("\n");
                        const blob = new Blob([csv], {type: "text/csv;charset=utf-8;"});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "luna_auto_test_results_v1_1.csv";
                        a.click();
                        URL.revokeObjectURL(url);
                    };
                }
                
                console.log("[AutoTest] v1.1 自动测试面板已初始化");
            })();
            
            // ====== v1.2: 视频自动测试 ======
            (function () {
                "use strict";
                
                const videoKw = document.getElementById("videoTestKeyword");
                const videoFile = document.getElementById("videoTestFile");
                const btnVideo = document.getElementById("btnRunVideoTest");
                const videoResult = document.getElementById("videoTestResult");
                
                if (!videoKw || !videoFile || !btnVideo || !videoResult) {
                    console.warn("[AutoTest] v1.2 视频测试元素未找到");
                    return;
                }
                
                async function runVideoTest() {
                    const kw = videoKw.value.trim();
                    const file = videoFile.files[0];
                    if (!kw || !file) {
                        alert("请填写关键词并选择视频文件");
                        return;
                    }
                    
                    const form = new FormData();
                    form.append("keyword", kw);
                    form.append("video_file", file);
                    
                    videoResult.textContent = "正在分析视频，请稍候...";
                    btnVideo.disabled = true;
                    
                    try {
                        const resp = await fetch("/api/auto/run_video_test", {
                            method: "POST",
                            body: form
                        });
                        const data = await resp.json();
                        if (!data.success) {
                            videoResult.textContent = "视频测试失败：" + (data.error || "未知错误");
                            return;
                        }
                        const d = data.data;
                        videoResult.textContent = `关键词：${d.keyword} | 总帧数：${d.total_frames} | 匹配帧：${d.match_frames} | 准确率：${(d.accuracy * 100).toFixed(1)}%`;
                    } catch (e) {
                        console.error(e);
                        videoResult.textContent = "视频测试异常：" + e.message;
                    } finally {
                        btnVideo.disabled = false;
                    }
                }
                
                btnVideo.onclick = runVideoTest;
                
                console.log("[AutoTest] v1.2 视频自动测试已初始化");
            })();
            
            // ====== v1.3: Playlist 自动测试 ======
            (function () {
                "use strict";
                
                const elPlaylistKeywords = document.getElementById("playlistKeywords");
                const elPlaylistCount = document.getElementById("playlistCount");
                const btnRunPlaylist = document.getElementById("btnRunPlaylist");
                const playlistResult = document.getElementById("playlistResult");
                const elImage = document.getElementById("autoTestImage"); // v1.1 里的
                
                if (!elPlaylistKeywords || !elPlaylistCount || !btnRunPlaylist || !playlistResult) {
                    console.warn("[AutoTest] v1.3 Playlist 测试元素未找到");
                    return;
                }
                
                async function playlistRun() {
                    const text = elPlaylistKeywords.value.trim();
                    const file = elImage ? elImage.files[0] : null;
                    const times = parseInt(elPlaylistCount.value || "1", 10);
                    
                    if (!text) {
                        alert("请填写场景列表");
                        return;
                    }
                    if (!file) {
                        alert("请先在上面的自动测试面板上传一张测试图片");
                        return;
                    }
                    if (!times || times <= 0) {
                        alert("次数必须大于0");
                        return;
                    }
                    
                    const keywords = text.split(/[,，]/).map(s => s.trim()).filter(Boolean);
                    const b64 = await new Promise((resolve, reject) => {
                        const r = new FileReader();
                        r.onload = () => resolve(r.result);
                        r.onerror = reject;
                        r.readAsDataURL(file);
                    });
                    
                    playlistResult.textContent = "正在运行 Playlist 测试...";
                    btnRunPlaylist.disabled = true;
                    
                    const summary = []; // {keyword, total, match}
                    
                    try {
                        for (const kw of keywords) {
                            let total = 0;
                            let matchCount = 0;
                            
                            for (let i = 0; i < times; i++) {
                                const resp = await fetch("/api/auto/run_full_test", {
                                    method: "POST",
                                    headers: {"Content-Type": "application/json"},
                                    body: JSON.stringify({keyword: kw, image_base64: b64})
                                });
                                const data = await resp.json();
                                if (!data.success) continue;
                                total += 1;
                                if (data.data.match) matchCount += 1;
                            }
                            
                            summary.push({keyword: kw, total, match: matchCount});
                        }
                        
                        playlistResult.innerHTML = `
                            <p style="margin-bottom:10px;"><strong>场景数：</strong>${summary.length} | <strong>每个场景测试次数：</strong>${times}</p>
                            <table class="table table-sm table-bordered" style="width:100%; border-collapse:collapse; font-size:13px;">
                                <thead><tr style="background:#e9ecef;"><th style="padding:8px; border:1px solid #ddd;">场景</th><th style="padding:8px; border:1px solid #ddd;">总次数</th><th style="padding:8px; border:1px solid #ddd;">匹配次数</th><th style="padding:8px; border:1px solid #ddd;">准确率</th></tr></thead>
                                <tbody>
                                    ${summary.map(s => `
                                        <tr>
                                            <td style="padding:8px; border:1px solid #ddd;">${s.keyword}</td>
                                            <td style="padding:8px; border:1px solid #ddd; text-align:center;">${s.total}</td>
                                            <td style="padding:8px; border:1px solid #ddd; text-align:center;">${s.match}</td>
                                            <td style="padding:8px; border:1px solid #ddd; text-align:center;">${s.total ? ((s.match / s.total) * 100).toFixed(1) + "%" : "-"}</td>
                                        </tr>
                                    `).join("")}
                                </tbody>
                            </table>
                        `;
                    } catch (e) {
                        console.error(e);
                        playlistResult.textContent = "Playlist 测试异常：" + e.message;
                    } finally {
                        btnRunPlaylist.disabled = false;
                    }
                }
                
                btnRunPlaylist.onclick = playlistRun;
                
                console.log("[AutoTest] v1.3 Playlist 自动测试已初始化");
            })();
            
            const comprehensiveDetectionBtn = document.getElementById('comprehensiveDetectionBtn');
            if (comprehensiveDetectionBtn) {
                comprehensiveDetectionBtn.addEventListener('click', () => {
                    comprehensiveDetection();
                });
            }
            
            // 导航功能按钮
            const planRouteBtn = document.getElementById('planRouteBtn');
            if (planRouteBtn) {
                planRouteBtn.addEventListener('click', () => {
                    planRoute();
                });
            }
            
            const loadPathsBtn = document.getElementById('loadPathsBtn');
            if (loadPathsBtn) {
                loadPathsBtn.addEventListener('click', () => {
                    loadAvailablePaths();
                });
            }
            
            const startNavBtn = document.getElementById('startNavBtn');
            if (startNavBtn) {
                startNavBtn.addEventListener('click', () => {
                    startNavigation();
                });
            }
            
            const pauseNavBtn = document.getElementById('pauseNavBtn');
            if (pauseNavBtn) {
                pauseNavBtn.addEventListener('click', () => {
                    pauseNavigation();
                });
            }
            
            const resumeNavBtn = document.getElementById('resumeNavBtn');
            if (resumeNavBtn) {
                resumeNavBtn.addEventListener('click', () => {
                    resumeNavigation();
                });
            }
            
            const cancelNavBtn = document.getElementById('cancelNavBtn');
            if (cancelNavBtn) {
                cancelNavBtn.addEventListener('click', () => {
                    cancelNavigation();
                });
            }
            
            const completeNavBtn = document.getElementById('completeNavBtn');
            if (completeNavBtn) {
                completeNavBtn.addEventListener('click', () => {
                    completeNavigation();
                });
            }
            
            const getNavStatusBtn = document.getElementById('getNavStatusBtn');
            if (getNavStatusBtn) {
                getNavStatusBtn.addEventListener('click', () => {
                    getNavigationStatus();
                });
            }
            
            // 位置功能按钮
            const updatePositionBtn = document.getElementById('updatePositionBtn');
            if (updatePositionBtn) {
                updatePositionBtn.addEventListener('click', () => {
                    updatePosition();
                });
            }
            
            const getCurrentLocationBtn = document.getElementById('getCurrentLocationBtn');
            if (getCurrentLocationBtn) {
                getCurrentLocationBtn.addEventListener('click', () => {
                    getCurrentLocation();
                });
            }
            
            // 日志功能按钮
            const startRealtimeLogsBtn = document.getElementById('startRealtimeLogsBtn');
            if (startRealtimeLogsBtn) {
                startRealtimeLogsBtn.addEventListener('click', () => {
                    startRealtimeLogs();
                });
            }
            
            const stopRealtimeLogsBtn = document.getElementById('stopRealtimeLogsBtn');
            if (stopRealtimeLogsBtn) {
                stopRealtimeLogsBtn.addEventListener('click', () => {
                    stopRealtimeLogs();
                });
            }
            
            const viewLogsBtn = document.getElementById('viewLogsBtn');
            if (viewLogsBtn) {
                viewLogsBtn.addEventListener('click', () => {
                    viewLogs();
                });
            }
            
            const getLogStatsBtn = document.getElementById('getLogStatsBtn');
            if (getLogStatsBtn) {
                getLogStatsBtn.addEventListener('click', () => {
                    getLogStatistics();
                });
            }
            
            const uploadLogsBtn = document.getElementById('uploadLogsBtn');
            if (uploadLogsBtn) {
                uploadLogsBtn.addEventListener('click', () => {
                    uploadLogs();
                });
            }
            
            const downloadLogsBtn = document.getElementById('downloadLogsBtn');
            if (downloadLogsBtn) {
                downloadLogsBtn.addEventListener('click', () => {
                    downloadLogs();
                });
            }
            
            // 其他按钮（通过data-action属性识别）
            document.querySelectorAll('[data-action]').forEach(btn => {
                const action = btn.getAttribute('data-action');
                if (action && typeof window[action] === 'function') {
                    btn.addEventListener('click', () => {
                        window[action]();
                    });
                }
            });
        }
        
        // 在DOM加载完成后设置事件监听器
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupEventListeners);
        } else {
            setupEventListeners();
        }
        
        // 全局音频上下文和音量控制
        let globalAudioContext = null;
        let currentAudioVolume = 1.0;  // 当前音量（0.0-1.0）
        let audioUnlocked = false;  // 音频是否已解锁（通过用户交互）
        
        // 初始化音频上下文（用于解锁音频播放）
        function initAudioContext() {
            try {
                if (!globalAudioContext) {
                    globalAudioContext = new (window.AudioContext || window.webkitAudioContext)();
                }
                return globalAudioContext;
            } catch (e) {
                console.warn('音频上下文初始化失败:', e);
                return null;
            }
        }
        
        // 解锁音频播放（需要在用户交互时调用）
        async function unlockAudio() {
            if (audioUnlocked) return true;
            
            try {
                const ctx = initAudioContext();
                if (!ctx) return false;
                
                // 创建静音音频并播放，用于解锁音频权限
                const buffer = ctx.createBuffer(1, 1, 22050);
                const source = ctx.createBufferSource();
                source.buffer = buffer;
                source.connect(ctx.destination);
                source.start(0);
                
                // 等待一小段时间确保音频已解锁
                await new Promise(resolve => setTimeout(resolve, 100));
                
                audioUnlocked = true;
                console.log('✅ 音频已解锁');
                return true;
            } catch (e) {
                console.warn('音频解锁失败:', e);
                return false;
            }
        }
        
        // 调整音量（全局函数，供按钮调用）- 必须先定义
        function adjustVolume(delta) {
            try {
                currentAudioVolume = Math.max(0.0, Math.min(1.0, currentAudioVolume + delta));
                
                // 更新所有正在播放的音频音量
                if (window.currentPlayingAudios) {
                    window.currentPlayingAudios.forEach(audio => {
                        if (audio && !audio.paused) {
                            audio.volume = currentAudioVolume;
                        }
                    });
                }
                
                // 更新音量显示
                const volumeDisplay = document.getElementById('volumeDisplay');
                if (volumeDisplay) {
                    volumeDisplay.textContent = Math.round(currentAudioVolume * 100) + '%';
                }
                
                // 显示音量提示
                if (typeof showVolumeIndicator === 'function') {
                    showVolumeIndicator(currentAudioVolume);
                }
                console.log(`🔊 音量: ${Math.round(currentAudioVolume * 100)}%`);
            } catch (e) {
                console.error('调整音量失败:', e);
            }
        }
        
        // 音量键事件监听（移动端）
        function setupVolumeControls() {
            try {
                // 监听音量键（通过媒体键事件）
                document.addEventListener('keydown', (e) => {
                    try {
                        // 音量上键（某些浏览器）
                        if (e.key === 'VolumeUp' || e.code === 'VolumeUp') {
                            e.preventDefault();
                            if (typeof adjustVolume === 'function') {
                                adjustVolume(0.1);
                            }
                        }
                        // 音量下键
                        else if (e.key === 'VolumeDown' || e.code === 'VolumeDown') {
                            e.preventDefault();
                            if (typeof adjustVolume === 'function') {
                                adjustVolume(-0.1);
                            }
                        }
                    } catch (err) {
                        console.error('音量键处理错误:', err);
                    }
                });
                
                // 注意：Media Session API 不支持音量控制动作（volumeup/volumedown）
                // 音量控制已通过键盘事件监听实现（见 setupVolumeControls 函数）
                // 如果需要媒体控制，可以使用支持的标准动作：'play', 'pause', 'nexttrack', 'previoustrack', 'seekbackward', 'seekforward'
                // if ('mediaSession' in navigator) {
                //     try {
                //         // 只设置支持的标准媒体动作
                //         // navigator.mediaSession.setActionHandler('play', () => { ... });
                //         // navigator.mediaSession.setActionHandler('pause', () => { ... });
                //     } catch (err) {
                //         console.warn('媒体会话API不支持:', err);
                //     }
                // }
                // 注意：不监听touchstart事件，避免干扰页面正常操作
            } catch (e) {
                console.error('设置音量控制失败:', e);
            }
        }
        
        // 显示音量指示器
        function showVolumeIndicator(volume) {
            const indicator = document.getElementById('volumeIndicator') || createVolumeIndicator();
            const percentage = Math.round(volume * 100);
            indicator.textContent = `🔊 ${percentage}%`;
            indicator.style.display = 'block';
            indicator.style.opacity = '1';
            
            setTimeout(() => {
                indicator.style.opacity = '0';
                setTimeout(() => {
                    indicator.style.display = 'none';
                }, 300);
            }, 1500);
        }
        
        // 创建音量指示器
        function createVolumeIndicator() {
            const indicator = document.createElement('div');
            indicator.id = 'volumeIndicator';
            indicator.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 20px 40px;
                border-radius: 10px;
                font-size: 24px;
                font-weight: bold;
                z-index: 10000;
                display: none;
                transition: opacity 0.3s;
                pointer-events: none;
            `;
            document.body.appendChild(indicator);
            return indicator;
        }
        
        // 初始化音频功能（延迟执行，避免阻塞页面）
        function initAudioFeatures() {
            try {
                // 延迟初始化，确保所有函数都已定义
                setTimeout(() => {
                    try {
                        if (typeof initAudioContext === 'function') {
                            initAudioContext();
                        }
                        if (typeof setupVolumeControls === 'function') {
                            setupVolumeControls();
                        }
                        
                        // 在用户首次交互时解锁音频
                        const unlockOnInteraction = () => {
                            try {
                                if (typeof unlockAudio === 'function') {
                                    unlockAudio();
                                }
                                document.removeEventListener('click', unlockOnInteraction);
                                document.removeEventListener('touchstart', unlockOnInteraction);
                            } catch (e) {
                                console.error('解锁音频失败:', e);
                            }
                        };
                        document.addEventListener('click', unlockOnInteraction, { once: true });
                        document.addEventListener('touchstart', unlockOnInteraction, { once: true });
                    } catch (e) {
                        console.error('初始化音频功能失败:', e);
                    }
                }, 200);
            } catch (e) {
                console.error('音频功能初始化失败:', e);
            }
        }
        
        // 在页面加载时初始化（简化版，避免阻塞页面）
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAudioFeatures);
        } else {
            // DOM已经加载完成
            setTimeout(initAudioFeatures, 100);
        }
        
        // 全局音频元素追踪
        window.currentPlayingAudios = window.currentPlayingAudios || [];
        let lastVoiceRecognitionTime = 0;  // 上次语音识别时间
        let lastLogTimestamp = null;  // 上次获取的日志时间戳
        
        // 获取DOM元素的辅助函数（延迟获取，避免在元素创建前访问）
        function getVideo() {
            return document.getElementById('video');
        }
        
        function getCanvas() {
            return document.getElementById('canvas');
        }
        
        // 为了兼容旧代码，保留变量引用（延迟初始化）
        let video = null;
        let canvas = null;
        
        function initDOMElements() {
            if (!video) video = getVideo();
            if (!canvas) canvas = getCanvas();
        }
        
        // 在DOM加载后初始化元素引用
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initDOMElements);
        } else {
            initDOMElements();
        }
        
        // 在使用video和canvas的函数中，确保它们已初始化
        function ensureDOMElements() {
            if (!video) video = getVideo();
            if (!canvas) canvas = getCanvas();
        }
        
        function switchTab(tabName, event) {
            // 确保函数暴露到全局作用域
            window.switchTab = switchTab;
            console.log('switchTab被调用:', tabName, event);
            // 防止默认行为
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
            try {
                // 移除所有标签的active状态
                const tabs = document.querySelectorAll('.tab');
                const contents = document.querySelectorAll('.tab-content');
                console.log('找到标签数:', tabs.length, '内容数:', contents.length);
                
                tabs.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                
                // 添加当前标签的active状态
                let clickedTab = null;
                if (event && event.target) {
                    clickedTab = event.target;
                    console.log('使用event.target');
                } else {
                    // 如果没有event对象，通过tabName查找对应的按钮
                    clickedTab = document.querySelector(`.tab[onclick*="${tabName}"]`);
                    console.log('通过选择器查找:', clickedTab);
                }
                
                if (clickedTab) {
                    clickedTab.classList.add('active');
                    console.log('标签已激活');
                } else {
                    console.warn('未找到对应的标签按钮');
                }
                
                // 显示对应的内容
                const contentId = tabName + '-tab';
                const content = document.getElementById(contentId);
                console.log('查找内容:', contentId, content);
                if (content) {
                    content.classList.add('active');
                    console.log('内容已显示');
                } else {
                    console.error('未找到内容区域:', contentId);
                }
            } catch (e) {
                console.error('切换标签页失败:', e, e.stack);
                // 即使出错也尝试显示内容
                try {
                    const contentId = tabName + '-tab';
                    const content = document.getElementById(contentId);
                    if (content) {
                        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                        content.classList.add('active');
                    }
                } catch (err) {
                    console.error('恢复失败:', err);
                }
            }
        }
        
        async function startCamera() {
            try {
                ensureDOMElements();
                const videoEl = getVideo();
                if (!videoEl) {
                    showError('无法找到视频元素');
                    return;
                }
                
                // 检测Safari浏览器
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                const isSecureContext = window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                
                // Safari特殊检查
                if ((isSafari || isIOS) && !isSecureContext) {
                    showError(`⚠️ Safari浏览器需要HTTPS才能访问摄像头。\n\n解决方案：\n1. 使用"选择图片"功能代替摄像头\n2. 或配置HTTPS访问`);
                    return;
                }
                
                // 检查浏览器支持
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    showError(`您的浏览器不支持摄像头访问。\n\n建议：使用"选择图片"功能上传照片进行识别。`);
                    return;
                }
                
                // ✅ 优先后置摄像头（environment），前置作为fallback
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: { 
                            facingMode: { exact: "environment" },   // 优先后置摄像头
                            width: { ideal: 1280 },
                            height: { ideal: 720 }
                        },
                        audio: false
                    });
                    console.log('✅ 使用后置摄像头（environment）');
                } catch (err1) {
                    // 若设备不支持后置，则自动 fallback 前置摄像头
                    console.warn('⚠️ 后置摄像头获取失败，尝试前置摄像头:', err1);
                    stream = await navigator.mediaDevices.getUserMedia({
                        video: { 
                            facingMode: "user",
                            width: { ideal: 1280 },
                            height: { ideal: 720 }
                        },
                        audio: false
                    });
                    console.log('✅ 使用前置摄像头（fallback）');
                }
                videoEl.srcObject = stream;
                video = videoEl;  // 更新引用
                videoEl.setAttribute('playsinline', 'true');
                videoEl.setAttribute('webkit-playsinline', 'true');
                await videoEl.play();
                document.getElementById('captureBtn').style.display = 'block';
                document.getElementById('stopBtn').style.display = 'block';
                document.querySelector('#vision-tab .btn-primary').style.display = 'none';
                
                // 如果产品模式已激活，自动启动视觉导航和语音监听
                if (productModeActive) {
                    setTimeout(() => {
                        startVisualNavigation();
                        startVoiceListening();
                    }, 1000);
                }
            } catch (err) {
                let errorMsg = '无法访问摄像头: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问摄像头权限（在Safari设置中允许）';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到摄像头设备';
                } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
                    errorMsg += '摄像头被其他应用占用，请关闭其他应用后重试';
                } else if (err.name === 'OverconstrainedError') {
                    errorMsg += '摄像头不支持请求的配置';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                errorMsg += '\\n\\n💡 提示：可以使用"选择图片"功能上传照片';
                showError(errorMsg);
            }
        }
        
        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            ensureDOMElements();
            const videoEl = getVideo();
            if (videoEl) {
                videoEl.srcObject = null;
            }
            document.getElementById('captureBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'none';
            document.querySelector('#vision-tab .btn-primary').style.display = 'block';
        }
        
        function capturePhoto() {
            ensureDOMElements();
            const videoEl = getVideo();
            const canvasEl = getCanvas();
            if (!videoEl || !canvasEl) {
                showError('无法找到视频或画布元素');
                return;
            }
            canvasEl.width = videoEl.videoWidth;
            canvasEl.height = videoEl.videoHeight;
            const ctx = canvasEl.getContext('2d');
            ctx.drawImage(videoEl, 0, 0);
            canvasEl.toBlob(function(blob) {
                currentImageBlob = blob;
                sendImage(blob, '/api/recognize');
            }, 'image/jpeg', 0.9);
        }
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                currentImageBlob = file;
                sendImage(file, '/api/recognize');
            }
        }
        
        async function sendImage(imageBlob, endpoint) {
            showLoading();
            const formData = new FormData();
            formData.append('image', imageBlob);
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                } else {
                    showError(data.error || '处理失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        function testStepDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/step');
        }
        
        function testSignboardDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/signboard');
        }
        
        function testHazardDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/hazard');
        }
        
        function testFacilityDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/facility');
        }
        
        function testTrafficLightDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/traffic_light');
        }
        
        function testCrowdDensityDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/crowd_density');
        }
        
        function testQueueDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/queue');
        }
        
        function testDoorplateDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/doorplate');
        }
        
        function comprehensiveDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/comprehensive');
        }
        
        async function startRecording() {
            try {
                // 检测Safari浏览器
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                const isSecureContext = window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                
                // Safari特殊检查
                if ((isSafari || isIOS) && !isSecureContext) {
                    showError(`⚠️ Safari浏览器需要HTTPS才能访问麦克风。\n\n当前功能受限，建议使用桌面浏览器测试。`);
                    return;
                }
                
                // 检查浏览器支持
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    showError(`您的浏览器不支持麦克风访问。\n\nSafari在iOS上可能需要HTTPS。`);
                    return;
                }
                
                const audioStream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        sampleRate: 16000
                    }
                });
                audioChunks = [];
                
                // 检查MediaRecorder支持（Safari支持有限）
                if (!window.MediaRecorder) {
                    showError(`您的浏览器不支持录音功能。\n\nSafari的MediaRecorder支持有限，建议使用Chrome浏览器。`);
                    return;
                }
                
                // Safari需要指定MIME类型
                let options = {};
                if (MediaRecorder.isTypeSupported('audio/webm')) {
                    options = { mimeType: 'audio/webm' };
                } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                    options = { mimeType: 'audio/mp4' };
                } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
                    options = { mimeType: 'audio/ogg' };
                }
                
                mediaRecorder = new MediaRecorder(audioStream, options);
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data && event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                mediaRecorder.onstop = async () => {
                    const mimeType = mediaRecorder.mimeType || 'audio/webm';
                    const audioBlob = new Blob(audioChunks, { type: mimeType });
                    await sendAudio(audioBlob);
                };
                
                mediaRecorder.onerror = (event) => {
                    showError('录音过程中出错: ' + (event.error?.message || '未知错误'));
                };
                
                mediaRecorder.start();
                document.getElementById('stopRecordBtn').style.display = 'block';
                document.getElementById('recordingStatus').style.display = 'block';
            } catch (err) {
                let errorMsg = '无法访问麦克风: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问麦克风权限（在Safari设置 > 网站设置中允许）';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到麦克风设备';
                } else if (err.name === 'NotReadableError') {
                    errorMsg += '麦克风被其他应用占用';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                if (isIOS || isSafari) {
                    errorMsg += '\\n\\n💡 Safari在iOS上需要HTTPS才能使用麦克风';
                }
                showError(errorMsg);
            }
        }
        
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                document.getElementById('stopRecordBtn').style.display = 'none';
                document.getElementById('recordingStatus').style.display = 'none';
            }
        }
        
        async function sendAudio(audioBlob) {
            showLoading();
            const formData = new FormData();
            formData.append('audio', audioBlob);
            
            try {
                const response = await fetch('/api/recognize/voice', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    displayResults({ voice_result: data });
                } else {
                    showError(data.error || '识别失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        async function testTTS(style) {
            const text = document.getElementById('ttsText').value;
            if (!text) {
                showError('请输入要合成的文字');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/api/tts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, style })
                });
                const data = await response.json();
                
                if (data.success) {
                    // Edge-TTS返回的是MP3格式
                    const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                    audio.play().catch(err => {
                        showError('播放失败: ' + err.message);
                    });
                } else {
                    showError(data.error || '合成失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        function displayResults(data) {
            const results = document.getElementById('results');
            results.innerHTML = '';
            
            // 视觉识别结果
            if (data.detections || data.ocr_results) {
                if (data.ocr_results && data.ocr_results.length > 0) {
                    const div = document.createElement('div');
                    div.innerHTML = '<div class="result-title">📝 识别的文字</div>';
                    data.ocr_results.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'result-item';
                        itemDiv.innerHTML = `
                            <div class="result-text">${item.text}</div>
                            <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                        `;
                        div.appendChild(itemDiv);
                    });
                    results.appendChild(div);
                }
                
                if (data.detections && data.detections.length > 0) {
                    const div = document.createElement('div');
                    div.innerHTML = '<div class="result-title">🎯 检测到的物体</div>';
                    data.detections.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'result-item';
                        itemDiv.innerHTML = `
                            <div class="result-text">${item.class}</div>
                            <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                        `;
                        div.appendChild(itemDiv);
                    });
                    results.appendChild(div);
                }
            }
            
            // 台阶检测结果
            if (data.step_detection) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🪜 台阶检测</div>';
                const itemDiv = document.createElement('div');
                itemDiv.className = 'result-item';
                const step = data.step_detection;
                
                if (step.detected === false || !step.direction) {
                    // 未检测到台阶
                    itemDiv.innerHTML = `
                        <div class="result-text" style="color: #666;">${step.message || '未检测到台阶'}</div>
                        <div style="margin-top: 10px; font-size: 12px; color: #999;">
                            可能原因：<br>
                            • 图片中没有台阶/楼梯<br>
                            • YOLO模型未加载或加载失败<br>
                            • 台阶特征不明显
                        </div>
                    `;
                } else {
                    // 检测到台阶
                    itemDiv.innerHTML = `
                        <div class="result-text">方向: ${step.direction || '未知'}</div>
                        <div class="result-confidence">置信度: ${(step.confidence * 100).toFixed(1)}%</div>
                        ${step.steps_count ? `<div style="margin-top: 5px;">台阶数量: ${step.steps_count}</div>` : ''}
                        ${step.height_cm ? `<div style="margin-top: 5px;">高度: ${step.height_cm}cm</div>` : ''}
                    `;
                }
                div.appendChild(itemDiv);
                results.appendChild(div);
            }
            
            // 标识牌检测结果
            if (data.signboards && data.signboards.length > 0) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🚏 标识牌检测</div>';
                data.signboards.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.text} <span class="badge badge-success">${item.type}</span></div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    div.appendChild(itemDiv);
                });
                results.appendChild(div);
            }
            
            // 危险检测结果
            if (data.hazards && data.hazards.length > 0) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">⚠️ 危险检测</div>';
                data.hazards.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    const severityClass = item.severity === 'high' || item.severity === 'critical' ? 'badge-danger' : 'badge-warning';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.type} <span class="badge ${severityClass}">${item.severity}</span></div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    div.appendChild(itemDiv);
                });
                results.appendChild(div);
            }
            
            // 语音识别结果
            if (data.voice_result) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🎤 语音识别</div>';
                const itemDiv = document.createElement('div');
                itemDiv.className = 'result-item';
                
                const voiceData = data.voice_result;
                const confidence = voiceData.details?.confidence || 0;
                const confidencePercent = (confidence * 100).toFixed(1);
                const confidenceColor = confidence > 0.7 ? '#51cf66' : confidence > 0.5 ? '#ffd43b' : '#ff6b6b';
                
                itemDiv.innerHTML = `
                    <div class="result-text">${voiceData.text || '未识别到语音'}</div>
                    <div style="margin-top: 8px;">
                        <span style="font-size: 13px; color: #666;">置信度: </span>
                        <span style="font-size: 14px; font-weight: bold; color: ${confidenceColor};">
                            ${confidencePercent}%
                        </span>
                        ${voiceData.details?.language ? `<span style="font-size: 12px; color: #999; margin-left: 10px;">语言: ${voiceData.details.language}</span>` : ''}
                    </div>
                    ${confidence < 0.5 ? '<div style="margin-top: 5px; font-size: 12px; color: #ff6b6b;">⚠️ 识别置信度较低，建议在安静环境下清晰说话</div>' : ''}
                `;
                div.appendChild(itemDiv);
                results.appendChild(div);
            }
            
            if (results.innerHTML === '') {
                results.innerHTML = '<div class="result-item">未识别到内容</div>';
            }
            
            document.getElementById('resultSection').classList.add('active');
        }
        
        function showLoading() {
            document.getElementById('loading').classList.add('active');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('active');
        }
        
        function showError(message) {
            console.log('showError被调用:', message);
            try {
                const error = document.getElementById('error');
                if (!error) {
                    console.error('未找到error元素');
                    alert('错误: ' + message);  // 备用方案
                    return;
                }
                error.textContent = message;
                error.classList.add('active');
                setTimeout(() => error.classList.remove('active'), 5000);
            } catch (e) {
                console.error('showError失败:', e);
                alert('错误: ' + message);  // 备用方案
            }
        }
        
        // 字符计数
        document.addEventListener('DOMContentLoaded', function() {
            const ttsText = document.getElementById('ttsText');
            const charCount = document.getElementById('charCount');
            if (ttsText && charCount) {
                ttsText.addEventListener('input', function() {
                    const length = this.value.length;
                    charCount.textContent = length;
                    if (length > 5000) {
                        charCount.style.color = '#ff6b6b';
                    } else if (length > 4500) {
                        charCount.style.color = '#ffd43b';
                    } else {
                        charCount.style.color = '#666';
                    }
                });
            }
        });
        
        // 导航相关函数
        async function planRoute() {
            const start = document.getElementById('navStart').value.trim();
            const destinationsStr = document.getElementById('navDestinations').value.trim();
            
            if (!start || !destinationsStr) {
                showError('请填写起点和目的地');
                return;
            }
            
            const destinations = destinationsStr.split(',').map(d => d.trim()).filter(d => d);
            
            showLoading();
            try {
                const response = await fetch('/api/navigation/plan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ start, destinations })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    // 保存路径规划结果，供导航使用
                    window.lastRouteResult = data.route;
                    displayNavigationResult('路径规划结果', data.route);
                } else {
                    showError('路径规划失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('路径规划错误: ' + err.message);
            }
        }
        
        async function loadAvailablePaths() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/paths');
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('可用路径列表', data.paths);
                } else {
                    showError('获取路径列表失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取路径列表错误: ' + err.message);
            }
        }
        
        async function startNavigation() {
            const destination = document.getElementById('navDestination').value.trim();
            
            if (!destination) {
                showError('请填写目的地');
                return;
            }
            
            // 如果之前有路径规划结果，使用路径段
            let routeSegments = null;
            const lastRouteResult = window.lastRouteResult;
            if (lastRouteResult && lastRouteResult.segments) {
                routeSegments = lastRouteResult.segments;
            }
            
            showLoading();
            try {
                const response = await fetch('/api/navigation/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        destination,
                        route_segments: routeSegments
                    })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已启动', data.status);
                    // 如果TTS可用，会自动播报开始导航
                } else {
                    showError('启动导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('启动导航错误: ' + err.message);
            }
        }
        
        async function pauseNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/pause', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: '用户暂停' })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已暂停', data.status);
                } else {
                    showError('暂停导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('暂停导航错误: ' + err.message);
            }
        }
        
        async function resumeNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/resume', {
                    method: 'POST'
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已恢复', data.status);
                } else {
                    showError('恢复导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('恢复导航错误: ' + err.message);
            }
        }
        
        async function cancelNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/cancel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: '用户取消' })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已取消', data.status);
                } else {
                    showError('取消导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('取消导航错误: ' + err.message);
            }
        }
        
        async function completeNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/complete', {
                    method: 'POST'
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已完成', data.status);
                } else {
                    showError('完成导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('完成导航错误: ' + err.message);
            }
        }
        
        async function getNavigationStatus() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/status');
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航状态', data.status || '当前没有进行中的导航');
                } else {
                    showError('获取导航状态失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取导航状态错误: ' + err.message);
            }
        }
        
        async function updatePosition() {
            const lat = parseFloat(document.getElementById('navLat').value);
            const lng = parseFloat(document.getElementById('navLng').value);
            
            if (isNaN(lat) || isNaN(lng)) {
                showError('请填写有效的经纬度');
                return;
            }
            
            // 尝试获取当前摄像头画面进行障碍检测
            let imageData = null;
            ensureDOMElements();
            const videoEl = getVideo();
            const canvasEl = getCanvas();
            if (videoEl && videoEl.srcObject) {
                try {
                    canvasEl.width = videoEl.videoWidth;
                    canvasEl.height = videoEl.videoHeight;
                    const ctx = canvasEl.getContext('2d');
                    ctx.drawImage(videoEl, 0, 0);
                    imageData = canvasEl.toDataURL('image/jpeg', 0.8);
                } catch (e) {
                    console.log('无法获取摄像头画面:', e);
                }
            }
            
            showLoading();
            try {
                const requestBody = { lat, lng };
                if (imageData) {
                    requestBody.image = imageData;
                }
                
                const response = await fetch('/api/navigation/update_position', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    const result = {
                        status: data.status,
                        is_idle: data.is_idle ? '是（静止）' : '否（移动中）'
                    };
                    if (data.detected_hazards && data.detected_hazards.length > 0) {
                        result.detected_hazards = data.detected_hazards;
                        result.message = '检测到障碍，已自动播报提示';
                    }
                    displayNavigationResult('位置已更新', result);
                } else {
                    showError('更新位置失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('更新位置错误: ' + err.message);
            }
        }
        
        function getCurrentLocation() {
            if (!navigator.geolocation) {
                showError('您的浏览器不支持GPS定位');
                return;
            }
            
            showLoading();
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    document.getElementById('navLat').value = lat.toFixed(6);
                    document.getElementById('navLng').value = lng.toFixed(6);
                    hideLoading();
                    showSuccess('已获取当前位置: ' + lat.toFixed(6) + ', ' + lng.toFixed(6));
                },
                (error) => {
                    hideLoading();
                    let errorMsg = '获取位置失败: ';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMsg += '用户拒绝了位置权限';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMsg += '位置信息不可用';
                            break;
                        case error.TIMEOUT:
                            errorMsg += '获取位置超时';
                            break;
                        default:
                            errorMsg += '未知错误';
                    }
                    showError(errorMsg);
                }
            );
        }
        
        function displayNavigationResult(title, data) {
            const results = document.getElementById('results');
            results.innerHTML = '';
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'result-title';
            titleDiv.textContent = title;
            results.appendChild(titleDiv);
            
            const dataDiv = document.createElement('div');
            dataDiv.className = 'result-item';
            dataDiv.innerHTML = '<pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 13px;">' + JSON.stringify(data, null, 2) + '</pre>';
            results.appendChild(dataDiv);
            
            document.getElementById('resultSection').classList.add('active');
        }
        
        function showSuccess(message) {
            const error = document.getElementById('error');
            error.style.background = '#d4edda';
            error.style.color = '#155724';
            error.textContent = '✅ ' + message;
            error.classList.add('active');
            setTimeout(() => {
                error.classList.remove('active');
                error.style.background = '#fee';
                error.style.color = '#c33';
            }, 3000);
        }
        
        // 实时日志功能
        async function startRealtimeLogs() {
            if (realtimeLogsInterval) {
                return; // 已在运行
            }
            
            document.getElementById('startRealtimeLogsBtn').style.display = 'none';
            document.getElementById('stopRealtimeLogsBtn').style.display = 'block';
            document.getElementById('realtimeLogsContainer').style.display = 'block';
            
            const logsContent = document.getElementById('realtimeLogsContent');
            logsContent.innerHTML = '<div style="color:#666;">正在加载实时日志...</div>';
            
            // 先获取一次日志，获取最后的时间戳
            try {
                const response = await fetch('/api/logs/view?limit=10');
                const data = await response.json();
                if (data.success && data.logs && data.logs.length > 0) {
                    lastLogTimestamp = data.logs[data.logs.length - 1].timestamp;
                    displayRealtimeLogs(data.logs);
                }
            } catch (err) {
                logsContent.innerHTML = `<div style="color:#F44336;">加载失败: ${err.message}</div>`;
            }
            
            // 每2秒轮询一次新日志（使用全局引用）
            if (window.__intervals.realtimeLogs) {
                clearInterval(window.__intervals.realtimeLogs);
            }
            window.__intervals.realtimeLogs = setInterval(async () => {
                try {
                    let url = '/api/logs/realtime';
                    if (lastLogTimestamp) {
                        url += `?since=${lastLogTimestamp}`;
                    }
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (data.success && data.logs && data.logs.length > 0) {
                        // 更新最后的时间戳
                        lastLogTimestamp = data.logs[data.logs.length - 1].timestamp;
                        // 追加新日志
                        appendRealtimeLogs(data.logs);
                    }
                } catch (err) {
                    console.error('实时日志获取失败:', err);
                }
            }, 2000); // 每2秒更新一次
        }
        
        function stopRealtimeLogs() {
            if (window.__intervals.realtimeLogs) {
                clearInterval(window.__intervals.realtimeLogs);
                delete window.__intervals.realtimeLogs;
            }
            document.getElementById('startRealtimeLogsBtn').style.display = 'block';
            document.getElementById('stopRealtimeLogsBtn').style.display = 'none';
        }
        
        function displayRealtimeLogs(logs) {
            const logsContent = document.getElementById('realtimeLogsContent');
            logsContent.innerHTML = '';
            logs.forEach(log => {
                appendLogEntry(log);
            });
            // 滚动到底部
            const container = document.getElementById('realtimeLogsContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        function appendRealtimeLogs(logs) {
            logs.forEach(log => {
                appendLogEntry(log);
            });
            // 滚动到底部
            const container = document.getElementById('realtimeLogsContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        function appendLogEntry(log) {
            const logsContent = document.getElementById('realtimeLogsContent');
            const time = new Date(log.timestamp).toLocaleTimeString();
            const levelColor = log.level === 'error' ? '#F44336' : log.level === 'warning' ? '#FF9800' : '#2196F3';
            const levelIcon = log.level === 'error' ? '❌' : log.level === 'warning' ? '⚠️' : 'ℹ️';
            
            const entry = document.createElement('div');
            entry.style.cssText = `margin-bottom:5px; padding:5px; border-left:3px solid ${levelColor}; padding-left:10px;`;
            entry.innerHTML = `
                <span style="color:#666; font-size:11px;">[${time}]</span>
                <span style="color:${levelColor}; font-weight:bold;">${levelIcon} ${log.level.toUpperCase()}</span>
                <span style="color:#333;">${log.content || log.source || ''}</span>
                ${log.metadata ? `<span style="color:#999; font-size:11px;">(${JSON.stringify(log.metadata).substring(0, 50)}...)</span>` : ''}
            `;
            logsContent.appendChild(entry);
        }
        
        // 日志管理相关函数
        async function viewLogs() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                let url = '/api/logs/view';
                if (date) {
                    url += `?date=${date}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult(`日志列表（${data.count} 条）`, {
                        date: data.date,
                        count: data.count,
                        logs: data.logs
                    });
                } else {
                    showError('查看日志失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('查看日志错误: ' + err.message);
            }
        }
        
        async function getLogStatistics() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                let url = '/api/logs/statistics';
                if (date) {
                    url += `?date=${date}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('日志统计信息', {
                        date: data.date,
                        statistics: data.statistics
                    });
                } else {
                    showError('获取统计信息失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取统计信息错误: ' + err.message);
            }
        }
        
        async function uploadLogs() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                const response = await fetch('/api/logs/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ date: date || null })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    showSuccess(data.message + (data.upload_file ? `\\n文件: ${data.upload_file}` : ''));
                } else {
                    showError('上传日志失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('上传日志错误: ' + err.message);
            }
        }
        
        function downloadLogs() {
            const date = document.getElementById('logDate').value;
            
            let url = '/api/logs/download';
            if (date) {
                url += `?date=${date}`;
            }
            
            // 直接下载文件
            window.location.href = url;
        }
        
        // 实时视觉导航功能
        function startVisualNavigation() {
            // 确保函数暴露到全局作用域
            window.startVisualNavigation = startVisualNavigation;
            // 优先使用产品模式的摄像头流（如果已开启）
            const productVideo = document.getElementById('productVideo');
            let videoToUse = video;
            
            // 如果产品模式已开启摄像头，共享使用
            if (productVideo && productVideo.srcObject && productVideo.readyState >= 2) {
                console.log('使用产品模式的摄像头流');
                // 将产品模式的流也赋值给普通模式的video
                ensureDOMElements();
                const videoEl = getVideo();
                if (videoEl && !videoEl.srcObject) {
                    videoEl.srcObject = productVideo.srcObject;
                    videoEl.play().then(() => {
                        video = videoEl;  // 更新引用
                        continueStartVisualNavigation();
                    }).catch((err) => {
                        console.error('视频播放失败:', err);
                        continueStartVisualNavigation();
                    });
                    return;
                }
            }
            
            continueStartVisualNavigation();
            
            function continueStartVisualNavigation() {
                // 检查摄像头是否开启
                ensureDOMElements();
                const videoEl = getVideo();
                if (!videoEl || !videoEl.srcObject) {
                    showError('请先开启摄像头');
                    return;
                }
                
                // 检查视频是否已播放
                if (videoEl.readyState < 2) {
                    showError('摄像头未就绪，请稍候再试');
                    return;
                }
                
                // 显示结果区域
                document.getElementById('visualGuidanceResult').style.display = 'block';
                document.getElementById('guidanceMessages').innerHTML = '<div style="color:#4CAF50;">🎥 视觉导航已启动，正在分析画面...</div>';
                
                // 开始定时分析画面（每1.5秒一次，提高响应速度）（使用全局引用）
                if (window.__intervals.visualNavigation) {
                    clearInterval(window.__intervals.visualNavigation);
                }
                window.__intervals.visualNavigation = setInterval(() => {
                    analyzeVisualGuidanceFrame().catch((err) => {
                        console.error('视觉导航分析失败:', err);
                    });
                }, 1500);
                
                // ✅ 指令5：开始导航时添加日志
                if (window.logInfo) {
                    window.logInfo('视觉导航已启动', { 
                        component: 'navigation', 
                        mode: productModeActive ? 'product' : 'normal' 
                    });
                }
                
                // 立即执行一次
                analyzeVisualGuidanceFrame().then(() => {
                    showSuccess('实时视觉导航已启动');
                }).catch((err) => {
                    console.error('视觉导航分析失败:', err);
                    showSuccess('实时视觉导航已启动');
                });
            }
        }
        
        function stopVisualNavigation() {
            if (window.__intervals.visualNavigation) {
                clearInterval(window.__intervals.visualNavigation);
                delete window.__intervals.visualNavigation;
            }
            document.getElementById('visualGuidanceResult').style.display = 'none';
            document.getElementById('guidanceMessages').innerHTML = '';
            showSuccess('视觉导航已停止');
        }
        
        // ========== 统一视觉模块入口（规范要求）==========
        /**
         * 统一的视觉分析入口函数
         * @param {Blob} frameBlob - 视频帧的Blob对象（可选，如果不提供则自动获取）
         * @returns {Promise<void>}
         */
        async function analyzeVisualGuidanceFrame(frameBlob = null) {
            try {
                // 如果没有提供Blob，则根据模式获取
                if (!frameBlob) {
                    if (productModeActive) {
                        frameBlob = await _getFrameBlobForProductMode();
                    } else {
                        frameBlob = await _getFrameBlobForNormalMode();
                    }
                }
                
                if (!frameBlob) {
                    console.warn('⚠️ 无法获取视频帧');
                    return;
                }
                
                // 发送到API进行分析
                const formData = new FormData();
                formData.append('image', frameBlob, 'frame.jpg');
                
                const response = await fetch('/api/navigation/visual_guidance', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // 【节点记忆系统】设置全局变量供NodeEngine使用
                    if (data.vision_summary) {
                        const vs = data.vision_summary || {};
                        const rawDetections = vs.detections || vs.objects || [];
                        // 设置YOLO结果（供NodeEngine使用）
                        window.latestYOLOResult = rawDetections.map(det => ({
                            label: det.class || det.label || '',
                            confidence: det.confidence || 0,
                            bbox: det.box || det.bbox || det.rect || {},
                            distance: det.distance || null
                        }));
                        // 设置OCR结果（供NodeEngine使用）
                        if (vs.ocr_text || vs.ocr_blocks) {
                            const ocrText = vs.ocr_text || (Array.isArray(vs.ocr_blocks) ? vs.ocr_blocks.map(b => b.text || '').join(' ') : '');
                            window.latestOCRResult = { text: ocrText };
                        }
                        // 调用节点处理桥接函数
                        if (window.handleVisionFrameForNodes) {
                            try {
                                window.handleVisionFrameForNodes();
                            } catch (e) {
                                console.warn('节点处理失败:', e);
                            }
                        }
                    }
                    
                    // 🚀【旗舰版视觉增强】- 接入VisionEnhancer处理YOLO输出
                    // ========== 指令2：前端兼容新结构 & 优雅降级 ==========
                    if (window.VisionEnhancer && data.vision_summary) {
                        try {
                            const vs = data.vision_summary || {};
                            // 兼容新结构：优先使用detections，降级到objects
                            const rawDetections = vs.detections || vs.objects || [];
                            
                            // ✅ 构造VisionEnhancer需要的格式（兼容多种bbox格式）
                            // 先过滤掉 null/undefined，再处理
                            const detections = (rawDetections || [])
                                .filter(Boolean)  // ① 先把 null / undefined 过滤掉
                                .map(rawDet => {
                                    const det = rawDet || {};  // ② 再兜一层保险
                                    
                                    let box = { x1: 0, y1: 0, x2: 0, y2: 0 };
                                    
                                    // 兼容多种bbox格式：box / bbox / rect
                                    if (det.box) {
                                        box = det.box;
                                    } else if (det.bbox) {
                                        // bbox可能是 [x, y, w, h] 或 {x1, y1, x2, y2}
                                        if (Array.isArray(det.bbox) && det.bbox.length >= 4) {
                                            // [x, y, w, h] -> {x1, y1, x2, y2}
                                            box = {
                                                x1: det.bbox[0],
                                                y1: det.bbox[1],
                                                x2: det.bbox[0] + det.bbox[2],
                                                y2: det.bbox[1] + det.bbox[3]
                                            };
                                        } else if (typeof det.bbox === 'object') {
                                            box = det.bbox;
                                        }
                                    } else if (det.rect) {
                                        box = det.rect;
                                    }
                                    
                                    return {
                                        label: det.class || det.label || '',
                                        class: det.class || det.label || '',
                                        box: box,
                                        confidence: det.confidence || 0
                                    };
                                });
                            
                            const yoloOutput = {
                                detections: detections,
                                frameWidth: vs.frame_width || vs.width || 640,
                                frameHeight: vs.frame_height || vs.height || 480
                            };
                            
                            // 如果detections为空，记录日志但不报错
                            if (detections.length === 0) {
                                if (window.logDebug) {
                                    window.logDebug('VisionEnhancer: empty detections, treat as safe frame', {
                                        component: 'vision',
                                        has_vision_summary: !!data.vision_summary
                                    });
                                }
                            }
                            
                            // 通过VisionEnhancer处理（即使detections为空也调用，让其返回safe状态）
                            const enhancedSummary = window.VisionEnhancer.processFrame(yoloOutput);
                            
                            if (enhancedSummary && window.logDebug) {
                                window.logDebug('VisionEnhancer处理完成', enhancedSummary);
                            }
                        } catch (e) {
                            if (window.logError) {
                                window.logError('VisionEnhancer处理失败', { error: e.toString(), stack: e.stack });
                            } else {
                                console.error('VisionEnhancer处理失败', e);
                            }
                        }
                    }
                    
                    // ⑤【加入：视觉 + 导航同步调度（关键）】
                    // 将视觉事件接入TaskChain
                    // ✅ 安全防护：确保 guidance 存在才入队
                    if (window.taskChain) {
                        if (data.guidance && typeof data.guidance === 'object' && data.guidance.direction) {
                            window.taskChain.enqueue('visual_event', {
                                guidance: data.guidance,
                                vision_summary: data.vision_summary || null
                            }, 2);
                            // ④【加入：TaskChain完整日志】
                            if (window.logDebug) {
                                window.logDebug('[TaskChain] 视觉事件入队', data.vision_summary);
                            } else {
                                console.log('[TaskChain] 视觉事件入队:', data.vision_summary);
                            }
                            if (window.sendLog) {
                                window.sendLog({ type: 'task_enqueue', taskType: 'visual_event', payload: data.vision_summary });
                            }
                        }
                    }
                    
                    // 根据模式使用对应的显示函数
                    if (productModeActive) {
                        displayVisualGuidanceForProduct(data.guidance, data.vision_summary);
                    } else {
                        displayVisualGuidance(data.guidance, data.vision_summary);
                    }
                    
                    // ③【新增：后台日志上传】
                    if (window.sendLog) {
                        window.sendLog({ type: 'vision_result', guidance: data.guidance, summary: data.vision_summary });
                    }
                } else {
                    console.error('视觉导航分析失败:', data.error);
                    // ③【新增：后台日志上传】
                    if (window.sendLog) {
                        window.sendLog({ type: 'vision_error', error: data.error });
                    }
                }
            } catch (err) {
                console.error('视觉导航分析错误:', err);
            }
        }
        
        /**
         * 普通模式：从视频获取帧Blob
         * @returns {Promise<Blob|null>}
         */
        function _getFrameBlobForNormalMode() {
            return new Promise((resolve) => {
                try {
                    ensureDOMElements();
                    const videoEl = getVideo();
                    const canvasEl = getCanvas();
                    if (!videoEl || !canvasEl) {
                        console.error('无法找到视频或画布元素');
                        resolve(null);
                        return;
                    }
                    canvasEl.width = videoEl.videoWidth;
                    canvasEl.height = videoEl.videoHeight;
                    const ctx = canvasEl.getContext('2d');
                    ctx.drawImage(videoEl, 0, 0);
                    
                    canvasEl.toBlob((blob) => {
                        resolve(blob);
                    }, 'image/jpeg', 0.8);
                } catch (err) {
                    console.error('获取普通模式视频帧失败:', err);
                    resolve(null);
                }
            });
        }
        
        /**
         * 产品模式：从视频获取帧Blob
         * @returns {Promise<Blob|null>}
         */
        function _getFrameBlobForProductMode() {
            return new Promise((resolve) => {
                try {
                    const productVideo = document.getElementById('productVideo');
                    const productCanvas = document.getElementById('productCanvas');
                    
                    if (!productVideo || !productVideo.srcObject) {
                        console.warn('⚠️ 摄像头未就绪');
                        resolve(null);
                        return;
                    }
                    
                    if (productVideo.readyState < 2) {
                        console.warn('⚠️ 视频未就绪（readyState=' + productVideo.readyState + '）');
                        resolve(null);
                        return;
                    }
                    
                    // 设置分析标志
                    if (window.isAnalyzingVision) {
                        resolve(null); // 如果正在分析，跳过
                        return;
                    }
                    window.isAnalyzingVision = true;
                    
                    // 更新状态：显示正在扫描
                    const guidanceMessages = document.getElementById('guidanceMessages');
                    if (guidanceMessages) {
                        guidanceMessages.innerHTML = '<div style="color:#FF9800;">🔍 正在扫描环境...</div>';
                    }
                    
                    // 从视频获取当前帧（确保尺寸有效）
                    if (productVideo.videoWidth === 0 || productVideo.videoHeight === 0) {
                        console.warn('⚠️ 视频尺寸无效，等待中...');
                        window.isAnalyzingVision = false;
                        resolve(null);
                        return;
                    }
                    
                    productCanvas.width = productVideo.videoWidth;
                    productCanvas.height = productVideo.videoHeight;
                    const ctx = productCanvas.getContext('2d');
                    
                    // 确保canvas尺寸有效
                    if (productCanvas.width === 0 || productCanvas.height === 0) {
                        console.warn('⚠️ Canvas尺寸无效');
                        window.isAnalyzingVision = false;
                        resolve(null);
                        return;
                    }
                    
                    ctx.drawImage(productVideo, 0, 0);
                    
                    // 镜头运动检测
                    const frameData = productCanvas.toDataURL('image/jpeg', 0.1);
                    detectCameraMotion(frameData);
                    
                    // 转换为Blob
                    productCanvas.toBlob((blob) => {
                        window.isAnalyzingVision = false; // 重置标志
                        if (!blob || blob.size === 0) {
                            console.warn('⚠️ Blob为空或无效');
                            resolve(null);
                            return;
                        }
                        console.log('📸 准备发送图片: 大小=' + blob.size + '字节, 类型=' + blob.type);
                        resolve(blob);
                    }, 'image/jpeg', 0.7);
                } catch (err) {
                    window.isAnalyzingVision = false;
                    console.error('获取产品模式视频帧失败:', err);
                    resolve(null);
                }
            });
        }
        
        // ========== 向后兼容：保留旧函数名（内部调用统一入口）==========
        /**
         * @deprecated 使用 analyzeVisualGuidanceFrame() 代替
         */
        async function analyzeVisualGuidance() {
            return analyzeVisualGuidanceFrame();
        }
        
        /**
         * @deprecated 使用 analyzeVisualGuidanceFrame() 代替
         */
        async function analyzeVisualGuidanceForProduct() {
            return analyzeVisualGuidanceFrame();
        }
        
        function displayVisualGuidance(guidance, visionSummary) {
            // ✅ 安全防护：检查 guidance 参数
            if (!guidance || typeof guidance !== 'object') {
                console.warn("[视觉导航] guidance 数据为空或无效，跳过本次导航播报", guidance);
                return;
            }
            
            if (!guidance.direction) {
                console.warn("[视觉导航] guidance.direction 缺失，跳过本次导航播报", guidance);
                return;
            }
            
            const messagesDiv = document.getElementById('guidanceMessages');
            let html = '';
            
            // 方向指示
            const directionIcons = {
                'forward': '⬆️',
                'left': '⬅️',
                'right': '➡️',
                'stop': '⛔'
            };
            
            const directionColors = {
                'forward': '#4CAF50',
                'left': '#2196F3',
                'right': '#FF9800',
                'stop': '#F44336'
            };
            
            const direction = guidance.direction || 'forward';
            const icon = directionIcons[direction] || '➡️';
            const color = directionColors[direction] || '#666';
            
            html += `<div style="font-size:24px; text-align:center; margin-bottom:15px; color:${color}; font-weight:bold;">
                ${icon} ${direction.toUpperCase()}
            </div>`;
            
            // 指引消息
            if (guidance.messages && guidance.messages.length > 0) {
                html += '<div style="margin-bottom:10px;">';
                guidance.messages.forEach(msg => {
                    html += `<div style="padding:8px; margin:5px 0; background:#f5f5f5; border-radius:5px; font-size:14px;">${msg}</div>`;
                });
                html += '</div>';
            }
            
            // 房间号
            if (guidance.room_numbers && guidance.room_numbers.length > 0) {
                html += `<div style="margin-top:10px; padding:8px; background:#e3f2fd; border-radius:5px;">
                    <strong>房间号：</strong>${guidance.room_numbers.join(', ')}
                </div>`;
            }
            
            // 检测摘要
            html += '<div style="margin-top:15px; padding:10px; background:#f9f9f9; border-radius:5px; font-size:12px; color:#666;">';
            html += `<div>检测到 ${visionSummary.objects_detected || 0} 个物体，${visionSummary.texts_detected || 0} 段文字</div>`;
            if (guidance.signboards && guidance.signboards.length > 0) {
                html += `<div>标识牌：${guidance.signboards.length} 个</div>`;
            }
            if (guidance.step_detected) {
                html += `<div style="color:#F44336;">⚠️ 检测到台阶</div>`;
            }
            if (guidance.hazards_count > 0) {
                html += `<div style="color:#F44336;">⚠️ 检测到 ${guidance.hazards_count} 个危险区域</div>`;
            }
            html += '</div>';
            
            messagesDiv.innerHTML = html;
        }
        
        // ✅ 重置完整产品模式状态
        function resetFullProductModeState() {
            console.log('[FullMode] resetFullProductModeState() called');
            isWelcomePlayed = false;
            hasStartedOnce = false;
            isProductModeRunning = false;
            // 注意：不重置 productModeActive，因为它由 stopProductMode() 管理
            // 注意：不重置 isPlayingTTS，因为它由 TTS 系统管理
            console.log('[FullMode] State reset complete');
        }
        
        // 完整产品模式功能
        function startProductMode() {
            // ✅ 日志：记录点击时的状态
            console.log('[FullMode] clicked', {
                isProductModeRunning: isProductModeRunning,
                isWelcomePlayed: isWelcomePlayed,
                isSpeaking: isPlayingTTS,
                productModeActive: productModeActive,
                hasStartedOnce: hasStartedOnce
            });
            
            // ✅ 修复：每次点击前先重置状态，确保可以多次启动
            resetFullProductModeState();
            
            // 确保函数暴露到全局作用域
            window.startProductMode = startProductMode;
            window.resetFullProductModeState = resetFullProductModeState;
            
            // 检查必要模块
            const productVideo = document.getElementById('productVideo');
            if (!productVideo) {
                showError('视频元素未找到');
                return;
            }
            
            // 显示状态
            document.getElementById('productModeStatus').style.display = 'block';
            document.getElementById('productGuidance').style.display = 'block';
            document.getElementById('productVoiceStatus').style.display = 'block';
            document.getElementById('startProductModeBtn').style.display = 'none';
            document.getElementById('stopProductModeBtn').style.display = 'block';
            
            productModeActive = true;
            isProductModeRunning = true;
            hasStartedOnce = true;
            
            // 更新状态
            updateProductStatus('正在启动...');
            
            // 1. 自动开启摄像头（如果未开启）
            if (!productVideo.srcObject) {
                updateProductStatus('正在开启摄像头...');
                startCameraForProduct().then((cameraStarted) => {
                    if (!cameraStarted) {
                        showError('摄像头启动失败，请检查权限设置');
                        productModeActive = false;
                        document.getElementById('startProductModeBtn').style.display = 'block';
                        document.getElementById('stopProductModeBtn').style.display = 'none';
                        return;
                    }
                    // 摄像头启动后，继续后续步骤
                    continueAfterCameraReady();
                }).catch((err) => {
                    console.error('摄像头启动失败:', err);
                    showError('摄像头启动失败，请检查权限设置');
                    productModeActive = false;
                    document.getElementById('startProductModeBtn').style.display = 'block';
                    document.getElementById('stopProductModeBtn').style.display = 'none';
                });
            } else {
                // 摄像头已开启，直接继续
                continueAfterCameraReady();
            }
            
            // 继续后续步骤的函数
            function continueAfterCameraReady() {
                // 等待摄像头就绪（增加超时保护）
                new Promise((resolve, reject) => {
                    let checkCount = 0;
                    const maxChecks = 50; // 最多等待5秒
                    const checkReady = () => {
                        checkCount++;
                        if (productVideo.readyState >= 2) {
                            console.log('✅ 摄像头已就绪');
                            resolve();
                        } else if (checkCount >= maxChecks) {
                            console.warn('⚠️ 摄像头就绪超时');
                            reject(new Error('摄像头就绪超时'));
                        } else {
                            setTimeout(checkReady, 100);
                        }
                    };
                    checkReady();
                }).then(() => {
                    // ①【修复：导航无法持续语音播报】- 启动导航状态机和路点系统
                    const destination = '产品模式导航';
                    if (window.NavigationFSM) {
                        window.NavigationFSM.start(destination);
                    }
                    if (window.WaypointManager) {
                        window.WaypointManager.clearWaypoints();
                    }
                    if (window.AutoRecovery) {
                        window.AutoRecovery.record('navigation', 'start', { destination });
                    }
                    
                    // 2. 立即启动视觉导航（自动环境扫描，不阻塞）
                    updateProductStatus('启动环境扫描...');
                    console.log('🎥 启动视觉导航...');
                    // 不等待，立即开始（异步），自动开始扫描
                    startVisualNavigationForProduct();
                    
                    // 3. 启动语音监听
                    updateProductStatus('启动语音监听...');
                    console.log('🎤 启动语音监听...');
                    return startVoiceListening();
                }).then(() => {
                    // 启动完成
                    console.log('✅ 产品模式启动完成');
                    // ③【新增：后台日志上传】
                    if (window.sendLog) {
                        window.sendLog({ type: 'product_mode_started' });
                    }
                }).catch((err) => {
                    console.error('摄像头就绪失败:', err);
                    showError('摄像头就绪失败，请刷新页面重试');
                    productModeActive = false;
                    document.getElementById('startProductModeBtn').style.display = 'block';
                    document.getElementById('stopProductModeBtn').style.display = 'none';
                });
            }
            
            // 更新状态显示
            const voiceStatusDiv = document.getElementById('voiceStatusText');
            if (voiceStatusDiv) {
                voiceStatusDiv.innerHTML = '<span style="color:#4CAF50;">✅ 正在监听语音...</span>';
            }
            
            // 4. 播放欢迎语音（立即播放，不等待用户交互）
            // 注意：Mac上摄像头启动后可以立即播放，不需要等待用户交互
            updateProductStatus('产品模式运行中 - 自动环境扫描已开启');
            showSuccess('完整产品模式已启动，环境扫描和语音提示已自动开启');
            
            // ✅ 修复：播放欢迎语音（仅在未播放过时播放）
            // 立即尝试播放欢迎语音（不阻塞）
            // 注意：由于用户已经点击了按钮，这个点击事件可以用于触发音频播放
            if (!isWelcomePlayed) {
                setTimeout(() => {
                    try {
                        debugLog('准备播放欢迎语音...', 'info');
                        console.log('[FullMode] Starting welcome speech...');
                        if (window.speakText) {
                            // ✅ 修复：使用 Promise 包装，确保播报完成时设置标志
                            const welcomeText = 'Luna已启动，开始环境扫描，我将主动为您提示周围环境';
                            window.speakText(welcomeText, 'calm');
                            // ✅ 标记欢迎语音已发送（实际完成由 TTS 回调处理）
                            isWelcomePlayed = true;
                            console.log('[FullMode] Welcome speech sent to queue');
                        }
                        debugLog('✅ 欢迎语音已发送到播放队列', 'info');
                    } catch (err) {
                        debugLog(`⚠️ 欢迎语音播放失败: ${err.message}`, 'warn');
                        console.error('欢迎语音播放错误:', err);
                        // ✅ 修复：即使失败也标记为已尝试，避免重复尝试
                        isWelcomePlayed = true;
                        // 如果自动播放失败，等待用户交互
                        const playWelcomeOnce = () => {
                            try {
                                debugLog('用户交互后尝试播放欢迎语音...', 'info');
                                if (window.speakText) {
                                    window.speakText('Luna已启动，开始环境扫描，我将主动为您提示周围环境', 'calm');
                                    isWelcomePlayed = true;
                                }
                                debugLog('✅ 用户交互后欢迎语音已发送', 'info');
                            } catch (e) {
                                debugLog(`❌ 用户交互后播放也失败: ${e.message}`, 'error');
                                console.error('用户交互后播放错误:', e);
                                isWelcomePlayed = true; // 即使失败也标记，避免无限重试
                            }
                            document.removeEventListener('click', playWelcomeOnce);
                            document.removeEventListener('touchstart', playWelcomeOnce);
                        };
                        document.addEventListener('click', playWelcomeOnce, { once: true });
                        document.addEventListener('touchstart', playWelcomeOnce, { once: true });
                    }
                }, 1000); // 延迟1秒确保摄像头已启动
            } else {
                console.log('[FullMode] Welcome speech already played, skipping');
            }
        }
        
        function stopProductMode() {
            productModeActive = false;
            isProductModeRunning = false;
            // ✅ 注意：不重置 isWelcomePlayed 和 hasStartedOnce，因为它们用于下次启动时的判断
            
            // 停止视觉导航
            stopVisualNavigation();
            
            // 停止语音监听
            stopVoiceListening();
            
            // 停止摄像头
            stopCameraForProduct();
            
            // 隐藏状态
            document.getElementById('productModeStatus').style.display = 'none';
            document.getElementById('productGuidance').style.display = 'none';
            document.getElementById('productVoiceStatus').style.display = 'none';
            document.getElementById('startProductModeBtn').style.display = 'block';
            document.getElementById('stopProductModeBtn').style.display = 'none';
            
            console.log('[FullMode] Product mode stopped');
            showSuccess('产品模式已停止');
        }
        
        async function startCameraForProduct() {
            try {
                const productVideo = document.getElementById('productVideo');
                if (!productVideo) {
                    showError('视频元素未找到');
                    return false;
                }
                
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                // 修复：更准确的HTTPS检测（包括IP地址访问）
                const isSecureContext = window.location.protocol === 'https:' || 
                                       window.location.hostname === 'localhost' || 
                                       window.location.hostname === '127.0.0.1' ||
                                       window.isSecureContext === true; // 使用浏览器原生API
                
                console.log('🔍 摄像头启动检查:', {
                    isSafari, isIOS, isSecureContext,
                    protocol: window.location.protocol,
                    hostname: window.location.hostname,
                    href: window.location.href,
                    isSecureContext_native: window.isSecureContext,
                    userAgent: navigator.userAgent,
                    hasMediaDevices: !!navigator.mediaDevices,
                    hasGetUserMedia: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
                });
                
                // 在页面上显示调试信息（iPhone Safari无法使用控制台）
                debugLog(`协议: ${window.location.protocol}`, 'info');
                debugLog(`地址: ${window.location.href}`, 'info');
                debugLog(`安全上下文: ${window.isSecureContext ? '是' : '否'}`, window.isSecureContext ? 'info' : 'warn');
                debugLog(`iOS: ${isIOS}, Safari: ${isSafari}`, 'info');
                
                // iOS Safari 在HTTP模式下无法使用摄像头（修复：使用原生isSecureContext）
                const actuallySecure = window.isSecureContext !== undefined ? window.isSecureContext : isSecureContext;
                
                if (isIOS && !actuallySecure) {
                    const errorMsg = `⚠️ iOS Safari浏览器需要HTTPS才能访问摄像头\n\n当前协议: ${window.location.protocol}\n当前地址: ${window.location.href}\n\n解决方案：\n1. 确保使用 https:// 访问\n2. 信任自签名证书\n3. 或使用Chrome浏览器`;
                    showError(errorMsg);
                    updateProductStatus('❌ iOS Safari需要HTTPS（当前: ' + window.location.protocol + '）');
                    
                    // 显示更详细的提示
                    const statusDiv = document.getElementById('productStatusDetails');
                    if (statusDiv) {
                        statusDiv.innerHTML = `
                            <div style="color:#F44336; font-weight:bold; margin-bottom:10px;">⚠️ iOS Safari限制</div>
                            <div style="font-size:13px; line-height:1.6; color:#666;">
                                当前协议: <strong>${window.location.protocol}</strong><br>
                                当前地址: <strong>${window.location.href}</strong><br>
                                安全上下文: <strong>${window.isSecureContext ? '是' : '否'}</strong><br><br>
                                iOS Safari浏览器出于安全考虑，在HTTP模式下无法使用摄像头和麦克风。<br><br>
                                <strong>解决方案：</strong><br>
                                1. 📱 确保使用 <code>https://</code> 访问（不是 http://）<br>
                                2. 🔒 信任自签名证书（点击"访问此网站"）<br>
                                3. 🌐 或使用Chrome浏览器访问
                            </div>
                        `;
                    }
                    return false;
                }
                
                // Safari桌面版也需要HTTPS
                if (isSafari && !isIOS && !actuallySecure) {
                    const errorMsg = `⚠️ Safari浏览器需要HTTPS才能访问摄像头\n\n当前协议: ${window.location.protocol}\n建议：\n1. 使用 https:// 访问\n2. 或使用Chrome浏览器测试`;
                    showError(errorMsg);
                    updateProductStatus('摄像头启动失败：需要HTTPS（当前: ' + window.location.protocol + '）');
                    return false;
                }
                
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    const errorMsg = `您的浏览器不支持摄像头访问\n\n建议使用Chrome、Edge或Firefox浏览器`;
                    showError(errorMsg);
                    updateProductStatus('摄像头启动失败：浏览器不支持');
                    return false;
                }
                
                updateProductStatus('正在请求摄像头权限...');
                console.log('📹 正在请求摄像头权限...');
                debugLog('正在请求摄像头权限...', 'info');
                
                // ✅ 优先后置摄像头（environment），前置作为fallback
                let stream = null;
                try {
                    // 先尝试后置摄像头（environment）
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: { 
                            facingMode: { exact: "environment" },   // 优先后置摄像头
                            width: { ideal: 640 },
                            height: { ideal: 480 }
                        },
                        audio: false
                    });
                    console.log('✅ 使用后置摄像头（environment）');
                    debugLog('✅ 使用后置摄像头（environment）', 'info');
                } catch (err1) {
                    // 若设备不支持后置，则自动 fallback 前置摄像头
                    console.warn('⚠️ 后置摄像头获取失败，尝试前置摄像头:', err1);
                    debugLog(`⚠️ 后置摄像头失败: ${err1.name} - ${err1.message}`, 'warn');
                    try {
                        // 如果后置摄像头失败，尝试前置摄像头
                        stream = await navigator.mediaDevices.getUserMedia({ 
                            video: { 
                                facingMode: "user",
                                width: { ideal: 640 },
                                height: { ideal: 480 }
                            },
                            audio: false
                        });
                        console.log('✅ 使用前置摄像头（fallback）');
                        debugLog('✅ 使用前置摄像头（fallback）', 'info');
                    } catch (err2) {
                        // 最后尝试默认配置
                        console.warn('⚠️ 前置摄像头也失败，尝试默认配置:', err2);
                        debugLog(`⚠️ 前置摄像头也失败: ${err2.name} - ${err2.message}`, 'warn');
                        stream = await navigator.mediaDevices.getUserMedia({ 
                            video: true,
                            audio: false
                        });
                        console.log('✅ 使用默认摄像头配置');
                        debugLog('✅ 使用默认摄像头配置', 'info');
                    }
                }
                
                if (!stream) {
                    throw new Error('无法获取摄像头流');
                }
                
                console.log('✅ 摄像头权限已授予，流已获取');
                debugLog('✅ 摄像头权限已授予', 'info');
                console.log('📹 流信息:', {
                    active: stream.active,
                    id: stream.id,
                    tracks: stream.getTracks().map(t => ({
                        kind: t.kind,
                        enabled: t.enabled,
                        readyState: t.readyState,
                        settings: t.getSettings()
                    }))
                });
                
                updateProductStatus('正在设置视频流...');
                
                // 停止之前的流（如果有）
                if (productVideo.srcObject) {
                    const oldStream = productVideo.srcObject;
                    oldStream.getTracks().forEach(track => track.stop());
                }
                
                productVideo.srcObject = stream;
                productVideo.setAttribute('playsinline', 'true');
                productVideo.setAttribute('webkit-playsinline', 'true');
                productVideo.setAttribute('autoplay', 'true');
                productVideo.muted = false; // 确保不是静音状态
                
                // 等待视频元数据加载（增加超时）
                updateProductStatus('正在加载视频元数据...');
                await new Promise((resolve, reject) => {
                    let resolved = false;
                    const timeout = setTimeout(() => {
                        if (!resolved) {
                            resolved = true;
                            console.error('❌ 视频元数据加载超时');
                            reject(new Error('视频元数据加载超时'));
                        }
                    }, 10000); // 10秒超时
                    
                    productVideo.onloadedmetadata = () => {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.log('✅ 视频元数据已加载:', {
                                videoWidth: productVideo.videoWidth,
                                videoHeight: productVideo.videoHeight,
                                readyState: productVideo.readyState
                            });
                            resolve();
                        }
                    };
                    
                    productVideo.onerror = (err) => {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.error('❌ 视频加载错误:', err);
                            reject(err);
                        }
                    };
                    
                    // 如果已经加载完成，立即resolve
                    if (productVideo.readyState >= 1) {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.log('✅ 视频已就绪（readyState=' + productVideo.readyState + '）');
                            resolve();
                        }
                    }
                });
                
                updateProductStatus('正在播放视频...');
                console.log('📹 准备播放视频...');
                
                // 尝试播放视频
                try {
                    await productVideo.play();
                    console.log('✅ 视频播放已启动');
                } catch (playErr) {
                    console.warn('⚠️ 自动播放失败，尝试用户交互后播放:', playErr);
                    // 如果自动播放失败，等待用户交互
                    updateProductStatus('请点击页面以启用摄像头画面');
                    // 添加点击事件来触发播放
                    const playOnClick = async () => {
                        try {
                            await productVideo.play();
                            console.log('✅ 用户交互后视频播放成功');
                            updateProductStatus('✅ 摄像头已开启并运行中');
                        } catch (e) {
                            console.error('❌ 用户交互后播放也失败:', e);
                        }
                        document.removeEventListener('click', playOnClick);
                        document.removeEventListener('touchstart', playOnClick);
                    };
                    document.addEventListener('click', playOnClick, { once: true });
                    document.addEventListener('touchstart', playOnClick, { once: true });
                }
                
                // 保存stream引用以便后续停止
                window.productVideoStream = stream;
                
                // 添加视频事件监听
                productVideo.onplay = () => {
                    console.log('✅ 视频正在播放');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.onloadeddata = () => {
                    console.log('✅ 视频数据已加载');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.oncanplay = () => {
                    console.log('✅ 视频可以播放');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.onerror = (err) => {
                    console.error('❌ 视频播放错误:', err);
                    updateProductStatus('❌ 摄像头播放失败');
                    showError('摄像头播放失败，请刷新页面重试');
                };
                
                // 检查视频是否真的在播放
                setTimeout(() => {
                    if (productVideo.readyState >= 2 && productVideo.videoWidth > 0) {
                        console.log('✅ 摄像头确认运行中:', {
                            readyState: productVideo.readyState,
                            videoWidth: productVideo.videoWidth,
                            videoHeight: productVideo.videoHeight,
                            paused: productVideo.paused,
                            ended: productVideo.ended
                        });
                        updateProductStatus('✅ 摄像头已开启并运行中');
                    } else {
                        console.warn('⚠️ 摄像头可能未正常启动:', {
                            readyState: productVideo.readyState,
                            videoWidth: productVideo.videoWidth,
                            videoHeight: productVideo.videoHeight,
                            paused: productVideo.paused
                        });
                        updateProductStatus('⚠️ 摄像头启动中，请稍候...');
                    }
                }, 2000);
                
                return true;
            } catch (err) {
                console.error('❌ 摄像头启动失败:', err);
                debugLog(`❌ 摄像头启动失败: ${err.name} - ${err.message}`, 'error');
                let errorMsg = '无法访问摄像头: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问摄像头权限\\n\\n请在浏览器设置中允许摄像头访问';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到摄像头设备\\n\\n请检查摄像头是否已连接';
                } else if (err.name === 'NotReadableError') {
                    errorMsg += '摄像头被其他程序占用\\n\\n请关闭其他使用摄像头的应用';
                } else {
                    errorMsg += (err.message || '未知错误');
                }
                showError(errorMsg);
                updateProductStatus('❌ 摄像头启动失败: ' + err.name);
                return false;
            }
        }
        
        function stopCameraForProduct() {
            const productVideo = document.getElementById('productVideo');
            if (productVideo && productVideo.srcObject) {
                const stream = productVideo.srcObject;
                stream.getTracks().forEach(track => track.stop());
                productVideo.srcObject = null;
            }
            if (window.productVideoStream) {
                window.productVideoStream.getTracks().forEach(track => track.stop());
                window.productVideoStream = null;
            }
        }
        
        async function startVisualNavigationForProduct() {
            const productVideo = document.getElementById('productVideo');
            const productCanvas = document.getElementById('productCanvas');
            
            if (!productVideo || !productVideo.srcObject) {
                console.warn('摄像头未就绪，等待中...');
                // 等待摄像头就绪
                await new Promise(resolve => {
                    const checkReady = () => {
                        if (productVideo && productVideo.srcObject && productVideo.readyState >= 2) {
                            resolve();
                        } else {
                            setTimeout(checkReady, 100);
                        }
                    };
                    checkReady();
                });
            }
            
            // 显示结果区域
            document.getElementById('productGuidance').style.display = 'block';
            document.getElementById('guidanceMessages').innerHTML = '<div style="color:#4CAF50;">🎥 环境扫描已启动，正在分析周围环境...</div>';
            
            // 优化：降低检测频率到1-2秒，提高响应速度
            let lastFrameTime = 0;
            let frameSkipCount = 0;
            // 每3帧检测一次(约0.5-1秒,假设30fps)
            // 优化:提高检测频率
            const FRAME_SKIP = 3;
            // 最小间隔0.8秒(优化:提高响应速度,目标<1秒)
            const MIN_INTERVAL = 800;
            let isAnalyzing = false; // 防止并发分析
            
            function analyzeFrame() {
                if (!productModeActive) return;
                
                const now = Date.now();
                frameSkipCount++;
                
                // 如果正在分析中，跳过本次
                if (isAnalyzing) {
                    requestAnimationFrame(analyzeFrame);
                    return;
                }
                
                // 检查时间间隔和帧数
                if (now - lastFrameTime < MIN_INTERVAL || frameSkipCount < FRAME_SKIP) {
                    requestAnimationFrame(analyzeFrame);
                    return;
                }
                
                frameSkipCount = 0;
                lastFrameTime = now;
                
                // 执行检测（异步，不阻塞）- 使用统一入口
                analyzeVisualGuidanceFrame().finally(() => {
                    isAnalyzing = false;
                });
                
                // 继续下一帧
                requestAnimationFrame(analyzeFrame);
            }
            
            // 开始检测循环
            requestAnimationFrame(analyzeFrame);
            
            // 立即执行一次（不等待）- 使用统一入口
            analyzeVisualGuidanceFrame();
        }
        // 调试日志函数（在页面上显示，方便iPhone Safari调试）
        function debugLog(message, type = 'info') {
            const debugDiv = document.getElementById('debugInfo');
            const debugLogDiv = document.getElementById('debugLog');
            if (debugDiv && debugLogDiv) {
                debugDiv.style.display = 'block';
                const time = new Date().toLocaleTimeString();
                const color = type === 'error' ? '#F44336' : type === 'warn' ? '#FF9800' : '#2196F3';
                const icon = type === 'error' ? '❌' : type === 'warn' ? '⚠️' : 'ℹ️';
                debugLogDiv.innerHTML += `<div style="color:${color}; margin-bottom:3px;">[${time}] ${icon} ${message}</div>`;
                // 自动滚动到底部
                debugDiv.scrollTop = debugDiv.scrollHeight;
            }
            // 同时输出到控制台（如果可用）
            if (console && console.log) {
                console.log(message);
            }
        }
        
        function updateProductStatus(text) {
            const statusDiv = document.getElementById('productStatusDetails');
            if (statusDiv) {
                statusDiv.innerHTML = `<div>${new Date().toLocaleTimeString()}</div><div>${text}</div>`;
            }
        }
        
        // 持续语音监听模式（优化版：实时检测）
        function startVoiceListening() {
            // 确保函数暴露到全局作用域
            window.startVoiceListening = startVoiceListening;
            if (voiceListeningInterval) {
                console.log('⚠️ 语音监听已在运行中');
                return Promise.resolve(); // 已在运行
            }
            
            // 保持音频流持续开启，避免重复请求权限
            let continuousAudioStream = null;
            let isRecording = false;
            
            console.log('🎤 开始启动语音监听...');
            updateProductStatus('正在请求麦克风权限...');
            
            return navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
                continuousAudioStream = stream;
                console.log('✅ 麦克风权限已授予');
                updateProductStatus('✅ 麦克风已开启，正在监听...');
                return stream;
            }).catch((err) => {
                console.error('❌ 无法获取音频流:', err);
                let errorMsg = '无法访问麦克风: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问麦克风权限';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到麦克风设备';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                showError(errorMsg);
                updateProductStatus('❌ 麦克风启动失败: ' + err.name);
                throw err;
            }).then((stream) => {
                if (!stream) return;
                
                // 使用AudioContext进行实时语音检测
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const analyser = audioContext.createAnalyser();
                const microphone = audioContext.createMediaStreamSource(continuousAudioStream);
                microphone.connect(analyser);
                
                analyser.fftSize = 128; // 优化：降低FFT大小减少计算量
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);
                
                // 语音活动检测参数
                const SILENCE_THRESHOLD = 30; // 静音阈值
                const SPEECH_THRESHOLD = 50;  // 语音阈值
                let silenceCount = 0;
                let speechCount = 0;
                let recordingStartTime = null;
                const MIN_RECORDING_TIME = 0.5; // 最小录音时间（秒）
                const MAX_RECORDING_TIME = 2.0;  // 最大录音时间（秒）
                
                let audioChunksForVAD = [];
                let mediaRecorderForVAD = null;
                
                // 开始录音
                function startRecording() {
                    if (isRecording) return;
                    
                    isRecording = true;
                    recordingStartTime = Date.now();
                    audioChunksForVAD = [];
                    
                    let options = {};
                    if (MediaRecorder.isTypeSupported('audio/webm')) {
                        options = { mimeType: 'audio/webm' };
                    } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                        options = { mimeType: 'audio/mp4' };
                    }
                    
                    mediaRecorderForVAD = new MediaRecorder(continuousAudioStream, options);
                    
                    mediaRecorderForVAD.ondataavailable = (event) => {
                        if (event.data && event.data.size > 0) {
                            audioChunksForVAD.push(event.data);
                        }
                    };
                    
                    mediaRecorderForVAD.onstop = () => {
                        if (audioChunksForVAD.length > 0) {
                            const audioBlob = new Blob(audioChunksForVAD, { type: mediaRecorderForVAD.mimeType || 'audio/webm' });
                            recognizeAndRespond(audioBlob).catch((err) => {
                                console.error('语音识别失败:', err);
                            });
                        }
                        isRecording = false;
                    };
                    
                    mediaRecorderForVAD.start();
                    
                    // 更新状态
                    const voiceStatusDiv = document.getElementById('voiceStatusText');
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#F44336;">🔴 正在录音...</span>';
                    }
                }
                
                // 停止录音
                function stopRecording() {
                    if (!isRecording || !mediaRecorderForVAD) return;
                    
                    const recordingDuration = (Date.now() - recordingStartTime) / 1000;
                    
                    // 如果录音时间太短，忽略
                    if (recordingDuration < MIN_RECORDING_TIME) {
                        isRecording = false;
                        return;
                    }
                    
                    if (mediaRecorderForVAD.state !== 'inactive') {
                        mediaRecorderForVAD.stop();
                    }
                    
                    // 更新状态：显示正在识别
                    const voiceStatusDiv = document.getElementById('voiceStatusText');
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#FF9800;">🟡 正在识别...</span>';
                    }
                }
                
                // 实时检测循环（优化：降低检测频率到200ms）
                function detectVoiceActivity() {
                    if (!productModeActive) {
                        if (isRecording) {
                            stopRecording();
                        }
                        return;
                    }
                    
                    analyser.getByteFrequencyData(dataArray);
                    
                    // 计算平均音量
                    let sum = 0;
                    for (let i = 0; i < bufferLength; i++) {
                        sum += dataArray[i];
                    }
                    const average = sum / bufferLength;
                    
                    if (average > SPEECH_THRESHOLD) {
                        // 检测到语音
                        speechCount++;
                        silenceCount = 0;
                        
                        if (!isRecording && speechCount > 2) {
                            // 连续2次检测到语音，开始录音
                            startRecording();
                        }
                    } else if (average < SILENCE_THRESHOLD) {
                        // 检测到静音
                        silenceCount++;
                        speechCount = 0;
                        
                        if (isRecording) {
                            const recordingDuration = (Date.now() - recordingStartTime) / 1000;
                            
                            // 如果静音超过0.5秒或录音超过最大时间，停止录音
                            if (silenceCount > 5 || recordingDuration >= MAX_RECORDING_TIME) {
                                stopRecording();
                            }
                        }
                    } else {
                        // 中间状态，重置计数
                        speechCount = Math.max(0, speechCount - 1);
                        silenceCount = Math.max(0, silenceCount - 1);
                    }
                    
                    // 优化：200ms检测一次（而不是每帧）
                    setTimeout(detectVoiceActivity, 200);
                }
                
                // 开始检测
                console.log('✅ 语音活动检测已启动');
                detectVoiceActivity();
                
                // 保存引用以便停止
                voiceListeningInterval = {
                    stop: () => {
                        console.log('🛑 停止语音监听...');
                        if (continuousAudioStream) {
                            continuousAudioStream.getTracks().forEach(track => track.stop());
                        }
                        if (audioContext) {
                            audioContext.close();
                        }
                        if (mediaRecorderForVAD && mediaRecorderForVAD.state !== 'inactive') {
                            mediaRecorderForVAD.stop();
                        }
                        voiceListeningInterval = null;
                        const voiceStatusDiv = document.getElementById('voiceStatusText');
                        if (voiceStatusDiv) {
                            voiceStatusDiv.innerHTML = '<span style="color:#999;">已停止监听</span>';
                        }
                    }
                };
            });
        }
        
        function stopVoiceListening() {
            if (voiceListeningInterval) {
                if (typeof voiceListeningInterval.stop === 'function') {
                    voiceListeningInterval.stop();
                } else {
                    clearInterval(voiceListeningInterval);
                }
                voiceListeningInterval = null;
            }
            const voiceStatusDiv = document.getElementById('voiceStatusText');
            if (voiceStatusDiv) {
                voiceStatusDiv.textContent = '语音监听已停止';
            }
            const voiceResultDiv = document.getElementById('voiceRecognitionResult');
            if (voiceResultDiv) {
                voiceResultDiv.style.display = 'none';
            }
        }
        
        async function captureAndRecognizeVoice() {
            try {
                // 更新状态：显示正在录音
                const voiceStatusDiv = document.getElementById('voiceStatusText');
                if (voiceStatusDiv) {
                    voiceStatusDiv.innerHTML = '<span style="color:#F44336;">🔴 正在录音...</span>';
                }
                
                const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];
                
                let options = {};
                if (MediaRecorder.isTypeSupported('audio/webm')) {
                    options = { mimeType: 'audio/webm' };
                } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                    options = { mimeType: 'audio/mp4' };
                }
                
                const recorder = new MediaRecorder(audioStream, options);
                
                recorder.ondataavailable = (event) => {
                    if (event.data && event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                recorder.onstop = async () => {
                    // 更新状态：显示正在识别
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#FF9800;">🟡 正在识别...</span>';
                    }
                    
                    const audioBlob = new Blob(audioChunks, { type: recorder.mimeType || 'audio/webm' });
                    await recognizeAndRespond(audioBlob);
                    
                    // 更新状态：显示监听中
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#1976D2;">🎤 正在监听...</span>';
                    }
                    
                    audioStream.getTracks().forEach(track => track.stop());
                };
                
                recorder.start();
                
                // 录音1.5秒
                setTimeout(() => {
                    if (recorder.state !== 'inactive') {
                        recorder.stop();
                    }
                }, 1500);
            } catch (err) {
                console.error('启动录音失败:', err);
                const voiceStatusDiv = document.getElementById('voiceStatusText');
                if (voiceStatusDiv) {
                    voiceStatusDiv.innerHTML = '<span style="color:#F44336;">❌ 录音失败: ' + (err.message || '未知错误') + '</span>';
                }
            }
        }
        
        async function recognizeAndRespond(audioBlob) {
            try {
                const formData = new FormData();
                formData.append('audio', audioBlob);
                
                const response = await fetch('/api/recognize/voice', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                // 显示识别结果（无论成功与否）
                const voiceResultDiv = document.getElementById('voiceRecognitionResult');
                if (voiceResultDiv) {
                    voiceResultDiv.style.display = 'block';
                }
                
                if (data.success && data.text && data.text.trim()) {
                    const recognizedText = data.text.trim();
                    const now = Date.now();
                    
                    // 避免重复识别（3秒内相同文本）
                    if (now - lastVoiceRecognitionTime < 3000) {
                        if (voiceResultDiv) {
                            voiceResultDiv.innerHTML = '<div style="color:#999;">识别中（避免重复）...</div>';
                        }
                        return;
                    }
                    lastVoiceRecognitionTime = now;
                    
                    // 显示识别结果
                    if (voiceResultDiv) {
                        voiceResultDiv.innerHTML = 
                            `<div style="color:#1976D2;"><strong>识别：</strong>${recognizedText}</div>`;
                    }
                    
                    // 处理语音指令
                    await processVoiceCommand(recognizedText);
                } else {
                    // 识别失败或没有识别到内容
                    if (voiceResultDiv) {
                        const errorMsg = data.error || '未识别到语音内容';
                        voiceResultDiv.innerHTML = `<div style="color:#999;">${errorMsg}</div>`;
                    }
                    console.log('语音识别结果:', data);
                }
            } catch (err) {
                console.error('语音识别错误:', err);
                const voiceResultDiv = document.getElementById('voiceRecognitionResult');
                if (voiceResultDiv) {
                    voiceResultDiv.style.display = 'block';
                    voiceResultDiv.innerHTML = `<div style="color:#F44336;">识别错误: ${err.message}</div>`;
                }
            }
        }
        
        async function processVoiceCommand(text) {
            const lowerText = text.toLowerCase();
            
            // 导航相关指令
            if (lowerText.includes('导航') || lowerText.includes('去') || lowerText.includes('到')) {
                // 提取目的地
                const destinationMatch = text.match(/(?:去|到|导航)(.+)/);
                if (destinationMatch) {
                    const destination = destinationMatch[1].trim();
                    if (window.speakText) {
                        window.speakText(`好的，我将为您导航到${destination}`, 'cheerful');
                    }
                    // 这里可以调用导航API
                }
            }
            // 停止指令
            else if (lowerText.includes('停止') || lowerText.includes('暂停')) {
                if (window.speakText) {
                    window.speakText('好的，已暂停', 'calm');
                }
            }
            // 继续指令
            else if (lowerText.includes('继续') || lowerText.includes('恢复')) {
                if (window.speakText) {
                    window.speakText('好的，继续导航', 'cheerful');
                }
            }
            // 帮助指令
            else if (lowerText.includes('帮助') || lowerText.includes('怎么用')) {
                if (window.speakText) {
                    window.speakText('我可以帮您导航、识别物体、检测障碍。请告诉我您要去哪里', 'calm');
                }
            }
            // 默认响应
            else {
                if (window.speakText) {
                    window.speakText('我听到了，请告诉我您需要什么帮助', 'calm');
                }
            }
        }
        
        // ========== 优先级TTS播放队列管理器（升级版：Worker Loop架构）==========
        class PriorityTTSQueue {
            constructor() {
                this.queue = [];
                this.priorityLevels = {
                    'critical': 0,  // 台阶、危险（最高优先级）
                    'high': 1,      // 转向提示
                    'medium': 2,    // 标识牌
                    'low': 3        // 普通提示
                };
                this.stats = {
                    totalPlayed: 0,
                    totalInterrupted: 0,
                    latencyHistory: []
                };
            }
            
            getPriorityLevel(style, message) {
                // 根据消息内容和风格确定优先级
                if (message.includes('台阶') || message.includes('危险')) {
                    return this.priorityLevels.critical;
                } else if (message.includes('左转') || message.includes('右转')) {
                    return this.priorityLevels.high;
                } else if (message.includes('洗手间') || message.includes('电梯')) {
                    return this.priorityLevels.medium;
                } else {
                    return this.priorityLevels.low;
                }
            }
            
            enqueue(item) {
                // item: { text, style, priority, options, id? }
                this.queue.push(item);
                // 按优先级排序（数字越小优先级越高）
                this.queue.sort((a, b) => {
                    const pa = typeof a.priority === 'number' ? a.priority : this.getPriorityLevel(a.style || 'calm', a.text || '');
                    const pb = typeof b.priority === 'number' ? b.priority : this.getPriorityLevel(b.style || 'calm', b.text || '');
                    return pa - pb;
                });
            }
            
            dequeue() {
                return this.queue.shift() || null;
            }
            
            isEmpty() {
                return this.queue.length === 0;
            }
            
            getStats() {
                const latencies = this.stats.latencyHistory.map(h => h.latency);
                const avgLatency = latencies.length > 0 
                    ? latencies.reduce((a, b) => a + b, 0) / latencies.length 
                    : 0;
                const maxLatency = latencies.length > 0 ? Math.max(...latencies) : 0;
                
                return {
                    totalPlayed: this.stats.totalPlayed,
                    totalInterrupted: this.stats.totalInterrupted,
                    avgLatency: Math.round(avgLatency),
                    maxLatency: maxLatency,
                    queueLength: this.queue.length
                };
            }
        }
        
        // 创建全局优先级队列管理器
        const priorityTTSQueue = new PriorityTTSQueue();
        window.priorityTTSQueue = priorityTTSQueue;
        
        // TTS播放队列（保留兼容性）
        let ttsQueue = [];
        let isPlayingTTS = false;
        
        // ========== TTS Worker Loop（独立后台线程）==========
        (function () {
            'use strict';
            
            const TTS_WORKER_INTERVAL_MS = 200; // 轮询间隔，200ms 足够平滑
            
            function log(event, payload) {
                if (window.__lunaLog) {
                    window.__lunaLog(event, payload);
                } else {
                    // console.log('[TTSWorker]', event, payload);
                }
            }
            
            const TTSWorker = {
                isRunning: false,
                isPlaying: false,
                timer: null,
                lastPlayId: 0,
                currentAudio: null,
                currentPriority: 999,
                
                start() {
                    if (this.isRunning) return;
                    this.isRunning = true;
                    this.loop();
                    log('tts_worker_started', {});
                },
                
                stop() {
                    this.isRunning = false;
                    if (this.timer) {
                        clearTimeout(this.timer);
                        this.timer = null;
                    }
                    log('tts_worker_stopped', {});
                },
                
                loop() {
                    if (!this.isRunning) return;
                    
                    // 如果正在播报，就稍后再检查
                    if (this.isPlaying) {
                        this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                        return;
                    }
                    
                    // 队列为空也不急，过会再看
                    if (!window.priorityTTSQueue || window.priorityTTSQueue.isEmpty()) {
                        this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                        return;
                    }
                    
                    // 取队列中优先级最高的一条
                    const item = window.priorityTTSQueue.dequeue();
                    if (!item) {
                        this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                        return;
                    }
                    
                    const id = ++this.lastPlayId;
                    const text = item.text || '';
                    const style = item.style || 'calm';
                    const priority = typeof item.priority === 'number' ? item.priority : window.priorityTTSQueue.getPriorityLevel(style, text);
                    
                    this.isPlaying = true;
                    this.currentPriority = priority;
                    log('tts_start_play', { id, text: text.substring(0, 50), style, priority });
                    
                    // 调用 _playTTS 播放
                    Promise.resolve()
                        .then(() => _playTTS(text, style))
                        .then((audio) => {
                            if (audio) {
                                this.currentAudio = audio;
                                // 保存原有的 onended 回调（如果有）
                                const originalOnEnded = audio.onended;
                                
                                // 播放结束回调（在原有回调之后执行）
                                audio.onended = () => {
                                    // 先执行原有清理逻辑（如果有）
                                    if (originalOnEnded) {
                                        try {
                                            originalOnEnded.call(audio);
                                        } catch (e) {
                                            console.warn('原始onended回调执行失败:', e);
                                        }
                                    }
                                    // Worker 自己的逻辑
                                    this.currentAudio = null;
                                    this.currentPriority = 999;
                                    this.isPlaying = false;
                                    window.priorityTTSQueue.stats.totalPlayed++;
                                    log('tts_finish', { id, text: text.substring(0, 50) });
                                    // 继续循环
                                    this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                                };
                                
                                // 播放错误回调
                                audio.onerror = (err) => {
                                    this.currentAudio = null;
                                    this.currentPriority = 999;
                                    this.isPlaying = false;
                                    log('tts_error', { id, text: text.substring(0, 50), error: err ? err.toString() : 'unknown' });
                                    // 继续循环
                                    this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                                };
                            } else {
                                this.isPlaying = false;
                                log('tts_error', { id, text: text.substring(0, 50), error: 'audio creation failed' });
                                this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                            }
                        })
                        .catch(err => {
                            this.isPlaying = false;
                            this.currentAudio = null;
                            this.currentPriority = 999;
                            log('tts_error', { id, text: text.substring(0, 50), error: err ? err.toString() : 'unknown' });
                            // 继续循环，不中断
                            this.timer = setTimeout(() => this.loop(), TTS_WORKER_INTERVAL_MS);
                        });
                }
            };
            
            // 统一的 enqueueTTS 入口（所有地方都用这个，非阻塞）
            // ✅ 修复：添加 priority 容错处理
            window.enqueueTTS = function (text, options) {
                if (!text) return;
                
                const style = (options && options.style) || 'calm';
                // ✅ 容错：如果 options.priority 存在，忽略它，不抛出异常
                // ✅ 始终使用 getPriorityLevel 计算优先级
                const priority = window.priorityTTSQueue ? window.priorityTTSQueue.getPriorityLevel(style, text) : 3;
                
                const item = {
                    text,
                    style,
                    priority,
                    options: options || {}
                };
                
                log('tts_enqueued', {
                    text: text.substring(0, 50),
                    priority,
                    style
                });
                
                if (!window.priorityTTSQueue) {
                    window.priorityTTSQueue = new PriorityTTSQueue();
                }
                
                window.priorityTTSQueue.enqueue(item);
                TTSWorker.start(); // 确保 worker 在运行
            };
            
            // 导出给其他模块用
            window.TTSWorker = TTSWorker;
            
            // 非阻塞版本的 speakText（兼容旧代码）
            // ✅ 修复：移除 priority 参数，添加容错处理
            window.speakText = function (text, style = 'calm', priority = false) {
                // ✅ 容错：如果 priority 参数存在，忽略它（不抛出异常）
                // ✅ 记录 speakText 调用日志
                if (window.NavLog) {
                    window.NavLog.info("TTS", "speakText调用", { text: text.substring(0, 100), style });
                }
                // ✅ 不再使用 priority 参数，直接使用默认优先级
                window.enqueueTTS(text, { style });
            };
        })();
        
        async function _playTTS(text, style = 'calm') {
            isPlayingTTS = true;
            let audioElement = null;
            // ✅ 修复：添加错误处理，确保即使出错也触发播报结束信号
            try {
                // 显示播放状态
                const playbackDiv = document.getElementById('voicePlaybackStatus');
                const playbackTextDiv = document.getElementById('playbackText');
                if (playbackDiv) {
                    playbackDiv.style.display = 'block';
                    playbackDiv.style.background = '#fff3cd';
                    if (playbackTextDiv) {
                        playbackTextDiv.textContent = text;
                    }
                }
                
                const startTime = Date.now();
                const response = await fetch('/api/tts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, style })
                });
                
                const data = await response.json();
                
                const ttsTime = Date.now() - startTime;
                console.log(`TTS生成时间: ${ttsTime}ms${data.cached ? ' ⚡(缓存)' : ''}`);
                
                if (data.success && data.audio) {
                    // 直接使用base64数据创建Blob，避免额外请求
                    const base64Data = data.audio;
                    const byteCharacters = atob(base64Data);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const audioBlob = new Blob([byteArray], { type: 'audio/mp3' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    audioElement = audio; // 保存引用，用于优先级队列管理
                    
                    // 设置初始音量
                    audio.volume = currentAudioVolume;
                    
                    // 添加到全局音频列表
                    if (!window.currentPlayingAudios) {
                        window.currentPlayingAudios = [];
                    }
                    window.currentPlayingAudios.push(audio);
                    
                    // 播放开始
                    audio.onplay = () => {
                        const playTime = Date.now() - startTime;
                        console.log(`TTS总延迟: ${playTime}ms${data.cached ? ' ⚡(缓存)' : ''}`);
                        
                        // ✅ 记录 TTS 开始播报日志
                        if (window.NavLog) {
                            window.NavLog.info("TTS", "开始播报", { text: text.substring(0, 100), style, delay: playTime, cached: data.cached });
                        }
                        
                        // ③【新增：后台日志上传】
                        if (window.sendLog) {
                            window.sendLog({ type: 'tts_play', text: text ? text.substring(0, 100) : '', style, delay: playTime });
                        }
                        if (playbackDiv) {
                            playbackDiv.style.display = 'block';
                            playbackDiv.style.background = '#d4edda';
                            playbackDiv.innerHTML = '<div style="color:#155724;">🔊 正在播放语音...</div><div style="margin-top:5px; color:#666;">' + text + '</div>';
                        }
                    };
                    
                    // ✅ 修复：播放结束（统一处理，确保安全回调）
                    audio.onended = () => {
                        try {
                            isPlayingTTS = false;
                            // 从全局音频列表移除
                            const index = window.currentPlayingAudios.indexOf(audio);
                            if (index > -1) {
                                window.currentPlayingAudios.splice(index, 1);
                            }
                            if (playbackDiv) {
                                playbackDiv.style.display = 'none';
                            }
                            URL.revokeObjectURL(audioUrl);
                            
                            // ✅ 记录 TTS 播报完成日志
                            if (window.NavLog) {
                                window.NavLog.info("TTS", "播报完成", { text: text.substring(0, 100), style });
                            }
                            
                            // ✅ 修复：完整产品模式 - 记录播报完成
                            console.log('[FullMode] TTS finished, ready for next trigger', {
                                text: text.substring(0, 50),
                                isProductModeRunning: isProductModeRunning
                            });
                            
                            // ✅ 安全回调：确保无论成功还是失败，都会触发"本次播报完成"
                            // 触发自定义事件，供其他模块监听
                            if (window.dispatchEvent) {
                                window.dispatchEvent(new CustomEvent('ttsFinished', {
                                    detail: { text, style, success: true }
                                }));
                            }
                            
                            // 注意：TTSWorker 会在自己的 onended 回调中继续循环，这里不需要额外处理
                        } catch (err) {
                            console.error('[FullMode] Error in audio.onended callback:', err);
                            // ✅ 即使回调出错，也确保状态重置
                            isPlayingTTS = false;
                            if (window.dispatchEvent) {
                                window.dispatchEvent(new CustomEvent('ttsFinished', {
                                    detail: { text, style, success: false, error: err.toString() }
                                }));
                            }
                        }
                    };
                    
                    // ✅ 修复：播放错误（确保安全回调）
                    audio.onerror = (err) => {
                        try {
                            isPlayingTTS = false;
                            console.error('音频播放错误:', err);
                            if (playbackDiv) {
                                playbackDiv.style.display = 'none';
                            }
                            URL.revokeObjectURL(audioUrl);
                            showError('语音播报失败，请检查音频权限');
                            
                            // ✅ 修复：完整产品模式 - 记录播报失败
                            console.log('[FullMode] TTS error, ready for next trigger', {
                                text: text.substring(0, 50),
                                error: err.toString(),
                                isProductModeRunning: isProductModeRunning
                            });
                            
                            // ✅ 安全回调：确保错误时也触发"本次播报完成"
                            if (window.dispatchEvent) {
                                window.dispatchEvent(new CustomEvent('ttsFinished', {
                                    detail: { text, style, success: false, error: err.toString() }
                                }));
                            }
                            
                            // 继续播放队列
                            if (ttsQueue.length > 0) {
                                const next = ttsQueue.shift();
                                _playTTS(next.text, next.style);
                            }
                        } catch (callbackErr) {
                            console.error('[FullMode] Error in audio.onerror callback:', callbackErr);
                            // ✅ 即使回调出错，也确保状态重置
                            isPlayingTTS = false;
                            if (window.dispatchEvent) {
                                window.dispatchEvent(new CustomEvent('ttsFinished', {
                                    detail: { text, style, success: false, error: callbackErr.toString() }
                                }));
                            }
                        }
                    };
                    
                    // 尝试播放（添加用户交互检查和音量设置）
                    try {
                        // 确保音频已解锁
                        await unlockAudio();
                        
                        // 设置音量（使用当前音量设置）
                        audio.volume = currentAudioVolume;
                        
                        // 检查是否需要用户交互
                        const playPromise = audio.play();
                        
                        if (playPromise !== undefined) {
                            playPromise
                                .then(() => {
                                    console.log('✅ 音频播放成功');
                                })
                                .catch((playError) => {
                                    isPlayingTTS = false;
                                    console.error('播放失败:', playError);
                                    
                                    if (playError.name === 'NotAllowedError' || playError.name === 'NotSupportedError') {
                                        // 浏览器阻止自动播放，需要用户交互
                                        const errorMsg = '需要用户交互才能播放音频。请点击页面任意位置后，音频将自动播放。如果问题持续，请检查浏览器音频权限设置。';
                                        showError(errorMsg);
                                        
                                        // 尝试解锁音频（使用Promise链式调用，不使用await）
                                        unlockAudio().then(() => {
                                            // 添加点击事件监听，用户点击后重试播放
                                            const retryPlay = async () => {
                                                try {
                                                    await unlockAudio();
                                                    audio.volume = currentAudioVolume;
                                                    await audio.play();
                                                    console.log('✅ 用户交互后播放成功');
                                                    document.removeEventListener('click', retryPlay);
                                                    document.removeEventListener('touchstart', retryPlay);
                                                } catch (e) {
                                                    console.error('重试播放失败:', e);
                                                    showError('播放失败: ' + (e.message || '请检查浏览器音频权限设置'));
                                                }
                                            };
                                            
                                            document.addEventListener('click', retryPlay, { once: true });
                                            document.addEventListener('touchstart', retryPlay, { once: true });
                                        }).catch((err) => {
                                            console.error('解锁音频失败:', err);
                                        });
                                    } else {
                                        showError(`语音播报失败: ${playError.message || '未知错误'}\n\n错误类型: ${playError.name}`);
                                    }
                                    
                                    if (playbackDiv) {
                                        playbackDiv.style.display = 'none';
                                    }
                                    URL.revokeObjectURL(audioUrl);
                                    
                                    // 继续播放队列
                                    if (ttsQueue.length > 0) {
                                        const next = ttsQueue.shift();
                                        _playTTS(next.text, next.style);
                                    }
                                });
                        }
                    } catch (playError) {
                        isPlayingTTS = false;
                        console.error('播放异常:', playError);
                        showError('语音播报失败: ' + (playError.message || '未知错误'));
                        if (playbackDiv) {
                            playbackDiv.style.display = 'none';
                        }
                        URL.revokeObjectURL(audioUrl);
                        
                        // 继续播放队列
                        if (ttsQueue.length > 0) {
                            const next = ttsQueue.shift();
                            _playTTS(next.text, next.style);
                        }
                    }
                } else {
                    isPlayingTTS = false;
                    console.error('TTS API返回失败:', data);
                    if (playbackDiv) {
                        playbackDiv.style.display = 'none';
                    }
                }
            } catch (err) {
                isPlayingTTS = false;
                console.error('语音播报错误:', err);
                const playbackDiv = document.getElementById('voicePlaybackStatus');
                if (playbackDiv) {
                    playbackDiv.style.display = 'none';
                }
                // ✅ 修复：确保错误时也触发播报结束信号，恢复监听系统
                // ✅ 记录 TTS 播报失败日志
                if (window.NavLog) {
                    window.NavLog.info("TTS", "播报失败", { text: text ? text.substring(0, 100) : '', style, error: err.toString() });
                }
                
                // ✅ 修复：完整产品模式 - 记录播报失败
                console.log('[FullMode] TTS catch error, ready for next trigger', {
                    text: text ? text.substring(0, 50) : '',
                    error: err.toString(),
                    isProductModeRunning: isProductModeRunning
                });
                
                // ✅ 安全回调：确保 catch 错误时也触发"本次播报完成"
                if (window.dispatchEvent) {
                    window.dispatchEvent(new CustomEvent('ttsFinished', {
                        detail: { text: text || '', style, success: false, error: err.toString() }
                    }));
                }
                
                // ✅ 确保 TTSWorker 继续循环
                if (window.TTSWorker && window.TTSWorker.timer) {
                    window.TTSWorker.timer = setTimeout(() => window.TTSWorker.loop(), 300);
                }
            }
            
            return audioElement; // 返回audio元素，用于优先级队列管理
        }
        
        // ========== 镜头运动检测（ChatGPT建议优化）==========
        const cameraMotionState = {
            lastFrame: null,
            motionDetected: false,
            lastMotionTime: 0,
            motionThreshold: 0.15,  // 运动阈值（帧差百分比）
            stabilityThreshold: 300  // 稳定阈值（ms）
        };
        
        function detectCameraMotion(currentFrameData) {
            if (!cameraMotionState.lastFrame) {
                cameraMotionState.lastFrame = currentFrameData;
                return false;
            }
            
            // 计算帧差（简化版：比较图像数据哈希）
            const currentHash = simpleHash(currentFrameData);
            const lastHash = cameraMotionState.lastFrame;
            
            // 如果哈希差异超过阈值，认为有运动
            const diff = Math.abs(currentHash - lastHash) / Math.max(currentHash, lastHash);
            
            if (diff > cameraMotionState.motionThreshold) {
                cameraMotionState.motionDetected = true;
                cameraMotionState.lastMotionTime = Date.now();
            } else {
                // 如果超过稳定阈值，认为镜头已稳定
                if (Date.now() - cameraMotionState.lastMotionTime > cameraMotionState.stabilityThreshold) {
                    cameraMotionState.motionDetected = false;
                }
            }
            
            cameraMotionState.lastFrame = currentHash;
            return cameraMotionState.motionDetected;
        }
        
        function simpleHash(data) {
            // 简单的哈希函数（用于快速比较）
            if (typeof data === 'string') {
                let hash = 0;
                for (let i = 0; i < data.length; i++) {
                    hash = ((hash << 5) - hash) + data.charCodeAt(i);
                    hash = hash & hash;
                }
                return hash;
            }
            return data;
        }
        
        // ========== 冷却时间配置（ChatGPT建议优化）==========
        const COOL_DOWN_MS = {
            'step': 2000,        // 台阶：2秒（降低，提高响应速度）
            'hazard': 1500,      // 危险：1.5秒（降低，确保及时播报）
            'direction': 2000,   // 转向：2秒
            'signboard': 5000,   // 标识牌：5秒
            'room': 3000,        // 房间号：3秒
            'default': 2000      // 默认：2秒（降低）
        };
        
        function getCooldownTime(message) {
            if (message.includes('台阶')) return COOL_DOWN_MS.step;
            if (message.includes('危险')) return COOL_DOWN_MS.hazard;
            if (message.includes('左转') || message.includes('右转')) return COOL_DOWN_MS.direction;
            if (message.includes('洗手间') || message.includes('电梯') || message.includes('出口')) return COOL_DOWN_MS.signboard;
            if (message.includes('房间号')) return COOL_DOWN_MS.room;
            return COOL_DOWN_MS.default;
        }
        
        // 判断是否为紧急消息（需要立即播报，不受镜头运动限制）
        function isUrgentMessage(message) {
            return message.includes('危险') || message.includes('台阶');
        }
        
        // 增强的视觉导航显示（产品模式专用）- 主动提示版（ChatGPT优化）
        let lastSpokenGuidance = {};
        const CAMERA_MOTION_THRESHOLD = 300; // 300ms（ChatGPT建议）
        
        function displayVisualGuidanceForProduct(guidance, visionSummary) {
            // ✅ 安全防护：检查 guidance 参数
            if (!guidance || typeof guidance !== 'object') {
                console.warn("[视觉导航] guidance 数据为空或无效，跳过本次导航播报", guidance);
                return;
            }
            
            if (!guidance.direction) {
                console.warn("[视觉导航] guidance.direction 缺失，跳过本次导航播报", guidance);
                return;
            }
            
            // 更新方向指示
            const directionIcons = {
                'forward': '⬆️',
                'left': '⬅️',
                'right': '➡️',
                'stop': '⛔'
            };
            
            const directionColors = {
                'forward': '#4CAF50',
                'left': '#2196F3',
                'right': '#FF9800',
                'stop': '#F44336'
            };
            
            const direction = guidance.direction || 'forward';
            const icon = directionIcons[direction] || '➡️';
            const color = directionColors[direction] || '#666';
            
            const directionDiv = document.getElementById('guidanceDirection');
            if (directionDiv) {
                directionDiv.innerHTML = `<span style="color:${color}; font-size:24px;">${icon}</span> <span style="color:${color};">${direction.toUpperCase()}</span>`;
            }
            
            // 更新指引消息
            let html = '';
            if (guidance.messages && guidance.messages.length > 0) {
                guidance.messages.forEach(msg => {
                    html += `<div style="padding:8px; margin:5px 0; background:#f5f5f5; border-radius:5px;">${msg}</div>`;
                });
            } else {
                html = '<div style="color:#999;">环境扫描中，未检测到特殊提示</div>';
            }
            const messagesDiv = document.getElementById('guidanceMessages');
            if (messagesDiv) {
                // 保留处理时间信息
                const existingTimeInfo = messagesDiv.innerHTML.match(/处理时间:.*?ms/);
                messagesDiv.innerHTML = html;
                if (existingTimeInfo && visionSummary && visionSummary.processing_time_ms) {
                    messagesDiv.innerHTML += `<div style="margin-top:10px; padding:5px; background:#e8f5e9; border-radius:5px; font-size:11px; color:#2E7D32;">
                        处理时间: ${visionSummary.processing_time_ms}ms | 物体: ${visionSummary.objects_detected || 0} | 文字: ${visionSummary.texts_detected || 0}
                    </div>`;
                }
            }
            
            // ========== 主动语音播报（优化版：确保危险提醒及时播报）==========
            // ========== 指令3：放宽导航巡航语音（避免"只说一句就沉默"）==========
            if (guidance.messages && guidance.messages.length > 0) {
                const now = Date.now();
                
                // 筛选重要消息（台阶、危险、方向、标识牌）
                const importantMessages = guidance.messages.filter(msg => 
                    msg.includes('台阶') || 
                    msg.includes('危险') || 
                    msg.includes('左转') || 
                    msg.includes('右转') || 
                    msg.includes('直行') ||
                    msg.includes('洗手间') ||
                    msg.includes('电梯') ||
                    msg.includes('出口') ||
                    msg.includes('房间号')
                );
                
                // ✅ 新增：专门处理"巡航提示"（无危险，仅提示前方畅通）
                const cruiseMessages = guidance.messages.filter(msg =>
                    msg.includes('前方道路畅通') ||
                    msg.includes('请继续前行') ||
                    msg.includes('请保持直行') ||
                    msg.includes('道路畅通')
                );
                
                // 添加调试日志：记录所有消息
                console.log(`📋 [视觉识别] 收到 ${guidance.messages.length} 条消息，筛选出 ${importantMessages.length} 条重要消息，${cruiseMessages.length} 条巡航消息`);
                if (window.logDebug) {
                    window.logDebug('视觉导航帧结果', {
                        direction: guidance.direction,
                        msg_count: guidance.messages.length,
                        important_count: importantMessages.length,
                        cruise_count: cruiseMessages.length,
                        objects: visionSummary && visionSummary.objects_detected,
                        texts: visionSummary && visionSummary.texts_detected
                    });
                }
                debugLog(`收到 ${guidance.messages.length} 条消息，筛选出 ${importantMessages.length} 条重要消息`, 'info');
                
                // ✅ 巡航消息单独处理（每10-15秒允许播报一次）
                const CRUISE_COOLDOWN = 10000; // 10秒，测试阶段可以再缩短
                if (cruiseMessages.length > 0) {
                    const cruiseKey = '__CRUISE__';
                    const lastCruise = lastSpokenGuidance[cruiseKey] || 0;
                    if (now - lastCruise > CRUISE_COOLDOWN) {
                        const cruiseMsg = cruiseMessages[0];
                        speakText(cruiseMsg, 'info');
                        lastSpokenGuidance[cruiseKey] = now;
                        if (window.logInfo) {
                            window.logInfo('TTS播报', { message: cruiseMsg, reason: 'cruise' });
                        }
                        debugLog(`巡航提示播报: ${cruiseMsg}`, 'info');
                    } else {
                        const cruiseMsg = cruiseMessages[0];
                        if (window.logDebug) {
                            window.logDebug('TTS冷却跳过', { 
                                message: cruiseMsg, 
                                cooldown_left: CRUISE_COOLDOWN - (now - lastCruise) 
                            });
                        }
                    }
                }
                
                if (importantMessages.length > 0) {
                    // 优先处理危险和台阶消息
                    const urgentMessages = importantMessages.filter(msg => isUrgentMessage(msg));
                    const currentMessage = urgentMessages.length > 0 ? urgentMessages[0] : importantMessages[0];
                    const messageKey = currentMessage.substring(0, 30); // 使用前30个字符作为唯一标识（增加长度避免重复）
                    const isUrgent = isUrgentMessage(currentMessage);
                    
                    console.log(`🎯 [TTS决策] 当前消息: "${currentMessage.substring(0, 40)}..." | 是否紧急: ${isUrgent}`);
                    debugLog(`准备处理消息: "${currentMessage.substring(0, 30)}..."`, 'info');
                    
                    // 1. 镜头状态检查（紧急消息不受限制）
                    if (!isUrgent && cameraMotionState.motionDetected && 
                        (now - cameraMotionState.lastMotionTime) < CAMERA_MOTION_THRESHOLD) {
                        // 镜头未稳定，延迟提示或跳过（但紧急消息不受此限制）
                        console.log(`📹 [TTS决策] 镜头运动中，延迟提示: ${currentMessage.substring(0, 20)}...`);
                        if (window.logDebug) {
                            window.logDebug('TTS因镜头运动跳过', { message: currentMessage.substring(0, 30) });
                        }
                        debugLog(`镜头运动中，延迟提示`, 'warn');
                        return;
                    }
                    
                    // 2. 冷却时间检查（紧急消息使用更短的冷却时间）
                    // ✅ 测试阶段：将普通重要消息的默认冷却时间调短（800-1500ms）
                    const cooldownTime = getCooldownTime(currentMessage);
                    const lastSpokenTime = lastSpokenGuidance[messageKey] || 0;
                    const timeSinceLastSpoken = now - lastSpokenTime;
                    
                    if (timeSinceLastSpoken < cooldownTime) {
                        console.log(`⏱️ [TTS决策] 冷却中，跳过提示: ${currentMessage.substring(0, 20)}... (剩余: ${cooldownTime - timeSinceLastSpoken}ms)`);
                        if (window.logDebug) {
                            window.logDebug('TTS冷却跳过', { 
                                message: currentMessage.substring(0, 30), 
                                cooldown_left: cooldownTime - timeSinceLastSpoken 
                            });
                        }
                        debugLog(`冷却中，剩余 ${cooldownTime - timeSinceLastSpoken}ms`, 'warn');
                        return;
                    }
                    
                    // 3. 更新冷却时间记录
                    lastSpokenGuidance[messageKey] = now;
                    
                    // 4. 根据消息类型选择语音风格和优先级
                    let style = 'calm';
                    let priority = false;
                    let reason = 'normal';
                    
                    if (currentMessage.includes('台阶') || currentMessage.includes('危险')) {
                        style = 'urgent'; // 紧急提示
                        priority = true;   // 高优先级（critical）
                        reason = 'urgent';
                    } else if (currentMessage.includes('左转') || currentMessage.includes('右转')) {
                        style = 'cheerful'; // 导航提示
                        priority = true;    // 高优先级（high）
                        reason = 'direction';
                    } else {
                        priority = false;   // 普通优先级（medium/low）
                        reason = 'normal';
                    }
                    
                    // ✅ 指令5：TTS决策分支添加调试日志
                    if (window.logInfo) {
                        window.logInfo('TTS播报', { message: currentMessage, reason: reason });
                    }
                    
                    // 5. 通过EventBridge派发事件（平滑切换方案）
                    // 检测消息类型，通过统一事件流处理
                    if (currentMessage.includes('危险')) {
                        // ②【修复：视觉"误报危险"】- 使用VisualHazardFilter过滤
                        const hazardData = {
                            danger: true,
                            type: currentMessage.match(/危险[：:](.+?)[，,。]/)?.[1] || 
                                 currentMessage.match(/(积水|障碍物|湿滑|施工)/)?.[1] || 'unknown',
                            message: currentMessage,
                            raw: guidance
                        };
                        
                        // 推送到过滤器
                        if (window.VisualHazardFilter) {
                            window.VisualHazardFilter.push(hazardData);
                            
                            // 只有稳定检测到危险才播报
                            if (window.VisualHazardFilter.isDangerStable()) {
                                const hazardType = hazardData.type;
                                if (window.EventBridge) {
                                    window.EventBridge.dispatch("hazard", {
                                        type: hazardType,
                                        level: isUrgent ? 'critical' : 'high',
                                        meta: { message: currentMessage, raw: guidance }
                                    });
                                    // ③【新增：后台日志上传】
                                    if (window.sendLog) {
                                        window.sendLog({ type: 'hazard_detected', frame: hazardData });
                                    }
                                } else {
                                    // 降级：直接调用TTS
                                    speakText(currentMessage, style)
                                        .then(() => {
                                            debugLog(`✅ 语音已发送到播放队列: "${currentMessage.substring(0, 30)}..."`, 'info');
                                            console.log(`✅ [TTS播报] 已发送到播放队列: "${currentMessage.substring(0, 40)}..."`);
                                        })
                                        .catch((err) => {
                                            debugLog(`❌ 语音播放失败: ${err.message}`, 'error');
                                            console.error(`❌ [TTS播报] 失败:`, err);
                                        });
                                }
                            } else {
                                // 不稳定 → 不播报，但记录日志
                                console.log('[VisualHazardFilter] 危险检测不稳定，跳过播报');
                                if (window.sendLog) {
                                    window.sendLog({ type: 'hazard_unstable', frame: hazardData });
                                }
                            }
                        } else {
                            // VisualHazardFilter未加载，直接播报（降级）
                            const hazardType = hazardData.type;
                            if (window.EventBridge) {
                                window.EventBridge.dispatch("hazard", {
                                    type: hazardType,
                                    level: isUrgent ? 'critical' : 'high',
                                    meta: { message: currentMessage, raw: guidance }
                                });
                            }
                        }
                        
                        // 如果检测到没有危险，重置过滤器
                        if (!currentMessage.includes('危险') && window.VisualHazardFilter) {
                            window.VisualHazardFilter.reset();
                        }
                    } else if (currentMessage.includes('台阶')) {
                        // 台阶事件：通过EventBridge派发
                        const direction = currentMessage.includes('上') ? 'up' : currentMessage.includes('下') ? 'down' : 'up';
                        const distanceMatch = currentMessage.match(/(\d+)/);
                        const distance = distanceMatch ? parseInt(distanceMatch[1]) : null;
                        if (window.EventBridge) {
                            window.EventBridge.dispatch("step", {
                                direction: direction,
                                distance: distance,
                                meta: { message: currentMessage, raw: guidance }
                            });
                        } else {
                            // 降级：直接调用TTS
                            speakText(currentMessage, style)
                                .then(() => {
                                    debugLog(`✅ 语音已发送到播放队列: "${currentMessage.substring(0, 30)}..."`, 'info');
                                    console.log(`✅ [TTS播报] 已发送到播放队列: "${currentMessage.substring(0, 40)}..."`);
                                })
                                .catch((err) => {
                                    debugLog(`❌ 语音播放失败: ${err.message}`, 'error');
                                    console.error(`❌ [TTS播报] 失败:`, err);
                                });
                        }
                    } else if (currentMessage.includes('左转') || currentMessage.includes('右转') || currentMessage.includes('直行')) {
                        // 导航事件：通过EventBridge派发
                        const action = currentMessage.includes('左转') ? 'turn' : 
                                    currentMessage.includes('右转') ? 'turn' : 
                                    currentMessage.includes('直行') ? 'straight' : 'continue';
                        const navDirection = currentMessage.includes('左转') ? 'left' : 
                                           currentMessage.includes('右转') ? 'right' : 'forward';
                        const distanceMatch = currentMessage.match(/(\d+)/);
                        const distance = distanceMatch ? parseInt(distanceMatch[1]) : null;
                        if (window.EventBridge) {
                            window.EventBridge.dispatch("navigation", {
                                action: action,
                                direction: navDirection,
                                distance: distance,
                                meta: { message: currentMessage, raw: guidance, direction: direction }
                            });
                        } else {
                            // 降级：直接调用TTS
                            speakText(currentMessage, style)
                                .then(() => {
                                    debugLog(`✅ 语音已发送到播放队列: "${currentMessage.substring(0, 30)}..."`, 'info');
                                    console.log(`✅ [TTS播报] 已发送到播放队列: "${currentMessage.substring(0, 40)}..."`);
                                })
                                .catch((err) => {
                                    debugLog(`❌ 语音播放失败: ${err.message}`, 'error');
                                    console.error(`❌ [TTS播报] 失败:`, err);
                                });
                        }
                    } else {
                        // 其他消息：直接调用TTS（保持原有逻辑）
                        console.log(`🔊 [TTS播报] 开始播放: "${currentMessage.substring(0, 40)}..." | 风格: ${style} | 优先级: ${priority}`);
                        debugLog(`开始播放语音: "${currentMessage.substring(0, 30)}..."`, 'info');
                        
                        speakText(currentMessage, style)
                            .then(() => {
                                debugLog(`✅ 语音已发送到播放队列: "${currentMessage.substring(0, 30)}..."`, 'info');
                                console.log(`✅ [TTS播报] 已发送到播放队列: "${currentMessage.substring(0, 40)}..."`);
                            })
                            .catch((err) => {
                                debugLog(`❌ 语音播放失败: ${err.message}`, 'error');
                                console.error(`❌ [TTS播报] 失败:`, err);
                                console.error(`❌ [TTS播报] 失败消息: "${currentMessage}"`);
                                // 如果失败，尝试用户交互后播放
                                const playWhenReady = () => {
                                    speakText(currentMessage, style)
                                        .then(() => {
                                            debugLog('✅ 用户交互后语音已播放', 'info');
                                            console.log(`✅ [TTS播报] 用户交互后已播放`);
                                        })
                                        .catch((e) => {
                                            debugLog(`❌ 用户交互后播放也失败: ${e.message}`, 'error');
                                            console.error(`❌ [TTS播报] 用户交互后也失败:`, e);
                                        });
                                    document.removeEventListener('click', playWhenReady);
                                    document.removeEventListener('touchstart', playWhenReady);
                                };
                                document.addEventListener('click', playWhenReady, { once: true });
                                document.addEventListener('touchstart', playWhenReady, { once: true });
                            });
                    }
                } else {
                    console.log(`ℹ️ [TTS决策] 没有重要消息需要播报`);
                }
            }
        }
    </script>

    <!-- ===================== -->
    <!-- Luna Task Chain System -->
    <!-- ===================== -->
    <script>
        /* ===== BEGIN: task_logger.js ===== */
// =====================================================
// Task Logger — v1.0 (简化版)
// 记录 TaskChain 的执行情况、错误、任务切换、节点状态
// =====================================================

(function () {
    "use strict";

    if (window.TaskLogger) return;

    class TaskLogger {
        constructor() {
            this.logs = [];
            this.uploadUrl = "/log_task_event"; // 后端路由
        }

        _push(level, source, message, extra) {
            const entry = {
                ts: new Date().toISOString(),
                level,
                source,
                message,
                extra: extra || null,
            };
            this.logs.push(entry);
            console.log(`[TaskLog][${level}][${source}] ${message}`, extra || "");

            // 简单异步上报
            try {
                if (typeof fetch !== 'undefined') {
                    fetch(this.uploadUrl, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(entry),
                    }).catch(() => {
                        // ignore upload errors
                    });
                }
            } catch (e) {
                // ignore
            }
        }

        info(source, msg, extra) {
            this._push("INFO", source, msg, extra);
        }

        warn(source, msg, extra) {
            this._push("WARN", source, msg, extra);
        }

        error(source, msg, extra) {
            this._push("ERROR", source, msg, extra);
        }

        dump() {
            return this.logs.slice();
        }
    }

    window.TaskLogger = new TaskLogger();
    console.log("[TaskLogger] 已加载");
})();
        /* ===== END: task_logger.js ===== */
    </script>

    <script>
        /* ===== BEGIN: task_fsm.js ===== */
// =====================================================
// Task FSM — v1.0 (简化版)
// 任务状态机：控制任务状态流转
// =====================================================

(function () {
  "use strict";

  if (window.TaskFSM) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class TaskFSM {
    constructor() {
      this.state = "idle"; // idle | pending | running | waiting | paused | finished | failed
      this.currentTask = null; // 当前正在执行的 task 对象
    }

    getState() {
      return this.state;
    }

    _setState(next, detail) {
      const prev = this.state;
      this.state = next;
      logger.info("TaskFSM", `状态 ${prev} → ${next}`, detail || {});
    }

    onTaskEnqueued(task) {
      // 有任务入队
      if (this.state === "idle" || this.state === "finished") {
        this._setState("pending", { reason: "first_task_enqueued" });
      }
    }

    beforeTaskRun(task) {
      this.currentTask = task;
      this._setState("running", { taskType: task.type });
    }

    afterTaskRun(task, ok) {
      if (!ok) {
        this._setState("failed", { taskType: task.type });
      } else {
        // 不在这里转 finished，交给 TaskChain 看队列是否为空
        logger.info("TaskFSM", "单个任务执行完成", { taskType: task.type });
      }
    }

    onAllTasksFinished() {
      this.currentTask = null;
      this._setState("finished");
    }

    pause(reason) {
      this._setState("paused", { reason });
    }

    resume() {
      this._setState("running", { reason: "resume" });
    }

    wait(reason) {
      this._setState("waiting", { reason });
    }

    reset() {
      this.currentTask = null;
      this._setState("idle", { reason: "reset" });
    }
  }

  window.TaskFSM = new TaskFSM();
  console.log("[TaskFSM] 已加载");
})();
        /* ===== END: task_fsm.js ===== */
    </script>

    <script>
        /* ===== BEGIN: intent_tracker_simple.js ===== */
// =====================================================
// Intent Tracker — v1.0 (简化版)
// 意图追踪器：判断用户意图（取消/恢复/插入/替换/继续）
// =====================================================

(function () {
  "use strict";

  if (window.IntentTracker) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class IntentTracker {
    constructor() {
      this.lastUtterance = null;
    }

    /**
     * 输入用户原始语句，输出决策：
     * "cancel" | "resume" | "insert" | "replace" | "continue"
     */
    updateIntent(text) {
      this.lastUtterance = text;
      logger.info("Intent", "收到用户语句", { text });

      if (/(停|不要了|算了|取消|先这样)/.test(text)) {
        return "cancel";
      }
      if (/(继续|接着|刚才|恢复导航)/.test(text)) {
        return "resume";
      }
      if (/(顺便|先去|顺路|路过)/.test(text)) {
        return "insert";
      }
      if (/(我要去|带我去|导航到|帮我去)/.test(text)) {
        return "replace";
      }
      return "continue";
    }
  }

  window.IntentTracker = new IntentTracker();
  console.log("[IntentTracker] 已加载");
})();
        /* ===== END: intent_tracker_simple.js ===== */
    </script>

    <script>
        /* ===== BEGIN: task_chain.js ===== */
        /**
         * 轻量级任务链系统（规范要求）
         * 提供可插拔、可恢复、可中断的任务执行流程
         */
        (function() {
            'use strict';
            const TaskPriority = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
            const TaskType = {
                HAZARD_WARNING: 'hazard_warning',
                STEP_WARNING: 'step_warning',
                NAVIGATION: 'navigation',
                TTS_BROADCAST: 'tts_broadcast',
                UI_UPDATE: 'ui_update',
                LOG_RECORD: 'log_record',
                EMOTION_EVENT: 'emotion_event'
            };
            class TaskChain {
                constructor() {
                    this.queue = [];
                    this.running = false;
                    this.currentTask = null;
                    this.handlers = new Map();
                    this.stats = { totalEnqueued: 0, totalCompleted: 0, totalFailed: 0, totalInterrupted: 0 };
                    this._registerDefaultHandlers();
                    console.log('✅ TaskChain初始化完成', { module: 'task_chain' });
                }
                _registerDefaultHandlers() {
                    this.registerHandler(TaskType.HAZARD_WARNING, async (payload) => {
                        const { type, level, meta } = payload;
                        console.log(`🚨 [TaskChain] 处理危险警告: ${type}`, { module: 'task_chain' });
                        if (window.emitHazardEvent) {
                            window.emitHazardEvent({ type, level, meta });
                        } else if (window.speakText) {
                            const message = `检测到${type}危险，请小心`;
                            window.speakText(message, 'urgent');
                        }
                    });
                    this.registerHandler(TaskType.STEP_WARNING, async (payload) => {
                        const { direction, distance, meta } = payload;
                        console.log(`📐 [TaskChain] 处理台阶警告: ${direction}`, { module: 'task_chain' });
                        if (window.emitHazardEvent) {
                            window.emitHazardEvent({ type: 'step', level: 'high', meta: { direction, distance, ...meta } });
                        } else if (window.speakText) {
                            const message = `前方${distance || ''}米有台阶，请${direction === 'up' ? '减速' : '小心'}`;
                            window.speakText(message, 'urgent');
                        }
                    });
                    this.registerHandler(TaskType.NAVIGATION, async (payload) => {
                        const { action, direction, distance, meta } = payload;
                        console.log(`🧭 [TaskChain] 处理导航: ${action}`, { module: 'task_chain' });
                        if (window.emitNavigationEvent) {
                            window.emitNavigationEvent({ action, direction, distance, ...meta });
                        } else if (window.speakText) {
                            const message = action === 'turn' ? `前方${distance || ''}米${direction === 'left' ? '左' : '右'}转` : '请跟随导航指引';
                            window.speakText(message, 'cheerful');
                        }
                    });
                    this.registerHandler(TaskType.TTS_BROADCAST, async (payload) => {
                        const { text, style, priority } = payload;
                        // ③【新增：后台日志上传】
                        if (window.sendLog) {
                            window.sendLog({ type: 'tts_play', text: text ? text.substring(0, 100) : '', style, priority });
                        }
                        if (window.speakText) {
                            window.speakText(text, style || 'calm');
                        }
                    });
                    this.registerHandler(TaskType.UI_UPDATE, async (payload) => {
                        const { elementId, content, className } = payload;
                        const element = document.getElementById(elementId);
                        if (element) {
                            if (content !== undefined) element.textContent = content;
                            if (className !== undefined) element.className = className;
                        }
                    });
                    this.registerHandler(TaskType.LOG_RECORD, async (payload) => {
                        const { level, message, meta } = payload;
                        if (window.lunaLog) {
                            window.lunaLog(level, message, meta || {});
                        }
                    });
                    this.registerHandler(TaskType.EMOTION_EVENT, async (payload) => {
                        const { event, level, meta } = payload;
                        if (window.emotion_event) {
                            window.emotion_event(event, level, meta);
                        }
                    });
                }
                registerHandler(taskType, handler) {
                    this.handlers.set(taskType, handler);
                }
                enqueue(taskType, payload, priority = TaskPriority.MEDIUM) {
                    const task = {
                        id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                        type: taskType,
                        payload: payload || {},
                        priority: priority,
                        timestamp: Date.now(),
                        status: 'pending'
                    };
                    let inserted = false;
                    for (let i = 0; i < this.queue.length; i++) {
                        if (this.queue[i].priority > priority) {
                            this.queue.splice(i, 0, task);
                            inserted = true;
                            break;
                        }
                    }
                    if (!inserted) this.queue.push(task);
                    this.stats.totalEnqueued++;
                    
                    // ④【加入：TaskChain完整日志】
                    console.log('[TaskChain] enqueue', taskType, payload);
                    if (window.sendLog) {
                        window.sendLog({ type: 'task_enqueue', taskType, payload, priority });
                    }
                    
                    if (!this.running) this._processQueue();
                    return task.id;
                }
                async _processQueue() {
                    if (this.running) return;
                    this.running = true;
                    while (this.queue.length > 0) {
                        const task = this.queue.shift();
                        this.currentTask = task;
                        
                        // ④【加入：TaskChain完整日志】
                        console.log('[TaskChain] process', task);
                        if (window.sendLog) {
                            window.sendLog({ type: 'task_process', task });
                        }
                        try {
                            task.status = 'running';
                            const handler = this.handlers.get(task.type);
                            if (handler) {
                                await handler(task.payload);
                                task.status = 'completed';
                                this.stats.totalCompleted++;
                            } else {
                                task.status = 'skipped';
                            }
                        } catch (error) {
                            task.status = 'failed';
                            task.error = error.message;
                            this.stats.totalFailed++;
                            console.error(`❌ [TaskChain] 任务失败: ${task.type}`, error);
                        }
                        this.currentTask = null;
                    }
                    this.running = false;
                }
                interrupt() {
                    if (this.currentTask) {
                        this.currentTask.status = 'interrupted';
                        this.stats.totalInterrupted++;
                        this.currentTask = null;
                    }
                }
                clear() {
                    this.queue = [];
                    this.interrupt();
                }
                getStats() {
                    return {
                        ...this.stats,
                        queueLength: this.queue.length,
                        currentTask: this.currentTask ? { id: this.currentTask.id, type: this.currentTask.type, status: this.currentTask.status } : null
                    };
                }
                
                /**
                 * ⑥【修复：TTS队列卡死】- processNext方法
                 * 处理下一个任务（用于TTS播放完成后的回调）
                 */
                processNext() {
                    if (!this.running && this.queue.length > 0) {
                        this._processQueue();
                    }
                }
            }
            window.taskChain = new TaskChain();
            window.taskChainEnqueue = function(taskType, payload, priority) {
                return window.taskChain.enqueue(taskType, payload, priority);
            };
        })();
        /* ===== END: task_chain.js ===== */
    </script>

    <!-- ============================ -->
    <!-- Navigation FSM & Executors -->
    <!-- ============================ -->
    <script>
        /* ===== BEGIN: navigation_fsm.js ===== */
        // frontend/navigation_fsm.js
        // 一期步行导航 FSM：YOLO → FSM → taskChain

        (function () {
          "use strict";

          if (window.NavigationFSM) return;

          const logger = window.TaskLogger || {
            info: console.log,
            warn: console.warn,
            error: console.error,
          };

          class NavigationFSMClass {
            constructor() {
              this.initialized = true;  // ✅ 标记为已初始化
              this.state = "IDLE"; 
              this.currentRoute = null;
              this.currentStepIndex = 0;
              this.lastAnnouncement = 0;
              this.minInterval = 2500;
            }

            getState() {
              return this.state;
            }

            getCurrentStep() {
              if (!this.currentRoute) return null;
              return this.currentRoute[this.currentStepIndex] || null;
            }

            now() {
              return Date.now();
            }

            start(route) {
              if (!Array.isArray(route) || route.length === 0) {
                return this._dispatchError("路线为空");
              }

              this.currentRoute = route;
              this.currentStepIndex = 0;
              this.state = "NAVIGATING";

              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_START",
                  priority: "HIGH",
                  payload: {
                    route: this.currentRoute,
                    eta: Math.ceil(route.length * 0.5)
                  }
                });
              }

              if (window.MiniMap) {
                window.MiniMap.setRouteLength(route.length || 0);
              }

              logger.info("NavigationFSM", "导航开始", {});
            }

            finish() {
              this.state = "ARRIVED";

              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_END",
                  priority: "HIGH",
                  payload: {}
                });
              }

              logger.info("NavigationFSM", "已到达终点", {});
            }

            onVisionUpdate(data) {
              if (this.state !== "NAVIGATING") return;
              const { direction, distance } = data || {};
              if (!direction) return;

              // 节流
              if (this.now() - this.lastAnnouncement < this.minInterval) return;
              this.lastAnnouncement = this.now();

              if (direction === "left" || direction === "right") {
                this._dispatchTurn(direction, distance);
              } else if (direction === "straight") {
                this._dispatchStraight(distance);
              }

              if (window.MiniMap) {
                const dir = direction === "straight" ? "front" : direction;
                window.MiniMap.addHazard(dir);
              }

              logger.info("NavigationFSM", "收到视觉更新", data);
            }

            nextStep() {
              if (!this.currentRoute) return;
              if (this.currentStepIndex < this.currentRoute.length - 1) {
                this.currentStepIndex++;
              } else {
                this.finish();
              }

              if (window.MiniMap) {
                window.MiniMap.setStepIndex(this.currentStepIndex);
              }
            }

            _dispatchTurn(direction, distance) {
              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_TURN",
                  priority: "HIGH",
                  payload: { direction, distance }
                });
              }
              logger.info("NavigationFSM", "触发转弯", { direction, distance });
            }

            _dispatchStraight(distance) {
              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_STRAIGHT",
                  priority: "MEDIUM",
                  payload: { distance }
                });
              }
              logger.info("NavigationFSM", "直行", { distance });
            }

            _dispatchPOI(name) {
              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_POI",
                  priority: "LOW",
                  payload: { name }
                });
              }
              logger.info("NavigationFSM", "进入关键节点", { name });
            }

            _dispatchError(reason) {
              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "NAV_ERROR",
                  priority: "HIGH",
                  payload: { reason }
                });
              }
              logger.error("NavigationFSM", "错误", { reason });
            }
          }

          window.NavigationFSM = new NavigationFSMClass();
    // 强制初始化检查
    if (!window.NavigationFSM.initialized) {
      window.NavigationFSM.initialized = true;
      window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
      console.log("✅ NavigationFSM 强制初始化完成 (Instance)");
    }
          // 强制初始化检查
          if (!window.NavigationFSM.initialized) {
            window.NavigationFSM.initialized = true;
            window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
            console.log("✅ NavigationFSM 强制初始化完成 (Instance)");
          }
          logger.info("NavigationFSM", "已加载", {});

        })();
        /* ===== END: navigation_fsm.js ===== */
    </script>

    <script>
        /* ===== BEGIN: navigation_executors.js ===== */
        // frontend/navigation_executors.js
        // 把 NAV_* 任务转成语音行为

        (function () {
          "use strict";

          if (window.NavigationExecutors) return;

          const TTS = window.speakText || (txt => Promise.resolve(console.log("[TTS]", txt)));
          const NavLog = window.NavLog || window.TaskLogger || {
            info: console.log,
            warn: console.warn,
            error: console.error,
          };

          async function execStart(payload) {
            const { eta } = payload || {};
            const text = eta ? `路线规划完成，预计需要 ${eta} 分钟。` : "路线规划完成，开始导航。";
            NavLog.info("Executor", "开始执行 NAV_START", payload);
            await TTS(text);
            NavLog.info("Executor", "NAV_START 执行完成", {});
          }

          async function execTurn(payload) {
            const { direction, distance } = payload || {};
            let text;
            if (direction === "left") {
              text = distance ? `前方 ${distance} 米左转` : "请在前方左转";
            } else if (direction === "right") {
              text = distance ? `前方 ${distance} 米右转` : "请在前方右转";
            } else {
              text = "请按提示转弯";
            }

            NavLog.info("Executor", "开始执行 NAV_TURN", payload);
            await TTS(text);
            NavLog.info("Executor", "NAV_TURN 执行完成", {});
          }

          async function execStraight(payload) {
            const { distance } = payload || {};
            const text = distance ? `请直行 ${distance} 米` : "请继续直行";
            NavLog.info("Executor", "开始执行 NAV_STRAIGHT", payload);
            await TTS(text);
            NavLog.info("Executor", "NAV_STRAIGHT 执行完成", {});
          }

          async function execPOI(payload) {
            const { name } = payload || {};
            const text = name ? `您已到达 ${name}` : "您已到达关键位置";
            NavLog.info("Executor", "开始执行 NAV_POI", payload);
            await TTS(text);
            NavLog.info("Executor", "NAV_POI 执行完成", {});
          }

          async function execEnd() {
            const text = "已到达目的地。导航结束。";
            NavLog.info("Executor", "开始执行 NAV_END", {});
            await TTS(text);
            NavLog.info("Executor", "NAV_END 执行完成", {});
          }

          async function execError(payload) {
            const { reason } = payload || {};
            const text = reason ? `导航出错：${reason}` : "导航出错，请稍后重试。";
            NavLog.error("Executor", "开始执行 NAV_ERROR", payload);
            await TTS(text);
            NavLog.error("Executor", "NAV_ERROR 执行完成", {});
          }

          window.NavigationExecutors = {
            execStart,
            execTurn,
            execStraight,
            execPOI,
            execEnd,
            execError,
          };

          console.log("[NavigationExecutors] 已加载");
        })();
        /* ===== END: navigation_executors.js ===== */
    </script>

    <script>
        /* ===== BEGIN: minimap.js ===== */
        // frontend/minimap.js
        // MiniMap：小雷达图，显示自己 + 危险 + 节点 + 大致方向

        (function () {
          "use strict";

          if (window.MiniMap) return;

          const NavLog = window.NavLog || window.TaskLogger || {
            info: console.log,
            warn: console.warn,
            error: console.error,
          };

          class MiniMap {
            constructor() {
              this.canvas = null;
              this.ctx = null;
              this.width = 220;
              this.height = 220;
              this.state = {
                routeLength: 0,
                currentStepIndex: 0,
                hazards: [],
                nodes: [],
              };

              this._initCanvas();
              this._startRenderLoop();
            }

            _initCanvas() {
              let container = document.getElementById("luna-minimap-container");
              if (!container) {
                container = document.createElement("div");
                container.id = "luna-minimap-container";
                Object.assign(container.style, {
                  position: "fixed",
                  right: "12px",
                  bottom: "12px",
                  width: this.width + "px",
                  height: this.height + "px",
                  background: "rgba(0,0,0,0.45)",
                  borderRadius: "10px",
                  border: "1px solid rgba(255,255,255,0.2)",
                  zIndex: 9999,
                  overflow: "hidden",
                  backdropFilter: "blur(4px)",
                  color: "#fff",
                  fontSize: "11px",
                  fontFamily: "system-ui, -apple-system, BlinkMacSystemFont",
                });
                document.body.appendChild(container);
              }

              const title = document.createElement("div");
              title.innerText = "Luna MiniMap";
              Object.assign(title.style, {
                padding: "4px 8px",
                borderBottom: "1px solid rgba(255,255,255,0.15)",
                fontSize: "11px",
                opacity: 0.8,
              });
              container.appendChild(title);

              const canvas = document.createElement("canvas");
              canvas.width = this.width;
              canvas.height = this.height - 18;
              canvas.style.display = "block";
              container.appendChild(canvas);

              this.canvas = canvas;
              this.ctx = canvas.getContext("2d");

              NavLog.info("MiniMap", "初始化完成", {});
            }

            _startRenderLoop() {
              const draw = () => {
                this._render();
                requestAnimationFrame(draw);
              };
              requestAnimationFrame(draw);
            }

            setRouteLength(len) {
              this.state.routeLength = len || 0;
              this.state.currentStepIndex = 0;
            }

            setStepIndex(idx) {
              this.state.currentStepIndex = idx;
            }

            addHazard(relativeDirection) {
              const base = { x: 0, y: 0 };

              switch (relativeDirection) {
                case "front":
                  base.y = -30;
                  break;
                case "back":
                  base.y = 30;
                  break;
                case "left":
                  base.x = -30;
                  break;
                case "right":
                  base.x = 30;
                  break;
                default:
                  base.y = -30;
              }

              this.state.hazards.push({
                x: base.x + (Math.random() * 10 - 5),
                y: base.y + (Math.random() * 10 - 5),
                ts: Date.now(),
              });

              if (this.state.hazards.length > 30) {
                this.state.hazards.shift();
              }

              NavLog.info("MiniMap", "记录危险点", { dir: relativeDirection });
            }

            addNode(nodeSummary) {
              this.state.nodes.push({
                x: Math.random() * 80 - 40,
                y: Math.random() * 80 - 40,
                type: nodeSummary.type || "facility",
                label: nodeSummary.label || nodeSummary.role || "节点",
              });

              if (window.NodeMemory) {
                window.NodeMemory.addNode({
                  role: nodeSummary.role,
                  type: nodeSummary.type,
                  label: nodeSummary.label,
                });
              }

              if (this.state.nodes.length > 40) {
                this.state.nodes.shift();
              }

              NavLog.info("MiniMap", "记录节点", nodeSummary);
            }

            _render() {
              if (!this.ctx) return;
              const ctx = this.ctx;
              const w = this.canvas.width;
              const h = this.canvas.height;

              ctx.clearRect(0, 0, w, h);
              ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
              ctx.fillRect(0, 0, w, h);

              // 网格
              ctx.strokeStyle = "rgba(255,255,255,0.06)";
              ctx.lineWidth = 1;
              ctx.beginPath();
              for (let x = 0; x <= w; x += 20) {
                ctx.moveTo(x, 0);
                ctx.lineTo(x, h);
              }
              for (let y = 0; y <= h; y += 20) {
                ctx.moveTo(0, y);
                ctx.lineTo(w, y);
              }
              ctx.stroke();

              const cx = w / 2;
              const cy = h / 2;

              // 自己
              ctx.fillStyle = "#00ffcc";
              ctx.beginPath();
              ctx.arc(cx, cy, 5, 0, Math.PI * 2);
              ctx.fill();

              // 导航方向（简化：用 stepIndex / routeLength 表示）
              if (this.state.routeLength > 0) {
                const progress = this.state.currentStepIndex / this.state.routeLength;
                const arrowLen = 40 + progress * 30;
                ctx.strokeStyle = "#00ffcc";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(cx, cy - arrowLen);
                ctx.stroke();
              }

              // 危险点
              const now = Date.now();
              ctx.fillStyle = "#ff5555";
              this.state.hazards = this.state.hazards.filter(hz => now - hz.ts < 10000);
              for (const hz of this.state.hazards) {
                ctx.beginPath();
                ctx.arc(cx + hz.x, cy + hz.y, 4, 0, Math.PI * 2);
                ctx.fill();
              }

              // 节点
              ctx.fillStyle = "#ffdd66";
              for (const n of this.state.nodes) {
                ctx.beginPath();
                ctx.arc(cx + n.x, cy + n.y, 3, 0, Math.PI * 2);
                ctx.fill();
              }
            }
          }

          window.MiniMap = new MiniMap();
        })();
        /* ===== END: minimap.js ===== */
    </script>

    <script>
        /* ===== BEGIN: node_memory.js ===== */
        // frontend/node_memory.js
        // 按区域存储"场景节点"的长期记忆

        (function () {
          "use strict";

          if (window.NodeMemory) return;

          class NodeMemory {
            constructor() {
              this.key = "luna_node_memory_v1";
              this.data = this._load() || {};
              this.currentZone = "DEFAULT";
            }

            _load() {
              try {
                return JSON.parse(localStorage.getItem(this.key)) || {};
              } catch (err) {
                console.warn("[NodeMemory] load failed", err);
                return {};
              }
            }

            _save() {
              localStorage.setItem(this.key, JSON.stringify(this.data));
            }

            setZone(zoneName) {
              this.currentZone = zoneName || "DEFAULT";
              if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
              }
              this._save();
            }

            getZone() {
              return this.currentZone;
            }

            getZoneNodes() {
              return this.data[this.currentZone] || [];
            }

            _isSimilarNode(a, b) {
              if (a.label && b.label && a.label === b.label) return true;
              if (a.role && b.role && a.role === b.role) return true;
              return false;
            }

            addNode(node) {
              if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
              }

              const zoneList = this.data[this.currentZone];
              for (let i = 0; i < zoneList.length; i++) {
                if (this._isSimilarNode(zoneList[i], node)) {
                  zoneList[i].lastSeen = Date.now();
                  this._save();
                  return;
                }
              }

              zoneList.push({
                role: node.role,
                type: node.type,
                label: node.label,
                lastSeen: Date.now(),
              });

              this._save();
            }
          }

          window.NodeMemory = new NodeMemory();
          console.log("[NodeMemory] 已加载");
        })();
        /* ===== END: node_memory.js ===== */
    </script>

    <script>
        /* ===== BEGIN: zone_manager.js ===== */
        // frontend/zone_manager.js
        // ZoneManager：A区 / B区 / 医院区 / 地铁区 等

        (function () {
          "use strict";

          if (window.ZoneManager) return;

          class ZoneManager {
            constructor() {
              this.current = "DEFAULT";
            }

            setZone(name) {
              this.current = name;
              console.log("[ZoneManager] 切换区域:", name);

              if (window.NodeMemory) {
                window.NodeMemory.setZone(name);
              }

              if (window.MiniMap) {
                window.MiniMap.state.nodes = [];
                window.MiniMap.state.hazards = [];
              }
            }

            getZone() {
              return this.current;
            }
          }

          window.ZoneManager = new ZoneManager();
          console.log("[ZoneManager] 已加载");
        })();
        /* ===== END: zone_manager.js ===== */
    </script>

    <script>
        /* ===== BEGIN: zone_auto_detector.js ===== */
        // frontend/zone_auto_detector.js
        // ZoneAutoDetector：根据节点特征自动推断当前区域

        (function () {
          "use strict";

          if (window.ZoneAutoDetector) return;

          class ZoneAutoDetector {
            constructor() {
              this.currentFeatures = {};
              this.visualHints = {};
              this.behaviorProfile = {};
              this.lastUpdate = 0;
            }

            feedNode(node) {
              const key = node.label || node.role || "unknown";
              if (!this.currentFeatures[key]) {
                this.currentFeatures[key] = 0;
              }
              this.currentFeatures[key]++;
              this.lastUpdate = Date.now();
            }

            feedVisualHint(hint) {
              this.visualHints[hint] = (this.visualHints[hint] || 0) + 1;
              this.lastUpdate = Date.now();
            }

            feedBehavior(eventName) {
              this.behaviorProfile[eventName] = (this.behaviorProfile[eventName] || 0) + 1;
              this.lastUpdate = Date.now();
            }

            computeSimilarity(zoneName) {
              if (!window.NodeMemory) return 0;
              // ✅ 防御性编程：确保 data 不为 null
              if (!window.NodeMemory.data || typeof window.NodeMemory.data !== 'object') {
                return 0;
              }
              const zoneNodes = (window.NodeMemory.data[zoneName] || []);
              if (!Array.isArray(zoneNodes) || !zoneNodes.length) return 0;

              let score = 0;
              for (const zn of zoneNodes) {
                const key = zn.label || zn.role;
                if (!key) continue;
                if (this.currentFeatures[key]) score += 1;
              }
              return score / (zoneNodes.length + 3);
            }

            detectZone() {
              if (!window.NodeMemory) return null;
              // ✅ 防御性编程：确保 data 不为 null
              if (!window.NodeMemory.data || typeof window.NodeMemory.data !== 'object') {
                return null;
              }

              let bestZone = null;
              let bestScore = 0;

              for (const zoneName of Object.keys(window.NodeMemory.data)) {
                const sim = this.computeSimilarity(zoneName);
                if (sim > bestScore) {
                  bestScore = sim;
                  bestZone = zoneName;
                }
              }

              if (bestScore > 0.4) {
                return { zone: bestZone, score: bestScore };
              }
              return null;
            }
          }

          window.ZoneAutoDetector = new ZoneAutoDetector();
          console.log("[ZoneAutoDetector] 已加载");

          // 简单定时器：每2秒尝试自动切换区域
          setInterval(() => {
            if (!window.ZoneAutoDetector || !window.ZoneManager) return;
            const res = window.ZoneAutoDetector.detectZone();
            if (res) {
              console.log("[AutoZone] 切换区域 →", res.zone, res.score);
              window.ZoneManager.setZone(res.zone);
            }
          }, 2000);

        })();
        /* ===== END: zone_auto_detector.js ===== */
    </script>

    <!-- ============================ -->
    <!-- Scene Nodes Engine (节点式场景任务模板) -->
    <!-- ============================ -->
    <script>
        /* ===== BEGIN: scene_nodes.js ===== */
        // =====================================================
        // Scene Nodes Engine — v1.0
        // 场景节点引擎：支持存储场景、添加节点、用户确认、任务链转换
        // =====================================================

        (function () {
          "use strict";

          if (window.SceneNodes) return;

          const logger = window.TaskLogger || {
            info: function(msg, extra) { console.log('[SceneNodes]', msg, extra || {}); },
            warn: function(msg, extra) { console.warn('[SceneNodes]', msg, extra || {}); },
            error: function(msg, extra) { console.error('[SceneNodes]', msg, extra || {}); }
          };

          class SceneNodes {
            constructor() {
              this.currentScene = null;               // "hospital", "metro", "mall"...
              this.nodeMap = {};                       // { sceneName: [node1,node2...] }
              this.nodeMemory = {};                    // { sceneName: { nodeName: {...}} }
              this._loadFromStorage();
            }

            /** 从 localStorage 加载场景节点记忆 */
            _loadFromStorage() {
              try {
                const stored = localStorage.getItem('luna_scene_nodes_v1');
                if (stored) {
                  const data = JSON.parse(stored);
                  this.nodeMap = data.nodeMap || {};
                  this.nodeMemory = data.nodeMemory || {};
                  logger.info("SceneNodes", "从存储加载场景节点", {
                    scenes: Object.keys(this.nodeMap).length
                  });
                }
              } catch (e) {
                logger.error("SceneNodes", "加载存储失败", { error: e.toString() });
              }
            }

            /** 保存到 localStorage */
            _saveToStorage() {
              try {
                localStorage.setItem('luna_scene_nodes_v1', JSON.stringify({
                  nodeMap: this.nodeMap,
                  nodeMemory: this.nodeMemory
                }));
              } catch (e) {
                logger.error("SceneNodes", "保存存储失败", { error: e.toString() });
              }
            }

            /** 切换场景，如 "hospital" */
            enterScene(sceneName) {
              this.currentScene = sceneName;
              if (!this.nodeMap[sceneName]) this.nodeMap[sceneName] = [];
              if (!this.nodeMemory[sceneName]) this.nodeMemory[sceneName] = {};
              
              logger.info("SceneNodes", "进入场景", { sceneName });
              this._saveToStorage();
            }

            /** 添加节点（来自视觉识别） */
            addDetectedNode(nodeName, meta) {
              const scene = this.currentScene;
              if (!scene) {
                logger.warn("SceneNodes", "未设置当前场景，无法添加节点", { nodeName });
                return;
              }

              if (!this.nodeMemory[scene][nodeName]) {
                logger.info("SceneNodes", "新增节点（待确认）", { scene, nodeName, meta });
                this.nodeMemory[scene][nodeName] = {
                  confirmed: false,
                  meta: meta || {},
                  detectedAt: Date.now()
                };
                this._saveToStorage();
              } else {
                // 更新已存在节点的元数据
                this.nodeMemory[scene][nodeName].meta = Object.assign(
                  this.nodeMemory[scene][nodeName].meta || {},
                  meta || {}
                );
                this.nodeMemory[scene][nodeName].detectedAt = Date.now();
                this._saveToStorage();
              }
            }

            /** 用户确认节点：如 "这里是挂号窗口" */
            confirmNode(nodeName, meta) {
              const scene = this.currentScene;
              if (!scene) {
                logger.warn("SceneNodes", "未设置当前场景，无法确认节点", { nodeName });
                return;
              }

              this.nodeMemory[scene][nodeName] = {
                confirmed: true,
                meta: Object.assign(
                  this.nodeMemory[scene][nodeName]?.meta || {},
                  meta || {}
                ),
                confirmedAt: Date.now()
              };

              if (!this.nodeMap[scene].includes(nodeName)) {
                this.nodeMap[scene].push(nodeName);
              }

              logger.info("SceneNodes", "用户确认节点", { scene, nodeName });
              this._saveToStorage();
            }

            /** 修正节点名称，如 "窗口1 → 挂号窗口" */
            renameNode(oldName, newName) {
              const scene = this.currentScene;
              if (!scene) {
                logger.warn("SceneNodes", "未设置当前场景，无法重命名节点", { oldName, newName });
                return;
              }

              if (this.nodeMemory[scene][oldName]) {
                this.nodeMemory[scene][newName] = this.nodeMemory[scene][oldName];
                delete this.nodeMemory[scene][oldName];
              }

              const idx = this.nodeMap[scene].indexOf(oldName);
              if (idx >= 0) {
                this.nodeMap[scene][idx] = newName;
              }

              logger.info("SceneNodes", "节点重命名", { scene, oldName, newName });
              this._saveToStorage();
            }

            /** 获取场景的所有节点 */
            getSceneNodes(sceneName) {
              return this.nodeMap[sceneName] || [];
            }

            /** 获取当前场景的节点 */
            getCurrentSceneNodes() {
              return this.getSceneNodes(this.currentScene);
            }

            /** 检查节点是否已确认 */
            isNodeConfirmed(nodeName) {
              const scene = this.currentScene;
              if (!scene || !this.nodeMemory[scene]) return false;
              return this.nodeMemory[scene][nodeName]?.confirmed === true;
            }

            /** 按节点生成任务链 */
            buildTaskChainFor(nodeName) {
              return [
                { 
                  type: "SCAN_ENV", 
                  payload: { 
                    target: nodeName,
                    scene: this.currentScene
                  } 
                },
                { 
                  type: "MOVE_TO_NODE", 
                  payload: { 
                    nodeName,
                    scene: this.currentScene
                  } 
                },
                { 
                  type: "CONFIRM_ARRIVAL", 
                  payload: { 
                    nodeName,
                    scene: this.currentScene
                  } 
                },
              ];
            }

            /** 获取节点的元数据 */
            getNodeMeta(nodeName) {
              const scene = this.currentScene;
              if (!scene || !this.nodeMemory[scene]) return null;
              return this.nodeMemory[scene][nodeName]?.meta || null;
            }
          }

          window.SceneNodes = new SceneNodes();
          console.log("[SceneNodes] 已加载");
        })();
        /* ===== END: scene_nodes.js ===== */
    </script>

    <script>
        /* ===== BEGIN: scene_node_detector.js ===== */
        // =====================================================
        // Scene Node Detector — v1.0
        // 视觉识别 → 场景节点（轻量桥接）
        // 将 YOLO 输出转换为"节点候选"
        // =====================================================

        (function () {
          "use strict";

          if (window.SceneNodeDetector) return;

          const logger = window.TaskLogger || {
            info: function(msg, extra) { console.log('[SceneNodeDetector]', msg, extra || {}); },
            debug: function(msg, extra) { console.debug('[SceneNodeDetector]', msg, extra || {}); }
          };

          class SceneNodeDetector {
            constructor() {
              this.yoloObjects = [];
              this.lastUpdateTime = 0;
              this.detectionCooldown = 2000; // 2秒内不重复检测同一节点
              this.recentDetections = {}; // { nodeName: timestamp }
            }

            /** 更新检测结果（来自 YOLO） */
            updateDetections(objects) {
              if (!objects || !Array.isArray(objects)) return;
              
              this.yoloObjects = objects;
              this.lastUpdateTime = Date.now();

              // 确保 SceneNodes 已加载
              if (!window.SceneNodes) {
                logger.debug("SceneNodeDetector", "SceneNodes 未加载，跳过检测");
                return;
              }

              // 遍历检测对象，识别场景节点
              objects.forEach(obj => {
                const label = (obj.label || obj.class || '').toLowerCase();
                const confidence = obj.confidence || obj.conf || 0.5;
                
                // 只处理置信度较高的检测
                if (confidence < 0.5) return;

                // 医院场景节点识别
                if (/regist|挂号|register|挂号处/.test(label)) {
                  this._addNodeIfNotRecent("挂号窗口", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/toilet|洗手间|wc|卫生间|厕所/.test(label)) {
                  this._addNodeIfNotRecent("洗手间", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/elevator|电梯|lift/.test(label)) {
                  this._addNodeIfNotRecent("电梯", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/payment|缴费|收费|pay/.test(label)) {
                  this._addNodeIfNotRecent("缴费处", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/pharmacy|药房|取药|pharm/.test(label)) {
                  this._addNodeIfNotRecent("药房", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/waiting|候诊|候诊区/.test(label)) {
                  this._addNodeIfNotRecent("候诊区", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                // 地铁场景节点识别
                if (/entrance|入口|进站/.test(label)) {
                  this._addNodeIfNotRecent("进站口", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/gate|闸机|检票/.test(label)) {
                  this._addNodeIfNotRecent("闸机", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/platform|站台/.test(label)) {
                  this._addNodeIfNotRecent("站台", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                // 商场场景节点识别
                if (/cashier|收银|收银台/.test(label)) {
                  this._addNodeIfNotRecent("收银台", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/service|客服|服务台/.test(label)) {
                  this._addNodeIfNotRecent("客服台", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/escalator|扶梯|手扶梯/.test(label)) {
                  this._addNodeIfNotRecent("扶梯", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }

                if (/restaurant|餐饮|餐厅/.test(label)) {
                  this._addNodeIfNotRecent("餐饮区", {
                    box: obj.box || obj.bbox,
                    confidence: confidence,
                    source: "yolo",
                    label: obj.label
                  });
                }
              });
            }

            /** 添加节点（带冷却时间） */
            _addNodeIfNotRecent(nodeName, meta) {
              const now = Date.now();
              const lastDetected = this.recentDetections[nodeName] || 0;
              
              // 冷却时间检查
              if (now - lastDetected < this.detectionCooldown) {
                return;
              }

              this.recentDetections[nodeName] = now;
              
              if (window.SceneNodes) {
                window.SceneNodes.addDetectedNode(nodeName, meta);
                logger.debug("SceneNodeDetector", "检测到节点", { nodeName, meta });
              }
            }

            /** 获取最近的检测结果 */
            getRecentDetections() {
              return this.yoloObjects;
            }

            /** 清除冷却记录（用于场景切换时） */
            clearCooldown() {
              this.recentDetections = {};
              logger.debug("SceneNodeDetector", "清除检测冷却记录");
            }
          }

          window.SceneNodeDetector = new SceneNodeDetector();
          console.log("[SceneNodeDetector] 已加载");
        })();
        /* ===== END: scene_node_detector.js ===== */
    </script>

    <script>
        /* ===== BEGIN: node_task_bridge.js ===== */
        // =====================================================
        // Node Task Bridge — v1.0
        // 节点 → 一期任务链桥接
        // 将场景节点转换为可执行的任务链
        // =====================================================

        (function () {
          "use strict";

          if (window.NodeTaskBridge) return;

          const logger = window.TaskLogger || {
            info: function(msg, extra) { console.log('[NodeTaskBridge]', msg, extra || {}); },
            warn: function(msg, extra) { console.warn('[NodeTaskBridge]', msg, extra || {}); },
            error: function(msg, extra) { console.error('[NodeTaskBridge]', msg, extra || {}); }
          };

          class NodeTaskBridge {
            constructor() {
              this.taskTypeMap = {
                "SCAN_ENV": "SCAN_ENV",
                "MOVE_TO_NODE": "MOVE_TO_NODE",
                "CONFIRM_ARRIVAL": "CONFIRM_ARRIVAL"
              };
            }

            /** 生成并执行"前往节点"的任务链 */
            goToNode(nodeName, options) {
              options = options || {};
              
              // 确保 SceneNodes 已加载
              if (!window.SceneNodes) {
                logger.error("NodeTaskBridge", "SceneNodes 未加载", { nodeName });
                return;
              }

              // 检查节点是否存在
              const nodeMeta = window.SceneNodes.getNodeMeta(nodeName);
              if (!nodeMeta && !options.force) {
                logger.warn("NodeTaskBridge", "节点不存在或未确认", { nodeName });
                return;
              }

              // 构建任务链
              const chain = window.SceneNodes.buildTaskChainFor(nodeName);
              
              if (!chain || chain.length === 0) {
                logger.warn("NodeTaskBridge", "无法生成任务链", { nodeName });
                return;
              }

              // 确保 taskChain 已加载
              if (!window.taskChain) {
                logger.error("NodeTaskBridge", "taskChain 未加载", { nodeName });
                return;
              }

              // 将任务链加入队列
              chain.forEach((task, index) => {
                const priority = index === 0 ? 'HIGH' : 'MEDIUM';
                window.taskChain.enqueue({
                  type: task.type,
                  payload: Object.assign({}, task.payload, options.payload || {}),
                  priority: options.priority || priority
                });
              });

              logger.info("NodeTaskBridge", "生成节点型任务链", {
                nodeName,
                steps: chain.length,
                scene: window.SceneNodes.currentScene
              });
            }

            /** 批量生成多个节点的任务链 */
            goToNodes(nodeNames, options) {
              if (!Array.isArray(nodeNames) || nodeNames.length === 0) {
                logger.warn("NodeTaskBridge", "节点列表为空", {});
                return;
              }

              nodeNames.forEach((nodeName, index) => {
                const nodeOptions = Object.assign({}, options || {}, {
                  priority: index === 0 ? 'HIGH' : 'MEDIUM'
                });
                this.goToNode(nodeName, nodeOptions);
              });

              logger.info("NodeTaskBridge", "批量生成节点任务链", {
                nodeCount: nodeNames.length,
                nodes: nodeNames
              });
            }

            /** 确认到达节点 */
            confirmArrival(nodeName) {
              if (!window.SceneNodes) {
                logger.error("NodeTaskBridge", "SceneNodes 未加载", { nodeName });
                return;
              }

              // 确认节点
              window.SceneNodes.confirmNode(nodeName, {
                confirmedBy: "user",
                confirmedAt: Date.now()
              });

              // 生成确认任务
              if (window.taskChain) {
                window.taskChain.enqueue({
                  type: "CONFIRM_ARRIVAL",
                  payload: {
                    nodeName: nodeName,
                    scene: window.SceneNodes.currentScene
                  },
                  priority: "MEDIUM"
                });
              }

              logger.info("NodeTaskBridge", "确认到达节点", { nodeName });
            }

            /** 获取节点的任务链预览（不执行） */
            previewTaskChain(nodeName) {
              if (!window.SceneNodes) {
                return null;
              }

              return window.SceneNodes.buildTaskChainFor(nodeName);
            }
          }

          window.NodeTaskBridge = new NodeTaskBridge();
          console.log("[NodeTaskBridge] 已加载");
        })();
        /* ===== END: node_task_bridge.js ===== */
    </script>

    <script>
        /* ===== BEGIN: scene_pattern_reasoner.js ===== */
        // frontend/scene_pattern_reasoner.js
        // 场景模式推理：记录节点序列 → 推测下一步节点

        (function () {
          "use strict";

          if (window.ScenePatternReasoner) return;

          const logger = window.TaskLogger || {
            info: console.log,
            warn: console.warn,
            error: console.error,
          };

          class ScenePatternReasoner {
            constructor() {
              this.currentScene = null;
              this.currentSequence = [];
              this.patternMemory = {}; // {sceneName: {sequences: [...], stats: {...}}}
              this.observers = [];
            }

            enterScene(sceneName) {
              this.currentScene = sceneName;
              this.currentSequence = [];

              if (!this.patternMemory[sceneName]) {
                this.patternMemory[sceneName] = {
                  sequences: [],
                  stats: {},
                  lastSuggested: null,
                };
              }

              logger.info("ScenePatternReasoner", "进入场景", { sceneName });
            }

            recordNodeArrival(nodeName) {
              if (!this.currentScene) return;

              this.currentSequence.push(nodeName);

              logger.info("ScenePatternReasoner", "抵达节点", {
                scene: this.currentScene,
                nodeName,
                stepIndex: this.currentSequence.length - 1,
              });

              this.observers.forEach(cb => cb(nodeName));
            }

            leaveScene() {
              const scene = this.currentScene;
              if (!scene || this.currentSequence.length === 0) return;

              this.patternMemory[scene].sequences.push([...this.currentSequence]);
              this._rebuildStats(scene);

              logger.info("ScenePatternReasoner", "场景离开，记录序列", {
                scene,
                sequence: this.currentSequence,
              });

              this.currentScene = null;
              this.currentSequence = [];
            }

            _rebuildStats(scene) {
              const data = this.patternMemory[scene];
              const sequences = data.sequences;
              const stats = {};

              sequences.forEach(seq => {
                for (let i = 0; i < seq.length - 1; i++) {
                  const A = seq[i];
                  const B = seq[i + 1];
                  if (!stats[A]) stats[A] = {};
                  if (!stats[A][B]) stats[A][B] = 0;
                  stats[A][B]++;
                }
              });

              data.stats = stats;
              logger.info("ScenePatternReasoner", "更新转移概率", { scene, stats });
            }

            predictNext(nodeName) {
              const scene = this.currentScene;
              if (!scene) return null;

              const stats = this.patternMemory[scene].stats;
              if (!stats[nodeName]) return null;

              const candidates = stats[nodeName];
              const sorted = Object.entries(candidates).sort((a, b) => b[1] - a[1]);
              const predicted = sorted.length > 0 ? sorted[0][0] : null;

              logger.info("ScenePatternReasoner", "推测下一节点", {
                current: nodeName,
                predicted,
                candidates,
              });

              return predicted;
            }

            overwriteSequence(sceneName, newSequence) {
              this.patternMemory[sceneName] = {
                sequences: [newSequence],
                stats: {},
                lastSuggested: null,
              };
              this._rebuildStats(sceneName);

              logger.info("ScenePatternReasoner", "用户覆盖场景模式", {
                scene: sceneName,
                newSequence,
              });
            }

            getScenePattern(sceneName) {
              return this.patternMemory[sceneName] || null;
            }
          }

          window.ScenePatternReasoner = new ScenePatternReasoner();
        })();
        /* ===== END: scene_pattern_reasoner.js ===== */
    </script>

    <!-- ============================ -->
    <!-- Node Memory & Inference System -->
    <!-- ============================ -->
    <script>
        /* ===== BEGIN: node_memory.js ===== */
        // node_memory.js
        // 节点记忆：支持按 regionId 存不同城市/场景的节点图
        (function () {
          'use strict';
          const STORAGE_KEY = 'luna_node_memory_v1';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          function nowTs() {
            return Date.now();
          }
          let memory = {
            regions: {}
          };
          function loadFromStorage() {
            try {
              const raw = window.localStorage.getItem(STORAGE_KEY);
              if (!raw) return;
              const parsed = JSON.parse(raw);
              if (parsed && parsed.regions) {
                memory = parsed;
                log('node_memory_loaded', { regions: Object.keys(memory.regions) });
              }
            } catch (e) {
              log('node_memory_load_error', { error: e.toString() });
            }
          }
          function saveToStorage() {
            try {
              const payload = JSON.stringify(memory);
              window.localStorage.setItem(STORAGE_KEY, payload);
            } catch (e) {
              log('node_memory_save_error', { error: e.toString() });
            }
          }
          let saveTimer = null;
          function scheduleSave() {
            if (saveTimer) return;
            saveTimer = setTimeout(() => {
              saveTimer = null;
              saveToStorage();
            }, 1500);
          }
          function ensureRegion(regionId) {
            if (!regionId) regionId = 'default';
            if (!memory.regions[regionId]) {
              memory.regions[regionId] = {
                nodes: {},
                updatedAt: nowTs()
              };
              log('node_region_created', { regionId });
              scheduleSave();
            }
            return memory.regions[regionId];
          }
          function addOrUpdateNode(regionId, nodeData) {
            const region = ensureRegion(regionId);
            const id = nodeData.id || nodeData.key || ('node-' + nowTs() + '-' + Math.floor(Math.random() * 9999));
            const existing = region.nodes[id];
            const merged = existing ? { ...existing } : {
              id,
              createdAt: nowTs(),
              confirmations: 0,
              corrections: 0
            };
            merged.type = nodeData.type || merged.type || 'unknown';
            merged.role = nodeData.role || merged.role || null;
            merged.confidence = nodeData.confidence != null ? nodeData.confidence : (merged.confidence || 0.5);
            merged.source = nodeData.source || merged.source || 'inferred';
            merged.regionId = regionId;
            merged.meta = Object.assign({}, merged.meta || {}, nodeData.meta || {});
            if (nodeData.position) {
              merged.position = nodeData.position;
            }
            merged.updatedAt = nowTs();
            region.nodes[id] = merged;
            region.updatedAt = merged.updatedAt;
            log('node_memory_upsert', { regionId, node: merged });
            scheduleSave();
            return merged;
          }
          function getNodes(regionId, filter = {}) {
            const region = ensureRegion(regionId);
            const nodes = Object.values(region.nodes);
            if (!filter || Object.keys(filter).length === 0) return nodes;
            return nodes.filter(n => {
              if (filter.type && n.type !== filter.type) return false;
              if (filter.role && n.role !== filter.role) return false;
              if (filter.source && n.source !== filter.source) return false;
              if (filter.minConfidence && n.confidence < filter.minConfidence) return false;
              return true;
            });
          }
          function recordUserFeedback(regionId, nodeId, feedback) {
            const region = ensureRegion(regionId);
            const node = region.nodes[nodeId];
            if (!node) {
              log('node_feedback_missing', { regionId, nodeId, feedback });
              return null;
            }
            if (feedback.correct === true) {
              node.confirmations = (node.confirmations || 0) + 1;
              node.confidence = Math.min(1, (node.confidence || 0.5) + 0.1);
            } else if (feedback.correct === false) {
              node.corrections = (node.corrections || 0) + 1;
              node.confidence = Math.max(0, (node.confidence || 0.5) - 0.15);
            }
            if (feedback.newRole) {
              node.role = feedback.newRole;
              node.source = 'user';
            }
            if (feedback.newName) {
              node.meta = node.meta || {};
              node.meta.displayName = feedback.newName;
              node.source = 'user';
            }
            node.updatedAt = nowTs();
            region.updatedAt = node.updatedAt;
            log('node_feedback_applied', { regionId, node });
            scheduleSave();
            return node;
          }
          function getRegionSnapshot(regionId) {
            const region = ensureRegion(regionId);
            return {
              regionId,
              updatedAt: region.updatedAt,
              nodes: Object.values(region.nodes)
            };
          }
          loadFromStorage();
          window.NodeMemory = {
            ensureRegion,
            addOrUpdateNode,
            getNodes,
            recordUserFeedback,
            getRegionSnapshot
          };
        })();
        /* ===== END: node_memory.js ===== */
    </script>
    <script>
        /* ===== BEGIN: node_inference.js ===== */
        // node_inference.js
        // 基于 YOLO + OCR 的节点推理（社会节点 + 推理节点）
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          const KEYWORDS = {
            toilet: ['厕所', '卫生间', '洗手间', 'WC', 'Toilet', 'Restroom'],
            elevator: ['电梯', '升降机', 'Elevator', 'Lift'],
            exit: ['出口', '安全出口', 'Exit'],
            entrance: ['入口', '大门', 'Entrance', 'Gate'],
            register: ['挂号', '登记', 'Registration'],
            payment: ['收费', '缴费', '收银', '收费处', '支付', '扫码支付', '收银台', '收费窗口'],
            inquiry: ['咨询', '问询', '服务台', '服务中心', 'Information'],
            lab: ['检验科', '检验', '化验', '化验室', '检验室'],
            waiting: ['候诊', '等候区', '候车', 'Waiting Area', '等候'],
            subway: ['地铁', 'Metro', 'Subway', '站台', '站厅'],
            bus: ['公交车站', '车站', 'Bus Stop', '公交站'],
            crosswalk: ['斑马线', '人行横道']
          };
          function textContainsAny(text, list) {
            if (!text) return false;
            return list.some(k => text.includes(k));
          }
          function groupObjects(yoloObjects) {
            const res = {
              persons: [],
              counters: [],
              screens: [],
              qrCodes: [],
              doors: [],
              elevators: [],
              others: []
            };
            if (!Array.isArray(yoloObjects)) return res;
            for (const obj of yoloObjects) {
              const label = (obj.label || '').toLowerCase();
              if (label === 'person' || label === 'people' || label === 'human') {
                res.persons.push(obj);
              } else if (label.includes('counter') || label.includes('desk') || label.includes('table')) {
                res.counters.push(obj);
              } else if (label.includes('screen') || label.includes('monitor')) {
                res.screens.push(obj);
              } else if (label.includes('qr') || label.includes('qrcode') || label.includes('barcode')) {
                res.qrCodes.push(obj);
              } else if (label.includes('door') || label.includes('entrance') || label.includes('gate')) {
                res.doors.push(obj);
              } else if (label.includes('elevator') || label.includes('escalator')) {
                res.elevators.push(obj);
              } else {
                res.others.push(obj);
              }
            }
            return res;
          }
          function inferNodes(frame) {
            const { regionId, yoloObjects, ocrText, positionHint } = frame || {};
            if (!yoloObjects && !ocrText) return [];
            const nodes = [];
            const grouped = groupObjects(yoloObjects || []);
            const pos = positionHint || null;
            if (textContainsAny(ocrText, KEYWORDS.toilet)) {
              nodes.push({ type: 'facility', role: 'toilet', confidence: 0.95, source: 'social', position: pos, meta: { keywordsHit: 'toilet' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.elevator)) {
              nodes.push({ type: 'facility', role: 'elevator', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'elevator' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.exit)) {
              nodes.push({ type: 'facility', role: 'exit', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'exit' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.entrance)) {
              nodes.push({ type: 'facility', role: 'entrance', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'entrance' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.register)) {
              nodes.push({ type: 'service', role: 'registration', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'register' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.payment)) {
              nodes.push({ type: 'service', role: 'payment', confidence: 0.92, source: 'social', position: pos, meta: { keywordsHit: 'payment' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.inquiry)) {
              nodes.push({ type: 'service', role: 'inquiry', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'inquiry' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.lab)) {
              nodes.push({ type: 'department', role: 'lab', confidence: 0.9, source: 'social', position: pos, meta: { keywordsHit: 'lab' } });
            }
            if (textContainsAny(ocrText, KEYWORDS.waiting)) {
              nodes.push({ type: 'area', role: 'waiting_area', confidence: 0.88, source: 'social', position: pos, meta: { keywordsHit: 'waiting' } });
            }
            if (grouped.counters.length && grouped.qrCodes.length && grouped.persons.length) {
              nodes.push({ type: 'service', role: 'payment_candidate', confidence: 0.7, source: 'inferred', position: pos, meta: { counters: grouped.counters.length, qrCodes: grouped.qrCodes.length, persons: grouped.persons.length } });
            }
            if (grouped.counters.length && grouped.persons.length >= 3) {
              nodes.push({ type: 'service', role: 'queue_candidate', confidence: 0.65, source: 'inferred', position: pos, meta: { counters: grouped.counters.length, persons: grouped.persons.length } });
            }
            if (grouped.doors.length && grouped.persons.length >= 2) {
              nodes.push({ type: 'facility', role: 'entrance_candidate', confidence: 0.6, source: 'inferred', position: pos, meta: { doors: grouped.doors.length, persons: grouped.persons.length } });
            }
            if (grouped.elevators.length) {
              nodes.push({ type: 'facility', role: 'elevator_candidate', confidence: 0.7, source: 'inferred', position: pos, meta: { elevators: grouped.elevators.length } });
            }
            if (nodes.length > 0) {
              log('node_inference_result', { regionId, ocrText, counts: { total: nodes.length, social: nodes.filter(n => n.source === 'social').length, inferred: nodes.filter(n => n.source === 'inferred').length } });
            }
            return nodes;
          }
          window.NodeInference = { inferNodes };
        })();
        /* ===== END: node_inference.js ===== */
    </script>
    <script>
        /* ===== BEGIN: node_engine.js ===== */
        // node_engine.js
        // 节点总控引擎：整合推理 + 记忆 + 用户修正接口
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          function getCurrentRegionId() {
            if (typeof window.getCurrentRegionId === 'function') {
              return window.getCurrentRegionId();
            }
            if (window.currentRegionId) return window.currentRegionId;
            return 'default';
          }
          function processFrame(frame) {
            const regionId = frame.regionId || getCurrentRegionId();
            if (!window.NodeInference || !window.NodeMemory) {
              log('node_engine_missing_dependency', { hasInference: !!window.NodeInference, hasMemory: !!window.NodeMemory });
              return;
            }
            const candidates = window.NodeInference.inferNodes({ regionId, yoloObjects: frame.yoloObjects, ocrText: frame.ocrText, positionHint: frame.positionHint || null });
            const storedNodes = [];
            for (const c of candidates) {
              const node = window.NodeMemory.addOrUpdateNode(regionId, { type: c.type, role: c.role, confidence: c.confidence, position: c.position, source: c.source, meta: c.meta });
              storedNodes.push(node);
            }
            if (storedNodes.length) {
              log('node_engine_frame_processed', { regionId, createdNodes: storedNodes.map(n => ({ id: n.id, role: n.role, confidence: n.confidence, source: n.source })) });
              
              // ✅ E4: 自动区域识别 - 输入节点特征
              if (window.ZoneAutoDetector && storedNodes.length > 0) {
                storedNodes.forEach(n => {
                  window.ZoneAutoDetector.feedNode({
                    label: (n.meta && n.meta.displayName) || n.role || "节点",
                    role: n.role,
                    type: n.type
                  });
                });
              }
            }
            return storedNodes;
          }
          function getNodesForNavigation(filter) {
            const regionId = getCurrentRegionId();
            if (!window.NodeMemory) return [];
            return window.NodeMemory.getNodes(regionId, filter || {});
          }
          function userConfirmNode(options) {
            const regionId = getCurrentRegionId();
            if (!window.NodeMemory) return null;
            const updated = window.NodeMemory.recordUserFeedback(regionId, options.nodeId, { correct: options.correct, newRole: options.newRole, newName: options.newName });
            if (updated) {
              log('node_engine_user_confirm', { regionId, node: { id: updated.id, role: updated.role, confidence: updated.confidence } });
            }
            return updated;
          }
          function getRegionSnapshot() {
            const regionId = getCurrentRegionId();
            if (!window.NodeMemory) return null;
            return window.NodeMemory.getRegionSnapshot(regionId);
          }
          window.NodeEngine = { processFrame, getNodesForNavigation, userConfirmNode, getRegionSnapshot };
          window.LunaNodes = window.LunaNodes || {};
          window.LunaNodes.processFrame = processFrame;
          window.LunaNodes.userConfirmNode = userConfirmNode;
          window.LunaNodes.getNodesForNavigation = getNodesForNavigation;
          window.LunaNodes.getRegionSnapshot = getRegionSnapshot;
        })();
        /* ===== END: node_engine.js ===== */
    </script>
    <script>
        /* ===== BEGIN: node_dynamic_update.js ===== */
        // node_dynamic_update.js
        // 视觉节点的动态更新机制：固定节点更新 + 临时节点管理
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          const TEMPORARY_NODE_TYPES = ['施工', '积水', '移动障碍', '临时摊位', 'construction', 'water', 'temporary'];
          const DRIFT_THRESHOLD = 2.0;
          const POSITION_TOLERANCE = 0.5;
          let currentSessionId = null;
          let sessionTempNodes = [];
          function getCurrentSessionId() {
            if (!currentSessionId) {
              currentSessionId = 'session-' + Date.now();
              log('session_started', { sessionId: currentSessionId });
            }
            return currentSessionId;
          }
          function isTemporaryNode(node) {
            const type = (node.type || '').toLowerCase();
            const role = (node.role || '').toLowerCase();
            return TEMPORARY_NODE_TYPES.some(t => 
              type.includes(t.toLowerCase()) || role.includes(t.toLowerCase())
            );
          }
          function processNodeUpdate(regionId, nodeData, visualFeature = null) {
            if (!window.NodeMemory) {
              log('node_update_no_memory', {});
              return null;
            }
            const isTemp = isTemporaryNode(nodeData);
            nodeData.is_temporary = isTemp;
            if (visualFeature) {
              nodeData.visual_feature = visualFeature;
            }
            if (isTemp) {
              const sessionId = getCurrentSessionId();
              const tempNode = { ...nodeData, sessionId, detectedAt: Date.now() };
              sessionTempNodes.push(tempNode);
              log('temp_node_detected', { sessionId, node: tempNode });
              return tempNode;
            }
            const existing = window.NodeMemory.getNodes(regionId, { role: nodeData.role, type: nodeData.type }).find(n => {
              if (n.role !== nodeData.role || n.type !== nodeData.type) return false;
              if (n.position && nodeData.position) {
                const dist = window.NodeMemory.calculateDistance(n.position, nodeData.position);
                return dist < 3.0;
              }
              return false;
            });
            if (existing) {
              const needsUpdate = checkIfNeedsUpdate(existing, nodeData);
              if (needsUpdate) {
                const updated = applyNodeUpdate(regionId, existing.id, nodeData);
                log('node_updated_by_observation', { regionId, nodeId: existing.id, driftScore: updated.drift_score, version: updated.version });
                return updated;
              } else {
                existing.confirmations = (existing.confirmations || 0) + 1;
                return existing;
              }
            } else {
              return window.NodeMemory.addOrUpdateNode(regionId, nodeData);
            }
          }
          function checkIfNeedsUpdate(existing, newData) {
            if (existing.position && newData.position) {
              const dist = window.NodeMemory.calculateDistance(existing.position, newData.position);
              if (dist > POSITION_TOLERANCE) return true;
            }
            if (existing.visual_feature && newData.visual_feature) {
              if (existing.visual_feature !== newData.visual_feature) return true;
            }
            if ((existing.drift_score || 0) > DRIFT_THRESHOLD) return true;
            return false;
          }
          function applyNodeUpdate(regionId, nodeId, newData) {
            const region = window.NodeMemory.ensureRegion(regionId);
            const node = region.nodes[nodeId];
            if (!node) return null;
            if (newData.position) node.position = newData.position;
            if (newData.visual_feature) node.visual_feature = newData.visual_feature;
            node.version = (node.version || 1) + 1;
            node.updatedBy = 'observation';
            node.updatedAt = Date.now();
            node.drift_score = 0;
            log('node_update_applied', { regionId, nodeId, version: node.version });
            return node;
          }
          function getSessionTempNodes(sessionId = null) {
            const sid = sessionId || getCurrentSessionId();
            return sessionTempNodes.filter(n => n.sessionId === sid);
          }
          function clearSessionTempNodes(sessionId = null) {
            const sid = sessionId || getCurrentSessionId();
            const count = sessionTempNodes.length;
            sessionTempNodes = sessionTempNodes.filter(n => n.sessionId !== sid);
            log('session_temp_nodes_cleared', { sessionId: sid, clearedCount: count });
          }
          function endSession() {
            if (currentSessionId) {
              log('session_ended', { sessionId: currentSessionId, tempNodesCount: sessionTempNodes.length });
              clearSessionTempNodes(currentSessionId);
              currentSessionId = null;
            }
          }
          window.NodeDynamicUpdate = {
            processNodeUpdate,
            isTemporaryNode,
            getSessionTempNodes,
            clearSessionTempNodes,
            endSession,
            getCurrentSessionId
          };
        })();
        /* ===== END: node_dynamic_update.js ===== */
    </script>
    <script>
        /* ===== BEGIN: node_relocalization.js ===== */
        // node_relocalization.js
        // 图像节点 × 地图的实时校正（Re-Localization）
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          const POSITION_TOLERANCE = 2.0;
          const MIN_CONFIDENCE = 0.7;
          let currentEstimatedPosition = null;
          let lastRelocalizationTime = 0;
          const RELOCALIZATION_COOLDOWN = 2000;
          function relocalize(regionId, observedNode, cameraPosition = null) {
            if (!window.NodeMemory) {
              log('relocalize_no_memory', {});
              return null;
            }
            const now = Date.now();
            if (now - lastRelocalizationTime < RELOCALIZATION_COOLDOWN) {
              return null;
            }
            const storedNodes = window.NodeMemory.getNodes(regionId, {
              role: observedNode.role,
              type: observedNode.type,
              minConfidence: MIN_CONFIDENCE
            });
            if (storedNodes.length === 0) return null;
            let bestMatch = null;
            let minDistance = Infinity;
            for (const stored of storedNodes) {
              if (!stored.position || !observedNode.position) continue;
              const dist = window.NodeMemory.calculateDistance(stored.position, observedNode.position);
              if (dist < minDistance) {
                minDistance = dist;
                bestMatch = stored;
              }
            }
            if (!bestMatch || minDistance > POSITION_TOLERANCE) {
              return null;
            }
            const offset = {
              x: observedNode.position.x - bestMatch.position.x,
              y: observedNode.position.y - bestMatch.position.y
            };
            if (minDistance > POSITION_TOLERANCE) {
              const adjustment = applyMapAdjustment(regionId, bestMatch, offset);
              log('relocalization_applied', { regionId, nodeId: bestMatch.id, offset, distance: minDistance, adjustment });
              lastRelocalizationTime = now;
              return adjustment;
            }
            currentEstimatedPosition = {
              x: bestMatch.position.x,
              y: bestMatch.position.y,
              confidence: bestMatch.confidence,
              nodeId: bestMatch.id
            };
            log('relocalization_position_updated', { regionId, position: currentEstimatedPosition });
            return { adjusted: false, position: currentEstimatedPosition };
          }
          function applyMapAdjustment(regionId, anchorNode, offset) {
            const region = window.NodeMemory.ensureRegion(regionId);
            const nodes = Object.values(region.nodes);
            const maxAdjustDistance = 5.0;
            const nearbyNodes = nodes.filter(n => {
              if (n.id === anchorNode.id) return false;
              if (!n.position) return false;
              const dist = window.NodeMemory.calculateDistance(anchorNode.position, n.position);
              return dist < maxAdjustDistance;
            });
            for (const node of nearbyNodes) {
              const dist = window.NodeMemory.calculateDistance(anchorNode.position, node.position);
              const weight = 1 - (dist / maxAdjustDistance);
              if (node.position) {
                node.position.x = (node.position.x || 0) + offset.x * weight * 0.3;
                node.position.y = (node.position.y || 0) + offset.y * weight * 0.3;
                node.updatedAt = Date.now();
                node.adjustedBy = 'relocalization';
              }
            }
            log('map_adjustment_applied', { regionId, anchorNodeId: anchorNode.id, adjustedNodesCount: nearbyNodes.length, offset });
            return {
              adjusted: true,
              anchorNodeId: anchorNode.id,
              adjustedNodesCount: nearbyNodes.length,
              offset
            };
          }
          function getCurrentPosition() {
            return currentEstimatedPosition;
          }
          function setCurrentPosition(position) {
            currentEstimatedPosition = position;
            log('position_set_manually', { position });
          }
          function quickLocalize(regionId, observedNodes) {
            if (!observedNodes || observedNodes.length === 0) return null;
            const storedNodes = window.NodeMemory.getNodes(regionId, { minConfidence: MIN_CONFIDENCE });
            if (storedNodes.length === 0) return null;
            let bestMatch = null;
            let maxMatches = 0;
            for (const stored of storedNodes) {
              const matches = observedNodes.filter(obs => 
                obs.role === stored.role && 
                obs.type === stored.type &&
                obs.confidence >= MIN_CONFIDENCE
              ).length;
              if (matches > maxMatches) {
                maxMatches = matches;
                bestMatch = stored;
              }
            }
            if (bestMatch && maxMatches >= 1) {
              currentEstimatedPosition = {
                x: bestMatch.position?.x || 0,
                y: bestMatch.position?.y || 0,
                confidence: bestMatch.confidence,
                nodeId: bestMatch.id
              };
              log('quick_localize_success', { regionId, nodeId: bestMatch.id, matches: maxMatches });
              return currentEstimatedPosition;
            }
            return null;
          }
          window.NodeRelocalization = {
            relocalize,
            getCurrentPosition,
            setCurrentPosition,
            quickLocalize
          };
        })();
        /* ===== END: node_relocalization.js ===== */
    </script>
    <script>
        /* ===== BEGIN: navigation_accelerator.js ===== */
        // navigation_accelerator.js
        // 节点 × 路线 × 视觉记忆 三合一的加速导航
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          let currentNavigation = {
            active: false,
            from: null,
            to: null,
            route: null,
            startTime: null,
            visitedNodes: [],
            currentPosition: null
          };
          function initializeNavigation(regionId, targetNodeId, options = {}) {
            if (!window.NodeMemory || !window.NodeRelocalization) {
              log('nav_init_no_dependencies', {});
              return null;
            }
            const regionId_final = regionId || (window.getCurrentRegionId ? window.getCurrentRegionId() : 'default');
            const observedNodes = options.observedNodes || [];
            let startPosition = null;
            if (observedNodes.length > 0 && window.NodeRelocalization.quickLocalize) {
              startPosition = window.NodeRelocalization.quickLocalize(regionId_final, observedNodes);
            }
            if (!startPosition && options.geoPosition) {
              startPosition = {
                x: options.geoPosition.x || 0,
                y: options.geoPosition.y || 0,
                confidence: 0.5,
                source: 'geo'
              };
            }
            const regionNodes = window.NodeMemory.getNodes(regionId_final, {});
            const targetNode = regionNodes.find(n => n.id === targetNodeId);
            if (!targetNode) {
              log('nav_init_target_not_found', { targetNodeId });
              return null;
            }
            const from = startPosition ? `pos_${startPosition.x}_${startPosition.y}` : 'unknown';
            const to = targetNodeId;
            let route = null;
            if (window.NodeMemory.getAuthoritativePath) {
              route = window.NodeMemory.getAuthoritativePath(from, to);
            }
            if (!route) {
              route = generateInitialRoute(regionNodes, startPosition, targetNode);
            }
            currentNavigation = {
              active: true,
              from: from,
              to: to,
              route: route,
              startTime: Date.now(),
              visitedNodes: [],
              currentPosition: startPosition,
              regionId: regionId_final
            };
            log('nav_initialized', {
              regionId: regionId_final,
              from,
              to,
              hasAuthoritativePath: !!route && route.visitCount >= 2,
              route
            });
            return currentNavigation;
          }
          function generateInitialRoute(nodes, startPos, targetNode) {
            const viaNodes = [];
            if (startPos && targetNode.position) {
              const midNodes = nodes.filter(n => {
                if (!n.position) return false;
                const distToStart = window.NodeMemory.calculateDistance(startPos, n.position);
                const distToTarget = window.NodeMemory.calculateDistance(n.position, targetNode.position);
                return distToStart < 10 && distToTarget < 10;
              });
              viaNodes.push(...midNodes.slice(0, 3));
            }
            return {
              from: startPos ? `pos_${startPos.x}_${startPos.y}` : 'unknown',
              to: targetNode.id,
              viaNodes: viaNodes.map(n => n.id),
              estimatedTime: 0,
              safetyScore: 0.7,
              smoothnessScore: 0.7
            };
          }
          function updateNavigation(observedNodes, cameraPosition = null) {
            if (!currentNavigation.active) return null;
            const { regionId, route } = currentNavigation;
            if (!regionId || !route) return null;
            const updates = {
              positionCorrected: false,
              newNodesDetected: [],
              mapAdjusted: false,
              routeAdjusted: false
            };
            if (observedNodes && observedNodes.length > 0) {
              for (const obsNode of observedNodes) {
                if (obsNode.role && obsNode.type) {
                  if (window.NodeRelocalization && window.NodeRelocalization.relocalize) {
                    const relocResult = window.NodeRelocalization.relocalize(regionId, obsNode, cameraPosition);
                    if (relocResult && relocResult.adjusted) {
                      updates.positionCorrected = true;
                      updates.mapAdjusted = true;
                      currentNavigation.currentPosition = relocResult.position;
                    }
                  }
                  const storedNodes = window.NodeMemory.getNodes(regionId, {
                    role: obsNode.role,
                    type: obsNode.type
                  });
                  if (storedNodes.length === 0) {
                    if (window.NodeDynamicUpdate && window.NodeDynamicUpdate.processNodeUpdate) {
                      const tempNode = window.NodeDynamicUpdate.processNodeUpdate(regionId, obsNode);
                      if (tempNode && tempNode.is_temporary) {
                        updates.newNodesDetected.push(tempNode);
                      }
                    }
                  } else {
                    const nodeId = storedNodes[0].id;
                    if (!currentNavigation.visitedNodes.includes(nodeId)) {
                      currentNavigation.visitedNodes.push(nodeId);
                    }
                  }
                }
              }
            }
            if (updates.positionCorrected && route.viaNodes) {
              const adjusted = adjustRouteForDeviation(route, currentNavigation.currentPosition);
              if (adjusted) {
                updates.routeAdjusted = true;
                currentNavigation.route = adjusted;
              }
            }
            log('nav_updated', {
              updates,
              visitedNodesCount: currentNavigation.visitedNodes.length
            });
            return updates;
          }
          function adjustRouteForDeviation(route, currentPos) {
            if (!currentPos || !route.viaNodes || route.viaNodes.length === 0) {
              return null;
            }
            return route;
          }
          function completeNavigation() {
            if (!currentNavigation.active) return null;
            const { from, to, route, startTime, visitedNodes } = currentNavigation;
            const timeUsed = (Date.now() - startTime) / 1000;
            const safetyScore = calculateSafetyScore(visitedNodes);
            const smoothnessScore = calculateSmoothnessScore(route, visitedNodes);
            const pathData = {
              from,
              to,
              viaNodes: visitedNodes,
              timeUsed,
              safetyScore,
              smoothnessScore
            };
            let pathRecord = null;
            if (window.NodeMemory && window.NodeMemory.recordPath) {
              pathRecord = window.NodeMemory.recordPath(pathData);
            }
            if (pathRecord && window.NodeMemory && window.NodeMemory.updatePathScore) {
              const existingPaths = Object.values(window.NodeMemory.paths || {}).filter(p => 
                p.from === from && p.to === to
              );
              if (existingPaths.length > 0) {
                const similarPath = existingPaths[0];
                window.NodeMemory.updatePathScore(similarPath.pathId, {
                  timeUsed,
                  safetyScore,
                  smoothnessScore
                });
              }
            }
            log('nav_completed', {
              from,
              to,
              timeUsed,
              safetyScore,
              smoothnessScore,
              pathRecord
            });
            currentNavigation = {
              active: false,
              from: null,
              to: null,
              route: null,
              startTime: null,
              visitedNodes: [],
              currentPosition: null
            };
            return pathRecord;
          }
          function calculateSafetyScore(visitedNodes) {
            return 0.8;
          }
          function calculateSmoothnessScore(route, visitedNodes) {
            if (!route || !route.viaNodes) return 0.7;
            const matchRatio = visitedNodes.filter(id => route.viaNodes.includes(id)).length / route.viaNodes.length;
            return Math.min(1, matchRatio);
          }
          function getNavigationState() {
            return { ...currentNavigation };
          }
          function stopNavigation() {
            if (currentNavigation.active) {
              completeNavigation();
            }
            currentNavigation.active = false;
          }
          window.NavigationAccelerator = {
            initializeNavigation,
            updateNavigation,
            completeNavigation,
            getNavigationState,
            stopNavigation
          };
        })();
        /* ===== END: navigation_accelerator.js ===== */
    </script>
    <script>
        /* ===== BEGIN: node_bridge.js ===== */
        // node_bridge.js
        // YOLO / OCR 与 NodeEngine 的桥接层
        (function () {
          'use strict';
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            }
          }
          function handleVisionFrameForNodes() {
            if (!window.NodeEngine) {
              log('node_bridge_no_engine', {});
              return;
            }
            const yolo = window.latestYOLOResult || null;
            const ocrText = (window.latestOCRResult && window.latestOCRResult.text) || '';
            if (!yolo && !ocrText) {
              return;
            }
            const frame = {
              yoloObjects: Array.isArray(yolo) ? yolo : [],
              ocrText: ocrText || '',
              positionHint: null
            };
            const nodes = window.NodeEngine.processFrame(frame);
            if (nodes && nodes.length) {
              log('node_bridge_frame_nodes', { count: nodes.length, sample: nodes.slice(0, 3).map(n => ({ id: n.id, role: n.role, confidence: n.confidence, source: n.source })) });
            }
          }
          window.handleVisionFrameForNodes = handleVisionFrameForNodes;
        })();
        /* ===== END: node_bridge.js ===== */
    </script>

    <!-- ============================ -->
    <!-- Luna Unified Event Dispatcher -->
    <!-- ============================ -->
    <script>
        /* ===== BEGIN: unified_events.js ===== */
        /**
         * 统一事件派发系统（规范要求）
         * 提供统一的危险/台阶/导航事件处理流程
         */
        (function() {
            'use strict';
            
            // ========== 事件桥接层（平滑切换方案）==========
            window.EventBridge = {
                // 原事件：旧逻辑（兼容保留）
                legacy: {
                    hazard: null,  // window.handleHazardDetection
                    step: null,    // window.handleStepDetection
                    navigation: null // window.handleNavigationDecision
                },
                
                // 新事件：统一事件流
                unified: {
                    hazard: null,  // 将在下面定义
                    step: null,    // 将在下面定义
                    navigation: null // 将在下面定义
                },
                
                // 开关（默认双跑，确保平滑过渡）
                mode: {
                    hazard: "both",     // "legacy" | "unified" | "both"
                    step: "both",
                    navigation: "both"
                },
                
                /**
                 * 统一派发方法
                 */
                dispatch(type, data) {
                    const mode = this.mode[type];
                    
                    // 旧逻辑继续执行（兼容阶段）
                    if (mode === "legacy" || mode === "both") {
                        const legacyHandler = this.legacy[type];
                        if (legacyHandler && typeof legacyHandler === 'function') {
                            try {
                                legacyHandler(data);
                            } catch (error) {
                                console.error(`❌ [EventBridge] 旧逻辑执行失败 (${type}):`, error);
                            }
                        }
                    }
                    
                    // 新逻辑开始接管
                    if (mode === "unified" || mode === "both") {
                        const unifiedHandler = this.unified[type];
                        if (unifiedHandler && typeof unifiedHandler === 'function') {
                            try {
                                unifiedHandler(data);
                            } catch (error) {
                                console.error(`❌ [EventBridge] 新逻辑执行失败 (${type}):`, error);
                            }
                        }
                    }
                },
                
                /**
                 * 注册旧逻辑处理器（向后兼容）
                 */
                registerLegacy(type, handler) {
                    if (this.legacy.hasOwnProperty(type)) {
                        this.legacy[type] = handler;
                        console.log(`✅ [EventBridge] 注册旧逻辑处理器: ${type}`, { module: 'event_bridge' });
                    }
                },
                
                /**
                 * 切换模式（用于逐步迁移）
                 */
                switchMode(type, newMode) {
                    if (this.mode.hasOwnProperty(type) && ['legacy', 'unified', 'both'].includes(newMode)) {
                        const oldMode = this.mode[type];
                        this.mode[type] = newMode;
                        console.log(`🔄 [EventBridge] 切换模式: ${type} (${oldMode} → ${newMode})`, { module: 'event_bridge' });
                    }
                }
            };
            
            const messageTemplates = {
                hazard: { water: '前方有积水，请小心', obstacle: '前方有障碍物，请绕行', slippery: '地面湿滑，请减速', construction: '前方施工，请注意安全', default: '检测到危险区域，请小心' },
                step: { up: (d) => `前方${d || ''}米有台阶，请减速`, down: (d) => `前方${d || ''}米有下台阶，请小心`, default: (d) => `前方${d || ''}米有台阶，请注意` },
                navigation: { turn_left: (d) => `前方${d || ''}米左转`, turn_right: (d) => `前方${d || ''}米右转`, straight: (d) => `请直行${d ? d + '米' : ''}`, stop: () => '已到达目的地', default: () => '请跟随导航指引' }
            };
            
            // 统一事件处理函数（内部实现）
            function _emitHazardEventInternal({ type, level = 'medium', meta = {} }) {
                const templates = messageTemplates.hazard;
                const message = templates[type] || templates.default;
                console.log(`🚨 [统一事件] 危险事件: ${type}`, { module: 'unified_events' });
                const finalMessage = meta.message || message;
                
                // ③【新增：后台日志上传】
                if (window.sendLog) {
                    window.sendLog({ type: 'hazard_detected', hazardType: type, level, message: finalMessage });
                }
                
                if (window.taskChain) {
                    window.taskChain.enqueue('hazard_warning', { type, level, meta: { ...meta, message: finalMessage } }, level === 'critical' || level === 'high' ? 0 : 2);
                } else if (window.speakText) {
                    window.speakText(finalMessage, 'urgent');
                }
                const uiElement = document.getElementById('hazardAlert');
                if (uiElement) {
                    uiElement.textContent = finalMessage;
                    uiElement.className = `hazard-alert level-${level}`;
                    uiElement.style.display = 'block';
                    setTimeout(() => { uiElement.style.display = 'none'; }, 3000);
                }
                if (window.emotion_event) {
                    window.emotion_event('hazard_detected', level, { type, ...meta });
                }
                return { success: true, message: finalMessage, type, level };
            }
            
            function _emitStepEventInternal({ direction = 'up', distance, meta = {} }) {
                const templates = messageTemplates.step;
                const template = templates[direction] || templates.default;
                const message = template(distance);
                console.log(`📐 [统一事件] 台阶事件: ${direction}`, { module: 'unified_events' });
                const finalMessage = meta.message || message;
                
                // ③【新增：后台日志上传】
                if (window.sendLog) {
                    window.sendLog({ type: 'step_detected', direction, distance, message: finalMessage });
                }
                
                if (window.taskChain) {
                    window.taskChain.enqueue('step_warning', { direction, distance, meta: { ...meta, message: finalMessage } }, 0);
                } else if (window.speakText) {
                    window.speakText(finalMessage, 'urgent');
                }
                const uiElement = document.getElementById('stepAlert');
                if (uiElement) {
                    uiElement.textContent = finalMessage;
                    uiElement.className = 'step-alert critical';
                    uiElement.style.display = 'block';
                    setTimeout(() => { uiElement.style.display = 'none'; }, 3000);
                }
                if (window.emotion_event) {
                    window.emotion_event('step_detected', 'high', { direction, distance, ...meta });
                }
                return { success: true, message: finalMessage, direction, distance };
            }
            
            function _emitNavigationEventInternal({ action, direction, distance, meta = {} }) {
                const templates = messageTemplates.navigation;
                const subtype = action === 'turn' ? `turn_${direction}` : action;
                const template = templates[subtype] || templates.default;
                const message = template(distance);
                console.log(`🧭 [统一事件] 导航事件: ${action}`, { module: 'unified_events' });
                const finalMessage = meta.message || message;
                if (window.taskChain) {
                    window.taskChain.enqueue('navigation', { action, direction, distance, meta: { ...meta, message: finalMessage } }, 1);
                } else if (window.speakText) {
                    window.speakText(finalMessage, 'cheerful');
                }
                const uiElement = document.getElementById('navigationGuidance');
                if (uiElement) {
                    uiElement.textContent = finalMessage;
                    uiElement.className = `navigation-guidance action-${action}`;
                    uiElement.style.display = 'block';
                }
                return { success: true, message: finalMessage, action, direction, distance };
            }
            
            // 注册到EventBridge的统一处理器
            window.EventBridge.unified.hazard = _emitHazardEventInternal;
            window.EventBridge.unified.step = _emitStepEventInternal;
            window.EventBridge.unified.navigation = _emitNavigationEventInternal;
            
            // 对外暴露的统一事件接口（通过EventBridge派发）
            window.emitHazardEvent = function(data) {
                window.EventBridge.dispatch("hazard", data);
            };
            
            window.emitStepEvent = function(data) {
                window.EventBridge.dispatch("step", data);
            };
            
            window.emitNavigationEvent = function(data) {
                // ①【修复：导航无法持续语音播报】- 记录导航事件
                if (window.AutoRecovery) {
                    window.AutoRecovery.record('navigation', 'event', data);
                }
                
                // 交给导航状态机
                if (window.NavigationFSM) {
                    window.NavigationFSM.handleEvent(data);
                }
                
                // 路点系统推进
                if (window.WaypointManager) {
                    window.WaypointManager.checkProgress(data);
                }
                
                // 先通过导航策略层处理
                if (window.NavigationStrategy && window.NavigationStrategy.run) {
                    const decision = window.NavigationStrategy.run(data);
                    if (decision && decision.msg) {
                        // 如果有决策消息，强制进入TTS队列
                        if (window.taskChain) {
                            window.taskChain.enqueue('tts_broadcast', {
                                text: decision.msg,
                                style: decision.style || 'cheerful',
                                priority: true
                            }, 1);
                            // ④【加入：TaskChain完整日志】
                            console.log('[TaskChain] 导航TTS入队:', decision.msg);
                            if (window.sendLog) {
                                window.sendLog({ type: 'task_enqueue', taskType: 'tts_broadcast', payload: { text: decision.msg } });
                            }
                        } else if (window.speakText) {
                            window.speakText(decision.msg, 'cheerful');
                        }
                    }
                }
                // 再通过EventBridge派发
                window.EventBridge.dispatch("navigation", data);
                
                // ③【新增：后台日志上传】
                if (window.sendLog) {
                    window.sendLog({ type: 'navigation_event', payload: data });
                }
            };
            
            console.log('✅ UnifiedEventManager模块加载完成', { module: 'unified_events' });
        })();
        /* ===== END: unified_events.js ===== */
    </script>

    <!-- ========================= -->
    <!-- Navigation Strategy Layer -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: navigation_strategy.js ===== */
        /**
         * 导航策略层（规范要求：可插拔导航策略）
         * 支持不同场景：走廊/街道/地铁等
         */
        (function() {
            'use strict';
            
            window.NavigationStrategy = {
                current: "default",  // default | corridor | street | subway | indoor
                
                strategies: {
                    /**
                     * 默认策略（保持现有MVP逻辑）
                     */
                    default: {
                        decide(navData) {
                            // 保持原有逻辑，不做改变
                            return { action: "continue", msg: null };
                        }
                    },
                    
                    /**
                     * 走廊策略（室内导航）
                     */
                    corridor: {
                        decide(navData) {
                            const { direction, distance, detectedObjects } = navData || {};
                            
                            if (direction === "left") {
                                return { 
                                    action: "turn-left", 
                                    msg: `前方${distance || ''}米，建议在走廊左转。`,
                                    priority: "high"
                                };
                            }
                            
                            if (direction === "right") {
                                return { 
                                    action: "turn-right", 
                                    msg: `前方${distance || ''}米，建议在走廊右转。`,
                                    priority: "high"
                                };
                            }
                            
                            if (direction === "forward") {
                                return { 
                                    action: "go-forward", 
                                    msg: `请沿走廊直行${distance ? distance + '米' : ''}。`,
                                    priority: "medium"
                                };
                            }
                            
                            return { action: "continue", msg: null };
                        }
                    },
                    
                    /**
                     * 街道策略（室外导航）
                     */
                    street: {
                        decide(navData) {
                            const { direction, distance, hasVehicle, hasTrafficLight, trafficLightState, crowdDensity } = navData || {};
                            
                            // 车辆检测优先
                            if (hasVehicle) {
                                return { 
                                    action: "stop", 
                                    msg: "前方有车辆，请暂时停下，等待安全后再前行。",
                                    priority: "critical"
                                };
                            }
                            
                            // 红绿灯检测
                            if (hasTrafficLight) {
                                if (trafficLightState === "red") {
                                    return { 
                                        action: "stop", 
                                        msg: "前方红灯，请停下等待。",
                                        priority: "critical"
                                    };
                                } else if (trafficLightState === "green") {
                                    return { 
                                        action: "go-forward", 
                                        msg: "前方绿灯，可以安全前行。",
                                        priority: "high"
                                    };
                                }
                            }
                            
                            // 人群密集度检测
                            if (crowdDensity === "high") {
                                return { 
                                    action: "slow-down", 
                                    msg: "前方人群密集，请减速慢行。",
                                    priority: "high"
                                };
                            }
                            
                            // 方向判断
                            if (direction === "left") {
                                return { 
                                    action: "turn-left", 
                                    msg: `前方${distance || ''}米左转，请注意车辆。`,
                                    priority: "high"
                                };
                            }
                            
                            if (direction === "right") {
                                return { 
                                    action: "turn-right", 
                                    msg: `前方${distance || ''}米右转，请注意车辆。`,
                                    priority: "high"
                                };
                            }
                            
                            if (direction === "forward") {
                                return { 
                                    action: "go-forward", 
                                    msg: `可以前行${distance ? distance + '米' : ''}。`,
                                    priority: "medium"
                                };
                            }
                            
                            return { action: "continue", msg: null };
                        }
                    },
                    
                    /**
                     * 地铁策略（站台导航）
                     */
                    subway: {
                        decide(navData) {
                            const { sign, platform, direction, line } = navData || {};
                            
                            // 站台指示牌识别
                            if (sign) {
                                if (sign.includes("往") || sign.includes("方向")) {
                                    const destination = sign.match(/往(.+?)[站方向]/)?.[1] || sign.match(/往(.+)/)?.[1];
                                    if (destination) {
                                        return { 
                                            action: "go-platform", 
                                            msg: `请前往${destination}方向站台。`,
                                            priority: "high",
                                            meta: { destination, platform }
                                        };
                                    }
                                }
                                
                                if (sign.includes("站台") || sign.includes("Platform")) {
                                    const platformNum = sign.match(/[A-Z]|[\u4e00-\u9fa5]/)?.[0];
                                    return { 
                                        action: "go-platform", 
                                        msg: `请前往${platformNum || ''}站台。`,
                                        priority: "high",
                                        meta: { platform: platformNum }
                                    };
                                }
                            }
                            
                            // 线路识别
                            if (line) {
                                return { 
                                    action: "follow-line", 
                                    msg: `请跟随${line}号线指引。`,
                                    priority: "high",
                                    meta: { line }
                                };
                            }
                            
                            // 方向判断
                            if (direction === "left") {
                                return { 
                                    action: "turn-left", 
                                    msg: "请向左前往站台。",
                                    priority: "high"
                                };
                            }
                            
                            if (direction === "right") {
                                return { 
                                    action: "turn-right", 
                                    msg: "请向右前往站台。",
                                    priority: "high"
                                };
                            }
                            
                            return { action: "continue", msg: null };
                        }
                    },
                    
                    /**
                     * 室内策略（医院/商场等）
                     */
                    indoor: {
                        decide(navData) {
                            const { direction, distance, facility, floor, doorplate } = navData || {};
                            
                            // 设施导航
                            if (facility) {
                                return { 
                                    action: "go-facility", 
                                    msg: `前往${facility}，${direction === 'left' ? '左转' : direction === 'right' ? '右转' : '直行'}${distance ? distance + '米' : ''}。`,
                                    priority: "high",
                                    meta: { facility }
                                };
                            }
                            
                            // 楼层导航
                            if (floor) {
                                return { 
                                    action: "go-floor", 
                                    msg: `请前往${floor}层。`,
                                    priority: "high",
                                    meta: { floor }
                                };
                            }
                            
                            // 门牌号导航
                            if (doorplate) {
                                return { 
                                    action: "go-doorplate", 
                                    msg: `目标位置：${doorplate}。`,
                                    priority: "high",
                                    meta: { doorplate }
                                };
                            }
                            
                            // 方向判断
                            if (direction === "left") {
                                return { 
                                    action: "turn-left", 
                                    msg: `前方${distance || ''}米左转。`,
                                    priority: "medium"
                                };
                            }
                            
                            if (direction === "right") {
                                return { 
                                    action: "turn-right", 
                                    msg: `前方${distance || ''}米右转。`,
                                    priority: "medium"
                                };
                            }
                            
                            return { action: "continue", msg: null };
                        }
                    }
                },
                
                /**
                 * 执行策略决策
                 */
                run(navData) {
                    const strategy = this.strategies[this.current];
                    if (!strategy) {
                        console.warn(`⚠️ [NavigationStrategy] 未找到策略: ${this.current}`, { module: 'navigation_strategy' });
                        return this.strategies.default.decide(navData);
                    }
                    
                    try {
                        const decision = strategy.decide(navData);
                        console.log(`🧭 [NavigationStrategy] 策略决策: ${this.current} → ${decision.action}`, { module: 'navigation_strategy' });
                        return decision;
                    } catch (error) {
                        console.error(`❌ [NavigationStrategy] 策略执行失败: ${this.current}`, { module: 'navigation_strategy', error: error.message });
                        return this.strategies.default.decide(navData);
                    }
                },
                
                /**
                 * 切换策略
                 */
                switchStrategy(strategyName) {
                    if (this.strategies.hasOwnProperty(strategyName)) {
                        const oldStrategy = this.current;
                        this.current = strategyName;
                        console.log(`🔄 [NavigationStrategy] 切换策略: ${oldStrategy} → ${strategyName}`, { module: 'navigation_strategy' });
                        
                        // 触发策略切换事件
                        if (window.emotion_event) {
                            window.emotion_event('navigation_strategy_changed', 'medium', {
                                old: oldStrategy,
                                new: strategyName
                            });
                        }
                        
                        return true;
                    } else {
                        console.warn(`⚠️ [NavigationStrategy] 未知策略: ${strategyName}`, { module: 'navigation_strategy' });
                        return false;
                    }
                },
                
                /**
                 * 获取当前策略信息
                 */
                getCurrentStrategy() {
                    return {
                        name: this.current,
                        available: Object.keys(this.strategies),
                        description: this.strategies[this.current]?.description || '无描述'
                    };
                }
            };
            
            console.log('✅ NavigationStrategy模块加载完成', { module: 'navigation_strategy' });
        })();
        /* ===== END: navigation_strategy.js ===== */
    </script>

    <!-- ========================= -->
    <!-- Luna Emotion Hook System -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: emotion_hook.js ===== */
        /**
         * 情绪事件Hook系统（规范要求）
         * 为Luna情绪系统预留接口
         */
        (function() {
            'use strict';
            class EmotionEventManager {
                constructor() {
                    this.hooks = new Map();
                    this.eventHistory = [];
                    this.maxHistory = 50;
                    this.enabled = true;
                    this._registerDefaultHooks();
                    console.log('✅ EmotionEventManager初始化完成', { module: 'emotion_hook' });
                }
                _registerDefaultHooks() {
                    this.registerHook('hazard_detected', (level, meta) => {
                        console.log(`💭 [情绪事件] 危险检测: 级别=${level}`, { module: 'emotion_hook' });
                    });
                    this.registerHook('step_detected', (level, meta) => {
                        console.log(`💭 [情绪事件] 台阶检测: 级别=${level}`, { module: 'emotion_hook' });
                    });
                    this.registerHook('navigation_started', (level, meta) => {
                        console.log(`💭 [情绪事件] 导航开始`, { module: 'emotion_hook' });
                    });
                    this.registerHook('navigation_completed', (level, meta) => {
                        console.log(`💭 [情绪事件] 导航完成`, { module: 'emotion_hook' });
                    });
                    this.registerHook('system_error', (level, meta) => {
                        console.log(`💭 [情绪事件] 系统错误: 级别=${level}`, { module: 'emotion_hook' });
                    });
                }
                registerHook(eventName, handler) {
                    if (!this.hooks.has(eventName)) {
                        this.hooks.set(eventName, []);
                    }
                    this.hooks.get(eventName).push(handler);
                }
                trigger(eventName, level = 'medium', meta = {}) {
                    if (!this.enabled) return;
                    this.eventHistory.push({ event: eventName, level, meta, timestamp: Date.now() });
                    if (this.eventHistory.length > this.maxHistory) {
                        this.eventHistory.shift();
                    }
                    const handlers = this.hooks.get(eventName) || [];
                    handlers.forEach(handler => {
                        try {
                            handler(level, meta);
                        } catch (error) {
                            console.error(`❌ [情绪事件] Hook执行失败: ${eventName}`, error);
                        }
                    });
                }
                getHistory(limit = 10) {
                    return this.eventHistory.slice(-limit);
                }
                enable() { this.enabled = true; }
                disable() { this.enabled = false; }
            }
            const emotionManager = new EmotionEventManager();
            window.emotion_event = function(eventName, level = 'medium', meta = {}) {
                emotionManager.trigger(eventName, level, meta);
            };
            window.emotionEventManager = emotionManager;
        })();
        /* ===== END: emotion_hook.js ===== */
    </script>

    <!-- ===================== -->
    <!-- 模块加载验证 -->
    <!-- ===================== -->
    <script>
        // 验证所有模块已正确加载
        (function() {
            const checks = {
                taskChain: typeof window.taskChain !== 'undefined',
                EventBridge: typeof window.EventBridge !== 'undefined',
                NavigationStrategy: typeof window.NavigationStrategy !== 'undefined',
                emitHazardEvent: typeof window.emitHazardEvent !== 'undefined',
                emitStepEvent: typeof window.emitStepEvent !== 'undefined',
                emitNavigationEvent: typeof window.emitNavigationEvent !== 'undefined',
                emotion_event: typeof window.emotion_event !== 'undefined'
            };
            const allLoaded = Object.values(checks).every(v => v === true);
            if (allLoaded) {
                console.log('✅ 所有规范模块已加载完成', checks);
                console.log('✅ EventBridge模式:', window.EventBridge?.mode);
                console.log('✅ NavigationStrategy当前策略:', window.NavigationStrategy?.current);
                console.log('✅ 可用导航策略:', window.NavigationStrategy?.getCurrentStrategy?.()?.available);
            } else {
                console.warn('⚠️ 部分模块未加载', checks);
            }
        })();
    <!-- ========================= -->
    <!-- Safe Mode -->
    <!-- ========================= -->
    <script>
        /* BEGIN: safe_mode.js */
/**
 * Safe Mode（安全模式）系统（规范要求）
 * 提供安全模式，暂停核心功能但保留基础能力
 */

(function() {
    'use strict';

    window.SafeMode = {
        enabled: false,
        reason: null,
        originalStates: {},  // 保存原始状态
        
        /**
         * 启用安全模式
         */
        enable(reason = "用户手动启用") {
            if (this.enabled) {
                console.log('⚠️ [SafeMode] 安全模式已启用', { module: 'safe_mode' });
                return;
            }
            
            this.enabled = true;
            this.reason = reason;
            
            console.log(`🛡️ [SafeMode] 启用安全模式: ${reason}`, { module: 'safe_mode' });
            
            // 保存原始状态
            this.originalStates = {
                visionActive: window.productModeActive || false,
                navigationActive: window.navigationActive || false,
                taskChainActive: window.taskChain ? window.taskChain.running : false
            };
            
            // 暂停视觉分析
            if (window.productModeActive !== undefined) {
                window.productModeActive = false;
            }
            
            // 暂停导航决策
            if (window.navigationActive !== undefined) {
                window.navigationActive = false;
            }
            
            // 暂停任务链执行（通过标志）
            if (window.taskChain) {
                window.taskChain.running = false;
            }
            
            // 显示安全模式状态条
            this._showStatusBar();
            
            // 播报提示
            if (window.speakText) {
                window.speakText(`系统已进入安全模式：${reason}`, 'calm');
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('safe_mode_enabled', 'medium', { reason });
            }
        },
        
        /**
         * 禁用安全模式
         */
        disable() {
            if (!this.enabled) {
                console.log('ℹ️ [SafeMode] 安全模式未启用', { module: 'safe_mode' });
                return;
            }
            
            console.log('✅ [SafeMode] 禁用安全模式', { module: 'safe_mode' });
            
            this.enabled = false;
            const reason = this.reason;
            this.reason = null;
            
            // 恢复原始状态
            if (this.originalStates.visionActive !== undefined) {
                window.productModeActive = this.originalStates.visionActive;
            }
            
            if (this.originalStates.navigationActive !== undefined) {
                window.navigationActive = this.originalStates.navigationActive;
            }
            
            if (window.taskChain && this.originalStates.taskChainActive) {
                window.taskChain.running = true;
                // 重新处理队列
                if (window.taskChain.queue && window.taskChain.queue.length > 0) {
                    window.taskChain._processQueue();
                }
            }
            
            // 隐藏状态条
            this._hideStatusBar();
            
            // 播报提示
            if (window.speakText) {
                window.speakText('安全模式已关闭，系统恢复正常运行', 'cheerful');
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('safe_mode_disabled', 'medium', { previous_reason: reason });
            }
        },
        
        /**
         * 检查是否启用
         */
        isEnabled() {
            return this.enabled;
        },
        
        /**
         * 显示安全模式状态条
         */
        _showStatusBar() {
            // 移除旧的状态条（如果存在）
            const existingBar = document.getElementById('safeModeStatusBar');
            if (existingBar) {
                existingBar.remove();
            }
            
            // 创建状态条
            const statusBar = document.createElement('div');
            statusBar.id = 'safeModeStatusBar';
            statusBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #ff9800;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                z-index: 10000;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            `;
            statusBar.textContent = `🛡️ SAFE MODE ACTIVE: ${this.reason}`;
            
            document.body.insertBefore(statusBar, document.body.firstChild);
        },
        
        /**
         * 隐藏安全模式状态条
         */
        _hideStatusBar() {
            const statusBar = document.getElementById('safeModeStatusBar');
            if (statusBar) {
                statusBar.remove();
            }
        },
        
        /**
         * 检查是否应该处理事件（在事件处理函数中调用）
         */
        shouldProcess() {
            return !this.enabled;
        }
    };
    
    console.log('✅ SafeMode模块加载完成', { module: 'safe_mode' });
})();


        /* END: safe_mode.js */
    </script>

    <!-- ========================= -->
    <!-- Recovery Mode -->
    <!-- ========================= -->
    <script>
        /* BEGIN: recovery_mode.js */
/**
 * Recovery Mode（恢复模式）系统（规范要求）
 * 提供系统恢复和重置功能
 */

(function() {
    'use strict';

    window.RecoveryMode = {
        /**
         * 重置所有状态
         */
        resetAll() {
            console.log('🔄 [RecoveryMode] 开始重置所有状态...', { module: 'recovery_mode' });
            
            // 1. 清理所有定时器
            if (window.__intervals) {
                let clearedCount = 0;
                for (const key in window.__intervals) {
                    if (window.__intervals.hasOwnProperty(key)) {
                        clearInterval(window.__intervals[key]);
                        clearedCount++;
                    }
                }
                window.__intervals = {};
                console.log(`  ✅ 已清理 ${clearedCount} 个定时器`, { module: 'recovery_mode' });
            }
            
            // 2. 清空TTS队列
            if (window.priorityTTSQueue) {
                window.priorityTTSQueue.queue = [];
                window.priorityTTSQueue.currentAudio = null;
                window.priorityTTSQueue.currentPriority = 999;
                console.log('  ✅ 已清空TTS队列', { module: 'recovery_mode' });
            }
            
            if (window.ttsQueue && Array.isArray(window.ttsQueue)) {
                window.ttsQueue.length = 0;
                console.log('  ✅ 已清空旧TTS队列', { module: 'recovery_mode' });
            }
            
            // 3. 清空任务链队列
            if (window.taskChain) {
                window.taskChain.clear();
                console.log('  ✅ 已清空任务链队列', { module: 'recovery_mode' });
            }
            
            // 4. 清空视觉/导航相关的临时状态
            if (window.lastSpokenGuidance) {
                window.lastSpokenGuidance = {};
            }
            
            if (window.cameraMotionState) {
                window.cameraMotionState.lastFrame = null;
                window.cameraMotionState.motionDetected = false;
                window.cameraMotionState.lastMotionTime = 0;
            }
            
            // 5. 停止所有正在播放的声音
            if (window.priorityTTSQueue && window.priorityTTSQueue.currentAudio) {
                try {
                    window.priorityTTSQueue.currentAudio.pause();
                    window.priorityTTSQueue.currentAudio.currentTime = 0;
                    window.priorityTTSQueue.currentAudio = null;
                } catch (e) {
                    console.warn('  ⚠️ 停止音频失败:', e);
                }
            }
            
            // 6. 重置导航状态（如果存在）
            if (window.getNavStateManager) {
                try {
                    const navManager = window.getNavStateManager();
                    if (navManager && navManager.cancel) {
                        navManager.cancel('系统重置');
                    }
                } catch (e) {
                    console.warn('  ⚠️ 重置导航状态失败:', e);
                }
            }
            
            // 7. 重置导航FSM（如果存在）
            if (window.NavigationFSM && window.NavigationFSM.reset) {
                window.NavigationFSM.reset();
                console.log('  ✅ 已重置导航状态机', { module: 'recovery_mode' });
            }
            
            // 8. 清空路点（如果存在）
            if (window.WaypointManager && window.WaypointManager.clearWaypoints) {
                window.WaypointManager.clearWaypoints();
                console.log('  ✅ 已清空路点', { module: 'recovery_mode' });
            }
            
            console.log('✅ [RecoveryMode] 重置完成', { module: 'recovery_mode' });
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('system_reset', 'medium', {});
            }
        },
        
        /**
         * 重启核心模块
         */
        restartCore() {
            console.log('🔄 [RecoveryMode] 开始重启核心模块...', { module: 'recovery_mode' });
            
            // 1. 先重置所有状态
            this.resetAll();
            
            // 2. 重新初始化（按顺序）
            try {
                // 2.1 重新初始化任务链（如果存在）
                if (window.taskChain) {
                    // 任务链会自动初始化，这里只需要确保运行标志正确
                    window.taskChain.running = false;
                    console.log('  ✅ 任务链已准备就绪', { module: 'recovery_mode' });
                }
                
                // 2.2 重新初始化视觉模块（如果有初始化函数）
                if (typeof window.initProductMode === 'function') {
                    // 不直接调用，避免重复初始化
                    console.log('  ℹ️ 视觉模块初始化函数存在，但跳过自动调用', { module: 'recovery_mode' });
                }
                
                // 2.3 恢复UI按钮状态
                const startBtn = document.getElementById('startProductModeBtn');
                const stopBtn = document.getElementById('stopProductModeBtn');
                if (startBtn) {
                    startBtn.disabled = false;
                }
                if (stopBtn) {
                    stopBtn.disabled = true;
                }
                
                // 2.4 重置产品模式状态
                if (window.productModeActive !== undefined) {
                    window.productModeActive = false;
                }
                
                console.log('✅ [RecoveryMode] 核心模块重启完成', { module: 'recovery_mode' });
                
                // 3. 播报恢复消息
                if (window.speakText) {
                    setTimeout(() => {
                        window.speakText('系统已恢复，可以重新开始使用', 'cheerful');
                    }, 500);
                }
                
                // 触发情绪事件
                if (window.emotion_event) {
                    window.emotion_event('system_recovered', 'medium', {});
                }
                
            } catch (error) {
                console.error('❌ [RecoveryMode] 重启失败:', error, { module: 'recovery_mode' });
                
                // 即使失败也播报消息
                if (window.speakText) {
                    window.speakText('系统恢复过程中遇到问题，请手动重启', 'urgent');
                }
            }
        },
        
        /**
         * 软重启（只重置关键状态，不重启整个系统）
         */
        softReset() {
            console.log('🔄 [RecoveryMode] 执行软重置...', { module: 'recovery_mode' });
            
            // 只清理队列和定时器，不重启模块
            if (window.__intervals) {
                for (const key in window.__intervals) {
                    if (window.__intervals.hasOwnProperty(key)) {
                        clearInterval(window.__intervals[key]);
                    }
                }
                window.__intervals = {};
            }
            
            if (window.taskChain) {
                window.taskChain.clear();
            }
            
            if (window.priorityTTSQueue) {
                window.priorityTTSQueue.queue = [];
            }
            
            console.log('✅ [RecoveryMode] 软重置完成', { module: 'recovery_mode' });
        }
    };
    
    console.log('✅ RecoveryMode模块加载完成', { module: 'recovery_mode' });
})();


        /* END: recovery_mode.js */
    </script>

    <!-- ========================= -->
    <!-- Navigation Fsm -->
    <!-- ========================= -->
    <script>
        /* BEGIN: navigation_fsm.js */
/**
 * Navigation FSM（导航状态机）（规范要求）
 * 标准化导航状态流转：开始 → 运行 → 暂停 → 恢复 → 完成
 */

(function() {
    'use strict';

    /**
     * 导航状态枚举
     */
    const NavState = {
        IDLE: "IDLE",
        STARTING: "STARTING",
        ACTIVE: "ACTIVE",
        PAUSED: "PAUSED",
        RECOVERING: "RECOVERING",
        FINISHED: "FINISHED"
    };

    window.NavigationFSM = {
      state: NavState.IDLE,
      initialized: true,  // ✅ 标记为已初始化
        startTime: null,
        pauseTime: null,
        history: [],
        maxHistory: 50,
        
        /**
         * 开始导航
         */
        start(destination = null) {
            if (this.state === NavState.ACTIVE) {
                console.warn('⚠️ [NavigationFSM] 导航已在进行中', { module: 'navigation_fsm' });
                return false;
            }
            
            const oldState = this.state;
            this.state = NavState.STARTING;
            this.startTime = Date.now();
            
            console.log(`🔄 [NavigationFSM] 状态转换: ${oldState} → ${NavState.STARTING}`, { module: 'navigation_fsm' });
            
            // 记录历史
            this._recordTransition(oldState, NavState.STARTING, { destination });
            
            // 短暂延迟后进入ACTIVE状态（模拟启动过程）
            setTimeout(() => {
                if (this.state === NavState.STARTING) {
                    this.state = NavState.ACTIVE;
                    console.log(`✅ [NavigationFSM] 状态转换: ${NavState.STARTING} → ${NavState.ACTIVE}`, { module: 'navigation_fsm' });
                    this._recordTransition(NavState.STARTING, NavState.ACTIVE, { destination });
                    
                    // 触发情绪事件
                    if (window.emotion_event) {
                        window.emotion_event('navigation_started', 'medium', { destination });
                    }
                }
            }, 100);
            
            return true;
        },
        
        /**
         * 暂停导航
         */
        pause(reason = "用户暂停") {
            if (this.state !== NavState.ACTIVE) {
                console.warn(`⚠️ [NavigationFSM] 无法暂停，当前状态: ${this.state}`, { module: 'navigation_fsm' });
                return false;
            }
            
            const oldState = this.state;
            this.state = NavState.PAUSED;
            this.pauseTime = Date.now();
            
            console.log(`⏸️ [NavigationFSM] 状态转换: ${oldState} → ${NavState.PAUSED} (原因: ${reason})`, { module: 'navigation_fsm' });
            this._recordTransition(oldState, NavState.PAUSED, { reason });
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('navigation_paused', 'medium', { reason });
            }
            
            return true;
        },
        
        /**
         * 恢复导航
         */
        resume() {
            if (this.state !== NavState.PAUSED) {
                console.warn(`⚠️ [NavigationFSM] 无法恢复，当前状态: ${this.state}`, { module: 'navigation_fsm' });
                return false;
            }
            
            const oldState = this.state;
            this.state = NavState.RECOVERING;
            
            console.log(`🔄 [NavigationFSM] 状态转换: ${oldState} → ${NavState.RECOVERING}`, { module: 'navigation_fsm' });
            this._recordTransition(oldState, NavState.RECOVERING, {});
            
            // 短暂延迟后进入ACTIVE状态
            setTimeout(() => {
                if (this.state === NavState.RECOVERING) {
                    this.state = NavState.ACTIVE;
                    const pauseDuration = this.pauseTime ? Date.now() - this.pauseTime : 0;
                    this.pauseTime = null;
                    
                    console.log(`✅ [NavigationFSM] 状态转换: ${NavState.RECOVERING} → ${NavState.ACTIVE}`, { module: 'navigation_fsm' });
                    this._recordTransition(NavState.RECOVERING, NavState.ACTIVE, { pauseDuration });
                    
                    // 触发情绪事件
                    if (window.emotion_event) {
                        window.emotion_event('navigation_resumed', 'medium', { pauseDuration });
                    }
                }
            }, 100);
            
            return true;
        },
        
        /**
         * 完成导航
         */
        finish(success = true) {
            if (this.state !== NavState.ACTIVE && this.state !== NavState.PAUSED) {
                console.warn(`⚠️ [NavigationFSM] 无法完成，当前状态: ${this.state}`, { module: 'navigation_fsm' });
                return false;
            }
            
            const oldState = this.state;
            this.state = NavState.FINISHED;
            const duration = this.startTime ? Date.now() - this.startTime : 0;
            
            console.log(`🏁 [NavigationFSM] 状态转换: ${oldState} → ${NavState.FINISHED} (成功: ${success}, 耗时: ${duration}ms)`, { module: 'navigation_fsm' });
            this._recordTransition(oldState, NavState.FINISHED, { success, duration });
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('navigation_completed', 'medium', { success, duration });
            }
            
            return true;
        },
        
        /**
         * 重置状态机
         */
        reset() {
            const oldState = this.state;
            this.state = NavState.IDLE;
            this.startTime = null;
            this.pauseTime = null;
            
            console.log(`🔄 [NavigationFSM] 状态重置: ${oldState} → ${NavState.IDLE}`, { module: 'navigation_fsm' });
            this._recordTransition(oldState, NavState.IDLE, { reason: 'reset' });
        },
        
        /**
         * 处理导航事件
         */
        handleEvent(navData) {
            if (!navData) {
                return;
            }
            
            // 根据事件数据更新状态（如果需要）
            const { action, direction, distance } = navData;
            
            // 如果导航完成
            if (action === 'stop' || action === 'complete') {
                if (this.state === NavState.ACTIVE) {
                    this.finish(true);
                }
            }
            
            // 记录事件（用于状态机日志）
            this._recordEvent(navData);
        },
        
        /**
         * 记录状态转换
         */
        _recordTransition(from, to, meta) {
            this.history.push({
                type: 'transition',
                from,
                to,
                timestamp: Date.now(),
                meta
            });
            
            if (this.history.length > this.maxHistory) {
                this.history.shift();
            }
        },
        
        /**
         * 记录事件
         */
        _recordEvent(eventData) {
            this.history.push({
                type: 'event',
                state: this.state,
                data: eventData,
                timestamp: Date.now()
            });
            
            if (this.history.length > this.maxHistory) {
                this.history.shift();
            }
        },
        
        /**
         * 获取当前状态信息
         */
        getState() {
            return {
                state: this.state,
                startTime: this.startTime,
                pauseTime: this.pauseTime,
                duration: this.startTime ? Date.now() - this.startTime : 0,
                pauseDuration: this.pauseTime ? Date.now() - this.pauseTime : 0
            };
        },
        
        /**
         * 获取历史记录
         */
        getHistory(limit = 10) {
            return this.history.slice(-limit);
        }
    };
    
    console.log('✅ NavigationFSM模块加载完成', { module: 'navigation_fsm' });
})();


        /* END: navigation_fsm.js */
    </script>
    <script>
        /* ===== BEGIN: navigation_task_executors.js ===== */
        // frontend/navigation_task_executors.js
        // 导航任务执行器：将导航 Step 转换为语音/UI/日志
        (function () {
          'use strict';
          if (window.NavigationTaskExecutors) return;
          function log(event, payload) {
            if (window.__lunaLog) {
              window.__lunaLog(event, payload);
            } else if (window.logInfo) {
              window.logInfo(`[NavExecutors] ${event}`, payload || {});
            }
          }
          function speakText(text, style = 'calm', priority = false) {
            // ✅ 修复：移除 priority 参数的使用，添加容错处理
            if (window.speakText) {
              window.speakText(text, style);
            } else if (window.enqueueTTS) {
              window.enqueueTTS(text, { style });
            }
          }
          window.NavigationTaskExecutors = {
            "NAV_START": async (step) => {
              const { route, eta, distance } = step.payload || {};
              const etaText = eta ? `预计需要 ${eta} 分钟` : '';
              const distText = distance ? `，距离 ${distance} 米` : '';
              const message = `路线规划完成${distText}${etaText}。`;
              log('nav_start', { route, eta, distance });
              speakText(message, 'cheerful');
              if (window.NavigationFSM && typeof window.NavigationFSM.start === 'function') {
                window.NavigationFSM.start({ route, destination: route?.goalId || route?.to });
              }
            },
            "NAV_TURN": async (step) => {
              const { direction, distance } = step.payload || {};
              let message = '';
              if (direction === 'left') {
                message = distance ? `前方 ${distance} 米左转` : '请左转';
              } else if (direction === 'right') {
                message = distance ? `前方 ${distance} 米右转` : '请右转';
              } else if (direction === 'u-turn' || direction === 'uturn') {
                message = distance ? `前方 ${distance} 米掉头` : '请掉头';
              } else {
                message = '请按提示行进';
              }
              log('nav_turn', { direction, distance });
              speakText(message, 'cheerful');
            },
            "NAV_STRAIGHT": async (step) => {
              const { distance } = step.payload || {};
              const message = distance ? `继续直行 ${distance} 米` : '请继续直行';
              log('nav_straight', { distance });
              speakText(message, 'calm');
            },
            "NAV_POI": async (step) => {
              const { name, type } = step.payload || {};
              const message = name ? `前方是 ${name}` : (type ? `前方是 ${type}` : '前方是关键节点');
              log('nav_poi', { name, type });
              speakText(message, 'cheerful');
            },
            "NAV_END": async (step) => {
              const { destination } = step.payload || {};
              const message = destination ? `已到达 ${destination}` : '已到达目的地';
              log('nav_end', { destination });
              speakText(message, 'cheerful');
              if (window.NavigationFSM && typeof window.NavigationFSM.finish === 'function') {
                window.NavigationFSM.finish({ destination });
              }
            },
            "NAV_ERROR": async (step) => {
              const { reason, code } = step.payload || {};
              const message = reason ? `导航出错：${reason}` : '导航出现错误，请重新规划路线';
              log('nav_error', { reason, code });
              speakText(message, 'urgent');
              if (window.NavigationFSM && typeof window.NavigationFSM.reset === 'function') {
                window.NavigationFSM.reset({ reason: reason || 'error' });
              }
            }
          };
          console.log('✅ NavigationTaskExecutors 初始化完成', { module: 'navigation_executors' });
        })();
        /* ===== END: navigation_task_executors.js ===== */
    </script>
    <script>
        /* ===== BEGIN: navigation_logger.js ===== */
        // frontend/navigation_logger.js
        // Unified Navigation Logger — v1.0
        // 统一记录导航视觉 → 推理 → FSM → taskChain → 执行器 → 播报 的全链路日志
        (function () {
          'use strict';
          if (window.NavLog) return;
          class NavLogger {
            constructor() {
              this.logs = [];
              this.enabled = true;
              this.autoUpload = true;
              this.uploadURL = "/log_nav_event";
            }
            _log(level, source, message, extra = null) {
              if (!this.enabled) return;
              const entry = {
                time: new Date().toISOString(),
                level,
                source,
                message,
                extra
              };
              this.logs.push(entry);
              const logMethod = level === 'ERROR' ? console.error : (level === 'WARN' ? console.warn : console.log);
              logMethod(`[${level}] [${source}] ${message}`, extra || "");
              if (this.logs.length > 1000) {
                this.logs.shift();
              }
              if (this.autoUpload) {
                this._upload(entry);
              }
            }
            info(source, msg, extra = null) {
              this._log("INFO", source, msg, extra);
            }
            warn(source, msg, extra = null) {
              this._log("WARN", source, msg, extra);
            }
            error(source, msg, extra = null) {
              this._log("ERROR", source, msg, extra);
            }
            _upload(entry) {
              try {
                fetch(this.uploadURL, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(entry)
                }).catch(err => {
                  console.warn("[NavLog] 后台上传失败", err);
                });
              } catch (err) {
                console.warn("[NavLog] 后台上传异常", err);
              }
            }
            clear() {
              this.logs = [];
            }
            download() {
              const blob = new Blob(
                [JSON.stringify(this.logs, null, 2)],
                { type: "application/json" }
              );
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = `navigation_logs_${Date.now()}.json`;
              a.click();
              URL.revokeObjectURL(url);
            }
            getRecent(count = 50) {
              return this.logs.slice(-count);
            }
            getBySource(source) {
              return this.logs.filter(log => log.source === source);
            }
          }
          window.NavLog = new NavLogger();
          console.log("[NavLog] 统一导航日志系统已加载");
        })();
        /* ===== END: navigation_logger.js ===== */
    </script>

    <!-- ========================= -->
    <!-- MiniMap - Visual × Node × Navigation -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: minimap.js ===== */
// =====================================================
// MiniMap — v1.0
// 视觉 × 节点 × 导航 的小地图联动（简化版）
// =====================================================

(function () {
    "use strict";

    if (window.MiniMap) return;

    const NavLog = window.NavLog || {
        info: () => {},
        warn: () => {},
        error: () => {}
    };

    class MiniMap {
        constructor() {
            this.canvas = null;
            this.ctx = null;
            this.width = 220;
            this.height = 220;

            // 状态：不是真实坐标，先用相对坐标表达"周围东西"
            this.state = {
                // 导航路线（只存长度，用 stepIndex 表示进度）
                routeLength: 0,
                currentStepIndex: 0,

                // 危险点（相对坐标）
                hazards: [],   // {x, y, ts}

                // 节点（服务台 / 电梯 / 收银台等）
                nodes: []      // {x, y, type, label}
            };

            this._initCanvas();
            this._startRenderLoop();
        }

        _initCanvas() {
            let container = document.getElementById("luna-minimap-container");
            if (!container) {
                container = document.createElement("div");
                container.id = "luna-minimap-container";
                Object.assign(container.style, {
                    position: "fixed",
                    right: "12px",
                    bottom: "12px",
                    width: this.width + "px",
                    height: this.height + "px",
                    background: "rgba(0,0,0,0.45)",
                    borderRadius: "10px",
                    border: "1px solid rgba(255,255,255,0.2)",
                    zIndex: 9999,
                    overflow: "hidden",
                    backdropFilter: "blur(4px)",
                    color: "#fff",
                    fontSize: "11px",
                    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont"
                });
                document.body.appendChild(container);
            }

            const title = document.createElement("div");
            title.innerText = "Luna MiniMap";
            Object.assign(title.style, {
                padding: "4px 8px",
                borderBottom: "1px solid rgba(255,255,255,0.15)",
                fontSize: "11px",
                opacity: 0.8
            });
            container.appendChild(title);

            const canvas = document.createElement("canvas");
            canvas.width = this.width;
            canvas.height = this.height - 18;
            canvas.style.display = "block";
            container.appendChild(canvas);

            this.canvas = canvas;
            this.ctx = canvas.getContext("2d");

            NavLog.info("MiniMap", "初始化完成", {});
        }

        _startRenderLoop() {
            const draw = () => {
                this._render();
                requestAnimationFrame(draw);
            };
            requestAnimationFrame(draw);
        }

        // ===========================
        // 公共接口：由其他模块调用
        // ===========================

        /** 导航开始时设置路线长度（用 step 数表示） */
        setRouteLength(len) {
            this.state.routeLength = len || 0;
            this.state.currentStepIndex = 0;
        }

        /** 导航步骤推进时更新"当前位置" */
        setStepIndex(idx) {
            this.state.currentStepIndex = idx;
        }

        /** 视觉检测到危险时调用 */
        addHazard(relativeDirection) {
            // relativeDirection: "front" | "left" | "right" | "back"
            const base = { x: 0, y: 0 };

            switch (relativeDirection) {
                case "front":
                    base.y = -30;
                    break;
                case "back":
                    base.y = 30;
                    break;
                case "left":
                    base.x = -30;
                    break;
                case "right":
                    base.x = 30;
                    break;
                default:
                    base.y = -30;
            }

            this.state.hazards.push({
                x: base.x + (Math.random() * 10 - 5),
                y: base.y + (Math.random() * 10 - 5),
                ts: Date.now()
            });

            // 只保留最近的 N 个
            if (this.state.hazards.length > 30) {
                this.state.hazards.shift();
            }

            NavLog.info("MiniMap", "记录危险点", { dir: relativeDirection });
        }

        /** NodeEngine 识别到节点时调用 */
        addNode(nodeSummary) {
            // nodeSummary: {role, type, label}
            this.state.nodes.push({
                x: (Math.random() * 80 - 40),
                y: (Math.random() * 80 - 40),
                type: nodeSummary.type || "facility",
                label: nodeSummary.label || nodeSummary.role || "节点"
            });

            if (this.state.nodes.length > 40) {
                this.state.nodes.shift();
            }

            // ✅ E2: 保存到 NodeMemoryZone
            if (window.NodeMemoryZone) {
                window.NodeMemoryZone.addNode({
                    role: nodeSummary.role,
                    type: nodeSummary.type,
                    label: nodeSummary.label
                });
            }

            NavLog.info("MiniMap", "记录节点", nodeSummary);
        }

        // ===========================
        // 渲染逻辑
        // ===========================
        _render() {
            if (!this.ctx) return;

            const ctx = this.ctx;
            const w = this.canvas.width;
            const h = this.canvas.height;

            // 背景
            ctx.clearRect(0, 0, w, h);
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            ctx.fillRect(0, 0, w, h);

            // 网格
            ctx.strokeStyle = "rgba(255,255,255,0.06)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            for (let x = 0; x <= w; x += 20) {
                ctx.moveTo(x, 0);
                ctx.lineTo(x, h);
            }
            for (let y = 0; y <= h; y += 20) {
                ctx.moveTo(0, y);
                ctx.lineTo(w, y);
            }
            ctx.stroke();

            // 中心点（自己）
            const cx = w / 2;
            const cy = h / 2;
            ctx.fillStyle = "#00ffcc";
            ctx.beginPath();
            ctx.arc(cx, cy, 5, 0, Math.PI * 2);
            ctx.fill();

            // 当前行进方向箭头（简单用 stepIndex / routeLength 表示）
            if (this.state.routeLength > 0) {
                const progress = this.state.currentStepIndex / this.state.routeLength;
                const arrowLen = 40 + progress * 30;
                ctx.strokeStyle = "#00ffcc";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(cx, cy - arrowLen);
                ctx.stroke();
            }

            // 危险点（红色）
            const now = Date.now();
            ctx.fillStyle = "#ff5555";
            this.state.hazards = this.state.hazards.filter(hz => now - hz.ts < 10000);
            for (const hz of this.state.hazards) {
                ctx.beginPath();
                ctx.arc(cx + hz.x, cy + hz.y, 4, 0, Math.PI * 2);
                ctx.fill();
            }

            // ✅ E2: 从 NodeMemoryZone 同步节点（合并到当前显示列表）
            const displayNodes = [...this.state.nodes];
            if (window.NodeMemoryZone) {
                const memNodes = window.NodeMemoryZone.getZoneNodes();
                memNodes.forEach(n => {
                    // 检查是否已存在（避免重复）
                    const exists = displayNodes.some(dn => 
                        (dn.label === n.label) || (dn.type === n.type && dn.label === n.label)
                    );
                    if (!exists) {
                        displayNodes.push({
                            x: (Math.random() * 80 - 40),
                            y: (Math.random() * 80 - 40),
                            type: n.type,
                            label: n.label
                        });
                    }
                });
            }

            // 节点（黄色）
            ctx.fillStyle = "#ffdd66";
            for (const n of displayNodes) {
                ctx.beginPath();
                ctx.arc(cx + n.x, cy + n.y, 3, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }

    window.MiniMap = new MiniMap();
})();
        /* ===== END: minimap.js ===== */
    </script>

    <!-- ========================= -->
    <!-- NodeMemoryZone - E1: 区域节点记忆系统 -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: node_memory_zone.js ===== */
// =====================================================
// NodeMemoryZone — v1.0
// 场景节点的本地记忆系统（按区域存储）
// =====================================================

(function () {
    "use strict";

    if (window.NodeMemoryZone) return;

    class NodeMemoryZone {
        constructor() {
            this.key = "luna_node_memory_zone_v1";
            this.data = this._load() || {};

            // 当前区域：可以由外部设置
            this.currentZone = "DEFAULT";
        }

        // ===========================
        // 存储
        // ===========================
        _load() {
            try {
                return JSON.parse(localStorage.getItem(this.key)) || {};
            } catch (err) {
                console.warn("[NodeMemoryZone] load failed", err);
                return {};
            }
        }

        _save() {
            localStorage.setItem(this.key, JSON.stringify(this.data));
        }

        // ===========================
        // 区域管理
        // ===========================
        setZone(zoneName) {
            this.currentZone = zoneName || "DEFAULT";
            if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
            }
            this._save();
        }

        getZone() {
            return this.currentZone;
        }

        getZoneNodes() {
            return this.data[this.currentZone] || [];
        }

        // ===========================
        // 节点合并逻辑
        // ===========================
        _isSimilarNode(a, b) {
            // 简化合并条件：标签相同 或 角色相同
            if (a.label && b.label && a.label === b.label) return true;
            if (a.role && b.role && a.role === b.role) return true;
            return false;
        }

        // ===========================
        // 添加节点（自动合并）
        // ===========================
        addNode(node) {
            if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
            }

            const zoneList = this.data[this.currentZone];

            for (let i = 0; i < zoneList.length; i++) {
                if (this._isSimilarNode(zoneList[i], node)) {
                    // 合并更新时间
                    zoneList[i].lastSeen = Date.now();
                    this._save();
                    return;
                }
            }

            // 新节点
            this.data[this.currentZone].push({
                role: node.role,
                type: node.type,
                label: node.label,
                lastSeen: Date.now()
            });

            this._save();
        }
    }

    window.NodeMemoryZone = new NodeMemoryZone();
    console.log("[NodeMemoryZone] 已加载");
})();
        /* ===== END: node_memory_zone.js ===== */
    </script>

    <!-- ========================= -->
    <!-- ZoneManager - E3: 区域切换管理器 -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: zone_manager.js ===== */
// =====================================================
// ZoneManager — v1.0
// 区域切换控制器：A区 / B区 / 医院区 / 地铁区 等
// =====================================================

(function () {

    if (window.ZoneManager) return;

    class ZoneManager {
        constructor() {
            this.current = "DEFAULT";
        }

        setZone(name) {
            this.current = name;
            console.log("[ZoneManager] 切换区域:", name);

            if (window.NodeMemoryZone) {
                window.NodeMemoryZone.setZone(name);
            }

            if (window.MiniMap) {
                window.MiniMap.state.nodes = [];
                window.MiniMap.state.hazards = [];
            }
            
            // ✅ E4: 切换区域后重置自动检测器
            if (window.ZoneAutoDetector) {
                window.ZoneAutoDetector.reset();
            }
        }

        getZone() {
            return this.current;
        }
    }

    window.ZoneManager = new ZoneManager();
    console.log("[ZoneManager] 已加载");

})();
        /* ===== END: zone_manager.js ===== */
    </script>

    <!-- ========================= -->
    <!-- ZoneAutoDetector - E4: 自动区域识别 -->
    <!-- ========================= -->
    <script>
        /* ===== BEGIN: zone_auto_detector.js ===== */
// =====================================================
// ZoneAutoDetector — v1.0
// 自动区域识别：环境节点向量 × 视觉模式 × 用户行为
// =====================================================

(function () {

    if (window.ZoneAutoDetector) return;

    class ZoneAutoDetector {

        constructor() {
            this.currentFeatures = {};   // 当前识别到的节点统计
            this.visualHints = {};       // 视觉结构提示（走廊/店铺/走廊）
            this.behaviorProfile = {};   // 用户行为模式
            this.lastUpdate = 0;
            this.lastDetectedZone = null;
            this.detectionCooldown = 5000; // 5秒冷却，避免频繁切换
            this.lastDetectionTime = 0;
        }

        // ======================================
        // 输入：节点（来自 NodeEngine）
        // ======================================
        feedNode(node) {
            const key = node.label || node.role || "unknown";
            if (!this.currentFeatures[key]) {
                this.currentFeatures[key] = 0;
            }
            this.currentFeatures[key]++;

            this.lastUpdate = Date.now();
        }

        // ======================================
        // 输入：视觉结构（来自 YOLO 分析或 VisionEnhancer）
        // ======================================
        feedVisualHint(hint) {
            // hint = "corridor" | "mall" | "clinic" | "office" | ...
            this.visualHints[hint] = (this.visualHints[hint] || 0) + 1;
            this.lastUpdate = Date.now();
        }

        // ======================================
        // 输入：用户行为（未来可接 emotion hook）
        // ======================================
        feedBehavior(eventName) {
            this.behaviorProfile[eventName] = (this.behaviorProfile[eventName] || 0) + 1;
            this.lastUpdate = Date.now();
        }

        // ======================================
        // 与 NodeMemoryZone 的区域特征比较
        // ======================================
        computeSimilarity(zoneName) {
            if (!window.NodeMemoryZone) return 0;
            
            const zoneNodes = window.NodeMemoryZone.data[zoneName] || [];
            if (!zoneNodes.length) return 0;

            let score = 0;
            let matchedCount = 0;

            for (const zn of zoneNodes) {
                const key = zn.label || zn.role;
                if (!key) continue;

                if (this.currentFeatures[key]) {
                    score += 1;
                    matchedCount++;
                }
            }

            // 简单归一化：匹配节点数 / (区域节点总数 + 平滑因子)
            const similarity = score / (zoneNodes.length + 3);
            
            // 如果有视觉提示匹配，增加分数
            if (this.visualHints[zoneName] || this.visualHints[zoneName.toLowerCase()]) {
                return Math.min(1.0, similarity + 0.2);
            }

            return similarity;
        }

        // ======================================
        // 最终判断：是否切换区域
        // ======================================
        detectZone() {
            if (!window.NodeMemoryZone) return null;

            // 冷却期检查
            const now = Date.now();
            if (now - this.lastDetectionTime < this.detectionCooldown) {
                return null;
            }

            let bestZone = null;
            let bestScore = 0;

            // 遍历所有已存储的区域
            for (const zoneName of Object.keys(window.NodeMemoryZone.data)) {
                const sim = this.computeSimilarity(zoneName);
                if (sim > bestScore) {
                    bestScore = sim;
                    bestZone = zoneName;
                }
            }

            // 阈值：> 0.4 就切换
            if (bestScore > 0.4 && bestZone !== this.lastDetectedZone) {
                this.lastDetectionTime = now;
                this.lastDetectedZone = bestZone;
                return { zone: bestZone, score: bestScore };
            }

            return null;
        }

        // ======================================
        // 重置当前特征（切换区域后调用）
        // ======================================
        reset() {
            this.currentFeatures = {};
            this.visualHints = {};
            this.lastUpdate = 0;
        }

    }

    window.ZoneAutoDetector = new ZoneAutoDetector();
    console.log("[ZoneAutoDetector] 已加载");

    // 自动检测循环（每2秒执行一次）
    setInterval(() => {
        if (!window.ZoneAutoDetector || !window.ZoneManager) return;

        const res = window.ZoneAutoDetector.detectZone();
        if (res && res.zone) {
            const currentZone = window.ZoneManager.getZone();
            if (res.zone !== currentZone) {
                console.log("[AutoZone] 自动切换区域 →", res.zone, "相似度:", res.score.toFixed(2));
                window.ZoneManager.setZone(res.zone);
                // 切换后重置检测器特征
                window.ZoneAutoDetector.reset();
            }
        }
    }, 2000);

})();
        /* ===== END: zone_auto_detector.js ===== */
    </script>

    <!-- ========================= -->
    <!-- Waypoint System -->
    <!-- ========================= -->
    <script>
        /* BEGIN: waypoint_system.js */
/**
 * Waypoint System（路点系统）（规范要求）
 * 支持多路点导航能力（医院、地铁、商场等）
 */

(function() {
    'use strict';

    window.WaypointManager = {
        waypoints: [],
        currentIndex: 0,
        reachedWaypoints: [],
        
        /**
         * 添加路点
         */
        addWaypoint(wp) {
            if (!wp || !wp.id) {
                console.warn('⚠️ [WaypointManager] 无效的路点数据', { module: 'waypoint_system' });
                return false;
            }
            
            // 检查是否已存在
            const exists = this.waypoints.find(w => w.id === wp.id);
            if (exists) {
                console.warn(`⚠️ [WaypointManager] 路点已存在: ${wp.id}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 确保有必要的字段
            const waypoint = {
                id: wp.id,
                type: wp.type || 'custom',
                label: wp.label || wp.id,
                tts_message: wp.tts_message || `到达${wp.label || wp.id}`,
                metadata: wp.metadata || {},
                order: wp.order !== undefined ? wp.order : this.waypoints.length,
                ...wp
            };
            
            this.waypoints.push(waypoint);
            
            // 按order排序
            this.waypoints.sort((a, b) => a.order - b.order);
            
            console.log(`✅ [WaypointManager] 添加路点: ${waypoint.id} (${waypoint.label})`, { module: 'waypoint_system' });
            
            return true;
        },
        
        /**
         * 清空所有路点
         */
        clearWaypoints() {
            const count = this.waypoints.length;
            this.waypoints = [];
            this.currentIndex = 0;
            this.reachedWaypoints = [];
            
            console.log(`🗑️ [WaypointManager] 已清空 ${count} 个路点`, { module: 'waypoint_system' });
        },
        
        /**
         * 获取当前路点
         */
        getCurrent() {
            if (this.waypoints.length === 0) {
                return null;
            }
            
            if (this.currentIndex >= this.waypoints.length) {
                return null;  // 所有路点已完成
            }
            
            return this.waypoints[this.currentIndex];
        },
        
        /**
         * 标记当前路点已到达
         */
        markReached(waypointId = null) {
            const targetId = waypointId || (this.getCurrent()?.id);
            
            if (!targetId) {
                console.warn('⚠️ [WaypointManager] 无法标记到达：无目标路点', { module: 'waypoint_system' });
                return false;
            }
            
            const waypoint = this.waypoints.find(w => w.id === targetId);
            if (!waypoint) {
                console.warn(`⚠️ [WaypointManager] 路点不存在: ${targetId}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 检查是否已到达
            if (this.reachedWaypoints.includes(targetId)) {
                console.log(`ℹ️ [WaypointManager] 路点已标记为到达: ${targetId}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 标记为已到达
            this.reachedWaypoints.push(targetId);
            
            // 如果到达的是当前路点，移动到下一个
            if (this.getCurrent()?.id === targetId) {
                this.currentIndex++;
            }
            
            console.log(`✅ [WaypointManager] 路点已到达: ${waypoint.label} (${targetId})`, { module: 'waypoint_system' });
            
            // 播报TTS消息
            if (waypoint.tts_message && window.speakText) {
                window.speakText(waypoint.tts_message, 'cheerful');
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('waypoint_reached', 'medium', {
                    waypoint_id: targetId,
                    waypoint_label: waypoint.label,
                    progress: this.getProgress()
                });
            }
            
            return true;
        },
        
        /**
         * 检查导航进度
         */
        checkProgress(navData) {
            if (!navData || this.waypoints.length === 0) {
                return null;
            }
            
            const currentWaypoint = this.getCurrent();
            if (!currentWaypoint) {
                // 所有路点已完成
                return {
                    completed: true,
                    progress: 1.0,
                    message: "所有路点已完成"
                };
            }
            
            // 简单的到达判断逻辑（可根据实际需求扩展）
            const { action, direction, distance, detectedObjects, signboards } = navData;
            
            // 检查1：方向匹配
            if (currentWaypoint.metadata.expectedDirection) {
                if (direction !== currentWaypoint.metadata.expectedDirection) {
                    return null;  // 方向不匹配，未到达
                }
            }
            
            // 检查2：距离判断
            if (currentWaypoint.metadata.expectedDistance !== undefined) {
                const expectedDist = currentWaypoint.metadata.expectedDistance;
                const tolerance = currentWaypoint.metadata.distanceTolerance || 5;
                if (distance && Math.abs(distance - expectedDist) > tolerance) {
                    return null;  // 距离不匹配
                }
            }
            
            // 检查3：标识牌匹配
            if (currentWaypoint.metadata.expectedSign) {
                const expectedSign = currentWaypoint.metadata.expectedSign;
                if (signboards && Array.isArray(signboards)) {
                    const found = signboards.some(sb => 
                        sb.text && sb.text.includes(expectedSign)
                    );
                    if (!found) {
                        return null;  // 标识牌不匹配
                    }
                }
            }
            
            // 检查4：设施匹配
            if (currentWaypoint.metadata.expectedFacility) {
                const expectedFacility = currentWaypoint.metadata.expectedFacility;
                if (detectedObjects && Array.isArray(detectedObjects)) {
                    const found = detectedObjects.some(obj => 
                        obj.class && obj.class.includes(expectedFacility)
                    );
                    if (!found) {
                        return null;  // 设施不匹配
                    }
                }
            }
            
            // 如果所有条件都满足（或没有条件），标记为到达
            if (action === 'stop' || (distance !== undefined && distance < 3)) {
                this.markReached(currentWaypoint.id);
                return {
                    reached: true,
                    waypoint: currentWaypoint,
                    progress: this.getProgress()
                };
            }
            
            return {
                current: currentWaypoint,
                progress: this.getProgress(),
                remaining: this.waypoints.length - this.currentIndex
            };
        },
        
        /**
         * 获取进度
         */
        getProgress() {
            if (this.waypoints.length === 0) {
                return 0;
            }
            
            return {
                current: this.currentIndex + 1,
                total: this.waypoints.length,
                percentage: Math.round(((this.currentIndex + 1) / this.waypoints.length) * 100),
                reached: this.reachedWaypoints.length,
                remaining: this.waypoints.length - this.currentIndex
            };
        },
        
        /**
         * 获取所有路点
         */
        getAllWaypoints() {
            return this.waypoints.map((wp, index) => ({
                ...wp,
                index,
                reached: this.reachedWaypoints.includes(wp.id),
                isCurrent: index === this.currentIndex
            }));
        }
    };
    
    console.log('✅ WaypointManager模块加载完成', { module: 'waypoint_system' });
})();


        /* END: waypoint_system.js */
    </script>

    <!-- ========================= -->
    <!-- Auto Recovery -->
    <!-- ========================= -->
    <script>
        /* BEGIN: auto_recovery.js */
/**
 * Auto-Recovery（自动恢复）模块（规范要求）
 * 监控核心模块是否异常，并调用RecoveryMode自愈
 */

(function() {
    'use strict';

    window.AutoRecovery = {
        stats: {
            visionErrors: 0,
            navErrors: 0,
            ttsBlockedCount: 0,
            taskChainStallCount: 0,
            lastCheckTime: Date.now()
        },
        
        thresholds: {
            visionErrors: 3,      // 视觉错误超过3次触发恢复
            navErrors: 3,         // 导航错误超过3次触发恢复
            ttsBlocked: 5,        // TTS阻塞超过5次触发恢复
            taskChainStall: 10,   // 任务链停滞超过10次触发恢复
            checkInterval: 5000   // 每5秒检查一次
        },
        
        errorHistory: [],
        maxHistory: 20,
        
        /**
         * 记录错误
         */
        record(module, type, detail = {}) {
            const record = {
                module,
                type,
                detail,
                timestamp: Date.now()
            };
            
            this.errorHistory.push(record);
            if (this.errorHistory.length > this.maxHistory) {
                this.errorHistory.shift();
            }
            
            // 更新统计
            if (module === 'vision' && type === 'error') {
                this.stats.visionErrors++;
            } else if (module === 'navigation' && type === 'error') {
                this.stats.navErrors++;
            } else if (module === 'tts' && type === 'blocked') {
                this.stats.ttsBlockedCount++;
            } else if (module === 'taskChain' && type === 'stall') {
                this.stats.taskChainStallCount++;
            }
            
            console.log(`📊 [AutoRecovery] 记录错误: ${module}.${type}`, { module: 'auto_recovery', detail });
            
            // 如果超过阈值，立即检查
            if (this._shouldTriggerRecovery(module, type)) {
                console.warn(`⚠️ [AutoRecovery] ${module}错误超过阈值，触发检查`, { module: 'auto_recovery' });
                this.checkAndRecover();
            }
        },
        
        /**
         * 检查并恢复
         */
        checkAndRecover() {
            const now = Date.now();
            const timeSinceLastCheck = now - this.stats.lastCheckTime;
            this.stats.lastCheckTime = now;
            
            console.log('🔍 [AutoRecovery] 执行健康检查...', { module: 'auto_recovery' });
            
            let recoveryNeeded = false;
            const recoveryReasons = [];
            
            // 1. 检查视觉模块
            if (this.stats.visionErrors >= this.thresholds.visionErrors) {
                recoveryNeeded = true;
                recoveryReasons.push(`视觉错误过多 (${this.stats.visionErrors}次)`);
            }
            
            // 2. 检查导航模块
            if (this.stats.navErrors >= this.thresholds.navErrors) {
                recoveryNeeded = true;
                recoveryReasons.push(`导航错误过多 (${this.stats.navErrors}次)`);
            }
            
            // 3. 检查TTS队列
            if (this.stats.ttsBlockedCount >= this.thresholds.ttsBlocked) {
                recoveryNeeded = true;
                recoveryReasons.push(`TTS队列阻塞 (${this.stats.ttsBlockedCount}次)`);
            }
            
            // 4. 检查任务链
            if (this.stats.taskChainStallCount >= this.thresholds.taskChainStall) {
                recoveryNeeded = true;
                recoveryReasons.push(`任务链停滞 (${this.stats.taskChainStallCount}次)`);
            }
            
            // 5. 检查任务链是否真的停滞
            if (window.taskChain) {
                const stats = window.taskChain.getStats();
                const currentTask = stats.currentTask;
                
                // 如果当前任务运行时间过长（超过30秒）
                if (currentTask && currentTask.status === 'running') {
                    const taskAge = now - (currentTask.timestamp || 0);
                    if (taskAge > 30000) {
                        recoveryNeeded = true;
                        recoveryReasons.push(`任务链任务运行超时 (${Math.round(taskAge/1000)}秒)`);
                    }
                }
            }
            
            // 6. 检查TTS队列是否长时间未处理
            if (window.priorityTTSQueue) {
                const queueLength = window.priorityTTSQueue.queue ? window.priorityTTSQueue.queue.length : 0;
                if (queueLength > 10) {
                    recoveryNeeded = true;
                    recoveryReasons.push(`TTS队列积压过多 (${queueLength}条)`);
                }
            }
            
            if (recoveryNeeded) {
                console.warn(`⚠️ [AutoRecovery] 检测到异常，开始恢复...`, { 
                    module: 'auto_recovery',
                    reasons: recoveryReasons
                });
                
                // 记录日志
                if (window.lunaLog) {
                    window.lunaLog('warning', '自动恢复触发', {
                        reasons: recoveryReasons,
                        stats: { ...this.stats }
                    });
                }
                
                // ③【新增：后台日志上传】
                if (window.sendLog) {
                    window.sendLog({ type: 'auto_recovery_trigger', reason: recoveryReasons.join('; '), stats: { ...this.stats } });
                }
                
                // 触发情绪事件
                if (window.emotion_event) {
                    window.emotion_event('system_error', 'high', {
                        type: 'auto_recovery_triggered',
                        reasons: recoveryReasons,
                        stats: { ...this.stats }
                    });
                }
                
                // 执行恢复
                if (window.RecoveryMode) {
                    // 根据严重程度选择恢复方式
                    const isCritical = recoveryReasons.some(r => r.includes('超时') || r.includes('积压'));
                    
                    if (isCritical) {
                        console.log('  🔄 [AutoRecovery] 执行完整重启...', { module: 'auto_recovery' });
                        window.RecoveryMode.restartCore();
                    } else {
                        console.log('  🔄 [AutoRecovery] 执行软重置...', { module: 'auto_recovery' });
                        window.RecoveryMode.softReset();
                    }
                } else {
                    console.warn('  ⚠️ [AutoRecovery] RecoveryMode未加载，无法执行恢复', { module: 'auto_recovery' });
                }
                
                // 重置错误计数（避免重复触发）
                this.stats.visionErrors = 0;
                this.stats.navErrors = 0;
                this.stats.ttsBlockedCount = 0;
                this.stats.taskChainStallCount = 0;
                
                console.log('✅ [AutoRecovery] 恢复完成', { module: 'auto_recovery' });
            } else {
                console.log('✅ [AutoRecovery] 系统健康，无需恢复', { module: 'auto_recovery' });
            }
        },
        
        /**
         * 判断是否应该触发恢复
         */
        _shouldTriggerRecovery(module, type) {
            if (module === 'vision' && type === 'error') {
                return this.stats.visionErrors >= this.thresholds.visionErrors;
            }
            if (module === 'navigation' && type === 'error') {
                return this.stats.navErrors >= this.thresholds.navErrors;
            }
            if (module === 'tts' && type === 'blocked') {
                return this.stats.ttsBlockedCount >= this.thresholds.ttsBlocked;
            }
            if (module === 'taskChain' && type === 'stall') {
                return this.stats.taskChainStallCount >= this.thresholds.taskChainStall;
            }
            return false;
        },
        
        /**
         * 启动自动监控
         */
        startMonitoring() {
            if (this.monitoringInterval) {
                console.log('ℹ️ [AutoRecovery] 监控已在运行', { module: 'auto_recovery' });
                return;
            }
            
            console.log('✅ [AutoRecovery] 启动自动监控', { module: 'auto_recovery' });
            
            // 注册到全局定时器管理
            if (window.__intervals) {
                window.__intervals.autoRecovery = setInterval(() => {
                    this.checkAndRecover();
                }, this.thresholds.checkInterval);
            } else {
                // 降级：直接使用setInterval
                this.monitoringInterval = setInterval(() => {
                    this.checkAndRecover();
                }, this.thresholds.checkInterval);
            }
        },
        
        /**
         * 停止自动监控
         */
        stopMonitoring() {
            if (window.__intervals && window.__intervals.autoRecovery) {
                clearInterval(window.__intervals.autoRecovery);
                delete window.__intervals.autoRecovery;
            }
            
            if (this.monitoringInterval) {
                clearInterval(this.monitoringInterval);
                this.monitoringInterval = null;
            }
            
            console.log('⏸️ [AutoRecovery] 停止自动监控', { module: 'auto_recovery' });
        },
        
        /**
         * 获取统计信息
         */
        getStats() {
            return {
                ...this.stats,
                errorHistory: this.errorHistory.slice(-10),  // 最近10条错误
                thresholds: this.thresholds
            };
        },
        
        /**
         * 重置统计
         */
        resetStats() {
            this.stats = {
                visionErrors: 0,
                navErrors: 0,
                ttsBlockedCount: 0,
                taskChainStallCount: 0,
                lastCheckTime: Date.now()
            };
            this.errorHistory = [];
            console.log('🔄 [AutoRecovery] 统计已重置', { module: 'auto_recovery' });
        }
    };
    
    // 自动启动监控（延迟启动，确保其他模块已加载）
    setTimeout(() => {
        if (window.AutoRecovery && window.AutoRecovery.startMonitoring) {
            window.AutoRecovery.startMonitoring();
        }
    }, 2000);
    
    console.log('✅ AutoRecovery模块加载完成', { module: 'auto_recovery' });
})();


        /* END: auto_recovery.js */
    </script>

    <!-- ========================= -->
    <!-- Visual Hazard Filter -->
    <!-- ========================= -->
    <script>
        /* BEGIN: visual_filter.js */
        /**
         * ②【修复：视觉"误报危险"】- VisualHazardFilter
         * 通过多帧稳定判断减少误报
         */
        (function() {
            'use strict';
            
            window.VisualHazardFilter = {
                lastFrames: [],
                maxFrames: 5,
                threshold: 3,  // 至少3帧检测到危险才算稳定
                
                /**
                 * 推送新帧数据
                 */
                push(frame) {
                    this.lastFrames.push({
                        danger: frame.danger === true || frame.danger === 'true',
                        type: frame.type,
                        timestamp: Date.now()
                    });
                    
                    // 保持最近maxFrames帧
                    if (this.lastFrames.length > this.maxFrames) {
                        this.lastFrames.shift();
                    }
                },
                
                /**
                 * 检查危险是否稳定
                 */
                isDangerStable() {
                    if (this.lastFrames.length < this.threshold) {
                        return false;
                    }
                    
                    const dangerCount = this.lastFrames.filter(f => f.danger === true).length;
                    return dangerCount >= this.threshold;
                },
                
                /**
                 * 重置过滤器
                 */
                reset() {
                    this.lastFrames = [];
                },
                
                /**
                 * 获取当前状态
                 */
                getState() {
                    return {
                        frameCount: this.lastFrames.length,
                        dangerCount: this.lastFrames.filter(f => f.danger === true).length,
                        isStable: this.isDangerStable()
                    };
                }
            };
            
            console.log('✅ VisualHazardFilter模块加载完成', { module: 'visual_filter' });
        })();
        /* END: visual_filter.js */
    </script>

    <!-- ========================= -->
    <!-- Log Upload System -->
    <!-- ========================= -->
    <script>
        /* BEGIN: log_upload.js */
        /**
         * ③【新增：后台日志上传（手机端 → Python → 后台）】
         */
        (function() {
            'use strict';
            
            // 生成session_id（如果不存在）
            if (!window.sessionId) {
                window.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            }
            
            // 日志上传函数
            window.sendLog = function(data) {
                try {
                    const logData = {
                        ts: Date.now(),
                        session_id: window.sessionId,
                        trace_id: data.trace_id || `trace_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                        ...data
                    };
                    
                    // 发送到Python后端
                    fetch('/api/logs/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(logData)
                    }).catch(err => {
                        console.warn('[LogUpload] 上传失败:', err);
                    });
                } catch (err) {
                    console.warn('[LogUpload] 日志发送异常:', err);
                }
            };
            
            console.log('✅ LogUpload模块加载完成', { module: 'log_upload', sessionId: window.sessionId });
        })();
        /* END: log_upload.js */
    </script>

    <!-- ========================= -->
    <!-- Luna Logger (统一日志系统) -->
    <!-- ========================= -->
    <script>
        /* BEGIN: logger.js */
        // frontend/logger.js
        /**
         * 统一日志系统（浏览器 → 后端）
         * 支持 info / warn / error / debug 等级
         * 所有视觉 / 导航 / TTS / 状态机 / 异常都走这里
         */
        (function () {
          'use strict';
          
          if (window.LunaLogger) return;

          const DEFAULT_ENDPOINT = "/api/logs/upload";

          class LunaLogger {
            constructor() {
              this.sessionId = this._generateSessionId();
              this.endpoint = DEFAULT_ENDPOINT;
              this.enabled = true;
            }

            _generateSessionId() {
              if (window.crypto && window.crypto.randomUUID) {
                return window.crypto.randomUUID();
              }
              return 'sess-' + Date.now() + '-' + Math.random().toString(16).slice(2);
            }

            setEndpoint(url) {
              this.endpoint = url;
            }

            _basePayload(extra) {
              return Object.assign({
                ts: Date.now(),
                sessionId: this.sessionId,
                userAgent: navigator.userAgent || '',
              }, extra || {});
            }

            _toConsole(level, msg, payload) {
              const prefix = `[Luna/${level.toUpperCase()}]`;
              if (level === 'error') {
                console.error(prefix, msg, payload || '');
              } else if (level === 'warn') {
                console.warn(prefix, msg, payload || '');
              } else if (level === 'debug') {
                console.debug(prefix, msg, payload || '');
              } else {
                console.log(prefix, msg, payload || '');
              }
            }

            _toBackend(level, msg, payload) {
              if (!this.enabled || !this.endpoint || !window.fetch) return;
              const body = this._basePayload(Object.assign({
                level,
                message: msg,
                payload: payload || {}
              }));

              try {
                fetch(this.endpoint, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(body)
                }).catch(() => { /* 静默失败，不打断主流程 */ });
              } catch (e) {
                // ignore
              }
            }

            log(level, msg, payload) {
              this._toConsole(level, msg, payload);
              this._toBackend(level, msg, payload);
            }

            info(msg, payload) { this.log('info', msg, payload); }
            warn(msg, payload) { this.log('warn', msg, payload); }
            error(msg, payload) { this.log('error', msg, payload); }
            debug(msg, payload) { this.log('debug', msg, payload); }
          }

          window.LunaLogger = new LunaLogger();

          window.logInfo = (msg, payload) => window.LunaLogger.info(msg, payload);
          window.logWarn = (msg, payload) => window.LunaLogger.warn(msg, payload);
          window.logError = (msg, payload) => window.LunaLogger.error(msg, payload);
          window.logDebug = (msg, payload) => window.LunaLogger.debug(msg, payload);
          
          console.log('✅ LunaLogger模块加载完成', { module: 'logger' });
        })();
        /* END: logger.js */
    <!-- ===================== -->
    <!-- Luna E Series: Logging + Memory Audit -->
    <!-- ===================== -->
    <script>
    /* BEGIN: e_logging_memory.js */
// frontend/e_logging_memory.js
// E 系列：结构化日志 + 远程上传 + 记忆审计
// 说明：不会破坏现有 console.*，而是在此基础上增强。

(function () {
  'use strict';
  
  if (window.LunaLogger && window.RemoteLogger && window.MemoryAudit) {
    return;
  }

  // =========================
  // E1. LunaLogger 结构化日志
  // =========================
  if (!window.LunaLogger) {
    function LunaLoggerClass() {
      this.deviceId = window.__LUNA_DEVICE_ID__ || null;
      this.sessionId =
        window.__LUNA_SESSION_ID__ ||
        (Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8));
      this.buffer = [];
      this.subscribers = [];
      this.maxBuffer = 500;
    }

    LunaLoggerClass.prototype._emit = function (level, message, details) {
      const evt = {
        ts: new Date().toISOString(),
        level: level.toUpperCase(),
        message: message || '',
        details: details || {},
        deviceId: this.deviceId,
        sessionId: this.sessionId,
      };

      // console 输出
      try {
        const tag = `[Luna][${evt.level}]`;
        if (evt.level === 'ERROR') console.error(tag, evt.message, evt.details);
        else if (evt.level === 'WARN') console.warn(tag, evt.message, evt.details);
        else console.log(tag, evt.message, evt.details);
      } catch (e) {
        console.log('[Luna][LOG-FALLBACK]', evt);
      }

      // 放入缓冲
      this.buffer.push(evt);
      if (this.buffer.length > this.maxBuffer) {
        this.buffer.shift();
      }

      // 通知订阅者（例如 RemoteLogger / 本地调试 UI）
      for (const sub of this.subscribers) {
        try {
          sub(evt);
        } catch (e) {
          console.log('[Luna][Logger subscriber error]', e);
        }
      }

      return evt;
    };

    LunaLoggerClass.prototype.debug = function (msg, details) {
      return this._emit('DEBUG', msg, details);
    };

    LunaLoggerClass.prototype.info = function (msg, details) {
      return this._emit('INFO', msg, details);
    };

    LunaLoggerClass.prototype.warn = function (msg, details) {
      return this._emit('WARN', msg, details);
    };

    LunaLoggerClass.prototype.error = function (msg, details) {
      return this._emit('ERROR', msg, details);
    };

    LunaLoggerClass.prototype.subscribe = function (fn) {
      if (typeof fn === 'function') {
        this.subscribers.push(fn);
      }
    };

    LunaLoggerClass.prototype.drainBuffer = function () {
      const data = this.buffer.slice();
      this.buffer = [];
      return data;
    };

    window.LunaLogger = new LunaLoggerClass();

    // 全局便捷函数（兼容之前 logInfo/logWarn 等）
    window.logDebug = function (msg, details) {
      window.LunaLogger.debug(msg, details);
    };

    window.logInfo = function (msg, details) {
      window.LunaLogger.info(msg, details);
    };

    window.logWarn = function (msg, details) {
      window.LunaLogger.warn(msg, details);
    };

    window.logError = function (msg, details) {
      window.LunaLogger.error(msg, details);
    };
  }

  // =========================
  // E2. RemoteLogger 远程日志上传
  // =========================
  if (!window.RemoteLogger) {
    function RemoteLoggerClass() {
      this.endpoint = window.__LUNA_LOG_ENDPOINT__ || '/api/logs';
      this.queue = [];
      this.sending = false;
      this.timer = null;
      this.batchSize = 30;
      this.intervalMs = 3000;
      this.maxQueue = 1000;
      this.enabled = true;
      this._initTimer();
    }

    RemoteLoggerClass.prototype._initTimer = function () {
      if (this.timer) clearInterval(this.timer);
      this.timer = setInterval(() => this._flush(), this.intervalMs);
    };

    RemoteLoggerClass.prototype.push = function (evt) {
      if (!this.enabled) return;
      this.queue.push(evt);
      if (this.queue.length > this.maxQueue) {
        this.queue.splice(0, this.queue.length - this.maxQueue);
      }
    };

    RemoteLoggerClass.prototype._flush = function () {
      if (!this.enabled) return;
      if (this.sending) return;
      if (!this.queue.length) return;
      if (typeof fetch !== 'function') return;

      const batch = this.queue.splice(0, this.batchSize);
      if (!batch.length) return;

      this.sending = true;

      fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ logs: batch }),
      })
        .then((res) => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.text();
        })
        .then(() => {
          this.sending = false;
        })
        .catch((e) => {
          // 出错则把 batch 放回队列前面
          this.sending = false;
          this.queue = batch.concat(this.queue);
          console.warn('[RemoteLogger] flush error, will retry', e);
        });
    };

    RemoteLoggerClass.prototype.setEnabled = function (flag) {
      this.enabled = !!flag;
    };

    window.RemoteLogger = new RemoteLoggerClass();

    // 订阅 LunaLogger
    window.LunaLogger.subscribe(function (evt) {
      window.RemoteLogger.push(evt);
    });
  }

  // =========================
  // E3. MemoryAudit 记忆修改审计
  // =========================
  if (!window.MemoryAudit) {
    function MemoryAuditClass() {
      this.records = [];
      this.maxRecords = 500;
    }

    /**
     * 记录一次记忆更新
     * @param {Object} payload - {
     *   source: 'vision' | 'user' | 'system' | ...,
     *   key: 'scene.hospital.3f.toilet',
     *   before: any,
     *   after: any,
     *   confidence: number,
     *   note: string
     * }
     */
    MemoryAuditClass.prototype.recordUpdate = function (payload) {
      const rec = {
        ts: new Date().toISOString(),
        source: payload.source || 'unknown',
        key: payload.key || '',
        before: payload.before,
        after: payload.after,
        confidence:
          typeof payload.confidence === 'number' ? payload.confidence : null,
        note: payload.note || '',
      };

      this.records.push(rec);
      if (this.records.length > this.maxRecords) {
        this.records.shift();
      }

      if (window.LunaLogger) {
        window.LunaLogger.info('Memory update', { memoryUpdate: rec });
      }

      return rec;
    };

    MemoryAuditClass.prototype.getRecent = function (limit) {
      if (!limit || limit <= 0) limit = 50;
      if (this.records.length <= limit) {
        return this.records.slice();
      }
      return this.records.slice(this.records.length - limit);
    };

    window.MemoryAudit = new MemoryAuditClass();

    // 一个便捷函数：统一入口
    window.logMemoryUpdate = function (payload) {
      return window.MemoryAudit.recordUpdate(payload || {});
    };
  }

  // =========================
  // E4. 未捕获错误 & Promise 拦截
  // =========================
  if (typeof window !== 'undefined') {
    window.addEventListener('error', function (event) {
      try {
        window.LunaLogger.error('window.error', {
          message: event.message,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno,
          error: event.error ? String(event.error) : null,
        });
      } catch (e) {
        console.error('[Luna][window.error logger failed]', e);
      }
    });

    window.addEventListener('unhandledrejection', function (event) {
      try {
        window.LunaLogger.error('unhandledrejection', {
          reason: event.reason ? String(event.reason) : null,
        });
      } catch (e) {
        console.error('[Luna][unhandledrejection logger failed]', e);
      }
    });
  }

  window.LunaLogger.info('E Logging+Memory module initialized', {});
})();


    /* END: e_logging_memory.js */
    </script>

    </script>

    <!-- ========================= -->
    <!-- Vision Enhancer (旗舰视觉增强) -->
    <!-- ========================= -->
    <script>
        /* BEGIN: vision_enhancer.js
// frontend/vision_enhancer.js
/**
 * 旗舰视觉增强（YOLO六层逻辑）
 * - 多帧稳定（Stability）
 * - 伪深度估计（Pseudo-Depth）
 * - 场景分层（Scene / Geometry / Risk）
 * - 简易对象追踪（可占位实现）
 * - 环境"空场景"稳定滤波
 * - 输出统一的 visionSummary 供导航/危险逻辑使用
 */
(function () {
  'use strict';
  
  if (window.VisionEnhancer) return;

  const CENTER_REGION_RATIO = 0.5;   // 中央区域判定
  const NEAR_DISTANCE_CM = 150;      // 近距离危险阈值
  const STABILITY_WINDOW = 6;        // 多帧窗口
  const STABILITY_DANGER_THRESHOLD = 4;
  const SAFE_FRAME_WINDOW = 10;
  const SAFE_FRAME_THRESHOLD = 7;

  class StabilityFilter {
    constructor() {
      this.frames = [];
    }
    push(frame) {
      this.frames.push(frame);
      if (this.frames.length > STABILITY_WINDOW) {
        this.frames.shift();
      }
    }
    isDangerStable() {
      const count = this.frames.filter(f => f.isDangerFrame).length;
      return count >= STABILITY_DANGER_THRESHOLD;
    }
    reset() {
      this.frames = [];
    }
  }

  class SafeFrameFilter {
    constructor() {
      this.safeFrames = [];
    }
    push(isSafe) {
      this.safeFrames.push(isSafe);
      if (this.safeFrames.length > SAFE_FRAME_WINDOW) {
        this.safeFrames.shift();
      }
    }
    isStableSafe() {
      const countSafe = this.safeFrames.filter(Boolean).length;
      return countSafe >= SAFE_FRAME_THRESHOLD;
    }
    reset() {
      this.safeFrames = [];
    }
  }

  class VisionEnhancer {
    constructor() {
      this.stabilityFilter = new StabilityFilter();
      this.safeFilter = new SafeFrameFilter();
      this.suppressDangerUntil = 0;
      this.lastSummary = null;
    }

    estimateDistance(box, frameWidth, frameHeight) {
      const w = (box.x2 - box.x1);
      const h = (box.y2 - box.y1);
      const area = Math.max(w * h, 1);
      const k = 20000; // 可以后续通过标定调整
      return k / Math.sqrt(area);
    }

    isBoxCenter(block, frameWidth, frameHeight) {
      const cx = (block.x1 + block.x2) / 2;
      const cy = (block.y1 + block.y2) / 2;
      const rx = frameWidth * CENTER_REGION_RATIO / 2;
      const ry = frameHeight * CENTER_REGION_RATIO / 2;
      const centerX = frameWidth / 2;
      const centerY = frameHeight / 2;
      return (Math.abs(cx - centerX) <= rx && Math.abs(cy - centerY) <= ry);
    }

    classifyScene(detections) {
      // ✅ 防御性编程：确保 detections 不为 null
      if (!detections || !Array.isArray(detections)) {
        return 'unknown';
      }
      const labels = detections.map(d => d.label || d.class || '').filter(Boolean);
      let sceneType = 'unknown';
      if (labels.some(l => l.includes('train') || l.includes('platform'))) sceneType = 'subway';
      else if (labels.some(l => l.includes('escalator') || l.includes('shopping'))) sceneType = 'mall';
      else if (labels.some(l => l.includes('car') || l.includes('bus') || l.includes('vehicle'))) sceneType = 'street';
      else if (labels.some(l => l.includes('bed') || l.includes('monitor') || l.includes('chair'))) sceneType = 'indoor';
      
      // ✅ E4: 自动区域识别 - 输入视觉提示
      if (window.ZoneAutoDetector && sceneType !== 'unknown') {
        window.ZoneAutoDetector.feedVisualHint(sceneType);
      }
      
      return sceneType;
    }

    analyzeRisk(raw) {
      // ✅ 防御性编程：检查输入有效性
      if (!raw || !raw.detections || !Array.isArray(raw.detections)) {
        // 没有有效检测结果，当作安全帧处理
        this.stabilityFilter.push({ isDangerFrame: false });
        this.safeFilter.push(true);

        const summary = {
          ts: Date.now(),
          scene: 'unknown',
          hasDangerFrame: false,
          isDangerStable: this.stabilityFilter.isDangerStable(),
          dangerSuppressed: false,
          riskLevel: 'low',
          closestDanger: null,
          hazards: [],
          rawDetections: []
        };
        this.lastSummary = summary;
        return summary;
      }

      const { detections, frameWidth, frameHeight } = raw;
      let hasDanger = false;
      let closestDanger = null;
      const hazards = [];

      const now = Date.now();
      const dangerSuppressed = now < this.suppressDangerUntil;

      // ✅ 修复：先过滤掉 null/undefined，再处理
      const processed = (detections || [])
        .filter(Boolean)                 // ① 先把 null / undefined 过滤掉
        .map(rawDet => {
          const det = rawDet || {};      // ② 再兜一层保险

          // 兼容不同的box格式
          const box = det.box || det.bbox || { x1: 0, y1: 0, x2: 0, y2: 0 };
          const distance = this.estimateDistance(box, frameWidth || 640, frameHeight || 480);
          const inCenter = this.isBoxCenter(box, frameWidth || 640, frameHeight || 480);
          return Object.assign({}, det, { distance, inCenter, box }); // ③ 这里就安全了
        });

      for (const det of processed) {
        const { label, class: className, distance, inCenter } = det;
        const labelStr = label || className || '';

        if (labelStr.includes('person') && distance < 100 && inCenter) {
          // 认为可能是"自己"或紧贴镜头人脸，默认不报危险
          continue;
        }

        if (distance < NEAR_DISTANCE_CM && inCenter) {
          hasDanger = true;
          hazards.push({
            label: labelStr,
            distance,
            reason: 'near_center_obstacle',
          });
          if (!closestDanger || distance < closestDanger.distance) {
            closestDanger = { label: labelStr, distance };
          }
        }
      }

      const isDangerFrame = hasDanger && !dangerSuppressed;

      this.stabilityFilter.push({ isDangerFrame });
      this.safeFilter.push(!hasDanger);

      if (this.safeFilter.isStableSafe()) {
        // 连续多帧安全 → 短时间内压制危险
        this.suppressDangerUntil = Date.now() + 1000;
      }

      const stableDanger = this.stabilityFilter.isDangerStable() && !dangerSuppressed;

      const riskLevel = stableDanger
        ? (closestDanger && closestDanger.distance < 80 ? 'high' : 'medium')
        : 'low';

      const summary = {
        ts: Date.now(),
        scene: this.classifyScene(detections || []),
        hasDangerFrame: hasDanger,
        isDangerStable: this.stabilityFilter.isDangerStable(),
        dangerSuppressed,
        riskLevel,
        closestDanger,
        hazards,
        rawDetections: processed
      };

      this.lastSummary = summary;
      return summary;
    }

    processFrame(yoloOutput) {
      try {
        const summary = this.analyzeRisk(yoloOutput);

        // 原来：this.lastSummary = summary;
        this.lastSummary = summary;

        // ✅ 新增：把 yoloOutput 交给 SpaceEngine 构建 spaceState
        if (window.SpaceEngine) {
          try {
            const spaceState = window.SpaceEngine.updateFromDetections({
              detections: (yoloOutput && yoloOutput.detections) || [],
              frameWidth: yoloOutput.frameWidth,
              frameHeight: yoloOutput.frameHeight
            });
            summary.space_state = spaceState || null;
          } catch (e) {
            if (window.logError) {
              window.logError('SpaceEngine.updateFromDetections error in VisionEnhancer', {
                error: e.toString(),
                stack: e.stack
              });
            }
          }
        }

        if (window.logDebug) {
          window.logDebug('VisionEnhancer.summary', summary);
        }

        // 继续走 EventFlow
        if (window.EventFlow && window.EventFlow.onVisionSummary) {
          window.EventFlow.onVisionSummary(summary);
        }

        return summary;
      } catch (e) {
        if (window.logError) {
          window.logError('VisionEnhancer.processFrame error', { error: e.toString(), stack: e.stack });
        } else {
          console.error('VisionEnhancer.processFrame error', e);
        }
        return null;
      }
    }
  }

  window.VisionEnhancer = new VisionEnhancer();
  console.log('✅ VisionEnhancer模块加载完成', { module: 'vision_enhancer' });
})();



    END: vision_enhancer.js */
    </script>

    <!-- ========================= -->
    <!-- Event Flow (视觉×导航×语音总管线) -->
    <!-- ========================= -->
    <script>
        /* BEGIN: event_flow.js
// frontend/event_flow.js
/**
 * 视觉 × 导航 × 语音总管线
 * 把 VisionEnhancer → EventBridge → NavigationStrategy → TTS / UI / emotion_event 串成统一的总线
 */
(function () {
  'use strict';
  
  if (window.EventFlow) return;

  // === 保证 NavigationFSM 已初始化 ===
  if (!window.NavigationFSM) {
    console.warn("⚠️ EventFlow: NavigationFSM 未初始化 → 自动创建");
    window.NavigationFSM = { initialized: true, state: "IDLE" };
  } else if (!window.NavigationFSM.initialized) {
    window.NavigationFSM.initialized = true;
    window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
    console.log("✅ NavigationFSM 自动初始化完成 (EventFlow)");
  }

  const EventFlow = {
    onVisionSummary(summary) {
      if (!summary) return;

      // 1. 日志记录
      if (window.logDebug) {
        window.logDebug('EventFlow.onVisionSummary', summary);
      }

      // 2. 危险流：如果稳定危险 → 派发 hazard 事件
      if (summary.isDangerStable && !summary.dangerSuppressed) {
        const payload = {
          type: 'vision_hazard',
          scene: summary.scene,
          riskLevel: summary.riskLevel,
          closestDanger: summary.closestDanger,
          hazards: summary.hazards
        };
        
        if (window.emitHazardEvent) {
          window.emitHazardEvent(payload);
        }
        
        if (window.emotion_event) {
          window.emotion_event('hazard_detected', 'high', payload);
        }
      }

      // 3. 导航流：始终发送导航"环境信息"，用于策略与路点系统
      const navPayload = {
        scene: summary.scene,
        riskLevel: summary.riskLevel,
        closestDanger: summary.closestDanger,
        hasDanger: summary.hasDangerFrame,
        rawDetections: summary.rawDetections
      };

      if (window.emitNavigationEvent) {
        window.emitNavigationEvent(navPayload);
      }

      // 4. AutoRecovery：视觉异常时可记录
      if (window.AutoRecovery && summary.riskLevel === 'low' && !summary.hasDangerFrame) {
        if (window.AutoRecovery.record) {
          window.AutoRecovery.record('vision', 'stable', { ts: summary.ts });
        }
      }

      // 5. SpaceEngine 空间状态处理（如果 summary 中包含 space_state）
      if (summary.space_state && window.EventFlow.onSpaceState) {
        window.EventFlow.onSpaceState(summary.space_state);
      }
    },

    onSpaceState(spaceState) {
      if (!spaceState) return;

      // ✅ 优先调用 SpatialEnginePro（Pro 版增强层）
      if (window.SpatialEnginePro) {
        window.SpatialEnginePro.ingestSpaceState(spaceState);
        return; // Pro 版会自己处理后续流程
      }

      // 只有在 Pro 不存在时，才走旧逻辑
      if (window.logDebug) {
        window.logDebug('EventFlow.onSpaceState', {
          scene_type: spaceState.scene_type,
          overall_risk: spaceState.overall_risk,
          has_primary: !!spaceState.primary_hazard
        });
      }

      // 1) 危险事件：核心危险体 + 总体风险
      if (spaceState.primary_hazard && spaceState.overall_risk !== 'low') {
        const h = spaceState.primary_hazard;
        const payload = {
          type: 'space_hazard',
          scene_type: spaceState.scene_type,
          risk_level: spaceState.overall_risk,
          hazard: h
        };
        
        if (window.emitHazardEvent) {
          window.emitHazardEvent(payload);
        }
        
        if (window.emotion_event) {
          window.emotion_event('hazard_detected', spaceState.overall_risk, payload);
        }
      }

      // 2) 导航状态机：把空间更新丢给 NavigationFSM
      if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
        window.NavigationFSM.handleEvent({
          type: 'space_update',
          spaceState: spaceState
        });
      }

      // 3) 路点系统：根据空间状态检查进度
      if (window.WaypointManager && typeof window.WaypointManager.checkProgress === 'function') {
        window.WaypointManager.checkProgress({
          spaceState: spaceState
        });
      }

      // 4) 如果有地图记忆中的静态危险点，且当前整体风险为 low/medium，也可以做"记忆驱动的温和提示"
      try {
        if (window.MapMemory && spaceState.grid && spaceState.objects && spaceState.objects.length) {
          const staticHazards = [];

          for (let i = 0; i < spaceState.objects.length; i++) {
            const obj = spaceState.objects[i];
            if (obj.memory && obj.memory.is_static_hazard) {
              staticHazards.push(obj);
            }
          }

          if (staticHazards.length > 0) {
            // 记忆层面的危险，哪怕 YOLO 当前帧没报高风险，也可以轻声提醒
            if (window.logInfo) {
              window.logInfo('EventFlow: memory-driven static hazard detected', {
                count: staticHazards.length,
                examples: staticHazards.slice(0, 3)
              });
            }

            // 可以选择通过 taskChain/tts 做温和提示，这里只触发一个导航事件，具体 TTS 策略留在现有逻辑
            if (window.emitNavigationEvent) {
              window.emitNavigationEvent({
                type: 'memory_static_hazard',
                hazards: staticHazards
              });
            }
          }
        }
      } catch (e) {
        if (window.logError) {
          window.logError('EventFlow.onSpaceState memory logic error', {
            error: e.toString(),
            stack: e.stack
          });
        }
      }

      // 5) AutoRecovery 记录低/高风险状态（便于后端分析卡顿/误报）
      if (window.AutoRecovery && typeof window.AutoRecovery.record === 'function') {
        let statusLabel = 'stable';
        if (spaceState.overall_risk === 'high' || spaceState.overall_risk === 'critical') {
          statusLabel = 'high_risk';
        }
        window.AutoRecovery.record('navigation', statusLabel, {
          overall_risk: spaceState.overall_risk,
          scene_type: spaceState.scene_type
        });
      }
    }
  };

  window.EventFlow = EventFlow;
  console.log('✅ EventFlow模块加载完成', { module: 'event_flow' });
})();



    END: event_flow.js */
    <!-- ===================== -->
    <!-- Luna SpaceEngine (Spatial Engine) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: spatial_engine.js
// frontend/spatial_engine.js
/**
 * SpaceEngine / 空间引擎
 * 在 YOLO 之上构建"鸟瞰图 + 风险评估 + 行为建议"
 * 
 * 输入：YOLO检测结果（detections, frameWidth, frameHeight）
 * 输出：spaceState（场景类型、鸟瞰图、风险评估、行为建议）
 */
(function () {
  'use strict';
  
  if (window.SpaceEngine) return;

  const M_PER_PIXEL_BASE = 0.002; // 粗略系数：后期可标定调整
  const BEV_MAX_FORWARD_M = 5.0;
  const BEV_HALF_WIDTH_M = 2.0;
  const BEV_RESOLUTION_M = 0.25; // 每格 25cm

  const SCENE_TYPES = {
    UNKNOWN: 'unknown',
    STREET: 'street',
    SUBWAY: 'subway',
    MALL: 'mall',
    HOSPITAL: 'hospital',
    INDOOR_CORRIDOR: 'indoor_corridor',
    STAIRS_AREA: 'stairs_area'
  };

  const RISK_LEVELS = ['low', 'medium', 'high', 'critical'];

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function sign(v) {
    return v >= 0 ? 1 : -1;
  }

  /**
   * Track：多帧追踪单个目标
   */
  class Track {
    constructor(id, det, frameWidth, frameHeight) {
      this.id = id;
      this.label = det.label || det.class || '';
      this.history = [];
      this.stableFrames = 0;
      this.lastUpdateTs = Date.now();
      this.addObservation(det, frameWidth, frameHeight);
    }

    addObservation(det, frameWidth, frameHeight) {
      const now = Date.now();
      const geom = SpaceEngineGeometry.computeGeometry(det, frameWidth, frameHeight);
      this.history.push({
        ts: now,
        det,
        geom
      });
      if (this.history.length > 10) {
        this.history.shift();
      }
      this.lastUpdateTs = now;

      // 稳定帧数：连续出现则增加
      this.stableFrames += 1;
    }

    getLatest() {
      return this.history[this.history.length - 1] || null;
    }

    // 速度/运动趋势估计
    getMotion() {
      if (this.history.length < 2) return 'static';
      const last = this.history[this.history.length - 1];
      const prev = this.history[this.history.length - 2];
      const dy = prev.geom.distance_m - last.geom.distance_m; // 正数表示靠近
      const dx = last.geom.bearing_deg - prev.geom.bearing_deg;

      if (Math.abs(dy) < 0.05 && Math.abs(dx) < 1) return 'static';
      if (dy > 0.1) return 'approaching';
      if (dy < -0.1) return 'leaving';
      // 水平穿越
      if (Math.abs(dx) > 3) return 'crossing';
      return 'unknown';
    }
  }

  /**
   * SpaceEngineGeometry：几何计算（2D → 伪3D）
   */
  const SpaceEngineGeometry = {
    // 估算距离 & 方位；不用物理精度，保持一致性即可
    computeGeometry(det, frameWidth, frameHeight) {
      const box = det.box || det.bbox || det.rect;
      if (!box) {
        return {
          distance_m: 10,
          bearing_deg: 0,
          in_path: false,
          bev_x: 0,
          bev_y: 10
        };
      }
      const x1 = box.x1, y1 = box.y1, x2 = box.x2, y2 = box.y2;
      const w = x2 - x1;
      const h = y2 - y1;
      const cx = (x1 + x2) / 2;
      const cy = (y1 + y2) / 2;
      const area = Math.max(w * h, 1);

      // 距离估算：面积越大，距离越近
      const approxDistanceM = clamp((1.0 / Math.sqrt(area)) / M_PER_PIXEL_BASE, 0.2, 10.0);

      // bearing：相对水平中心的偏移
      const centerX = frameWidth / 2;
      const offsetX = (cx - centerX) / centerX; // -1 ~ 1
      const MAX_FOV_DEG = 80; // 视场角可以后续标定
      const bearingDeg = clamp(offsetX * (MAX_FOV_DEG / 2), -MAX_FOV_DEG / 2, MAX_FOV_DEG / 2);

      // in_path：中心区域
      const PATH_REGION_RATIO = 0.4;
      const pathHalfWidthPx = frameWidth * PATH_REGION_RATIO / 2;
      const inPath = Math.abs(cx - centerX) <= pathHalfWidthPx;

      // 鸟瞰坐标：以脚下为原点，y 正向前，x 左负右正
      const rad = bearingDeg * Math.PI / 180.0;
      const bevY = approxDistanceM * Math.cos(rad);
      const bevX = approxDistanceM * Math.sin(rad);

      return {
        distance_m: approxDistanceM,
        bearing_deg: bearingDeg,
        in_path: inPath,
        bev_x: bevX,
        bev_y: bevY
      };
    }
  };

  /**
   * SpaceEngineClass：主引擎类
   */
  class SpaceEngineClass {
    constructor() {
      this.tracks = {};
      this.nextId = 1;
      this.lastSpaceState = null;
    }

    _allocId() {
      return 'trk_' + (this.nextId++);
    }

    // 简单 IoU 匹配：将新检测匹配到已有 Track
    _matchDetectionsToTracks(detections, frameWidth, frameHeight) {
      const usedTrackIds = new Set();
      const detAssignments = []; // {det, track}

      // 把历史 track 的最新 box 拿出来
      const trackList = Object.values(this.tracks).map(track => {
        const latest = track.getLatest();
        return latest ? { track, box: latest.det.box || latest.det.bbox || latest.det.rect } : null;
      }).filter(Boolean);

      function iou(boxA, boxB) {
        if (!boxA || !boxB) return 0;
        const x1 = Math.max(boxA.x1, boxB.x1);
        const y1 = Math.max(boxA.y1, boxB.y1);
        const x2 = Math.min(boxA.x2, boxB.x2);
        const y2 = Math.min(boxA.y2, boxB.y2);
        const interW = Math.max(0, x2 - x1);
        const interH = Math.max(0, y2 - y1);
        const interArea = interW * interH;
        const areaA = (boxA.x2 - boxA.x1) * (boxA.y2 - boxA.y1);
        const areaB = (boxB.x2 - boxB.x1) * (boxB.y2 - boxB.y1);
        if (areaA <= 0 || areaB <= 0) return 0;
        return interArea / (areaA + areaB - interArea);
      }

      detections.forEach(det => {
        const box = det.box || det.bbox || det.rect;
        let bestTrack = null;
        let bestIoU = 0;

        trackList.forEach(entry => {
          if (usedTrackIds.has(entry.track.id)) return;
          const score = iou(box, entry.box);
          if (score > bestIoU) {
            bestIoU = score;
            bestTrack = entry.track;
          }
        });

        if (bestTrack && bestIoU > 0.3) {
          usedTrackIds.add(bestTrack.id);
          detAssignments.push({ det, track: bestTrack });
        } else {
          // 新建 track
          const newId = this._allocId();
          const t = new Track(newId, det, frameWidth, frameHeight);
          this.tracks[newId] = t;
          usedTrackIds.add(newId);
          detAssignments.push({ det, track: t });
        }
      });

      // 清理长时间未更新的 Track
      const now = Date.now();
      Object.keys(this.tracks).forEach(id => {
        const t = this.tracks[id];
        if (now - t.lastUpdateTs > 5000) { // 5s 没更新就删
          delete this.tracks[id];
        }
      });

      // 更新匹配到的 track
      detAssignments.forEach(assign => {
        assign.track.addObservation(assign.det, frameWidth, frameHeight);
      });

      return Object.values(this.tracks);
    }

    // 场景类型判断
    _classifyScene(detections) {
      const labels = detections.map(d => d.label || d.class || '');
      const has = (name) => labels.some(l => l && l.toLowerCase().includes(name));

      if (has('train') || has('platform')) return SCENE_TYPES.SUBWAY;
      if (has('escalator') || has('shopping_cart') || has('shelf')) return SCENE_TYPES.MALL;
      if (has('car') || has('bus') || has('traffic_light') || has('crosswalk')) return SCENE_TYPES.STREET;
      if (has('bed') || has('wheelchair') || has('stretcher')) return SCENE_TYPES.HOSPITAL;
      if (has('stairs') || has('staircase')) return SCENE_TYPES.STAIRS_AREA;
      if (has('door') || has('corridor')) return SCENE_TYPES.INDOOR_CORRIDOR;
      return SCENE_TYPES.UNKNOWN;
    }

    // 风险打分
    _computeRiskForTrack(track, sceneType) {
      const latest = track.getLatest();
      if (!latest) return { score: 0, level: 'low' };

      const g = latest.geom;
      const motion = track.getMotion();
      const label = track.label.toLowerCase();
      let score = 0;

      if (g.in_path) score += 3;
      if (g.distance_m < 1.5) score += 3;
      if (g.distance_m < 0.8) score += 3;
      if (motion === 'approaching') score += 3;
      if (motion === 'crossing') score += 2;
      if (track.stableFrames >= 3) score += 2;

      // 类型 + 场景加权
      if (label.includes('stairs') || label.includes('staircase')) {
        score += 5;
      }
      if (sceneType === SCENE_TYPES.STREET && (label.includes('car') || label.includes('bus'))) {
        score += 4;
      }
      if (sceneType === SCENE_TYPES.SUBWAY && label.includes('platform_edge')) {
        score += 5;
      }

      // ✅ 使用地图记忆加权风险（如果某点被记为静态危险点，就加权）
      if (window.MapMemory && this.lastSpaceState && this.lastSpaceState.grid) {
        try {
          const gridMeta = this.lastSpaceState.grid;
          const latest = track.getLatest();
          if (latest && typeof latest.geom.bev_x === 'number' && typeof latest.geom.bev_y === 'number') {
            const place = window.MapMemory.getCurrentPlace && window.MapMemory.getCurrentPlace();
            if (place) {
              const cell = place.queryByBevCoord(latest.geom.bev_x, latest.geom.bev_y, gridMeta);
              if (cell && cell.isStaticHazard) {
                score += 2; // 静态危险点：额外加权
                if (window.logDebug) {
                  window.logDebug('SpaceEngine: risk boosted by MapMemory', {
                    label: track.label,
                    bev_x: latest.geom.bev_x,
                    bev_y: latest.geom.bev_y,
                    cell_type: cell.staticType,
                    new_score: score
                  });
                }
              }
            }
          }
        } catch (e) {
          if (window.logError) {
            window.logError('SpaceEngine: MapMemory risk boost error', {
              error: e.toString(),
              stack: e.stack
            });
          }
        }
      }

      // 转 level
      let level = 'low';
      if (score >= 12) level = 'critical';
      else if (score >= 8) level = 'high';
      else if (score >= 4) level = 'medium';

      return { score, level };
    }

    // 构建鸟瞰 Grid
    _buildGridFromTracks(tracks) {
      const widthM = BEV_HALF_WIDTH_M * 2;
      const heightM = BEV_MAX_FORWARD_M;
      const res = BEV_RESOLUTION_M;
      const cols = Math.ceil(widthM / res);
      const rows = Math.ceil(heightM / res);
      const cells = [];

      function coordToIndex(x, y) {
        const col = Math.floor((x + BEV_HALF_WIDTH_M) / res);
        const row = Math.floor(y / res);
        if (col < 0 || col >= cols || row < 0 || row >= rows) return null;
        return { col, row };
      }

      tracks.forEach(track => {
        const latest = track.getLatest();
        if (!latest) return;
        const gx = latest.geom.bev_x;
        const gy = latest.geom.bev_y;
        const idx = coordToIndex(gx, gy);
        if (!idx) return;
        cells.push({
          xIndex: idx.col,
          yIndex: idx.row,
          occupied: true,
          type: track.label,
          risk: track._riskLevel || 'low'
        });
      });

      return {
        width_m: widthM,
        height_m: heightM,
        resolution_m: res,
        cells
      };
    }

    // 入口：每帧更新
    updateFromDetections(frameData) {
      try {
        const { detections, frameWidth, frameHeight } = frameData || {};
        if (!Array.isArray(detections) || !frameWidth || !frameHeight) {
          if (window.logDebug) {
            window.logDebug('SpaceEngine.updateFromDetections: invalid frameData', frameData);
          }
          return null;
        }

        // 1) 更新追踪
        const tracks = this._matchDetectionsToTracks(detections, frameWidth, frameHeight);

        // 2) 场景判断
        const sceneType = this._classifyScene(detections);

        // 3) 风险评估
        let primaryHazard = null;
        let maxScore = -1;
        const objectStates = [];

        tracks.forEach(track => {
          const latest = track.getLatest();
          if (!latest) return;
          const geom = latest.geom;
          const motion = track.getMotion();
          const risk = this._computeRiskForTrack(track, sceneType);
          track._riskScore = risk.score;
          track._riskLevel = risk.level;

          const objState = {
            trackId: track.id,
            type: track.label,
            distance: geom.distance_m,
            bearing: geom.bearing_deg,
            in_path: geom.in_path,
            stable_frames: track.stableFrames,
            motion,
            risk_score: risk.score,
            risk_level: risk.level,
            bev: { x: geom.bev_x, y: geom.bev_y }
          };
          objectStates.push(objState);

          if (risk.score > maxScore) {
            maxScore = risk.score;
            primaryHazard = objState;
          }
        });

        // 4) overall risk
        let overallRisk = 'low';
        if (maxScore >= 12) overallRisk = 'critical';
        else if (maxScore >= 8) overallRisk = 'high';
        else if (maxScore >= 4) overallRisk = 'medium';

        // 5) 推荐行为
        let recommendedAction = 'keep';
        if (overallRisk === 'medium') recommendedAction = 'slow_down';
        if (overallRisk === 'high') recommendedAction = 'prepare_stop';
        if (overallRisk === 'critical') recommendedAction = 'stop_immediately';

        // 6) 构建鸟瞰 grid
        const grid = this._buildGridFromTracks(tracks);

        let spaceState = {
          ts: Date.now(),
          scene_type: sceneType,
          ego: {
            position: { x: 0, y: 0 },
            direction: 'forward'
          },
          grid,
          objects: objectStates,
          primary_hazard: primaryHazard,
          overall_risk: overallRisk,
          recommended_action: recommendedAction
        };

        // ✅ 利用地图记忆模块：更新 + 增强
        if (window.MapMemory) {
          try {
            window.MapMemory.update(spaceState, {
              placeId: 'session_default'  // 一期先这样，后面可以用真实 placeId
            });
            const enriched = window.MapMemory.enrichSpaceState(spaceState);
            if (enriched) {
              spaceState = enriched;
            }
          } catch (e) {
            if (window.logError) {
              window.logError('SpaceEngine: MapMemory integration error', {
                error: e.toString(),
                stack: e.stack
              });
            }
          }
        }

        this.lastSpaceState = spaceState;

        if (window.logDebug) {
          window.logDebug('SpaceEngine.spaceState', spaceState);
        }

        // 通知 EventFlow / NavigationFSM / WaypointManager
        if (window.EventFlow && window.EventFlow.onSpaceState) {
          window.EventFlow.onSpaceState(spaceState);
        }

        return spaceState;
      } catch (e) {
        if (window.logError) {
          window.logError('SpaceEngine.updateFromDetections error', {
            error: e.toString(),
            stack: e.stack
          });
        } else {
          console.error('SpaceEngine.updateFromDetections error', e);
        }
        return null;
      }
    }

    getLastSpaceState() {
      return this.lastSpaceState;
    }
  }

  window.SpaceEngine = new SpaceEngineClass();
  
  if (window.logInfo) {
    window.logInfo('SpaceEngine模块加载完成', { module: 'spatial_engine' });
  } else {
    console.log('✅ SpaceEngine模块加载完成', { module: 'spatial_engine' });
  }
})();


    END: spatial_engine.js */
    <!-- ===================== -->
    <!-- Luna MapMemory (Map Memory System) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: map_memory.js
// frontend/map_memory.js
/**
 * MapMemory / 地图记忆系统
 * 场景级记忆引擎：记住环境结构、静态地标、高频危险区域
 * 含记忆变更日志输出
 */
(function () {
  'use strict';
  
  if (window.MapMemory) return;

  const MAX_CELL_HISTORY = 50;     // 每个格子最多保留多少条样本
  const MIN_STATIC_COUNT = 5;      // 超过多少次可以认为是"稳定存在"
  const STATIC_TYPES = ['stairs', 'staircase', 'pillar', 'wall', 'door'];

  // 统一的 risk 数值映射
  const RISK_WEIGHT = {
    low: 0,
    medium: 1,
    high: 2,
    critical: 3
  };

  function safeLogInfo(msg, payload) {
    if (window.logInfo) {
      window.logInfo(msg, payload);
    } else {
      console.log('[MapMemory/INFO]', msg, payload || '');
    }
  }

  function safeLogDebug(msg, payload) {
    if (window.logDebug) {
      window.logDebug(msg, payload);
    } else {
      console.debug('[MapMemory/DEBUG]', msg, payload || '');
    }
  }

  function safeLogError(msg, payload) {
    if (window.logError) {
      window.logError(msg, payload);
    } else {
      console.error('[MapMemory/ERROR]', msg, payload || '');
    }
  }

  function normalizeType(type) {
    if (!type) return 'unknown';
    return String(type).toLowerCase();
  }

  /**
   * CellStats：单个格子的统计信息
   */
  class CellStats {
    constructor(xIndex, yIndex) {
      this.xIndex = xIndex;
      this.yIndex = yIndex;
      this.samples = [];       // [{type, risk, ts}]
      this.typeCounts = {};    // { 'stairs': 10, 'wall': 5 ...}
      this.riskSum = 0;
      this.riskCount = 0;
      this.isStaticHazard = false;
      this.staticType = null;
    }

    addSample(obj) {
      const now = Date.now();
      const type = normalizeType(obj.type);
      const risk = obj.risk_level || 'low';

      this.samples.push({
        type: type,
        risk: risk,
        ts: now
      });
      if (this.samples.length > MAX_CELL_HISTORY) {
        this.samples.shift();
      }

      // 类型统计
      this.typeCounts[type] = (this.typeCounts[type] || 0) + 1;

      // 风险统计
      const weight = RISK_WEIGHT[risk] || 0;
      this.riskSum += weight;
      this.riskCount += 1;

      this._updateStaticHazard();
    }

    _updateStaticHazard() {
      const before = this.isStaticHazard;
      const dom = this.getDominantType();
      const avgRisk = this.getAvgRiskLevel();

      const isStaticType = dom.type &&
        STATIC_TYPES.some(t => dom.type.indexOf(t) !== -1);

      const enoughCount = dom.count >= MIN_STATIC_COUNT;
      const riskHigh = avgRisk === 'high' || avgRisk === 'critical';

      this.isStaticHazard = !!(isStaticType && (enoughCount || riskHigh));
      this.staticType = this.isStaticHazard ? dom.type : null;

      // 只有从 false -> true 时才记一条日志
      if (!before && this.isStaticHazard) {
        safeLogInfo('MapMemory: cell promoted to static hazard', {
          cell: { xIndex: this.xIndex, yIndex: this.yIndex },
          static_type: this.staticType,
          dominant_count: dom.count,
          avg_risk: avgRisk
        });
      }
    }

    getDominantType() {
      let bestType = null;
      let bestCount = 0;
      Object.keys(this.typeCounts).forEach(k => {
        const v = this.typeCounts[k];
        if (v > bestCount) {
          bestCount = v;
          bestType = k;
        }
      });
      return { type: bestType, count: bestCount };
    }

    getAvgRiskLevel() {
      if (!this.riskCount) return 'low';
      const avg = this.riskSum / this.riskCount;
      if (avg >= 2.5) return 'critical';
      if (avg >= 1.5) return 'high';
      if (avg >= 0.5) return 'medium';
      return 'low';
    }
  }

  /**
   * PlaceMap：地点地图（对应一个场景）
   */
  class PlaceMap {
    constructor(placeId) {
      this.placeId = placeId;
      this.grid = {}; // key: "xIndex,yIndex" -> CellStats
      this.lastUpdateTs = Date.now();
      this.sceneTypes = {}; // 场景类型分布
    }

    _cellKey(xIndex, yIndex) {
      return xIndex + ',' + yIndex;
    }

    updateFromSpaceState(spaceState) {
      this.lastUpdateTs = Date.now();
      if (!spaceState || !spaceState.grid) return;

      const st = spaceState.scene_type || 'unknown';
      this.sceneTypes[st] = (this.sceneTypes[st] || 0) + 1;

      const grid = spaceState.grid;
      const objects = spaceState.objects || [];

      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = bev.x;
        const y = bev.y;
        if (typeof x !== 'number' || typeof y !== 'number') continue;

        const xIndex = Math.floor((x + grid.width_m / 2) / grid.resolution_m);
        const yIndex = Math.floor(y / grid.resolution_m);
        if (xIndex < 0 || yIndex < 0) continue;

        const key = this._cellKey(xIndex, yIndex);
        if (!this.grid[key]) {
          this.grid[key] = new CellStats(xIndex, yIndex);
        }

        this.grid[key].addSample({
          type: obj.type,
          risk_level: obj.risk_level
        });
      }
    }

    queryCell(xIndex, yIndex) {
      const key = this._cellKey(xIndex, yIndex);
      return this.grid[key] || null;
    }

    queryByBevCoord(x, y, gridMeta) {
      if (!gridMeta) return null;
      const xIndex = Math.floor((x + gridMeta.width_m / 2) / gridMeta.resolution_m);
      const yIndex = Math.floor(y / gridMeta.resolution_m);
      return this.queryCell(xIndex, yIndex);
    }

    /**
     * 判断某点是否是"记忆中的静态危险点"
     */
    isStaticHazardAt(x, y, gridMeta) {
      const cell = this.queryByBevCoord(x, y, gridMeta);
      return !!(cell && cell.isStaticHazard);
    }

    getSnapshotSummary() {
      // 用于调试：导出一个简要概览
      const cells = [];
      Object.keys(this.grid).forEach(key => {
        const cell = this.grid[key];
        const dom = cell.getDominantType();
        const avgRisk = cell.getAvgRiskLevel();
        if (!dom.type) return;
        cells.push({
          key: key,
          type: dom.type,
          count: dom.count,
          avg_risk: avgRisk,
          is_static_hazard: cell.isStaticHazard
        });
      });
      return {
        placeId: this.placeId,
        updated_at: this.lastUpdateTs,
        sceneTypes: this.sceneTypes,
        cells: cells
      };
    }
  }

  /**
   * MapMemoryClass：地图记忆主类
   */
  class MapMemoryClass {
    constructor() {
      this.places = {}; // placeId -> PlaceMap
      this.currentPlaceId = 'session_default';
    }

    setCurrentPlace(placeId) {
      if (!placeId) return;
      this.currentPlaceId = placeId;
      if (!this.places[placeId]) {
        this.places[placeId] = new PlaceMap(placeId);
        safeLogInfo('MapMemory: new place created', { placeId: placeId });
      } else {
        safeLogDebug('MapMemory: switch to existing place', { placeId: placeId });
      }
    }

    getCurrentPlace() {
      if (!this.places[this.currentPlaceId]) {
        this.places[this.currentPlaceId] = new PlaceMap(this.currentPlaceId);
      }
      return this.places[this.currentPlaceId];
    }

    /**
     * 入口：SpaceEngine 每帧调用，用当前空间状态更新记忆
     * context 可以传 placeId、gps 等
     */
    update(spaceState, context) {
      try {
        if (!spaceState || !spaceState.grid) return;
        if (context && context.placeId) {
          this.setCurrentPlace(context.placeId);
        }

        const place = this.getCurrentPlace();
        place.updateFromSpaceState(spaceState);

        safeLogDebug('MapMemory.update', {
          placeId: this.currentPlaceId,
          scene_type: spaceState.scene_type,
          objects: (spaceState.objects || []).length
        });
      } catch (e) {
        safeLogError('MapMemory.update error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    /**
     * 用记忆增强 SpaceState，在每个 object 上挂 memory 字段
     */
    enrichSpaceState(spaceState) {
      if (!spaceState || !spaceState.grid) return spaceState;
      const place = this.getCurrentPlace();
      const gridMeta = spaceState.grid;

      const enrichedObjects = (spaceState.objects || []).map(obj => {
        const bev = obj.bev || {};
        const cell = place.queryByBevCoord(bev.x, bev.y, gridMeta);
        if (!cell) {
          return obj;
        }
        const dom = cell.getDominantType();
        const avgRisk = cell.getAvgRiskLevel();
        const memoryTag = {
          dominant_type: dom.type,
          dominant_count: dom.count,
          avg_risk: avgRisk,
          is_static_hazard: cell.isStaticHazard
        };
        return Object.assign({}, obj, { memory: memoryTag });
      });

      return Object.assign({}, spaceState, {
        objects: enrichedObjects
      });
    }

    /** 调试接口：打印当前 PlaceMap 概览 */
    debugPrintCurrentPlace() {
      const place = this.getCurrentPlace();
      const snapshot = place.getSnapshotSummary();
      safeLogInfo('MapMemory snapshot', snapshot);
      return snapshot;
    }
  }

  // 挂到全局
  window.MapMemory = new MapMemoryClass();

  // 提供一个便捷调试函数
  window.debugPrintMapMemory = function () {
    if (!window.MapMemory) return;
    return window.MapMemory.debugPrintCurrentPlace();
  };

  if (window.logInfo) {
    window.logInfo('MapMemory模块加载完成', { module: 'map_memory' });
  } else {
    console.log('✅ MapMemory模块加载完成', { module: 'map_memory' });
  }
})();

    END: map_memory.js */
    <!-- ===================== -->
    <!-- Luna Pro Modules (SpatialEnginePro / MapMemoryPro / EventFlowPro) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: spatial_engine_pro.js */
// frontend/spatial_engine_pro.js
/**
 * SpatialEnginePro / 空间引擎 Pro 版
 * 基于现有 spaceState 做增强：伪深度、接近速度、简单运动向量 + pointGrid
 * 
 * 输入：spaceState（来自 SpaceEngine）
 * 输出：enhancedState（交给 EventFlowPro / 导航 / 记忆Pro）
 */
(function () {
  'use strict';
  
  if (window.SpatialEnginePro) return;

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[SpatialEnginePro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[SpatialEnginePro]', msg, payload || '');
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  /**
   * SpatialEngineProClass：空间引擎 Pro 版主类
   * 简单的运动估计：用历史空间状态里的同一 trackId 做差分
   */
  class SpatialEngineProClass {
    constructor() {
      this.lastObjectsById = {}; // trackId -> { ts, distance, bearing, bev_x, bev_y }
      this.lastEnhancedState = null;
    }

    /**
     * 主入口：由 EventFlow.onSpaceState 调用
     * @param {Object} spaceState 原始SpaceEngine输出
     * @returns {Object|null} enhancedState
     */
    ingestSpaceState(spaceState) {
      try {
        if (!spaceState || !spaceState.objects) {
          return null;
        }

        const now = Date.now();
        const objects = spaceState.objects || [];
        const enhancedObjects = [];
        const pointGrid = [];

        for (let i = 0; i < objects.length; i++) {
          const obj = objects[i];
          const trackId = obj.trackId || ('obj_' + i);
          const geom = {
            distance: obj.distance,
            bearing: obj.bearing,
            bev_x: obj.bev && typeof obj.bev.x === 'number' ? obj.bev.x : null,
            bev_y: obj.bev && typeof obj.bev.y === 'number' ? obj.bev.y : null
          };

          const history = this.lastObjectsById[trackId];
          let approachSpeed = 0; // m/s，正数表示靠近
          let lateralSpeed = 0;  // m/s，正数表示向右

          if (history && typeof history.distance === 'number' && typeof geom.distance === 'number') {
            const dtSec = (now - history.ts) / 1000.0;
            if (dtSec > 0.01 && dtSec < 2.0) {
              approachSpeed = (history.distance - geom.distance) / dtSec;
              if (typeof history.bev_x === 'number' && typeof geom.bev_x === 'number') {
                lateralSpeed = (geom.bev_x - history.bev_x) / dtSec;
              }
            }
          }

          this.lastObjectsById[trackId] = {
            ts: now,
            distance: geom.distance,
            bearing: geom.bearing,
            bev_x: geom.bev_x,
            bev_y: geom.bev_y
          };

          // 运动趋势基本判断
          let motionPro = 'static';
          if (approachSpeed > 0.2) motionPro = 'approaching_fast';
          else if (approachSpeed > 0.05) motionPro = 'approaching';
          else if (approachSpeed < -0.2) motionPro = 'leaving_fast';
          else if (approachSpeed < -0.05) motionPro = 'leaving';
          else if (Math.abs(lateralSpeed) > 0.2) motionPro = 'crossing';

          const enhancedObj = Object.assign({}, obj, {
            pro_motion: motionPro,
            pro_approach_speed: approachSpeed, // m/s
            pro_lateral_speed: lateralSpeed    // m/s
          });
          enhancedObjects.push(enhancedObj);

          // pointGrid 点云增强
          if (geom.bev_x !== null && geom.bev_y !== null && typeof geom.distance === 'number') {
            pointGrid.push({
              x: geom.bev_x,
              y: geom.bev_y,
              distance: geom.distance,
              type: obj.type || obj.label || 'unknown',
              risk_level: obj.risk_level || 'low',
              trackId: trackId,
              pro_motion: motionPro,
              pro_approach_speed: approachSpeed,
              pro_lateral_speed: lateralSpeed
            });
          }
        }

        const enhancedState = Object.assign({}, spaceState, {
          objects: enhancedObjects,
          pointGrid: pointGrid
        });

        this.lastEnhancedState = enhancedState;
        logDebug('SpatialEnginePro.enhancedState', {
          scene_type: enhancedState.scene_type,
          object_count: enhancedObjects.length,
          point_count: pointGrid.length
        });

        // 分发给 Pro 版事件流优先，否则回落到普通 EventFlow
        if (window.EventFlowPro && typeof window.EventFlowPro.onSpaceStateEnhanced === 'function') {
          window.EventFlowPro.onSpaceStateEnhanced(enhancedState);
        } else if (window.EventFlow && typeof window.EventFlow.onSpaceState === 'function') {
          // 回落逻辑：用增强后的状态代替原来状态
          window.EventFlow.onSpaceState(enhancedState);
        }

        return enhancedState;
      } catch (e) {
        logError('SpatialEnginePro.ingestSpaceState error', {
          error: e.toString(),
          stack: e.stack
        });
        return null;
      }
    }

    getLastEnhancedState() {
      return this.lastEnhancedState;
    }
  }

  window.SpatialEnginePro = new SpatialEngineProClass();

  // 提供一个全局便捷函数：原来的 EventFlow.onSpaceState 可以改成调用这里
  window.ingestSpaceStatePro = function (spaceState) {
    if (!window.SpatialEnginePro) return null;
    return window.SpatialEnginePro.ingestSpaceState(spaceState);
  };

  if (window.logInfo) {
    window.logInfo('SpatialEnginePro模块加载完成', { module: 'spatial_engine_pro' });
  } else {
    console.log('✅ SpatialEnginePro模块加载完成', { module: 'spatial_engine_pro' });
  }
})();


    /* END: spatial_engine_pro.js */
    </script>
    <script>
    /* BEGIN: map_memory_pro.js */
// frontend/map_memory_pro.js
/**
 * MapMemoryPro / 地图记忆 Pro 版
 * 在已有 MapMemory 之上，再加一个 Pro 版（结构记忆 / 区域记忆 / 时间维度）
 * 
 * 输入：enhancedState（来自 SpatialEnginePro）
 * 输出：结构化 placeStructure + 记忆追踪日志
 */
(function () {
  'use strict';
  
  if (window.MapMemoryPro) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[MapMemoryPro]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[MapMemoryPro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[MapMemoryPro]', msg, payload || '');
  }

  const STATIC_TYPES = ['stairs', 'staircase', 'pillar', 'wall', 'door'];
  const CENTER_ZONE_RATIO = 0.4; // 中央行进区域宽度占整宽比例

  /**
   * ZoneStats：区域统计
   */
  class ZoneStats {
    constructor(name) {
      this.name = name;
      this.sampleCount = 0;
      this.staticHazards = 0;
      this.dynamicObjects = 0;
      this.avgWidthM = null;
    }

    addSample(sample) {
      this.sampleCount += 1;
      if (sample.isStaticHazard) this.staticHazards += 1;
      if (sample.isDynamic) this.dynamicObjects += 1;
      if (typeof sample.localWidthM === 'number') {
        if (this.avgWidthM == null) this.avgWidthM = sample.localWidthM;
        else this.avgWidthM = this.avgWidthM * 0.9 + sample.localWidthM * 0.1;
      }
    }
  }

  /**
   * PlaceStructure：地点结构（Pro 版）
   */
  class PlaceStructure {
    constructor(placeId) {
      this.placeId = placeId;
      this.lastUpdateTs = Date.now();
      this.sceneTypes = {};
      this.corridorWidthM = null;
      this.leftWallStable = false;
      this.rightWallStable = false;
      this.leftSideStaticCount = 0;
      this.rightSideStaticCount = 0;
      this.centerZone = new ZoneStats('center');
      this.leftZone = new ZoneStats('left');
      this.rightZone = new ZoneStats('right');
    }

    updateFromEnhancedState(enhancedState) {
      this.lastUpdateTs = Date.now();
      const st = enhancedState.scene_type || 'unknown';
      this.sceneTypes[st] = (this.sceneTypes[st] || 0) + 1;

      const grid = enhancedState.grid;
      const widthM = grid && typeof grid.width_m === 'number' ? grid.width_m : 4.0;

      const objects = enhancedState.objects || [];
      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = typeof bev.x === 'number' ? bev.x : null;
        const y = typeof bev.y === 'number' ? bev.y : null;
        if (x === null || y === null) continue;

        const type = (obj.type || obj.label || '').toLowerCase();
        const isStaticLike = STATIC_TYPES.some(t => type.indexOf(t) !== -1);
        const isStaticHazard = !!(obj.memory && obj.memory.is_static_hazard);
        const isDynamic =
          obj.pro_motion === 'approaching' ||
          obj.pro_motion === 'approaching_fast' ||
          obj.pro_motion === 'leaving' ||
          obj.pro_motion === 'leaving_fast' ||
          obj.pro_motion === 'crossing';

        const isLeft = x < 0;
        const isCenter = Math.abs(x) <= (widthM * CENTER_ZONE_RATIO / 2);

        const localWidth = widthM; // 简化：用当前grid宽作为局部宽度估计

        const sample = {
          isStaticHazard: isStaticHazard || isStaticLike,
          isDynamic: isDynamic,
          localWidthM: localWidth
        };

        if (isCenter) this.centerZone.addSample(sample);
        else if (isLeft) {
          this.leftZone.addSample(sample);
          if (sample.isStaticHazard) this.leftSideStaticCount += 1;
        } else {
          this.rightZone.addSample(sample);
          if (sample.isStaticHazard) this.rightSideStaticCount += 1;
        }
      }

      // 粗略判断走廊宽度
      if (this.centerZone.avgWidthM != null) {
        if (this.corridorWidthM == null) {
          this.corridorWidthM = this.centerZone.avgWidthM;
        } else {
          this.corridorWidthM =
            this.corridorWidthM * 0.9 + this.centerZone.avgWidthM * 0.1;
        }
      }

      // 左右墙稳定判断：静态结构次数达到一定数量
      this.leftWallStable = this.leftSideStaticCount >= 20;
      this.rightWallStable = this.rightSideStaticCount >= 20;
    }

    getSnapshot() {
      return {
        placeId: this.placeId,
        updated_at: this.lastUpdateTs,
        sceneTypes: this.sceneTypes,
        corridorWidthM: this.corridorWidthM,
        leftWallStable: this.leftWallStable,
        rightWallStable: this.rightWallStable,
        centerZone: {
          sampleCount: this.centerZone.sampleCount,
          staticHazards: this.centerZone.staticHazards,
          dynamicObjects: this.centerZone.dynamicObjects,
          avgWidthM: this.centerZone.avgWidthM
        },
        leftZone: {
          sampleCount: this.leftZone.sampleCount,
          staticHazards: this.leftZone.staticHazards,
          dynamicObjects: this.leftZone.dynamicObjects,
          avgWidthM: this.leftZone.avgWidthM
        },
        rightZone: {
          sampleCount: this.rightZone.sampleCount,
          staticHazards: this.rightZone.staticHazards,
          dynamicObjects: this.rightZone.dynamicObjects,
          avgWidthM: this.rightZone.avgWidthM
        }
      };
    }
  }

  /**
   * MapMemoryProClass：地图记忆 Pro 版主类
   */
  class MapMemoryProClass {
    constructor() {
      this.places = {}; // placeId -> PlaceStructure
      this.currentPlaceId = 'session_default';
      this.lastTraceId = 0;
    }

    _allocTraceId() {
      this.lastTraceId += 1;
      return 'mmtrace_' + this.lastTraceId;
    }

    getCurrentPlaceStructure() {
      if (!this.places[this.currentPlaceId]) {
        this.places[this.currentPlaceId] = new PlaceStructure(this.currentPlaceId);
      }
      return this.places[this.currentPlaceId];
    }

    setCurrentPlaceId(placeId) {
      if (!placeId) return;
      this.currentPlaceId = placeId;
      if (!this.places[placeId]) {
        this.places[placeId] = new PlaceStructure(placeId);
        logInfo('MapMemoryPro: new place structure created', { placeId: placeId });
      } else {
        logDebug('MapMemoryPro: switch place structure', { placeId: placeId });
      }
    }

    /**
     * 主入口：由 SpatialEnginePro / EventFlowPro 调用
     * @param {Object} enhancedState
     * @param {Object} context {placeId?: string}
     */
    ingestEnhancedState(enhancedState, context) {
      try {
        if (!enhancedState || !enhancedState.grid) return;
        if (context && context.placeId) {
          this.setCurrentPlaceId(context.placeId);
        }
        const structure = this.getCurrentPlaceStructure();
        const before = structure.getSnapshot();
        structure.updateFromEnhancedState(enhancedState);
        const after = structure.getSnapshot();

        // 如果结构发生显著变化，记录一条 trace 日志
        this._maybeEmitStructureTrace(before, after);
      } catch (e) {
        logError('MapMemoryPro.ingestEnhancedState error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    _maybeEmitStructureTrace(before, after) {
      try {
        let changed = false;
        const diff = {};

        if (before.corridorWidthM !== after.corridorWidthM) {
          changed = true;
          diff.corridorWidthM = {
            before: before.corridorWidthM,
            after: after.corridorWidthM
          };
        }
        if (before.leftWallStable !== after.leftWallStable) {
          changed = true;
          diff.leftWallStable = {
            before: before.leftWallStable,
            after: after.leftWallStable
          };
        }
        if (before.rightWallStable !== after.rightWallStable) {
          changed = true;
          diff.rightWallStable = {
            before: before.rightWallStable,
            after: after.rightWallStable
          };
        }

        if (!changed) return;

        const traceId = this._allocTraceId();
        const payload = {
          traceId: traceId,
          placeId: after.placeId,
          event: 'structure_update',
          diff: diff,
          snapshot: after
        };
        logInfo('MapMemoryPro.structure_update', payload);

        // 若有后台上传模块，也可以在这里调用
        if (window.uploadLunaLog) {
          window.uploadLunaLog('map_memory_structure', payload);
        }
      } catch (e) {
        logError('MapMemoryPro._maybeEmitStructureTrace error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    getCurrentStructureSnapshot() {
      const structure = this.getCurrentPlaceStructure();
      return structure.getSnapshot();
    }
  }

  window.MapMemoryPro = new MapMemoryProClass();

  // 全局调试接口
  window.debugPrintMapMemoryPro = function () {
    if (!window.MapMemoryPro) return null;
    const snapshot = window.MapMemoryPro.getCurrentStructureSnapshot();
    logInfo('MapMemoryPro snapshot', snapshot);
    return snapshot;
  };

  if (window.logInfo) {
    window.logInfo('MapMemoryPro模块加载完成', { module: 'map_memory_pro' });
  } else {
    console.log('✅ MapMemoryPro模块加载完成', { module: 'map_memory_pro' });
  }
})();


    /* END: map_memory_pro.js */
    
    <!-- ===================== -->
    <!-- Luna StructureAnalyzer (结构分析器) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: structure_analyzer.js */
// frontend/structure_analyzer.js
/**
 * StructureAnalyzer / 结构分析器
 * 提取走廊边线、墙、柱子、台阶、坡道、宽度变化
 * 输出结构特征（走廊/开阔/狭窄/出口/弯道）
 */
(function () {
  'use strict';
  
  if (window.StructureAnalyzer) return;

  function logDebug(msg, p) { window.logDebug?.('[StructureAnalyzer] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[StructureAnalyzer] ' + msg, p || {}); }

  /**
   * StructureAnalyzer
   * 输入：enhancedState.pointGrid（BEV 投影点）
   * 输出：结构特征：左右墙、宽度、走廊感、坡度、台阶等
   */
  function StructureAnalyzerClass() {}

  StructureAnalyzerClass.prototype.analyze = function (enhancedState) {
    try {
      if (!enhancedState?.pointGrid) return null;

      const pts = enhancedState.pointGrid;
      const width = enhancedState.grid?.width_m ?? 4.0;

      let leftMin = 999, rightMin = 999;
      let leftHasWall = false, rightHasWall = false;

      let verticalCluster = 0;   // 是否形成"走廊线"
      let centerOpen = 0;

      let hasStair = false;
      let hasSlope = false;

      for (const p of pts) {
        if (p.y < 0.3 || p.y > 5.0) continue;

        // 楼梯识别
        if (p.type?.includes('stair')) hasStair = true;

        // 斜坡（高度变化）
        if (typeof p.slope === 'number' && Math.abs(p.slope) > 0.15)
          hasSlope = true;

        // 左右距中心的偏移
        if (p.x < 0) {
          leftMin = Math.min(leftMin, Math.abs(p.x));
          if (Math.abs(p.x) < 0.3) leftHasWall = true;
        } else {
          rightMin = Math.min(rightMin, Math.abs(p.x));
          if (Math.abs(p.x) < 0.3) rightHasWall = true;
        }

        // 走廊线：沿 y 方向延伸且 x 稳定
        if (Math.abs(p.x) < 0.5) verticalCluster++;
        if (Math.abs(p.x) < 0.3) centerOpen++;
      }

      const corridorScore = verticalCluster / pts.length;
      const isCorridor = corridorScore > 0.25;
      const isNarrow = leftMin + rightMin < 1.2;
      const isWide = leftMin + rightMin > 3.0;

      const result = {
        left_wall: leftHasWall,
        right_wall: rightHasWall,
        left_distance: leftMin,
        right_distance: rightMin,
        corridor_score: corridorScore,
        is_corridor: isCorridor,
        is_narrow: isNarrow,
        is_wide: isWide,
        has_stair: hasStair,
        has_slope: hasSlope
      };

      logDebug('analyze result', result);
      return result;
    } catch (e) {
      logError('Analyze error', e);
      return null;
    }
  };

  window.StructureAnalyzer = new StructureAnalyzerClass();

  if (window.logInfo) {
    window.logInfo('StructureAnalyzer模块加载完成', { module: 'structure_analyzer' });
  } else {
    console.log('✅ StructureAnalyzer模块加载完成', { module: 'structure_analyzer' });
  }
})();


    /* END: structure_analyzer.js */
    </script>

    <!-- ===================== -->
    <!-- Luna TopologyBuilder (拓扑构建器) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: topology_builder.js */
// frontend/topology_builder.js
/**
 * TopologyBuilder / 拓扑构建器
 * 把结构结果抽象成"拓扑点"
 * 输出：front_open / left_blocked / right_open / corridor_width / turn_hint
 */
(function () {
  'use strict';
  
  if (window.TopologyBuilder) return;

  function logDebug(msg, p) { window.logDebug?.('[TopologyBuilder] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[TopologyBuilder] ' + msg, p || {}); }

  function TopologyBuilderClass() {}

  /**
   * 输入：StructureAnalyzer 结果
   * 输出：拓扑结构（左右阻塞、中间是否开阔、是否走廊、是否转弯）
   */
  TopologyBuilderClass.prototype.build = function (structureInfo) {
    try {
      if (!structureInfo) return null;

      const {
        left_wall,
        right_wall,
        left_distance,
        right_distance,
        is_corridor,
        is_narrow,
        is_wide
      } = structureInfo;

      const frontOpen = !is_narrow || (!left_wall && !right_wall);

      const hint =
        is_corridor
          ? 'corridor'
          : is_wide
          ? 'open_area'
          : is_narrow
          ? 'narrow_passage'
          : 'normal';

      const result = {
        left_blocked: left_distance < 0.4,
        right_blocked: right_distance < 0.4,
        front_open: frontOpen,
        space_type: hint,
        width_m: left_distance + right_distance
      };

      logDebug('build result', result);
      return result;
    } catch (e) {
      logError('build error', e);
      return null;
    }
  };

  window.TopologyBuilder = new TopologyBuilderClass();

  if (window.logInfo) {
    window.logInfo('TopologyBuilder模块加载完成', { module: 'topology_builder' });
  } else {
    console.log('✅ TopologyBuilder模块加载完成', { module: 'topology_builder' });
  }
})();


    /* END: topology_builder.js */
    </script>

    <!-- ===================== -->
    <!-- Luna BottleneckDetector (瓶颈检测器) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: bottleneck_detector.js */
// frontend/bottleneck_detector.js
/**
 * BottleneckDetector / 瓶颈检测器
 * 判断是否进入拥挤区、出口通道、狭窄口
 * 输出：bottleneck / wide / narrow / exit
 */
(function () {
  'use strict';
  
  if (window.BottleneckDetector) return;

  function logDebug(msg, p) { window.logDebug?.('[BottleneckDetector] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[BottleneckDetector] ' + msg, p || {}); }

  function BottleneckDetectorClass() {}

  /**
   * 输入：StructureAnalyzer + TopologyBuilder
   * 输出：瓶颈、出口发现
   */
  BottleneckDetectorClass.prototype.detect = function (structureInfo, topologyInfo) {
    try {
      if (!structureInfo || !topologyInfo) return null;

      const isBottleneck =
        structureInfo.is_narrow ||
        (topologyInfo.left_blocked && topologyInfo.right_blocked);

      const isExit =
        structureInfo.is_wide && !topologyInfo.left_blocked && !topologyInfo.right_blocked;

      const result = {
        bottleneck: isBottleneck,
        exit: isExit,
        hint: isBottleneck
          ? 'bottleneck'
          : isExit
          ? 'exit_found'
          : 'normal'
      };

      logDebug('detect result', result);
      return result;
    } catch (e) {
      logError('detect error', e);
      return null;
    }
  };

  window.BottleneckDetector = new BottleneckDetectorClass();

  if (window.logInfo) {
    window.logInfo('BottleneckDetector模块加载完成', { module: 'bottleneck_detector' });
  } else {
    console.log('✅ BottleneckDetector模块加载完成', { module: 'bottleneck_detector' });
  }
})();


    /* END: bottleneck_detector.js */
    </script>
</script>
    <script>
    /* BEGIN: event_flow_pro.js
// frontend/event_flow_pro.js
/**
 * EventFlowPro / 事件流 Pro 版
 * Pro 版事件流：接收 enhancedState，联动导航 / 任务链 / TTS，并把记忆变化、危险判断写入日志
 */
(function () {
  'use strict';
  
  if (window.EventFlowPro) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[EventFlowPro]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[EventFlowPro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[EventFlowPro]', msg, payload || '');
  }

  function emitTask(task) {
    if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
      window.taskChain.enqueue(task);
    } else {
      logDebug('EventFlowPro: taskChain not available, skip enqueue', task);
    }
  }

  // === 保证 NavigationFSM 已初始化 ===
  if (!window.NavigationFSM) {
    console.warn("⚠️ EventFlowPro: NavigationFSM 未初始化 → 自动创建");
    window.NavigationFSM = { initialized: true, state: "IDLE" };
  } else if (!window.NavigationFSM.initialized) {
    window.NavigationFSM.initialized = true;
    window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
    console.log("✅ NavigationFSM 自动初始化完成 (EventFlowPro)");
  }

  const EventFlowPro = {
    /**
     * 主入口：由 SpatialEnginePro 调用
     * @param {Object} enhancedState
     */
    onSpaceStateEnhanced: function (enhancedState) {
      if (!enhancedState) return;

      try {
        logDebug('EventFlowPro.onSpaceStateEnhanced', {
          scene_type: enhancedState.scene_type,
          overall_risk: enhancedState.overall_risk,
          object_count: (enhancedState.objects || []).length
        });

        // 1) 先把 enhancedState 给 MapMemoryPro
        if (window.MapMemoryPro && typeof window.MapMemoryPro.ingestEnhancedState === 'function') {
          window.MapMemoryPro.ingestEnhancedState(enhancedState, {
            placeId: 'session_default'
          });
        }

        // ✅ 1.5) SceneReasoner 场景推理（在 MapMemoryPro 之后、导航之前）
        let sceneContext = null;
        if (window.SceneReasoner && typeof window.SceneReasoner.ingestEnhancedState === 'function') {
          sceneContext = window.SceneReasoner.ingestEnhancedState(enhancedState);
        }

        // ✅ 1.6) StructureAnalyzer + TopologyBuilder + BottleneckDetector 结构推理
        let structureInfo = null;
        let topologyInfo = null;
        let bottleneckInfo = null;
        
        if (window.StructureAnalyzer && typeof window.StructureAnalyzer.analyze === 'function') {
          structureInfo = window.StructureAnalyzer.analyze(enhancedState);
          
          if (structureInfo && window.TopologyBuilder && typeof window.TopologyBuilder.build === 'function') {
            topologyInfo = window.TopologyBuilder.build(structureInfo);
            
            if (topologyInfo && window.BottleneckDetector && typeof window.BottleneckDetector.detect === 'function') {
              bottleneckInfo = window.BottleneckDetector.detect(structureInfo, topologyInfo);
            }
          }
        }

        // ✅ 1.7) PathFeasibility 路径可行性分析（在结构推理之后）
        let pathHints = null;
        if (window.PathFeasibility && typeof window.PathFeasibility.analyze === 'function') {
          const structureSnapshot = window.MapMemoryPro && typeof window.MapMemoryPro.getCurrentStructureSnapshot === 'function' 
            ? window.MapMemoryPro.getCurrentStructureSnapshot() 
            : null;
          pathHints = window.PathFeasibility.analyze(enhancedState, structureSnapshot);
        }

        // ✅ 1.8) ActionGuidance 动作级导航引擎（在获取所有信息之后）
        if (window.ActionGuidance && sceneContext && pathHints) {
          const actions = window.ActionGuidance.deriveActions(
            sceneContext,
            pathHints,
            structureInfo,
            topologyInfo,
            bottleneckInfo
          );
          if (actions && actions.length > 0) {
            window.ActionGuidance.dispatch(actions);
          }
        }

        // 2) 危险判断：如果存在高风险或关键危险对象，走统一任务链
        this._handleHazardAndRisk(enhancedState, sceneContext, pathHints);

        // 3) 导航状态机更新（带路径建议和结构信息）
        this._updateNavigationFSM(enhancedState, sceneContext, pathHints, structureInfo, topologyInfo, bottleneckInfo);

        // 4) Waypoint 进度更新
        this._updateWaypointProgress(enhancedState);

        // 5) AutoRecovery 状态记录
        this._updateAutoRecovery(enhancedState);
      } catch (e) {
        logError('EventFlowPro.onSpaceStateEnhanced error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    },

    _handleHazardAndRisk: function (enhancedState, sceneContext, pathHints) {
      const risk = enhancedState.overall_risk || 'low';
      const hazard = enhancedState.primary_hazard || null;

      // 如果有主危险体，构造统一危险任务
      if (hazard && risk !== 'low') {
        // ✅ 使用 SpatialSemantic 生成危险文本
        let hazardText = '';
        if (window.SpatialSemantic && typeof window.SpatialSemantic.buildHazardText === 'function') {
          hazardText = window.SpatialSemantic.buildHazardText(hazard, enhancedState);
        }

        const hazardTask = {
          type: 'HAZARD_WARNING',
          priority: 'CRITICAL',
          payload: {
            scene_type: enhancedState.scene_type,
            risk_level: risk,
            hazard: hazard,
            enhancedState: enhancedState,
            hazard_text: hazardText  // ✅ 语义化文本
          }
        };
        emitTask(hazardTask);

        // ✅ 优先通过 MemoryAwareVoice，否则回落到 SpeechRhythm
        if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
          window.MemoryAwareVoice.handleTask(hazardTask);
        } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
          window.SpeechRhythm.handleTask(hazardTask);
        }

        logInfo('EventFlowPro: hazard detected', {
          scene_type: enhancedState.scene_type,
          risk_level: risk,
          hazard_type: hazard.type,
          distance: hazard.distance,
          motion: hazard.pro_motion || hazard.motion
        });

        if (window.emotion_event) {
          window.emotion_event('hazard_detected', risk, {
            hazard_type: hazard.type,
            scene_type: enhancedState.scene_type
          });
        }
      } else {
        // 无明显主危险体，但可以根据结构记忆温和提示
        if (window.MapMemoryPro) {
          const structure = window.MapMemoryPro.getCurrentStructureSnapshot();
          if (structure && (structure.leftWallStable || structure.rightWallStable)) {
            logDebug('EventFlowPro: structure context', {
              corridorWidthM: structure.corridorWidthM,
              leftWallStable: structure.leftWallStable,
              rightWallStable: structure.rightWallStable
            });
          }
        }
      }
    },

    _updateNavigationFSM: function (enhancedState, sceneContext, pathHints, structureInfo, topologyInfo, bottleneckInfo) {
      if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
        const eventData = {
          type: 'space_update_enhanced',
          spaceState: enhancedState
        };

        // ✅ 如果有场景上下文，添加到事件中
        if (sceneContext) {
          eventData.sceneContext = sceneContext;
        }

        // ✅ 如果有路径建议，添加到事件中
        if (pathHints) {
          eventData.pathHints = pathHints;
        }

        // ✅ 如果有结构信息，添加到事件中
        if (structureInfo) {
          eventData.structureInfo = structureInfo;
        }
        if (topologyInfo) {
          eventData.topologyInfo = topologyInfo;
        }
        if (bottleneckInfo) {
          eventData.bottleneckInfo = bottleneckInfo;
        }

        window.NavigationFSM.handleEvent(eventData);
      } else {
        logDebug('EventFlowPro: NavigationFSM not available');
      }

      // ✅ 如果有导航提示（场景上下文 + 路径建议），生成 NAV_HINT 任务
      if (sceneContext && pathHints) {
        let navHintText = '';
        if (window.SpatialSemantic && typeof window.SpatialSemantic.buildNavHintText === 'function') {
          navHintText = window.SpatialSemantic.buildNavHintText(sceneContext, pathHints);
        } else if (sceneContext.nav_hints && sceneContext.nav_hints.caution_text) {
          navHintText = sceneContext.nav_hints.caution_text;
        }

        if (navHintText) {
          const navHintTask = {
            type: 'NAV_HINT',
            priority: 'HIGH',
            payload: {
              text: navHintText,
              sceneContext: sceneContext,
              pathHints: pathHints,
              // ✅ 注入结构数据到 taskChain payload
              structureInfo: structureInfo,
              topologyInfo: topologyInfo,
              bottleneck: bottleneckInfo
            }
          };
          emitTask(navHintTask);

          // ✅ 优先通过 MemoryAwareVoice，否则回落到 SpeechRhythm
          if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
            window.MemoryAwareVoice.handleTask(navHintTask);
          } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
            window.SpeechRhythm.handleTask(navHintTask);
          }
        }
      }

      // ✅ 将结构数据写入 logger 发送到后台
      if (structureInfo || topologyInfo || bottleneckInfo) {
        const structureLog = {
          ts: Date.now(),
          structureInfo: structureInfo,
          topologyInfo: topologyInfo,
          bottleneckInfo: bottleneckInfo
        };

        logInfo('EventFlowPro: structure analysis', structureLog);

        // 如果有后台日志上传接口，上传结构数据
        if (window.uploadLunaLog && typeof window.uploadLunaLog === 'function') {
          window.uploadLunaLog('structure_analysis', structureLog);
        }
      }
    },

    _updateWaypointProgress: function (enhancedState) {
      if (window.WaypointManager && typeof window.WaypointManager.checkProgress === 'function') {
        window.WaypointManager.checkProgress({
          spaceState: enhancedState
        });
      } else {
        logDebug('EventFlowPro: WaypointManager not available');
      }
    },

    _updateAutoRecovery: function (enhancedState) {
      if (!window.AutoRecovery || typeof window.AutoRecovery.record !== 'function') return;

      const risk = enhancedState.overall_risk || 'low';
      let label = 'stable';
      if (risk === 'medium') label = 'elevated_risk';
      else if (risk === 'high' || risk === 'critical') label = 'high_risk';

      window.AutoRecovery.record('navigation_pro', label, {
        scene_type: enhancedState.scene_type,
        overall_risk: risk
      });
    }
  };

  window.EventFlowPro = EventFlowPro;

  if (window.logInfo) {
    window.logInfo('EventFlowPro模块加载完成', { module: 'event_flow_pro' });
  } else {
    console.log('✅ EventFlowPro模块加载完成', { module: 'event_flow_pro' });
  }
})();


    END: event_flow_pro.js */
    <!-- ===================== -->
    <!-- Luna SceneReasoner (Scene Reasoning Engine) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: scene_reasoner.js */
// frontend/scene_reasoner.js
/**
 * Scene Reasoning Engine (SRE) / 场景推理引擎
 * 输入：enhancedState（来自 SpatialEnginePro）
 * 输出：sceneContext（场景推理结果），自动打日志、可被导航/任务链使用
 */
(function () {
  'use strict';
  
  if (window.SceneReasoner) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[SceneReasoner]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[SceneReasoner]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[SceneReasoner]', msg, payload || '');
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function safeGet(obj, path, defVal) {
    try {
      const parts = path.split('.');
      let cur = obj;
      for (let i = 0; i < parts.length; i++) {
        if (!cur) return defVal;
        cur = cur[parts[i]];
      }
      return cur == null ? defVal : cur;
    } catch (e) {
      return defVal;
    }
  }

  // ---- 场景分类器（轻量规则版） ----------------------------------
  class SceneClassifier {
    constructor() {
      this.lastSceneType = 'unknown';
    }

    classify(enhancedState, structureSnapshot) {
      const baseType = enhancedState.scene_type || 'unknown';
      const grid = enhancedState.grid || {};
      const widthM = typeof grid.width_m === 'number' ? grid.width_m : 4.0;
      const objects = enhancedState.objects || [];

      let stairsCount = 0;
      let vehicleCount = 0;
      let chairCount = 0;
      let signCount = 0;

      for (let i = 0; i < objects.length; i++) {
        const t = (objects[i].type || objects[i].label || '').toLowerCase();
        if (t.indexOf('stair') !== -1) stairsCount++;
        if (t.indexOf('car') !== -1 || t.indexOf('bus') !== -1 || t.indexOf('truck') !== -1) vehicleCount++;
        if (t.indexOf('chair') !== -1 || t.indexOf('sofa') !== -1 || t.indexOf('seat') !== -1) chairCount++;
        if (t.indexOf('sign') !== -1 || t.indexOf('board') !== -1 || t.indexOf('panel') !== -1) signCount++;
      }

      const leftWallStable = structureSnapshot && !!structureSnapshot.leftWallStable;
      const rightWallStable = structureSnapshot && !!structureSnapshot.rightWallStable;
      const corridorWidthM = structureSnapshot && structureSnapshot.corridorWidthM;

      let inferred = 'unknown';
      let indoor = false;
      let corridorLike = false;
      let stairZone = false;

      // 1) 优先根据楼梯 + 墙 + 宽度判断"楼梯区 / 走廊"
      if (stairsCount > 0) {
        stairZone = true;
      }

      if ((leftWallStable || rightWallStable) && (corridorWidthM || widthM) <= 4.5) {
        corridorLike = true;
      }

      // 粗分：室内 vs 室外（很简化，但够用）
      // 有大量车辆 & 宽度大 → 街道 / 室外
      if (vehicleCount >= 2 && widthM >= 5.0) {
        indoor = false;
      } else if (chairCount > 0 || signCount > 0 || corridorLike || stairZone) {
        indoor = true;
      } else {
        // fallback：沿用 baseType 的室内/外特征
        indoor = (baseType.indexOf('indoor') !== -1 || baseType.indexOf('corridor') !== -1);
      }

      if (stairZone && corridorLike) {
        inferred = 'indoor_stair_corridor';
      } else if (stairZone && indoor) {
        inferred = 'indoor_stair_area';
      } else if (corridorLike && indoor) {
        inferred = 'indoor_corridor';
      } else if (!indoor && vehicleCount > 0) {
        inferred = 'street_roadside';
      } else if (!indoor && vehicleCount === 0 && widthM < 5.0) {
        inferred = 'street_sidewalk';
      } else if (indoor && widthM >= 6.0 && vehicleCount === 0 && stairsCount === 0) {
        inferred = 'indoor_open_area';
      } else {
        inferred = baseType || 'unknown';
      }

      this.lastSceneType = inferred;
      return {
        base_scene_type: baseType,
        inferred_scene_type: inferred,
        is_indoor: indoor,
        is_corridor_like: corridorLike,
        is_stair_zone: stairZone,
        widthM: corridorWidthM || widthM
      };
    }
  }

  // ---- 拓扑分析：左右区 / 中央区 / 密度 -----------------------------
  class TopologyAnalyzer {
    analyze(enhancedState, structureSnapshot) {
      const grid = enhancedState.grid || {};
      const widthM = typeof grid.width_m === 'number' ? grid.width_m : 4.0;
      const objects = enhancedState.objects || [];
      const pointGrid = enhancedState.pointGrid || [];

      // 分左右 + 中央区
      let leftDyn = 0, centerDyn = 0, rightDyn = 0;
      let leftStaticHaz = 0, centerStaticHaz = 0, rightStaticHaz = 0;
      let dynTotal = 0;

      const centerHalf = widthM * 0.4 / 2; // 中央区域宽度比例

      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = typeof bev.x === 'number' ? bev.x : null;
        if (x === null) continue;

        const isDynamic =
          obj.pro_motion === 'approaching' ||
          obj.pro_motion === 'approaching_fast' ||
          obj.pro_motion === 'leaving' ||
          obj.pro_motion === 'leaving_fast' ||
          obj.pro_motion === 'crossing';

        const isStaticHazard = !!(obj.memory && obj.memory.is_static_hazard);

        let zone = 'center';
        if (Math.abs(x) <= centerHalf) zone = 'center';
        else if (x < 0) zone = 'left';
        else zone = 'right';

        if (isDynamic) {
          dynTotal++;
          if (zone === 'center') centerDyn++;
          else if (zone === 'left') leftDyn++;
          else rightDyn++;
        }

        if (isStaticHazard) {
          if (zone === 'center') centerStaticHaz++;
          else if (zone === 'left') leftStaticHaz++;
          else rightStaticHaz++;
        }
      }

      const forwardPoints = pointGrid.filter(p => typeof p.y === 'number' && p.y > 0 && p.y <= 5.0);
      const crowdDensity = dynTotal / Math.max(forwardPoints.length || 1, 1); // 简单比值

      let preferredSide = 'center';
      // 如果中央动态太多，尽量靠人少的一侧
      if (centerDyn > leftDyn && centerDyn > rightDyn) {
        if (leftDyn <= rightDyn) preferredSide = 'left';
        else preferredSide = 'right';
      } else if (centerDyn === 0 && (leftDyn > 0 || rightDyn > 0)) {
        // 中央无动态，人都在两边
        preferredSide = 'center';
      }

      const staticHazAhead = (centerStaticHaz + leftStaticHaz + rightStaticHaz) > 0;

      return {
        widthM: widthM,
        crowd_density: crowdDensity,  // 0 ~ N
        dynamic_distribution: {
          left: leftDyn,
          center: centerDyn,
          right: rightDyn
        },
        static_hazard_distribution: {
          left: leftStaticHaz,
          center: centerStaticHaz,
          right: rightStaticHaz
        },
        preferred_side: preferredSide,
        has_static_hazard_ahead: staticHazAhead
      };
    }
  }

  // ---- 场景状态机（高层状态：行走 / 转向 / 接近出口/楼梯） ---------
  class SceneStateMachine {
    constructor() {
      this.state = {
        phase: 'idle', // idle / walking / turning / approaching_stairs / at_stairs / crowded
        since: Date.now(),
        lastUpdate: Date.now()
      };
    }

    update(enhancedState, classification, topology) {
      const now = Date.now();
      const oldPhase = this.state.phase;
      const crowd = topology.crowd_density;
      const stairZone = classification.is_stair_zone;

      let newPhase = oldPhase;

      // 简单启发式状态机
      if (crowd > 1.5) {
        newPhase = 'crowded';
      } else if (stairZone) {
        // 有楼梯目标，且风险不是 low → 接近或处于楼梯区域
        const hazard = enhancedState.primary_hazard;
        if (hazard && (hazard.type || '').toLowerCase().indexOf('stair') !== -1) {
          if (hazard.distance != null && hazard.distance < 1.5) {
            newPhase = 'at_stairs';
          } else {
            newPhase = 'approaching_stairs';
          }
        } else {
          newPhase = 'approaching_stairs';
        }
      } else {
        // 非楼梯、非高人群
        // 看一下 dynamic object 的接近速度，粗略判断是否在行走中
        const objs = enhancedState.objects || [];
        let maxApproach = 0;
        for (let i = 0; i < objs.length; i++) {
          const ap = objs[i].pro_approach_speed || 0;
          if (ap > maxApproach) maxApproach = ap;
        }
        if (maxApproach > 0.05) {
          newPhase = 'walking';
        } else if (crowd > 0.2) {
          newPhase = 'walking';
        } else {
          newPhase = 'idle';
        }
      }

      if (newPhase !== oldPhase) {
        this.state.phase = newPhase;
        this.state.since = now;
        logInfo('SceneStateMachine: phase changed', {
          from: oldPhase,
          to: newPhase
        });
      }

      this.state.lastUpdate = now;
      return Object.assign({}, this.state);
    }
  }

  // ---- 主 Reasoner ---------------------------------------------------
  class SceneReasonerClass {
    constructor() {
      this.classifier = new SceneClassifier();
      this.topologyAnalyzer = new TopologyAnalyzer();
      this.stateMachine = new SceneStateMachine();
      this.lastContext = null;
    }

    /**
     * 主入口：由 EventFlowPro.onSpaceStateEnhanced 调用
     * @param {Object} enhancedState
     * @returns {Object|null} sceneContext
     */
    ingestEnhancedState(enhancedState) {
      try {
        if (!enhancedState || !enhancedState.grid) return null;

        // 1) 取结构记忆快照（如果有）
        let structureSnapshot = null;
        if (window.MapMemoryPro && typeof window.MapMemoryPro.getCurrentStructureSnapshot === 'function') {
          structureSnapshot = window.MapMemoryPro.getCurrentStructureSnapshot();
        }

        // 2) 场景分类
        const classification = this.classifier.classify(enhancedState, structureSnapshot);

        // 3) 拓扑分析
        const topology = this.topologyAnalyzer.analyze(enhancedState, structureSnapshot);

        // 4) 状态机更新
        const phaseState = this.stateMachine.update(enhancedState, classification, topology);

        // 5) 导出综合场景上下文
        const sceneContext = {
          ts: Date.now(),
          base_scene_type: classification.base_scene_type,
          inferred_scene_type: classification.inferred_scene_type,
          is_indoor: classification.is_indoor,
          is_corridor_like: classification.is_corridor_like,
          is_stair_zone: classification.is_stair_zone,
          widthM: classification.widthM,
          topology: topology,
          phase: phaseState.phase,
          phase_since: phaseState.since,
          // 导航建议：当前是否建议减速 / 哪侧更安全
          nav_hints: this._buildNavHints(enhancedState, classification, topology, phaseState),
          // 可选：结构快照摘要
          structure: structureSnapshot
        };

        this.lastContext = sceneContext;

        logDebug('SceneReasoner.context', {
          inferred_scene_type: sceneContext.inferred_scene_type,
          phase: sceneContext.phase,
          preferred_side: sceneContext.nav_hints.preferred_side,
          should_slow_down: sceneContext.nav_hints.should_slow_down
        });

        // 6) 分发：给导航、任务链、AutoRecovery 等模块使用
        this._dispatchSceneContext(sceneContext);

        return sceneContext;
      } catch (e) {
        logError('SceneReasoner.ingestEnhancedState error', {
          error: e.toString(),
          stack: e.stack
        });
        return null;
      }
    }

    _buildNavHints(enhancedState, classification, topology, phaseState) {
      const risk = enhancedState.overall_risk || 'low';
      const crowd = topology.crowd_density;
      const staticHaz = topology.has_static_hazard_ahead;
      const preferredSide = topology.preferred_side;
      const isStair = classification.is_stair_zone || phaseState.phase === 'approaching_stairs' || phaseState.phase === 'at_stairs';

      let shouldSlowDown = false;
      let cautionText = null;

      if (risk === 'high' || risk === 'critical') {
        shouldSlowDown = true;
        cautionText = '前方存在高风险，请减速并注意脚下。';
      } else if (isStair) {
        shouldSlowDown = true;
        cautionText = '前方是楼梯区域，请注意台阶高度。';
      } else if (crowd > 1.0) {
        shouldSlowDown = true;
        cautionText = '前方人较多，请放慢速度。';
      } else if (staticHaz) {
        shouldSlowDown = true;
        cautionText = '前方存在固定障碍物，请小心通过。';
      }

      return {
        preferred_side: preferredSide,        // 'left' / 'right' / 'center'
        should_slow_down: shouldSlowDown,
        caution_text: cautionText
      };
    }

    _dispatchSceneContext(sceneContext) {
      try {
        // 1) 导航状态机可以直接接收 scene_context
        if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
          window.NavigationFSM.handleEvent({
            type: 'scene_context_update',
            scene: sceneContext
          });
        }

        // 2) 任务链：如果需要减速或特别小心，可以发一个导航提示任务（低优先级）
        if (sceneContext.nav_hints && sceneContext.nav_hints.should_slow_down && sceneContext.nav_hints.caution_text) {
          if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
            window.taskChain.enqueue({
              type: 'NAV_HINT',
              priority: 'MEDIUM',
              payload: {
                scene: {
                  inferred_scene_type: sceneContext.inferred_scene_type,
                  phase: sceneContext.phase
                },
                text: sceneContext.nav_hints.caution_text
              }
            });
          }
        }

        // 3) AutoRecovery 可用场景阶段监控稳定性
        if (window.AutoRecovery && typeof window.AutoRecovery.record === 'function') {
          window.AutoRecovery.record('scene_phase', sceneContext.phase, {
            inferred_scene_type: sceneContext.inferred_scene_type,
            should_slow_down: sceneContext.nav_hints.should_slow_down
          });
        }

        // 4) 如有 emotion_event，可以记录"环境状态"对情绪的影响（预留）
        if (window.emotion_event) {
          const sev = sceneContext.nav_hints.should_slow_down ? 'elevated' : 'normal';
          window.emotion_event('scene_update', sev, {
            inferred_scene_type: sceneContext.inferred_scene_type,
            phase: sceneContext.phase
          });
        }

        // 5) 如有后台日志上传，可上传结构化场景信息
        if (window.uploadLunaLog) {
          window.uploadLunaLog('scene_context', sceneContext);
        }
      } catch (e) {
        logError('SceneReasoner._dispatchSceneContext error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    getLastContext() {
      return this.lastContext;
    }
  }

  window.SceneReasoner = new SceneReasonerClass();

  // 全局调试函数
  window.debugSceneContext = function () {
    if (!window.SceneReasoner) return null;
    const ctx = window.SceneReasoner.getLastContext();
    logInfo('SceneReasoner lastContext', ctx);
    return ctx;
  };

  if (window.logInfo) {
    window.logInfo('SceneReasoner模块加载完成', { module: 'scene_reasoner' });
  } else {
    console.log('✅ SceneReasoner模块加载完成', { module: 'scene_reasoner' });
  }
})();


    /* END: scene_reasoner.js */
    <!-- ===================== -->
    <!-- Luna SpatialSemantic (空间语义化) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: spatial_semantic.js */
// frontend/spatial_semantic.js
/**
 * SpatialSemantic / 空间语义化
 * 把"位置 + 当下环境"转成中文句子
 */
(function () {
  'use strict';
  
  if (window.SpatialSemantic) return;

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug('[SpatialSemantic] ' + msg, payload || {});
    else console.debug('[SpatialSemantic]', msg, payload || {});
  }

  function logError(msg, payload) {
    if (window.logError) window.logError('[SpatialSemantic] ' + msg, payload || {});
    else console.error('[SpatialSemantic]', msg, payload || {});
  }

  function describeDirection(bearingDeg, bevX) {
    if (typeof bearingDeg !== 'number') {
      if (typeof bevX === 'number') {
        if (bevX < -0.5) return '左侧';
        if (bevX > 0.5) return '右侧';
      }
      return '前方';
    }

    let a = ((bearingDeg % 360) + 360) % 360;
    if (a > 180) a -= 360;

    if (a > -20 && a <= 20) return '正前方';
    if (a > 20 && a <= 70) return '右前方';
    if (a > 70 && a <= 140) return '右侧';
    if (a <= -20 && a > -70) return '左前方';
    if (a <= -70 && a > -140) return '左侧';
    return '前方';
  }

  function describeDistance(d) {
    if (typeof d !== 'number') return '';
    if (d < 0.7) return '就在身边';
    if (d < 1.5) return '一米左右';
    if (d < 3.0) return '两三米';
    if (d < 6.0) return '几米之外';
    return '稍远处';
  }

  function normalizeTypeLabel(t) {
    if (!t) return '障碍物';
    const s = String(t).toLowerCase();
    if (s.includes('stair') || s.includes('steps')) return '台阶';
    if (s.includes('person') || s.includes('human')) return '行人';
    if (s.includes('car') || s.includes('truck') || s.includes('bus')) return '车辆';
    if (s.includes('door')) return '门口';
    if (s.includes('elevator')) return '电梯';
    if (s.includes('bike')) return '自行车';
    return '障碍物';
  }

  function riskPrefix(level) {
    if (level === 'critical') return '危险！';
    if (level === 'high') return '注意，前方有风险，';
    if (level === 'medium') return '请注意，';
    return '';
  }

  window.SpatialSemantic = {
    buildHazardText(hazard, enhancedState) {
      try {
        if (!hazard) return '';

        const distance = hazard.distance ?? hazard.pro_distance;
        const bearing = hazard.bearing;
        const bevX = hazard.bev?.x;

        const dirText = describeDirection(bearing, bevX);
        const distText = describeDistance(distance);
        const typeText = normalizeTypeLabel(hazard.type || hazard.label);
        const risk = enhancedState?.overall_risk || hazard.risk_level || 'medium';

        return `${riskPrefix(risk)}${dirText}${distText}有${typeText}`;
      } catch (e) {
        logError('buildHazardText error', { e });
        return '';
      }
    },

    buildNavHintText(sceneCtx, pathHints) {
      try {
        if (!sceneCtx && !pathHints) return '';

        let txt = '';
        const side = pathHints?.best_side;
        const slow = pathHints?.bottleneck || sceneCtx?.topology?.crowd_density > 1.5;

        if (side === 'left') txt += '请稍微向左侧行走，避开右侧人群。';
        else if (side === 'right') txt += '请稍微向右侧行走，避开左侧人群。';

        if (slow) txt += ' 前方环境复杂，请放慢速度。';

        return txt;
      } catch (e) {
        logError('buildNavHintText error', { e });
        return '';
      }
    },

    buildSceneOverviewText(sceneCtx) {
      try {
        if (!sceneCtx) return '';

        const t = sceneCtx.inferred_scene_type || '';
        const crowd = sceneCtx.topology?.crowd_density;

        let txt = '';

        if (t.includes('stair')) txt += '当前处在楼梯附近。';
        else if (t.includes('corridor')) txt += '当前在走廊中。';
        else if (t.includes('street')) txt += '当前在街道上。';

        if (crowd > 1.5) txt += ' 前方人较多。';

        return txt;
      } catch (e) {
        logError('buildSceneOverviewText error', { e });
        return '';
      }
    }
  };

  if (window.logInfo) {
    window.logInfo('SpatialSemantic模块加载完成', { module: 'spatial_semantic' });
  } else {
    console.log('✅ SpatialSemantic模块加载完成', { module: 'spatial_semantic' });
  }
})();


    /* END: spatial_semantic.js */
    </script>

    <!-- ===================== -->
    <!-- Luna SpeechRhythm (语音播报节奏管理) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: speech_rhythm.js */
// frontend/speech_rhythm.js
/**
 * SpeechRhythm / 语音播报节奏管理
 * 节流、去骚扰、优先级、连续播报
 */
(function () {
  'use strict';
  
  if (window.SpeechRhythm) return;

  function logInfo(m, p) { window.logInfo?.('[SpeechRhythm] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[SpeechRhythm] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[SpeechRhythm] ' + m, p ?? {}); }

  const PRIORITY = { CRITICAL: 3, HIGH: 2, MEDIUM: 1, LOW: 0 };
  const now = () => Date.now();

  function sortQueue(q) {
    q.sort((a, b) => {
      const pa = PRIORITY[a.priority] ?? 0;
      const pb = PRIORITY[b.priority] ?? 0;
      if (pa !== pb) return pb - pa;
      return a.ts - b.ts;
    });
  }

  function Rhythm() {
    this.queue = [];
    this.lastTs = 0;
    this.minInterval = 1200;
    this.isSpeaking = false;
    this.timer = null;
    this.userMute = false;
  }

  Rhythm.prototype._ensureTimer = function () {
    if (this.timer) return;
    this.timer = setInterval(() => this._tick(), 300);
  };

  Rhythm.prototype._tick = function () {
    if (!this.queue.length) return;
    if (this.isSpeaking) return;
    if (now() - this.lastTs < this.minInterval) return;
    if (this.userMute) return;

    sortQueue(this.queue);
    const task = this.queue.shift();
    if (!task) return;

    this._speak(task);
  };

  Rhythm.prototype._speak = function (task) {
    this.isSpeaking = true;
    this.lastTs = now();

    logInfo('speak', task);

    try {
      if (window.PriorityTTSQueue?.enqueue) {
        window.PriorityTTSQueue.enqueue({
          text: task.text,
          priority: task.priority,
          category: task.category,
          onFinish: () => (this.isSpeaking = false),
          onError: () => (this.isSpeaking = false)
        });
        return;
      }

      if (window.speakText) {
        window.speakText(task.text);
        this.isSpeaking = false;
        return;
      }
    } catch (err) {
      logError('TTS error', err);
    }
    this.isSpeaking = false;
  };

  Rhythm.prototype.enqueueSpeech = function (o) {
    if (!o?.text) return;

    this.queue.push({
      text: o.text,
      category: o.category || 'info',
      priority: o.priority || 'MEDIUM',
      meta: o.meta || {},
      ts: now()
    });

    this._ensureTimer();
  };

  Rhythm.prototype.handleTask = function (task) {
    if (!task?.type) return;

    if (task.type === 'HAZARD_WARNING') {
      const text =
        task.payload?.hazard_text ||
        window.SpatialSemantic?.buildHazardText(task.payload?.hazard, task.payload?.enhancedState);

      if (!text) return;

      this.enqueueSpeech({
        text,
        category: 'hazard',
        priority: 'CRITICAL'
      });
      return;
    }

    if (task.type === 'NAV_HINT') {
      if (task.payload?.text)
        this.enqueueSpeech({
          text: task.payload.text,
          category: 'nav',
          priority: 'HIGH'
        });
      return;
    }

    if (task.type === 'INFO_TTS') {
      if (task.payload?.text)
        this.enqueueSpeech({
          text: task.payload.text,
          category: 'info',
          priority: 'LOW'
        });
    }
  };

  window.SpeechRhythm = new Rhythm();

  if (window.logInfo) {
    window.logInfo('SpeechRhythm模块加载完成', { module: 'speech_rhythm' });
  } else {
    console.log('✅ SpeechRhythm模块加载完成', { module: 'speech_rhythm' });
  }
})();


    /* END: speech_rhythm.js */
    </script>
    
    <!-- ===================== -->
    <!-- Luna D Series: Navigation FSM + Audio Pipeline + Danger Engine -->
    <!-- ===================== -->
    <script>
    /* BEGIN: de_navigation_audio.js */
// frontend/de_navigation_audio.js
// D 系列：导航 FSM + 播报链 + 危险打断/恢复
// 说明：全部挂在 window 上，不破坏现有代码，如果已有同名对象则跳过。

(function () {
  'use strict';
  
  // 避免重复加载
  if (window.NavigationFSM && window.AudioPipeline && window.DangerEnginePro) {
    return;
  }

  // 简单日志封装（优先走 LunaLogger）
  function log(level, msg, details) {
    try {
      if (window.LunaLogger && window.LunaLogger[level]) {
        window.LunaLogger[level](msg, details || {});
      } else {
        const tag = `[${level.toUpperCase()}][DE]`;
        if (level === 'error') console.error(tag, msg, details || {});
        else if (level === 'warn') console.warn(tag, msg, details || {});
        else console.log(tag, msg, details || {});
      }
    } catch (e) {
      console.log('[DE][log-fallback]', msg, details || {}, e);
    }
  }

  // =========================
  // D1. AudioPipeline 语音播报管线
  // =========================
  if (!window.AudioPipeline) {
    function AudioPipelineClass() {
      this.queue = [];
      this.playing = false;
      this.currentTaskId = null;
      this.defaultVoice = 'default';
      this.fallbackSpeakFn = window.speakText || window.speakTextSmart || null;
    }

    // 入队：text 必填，priority 越小优先级越高（0=critical）
    AudioPipelineClass.prototype.enqueue = function (opts) {
      const task = {
        id: opts.id || ('tts-' + Date.now() + '-' + Math.random().toString(16).slice(2)),
        text: opts.text,
        priority: typeof opts.priority === 'number' ? opts.priority : 5,
        category: opts.category || 'nav', // nav / danger / info / system
        meta: opts.meta || {},
        onDone: typeof opts.onDone === 'function' ? opts.onDone : null,
      };
      if (!task.text) return;

      this.queue.push(task);
      // 简单优先级排序
      this.queue.sort((a, b) => a.priority - b.priority);

      log('debug', 'AudioPipeline enqueue', { len: this.queue.length, task });
      this._drain();
    };

    AudioPipelineClass.prototype._drain = function () {
      if (this.playing) return;
      if (!this.queue.length) return;

      const task = this.queue.shift();
      this.playing = true;
      this.currentTaskId = task.id;

      log('info', 'AudioPipeline play', {
        id: task.id,
        category: task.category,
        text: task.text,
      });

      // 优先使用 SpeechRhythm（如果存在）
      if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        try {
          window.SpeechRhythm.handleTask({
            type: 'TTS',
            payload: {
              text: task.text,
              category: task.category,
              meta: task.meta,
              onDone: () => this._finish(task),
            },
          });
          // 注意：如果 SpeechRhythm 内部没有调用 onDone，我们需要兜底
          this._fallbackTimeout(task);
          return;
        } catch (e) {
          log('error', 'SpeechRhythm handleTask error', { e });
        }
      }

      // 然后尝试 PriorityTTSQueue（如果存在）
      if (window.PriorityTTSQueue && typeof window.PriorityTTSQueue.enqueue === 'function') {
        try {
          window.PriorityTTSQueue.enqueue({
            text: task.text,
            priority: task.priority,
            onFinish: () => this._finish(task),
          });
          this._fallbackTimeout(task);
          return;
        } catch (e) {
          log('error', 'PriorityTTSQueue enqueue error', { e });
        }
      }

      // 最后使用 fallback speak 函数（老逻辑）
      if (this.fallbackSpeakFn) {
        try {
          const maybePromise = this.fallbackSpeakFn(task.text);
          if (maybePromise && typeof maybePromise.then === 'function') {
            maybePromise
              .then(() => this._finish(task))
              .catch((e) => {
                log('error', 'fallbackSpeakFn error', { e });
                this._finish(task);
              });
          } else {
            // 没有 promise，则设置一个大致时长
            this._fallbackTimeout(task, Math.max(1500, task.text.length * 80));
          }
          return;
        } catch (e) {
          log('error', 'fallbackSpeakFn call error', { e });
        }
      }

      // 如果什么都没有，直接结束
      this._finish(task);
    };

    AudioPipelineClass.prototype._fallbackTimeout = function (task, ms) {
      const timeout = typeof ms === 'number' ? ms : Math.max(2000, task.text.length * 80);
      const id = task.id;
      setTimeout(() => {
        if (this.currentTaskId === id) {
          log('warn', 'AudioPipeline timeout fallback', { id, timeout });
          this._finish(task);
        }
      }, timeout);
    };

    AudioPipelineClass.prototype._finish = function (task) {
      this.playing = false;
      this.currentTaskId = null;
      try {
        if (task.onDone) task.onDone();
      } catch (e) {
        log('error', 'AudioPipeline onDone error', { e });
      }
      this._drain();
    };

    window.AudioPipeline = new AudioPipelineClass();
  }

  // =========================
  // D2. Navigation FSM 导航状态机
  // =========================
  if (!window.NavigationFSM) {
    const NAV_STATE = {
      IDLE: 'IDLE',
      PREPARING: 'PREPARING',
      NAVIGATING: 'NAVIGATING',
      PAUSED: 'PAUSED',
      ARRIVED: 'ARRIVED',
      ERROR: 'ERROR',
    };

    function NavigationFSMClass() {
      this.state = NAV_STATE.IDLE;
      this.currentRoute = null; // { goalId, waypoints, currentIndex }
      this.lastUpdateTs = 0;
      this.hazardPaused = false;
      this.initialized = true;  // ✅ 标记为已初始化
    }

    NavigationFSMClass.prototype._setState = function (nextState, meta) {
      if (this.state === nextState) return;
      const prev = this.state;
      this.state = nextState;
      this.lastUpdateTs = Date.now();

      log('info', 'NavigationFSM state change', { from: prev, to: nextState, meta: meta || {} });

      // 对外发事件（给 taskChain / 其他模块）
      try {
        if (window.taskChain && window.taskChain.enqueue) {
          window.taskChain.enqueue({
            type: 'NAV_FSM_EVENT',
            priority: 'HIGH',
            payload: {
              from: prev,
              to: nextState,
              meta: meta || {},
              ts: this.lastUpdateTs,
            },
          });
        }
      } catch (e) {
        log('error', 'NavigationFSM emit NAV_FSM_EVENT error', { e });
      }
    };

    NavigationFSMClass.prototype.startNavigation = function (route) {
      if (!route || !Array.isArray(route.waypoints) || !route.waypoints.length) {
        log('warn', 'startNavigation invalid route', { route });
        this._setState(NAV_STATE.ERROR, { reason: 'invalid_route' });
        return;
      }

      this.currentRoute = {
        goalId: route.goalId || route.goal_id || 'unknown',
        waypoints: route.waypoints,
        currentIndex: 0,
      };
      this.hazardPaused = false;

      this._setState(NAV_STATE.PREPARING, { route: this.currentRoute });

      // 起始播报
      const text =
        route.startText ||
        '导航已启动，我会根据前方环境和路线，提醒你安全前进。';

      window.AudioPipeline.enqueue({
        text,
        priority: 2,
        category: 'nav',
        meta: { phase: 'nav_start' },
        onDone: () => {
          this._setState(NAV_STATE.NAVIGATING, {});
          this._speakNextWaypoint();
        },
      });
    };

    NavigationFSMClass.prototype._speakNextWaypoint = function () {
      if (!this.currentRoute) return;

      const idx = this.currentRoute.currentIndex;
      const wp = this.currentRoute.waypoints[idx];
      if (!wp) return;

      // 文案可以由后端给，也可以简单拼接
      const text =
        wp.text ||
        `接下来，请沿当前方向前进大约 ${wp.distance || '一小段'}，在 ${wp.landmark ||
          '前方'} 位置附近准备 ${wp.action || '转向' }。`;

      window.AudioPipeline.enqueue({
        text,
        priority: 4,
        category: 'nav',
        meta: { phase: 'waypoint', index: idx },
      });
    };

    // 由导航模块 / 后端调用，更新当前进度
    // navInfo 例子：{ goal_id, distance_to_goal_m, reached_waypoint: true, at_goal: false }
    NavigationFSMClass.prototype.updateProgress = function (navInfo) {
      this.lastUpdateTs = Date.now();

      if (!this.currentRoute) return;

      // 到达目标
      if (navInfo && navInfo.at_goal) {
        this._setState(NAV_STATE.ARRIVED, { navInfo });

        window.AudioPipeline.enqueue({
          text: '已经到达目标位置。',
          priority: 1,
          category: 'nav',
          meta: { phase: 'arrived' },
        });
        return;
      }

      // 路径点推进
      if (navInfo && navInfo.reached_waypoint && this.state === NAV_STATE.NAVIGATING) {
        const len = this.currentRoute.waypoints.length;
        if (this.currentRoute.currentIndex < len - 1) {
          this.currentRoute.currentIndex += 1;
          log('info', 'NavigationFSM waypoint advanced', {
            index: this.currentRoute.currentIndex,
            len,
          });
          this._speakNextWaypoint();
        }
      }
    };

    NavigationFSMClass.prototype.pause = function (reason) {
      if (this.state !== NAV_STATE.NAVIGATING) return;
      this._setState(NAV_STATE.PAUSED, { reason: reason || 'manual' });
    };

    NavigationFSMClass.prototype.resume = function () {
      if (this.state !== NAV_STATE.PAUSED) return;
      this._setState(NAV_STATE.NAVIGATING, { reason: 'resume' });
      this._speakNextWaypoint();
    };

    NavigationFSMClass.prototype.stop = function (reason) {
      this._setState(NAV_STATE.IDLE, { reason: reason || 'stop' });
      this.currentRoute = null;
      this.hazardPaused = false;
    };

    // 危险打断：来自 DangerEnginePro
    NavigationFSMClass.prototype.onHazard = function (hazardInfo) {
      if (!hazardInfo) return;

      log('warn', 'NavigationFSM onHazard', hazardInfo);

      if (this.state === NAV_STATE.NAVIGATING) {
        this.hazardPaused = true;
        this._setState(NAV_STATE.PAUSED, { reason: 'hazard', hazard: hazardInfo });
      }

      // 播报危险警告
      const text =
        hazardInfo.text ||
        '前方存在潜在危险，请放慢速度，注意脚下和周围环境。';

      window.AudioPipeline.enqueue({
        text,
        priority: 0, // 最高优先级
        category: 'danger',
        meta: { hazard: hazardInfo },
        onDone: () => {
          // 危险播报结束后尝试恢复导航
          if (this.hazardPaused && this.currentRoute) {
            this.hazardPaused = false;
            this._setState(NAV_STATE.NAVIGATING, { reason: 'hazard_cleared' });
            this._speakNextWaypoint();
          }
        },
      });
    };

    window.NavigationFSM = new NavigationFSMClass();
    // 强制初始化检查
    if (!window.NavigationFSM.initialized) {
      window.NavigationFSM.initialized = true;
      window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
      console.log("✅ NavigationFSM 强制初始化完成 (Instance)");
    }
    
    // ✅ 强制初始化检查
    if (!window.NavigationFSM.initialized) {
      window.NavigationFSM.initialized = true;
      window.NavigationFSM.state = "IDLE";
      console.log('✅ NavigationFSM 强制初始化完成');
    }
  }

  // =========================
  // D3. DangerEnginePro 多帧危险降噪
  // =========================
  if (!window.DangerEnginePro) {
    function DangerEngineProClass() {
      this.history = []; // 最近 N 帧检测
      this.maxFrames = 8;
      this.minStableFrames = 3;
      this.minConfidence = 0.65;
    }

    // detections 结构假设：[{ label, confidence, bbox: { x, y, w, h }, distance_m }]
    DangerEngineProClass.prototype.ingestFrame = function (detections, meta) {
      const ts = Date.now();
      this.history.push({ ts, detections: detections || [], meta: meta || {} });

      if (this.history.length > this.maxFrames) {
        this.history.shift();
      }

      // 输出危险结论
      return this._analyzeDanger();
    };

    DangerEngineProClass.prototype._analyzeDanger = function () {
      if (!this.history.length) return null;

      // 简单合并最近几帧的"高置信度 + 近距离"目标
      const merged = {};

      for (const frame of this.history) {
        for (const det of frame.detections) {
          if (!det || typeof det.confidence !== 'number') continue;
          if (det.confidence < this.minConfidence) continue;

          const key = det.label || 'unknown';
          if (!merged[key]) {
            merged[key] = { count: 0, closest: Infinity, last: det };
          }

          merged[key].count += 1;
          const d = typeof det.distance_m === 'number' ? det.distance_m : 999;
          if (d < merged[key].closest) merged[key].closest = d;
          merged[key].last = det;
        }
      }

      let best = null;
      for (const [label, info] of Object.entries(merged)) {
        if (info.count >= this.minStableFrames && info.closest < 2.0) {
          // 前方 2m 内且持续出现
          best = {
            label,
            frames: info.count,
            nearest_distance_m: info.closest,
            raw: info.last,
          };
          break;
        }
      }

      if (!best) return null;

      // 生成文案
      let text = '前方有障碍物，请放慢速度。';
      if (best.label === 'person') {
        text = '前方有人，请注意避让，放慢脚步。';
      } else if (best.label === 'bicycle' || best.label === 'bike') {
        text = '前方有自行车或障碍物，请稍微靠一侧行走。';
      } else if (best.label === 'stairs' || best.label === 'stair') {
        text = '前方疑似是楼梯区域，请放慢速度，注意台阶。';
      }

      const hazardInfo = {
        type: 'obstacle',
        label: best.label,
        distance_m: best.nearest_distance_m,
        frames: best.frames,
        text,
      };

      log('warn', 'DangerEnginePro hazard detected', hazardInfo);
      return hazardInfo;
    };

    window.DangerEnginePro = new DangerEngineProClass();
  }

  log('info', 'DE Navigation+Audio module initialized', {});
})();


    /* END: de_navigation_audio.js */
    </script>
    <!-- ===================== -->
    <!-- Luna ActionGuidance (动作级导航引擎) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: action_guidance.js */
// frontend/action_guidance.js
/**
 * ActionGuidance / 动作级导航引擎
 * 负责把"场景 + 通行性"转换为动作建议：adjust_left / adjust_right / keep_center / slow_down / stop 等
 */
(function () {
  'use strict';
  
  if (window.ActionGuidance) return;

  function logInfo(m, p) { window.logInfo?.('[ActionGuidance] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[ActionGuidance] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[ActionGuidance] ' + m, p ?? {}); }

  /**
   * ActionGuidance
   * 负责把"场景 + 通行性"转换为 动作建议：
   * adjust_left / adjust_right / keep_center / slow_down / stop 等。
   */
  function ActionGuidanceClass() {
    this.lastAction = null;
    this.lastActionTs = 0;
    this.cooldownMs = 1500; // 相同动作的最小间隔
  }

  ActionGuidanceClass.prototype._canEmitSameAction = function (code) {
    if (!this.lastAction || this.lastAction !== code) return true;
    const now = Date.now();
    return now - this.lastActionTs > this.cooldownMs;
  };

  ActionGuidanceClass.prototype._recordAction = function (code) {
    this.lastAction = code;
    this.lastActionTs = Date.now();
  };

  /**
   * 主入口：
   * @param {Object} sceneCtx  SceneReasoner.getLastContext()
   * @param {Object} pathHints PathFeasibility.analyze(...)
   * @param {Object} structInfo StructureAnalyzer.analyze(...)
   * @param {Object} topoInfo TopologyBuilder.build(...)
   * @param {Object} bottleInfo BottleneckDetector.detect(...)
   * @returns {Array<{code, urgency, text}>}
   */
  ActionGuidanceClass.prototype.deriveActions = function (
    sceneCtx,
    pathHints,
    structInfo,
    topoInfo,
    bottleInfo
  ) {
    try {
      const actions = [];

      if (!sceneCtx || !pathHints) return actions;

      const phase = sceneCtx.phase || 'idle';
      const navHints = sceneCtx.nav_hints || {};
      const bestSide = pathHints.best_side || navHints.preferred_side || 'center';
      const bottleneck = pathHints.bottleneck || bottleInfo?.bottleneck;
      const exitFound = bottleInfo?.exit;

      // 1) 狭窄 / 瓶颈 → 减速 + 微调
      if (bottleneck) {
        actions.push({
          code: 'slow_down',
          urgency: 'high',
          text: '前方通道较窄，请放慢速度，小心通过。'
        });
      }

      // 2) 侧向微调
      if (bestSide === 'left') {
        actions.push({
          code: 'adjust_left',
          urgency: 'medium',
          text: '请稍微向左侧偏一点，避开右侧障碍。'
        });
      } else if (bestSide === 'right') {
        actions.push({
          code: 'adjust_right',
          urgency: 'medium',
          text: '请稍微向右侧偏一点，避开左侧障碍。'
        });
      } else {
        // center：不强制说话，除非真需要
      }

      // 3) 楼梯场景
      if (sceneCtx.is_stair_zone || phase === 'approaching_stairs' || phase === 'at_stairs') {
        if (phase === 'approaching_stairs') {
          actions.push({
            code: 'prep_stairs',
            urgency: 'high',
            text: '前方是楼梯区域，请放慢脚步，注意台阶。'
          });
        } else if (phase === 'at_stairs') {
          actions.push({
            code: 'on_stairs',
            urgency: 'high',
            text: '已经到达楼梯位置，请慢慢行走，注意脚下。'
          });
        }
      }

      // 4) 出口提示
      if (exitFound) {
        actions.push({
          code: 'near_exit',
          urgency: 'low',
          text: '前方空间变宽，这是一个出口区域。'
        });
      }

      // 5) 拥挤场景
      const crowd = sceneCtx.topology?.crowd_density;
      if (typeof crowd === 'number' && crowd > 1.5) {
        actions.push({
          code: 'crowded',
          urgency: 'high',
          text: '前方行人较多，请放慢速度，注意避让。'
        });
      }

      // 动作去重 + 冷却
      const filtered = [];
      for (const a of actions) {
        if (!this._canEmitSameAction(a.code)) continue;
        this._recordAction(a.code);
        filtered.push(a);
      }

      logDebug('deriveActions', {
        phase,
        bestSide,
        bottleneck,
        exitFound,
        crowd,
        actions: filtered
      });

      return filtered;
    } catch (e) {
      logError('deriveActions error', { e });
      return [];
    }
  };

  /**
   * 把动作转成 NAV_HINT 任务并交给 SpeechRhythm
   */
  ActionGuidanceClass.prototype.dispatch = function (actions) {
    if (!actions || !actions.length) return;

    for (const a of actions) {
      const task = {
        type: 'NAV_HINT',
        payload: { text: a.text, code: a.code, urgency: a.urgency || 'medium' }
      };

      // ✅ 优先通过 MemoryAwareVoice
      if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
        window.MemoryAwareVoice.handleTask(task);
      } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        window.SpeechRhythm.handleTask(task);
      }
    }
  };

  window.ActionGuidance = new ActionGuidanceClass();

  if (window.logInfo) {
    window.logInfo('ActionGuidance模块加载完成', { module: 'action_guidance' });
  } else {
    console.log('✅ ActionGuidance模块加载完成', { module: 'action_guidance' });
  }
})();


    /* END: action_guidance.js */
    </script>

    <!-- ===================== -->
    <!-- Luna MemoryAwareVoice (记忆敏感语音引擎) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: memory_aware_voice.js */
// frontend/memory_aware_voice.js
/**
 * MemoryAwareVoice / 记忆敏感语音引擎
 * 解决："同一个地方的同一条提醒，不要一直重复说"
 * 结合 MapMemoryPro 的结构记忆做语音抑制 / 降频
 */
(function () {
  'use strict';
  
  if (window.MemoryAwareVoice) return;

  function logInfo(m, p) { window.logInfo?.('[MemoryAwareVoice] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[MemoryAwareVoice] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[MemoryAwareVoice] ' + m, p ?? {}); }

  function MemoryAwareVoiceClass() {
    this.lastByKey = {}; // key -> { ts, count }
    this.cooldownMs = 8000; // 同一类提示 8 秒内不重复
  }

  MemoryAwareVoiceClass.prototype._makeKey = function (task) {
    try {
      if (!task?.type) return null;
      const type = task.type;
      const text = task.payload?.text || '';
      const sceneType = task.payload?.scene_type || '';
      const code = task.payload?.code || '';

      // 粗略 hash
      return `${type}|${code}|${sceneType}|${text.slice(0, 20)}`;
    } catch (e) {
      logError('_makeKey error', { e });
      return null;
    }
  };

  MemoryAwareVoiceClass.prototype._shouldSuppress = function (key) {
    if (!key) return false;
    const info = this.lastByKey[key];
    if (!info) return false;

    const now = Date.now();
    if (now - info.ts < this.cooldownMs) return true;
    return false;
  };

  MemoryAwareVoiceClass.prototype._record = function (key) {
    if (!key) return;
    const now = Date.now();
    const old = this.lastByKey[key];
    this.lastByKey[key] = {
      ts: now,
      count: old ? old.count + 1 : 1
    };
  };

  /**
   * 包装一个任务，决定是否让它继续进入 SpeechRhythm
   */
  MemoryAwareVoiceClass.prototype.handleTask = function (task) {
    try {
      const key = this._makeKey(task);
      if (this._shouldSuppress(key)) {
        logDebug('suppress repeated task', { key, task });
        return; // 丢弃
      }

      this._record(key);

      // 继续丢给 SpeechRhythm
      if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        window.SpeechRhythm.handleTask(task);
      } else {
        logDebug('SpeechRhythm not ready, skip', {});
      }
    } catch (e) {
      logError('handleTask error', { e });
    }
  };

  window.MemoryAwareVoice = new MemoryAwareVoiceClass();

  // 一个便捷函数：对外统一入口
  window.enqueueNavHintWithMemory = function (text, extra) {
    const task = {
      type: 'NAV_HINT',
      payload: Object.assign({ text }, extra || {})
    };
    window.MemoryAwareVoice.handleTask(task);
  };

  if (window.logInfo) {
    window.logInfo('MemoryAwareVoice模块加载完成', { module: 'memory_aware_voice' });
  } else {
    console.log('✅ MemoryAwareVoice模块加载完成', { module: 'memory_aware_voice' });
  }
})();


    /* END: memory_aware_voice.js */
    </script>

    <!-- ===================== -->
    <!-- Luna GoalAwareness (目标距离 × 阶段播报引擎) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: goal_awareness.js */
// frontend/goal_awareness.js
/**
 * GoalAwareness / 目标距离 × 阶段播报引擎
 * 用于："距离目标还有 50 米 / 20 米 / 5 米 / 已到达"
 * 支持楼层/建筑/科室多阶段
 * 不依赖地图细节，由后端传入高层导航状态
 */
(function () {
  'use strict';
  
  if (window.GoalAwareness) return;

  function logInfo(m, p) { window.logInfo?.('[GoalAwareness] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[GoalAwareness] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[GoalAwareness] ' + m, p ?? {}); }

  const DIST_MILESTONES = [50, 30, 20, 10, 5]; // 米
  const STAGES = [
    'outdoor_to_building',
    'in_building',
    'in_elevator',
    'on_floor',
    'at_goal'
  ];

  function GoalAwarenessClass() {
    this.currentGoalId = null;
    this.lastMilestoneIndex = null;
    this.stageAnnounced = {};
  }

  GoalAwarenessClass.prototype._resetForGoal = function (goalId) {
    this.currentGoalId = goalId;
    this.lastMilestoneIndex = null;
    this.stageAnnounced = {};
  };

  GoalAwarenessClass.prototype._pickMilestoneIndex = function (dist) {
    for (let i = 0; i < DIST_MILESTONES.length; i++) {
      if (dist <= DIST_MILESTONES[i]) return i;
    }
    return null;
  };

  GoalAwarenessClass.prototype._buildDistText = function (dist) {
    if (dist <= 3) return '马上就要到了。';
    if (dist <= 5) return '还有五米左右。';
    if (dist <= 10) return '还有十米左右。';
    if (dist <= 20) return '还有二十米左右。';
    if (dist <= 50) return '还有五十米左右。';
    return '';
  };

  GoalAwarenessClass.prototype._buildStageText = function (stage) {
    if (stage === 'outdoor_to_building') return '正在前往目标建筑。';
    if (stage === 'in_building') return '已经进入建筑内部，继续按照指引前进。';
    if (stage === 'in_elevator') return '已进入电梯，请根据楼层提示选择目标楼层。';
    if (stage === 'on_floor') return '已经在目标楼层附近，马上就要到达目的地。';
    if (stage === 'at_goal') return '已经到达目标位置。';
    return '';
  };

  /**
   * 后端每次导航状态更新时调用
   * @param {Object} navInfo
   *   - goal_id
   *   - distance_to_goal_m
   *   - eta_sec
   *   - stage
   *   - segment_index
   *   - segment_count
   */
  GoalAwarenessClass.prototype.update = function (navInfo) {
    try {
      if (!navInfo?.goal_id) return;

      if (navInfo.goal_id !== this.currentGoalId) {
        this._resetForGoal(navInfo.goal_id);
        logInfo('new goal', { goal_id: navInfo.goal_id });
      }

      const dist = navInfo.distance_to_goal_m;
      if (typeof dist !== 'number') return;

      const stage = navInfo.stage || 'unknown';
      const stageText = this._buildStageText(stage);

      // 1) 阶段播报（每阶段只说一次）
      if (stageText && !this.stageAnnounced[stage]) {
        this.stageAnnounced[stage] = true;
        this._speak(stageText, 'nav');
      }

      // 2) 距离里程碑播报
      const idx = this._pickMilestoneIndex(dist);
      if (idx === null) return;

      if (this.lastMilestoneIndex === null || idx < this.lastMilestoneIndex) {
        // 里程碑从大到小递进
        this.lastMilestoneIndex = idx;
        const text = this._buildDistText(dist);
        if (text) this._speak(text, 'nav');
      }

      // 3) 到达目标
      if (stage === 'at_goal') {
        this._speak('您已经到达目标位置。', 'nav');
      }
    } catch (e) {
      logError('update error', { e });
    }
  };

  GoalAwarenessClass.prototype._speak = function (text, category) {
    if (!text) return;
    const task = {
      type: 'NAV_HINT',
      payload: { text, code: 'goal_update' }
    };

    // 首选记忆敏感语音层
    if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
      window.MemoryAwareVoice.handleTask(task);
      return;
    }
    if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
      window.SpeechRhythm.handleTask(task);
      return;
    }
  };

  window.GoalAwareness = new GoalAwarenessClass();

  if (window.logInfo) {
    window.logInfo('GoalAwareness模块加载完成', { module: 'goal_awareness' });
  } else {
    console.log('✅ GoalAwareness模块加载完成', { module: 'goal_awareness' });
  }
})();


    /* END: goal_awareness.js */
    </script>
</script>

    <!-- ===================== -->
    <!-- Luna PathFeasibility (路径可行性评估) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: path_feasibility.js */
// frontend/path_feasibility.js
/**
 * PathFeasibility / 路径可行性评估
 * 左/中/右路径可行性评估 + 结合结构记忆
 */
(function () {
  'use strict';
  
  if (window.PathFeasibility) return;

  function logDebug(m, p) { window.logDebug?.('[PathFeasibility] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[PathFeasibility] ' + m, p ?? {}); }

  function PF() {
    this.last = null;
  }

  PF.prototype.analyze = function (enhancedState, structureSnapshot) {
    try {
      if (!enhancedState?.pointGrid) return null;

      const pts = enhancedState.pointGrid;
      const width = enhancedState.grid?.width_m ?? 4.0;
      const centerHalf = (width * 0.4) / 2;

      let L = 0, C = 0, R = 0;
      let leftCount = 0, centerCount = 0, rightCount = 0;

      for (const p of pts) {
        if (p.y < 0.5 || p.y > 4.0) continue;

        const zone =
          Math.abs(p.x) <= centerHalf ? 'C' : p.x < 0 ? 'L' : 'R';

        const level = p.risk_level || 'low';
        let base =
          level === 'critical' ? 3 :
          level === 'high' ? 2 :
          level === 'medium' ? 1 : 0;

        const dist = Math.max(p.distance ?? p.y, 0.1);
        const score = base * (1 / dist);

        if (zone === 'L') { L += score; leftCount++; }
        else if (zone === 'C') { C += score; centerCount++; }
        else { R += score; rightCount++; }
      }

      if (structureSnapshot?.leftWallStable) L *= 1.1;
      if (structureSnapshot?.rightWallStable) R *= 1.1;

      const passL = L < 3.0;
      const passC = C < 3.0;
      const passR = R < 3.0;

      let best = 'center';
      let bestScore = passC ? C : Infinity;

      if (passL && L < bestScore) { bestScore = L; best = 'left'; }
      if (passR && R < bestScore) { bestScore = R; best = 'right'; }

      const result = {
        left_passable: passL,
        center_passable: passC,
        right_passable: passR,
        left_block_score: L,
        center_block_score: C,
        right_block_score: R,
        best_side: best,
        bottleneck: !passL && !passC && !passR
      };

      this.last = result;
      logDebug('result', result);
      return result;
    } catch (err) {
      logError('analyze error', err);
      return null;
    }
  };

  PF.prototype.getLast = function () {
    return this.last;
  };

  window.PathFeasibility = new PF();

  if (window.logInfo) {
    window.logInfo('PathFeasibility模块加载完成', { module: 'path_feasibility' });
  } else {
    console.log('✅ PathFeasibility模块加载完成', { module: 'path_feasibility' });
  }
})();


    /* END: path_feasibility.js */
    </script>

    </script>

    </script>

    </script>

    </script>

    </script>

    <!-- ========================= -->
    <!-- Debug Panel -->
    <!-- ========================= -->
    <script>
        /* BEGIN: debug_panel.js */
        /**
         * ⑦【为你生成一个可直接测试的 DEBUG 面板】
         */
        (function() {
            'use strict';
            
            window.debugPanel = {
                /**
                 * 显示系统状态
                 */
                showState() {
                    const state = {
                        NavigationFSM: window.NavigationFSM ? {
                            state: window.NavigationFSM.state,
                            startTime: window.NavigationFSM.startTime,
                            duration: window.NavigationFSM.getState ? window.NavigationFSM.getState().duration : 0
                        } : '未加载',
                        WaypointManager: window.WaypointManager ? {
                            waypoints: window.WaypointManager.waypoints.length,
                            currentIndex: window.WaypointManager.currentIndex,
                            progress: window.WaypointManager.getProgress ? window.WaypointManager.getProgress() : null
                        } : '未加载',
                        NavigationStrategy: window.NavigationStrategy ? window.NavigationStrategy.getCurrentStrategy() : '未加载',
                        TaskChain: window.taskChain ? {
                            queueLength: window.taskChain.queue ? window.taskChain.queue.length : 0,
                            running: window.taskChain.running,
                            currentTask: window.taskChain.currentTask,
                            stats: window.taskChain.getStats ? window.taskChain.getStats() : null
                        } : '未加载',
                        VisualHazardFilter: window.VisualHazardFilter ? window.VisualHazardFilter.getState() : '未加载',
                        SafeMode: window.SafeMode ? {
                            enabled: window.SafeMode.enabled,
                            reason: window.SafeMode.reason
                        } : '未加载',
                        AutoRecovery: window.AutoRecovery ? window.AutoRecovery.getStats() : '未加载'
                    };
                    
                    console.log('='.repeat(70));
                    console.log('🔍 Luna 系统状态');
                    console.log('='.repeat(70));
                    console.log(JSON.stringify(state, null, 2));
                    console.log('='.repeat(70));
                    
                    return state;
                },
                
                /**
                 * 显示任务链队列
                 */
                showTaskQueue() {
                    if (window.taskChain && window.taskChain.queue) {
                        console.log('📋 TaskChain队列:', window.taskChain.queue);
                        return window.taskChain.queue;
                    } else {
                        console.log('⚠️ TaskChain未加载或队列为空');
                        return [];
                    }
                },
                
                /**
                 * 显示路点信息
                 */
                showWaypoints() {
                    if (window.WaypointManager) {
                        const waypoints = window.WaypointManager.getAllWaypoints ? window.WaypointManager.getAllWaypoints() : window.WaypointManager.waypoints;
                        console.log('📍 路点信息:', waypoints);
                        return waypoints;
                    } else {
                        console.log('⚠️ WaypointManager未加载');
                        return [];
                    }
                },
                
                /**
                 * 触发测试导航
                 */
                testNavigation(destination = '测试目的地') {
                    // === NavigationFSM 强制初始化检查 ===
                    if (!window.NavigationFSM) {
                        console.error('❌ NavigationFSM 未初始化，正在恢复…');
                        window.NavigationFSM = { initialized: true, state: "IDLE" };
                    } else if (!window.NavigationFSM.initialized) {
                        window.NavigationFSM.initialized = true;
                        window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
                        console.log('✅ NavigationFSM 状态已修复');
                    }
                    
                    if (window.NavigationFSM && typeof window.NavigationFSM.start === 'function') {
                        window.NavigationFSM.start(destination);
                        console.log(`✅ 测试导航已启动: ${destination}`);
                    } else {
                        console.error('❌ NavigationFSM.start 方法不可用');
                    }
                },
                
                /**
                 * 触发测试危险检测
                 */
                testHazard(type = 'water') {
                    if (window.emitHazardEvent) {
                        window.emitHazardEvent({ type, level: 'high', meta: { test: true } });
                        console.log(`✅ 测试危险事件已触发: ${type}`);
                    } else {
                        console.log('⚠️ emitHazardEvent未加载');
                    }
                }
            };
            
            console.log('✅ DebugPanel模块加载完成', { module: 'debug_panel' });
            console.log('💡 使用方式: debugPanel.showState()');
        })();
        /* END: debug_panel.js */
    </script>

    <!-- ===================== -->
    <!-- 最终模块加载验证 -->
    <!-- ===================== -->
    <script>
        // 验证所有新模块已正确加载
        (function() {
            const checks = {
                SafeMode: typeof window.SafeMode !== 'undefined',
                RecoveryMode: typeof window.RecoveryMode !== 'undefined',
                NavigationFSM: typeof window.NavigationFSM !== 'undefined',
                WaypointManager: typeof window.WaypointManager !== 'undefined',
                AutoRecovery: typeof window.AutoRecovery !== 'undefined',
                LunaLogger: typeof window.LunaLogger !== 'undefined',
                VisionEnhancer: typeof window.VisionEnhancer !== 'undefined',
                EventFlow: typeof window.EventFlow !== 'undefined'
            };
            const allLoaded = Object.values(checks).every(v => v === true);
            if (allLoaded) {
                console.log('✅ 所有新模块已加载完成', checks);
            } else {
                console.warn('⚠️ 部分新模块未加载', checks);
            }
        })();
    </script>

    <!-- ===================== -->
    <!-- Luna Watchdog (前端看门狗) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: watchdog.js */
// frontend/system/watchdog.js

(function () {
  "use strict";
  if (window.LunaWatchdog) return;

  const HEARTBEAT_INTERVAL = 5000; // ms
  let lastTaskActivity = Date.now();
  let lastNavActivity = Date.now();

  window.LunaWatchdog = {
    markTaskActivity: function () {
      lastTaskActivity = Date.now();
    },

    markNavActivity: function () {
      lastNavActivity = Date.now();
    },
  };

  function checkFrontendHealth() {
    const now = Date.now();
    const staleTask = now - lastTaskActivity > 15000; // 15s
    const staleNav = now - lastNavActivity > 15000;

    if (staleTask && staleNav) {
      // 触发一次前端自恢复（例如刷新导航、重置任务链）
      console.warn("[Watchdog] Frontend seems stalled, requesting backend status...");
      fetch("/api/v1/system/status")
        .then((r) => r.json())
        .then((data) => {
          console.log("[Watchdog] Backend status:", data);
          if (!data.success || data.data.status !== "running") {
            // 请求后端执行重启
            return fetch("/api/v1/system/reboot", { method: "POST" });
          }
        })
        .catch((err) => {
          console.error("[Watchdog] system status check failed", err);
        });
    }
  }

  setInterval(checkFrontendHealth, HEARTBEAT_INTERVAL);

  console.log("[LunaWatchdog] 前端看门狗已启动");
})();

    /* END: watchdog.js */
    </script>

    <!-- ===================== -->
    <!-- ParameterHub (全局参数中心) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: ParameterHub.js */
// frontend/params/ParameterHub.js
// 全局参数中心（危险阈值 / TTS速率 / 检测置信度 / 环境参数）

(function () {
  "use strict";
  if (window.ParameterHub) return;

  window.ParameterHub = {
    // YOLO 置信度阈值
    yolo: {
      dangerThreshold: 0.45,
      generalThreshold: 0.30,
      personThreshold: 0.50,
      distanceDangerMeters: 1.2,
      distanceWarnMeters: 2.5,
    },

    // 导航参数
    navigation: {
      rerouteDistanceMeters: 3.0,
      lostTrackingSeconds: 4,
      stuckRetryCount: 3,
      stuckRetryInterval: 1500,
    },

    // TTS 参数
    tts: {
      rate: 1.0,
      pitch: 1.0,
      volume: 1.0,
      queueEnabled: true,
      minIntervalMs: 1200,
    },

    // 场景图参数
    scene: {
      decayFactor: 0.88,
      memoryReinforceStep: 1.15,
      maxNodeAgeSec: 25,
      mergeDistanceMeter: 1.2,
    },

    // 获取参数值（支持嵌套路径）
    get(path, defaultValue) {
      const parts = path.split(".");
      let value = this;
      for (const part of parts) {
        if (value && typeof value === "object" && part in value) {
          value = value[part];
        } else {
          return defaultValue;
        }
      }
      return value;
    },

    // 设置参数值（支持嵌套路径）
    set(path, value) {
      const parts = path.split(".");
      const lastKey = parts.pop();
      let target = this;
      for (const part of parts) {
        if (!target[part] || typeof target[part] !== "object") {
          target[part] = {};
        }
        target = target[part];
      }
      target[lastKey] = value;
      return true;
    },
  };

  console.log("[ParameterHub] 全局参数中心已加载");
})();

    /* END: ParameterHub.js */
    </script>

    <!-- ===================== -->
    <!-- ErrorCode (前端错误码体系) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: ErrorCode.js */
// frontend/errors/ErrorCode.js
// 前端错误码体系

(function () {
  "use strict";
  if (window.ErrorCode) return;

  window.ErrorCode = {
    // 视觉相关
    YOLO_TIMEOUT: "E_VISION_TIMEOUT",
    YOLO_EMPTY: "E_VISION_EMPTY",
    YOLO_LOW_CONF: "E_VISION_LOW_CONF",

    // 场景图相关
    SCENE_NODE_FAIL: "E_SCENE_NODE_FAIL",
    SCENE_UPDATE_FAIL: "E_SCENE_UPDATE_FAIL",

    // 导航相关
    NAV_NO_ROUTE: "E_NAV_NO_ROUTE",
    NAV_STUCK: "E_NAV_STUCK",
    NAV_REROUTE_FAIL: "E_NAV_REROUTE_FAIL",

    // 任务链相关
    TASK_STEP_ERROR: "E_TASK_STEP_ERROR",
    TASK_ABORT: "E_TASK_ABORT",
    TASK_RECOVERY_FAIL: "E_TASK_RECOVERY_FAIL",

    // 系统错误
    SYS_MODULE_CRASH: "E_SYS_CRASH",
    SYS_RESTART: "E_SYS_RESTART",
    SYS_FORCE_RECOVER: "E_SYS_FORCE_RECOVER",
  };

  console.log("[ErrorCode] 前端错误码体系已加载");
})();

    /* END: ErrorCode.js */
    </script>

    <!-- ===================== -->
    <!-- LogUploader (全链路日志上传系统) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: LogUploader.js */
// frontend/logging/LogUploader.js
// 全链路日志上传系统

(function () {
  "use strict";
  if (window.LogUploader) return;

  const ErrorCode = window.ErrorCode || {};

  class LogUploaderClass {
    constructor() {
      this.queue = [];
      this.endpoint = "/api/v1/log/client"; // 使用统一API Gateway
      this.flushInterval = 5000; // 5秒自动刷新一次
      this.maxQueueSize = 100;
      this._startAutoFlush();
    }

    _startAutoFlush() {
      setInterval(() => {
        this.flush();
      }, this.flushInterval);
    }

    push(entry) {
      const log = {
        timestamp: Date.now(),
        ts: new Date().toISOString(),
        ...entry,
      };

      this.queue.push(log);

      // 防止队列过大
      if (this.queue.length > this.maxQueueSize) {
        this.queue.shift();
      }

      // 立即尝试上传（不阻塞）
      this.flush().catch(() => {
        // 静默失败，等待下次自动刷新
      });
    }

    async flush() {
      if (this.queue.length === 0) return;

      const payload = [...this.queue];
      this.queue = [];

      try {
        const response = await fetch(this.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
          console.debug("[LogUploader] 日志上传成功", { count: payload.length });
        } else {
          throw new Error(result.message || "Upload failed");
        }
      } catch (err) {
        // 上传失败，重新加入队列（保留最近的）
        console.warn("[LogUploader] 日志上传失败，重新入队", err);
        this.queue.unshift(...payload.slice(-50)); // 只保留最近50条
      }
    }

    // 立即上传并等待完成
    async flushSync() {
      while (this.queue.length > 0) {
        await this.flush();
      }
    }
  }

  window.LogUploader = new LogUploaderClass();
  console.log("[LogUploader] 全链路日志上传系统已加载");
})();

    /* END: LogUploader.js */
    </script>

    <!-- ===================== -->
    <!-- VisionBridge (YOLO → SceneGraph → Navigation 桥接) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: VisionBridge.js */
// frontend/vision/VisionBridge.js
// YOLO → SceneGraph → Navigation 桥接

(function () {
  "use strict";
  if (window.VisionBridge) return;

  const ErrorCode = window.ErrorCode || {};
  const LogUploader = window.LogUploader || { push: console.log };
  const ParameterHub = window.ParameterHub || { get: () => null };

  class VisionBridgeClass {
    constructor() {
      this.lastDetectionTime = 0;
      this.detectionCooldown = 100; // 100ms冷却
    }

    // YOLO 输出数据 → SceneGraph
    ingestYolo(detections) {
      const now = Date.now();
      if (now - this.lastDetectionTime < this.detectionCooldown) {
        return; // 冷却中，跳过
      }
      this.lastDetectionTime = now;

      if (!detections || detections.length === 0) {
        LogUploader.push({
          level: "warning",
          code: ErrorCode.YOLO_EMPTY || "E_VISION_EMPTY",
          message: "YOLO returned empty",
          source: "VisionBridge",
        });
        return;
      }

      // 过滤低置信度检测
      const threshold = ParameterHub.get("yolo.generalThreshold", 0.3);
      const filtered = detections.filter((d) => (d.confidence || d.conf) >= threshold);

      if (filtered.length === 0) {
        LogUploader.push({
          level: "warning",
          code: ErrorCode.YOLO_LOW_CONF || "E_VISION_LOW_CONF",
          message: "All detections below threshold",
          source: "VisionBridge",
        });
        return;
      }

      // 更新场景图（如果存在）
      let graphUpdate = null;
      if (window.SceneNodes) {
        try {
          filtered.forEach((detection) => {
            const label = detection.label || detection.class || "unknown";
            window.SceneNodeDetector &&
              window.SceneNodeDetector.updateDetections([detection]);
          });

          graphUpdate = {
            newNodes: filtered.map((d) => ({
              label: d.label || d.class,
              confidence: d.confidence || d.conf,
              position: { x: d.x, y: d.y },
              dangerLevel: this._calculateDangerLevel(d),
            })),
            timestamp: now,
          };
        } catch (err) {
          LogUploader.push({
            level: "error",
            code: ErrorCode.SCENE_UPDATE_FAIL || "E_SCENE_UPDATE_FAIL",
            message: "SceneGraph update failed",
            error: err.toString(),
            source: "VisionBridge",
          });
          return;
        }
      }

      // 场景变化 → 导航钩子
      if (graphUpdate && window.NavigationHook) {
        try {
          window.NavigationHook.handleSceneUpdate(graphUpdate);
        } catch (err) {
          console.warn("[VisionBridge] NavigationHook failed", err);
        }
      }

      // 记录日志
      LogUploader.push({
        level: "info",
        code: "VISION_UPDATE",
        message: "YOLO detection processed",
        source: "VisionBridge",
        details: {
          totalDetections: detections.length,
          filteredDetections: filtered.length,
          graphUpdate: graphUpdate ? graphUpdate.newNodes.length : 0,
        },
      });
    }

    _calculateDangerLevel(detection) {
      const label = (detection.label || detection.class || "").toLowerCase();
      const conf = detection.confidence || detection.conf || 0;

      // 危险物体
      if (label.includes("car") || label.includes("truck") || label.includes("bus")) {
        return conf > 0.5 ? 3 : 2;
      }

      // 台阶/楼梯
      if (label.includes("stair") || label.includes("step")) {
        return conf > 0.6 ? 2 : 1;
      }

      // 行人（中等风险）
      if (label.includes("person") || label.includes("human")) {
        return conf > 0.7 ? 2 : 1;
      }

      return 0;
    }
  }

  window.VisionBridge = new VisionBridgeClass();
  console.log("[VisionBridge] YOLO → SceneGraph → Navigation 桥接已加载");
})();

    /* END: VisionBridge.js */
    </script>

    <!-- ===================== -->
    <!-- NavigationHook (场景影响导航的钩子) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: NavigationHook.js */
// frontend/navigation/NavigationHook.js
// 场景影响导航的钩子

(function () {
  "use strict";
  if (window.NavigationHook) return;

  const ParameterHub = window.ParameterHub || { get: () => null };
  const LogUploader = window.LogUploader || { push: console.log };
  const ErrorCode = window.ErrorCode || {};

  class NavigationHookClass {
    static handleSceneUpdate(graphUpdate) {
      if (!graphUpdate || !graphUpdate.newNodes) return;

      // 检查导航是否激活
      const navFSM = window.NavigationFSM;
      if (!navFSM || !navFSM.getState || navFSM.getState() === "IDLE") {
        return;
      }

      const dangerThreshold = ParameterHub.get("yolo.dangerThreshold", 0.45);
      const distanceDanger = ParameterHub.get("yolo.distanceDangerMeters", 1.2);

      for (const node of graphUpdate.newNodes) {
        // 检查危险级别
        if (node.dangerLevel >= 2) {
          // 计算距离（如果有位置信息）
          let shouldAlert = true;
          if (node.position) {
            const distance = Math.sqrt(
              Math.pow(node.position.x || 0, 2) + Math.pow(node.position.y || 0, 2)
            );
            shouldAlert = distance < distanceDanger;
          }

          if (shouldAlert) {
            // 生成TTS警告
            const message = this._generateDangerMessage(node);
            if (window.speakText) {
              window.speakText(message);
            } else if (window.PriorityTTSQueue) {
              window.PriorityTTSQueue.enqueue({
                text: message,
                priority: "HIGH",
                category: "hazard",
              });
            }

            // 记录日志
            LogUploader.push({
              level: "alert",
              code: "NAV_DANGER",
              message: "Navigation danger detected",
              source: "NavigationHook",
              node: node,
            });

            // 更新调试面板
            if (window.__debugPanel) {
              window.__debugPanel.logNav(`⚠️ 危险检测: ${node.label}`);
            }
          }
        }
      }
    }

    static _generateDangerMessage(node) {
      const label = node.label || "障碍物";
      const dangerLevel = node.dangerLevel || 0;

      if (dangerLevel >= 3) {
        return `危险！前方有${label}，请立即避让。`;
      } else if (dangerLevel >= 2) {
        return `注意，前方有${label}，请小心通过。`;
      } else {
        return `前方有${label}，请注意。`;
      }
    }

    // 处理导航卡住
    static handleStuck() {
      const stuckRetryCount = ParameterHub.get("navigation.stuckRetryCount", 3);
      const stuckRetryInterval = ParameterHub.get("navigation.stuckRetryInterval", 1500);

      LogUploader.push({
        level: "warning",
        code: ErrorCode.NAV_STUCK || "E_NAV_STUCK",
        message: "Navigation appears stuck",
        source: "NavigationHook",
      });

      // 触发重路由逻辑（如果存在）
      if (window.NavigationFSM && window.NavigationFSM.reroute) {
        setTimeout(() => {
          window.NavigationFSM.reroute();
        }, stuckRetryInterval);
      }
    }
  }

  window.NavigationHook = NavigationHookClass;
  console.log("[NavigationHook] 场景影响导航钩子已加载");
})();

    /* END: NavigationHook.js */
    </script>

    <!-- ===================== -->
    <!-- TestFullChain (全链路测试脚本) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: test_full_chain.js */
// frontend/tests/test_full_chain.js
// 全链路测试脚本

(function () {
  "use strict";
  if (window.TestFullChain) return;

  class TestFullChainClass {
    constructor() {
      this.panel = null;
      this.vb = null;
      this.isRunning = false;
    }

    init() {
      // 初始化测试面板
      if (window.TestPanel) {
        this.panel = new window.TestPanel("luna_test_panel");
      }

      // 初始化VisionBridge
      if (window.VisionBridge) {
        this.vb = window.VisionBridge;
      } else {
        console.error("[TestFullChain] VisionBridge not found");
        return false;
      }

      return true;
    }

    simulate() {
      if (!this.init()) {
        console.error("[TestFullChain] Initialization failed");
        return;
      }

      console.log("[TestFullChain] Starting full test...");
      this.isRunning = true;

      // 模拟YOLO检测结果
      const fakeFrame = [
        {
          label: "person",
          conf: 0.71,
          x: 120,
          y: 200,
          w: 80,
          h: 140,
          confidence: 0.71,
          class: "person",
        },
        {
          label: "stairs",
          conf: 0.82,
          x: 260,
          y: 180,
          w: 90,
          h: 110,
          confidence: 0.82,
          class: "stairs",
        },
        {
          label: "door",
          conf: 0.65,
          x: 400,
          y: 150,
          w: 100,
          h: 200,
          confidence: 0.65,
          class: "door",
        },
      ];

      // 处理YOLO数据
      if (this.vb && this.vb.ingestYolo) {
        this.vb.ingestYolo(fakeFrame);
      }

      // 更新测试面板
      if (this.panel) {
        const navState = window.NavigationFSM
          ? {
              state: window.NavigationFSM.getState(),
              currentStep: window.NavigationFSM.getCurrentStep
            ? window.NavigationFSM.getCurrentStep()
            : null,
            }
          : { state: "IDLE" };

        const taskState = window.taskChain
          ? {
              queueLength: window.taskChain.queue ? window.taskChain.queue.length : 0,
              currentTask: window.taskChain.currentTask
            ? window.taskChain.currentTask.type
            : null,
              running: window.taskChain.running || false,
            }
          : { queueLength: 0 };

        this.panel.update({
          yolo: fakeFrame,
          navState: navState,
          taskState: taskState,
          timestamp: new Date().toISOString(),
        });
      }

      // 测试TTS（如果存在）
      if (window.speakText) {
        setTimeout(() => {
          window.speakText("测试播报：导航系统已启动", "cheerful");
        }, 1000);
      } else if (window.PriorityTTSQueue) {
        window.PriorityTTSQueue.enqueue({
          text: "测试播报：导航系统已启动",
          priority: "MEDIUM",
          category: "test",
        });
      }

      // 标记活动（看门狗）
      if (window.LunaWatchdog) {
        window.LunaWatchdog.markTaskActivity();
        window.LunaWatchdog.markNavActivity();
      }

      console.log("[TestFullChain] Full test completed");
      this.isRunning = false;
    }

    // 连续测试（模拟多帧）
    simulateContinuous(frames = 5, intervalMs = 2000) {
      if (!this.init()) {
        return;
      }

      console.log(`[TestFullChain] Starting continuous test: ${frames} frames`);
      let count = 0;

      const timer = setInterval(() => {
        count++;
        console.log(`[TestFullChain] Frame ${count}/${frames}`);

        // 生成随机检测结果
        const randomFrame = this._generateRandomFrame();
        if (this.vb && this.vb.ingestYolo) {
          this.vb.ingestYolo(randomFrame);
        }

        if (this.panel) {
          this.panel.append(`frame_${count}`, {
            detections: randomFrame.length,
            timestamp: new Date().toISOString(),
          });
        }

        if (count >= frames) {
          clearInterval(timer);
          console.log("[TestFullChain] Continuous test completed");
        }
      }, intervalMs);
    }

    _generateRandomFrame() {
      const labels = ["person", "stairs", "door", "elevator", "sign"];
      const count = Math.floor(Math.random() * 3) + 1;
      const frame = [];

      for (let i = 0; i < count; i++) {
        const label = labels[Math.floor(Math.random() * labels.length)];
        frame.push({
          label: label,
          conf: 0.5 + Math.random() * 0.4,
          confidence: 0.5 + Math.random() * 0.4,
          class: label,
          x: Math.random() * 640,
          y: Math.random() * 480,
          w: 50 + Math.random() * 100,
          h: 50 + Math.random() * 150,
        });
      }

      return frame;
    }
  }

  window.TestFullChain = new TestFullChainClass();

  // 全局测试函数
  window.testFullChain = function () {
    window.TestFullChain.simulate();
  };

  window.testFullChainContinuous = function (frames, interval) {
    window.TestFullChain.simulateContinuous(frames, interval);
  };

  console.log("[TestFullChain] 全链路测试脚本已加载");
  console.log("[TestFullChain] 使用方法: testFullChain() 或 testFullChainContinuous(5, 2000)");
})();

    /* END: test_full_chain.js */
    </script>

    <!-- Vision Health Check (视觉健康检测脚本) -->
    <script>
        /* BEGIN: vision_health_check.js */
// frontend/tests/vision_health_check.js
/**
 * Luna Badge Vision Health Check
 * 用于自动检测 vision_enhancer.js 是否仍然会触发 null/undefined 崩溃
 * 可在无摄像头、无 YOLO 输入的情况下运行
 * 
 * 使用方法：
 * 1. 在浏览器控制台运行：直接调用 window.runVisionHealthCheck()
 * 2. 页面加载后会自动运行一次
 */

(function() {
  'use strict';

  // 等待 VisionEnhancer 加载完成
  function waitForVisionEnhancer(callback, maxAttempts = 50) {
    let attempts = 0;
    const checkInterval = setInterval(() => {
      attempts++;
      if (window.VisionEnhancer && typeof window.VisionEnhancer.analyzeRisk === 'function') {
        clearInterval(checkInterval);
        callback();
      } else if (attempts >= maxAttempts) {
        clearInterval(checkInterval);
        console.error('❌ VisionEnhancer 未加载，请确保 vision_enhancer.js 已加载');
      }
    }, 100);
  }

  function safeAnalyze(input, label) {
    try {
      if (!window.VisionEnhancer || typeof window.VisionEnhancer.analyzeRisk !== 'function') {
        console.error(`❌ [${label}] VisionEnhancer.analyzeRisk 不可用`);
        return;
      }

      const result = window.VisionEnhancer.analyzeRisk(input);
      
      // 验证返回结果格式
      if (result && typeof result === 'object') {
        console.log(`✔ [${label}] 正常运行`, {
          hasSummary: !!result,
          riskLevel: result.riskLevel || 'unknown',
          hazardsCount: (result.hazards || []).length,
          hasDangerFrame: result.hasDangerFrame || false
        });
      } else {
        console.warn(`⚠️ [${label}] 返回结果格式异常`, result);
      }
    } catch (err) {
      console.error(`❌ [${label}] 崩溃:`, {
        error: err.toString(),
        message: err.message,
        stack: err.stack
      });
    }
  }

  function runHealthCheck() {
    console.log('='.repeat(60));
    console.log('🔍 Vision Health Check Start');
    console.log('='.repeat(60));

    // 1️⃣ 测试 null 输入
    safeAnalyze(null, '输入 null');

    // 2️⃣ 测试 undefined 输入
    safeAnalyze(undefined, '输入 undefined');

    // 3️⃣ 测试缺少 detections 字段
    safeAnalyze({}, '无 detections');

    // 4️⃣ 测试 detections: null
    safeAnalyze({ detections: null }, 'detections:null');

    // 5️⃣ 测试 detections: undefined
    safeAnalyze({ detections: undefined }, 'detections:undefined');

    // 6️⃣ detections 空数组
    safeAnalyze({ detections: [] }, 'detections:[]');

    // 7️⃣ detections 非数组（字符串）
    safeAnalyze({ detections: 'not an array' }, 'detections:字符串');

    // 8️⃣ detections 含 undefined / null
    safeAnalyze({
      detections: [null, undefined, {}, { box: null }, { box: { x1: 5, y1: 5, x2: 20, y2: 20 } }]
    }, 'detections 含 null/undefined');

    // 9️⃣ detections 含 null box
    safeAnalyze({
      detections: [
        { box: null },
        { bbox: undefined },
        { rect: null }
      ]
    }, 'detections 含 null box');

    // 🔟 模拟正常 YOLO 输出
    safeAnalyze({
      detections: [
        { label: 'person', class: 'person', box: { x1: 10, y1: 10, x2: 100, y2: 200 }, confidence: 0.9 },
        { label: 'obstacle', class: 'obstacle', bbox: { x1: 200, y1: 50, x2: 260, y2: 180 }, confidence: 0.8 }
      ],
      frameWidth: 640,
      frameHeight: 480
    }, '正常 YOLO 输入');

    // 1️⃣1️⃣ 模拟部分字段缺失
    safeAnalyze({
      detections: [
        { label: 'person' }, // 缺少 box
        { box: { x1: 10, y1: 10, x2: 100, y2: 200 } } // 缺少 label
      ],
      frameWidth: 640
      // 缺少 frameHeight
    }, '部分字段缺失');

    // 1️⃣2️⃣ 模拟极端情况：所有字段都是 null
    safeAnalyze({
      detections: [
        null,
        undefined,
        { box: null, label: null, class: null },
        { bbox: undefined, confidence: null }
      ],
      frameWidth: null,
      frameHeight: undefined
    }, '极端情况：所有字段都是 null');

    console.log('='.repeat(60));
    console.log('✅ Vision Health Check Done');
    console.log('='.repeat(60));
    console.log('\n📊 检查结果说明：');
    console.log('   ✔ = 正常运行，无崩溃');
    console.log('   ❌ = 出现崩溃，需要修复');
    console.log('   ⚠️  = 返回结果异常，但未崩溃');
  }

  // 如果 VisionEnhancer 已加载，直接运行
  if (window.VisionEnhancer && typeof window.VisionEnhancer.analyzeRisk === 'function') {
    runHealthCheck();
  } else {
    // 否则等待加载
    console.log('⏳ 等待 VisionEnhancer 加载...');
    waitForVisionEnhancer(runHealthCheck);
  }

  // 导出到全局，方便手动调用
  window.runVisionHealthCheck = runHealthCheck;
  console.log('\n💡 提示：可以随时调用 window.runVisionHealthCheck() 重新运行测试');
})();
        /* END: vision_health_check.js */
    </script>

    <!-- Navigation Diagnosis (导航系统诊断脚本) -->
    <script>
        /* BEGIN: navigation_diagnosis.js */
// frontend/tests/navigation_diagnosis.js
/**
 * Luna Badge 导航系统诊断脚本
 * 用于快速定位导航不启动的原因
 */

(function() {
  'use strict';

  function runDiagnosis() {
    // 兼容性：使用 Array.fill().join() 替代 .repeat()
    var separator = Array(60).fill('=').join('');
    console.log(separator);
    console.log("🔍 Vision Navigation Diagnosis");
    console.log(separator);

    const results = {
      yolo: {},
      visionEnhancer: {},
      navigationFSM: {},
      tts: {},
      eventDispatcher: {},
      overall: {}
    };

    // 1️⃣ 检查 YOLO 输出
    console.log("\n📋 1. YOLO 输出检查");
    console.log(Array(60).fill('-').join(''));
    
    results.yolo.lastOutput = window.lastYoloOutput;
    results.yolo.exists = typeof window.lastYoloOutput !== 'undefined';
    results.yolo.isNull = window.lastYoloOutput === null;
    results.yolo.isEmpty = window.lastYoloOutput && Object.keys(window.lastYoloOutput).length === 0;
    
    console.log("   lastYoloOutput:", results.yolo.lastOutput);
    console.log("   存在:", results.yolo.exists);
    console.log("   是否为null:", results.yolo.isNull);
    console.log("   是否为空对象:", results.yolo.isEmpty);
    
    if (!results.yolo.exists) {
      console.log("   ❌ YOLO 没有输出（undefined）");
    } else if (results.yolo.isNull) {
      console.log("   ❌ YOLO 输出为 null（可能报错）");
    } else if (results.yolo.isEmpty) {
      console.log("   ⚠️  YOLO 输出为空对象（格式可能不对）");
    } else {
      console.log("   ✅ YOLO 有输出");
    }

    // 检查 YOLO 就绪状态
    results.yolo.ready = window.yoloReady;
    console.log("   yoloReady:", results.yolo.ready);
    if (results.yolo.ready === false) {
      console.log("   ❌ YOLO 模型未加载");
    } else if (typeof results.yolo.ready === 'undefined') {
      console.log("   ⚠️  YOLO 脚本可能未执行");
    } else {
      console.log("   ✅ YOLO 已就绪");
    }

    // 2️⃣ 检查 VisionEnhancer
    console.log("\n📋 2. VisionEnhancer 检查");
    console.log(Array(60).fill("-").join(""));
    
    results.visionEnhancer.exists = !!window.VisionEnhancer;
    results.visionEnhancer.hasProcessFrame = typeof window.VisionEnhancer?.processFrame === 'function';
    results.visionEnhancer.hasAnalyzeRisk = typeof window.VisionEnhancer?.analyzeRisk === 'function';
    results.visionEnhancer.lastSummary = window.VisionEnhancer?.lastSummary;
    
    console.log("   VisionEnhancer 存在:", results.visionEnhancer.exists);
    console.log("   processFrame 方法:", results.visionEnhancer.hasProcessFrame ? "✅" : "❌");
    console.log("   analyzeRisk 方法:", results.visionEnhancer.hasAnalyzeRisk ? "✅" : "❌");
    console.log("   lastSummary:", results.visionEnhancer.lastSummary);
    
    if (!results.visionEnhancer.exists) {
      console.log("   ❌ VisionEnhancer 模块未加载");
    } else if (!results.visionEnhancer.hasProcessFrame) {
      console.log("   ❌ VisionEnhancer.processFrame 不可用");
    } else {
      console.log("   ✅ VisionEnhancer 正常");
    }

    // 3️⃣ 检查 NavigationFSM
    console.log("\n📋 3. NavigationFSM 检查");
    console.log(Array(60).fill("-").join(""));
    
    results.navigationFSM.exists = !!window.NavigationFSM;
    results.navigationFSM.state = window.NavigationFSM?.state;
    results.navigationFSM.hasStart = typeof window.NavigationFSM?.start === 'function';
    results.navigationFSM.hasHandleEvent = typeof window.NavigationFSM?.handleEvent === 'function';
    
    console.log("   NavigationFSM 存在:", results.navigationFSM.exists);
    console.log("   当前状态:", results.navigationFSM.state || "undefined");
    console.log("   start 方法:", results.navigationFSM.hasStart ? "✅" : "❌");
    console.log("   handleEvent 方法:", results.navigationFSM.hasHandleEvent ? "✅" : "❌");
    
    if (!results.navigationFSM.exists) {
      console.log("   ❌ NavigationFSM 模块未加载");
    } else if (results.navigationFSM.state === 'idle') {
      console.log("   ⚠️  导航处于 idle 状态（未启动）");
    } else if (results.navigationFSM.state === 'paused') {
      console.log("   ⚠️  导航处于 paused 状态（可能被挂起）");
    } else if (results.navigationFSM.state === 'active' || results.navigationFSM.state === 'NAVIGATING') {
      console.log("   ✅ 导航已启动");
    } else {
      console.log("   ⚠️  导航状态未知:", results.navigationFSM.state);
    }

    // 4️⃣ 检查 TTS 系统
    console.log("\n📋 4. TTS 系统检查");
    console.log(Array(60).fill("-").join(""));
    
    results.tts.hasSpeakText = typeof window.speakText === 'function';
    results.tts.hasPriorityTTS = !!window.PriorityTTSQueue;
    results.tts.hasTTS = !!window.TTS;
    
    console.log("   speakText 函数:", results.tts.hasSpeakText ? "✅" : "❌");
    console.log("   PriorityTTSQueue:", results.tts.hasPriorityTTS ? "✅" : "❌");
    console.log("   TTS 对象:", results.tts.hasTTS ? "✅" : "❌");
    
    if (!results.tts.hasSpeakText && !results.tts.hasPriorityTTS && !results.tts.hasTTS) {
      console.log("   ❌ TTS 系统未初始化");
    } else {
      console.log("   ✅ TTS 系统可用");
    }

    // 5️⃣ 检查 EventDispatcher
    console.log("\n📋 5. EventDispatcher 检查");
    console.log(Array(60).fill("-").join(""));
    
    results.eventDispatcher.exists = !!window.EventDispatcher;
    results.eventDispatcher.hasEmitHazard = typeof window.EventDispatcher?.emitHazardEvent === 'function';
    results.eventDispatcher.hasEmitNav = typeof window.EventDispatcher?.emitNavigationEvent === 'function';
    
    console.log("   EventDispatcher 存在:", results.eventDispatcher.exists);
    console.log("   emitHazardEvent:", results.eventDispatcher.hasEmitHazard ? "✅" : "❌");
    console.log("   emitNavigationEvent:", results.eventDispatcher.hasEmitNav ? "✅" : "❌");
    
    if (!results.eventDispatcher.exists) {
      console.log("   ❌ EventDispatcher 模块未加载");
    } else {
      console.log("   ✅ EventDispatcher 正常");
    }

    // 6️⃣ 综合诊断
    console.log("\n📋 6. 综合诊断结果");
    console.log(Array(60).fill("=").join(""));
    
    const issues = [];
    
    if (!results.yolo.exists || results.yolo.isNull) {
      issues.push("❌ YOLO 没有输出 → 导航永远不会启动");
    }
    
    if (!results.visionEnhancer.exists || !results.visionEnhancer.hasProcessFrame) {
      issues.push("❌ VisionEnhancer 未加载或不可用 → 视觉处理中断");
    }
    
    if (!results.navigationFSM.exists) {
      issues.push("❌ NavigationFSM 未加载 → 导航状态机不存在");
    } else if (results.navigationFSM.state === 'idle') {
      issues.push("⚠️  NavigationFSM 处于 idle 状态 → 导航未启动");
    }
    
    if (!results.tts.hasSpeakText && !results.tts.hasPriorityTTS) {
      issues.push("❌ TTS 系统不可用 → 无法播报");
    }
    
    if (!results.eventDispatcher.exists) {
      issues.push("❌ EventDispatcher 未加载 → 事件无法分发");
    }

    if (issues.length === 0) {
      console.log("✅ 所有模块正常，导航系统应该可以工作");
      console.log("\n💡 如果仍然没有播报，可能的原因：");
      console.log("   1. YOLO 没有检测到物体（正常，需要等待）");
      console.log("   2. 导航没有收到视觉更新（检查 YOLO 回调绑定）");
      console.log("   3. TTS 权限未授予（Safari 需要用户交互）");
    } else {
      console.log("⚠️  发现以下问题：");
      issues.forEach((issue, i) => {
        console.log(`   ${i + 1}. ${issue}`);
      });
    }

    console.log("\n" + Array(60).fill("=").join(""));
    console.log("📊 诊断完成");
    console.log(Array(60).fill("=").join(""));
    
    // 返回结果供进一步分析
    return results;
  }

  // 导出到全局（确保即使出错也能访问）
  try {
    window.runNavigationDiagnosis = runDiagnosis;
    console.log("✅ window.runNavigationDiagnosis 已定义");
  } catch (e) {
    console.error("❌ 导出 runNavigationDiagnosis 失败:", e);
    // 即使出错也尝试定义
    window.runNavigationDiagnosis = function() {
      console.error("导航诊断脚本加载失败，请检查控制台错误");
    };
  }
  
  // 如果页面已加载完成，自动运行一次
  try {
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      setTimeout(function() {
        try {
          runDiagnosis();
        } catch (e) {
          console.error("自动运行诊断失败:", e);
        }
      }, 2000); // 延迟2秒确保所有模块加载完成
    } else {
      window.addEventListener('load', function() {
        setTimeout(function() {
          try {
            runDiagnosis();
          } catch (e) {
            console.error("自动运行诊断失败:", e);
          }
        }, 2000);
      });
    }
  } catch (e) {
    console.error("设置自动运行失败:", e);
  }

  console.log("💡 导航诊断脚本已加载");
  console.log("   手动运行: window.runNavigationDiagnosis()");
  
  // 验证导出是否成功
  if (typeof window.runNavigationDiagnosis === 'function') {
    console.log("✅ 验证成功: window.runNavigationDiagnosis 是一个函数");
  } else {
    console.error("❌ 验证失败: window.runNavigationDiagnosis 不是函数，类型:", typeof window.runNavigationDiagnosis);
  }
})();
        /* END: navigation_diagnosis.js */
    </script>

    <!-- ===================== -->
    <!-- DirectionEstimator (方向估计) - v1.1.1 -->
    <!-- ===================== -->
    <script>
    /* BEGIN: direction_estimator.js */
// frontend/direction_estimator.js
// 方向估计：根据 bbox 横向位置判断 leftFront / front / rightFront

(function () {
  "use strict";
  if (window.calcDirection) return;

  /**
   * 根据 bbox 横向位置判断方向
   * @param {Object} bbox - 边界框 {x1, y1, x2, y2}，坐标范围 0~1
   * @returns {string} "leftFront" | "front" | "rightFront"
   */
  window.calcDirection = function (bbox) {
    if (!bbox || typeof bbox.x1 !== "number" || typeof bbox.x2 !== "number") {
      console.warn("[DirectionEstimator] Invalid bbox:", bbox);
      return "front"; // 默认值
    }

    const center = (bbox.x1 + bbox.x2) / 2; // 0~1 屏幕相对坐标

    if (center < 0.33) return "leftFront";
    if (center < 0.66) return "front";
    return "rightFront";
  };

  console.log("[DirectionEstimator] 方向估计算法已加载");
})();

    /* END: direction_estimator.js */
    </script>

    <!-- ===================== -->
    <!-- DistanceEstimator (距离估计) - v1.1.1 -->
    <!-- ===================== -->
    <script>
    /* BEGIN: distance_estimator.js */
// frontend/distance_estimator.js
// 距离估计（简单版）：根据 bbox 高度推测粗略距离

(function () {
  "use strict";
  if (window.calcDistance) return;

  /**
   * 根据 bbox 高度推测粗略距离
   * @param {Object} bbox - 边界框 {x1, y1, x2, y2}，坐标范围 0~1
   * @returns {number|null} 距离（米），如果太远则返回 null
   */
  window.calcDistance = function (bbox) {
    if (!bbox || typeof bbox.y1 !== "number" || typeof bbox.y2 !== "number") {
      console.warn("[DistanceEstimator] Invalid bbox:", bbox);
      return null;
    }

    const h = bbox.y2 - bbox.y1; // 0~1

    if (h > 0.45) return 0.3; // 30cm 以内
    if (h > 0.20) return 0.8; // 80cm 左右
    if (h > 0.10) return 1.2; // 1.2m+

    return null; // 太远，不报具体距离
  };

  console.log("[DistanceEstimator] 距离估计算法已加载");
})();

    /* END: distance_estimator.js */
    </script>

    <!-- ===================== -->
    <!-- TaskChainUnified (统一任务链) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: task_chain_unified.js */
// frontend/task_chain_unified.js
// 统一任务链（TaskChain）- 新增基础管线

(function () {
  "use strict";
  if (window.TaskChainUnified) return;

  class TaskChainUnified {
    constructor() {
      this.queue = [];
      this.running = false;
    }

    enqueue(task) {
      if (typeof task !== "function") {
        console.warn("[TaskChainUnified] Task must be a function");
        return;
      }
      this.queue.push(task);
      this.run();
    }

    async run() {
      if (this.running) return;
      this.running = true;

      while (this.queue.length > 0) {
        const task = this.queue.shift();
        try {
          await task();
        } catch (err) {
          console.error("[TaskChainUnified] Task error:", err);
          // 记录错误日志
          if (window.LogUploader) {
            window.LogUploader.push({
              level: "error",
              code: window.ErrorCode?.TASK_STEP_ERROR || "E_TASK_STEP_ERROR",
              message: "TaskChainUnified task failed",
              error: err.toString(),
              source: "TaskChainUnified",
            });
          }
        }
      }

      this.running = false;
    }

    clear() {
      this.queue = [];
      this.running = false;
    }

    getQueueLength() {
      return this.queue.length;
    }
  }

  window.TaskChainUnified = new TaskChainUnified();
  console.log("[TaskChainUnified] 统一任务链已加载");
})();

    /* END: task_chain_unified.js */
    </script>

    <!-- ===================== -->
    <!-- Hooks (全局钩子系统) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: hooks.js */
// frontend/hooks.js
// 全局钩子系统（Hooks）- 情绪/任务系统预留钩子

(function () {
  "use strict";
  if (window.Hooks) return;

  window.Hooks = {
    onHazard: [],
    onStep: [],
    onNavigation: [],
    onEmotion: [],
    onTask: [],
    onActionSuggest: [], // v1.1.1 新增：动作建议入口（1.2.0 用）

    emit(list, data) {
      if (!Array.isArray(list)) {
        console.warn("[Hooks] List must be an array");
        return;
      }
      list.forEach((fn) => {
        try {
          if (typeof fn === "function") {
            fn(data);
          }
        } catch (e) {
          console.error("[Hooks] Hook execution error:", e);
        }
      });
    },

    // 注册钩子
    on(eventName, callback) {
      if (!this[eventName]) {
        console.warn(`[Hooks] Unknown event: ${eventName}`);
        return;
      }
      if (typeof callback !== "function") {
        console.warn("[Hooks] Callback must be a function");
        return;
      }
      this[eventName].push(callback);
    },

    // 移除钩子
    off(eventName, callback) {
      if (!this[eventName]) return;
      const index = this[eventName].indexOf(callback);
      if (index > -1) {
        this[eventName].splice(index, 1);
      }
    },
  };

  console.log("[Hooks] 全局钩子系统已加载");
})();

    /* END: hooks.js */
    </script>

    <!-- ===================== -->
    <!-- SpeechPolicy (统一文案策略) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: speech_policy.js */
// frontend/speech_policy.js
// 统一文案策略（SpeechPolicy）

(function () {
  "use strict";
  if (window.SpeechPolicy) return;

  window.SpeechPolicy = {
    getHazardMessage(type) {
      const map = {
        obstacle: "前方有障碍物，请注意安全。",
        person: "前方有人接近，请注意避让。",
        vehicle: "前方有车辆经过，请特别小心。",
        stepDown: "前方是下台阶，请注意脚下落差。",
        stepUp: "前方是上台阶，请抬脚注意高度。",
        stairs: "前方有楼梯，请注意台阶。",
        door: "前方有门，请注意。",
        elevator: "前方有电梯，请注意。",
        crowd: "前方人群较多，请放慢速度。",
        narrow: "前方通道较窄，请小心通过。",
      };
      return map[type] || "请注意前方情况。";
    },

    getNavigationMessage(action, direction, distance) {
      if (action === "turn") {
        return `前方${distance || ""}米${direction === "left" ? "左" : "右"}转`;
      } else if (action === "straight") {
        return `请直行${distance ? distance + "米" : ""}`;
      } else if (action === "stop") {
        return "已到达目的地";
      }
      return "请跟随导航指引";
    },

    getStepMessage(direction, distance) {
      if (direction === "up") {
        return `前方${distance || ""}米有上台阶，请抬脚注意高度。`;
      } else if (direction === "down") {
        return `前方${distance || ""}米有下台阶，请注意脚下落差。`;
      }
      return `前方${distance || ""}米有台阶，请注意。`;
    },

    /**
     * v1.1.1 新增：根据方向 + 距离 + 类型生成更拟人的提示语句
     * @param {Object} params - {type, direction, distance}
     * @param {string} params.type - 危险类型 (obstacle/person/vehicle/stepUp/stepDown)
     * @param {string} params.direction - 方向 (leftFront/front/rightFront)
     * @param {number|null} params.distance - 距离（米）
     * @returns {string} 拟人化提示语句
     */
    getHazardSentence({ type, direction, distance }) {
      const dirMap = {
        leftFront: "左前方",
        front: "正前方",
        rightFront: "右前方",
      };

      const dirText = dirMap[direction] || "前方";

      const distText = distance
        ? distance < 0.5
          ? "半米内"
          : distance < 1.0
          ? "1米内"
          : `${distance.toFixed(1)}米处`
        : "前方";

      const typeMap = {
        obstacle: "有障碍物",
        person: "有人接近",
        vehicle: "有车辆经过",
        stepUp: "是上台阶",
        stepDown: "是下台阶",
        stairs: "有楼梯",
        door: "有门",
        elevator: "有电梯",
        crowd: "人群较多",
        narrow: "通道较窄",
      };

      const t = typeMap[type] || "情况不明";

      return `${dirText}${distText}${t}，请注意。`;
    },
  };

  console.log("[SpeechPolicy] 统一文案策略已加载");
})();

    /* END: speech_policy.js */
    </script>

    <!-- ===================== -->
    <!-- EventDispatcher (统一事件派发中心) -->
    <!-- ===================== -->
    <script>
    /* BEGIN: event_dispatcher.js */
// frontend/event_dispatcher.js
// 统一事件派发中心（EventDispatcher）

(function () {
  "use strict";
  if (window.EventDispatcher) return;

  const TaskChainUnified = window.TaskChainUnified || {
    enqueue: (fn) => {
      console.warn("[EventDispatcher] TaskChainUnified not found, executing directly");
      try {
        fn();
      } catch (e) {
        console.error("[EventDispatcher] Direct execution error:", e);
      }
    },
  };

  const Hooks = window.Hooks || {
    emit: () => {},
  };

  // 处理危险事件
  function handleHazard(data) {
    const { type, msg, level, meta } = data || {};
    const message = msg || window.SpeechPolicy?.getHazardMessage(type) || "请注意前方情况。";

    // 触发钩子
    Hooks.emit(Hooks.onHazard, { type, message, level, meta });

    // TTS播报
    if (window.speakText) {
      window.speakText(message, level === "critical" ? "urgent" : "calm");
    } else if (window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: level === "critical" ? "HIGH" : "MEDIUM",
        category: "hazard",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: level || "warning",
        code: "HAZARD_DETECTED",
        message: "Hazard detected",
        source: "EventDispatcher",
        details: { type, message, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`⚠️ 危险: ${type} - ${message}`);
    }
  }

  // 处理台阶事件
  function handleStep(data) {
    const { direction, distance, meta } = data || {};
    const message =
      window.SpeechPolicy?.getStepMessage(direction, distance) ||
      `前方${distance || ""}米有台阶，请注意。`;

    // 触发钩子
    Hooks.emit(Hooks.onStep, { direction, distance, message, meta });

    // TTS播报
    if (window.speakText) {
      window.speakText(message, "calm");
    } else if (window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: "MEDIUM",
        category: "step",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "info",
        code: "STEP_DETECTED",
        message: "Step detected",
        source: "EventDispatcher",
        details: { direction, distance, message, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`📐 台阶: ${direction} - ${distance}m`);
    }
  }

  // 处理导航事件
  function handleNavigation(data) {
    const { navState, action, direction, distance, meta } = data || {};
    const message =
      window.SpeechPolicy?.getNavigationMessage(action, direction, distance) ||
      "请跟随导航指引";

    // 触发钩子
    Hooks.emit(Hooks.onNavigation, { navState, action, direction, distance, message, meta });

    // TTS播报（如果需要）
    if (action && window.speakText) {
      window.speakText(message, "cheerful");
    } else if (action && window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: "MEDIUM",
        category: "navigation",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "info",
        code: "NAVIGATION_UPDATE",
        message: "Navigation state updated",
        source: "EventDispatcher",
        details: { navState, action, direction, distance, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.updateNavStatus(navState || {});
      if (action) {
        window.__debugPanel.logNav(`🧭 导航: ${action} - ${message}`);
      }
    }
  }

  // v1.1.1 新增：支持 enhanced hazard data（方向 + 距离）
  function handleEnhancedHazard(bbox, type) {
    const direction = window.calcDirection ? window.calcDirection(bbox) : "front";
    const distance = window.calcDistance ? window.calcDistance(bbox) : null;
    const data = {
      type,
      direction,
      distance,
      width: bbox.x2 - bbox.x1 || null,
      height: bbox.y2 - bbox.y1 || null,
      bbox: bbox, // 保留原始bbox供未来使用
    };

    // 1) 事件加入任务链
    TaskChainUnified.enqueue(() => handleHazard(data));

    // 2) 给语音策略处理（使用新的拟人化文案）
    const msg =
      window.SpeechPolicy?.getHazardSentence(data) ||
      window.SpeechPolicy?.getHazardMessage(type) ||
      "请注意前方情况。";

    TaskChainUnified.enqueue(() => {
      if (window.speakText) {
        window.speakText(msg, data.distance && data.distance < 0.5 ? "urgent" : "calm");
      } else if (window.PriorityTTSQueue) {
        window.PriorityTTSQueue.enqueue({
          text: msg,
          priority: data.distance && data.distance < 0.5 ? "HIGH" : "MEDIUM",
          category: "hazard",
        });
      }
    });

    // 3) 发给钩子（未来 Luna 情绪 / 动作建议 入口）
    Hooks.emit(Hooks.onHazard, data);
    Hooks.emit(Hooks.onActionSuggest, data);

    // 4) 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: data.distance && data.distance < 0.5 ? "warning" : "info",
        code: "ENHANCED_HAZARD_DETECTED",
        message: "Enhanced hazard detected",
        source: "EventDispatcher",
        details: data,
      });
    }

    // 5) 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`⚠️ 增强危险: ${type} - ${direction} - ${distance ? distance.toFixed(1) + "m" : "未知距离"}`);
    }
  }

  window.EventDispatcher = {
    emitHazardEvent(data) {
      TaskChainUnified.enqueue(() => handleHazard(data));
    },

    // v1.1.1 新增：支持 bbox + type 的增强危险事件
    emitEnhancedHazardEvent(bbox, type) {
      if (!bbox || !type) {
        console.warn("[EventDispatcher] emitEnhancedHazardEvent: missing bbox or type");
        return;
      }
      handleEnhancedHazard(bbox, type);
    },

    emitStepEvent(data) {
      TaskChainUnified.enqueue(() => handleStep(data));
    },

    emitNavigationEvent(data) {
      TaskChainUnified.enqueue(() => handleNavigation(data));
    },
  };

  console.log("[EventDispatcher] 统一事件派发中心已加载");
})();

    /* END: event_dispatcher.js */
    </script>

    <!-- ===================== -->
    <!-- 全局Promise异常兜底 -->
    <!-- ===================== -->
    <script>
    /* BEGIN: promise_error_handler.js */
// 全局Promise异常兜底 - 保证不会静默失败

(function () {
  "use strict";

  window.addEventListener("unhandledrejection", function (event) {
    console.error("[PromiseErrorHandler] Unhandled Promise Rejection:", event.reason);

    // 记录错误日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "error",
        code: window.ErrorCode?.SYS_MODULE_CRASH || "E_SYS_CRASH",
        message: "Unhandled Promise Rejection",
        error: event.reason?.toString() || String(event.reason),
        source: "PromiseErrorHandler",
        stack: event.reason?.stack,
      });
    }

    // 触发安全模式（如果可用）
    if (window.SafeMode && window.SafeMode.enable) {
      window.SafeMode.enable("系统进入安全模式：出现未捕获异常");
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logTask(`❌ 未捕获异常: ${event.reason}`);
    }

    // 阻止默认行为（避免控制台报错）
    event.preventDefault();
  });

  console.log("[PromiseErrorHandler] 全局Promise异常兜底已加载");
})();

    /* END: promise_error_handler.js */
    </script>

    <!-- ===================== -->
    <!-- 统一 TTS 入口 -->
    <!-- ===================== -->
    <script src="/frontend/speak_text_entry.js"></script>

    <!-- ===================== -->
    <!-- 语音指令解析器 -->
    <!-- ===================== -->
    <script src="/frontend/voice/CommandParser.js"></script>

    <!-- ===================== -->
    <!-- 导航诊断脚本 -->
    <!-- ===================== -->
    <script src="/frontend/tests/navigation_diagnosis.js"></script>

    <!-- ===================== -->
    <!-- 策略系统核心模块 (v1.2.0) -->
    <!-- ===================== -->
    <!-- 注意：这些文件使用ES6模块，但已兼容window全局变量 -->
    <script src="/frontend/core/strategy/StrategyPriorityQueue.js"></script>
    <script src="/frontend/core/strategy/StrategyCooldown.js"></script>
    <script src="/frontend/core/strategy/StrategyFusion.js"></script>

    <!-- ===================== -->
    <!-- 事件分发器 -->
    <!-- ===================== -->
    <script src="/frontend/core/event/EventDispatcher.js"></script>

    <!-- ===================== -->
    <!-- TTS管理器 -->
    <!-- ===================== -->
    <script src="/frontend/core/tts/TTSManager.js"></script>

    <!-- ===================== -->
    <!-- 视觉指引适配器 -->
    <!-- ===================== -->
    <script src="/frontend/adapters/VisionGuidanceAdapter.js"></script>

    <!-- ===================== -->
    <!-- 视觉桥接器（更新版，支持策略指引） -->
    <!-- ===================== -->
    <script src="/frontend/core/vision/VisionBridge.js"></script>

    <!-- ===================== -->
    <!-- 导航指引Hook（更新版，完整集成策略系统） -->
    <!-- ===================== -->
    <script src="/frontend/core/navigation/NavigationHook.js"></script>

    <!-- ===================== -->
    <!-- Guidance核心处理引擎 (v1.2.0) -->
    <!-- ===================== -->
    <!-- Guidance优先级队列 + 冷却机制 -->
    <script src="/frontend/core/guidance/GuidanceQueue.js"></script>

    <!-- Guidance去重融合器 -->
    <script src="/frontend/core/guidance/StrategyFusion.js"></script>

    <!-- Guidance处理器（整合融合器 + 队列 + TTS） -->
    <script src="/frontend/core/guidance/GuidanceProcessor.js"></script>

    <!-- ===================== -->
    <!-- 错误处理系统 (v2.0) -->
    <!-- ===================== -->
    <!-- 错误码映射器 -->
    <script src="/frontend/core/error/ErrorCodeMapper.js"></script>

    <!-- 错误处理器 -->
    <script src="/frontend/core/error/ErrorHandler.js"></script>

    <!-- ===================== -->
    <!-- UI组件 (v2.0) -->
    <!-- ===================== -->
    <!-- 策略提示卡片组件 -->
    <script src="/frontend/components/GuidanceBubble.js"></script>

    <!-- ===================== -->
    <!-- 场景描述系统 (v2.0) -->
    <!-- ===================== -->
    <!-- 场景描述桥接器 -->
    <script src="/frontend/core/scene/SceneDescriptionBridge.js"></script>

    <!-- 场景描述Hook（自动TTS和UI） -->
    <script src="/frontend/core/scene/SceneDescriptionHook.js"></script>

    <!-- ===================== -->
    <!-- 策略系统扩展模块 (A+B+C+D) -->
    <!-- ===================== -->
    <!-- A. 可视化策略UI（导航小条） -->
    <script src="/frontend/strategy_ui.js"></script>

    <!-- B. 策略调试面板 -->
    <script src="/frontend/strategy_debug_panel.js"></script>

    <!-- C. NavigationFSM × 策略行为联动 -->
    <script src="/frontend/navigation_strategy_bridge.js"></script>

    <!-- D. 声音包（不同等级用不同提示音） -->
    <script src="/frontend/sound_pack.js"></script>

    <!-- ===================== -->
    <!-- 测试中心 (v1.2.0) -->
    <!-- ===================== -->
    <!-- 测试中心核心API（纯JS版本，兼容React） -->
    <script src="/frontend/test_center/TestCenter.js"></script>

    <!-- 测试中心UI（纯JS版本） -->
    <script src="/frontend/test_center/TestCenterUI.js"></script>

    <!-- 测试中心快捷入口（按T键打开） -->
    <script>
      document.addEventListener('keydown', function(e) {
        if (e.key === 't' || e.key === 'T') {
          if (window.testCenterUI) {
            const center = document.getElementById('luna_test_center');
            if (center) {
              center.style.display = center.style.display === 'none' ? 'flex' : 'none';
            } else {
              window.testCenterUI.init();
            }
          }
        }
      });
    </script>

    <!-- ===================== -->
    <!-- 新测试界面入口 -->
    <!-- ===================== -->
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
      <a href="/frontend/test_center/new_test_interface.html" 
         style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        🧪 打开测试中心
      </a>
    </div>
</body>
</html>
"""

# ========== API响应辅助函数（规范要求：统一返回格式）==========
def api_success(data=None, message=None):
    """
    统一成功响应格式
    
    Args:
        data: 返回的数据（字典或列表）
        message: 可选的成功消息
    
    Returns:
        Flask Response: JSON格式的成功响应
    """
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response)

def api_error(error, details=None, status_code=500):
    """
    统一错误响应格式
    
    Args:
        error: 错误消息（字符串）
        details: 可选的错误详情（字典）
        status_code: HTTP状态码（默认500）
    
    Returns:
        Flask Response: JSON格式的错误响应
    """
    response = {'success': False, 'error': str(error)}
    if details:
        response['details'] = details
    return jsonify(response), status_code

# API路由
@app.before_request
def log_request():
    """记录所有API请求"""
    if log_manager:
        try:
            endpoint = request.endpoint or request.path
            method = request.method
            user_agent = request.headers.get('User-Agent', 'Unknown')
            ip_address = request.remote_addr
            
            log_manager.log_system_event(
                event=f"API请求: {method} {endpoint}",
                metadata={
                    "endpoint": endpoint,
                    "method": method,
                    "user_agent": user_agent,
                    "ip_address": ip_address,
                    "path": request.path,
                    "args": dict(request.args)
                }
            )
        except Exception as e:
            logger.warning(f"⚠️ 记录请求日志失败: {e}")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/frontend/<path:filename>')
def frontend_static(filename):
    """提供前端静态文件"""
    import os
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    file_path = os.path.join(frontend_dir, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return f"File not found: {filename}", 404

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """基础视觉识别"""
    try:
        if vision_engine is None:
            return api_error('视觉引擎未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        results = vision_engine.detect_and_recognize(image_np)
        
        # 记录日志
        if log_manager:
            try:
                log_manager.log_visual_event(
                    event_type="vision_recognition",
                    detection_result={
                        "detections_count": len(results.get('detections', [])),
                        "ocr_results_count": len(results.get('ocr_results', [])),
                        "processing_time": results.get('processing_time', 0)
                    },
                    system_response="视觉识别完成"
                )
            except Exception as e:
                logger.warning(f"⚠️ 记录视觉日志失败: {e}")
        
        return api_success({
            'detections': results.get('detections', []),
            'ocr_results': results.get('ocr_results', []),
            'processing_time': results.get('processing_time', 0)
        })
    except Exception as e:
        logger.error(f"识别错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/recognize"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/step', methods=['POST'])
def detect_step():
    """台阶检测"""
    try:
        if step_detector is None:
            return api_error('台阶检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        result = step_detector.detect_step(image_np)
        
        # 记录日志
        if log_manager:
            try:
                log_manager.log_visual_event(
                    event_type="step_detection",
                    detection_result={
                        "detected": result is not None,
                        "result": result if result else None
                    },
                    system_response="台阶检测完成" if result else "未检测到台阶"
                )
            except Exception as e:
                logger.warning(f"⚠️ 记录台阶检测日志失败: {e}")
        
        return api_success({
            'step_detection': result if result else {'detected': False, 'message': '未检测到台阶'}
        })
    except Exception as e:
        logger.error(f"台阶检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/step"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/signboard', methods=['POST'])
def detect_signboard():
    """标识牌检测"""
    try:
        if signboard_detector is None:
            return api_error('标识牌检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        results = signboard_detector.detect_signboards(image_np)
        
        return api_success({
            'signboards': [r.to_dict() for r in results] if results else []
        })
    except Exception as e:
        logger.error(f"标识牌检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/signboard"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/hazard', methods=['POST'])
def detect_hazard():
    """危险检测"""
    try:
        if hazard_detector is None:
            return api_error('危险检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        # 如果可能，传递YOLO检测结果用于过滤误报
        detected_objects = []
        if vision_engine:
            try:
                vision_results = vision_engine.detect_and_recognize(image_np)
                detected_objects = vision_results.get('detections', [])
            except:
                pass
        
        results = hazard_detector.detect_hazards(image_np, detected_objects=detected_objects)
        
        # 记录日志
        if log_manager:
            try:
                log_manager.log_visual_event(
                    event_type="hazard_detection",
                    detection_result={
                        "hazards_count": len(results),
                        "hazards": [r.to_dict() for r in results[:5]]  # 只记录前5个
                    },
                    system_response=f"检测到{len(results)}个危险区域"
                )
            except Exception as e:
                logger.warning(f"⚠️ 记录危险检测日志失败: {e}")
        
        return api_success({
            'hazards': [r.to_dict() for r in results] if results else [],
            'summary': hazard_detector.get_detection_summary(results) if results else {}
        })
    except Exception as e:
        logger.error(f"危险检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/hazard"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/facility', methods=['POST'])
def detect_facility():
    """公共设施检测"""
    try:
        if facility_detector is None:
            return api_error('公共设施检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        results = facility_detector.detect_facility(image_np)
        
        return api_success({
            'facilities': [r.to_dict() for r in results] if results else []
        })
    except Exception as e:
        logger.error(f"公共设施检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/facility"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/traffic_light', methods=['POST'])
def detect_traffic_light():
    """红绿灯检测"""
    try:
        if traffic_light_detector is None:
            return api_error('红绿灯检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        result = traffic_light_detector.detect_traffic_light(image_np)
        
        return api_success({
            'traffic_light': result.to_dict() if result else None,
            'broadcast_message': result.get_broadcast_message() if result else None
        })
    except Exception as e:
        logger.error(f"红绿灯检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/traffic_light"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/crowd_density', methods=['POST'])
def detect_crowd_density():
    """人群密度检测"""
    try:
        if crowd_density_detector is None:
            return api_error('人群密度检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        result = crowd_density_detector.detect_density(image_np)
        
        return api_success({
            'density': result.to_dict() if result else None
        })
    except Exception as e:
        logger.error(f"人群密度检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/crowd_density"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/queue', methods=['POST'])
def detect_queue():
    """排队检测"""
    try:
        if queue_detector is None:
            return api_error('排队检测器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        result = queue_detector.detect_queue(image_np)
        
        return api_success({
            'queue': result.to_dict() if result else None
        })
    except Exception as e:
        logger.error(f"排队检测错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/queue"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/doorplate', methods=['POST'])
def detect_doorplate():
    """门牌号识别"""
    try:
        if doorplate_reader is None:
            return api_error('门牌号识别器未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        results = doorplate_reader.read_doorplate(image_np)
        
        return api_success({
            'doorplates': [r.to_dict() for r in results] if results else []
        })
    except Exception as e:
        logger.error(f"门牌号识别错误: {e}", extra={"module_name": "api", "meta": {"endpoint": "/api/detect/doorplate"}})
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/map/generate', methods=['POST'])
def generate_local_map():
    """生成本地地图"""
    try:
        if local_map_generator is None:
            return api_error('本地地图生成器未初始化', status_code=500)
        
        data = request.get_json()
        dx = data.get('dx', 0.0)  # x方向移动距离（米）
        dy = data.get('dy', 0.0)  # y方向移动距离（米）
        angle_delta = data.get('angle_delta', 0.0)  # 角度变化（弧度）
        
        # 更新位置
        local_map_generator.update_position(dx, dy, angle_delta)
        
        # 如果有图片，添加地标
        if 'image' in request.files:
            file = request.files['image']
            image_np = image_to_numpy(file.read())
            if image_np is not None:
                # 检测地标（使用设施检测器）
                if facility_detector:
                    facilities = facility_detector.detect_facility(image_np)
                    for facility in facilities:
                        local_map_generator.add_landmark(
                            facility.type.value,
                            (0, 0),  # 位置需要根据实际情况计算
                            facility.label,
                            facility.confidence
                        )
        
        # 获取当前地图
        local_map = local_map_generator.get_map()
        
        return jsonify({
            'success': True,
            'map': local_map.to_dict() if local_map else None
        })
    except Exception as e:
        logger.error(f"本地地图生成错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/detect/comprehensive', methods=['POST'])
def comprehensive_detection():
    """综合检测 - 同时运行所有视觉检测模块"""
    try:
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        results = {}
        
        # 1. 基础视觉识别
        if vision_engine:
            try:
                vision_results = vision_engine.detect_and_recognize(image_np)
                results['vision'] = {
                    'detections': vision_results.get('detections', []),
                    'ocr_results': vision_results.get('ocr_results', [])
                }
            except Exception as e:
                results['vision'] = {'error': str(e)}
        
        # 2. 台阶检测
        if step_detector:
            try:
                step_result = step_detector.detect_step(image_np)
                results['step'] = step_result if step_result else {'detected': False}
            except Exception as e:
                results['step'] = {'error': str(e)}
        
        # 3. 标识牌检测
        if signboard_detector:
            try:
                signboards = signboard_detector.detect_signboards(image_np)
                results['signboard'] = [r.to_dict() for r in signboards] if signboards else []
            except Exception as e:
                results['signboard'] = {'error': str(e)}
        
        # 4. 危险检测
        if hazard_detector:
            try:
                # 传递YOLO检测结果用于过滤误报
                detected_objects = results.get('vision', {}).get('detections', [])
                hazards = hazard_detector.detect_hazards(image_np, detected_objects=detected_objects)
                results['hazard'] = [r.to_dict() for r in hazards] if hazards else []
            except Exception as e:
                results['hazard'] = {'error': str(e)}
        
        # 5. 公共设施检测
        if facility_detector:
            try:
                facilities = facility_detector.detect_facility(image_np)
                results['facility'] = [r.to_dict() for r in facilities] if facilities else []
            except Exception as e:
                results['facility'] = {'error': str(e)}
        
        # 6. 红绿灯检测
        if traffic_light_detector:
            try:
                traffic_light = traffic_light_detector.detect_traffic_light(image_np)
                results['traffic_light'] = traffic_light.to_dict() if traffic_light else None
            except Exception as e:
                results['traffic_light'] = {'error': str(e)}
        
        # 7. 人群密度检测
        if crowd_density_detector:
            try:
                density = crowd_density_detector.detect_density(image_np)
                results['crowd_density'] = density.to_dict() if density else None
            except Exception as e:
                results['crowd_density'] = {'error': str(e)}
        
        # 8. 排队检测
        if queue_detector:
            try:
                queue = queue_detector.detect_queue(image_np)
                results['queue'] = queue.to_dict() if queue else None
            except Exception as e:
                results['queue'] = {'error': str(e)}
        
        # 9. 门牌号识别
        if doorplate_reader:
            try:
                doorplates = doorplate_reader.read_doorplate(image_np)
                results['doorplate'] = [d.to_dict() for d in doorplates] if doorplates else []
            except Exception as e:
                results['doorplate'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'results': results,
            'timestamp': time.time()
        })
    except Exception as e:
        logger.error(f"综合检测错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/recognize/voice', methods=['POST'])
def recognize_voice():
    """语音识别（改进版：音频格式标准化）"""
    try:
        if whisper_recognizer is None:
            return api_error('语音识别器未初始化', status_code=500)
        
        if 'audio' not in request.files:
            return api_error('未上传音频', status_code=400)
        
        # 保存临时文件
        audio_file = request.files['audio']
        mime_type = audio_file.content_type or 'audio/webm'
        
        # 保存原始音频
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # 音频格式转换（统一转换为WAV格式，16kHz，单声道）
            converted_path = tmp_path
            try:
                import subprocess
                import os
                
                # 检查是否需要转换（非WAV格式需要转换）
                if not mime_type.startswith('audio/wav') and not tmp_path.endswith('.wav'):
                    wav_path = tmp_path + '.wav'
                    # 使用ffmpeg转换（如果可用）
                    try:
                        subprocess.run([
                            'ffmpeg', '-i', tmp_path,
                            '-ar', '16000',  # 采样率16kHz
                            '-ac', '1',      # 单声道
                            '-f', 'wav',     # WAV格式
                            '-y',            # 覆盖输出文件
                            wav_path
                        ], check=True, capture_output=True, timeout=10)
                        converted_path = wav_path
                        logger.info(f"音频格式转换成功: {mime_type} -> WAV")
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        # ffmpeg不可用，尝试直接使用（Whisper支持多种格式）
                        logger.warning("ffmpeg不可用，使用原始音频格式")
                        converted_path = tmp_path
            except Exception as e:
                logger.warning(f"音频格式转换失败，使用原始格式: {e}")
                converted_path = tmp_path
            
            # 加载模型（如果未加载）
            if not whisper_recognizer.is_loaded:
                whisper_recognizer.load_model()
            
            # 识别（使用优化的参数）
            result = whisper_recognizer.model.transcribe(
                converted_path,
                language="zh",
                task="transcribe",
                temperature=0.0,  # 降低随机性，提高一致性
                beam_size=5,      # 束搜索大小
                best_of=5,        # 候选数量
                fp16=False        # 使用FP32提高准确率（如果CPU）
            )
            
            text = result.get("text", "").strip()
            
            # 提取详细结果
            details = {
                "language": result.get("language", "zh"),
                "duration": result.get("segments", [{}])[0].get("duration", 0) if result.get("segments") else 0,
                "confidence": whisper_recognizer._calculate_confidence(result),
                "segments": [
                    {
                        "start": seg.get("start", 0),
                        "end": seg.get("end", 0),
                        "text": seg.get("text", "").strip(),
                        "confidence": 1.0 - seg.get("no_speech_prob", 0.5)
                    }
                    for seg in result.get("segments", [])
                ]
            }
            
            logger.info(f"✅ 识别成功: {text} (置信度: {details['confidence']:.2f})")
            
            # 记录日志
            if log_manager:
                try:
                    log_manager.log_voice_intent(
                        intent="voice_recognition",
                        content=text,
                        system_response="语音识别完成",
                        metadata={
                            "language": details.get("language", "zh"),
                            "confidence": details.get("confidence", 0.0),
                            "segments_count": len(details.get("segments", []))
                        }
                    )
                except Exception as e:
                    logger.warning(f"⚠️ 记录语音日志失败: {e}")
            
            return jsonify({
                'success': True,
                'text': text,
                'details': details,
                'audio_format': mime_type
            })
        finally:
            # 清理临时文件
            for path in [tmp_path, tmp_path + '.wav']:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                    except:
                        pass
    except Exception as e:
        logger.error(f"语音识别错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """语音合成（支持长文本自动分段）"""
    try:
        import asyncio
        import edge_tts
        
        data = request.json
        text = data.get('text', '')
        style_str = data.get('style', 'cheerful')
        
        if not text:
            return api_error('未提供文本', status_code=400)
        
        # Edge-TTS单次请求限制：5000字符
        MAX_CHARS_PER_REQUEST = 5000
        
        # 风格映射 - rate需要是字符串格式，如"+20%"表示加快20%
        style_map = {
            'cheerful': ('zh-CN-XiaoxiaoNeural', '+20%'),  # 加快20%
            'calm': ('zh-CN-XiaoyiNeural', '-5%'),         # 减慢5%
            'urgent': ('zh-CN-XiaoxiaoNeural', '+50%'),    # 加快50%
            'empathetic': ('zh-CN-YunxiNeural', '-10%'),   # 减慢10%
            'angry': ('zh-CN-YunjianNeural', '+30%'),      # 加快30%
            'gentle': ('zh-CN-YunxiNeural', '-15%')        # 减慢15%
        }
        
        voice, rate = style_map.get(style_str, style_map['cheerful'])
        
        start_time = time.time()
        
        # ========== 快速缓存检查（优化：优先使用缓存）==========
        if fast_tts_cache:
            cached_audio = fast_tts_cache.get_cached_audio(text, voice, rate)
            if cached_audio:
                cache_time = time.time() - start_time
                logger.info(f"⚡ 缓存命中！延迟: {cache_time*1000:.0f}ms - {text[:30]}...")
                
                # 转换为base64
                audio_base64 = base64.b64encode(cached_audio).decode('utf-8')
                
                # 记录日志
                if log_manager:
                    try:
                        log_manager.log_tts_output(
                            text=text[:100] + "..." if len(text) > 100 else text,
                            success=True,
                            metadata={
                                "text_length": len(text),
                                "style": style_str,
                                "cached": True,
                                "latency_ms": cache_time * 1000
                            }
                        )
                    except Exception as e:
                        logger.warning(f"⚠️ 记录TTS日志失败: {e}")
                
                return jsonify({
                    'success': True,
                    'audio': audio_base64,
                    'cached': True,
                    'latency_ms': round(cache_time * 1000, 2)
                })
        
        # ========== 未缓存，需要生成（优化：异步保存到缓存）==========
        logger.info(f"🔄 生成新音频: {text[:30]}... (风格: {style_str})")
        def split_text(text, max_length):
            """智能分段：优先在句号、问号、感叹号处分割"""
            if len(text) <= max_length:
                return [text]
            
            segments = []
            current_segment = ""
            
            # 按句子分割（中英文标点）
            import re
            sentences = re.split(r'([。！？.!?])', text)
            
            for i in range(0, len(sentences), 2):
                sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
                
                # 如果当前段落加上新句子不超过限制
                if len(current_segment) + len(sentence) <= max_length:
                    current_segment += sentence
                else:
                    # 保存当前段落
                    if current_segment:
                        segments.append(current_segment.strip())
                    # 如果单个句子就超过限制，强制分割
                    if len(sentence) > max_length:
                        # 按字符强制分割
                        for j in range(0, len(sentence), max_length):
                            segments.append(sentence[j:j+max_length])
                        current_segment = ""
                    else:
                        current_segment = sentence
            
            # 添加最后一段
            if current_segment:
                segments.append(current_segment.strip())
            
            return segments
        
        # 生成单段语音
        async def generate_audio_segment(segment_text):
            communicate = edge_tts.Communicate(text=segment_text, voice=voice, rate=rate)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        
        # 检查是否需要分段
        text_length = len(text)
        if text_length <= MAX_CHARS_PER_REQUEST:
            # 单段处理
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_data = loop.run_until_complete(generate_audio_segment(text))
            loop.close()
        else:
            # 分段处理
            logger.info(f"文本长度 {text_length} 字符，超过限制 {MAX_CHARS_PER_REQUEST}，开始分段处理")
            segments = split_text(text, MAX_CHARS_PER_REQUEST)
            logger.info(f"分为 {len(segments)} 段")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 逐段生成并拼接
            audio_segments = []
            for i, segment in enumerate(segments):
                logger.info(f"正在合成第 {i+1}/{len(segments)} 段（{len(segment)} 字符）")
                segment_audio = loop.run_until_complete(generate_audio_segment(segment))
                audio_segments.append(segment_audio)
                # 段之间添加短暂静音（可选）
                # silence = b'\x00' * (16000 * 0.3)  # 0.3秒静音
                # audio_segments.append(silence)
            
            loop.close()
            
            # 拼接所有音频段
            audio_data = b"".join(audio_segments)
            logger.info(f"分段合成完成，总音频长度: {len(audio_data)} 字节")
        
        # 保存到缓存（后台异步，不阻塞）
        if fast_tts_cache and audio_data:
            try:
                fast_tts_cache.save_cached_audio(text, voice, rate, audio_data)
            except Exception as e:
                logger.warning(f"⚠️ 保存缓存失败: {e}")
        
        generation_time = time.time() - start_time
        
        if audio_data:
            # 转换为base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 记录日志
            if log_manager:
                try:
                    log_manager.log_tts_output(
                        text=text[:100] + "..." if len(text) > 100 else text,  # 只记录前100字符
                        success=True,
                        metadata={
                            "text_length": text_length,
                            "style": style_str,
                            "cached": False,
                            "latency_ms": generation_time * 1000
                        }
                    )
                except Exception as e:
                    logger.warning(f"⚠️ 记录TTS日志失败: {e}")
            
            logger.info(f"✅ TTS生成完成，延迟: {generation_time*1000:.0f}ms")
            
            return jsonify({
                'success': True,
                'audio': audio_base64,
                'cached': False,
                'latency_ms': generation_time * 1000
            })
        else:
            return api_error('语音合成失败', status_code=500)
    except Exception as e:
        logger.error(f"TTS错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/performance/metrics', methods=['GET'])
def get_performance_metrics():
    """获取性能指标"""
    try:
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
        except:
            memory_mb = 0
        
        # 计算延迟统计
        vision_latencies = performance_metrics.get('vision_latency', [])
        audio_latencies = performance_metrics.get('audio_latency', [])
        
        def calc_stats(latencies):
            if not latencies:
                return {'avg': 0, 'p95': 0, 'p99': 0, 'min': 0, 'max': 0, 'count': 0}
            
            sorted_latencies = sorted(latencies[-100:])  # 最近100次
            count = len(sorted_latencies)
            avg = sum(sorted_latencies) / count if count > 0 else 0
            p95_index = int(count * 0.95)
            p99_index = int(count * 0.99)
            
            return {
                'avg': round(avg, 2),
                'p95': round(sorted_latencies[p95_index] if p95_index < count else 0, 2),
                'p99': round(sorted_latencies[p99_index] if p99_index < count else 0, 2),
                'min': round(sorted_latencies[0] if count > 0 else 0, 2),
                'max': round(sorted_latencies[-1] if count > 0 else 0, 2),
                'count': count
            }
        
        vision_stats = calc_stats(vision_latencies)
        audio_stats = calc_stats(audio_latencies)
        
        # 计算FPS
        fps_history = performance_metrics.get('fps', [])
        current_fps = fps_history[-1] if fps_history else 0
        avg_fps = sum(fps_history[-30:]) / len(fps_history[-30:]) if fps_history else 0
        
        return jsonify({
            'success': True,
            'metrics': {
                'memory_mb': round(memory_mb, 2),
                'vision': vision_stats,
                'audio': audio_stats,
                'fps': {
                    'current': round(current_fps, 1),
                    'average': round(avg_fps, 1)
                },
                'degrade_level': graceful_degrader.current_level.value if graceful_degrader else 'normal'
            }
        })
    except Exception as e:
        logger.error(f"获取性能指标错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/tts/cache/stats', methods=['GET'])
def tts_cache_stats():
    """获取TTS缓存统计信息"""
    try:
        if fast_tts_cache:
            stats = fast_tts_cache.get_cache_stats()
            return api_success({
                'stats': stats
            })
        else:
            return api_error('TTS缓存系统未初始化', status_code=500)
    except Exception as e:
        logger.error(f"获取缓存统计失败: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'modules': {
            'vision_engine': vision_engine is not None,
            'step_detector': step_detector is not None,
            'signboard_detector': signboard_detector is not None,
            'hazard_detector': hazard_detector is not None,
            'whisper_recognizer': whisper_recognizer is not None,
            'tts_manager': tts_manager is not None,
            'navigation_manager': navigation_manager is not None,
            'path_planner': path_planner is not None,
            'scene_memory_system': scene_memory_system is not None,
            'facility_detector': facility_detector is not None,
            'traffic_light_detector': traffic_light_detector is not None,
            'crowd_density_detector': crowd_density_detector is not None,
            'queue_detector': queue_detector is not None,
            'doorplate_reader': doorplate_reader is not None,
            'local_map_generator': local_map_generator is not None,
            'log_manager': log_manager is not None
        }
    })

@app.route('/api/navigation/plan', methods=['POST'])
def plan_route():
    """路径规划API"""
    try:
        if path_planner is None:
            return api_error('路径规划器未初始化', status_code=500)
        
        data = request.get_json()
        start = data.get('start', '')
        destinations = data.get('destinations', [])
        
        if not start or not destinations:
            return api_error('缺少起点或目的地参数', status_code=400)
        
        if not isinstance(destinations, list):
            destinations = [destinations]
        
        result = path_planner.plan_route(start, destinations)
        
        return api_success({
            'route': result
        })
    except Exception as e:
        logger.error(f"路径规划错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/start', methods=['POST'])
def start_navigation():
    """开始导航"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        data = request.get_json()
        destination = data.get('destination', '')
        route_segments = data.get('route_segments')  # 可选的路径段列表
        
        if not destination:
            return api_error('缺少目的地参数', status_code=400)
        
        success = navigation_manager.start_navigation(destination, route_segments)
        
        if success:
            status = navigation_manager.get_status()
            
            # 记录日志
            if log_manager:
                try:
                    log_manager.log_navigation(
                        action="start_navigation",
                        destination=destination,
                        path_info=route_segments,
                        system_response=f"导航已启动到{destination}"
                    )
                except Exception as e:
                    logger.warning(f"⚠️ 记录导航日志失败: {e}")
            
            return api_success({
                'status': status
            })
        else:
            return api_error('导航启动失败，可能已有导航在进行中', status_code=400)
    except Exception as e:
        logger.error(f"启动导航错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/update_position', methods=['POST'])
def update_position():
    """更新位置（支持障碍检测）"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        image_data = data.get('image')  # 可选的图片数据，用于障碍检测
        
        if lat is None or lng is None:
            return api_error('缺少位置参数', status_code=400)
        
        # 如果提供了图片，进行障碍检测
        detected_hazards = None
        if image_data and hazard_detector:
            try:
                # 解码base64图片
                import base64
                image_bytes = base64.b64decode(image_data.split(',')[-1] if ',' in image_data else image_data)
                image_np = image_to_numpy(image_bytes)
                if image_np is not None:
                    # 如果可能，传递YOLO检测结果用于过滤误报
                    detected_objects = []
                    if vision_engine:
                        try:
                            vision_results = vision_engine.detect_and_recognize(image_np)
                            detected_objects = vision_results.get('detections', [])
                        except:
                            pass
                    hazards = hazard_detector.detect_hazards(image_np, detected_objects=detected_objects)
                    detected_hazards = [h.to_dict() for h in hazards] if hazards else []
            except Exception as e:
                logger.warning(f"⚠️ 障碍检测失败: {e}")
        
        navigation_manager.update_position(lat, lng, detected_hazards)
        status = navigation_manager.get_status()
        is_idle = navigation_manager.check_idle()
        
        return api_success({
            'status': status,
            'is_idle': is_idle,
            'detected_hazards': detected_hazards or []
        })
    except Exception as e:
        logger.error(f"更新位置错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/status', methods=['GET'])
def get_navigation_status():
    """获取导航状态"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        status = navigation_manager.get_status()
        is_idle = navigation_manager.check_idle() if status else False
        
        return api_success({
            'status': status,
            'is_idle': is_idle
        })
    except Exception as e:
        logger.error(f"获取导航状态错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/pause', methods=['POST'])
def pause_navigation():
    """暂停导航"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        data = request.get_json()
        reason = data.get('reason', '用户暂停')
        
        success = navigation_manager.pause_navigation(reason)
        
        if success:
            status = navigation_manager.get_status()
            return api_success({
                'status': status
            })
        else:
            return api_error('暂停失败', status_code=400)
    except Exception as e:
        logger.error(f"暂停导航错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/resume', methods=['POST'])
def resume_navigation():
    """恢复导航"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        success = navigation_manager.resume_navigation()
        
        if success:
            status = navigation_manager.get_status()
            return api_success({
                'status': status
            })
        else:
            return api_error('恢复失败', status_code=400)
    except Exception as e:
        logger.error(f"恢复导航错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/cancel', methods=['POST'])
def cancel_navigation():
    """取消导航"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        data = request.get_json()
        reason = data.get('reason', '用户取消')
        
        success = navigation_manager.cancel_navigation(reason)
        
        if success:
            status = navigation_manager.get_status()
            return api_success({
                'status': status
            })
        else:
            return api_error('取消失败', status_code=400)
    except Exception as e:
        logger.error(f"取消导航错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/complete', methods=['POST'])
def complete_navigation():
    """完成导航"""
    try:
        if navigation_manager is None:
            return api_error('导航管理器未初始化', status_code=500)
        
        success = navigation_manager.complete_navigation()
        
        if success:
            status = navigation_manager.get_status()
            return api_success({
                'status': status
            })
        else:
            return api_error('完成失败', status_code=400)
    except Exception as e:
        logger.error(f"完成导航错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/describe_scene', methods=['POST'])
def describe_scene():
    """
    场景描述接口
    - 输入：图片（form-data: image） 或 base64（form-data: image_base64）
    - 输出：自然语言场景描述 + 结构化信息
    前端对口：VisionBridge.requestSceneDescription()
    """
    try:
        if scene_describe_service is None:
            return api_error(
                "场景描述服务未初始化",
                details={"code": "SCENE_SERVICE_NOT_INITIALIZED"},
                status_code=500
            )

        # 支持两种输入：
        # 1) multipart/form-data, files['image']
        # 2) application/json, body.image_base64
        image_np = None

        if 'image' in request.files:
            file = request.files['image']
            image_np = image_to_numpy(file.read())
        else:
            data = request.get_json(silent=True) or {}
            image_b64 = data.get('image_base64')
            if image_b64:
                try:
                    if ',' in image_b64:
                        image_b64 = image_b64.split(',', 1)[1]
                    img_bytes = base64.b64decode(image_b64)
                    image_np = image_to_numpy(img_bytes)
                except Exception as e:
                    logger.warning(f"解码 base64 图片失败: {e}")
                    image_np = None

        if image_np is None:
            return api_error(
                "未提供有效图片",
                details={"code": "INVALID_IMAGE"},
                status_code=400
            )

        # 调用场景描述服务（支持多模型融合）
        # 如果传入了 image_base64，优先传给引擎以启用融合
        image_b64_for_fusion = None
        if 'image' not in request.files:
            data = request.get_json(silent=True) or {}
            image_b64_for_fusion = data.get('image_base64')
        
        # 直接调用 scene_description_engine（如果可用）以支持融合
        if scene_description_engine is not None:
            try:
                desc_result = scene_description_engine.describe(
                    image_np, 
                    nav_state=None,
                    image_base64=image_b64_for_fusion,
                    task_hint="导航安全"
                )
                # 转换为 scene_describe_service 格式
                desc = {
                    "scene_type": "unknown",
                    "scene_tags": desc_result.get("tags") or desc_result.get("scene_tags") or [],
                    "short_description": desc_result.get("description") or desc_result.get("summary") or "",
                    "details": [],
                    "elements": desc_result
                }
            except Exception as e:
                logger.warning(f"直接调用 scene_description_engine 失败，回退到 scene_describe_service: {e}")
                desc = scene_describe_service.describe_scene_from_image(image_np)
        else:
            desc = scene_describe_service.describe_scene_from_image(image_np)

        # 记录日志（可选）
        if log_manager:
            try:
                log_manager.log_visual_event(
                    event_type="scene_description",
                    detection_result={
                        "scene_type": desc.get("scene_type"),
                        "scene_tags": desc.get("scene_tags"),
                    },
                    system_response=desc.get("short_description", "")
                )
            except Exception as e:
                logger.warning(f"⚠️ 记录场景描述日志失败: {e}")

        return api_success(desc)

    except Exception as e:
        logger.error(
            f"场景描述错误: {e}",
            extra={"module_name": "api", "meta": {"endpoint": "/api/navigation/describe_scene"}}
        )
        # 用 details.code 告诉前端是哪个模块炸了
        return api_error(
            "场景描述出现异常",
            details={
                "code": "SCENE_DESCRIBE_FAILED",
                "exception_type": type(e).__name__,
            },
            status_code=500
        )

@app.route('/api/navigation/visual_guidance', methods=['POST'])
def visual_guidance():
    """实时视觉导航指引（基于摄像头画面）"""
    try:
        if vision_engine is None:
            return api_error('视觉引擎未初始化', status_code=500)
        
        if scene_memory_system is None:
            return api_error('场景记忆系统未初始化', status_code=500)
        
        file = request.files.get('image')
        if not file:
            return api_error('未上传图片', status_code=400)
        
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return api_error('图片格式错误', status_code=400)
        
        start_time = time.time()
        
        # ========== 优化1: 显著性ROI提取（提高检测速度）==========
        use_roi_optimization = saliency_roi is not None
        vision_results = None
        
        if use_roi_optimization:
            try:
                # 提取高显著性区域
                roi_regions = saliency_roi.extract_roi(image_np, top_k=5)
                
                if roi_regions and len(roi_regions) > 0:
                    # 只在ROI区域进行检测（提高速度）
                    all_objects = []
                    all_texts = []
                    
                    for roi in roi_regions:
                        x, y, w, h = roi['bbox']
                        roi_image = image_np[y:y+h, x:x+w]
                        
                        if roi_image.size == 0:
                            continue
                        
                        # 在ROI区域进行检测
                        try:
                            roi_results = vision_engine.detect_and_recognize(roi_image)
                            
                            # 调整坐标（从ROI坐标转换到原图坐标）
                            for obj in roi_results.get('detections', []):
                                if 'bbox' in obj:
                                    orig_x, orig_y, orig_w, orig_h = obj['bbox']
                                    obj['bbox'] = (orig_x + x, orig_y + y, orig_w, orig_h)
                                all_objects.append(obj)
                            
                            for text in roi_results.get('ocr_results', []):
                                if 'bbox' in text:
                                    orig_x, orig_y, orig_w, orig_h = text['bbox']
                                    text['bbox'] = (orig_x + x, orig_y + y, orig_w, orig_h)
                                all_texts.append(text)
                        except Exception as e:
                            logger.warning(f"ROI区域检测失败: {e}")
                    
                    vision_results = {
                        'detections': all_objects,
                        'ocr_results': all_texts,
                        'processing_time': (time.time() - start_time),
                        'roi_optimized': True
                    }
                else:
                    # ROI提取失败，使用全图检测
                    vision_results = vision_engine.detect_and_recognize(image_np)
                    vision_results['roi_optimized'] = False
            except Exception as e:
                logger.warning(f"显著性ROI优化失败，使用全图检测: {e}")
                vision_results = vision_engine.detect_and_recognize(image_np)
                vision_results['roi_optimized'] = False
        else:
            # 未启用ROI优化，使用全图检测
            vision_results = vision_engine.detect_and_recognize(image_np)
            vision_results['roi_optimized'] = False
        
        # 1. 视觉识别：检测物体和文字（已完成）
        
        # 2. 检测关键节点（门牌、标识牌等）
        node_detector = scene_memory_system.node_detector
        detected_nodes = node_detector.detect_nodes(image_np) if node_detector else []
        
        # 3. 检测标识牌
        signboard_results = []
        if signboard_detector:
            try:
                signboard_results = signboard_detector.detect_signboards(image_np)
            except:
                pass
        
        # 4. 检测台阶和危险
        step_detected = False
        hazards_detected = []
        if step_detector:
            try:
                step_result = step_detector.detect_step(image_np)
                step_detected = step_result is not None
            except:
                pass
        
        if hazard_detector:
            try:
                # 传递YOLO检测结果，用于过滤人脸误报
                detected_objects = vision_results.get('detections', [])
                hazards_detected = hazard_detector.detect_hazards(image_np, detected_objects=detected_objects)
            except:
                pass
        
        # ========== 优化2: 时序融合（提高稳定性，减少误检）==========
        detection_data = {
            'objects': vision_results.get('detections', []),
            'texts': vision_results.get('ocr_results', []),
            'signboards': [{'type': r.type.value, 'bbox': r.bbox, 'confidence': r.confidence} 
                          for r in signboard_results] if signboard_results else [],
            'step_detected': step_detected,
            'hazards': [{'type': h.type.value, 'bbox': h.bbox, 'severity': h.severity.value, 'confidence': h.confidence}
                       for h in hazards_detected] if hazards_detected else []
        }
        
        stable_detection = detection_data  # 默认使用原始检测
        if temporal_fusion:
            try:
                stable_detection = temporal_fusion.fuse(detection_data)
                logger.debug(f"时序融合完成，稳定性得分: {stable_detection.get('stability_score', 0):.2f}")
            except Exception as e:
                logger.warning(f"时序融合失败: {e}")
        
        # 更新检测结果（使用稳定后的结果）
        vision_results['detections'] = stable_detection.get('objects', [])
        vision_results['ocr_results'] = stable_detection.get('texts', [])
        signboard_results_stable = stable_detection.get('signboards', [])
        step_detected = stable_detection.get('step_detected', step_detected)
        hazards_detected_stable = stable_detection.get('hazards', [])
        
        # ========== 优化3: 视觉-语言融合（如果有语音指令）==========
        voice_command = request.form.get('voice_command')  # 可选参数
        fusion_decision = None
        
        if voice_command and visual_language_fusion:
            try:
                fusion_detection = {
                    'objects': [{'class': obj.get('class', ''), 'bbox': obj.get('bbox', (0,0,0,0)), 
                               'confidence': obj.get('confidence', 0.0)} 
                              for obj in stable_detection.get('objects', [])],
                    'texts': [text.get('text', '') for text in stable_detection.get('texts', [])],
                    'signboards': signboard_results_stable
                }
                
                fusion_decision = visual_language_fusion.fuse(fusion_detection, voice_command)
                if fusion_decision:
                    logger.info(f"视觉-语言融合成功: {fusion_decision.get('message', '')}")
            except Exception as e:
                logger.warning(f"视觉-语言融合失败: {e}")
        
        # 5. 生成前进指引
        guidance_messages = []
        guidance_direction = "forward"  # forward, left, right, stop
        
        # 提取OCR文本（用于后续处理）
        ocr_texts = [r.get('text', '') for r in vision_results.get('ocr_results', [])]
        
        # 如果视觉-语言融合有结果，优先使用融合后的决策
        if fusion_decision:
            guidance_direction = fusion_decision.get('direction', 'forward')
            guidance_messages.append(fusion_decision.get('message', ''))
        else:
            # 分析OCR结果，查找方向指示
            all_text = ' '.join(ocr_texts).lower()
            
            # 检测方向关键词
            if any(keyword in all_text for keyword in ['左', 'left', '←']):
                guidance_direction = "left"
                guidance_messages.append("检测到左侧标识，请向左转")
            elif any(keyword in all_text for keyword in ['右', 'right', '→']):
                guidance_direction = "right"
                guidance_messages.append("检测到右侧标识，请向右转")
            elif any(keyword in all_text for keyword in ['直行', 'straight', 'forward', '↑']):
                guidance_direction = "forward"
                guidance_messages.append("请直行")
        
        # 检测门牌号/房间号
        room_numbers = []
        for text in ocr_texts:
            import re
            # 匹配房间号模式：数字+室/号/room等
            room_match = re.search(r'(\d+)[室号]|room\s*(\d+)', text, re.IGNORECASE)
            if room_match:
                room_num = room_match.group(1) or room_match.group(2)
                room_numbers.append(room_num)
        
        if room_numbers:
            guidance_messages.append(f"检测到房间号：{', '.join(room_numbers)}")
        
        # 检测标识牌（使用稳定后的结果）
        if signboard_results_stable:
            signboard_types = [r.get('type', '') for r in signboard_results_stable]
            if 'toilet' in signboard_types or 'restroom' in signboard_types:
                guidance_messages.append("检测到洗手间标识")
            if 'elevator' in signboard_types or 'lift' in signboard_types:
                guidance_messages.append("检测到电梯标识")
            if 'exit' in signboard_types or '出口' in signboard_types:
                guidance_messages.append("检测到出口标识")
        
        # 检测台阶警告
        if step_detected:
            guidance_direction = "stop"
            guidance_messages.append("⚠️ 前方有台阶，请小心")
        
        # 检测危险警告（使用稳定后的结果）
        if hazards_detected_stable:
            critical_hazards = [h for h in hazards_detected_stable if h.get('severity', '') in ['critical', 'high']]
            if critical_hazards:
                guidance_direction = "stop"
                guidance_messages.append(f"⚠️ 检测到{len(critical_hazards)}个危险区域，请谨慎前行")
        
        # 如果没有检测到明确的指引，提供通用建议
        if not guidance_messages:
            # 分析检测到的物体
            detections = vision_results.get('detections', [])
            ocr_texts = [r.get('text', '') for r in vision_results.get('ocr_results', [])]
            
            if detections:
                # 提取物体类型
                object_types = [d.get('class', '') for d in detections if d.get('class')]
                if object_types:
                    unique_types = list(set(object_types))[:3]  # 最多显示3种
                    guidance_messages.append(f"检测到前方有：{', '.join(unique_types)}，请保持直行并注意观察")
                else:
                    guidance_messages.append("检测到前方有物体，请保持直行并注意观察")
            elif ocr_texts:
                # 有文字但无明确方向
                guidance_messages.append("检测到文字信息，前方道路畅通，请继续前行")
            else:
                # 什么都没有检测到
                guidance_messages.append("前方道路畅通，请继续前行")
        
        # ========== SceneGraph 构建和推理 ==========
        scene_graph_result = None
        sg_reason_result = None
        floor_graph_result = None
        merged_graph_result = None
        map_kind = None
        
        try:
            from core.scene_graph import SceneGraphBuilder
            from core.scene_reasoner_sg import SceneGraphReasoner
            from core.structure_map_parser import FloorPlanParser, SceneGraphFusion
            
            # 1. 组装 YOLO / OCR 标准格式
            yolo_objects = []
            detections = vision_results.get('detections', [])
            for i, det in enumerate(detections):
                bbox = det.get('bbox', (0, 0, 0, 0))
                if isinstance(bbox, tuple) and len(bbox) == 4:
                    # 归一化 bbox（如果还没有归一化）
                    h, w = image_np.shape[:2]
                    x1, y1, x2, y2 = bbox
                    # 检查是否已经归一化（值在0-1之间）
                    if x2 > 1.0 or y2 > 1.0:
                        bbox_norm = [x1/w, y1/h, x2/w, y2/h]
                    else:
                        bbox_norm = list(bbox)
                else:
                    bbox_norm = [0.0, 0.0, 0.0, 0.0]
                
                yolo_objects.append({
                    "id": i,
                    "cls": det.get("class") or det.get("label") or "unknown",
                    "confidence": float(det.get("confidence", 0.5)),
                    "bbox": bbox_norm,
                    "distance_m": det.get("distance_m") or det.get("distance"),
                })
            
            ocr_blocks = []
            for blk in vision_results.get('ocr_results', []):
                bbox = blk.get('bbox', (0, 0, 0, 0))
                if isinstance(bbox, tuple) and len(bbox) == 4:
                    h, w = image_np.shape[:2]
                    x1, y1, x2, y2 = bbox
                    # 检查是否已经归一化
                    if x2 > 1.0 or y2 > 1.0:
                        bbox_norm = [x1/w, y1/h, x2/w, y2/h]
                    else:
                        bbox_norm = list(bbox)
                else:
                    bbox_norm = [0.0, 0.0, 0.0, 0.0]
                
                ocr_blocks.append({
                    "text": blk.get("text", ""),
                    "confidence": float(blk.get("confidence", 1.0)),
                    "bbox": bbox_norm,
                })
            
            frame_meta = {
                "timestamp": time.time(),
                "heading_deg": 0.0,  # 实际应从IMU获取
            }
            
            # 2. 构建 SceneGraph（真实场景）
            scene_graph = SceneGraphBuilder.build(
                yolo_objects=yolo_objects,
                ocr_blocks=ocr_blocks,
                frame_meta=frame_meta,
            )
            scene_graph_result = scene_graph.to_dict()
            
            # 2.5. 检查是否有结构图 OCR（从请求参数中获取）
            structure_ocr = request.form.get('structure_ocr')  # JSON 字符串或 None
            structure_ocr_blocks = []
            if structure_ocr:
                try:
                    import json
                    if isinstance(structure_ocr, str):
                        structure_data = json.loads(structure_ocr)
                    else:
                        structure_data = structure_ocr
                    structure_ocr_blocks = structure_data.get('blocks', [])
                except Exception as e:
                    logger.warning(f"[SceneGraph] 解析结构图 OCR 失败: {e}")
            
            # 如果没有显式提供结构图 OCR，尝试自动检测（OCR 结果中是否有大量结构图特征）
            if not structure_ocr_blocks and len(ocr_blocks) > 5:
                # 检查 OCR 文本中是否包含结构图特征（房间号、区域名等）
                structure_keywords = ["科", "诊室", "门诊", "L1", "L2", "负一层", "站台", "出入口"]
                structure_text_count = sum(1 for blk in ocr_blocks 
                                         if any(kw in blk.get("text", "") for kw in structure_keywords))
                if structure_text_count >= 3:  # 至少3个结构图特征文字
                    logger.info("[SceneGraph] 自动检测到结构图特征，尝试解析")
                    structure_ocr_blocks = ocr_blocks
            
            # 3. 如果有结构图 OCR，解析并融合
            scene_for_reason = scene_graph
            if structure_ocr_blocks:
                try:
                    # 归一化结构图 OCR 的 bbox（如果需要）
                    normalized_structure_blocks = []
                    for blk in structure_ocr_blocks:
                        bbox = blk.get("bbox", [0, 0, 0, 0])
                        if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
                            x1, y1, x2, y2 = bbox
                            # 检查是否已经归一化
                            if x2 > 1.0 or y2 > 1.0:
                                h, w = image_np.shape[:2]
                                bbox_norm = [x1/w, y1/h, x2/w, y2/h]
                            else:
                                bbox_norm = list(bbox)
                        else:
                            bbox_norm = [0.0, 0.0, 0.0, 0.0]
                        
                        normalized_structure_blocks.append({
                            "text": blk.get("text", ""),
                            "confidence": float(blk.get("confidence", 1.0)),
                            "bbox": bbox_norm
                        })
                    
                    # 解析结构图
                    floor_graph, map_kind = FloorPlanParser.parse_floorplan(normalized_structure_blocks)
                    floor_graph_result = floor_graph.to_dict()
                    
                    # 记录结构图日志
                    if log_manager:
                        log_manager.log_visual_event(
                            event_type="floorplan_graph",
                            detection_result={
                                "map_kind": map_kind,
                                "graph": floor_graph_result
                            }
                        )
                    
                    # 融合真实场景和结构图
                    merged_graph = SceneGraphFusion.merge(scene_graph, floor_graph)
                    merged_graph_result = merged_graph.to_dict()
                    
                    # 记录融合图日志
                    if log_manager:
                        log_manager.log_visual_event(
                            event_type="scene_graph_merged",
                            detection_result=merged_graph_result
                        )
                    
                    # 使用融合后的图进行推理
                    scene_for_reason = merged_graph
                    logger.info(f"[SceneGraph] 结构图融合完成: map_kind={map_kind}, "
                              f"merged_nodes={len(merged_graph.nodes)}, "
                              f"merged_relations={len(merged_graph.relations)}")
                    
                except Exception as e:
                    logger.error(f"[SceneGraph] 结构图解析或融合错误: {e}", exc_info=True)
            
            # 4. 推理（使用融合后的图或原始图）
            sg_reason_result = SceneGraphReasoner.reason(scene_for_reason)
            
            # 4. 写入日志
            if log_manager:
                log_manager.log_visual_event(
                    event_type="scene_graph",
                    detection_result=scene_graph_result
                )
                log_manager.log_visual_event(
                    event_type="scene_reason",
                    detection_result=sg_reason_result
                )
            
            # 5. 根据推理结果更新指引（如果 SceneGraph 推理有更好的建议）
            if sg_reason_result and sg_reason_result.get("message"):
                sg_direction = sg_reason_result.get("primary_direction", "forward")
                sg_message = sg_reason_result.get("message", "")
                sg_confidence = sg_reason_result.get("confidence", 0.0)
                
                # 如果 SceneGraph 推理置信度较高，优先使用其建议
                if sg_confidence > 0.7:
                    guidance_direction = sg_direction
                    if sg_message not in guidance_messages:
                        guidance_messages.insert(0, sg_message)
                
                # 触发导航事件（如果有统一事件管理器）
                # 这里使用 logger 记录，实际可以调用 UnifiedEventManager
                logger.info(f"[SceneGraphReasoner] 方向: {sg_direction}, 消息: {sg_message}")
                
                # TTS播报（如果有推荐消息且TTS管理器可用）
                if sg_message and tts_manager and sg_confidence > 0.7:
                    try:
                        tts_manager.speak(sg_message, priority=1)
                    except Exception as e:
                        logger.warning(f"SceneGraph TTS播报失败: {e}")
            
            logger.debug(f"[SceneGraph] 构建完成: {len(scene_graph.nodes)} 节点, {len(scene_graph.relations)} 关系")
            
        except Exception as e:
            logger.error(f"[SceneGraph] 构建或推理错误: {e}", exc_info=True)
        
        # ========== 新导航链路集成：YOLO → EnvironmentScanner → NavigationRuntime ==========
        nav_result = None
        if navigation_runtime and environment_scanner:
            try:
                from core.navigation import FrameContext
                
                # 1. 转换 YOLO 输出格式
                yolo_data = []
                detections = vision_results.get('detections', [])
                for det in detections:
                    bbox = det.get('bbox', (0, 0, 0, 0))
                    if isinstance(bbox, tuple) and len(bbox) == 4:
                        # 归一化 bbox（假设原图尺寸）
                        h, w = image_np.shape[:2]
                        x1, y1, x2, y2 = bbox
                        yolo_data.append({
                            "label": det.get('class', 'unknown'),
                            "bbox": [x1/w, y1/h, x2/w, y2/h],
                            "confidence": det.get('confidence', 0.5),
                            "distance_m": det.get('distance', None)
                        })
                
                # 2. 转换 OCR 输出格式
                ocr_data = []
                for ocr_item in vision_results.get('ocr_results', []):
                    bbox = ocr_item.get('bbox', (0, 0, 0, 0))
                    if isinstance(bbox, tuple) and len(bbox) == 4:
                        h, w = image_np.shape[:2]
                        x1, y1, x2, y2 = bbox
                        ocr_data.append({
                            "text": ocr_item.get('text', ''),
                            "bbox": [x1/w, y1/h, x2/w, y2/h],
                            "confidence": ocr_item.get('confidence', 0.5)
                        })
                
                # 3. 构造 FrameContext（使用默认值，实际应从IMU获取）
                frame_ctx = FrameContext.from_raw(
                    frame_id=int(time.time() * 1000) % 1000000,
                    camera_heading_deg=0.0,  # 实际应从IMU获取
                    camera_pitch_deg=0.0,
                    camera_roll_deg=0.0,
                    speed_mps=0.0,  # 实际应从IMU获取
                    turn_rate_deg_s=0.0  # 实际应从IMU获取
                )
                
                # 4. 调用 EnvironmentScanner
                stable_nodes = environment_scanner.process(
                    frame_ctx,
                    yolo_data,
                    ocr_data
                )
                
                # 记录扫描结果日志
                if log_manager:
                    log_manager.log_visual_event(
                        event_type="environment_scanner_output",
                        detection_result={
                            "stable_nodes_count": len(stable_nodes),
                            "nodes": [n.to_dict() for n in stable_nodes[:5]]  # 只记录前5个
                        }
                    )
                
                # 5. 调用 NavigationRuntime
                nav_data = {
                    "heading_deg": 0.0,  # 实际应从IMU获取
                    "speed_mps": 0.0,
                    "turn_rate_deg_s": 0.0,
                    "yolo": yolo_data,
                    "ocr": ocr_data
                }
                nav_result = navigation_runtime.feed(nav_data)
                
                # 记录导航结果日志
                if log_manager:
                    log_manager.log_visual_event(
                        event_type="navigation_runtime_output",
                        detection_result=nav_result
                    )
                
                # 6. 根据导航结果更新指引（如果新导航链路有更好的建议）
                if nav_result and nav_result.get("recommended_action"):
                    nav_direction = nav_result.get("primary_direction", "forward")
                    nav_action = nav_result.get("recommended_action", "")
                    
                    # 如果新导航链路检测到偏航或特殊方向，优先使用
                    if nav_result.get("is_deviation") or nav_direction != "forward":
                        guidance_direction = nav_direction
                        if nav_action not in guidance_messages:
                            guidance_messages.insert(0, nav_action)
                    
                    # 添加环境提示
                    if nav_result.get("environment_hint"):
                        hint = nav_result["environment_hint"]
                        if hint not in guidance_messages:
                            guidance_messages.append(hint)
                
                logger.info(f"[NavigationRuntime] 导航分析完成: {nav_result.get('primary_direction', 'unknown')}")
                
            except Exception as e:
                logger.error(f"[NavigationRuntime] 导航链路处理错误: {e}", exc_info=True)
        
        # 记录日志
        if log_manager:
            try:
                log_manager.log_visual_event(
                    event_type="visual_guidance",
                    detection_result={
                        "direction": guidance_direction,
                        "messages": guidance_messages,
                        "nodes_detected": len(detected_nodes),
                        "signboards_detected": len(signboard_results_stable),
                        "step_detected": step_detected,
                        "hazards_detected": len(hazards_detected_stable),
                        "roi_optimized": vision_results.get('roi_optimized', False),
                        "temporal_fused": temporal_fusion is not None,
                        "visual_language_fused": fusion_decision is not None,
                        "navigation_runtime_enabled": navigation_runtime is not None,
                        "nav_result": nav_result if nav_result else None,
                        "scene_graph_enabled": scene_graph_result is not None,
                        "scene_reason": sg_reason_result if sg_reason_result else None,
                        "floorplan_enabled": floor_graph_result is not None,
                        "map_kind": map_kind if map_kind else None,
                        "merged_graph_enabled": merged_graph_result is not None
                    },
                    system_response="视觉导航指引已生成（已应用优化、新导航链路、SceneGraph推理和结构图融合）"
                )
            except Exception as e:
                logger.warning(f"⚠️ 记录视觉导航日志失败: {e}")
        
        total_time = (time.time() - start_time) * 1000
        
        # 记录性能指标
        if 'vision_latency' in performance_metrics:
            performance_metrics['vision_latency'].append(total_time)
            if len(performance_metrics['vision_latency']) > 100:
                performance_metrics['vision_latency'].pop(0)
        
        # ========== 指令1：修复vision_summary输出格式（添加detections字段）==========
        # 构造简化版detections列表，供前端VisionEnhancer使用
        simple_detections = []
        for obj in vision_results.get('detections', []):
            try:
                bbox = obj.get('bbox', (0, 0, 0, 0))
                # 确保bbox是列表或元组，且可序列化
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    bbox_list = [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
                else:
                    bbox_list = [0.0, 0.0, 0.0, 0.0]
                
                simple_detections.append({
                    "class": str(obj.get("class") or obj.get("label") or ""),
                    "label": str(obj.get("label") or obj.get("class") or ""),
                    "bbox": bbox_list,  # (x, y, w, h) 格式
                    "confidence": float(obj.get("confidence", 0.0))
                })
            except Exception as e:
                logger.debug(f"跳过无效检测对象: {e}")
                continue
        
        # 获取图像尺寸
        frame_width = int(image_np.shape[1]) if image_np is not None else 640
        frame_height = int(image_np.shape[0]) if image_np is not None else 480
        
        # 构造返回结果，包含导航链路信息
        result_data = {
            'guidance': {
                'direction': guidance_direction,
                'messages': guidance_messages,
                'room_numbers': room_numbers,
                'optimizations': {
                    'roi_optimized': vision_results.get('roi_optimized', False),
                    'temporal_fused': temporal_fusion is not None,
                    'visual_language_fused': fusion_decision is not None,
                    'navigation_runtime_enabled': navigation_runtime is not None
                },
                'detected_nodes': detected_nodes[:5],  # 只返回前5个
                'signboards': [{'type': r.get('type', ''), 'bbox': r.get('bbox', ()), 'confidence': r.get('confidence', 0.0)} 
                              for r in signboard_results_stable[:3]],  # 只返回前3个
                'step_detected': step_detected,
                'hazards_count': len(hazards_detected_stable)
            },
            'vision_summary': {
                # 原来的三个字段保留
                'objects_detected': len(vision_results.get('detections', [])),
                'texts_detected': len(vision_results.get('ocr_results', [])),
                'processing_time_ms': round(total_time, 2),
                # ✅ 新增：给前端VisionEnhancer用
                'detections': simple_detections,
                'frame_width': frame_width,
                'frame_height': frame_height
            }
        }
        
        # 添加导航链路结果（如果可用）
        if nav_result:
            result_data['navigation_runtime'] = {
                'primary_direction': nav_result.get('primary_direction'),
                'confidence': nav_result.get('confidence'),
                'recommended_action': nav_result.get('recommended_action'),
                'environment_hint': nav_result.get('environment_hint'),
                'is_deviation': nav_result.get('is_deviation'),
                'deviation_deg': nav_result.get('deviation_deg'),
                'scene_nodes_count': len(nav_result.get('scene_nodes', []))
            }
        
        # 添加 SceneGraph 结果（如果可用）
        if sg_reason_result:
            result_data['scene_graph_reason'] = {
                'has_danger': sg_reason_result.get('has_danger'),
                'has_stairs': sg_reason_result.get('has_stairs'),
                'primary_direction': sg_reason_result.get('primary_direction'),
                'confidence': sg_reason_result.get('confidence'),
                'message': sg_reason_result.get('message')
            }
        
        if scene_graph_result:
            result_data['scene_graph'] = {
                'nodes_count': len(scene_graph_result.get('nodes', [])),
                'relations_count': len(scene_graph_result.get('relations', []))
            }
        
        # 添加结构图结果（如果可用）
        if floor_graph_result:
            result_data['floorplan_graph'] = {
                'map_kind': map_kind,
                'nodes_count': len(floor_graph_result.get('nodes', [])),
                'relations_count': len(floor_graph_result.get('relations', []))
            }
        
        if merged_graph_result:
            result_data['merged_graph'] = {
                'nodes_count': len(merged_graph_result.get('nodes', [])),
                'relations_count': len(merged_graph_result.get('relations', []))
            }
        
        return api_success(result_data)
    except Exception as e:
        logger.error(f"视觉导航指引错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/analyze_structure_map', methods=['POST'])
def api_analyze_structure_map():
    """解析结构图（医院/商场/地铁等平面图）"""
    try:
        from core.structure_map_parser import FloorPlanParser
        
        data = request.get_json(force=True, silent=True) or {}
        ocr_result = data.get("ocr_result", {})
        ocr_blocks = ocr_result.get("blocks", [])
        
        if not ocr_blocks:
            return api_error('未提供 OCR 结果', status_code=400)
        
        # 归一化 bbox（如果需要）
        file = request.files.get('image')
        image_np = None
        if file:
            image_np = image_to_numpy(file.read())
        
        normalized_blocks = []
        for blk in ocr_blocks:
            bbox = blk.get("bbox", [0, 0, 0, 0])
            if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                # 检查是否已经归一化
                if image_np is not None and (x2 > 1.0 or y2 > 1.0):
                    h, w = image_np.shape[:2]
                    bbox_norm = [x1/w, y1/h, x2/w, y2/h]
                else:
                    bbox_norm = list(bbox)
            else:
                bbox_norm = [0.0, 0.0, 0.0, 0.0]
            
            normalized_blocks.append({
                "text": blk.get("text", ""),
                "confidence": float(blk.get("confidence", 1.0)),
                "bbox": bbox_norm
            })
        
        # 解析结构图
        floor_graph, map_kind = FloorPlanParser.parse_floorplan(normalized_blocks)
        
        # 记录日志
        if log_manager:
            log_manager.log_visual_event(
                event_type="floorplan_graph",
                detection_result={
                    "map_kind": map_kind,
                    "graph": floor_graph.to_dict()
                }
            )
        
        return api_success({
            "map_kind": map_kind,
            "floor_graph": floor_graph.to_dict(),
            "nodes_count": len(floor_graph.nodes),
            "relations_count": len(floor_graph.relations)
        })
    except Exception as e:
        logger.error(f"解析结构图错误: {e}", exc_info=True)
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/voice_intent', methods=['POST'])
def api_voice_intent():
    """解析语音意图并生成任务计划"""
    try:
        from core.task_intent import TaskIntentParser
        from core.task_dispatcher import TaskDispatcher
        
        payload = request.get_json(force=True, silent=True) or {}
        text = payload.get("text", "").strip()
        
        if not text:
            return api_error('未提供文本', status_code=400)
        
        intent = TaskIntentParser.parse(text)
        if intent is None:
            # 可选：记录日志，前端据此提示"我没听懂"
            try:
                if log_manager:
                    log_manager.log_visual_event(
                        event_type="voice_intent_unrecognized",
                        detection_result={"text": text}
                    )
            except Exception:
                pass
            
            return api_success({
                "status": "no_intent",
                "message": "暂时没有理解你的任务，请再具体一点告诉我你想去哪儿或者想做什么。",
            })
        
        task_plan = TaskDispatcher.build_task_plan(intent)
        
        # 记录日志
        try:
            if log_manager:
                log_manager.log_visual_event(
                    event_type="voice_intent",
                    detection_result={
                        "text": text,
                        "intent": intent.to_dict(),
                        "task_plan": task_plan,
                    }
                )
        except Exception:
            pass
        
        return api_success({
            "status": "ok",
            "intent": intent.to_dict(),
            "task_plan": task_plan,
        })
    except Exception as e:
        logger.error(f"解析语音意图错误: {e}", exc_info=True)
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/navigation/paths', methods=['GET'])
def get_available_paths():
    """获取可用路径列表"""
    try:
        if scene_memory_system is None:
            return api_error('场景记忆系统未初始化', status_code=500)
        
        paths = {}
        for path_id, path_memory in scene_memory_system.memory_mapper.memories.items():
            paths[path_id] = {
                'path_id': path_id,
                'path_name': path_memory.path_name,
                'node_count': len(path_memory.nodes),
                'nodes': [node.label for node in path_memory.nodes]
            }
        
        return jsonify({
            'success': True,
            'paths': paths
        })
    except Exception as e:
        logger.error(f"获取路径列表错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

# =========================
# E 系列：日志接收接口（RemoteLogger 使用）
# =========================
LOG_FILE_PATH = 'luna_web_logs.jsonl'

@app.route("/log_task_event", methods=["POST"])
def log_task_event():
    """接收任务链日志事件"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # 写入任务日志文件
        log_file = "task_runtime_log.jsonl"
        log_entry = {
            "timestamp": data.get("ts", datetime.now().isoformat()),
            "level": data.get("level", "INFO"),
            "source": data.get("source", "unknown"),
            "message": data.get("message", ""),
            "extra": data.get("extra")
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        logger.info(f"📝 [TaskLog] {data.get('source')}: {data.get('message')}", extra={"module_name": "task_log", "meta": log_entry})

        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"❌ 任务日志接收失败: {e}", extra={"module_name": "task_log"})
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/log_nav_event", methods=["POST"])
def log_nav_event():
    """接收导航事件日志"""
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # 写入本地文件（JSONL格式）
        log_file = "nav_runtime_log.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
        # 同时记录到标准日志
        logger.info(f"导航事件日志: {data.get('source', 'unknown')} - {data.get('message', '')}", 
                   extra={"module_name": "nav_log", "meta": data})
        
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"导航日志接收失败: {e}", extra={"module_name": "nav_log", "error": str(e)})
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/logs", methods=["POST"])
def api_logs():
    """接收前端 RemoteLogger 批量上传的日志"""
    try:
        payload = request.get_json(force=True, silent=True) or {}
        logs = payload.get("logs") or []
        if not isinstance(logs, list):
            logs = [logs]

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            for evt in logs:
                evt["_server_ts"] = datetime.utcnow().isoformat() + "Z"
                f.write(json.dumps(evt, ensure_ascii=False) + "\n")

        return "OK", 200
    except Exception as e:
        logger.error(f"[LOG_SERVER_ERROR] {e}")
        return "ERROR", 500

@app.route('/api/logs/upload', methods=['POST'])
def upload_logs():
    """上传日志到后台（打包当天日志文件供下载/上传）"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        # 刷新缓冲区，确保所有日志都已写入文件
        log_manager.flush()
        
        data = request.get_json() or {}
        date = data.get('date')  # 可选，指定日期，默认今天
        
        # 读取日志
        logs = log_manager.read_logs(date=date)
        
        if not logs:
            return api_success({
                'message': '没有日志需要上传',
                'log_count': 0
            })
        
        # 准备上传数据
        upload_data = {
            'user_id': log_manager.user_id,
            'date': date or time.strftime('%Y-%m-%d'),
            'logs': logs,
            'total_count': len(logs),
            'upload_time': time.time()
        }
        
        # 这里可以添加实际上传到后台的逻辑
        # 例如：requests.post('https://api.luna.ai/logs/upload', json=upload_data)
        # 目前先保存到本地文件，供后续上传
        
        upload_file_path = f"logs/web_test/uploads/{time.strftime('%Y%m%d_%H%M%S')}_logs.json"
        os.makedirs(os.path.dirname(upload_file_path), exist_ok=True)
        
        with open(upload_file_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(upload_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📤 日志已准备上传: {len(logs)} 条日志")
        
        return api_success({
            'message': f'日志已准备上传（{len(logs)} 条）',
            'log_count': len(logs),
            'upload_file': upload_file_path,
            'date': date or time.strftime('%Y-%m-%d')
        })
    except Exception as e:
        logger.error(f"上传日志错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/logs/ingest', methods=['POST'])
def ingest_frontend_log():
    """接收前端日志并写入日志系统（指令4：新增接口）"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        data = request.get_json() or {}
        level = (data.get('level') or 'INFO').upper()
        message = data.get('message') or 'frontend_log'
        payload = data.get('payload') or {}
        
        extra = {
            "module": "frontend",
            "meta": {
                "session_id": data.get('sessionId'),
                "user_agent": data.get('userAgent'),
                **payload
            }
        }
        
        # 根据日志级别写入
        if level == 'DEBUG':
            logger.debug(message, extra=extra)
        elif level == 'WARN' or level == 'WARNING':
            logger.warning(message, extra=extra)
        elif level == 'ERROR':
            logger.error(message, extra=extra)
        else:
            logger.info(message, extra=extra)
        
        return api_success({"message": "frontend log ingested"})
    except Exception as e:
        logger.error(f"前端日志写入失败: {e}")
        return api_error(str(e), status_code=500)

@app.route('/api/yolo_frame', methods=['POST'])
def handle_yolo_frame():
    """接收 JS 端的 YOLO 检测结果，调用导航链路"""
    try:
        if navigation_runtime is None:
            return api_error('导航运行时未初始化', status_code=500)
        
        data = request.get_json(force=True, silent=True)
        if not data:
            return api_error('请求数据格式错误', status_code=400)
        
        # 记录原始 YOLO 数据
        if log_manager:
            log_manager.log_visual_event(
                event_type="yolo_raw",
                detection_result=data
            )
        
        # 调用 NavigationRuntime
        nav_result = navigation_runtime.feed(data)
        
        # 返回导航结果
        return api_success({
            'navigation_result': nav_result,
            'timestamp': time.time()
        })
    except Exception as e:
        logger.error(f"处理 YOLO 帧错误: {e}", exc_info=True)
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/ocr', methods=['POST'])
def handle_ocr_result():
    """接收 OCR 结果，更新导航上下文"""
    try:
        if navigation_runtime is None or environment_scanner is None:
            return api_error('导航模块未初始化', status_code=500)
        
        data = request.get_json(force=True, silent=True)
        if not data:
            return api_error('请求数据格式错误', status_code=400)
        
        # 记录 OCR 数据
        if log_manager:
            log_manager.log_visual_event(
                event_type="ocr_result",
                detection_result=data
            )
        
        # 构造 FrameContext
        from core.navigation import FrameContext
        frame_ctx = FrameContext.from_raw(
            frame_id=data.get('frame_id', int(time.time() * 1000) % 1000000),
            camera_heading_deg=data.get('heading_deg', 0.0),
            camera_pitch_deg=data.get('pitch_deg', 0.0),
            camera_roll_deg=data.get('roll_deg', 0.0),
            speed_mps=data.get('speed_mps', 0.0),
            turn_rate_deg_s=data.get('turn_rate_deg_s', 0.0)
        )
        
        # 处理 OCR 结果
        ocr_results = data.get('textBlocks', [])
        stable_nodes = environment_scanner.process(
            frame_ctx,
            yolo_results=[],  # OCR 路由不包含 YOLO
            ocr_results=ocr_results
        )
        
        # 更新导航运行时
        nav_data = {
            "heading_deg": data.get('heading_deg', 0.0),
            "speed_mps": data.get('speed_mps', 0.0),
            "turn_rate_deg_s": data.get('turn_rate_deg_s', 0.0),
            "yolo": [],
            "ocr": ocr_results
        }
        nav_result = navigation_runtime.feed(nav_data)
        
        return api_success({
            'navigation_result': nav_result,
            'stable_nodes_count': len(stable_nodes),
            'timestamp': time.time()
        })
    except Exception as e:
        logger.error(f"处理 OCR 结果错误: {e}", exc_info=True)
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/logs/realtime', methods=['GET'])
def get_realtime_logs():
    """获取实时日志（自指定时间戳之后的新日志）"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        since = request.args.get('since')  # 可选，指定时间戳
        
        # 刷新缓冲区
        log_manager.flush()
        
        # 读取日志
        logs = log_manager.read_logs()
        
        # 如果指定了since，只返回该时间戳之后的日志
        if since:
            filtered_logs = []
            for log in logs:
                if log.get('timestamp', '') > since:
                    filtered_logs.append(log)
            logs = filtered_logs
        
        # 只返回最近50条
        logs = logs[-50:]
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        })
    except Exception as e:
        logger.error(f"获取实时日志错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/logs/view', methods=['GET'])
def view_logs():
    """查看日志"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        date = request.args.get('date')  # 可选日期参数
        limit = request.args.get('limit', type=int)  # 可选限制条数
        
        # 刷新缓冲区
        log_manager.flush()
        
        # 读取日志
        if date:
            logs = log_manager.read_logs(date=date, limit=limit)
            actual_date = date
        else:
            # 如果没有指定日期，尝试读取今天的日志
            logs = log_manager.read_logs(date=None, limit=limit)
            actual_date = time.strftime('%Y-%m-%d')
            
            # 如果今天没有日志，自动查找最新的日志
            if not logs:
                available_dates = log_manager.list_available_dates()
                if available_dates:
                    actual_date = available_dates[0]
                    logs = log_manager.read_logs(date=actual_date, limit=limit)
        
        return api_success({
            'logs': logs,
            'count': len(logs),
            'date': actual_date,
            'available_dates': log_manager.list_available_dates()
        })
    except Exception as e:
        logger.error(f"查看日志错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/logs/statistics', methods=['GET'])
def get_log_statistics():
    """获取日志统计信息"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        date = request.args.get('date')  # 可选日期参数
        
        # 刷新缓冲区
        log_manager.flush()
        
        # 获取统计信息
        stats = log_manager.get_statistics(date=date)
        
        return api_success({
            'statistics': stats,
            'date': date or time.strftime('%Y-%m-%d')
        })
    except Exception as e:
        logger.error(f"获取日志统计错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/api/logs/download', methods=['GET'])
def download_logs():
    """下载日志文件"""
    try:
        if log_manager is None:
            return api_error('日志管理器未初始化', status_code=500)
        
        date = request.args.get('date')  # 可选日期参数
        
        # 刷新缓冲区
        log_manager.flush()
        
        # 读取日志
        if date:
            # 如果指定了日期，读取指定日期的日志
            logs = log_manager.read_logs(date=date)
            actual_date = date
        else:
            # 如果没有指定日期，尝试读取今天的日志
            logs = log_manager.read_logs(date=None)
            actual_date = time.strftime('%Y-%m-%d')
            
            # 如果今天没有日志，自动查找最新的日志
            if not logs:
                available_dates = log_manager.list_available_dates()
                if available_dates:
                    # 使用最新的日志日期
                    actual_date = available_dates[0]
                    logs = log_manager.read_logs(date=actual_date)
                    logger.info(f"📋 今天没有日志，使用最新日志日期: {actual_date}")
                else:
                    # 完全没有日志文件
                    return api_error('没有日志数据', details={'message': '系统中暂无任何日志文件，请先使用系统功能生成日志'}, status_code=404)
        
        if not logs:
            return api_error(f'{actual_date} 没有日志数据', details={'available_dates': log_manager.list_available_dates()}, status_code=404)
        
        # 准备下载数据
        download_data = {
            'user_id': log_manager.user_id,
            'date': actual_date,
            'logs': logs,
            'total_count': len(logs),
            'export_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 创建临时JSON文件
        import tempfile
        import json
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        json.dump(download_data, temp_file, ensure_ascii=False, indent=2)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'luna_logs_{actual_date.replace("-", "")}.json'
        )
    except Exception as e:
        logger.error(f"下载日志错误: {e}")
        return api_error(str(e), details={"exception_type": type(e).__name__}, status_code=500)

@app.route('/install-cert')
def install_cert():
    """证书安装页面"""
    cert_install_html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>安装SSL证书 - Luna</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .step {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .step-number {
            display: inline-block;
            width: 30px;
            height: 30px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 10px;
        }
        .step-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .step-content {
            color: #666;
            line-height: 1.6;
            margin-left: 40px;
        }
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            margin-top: 20px;
            transition: all 0.3s;
        }
        .btn:active {
            transform: scale(0.98);
            opacity: 0.9;
        }
        .btn-secondary {
            background: #28a745;
            margin-top: 10px;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
        .success {
            background: #d4edda;
            border: 1px solid #28a745;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #155724;
        }
        .code {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 6px;
            font-family: monospace;
            margin: 10px 0;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 安装SSL证书</h1>
        
        <div class="warning">
            <strong>⚠️ 重要提示：</strong><br>
            这是自签名证书，仅用于开发和测试。安装后需要在系统设置中信任证书。
        </div>
        
        <div class="step">
            <div class="step-title">
                <span class="step-number">1</span>
                下载证书文件
            </div>
            <div class="step-content">
                点击下面的按钮下载证书文件
            </div>
            <a href="/ssl/cert.pem" class="btn" download="luna-cert.pem">
                📥 下载证书文件
            </a>
        </div>
        
        <div class="step">
            <div class="step-title">
                <span class="step-number">2</span>
                安装证书
            </div>
            <div class="step-content">
                <strong>iPhone/iPad:</strong><br>
                1. 下载后，系统会提示"已下载描述文件"<br>
                2. 打开 <strong>设置</strong> > <strong>通用</strong> > <strong>VPN与设备管理</strong>（或<strong>描述文件</strong>）<br>
                3. 找到"Luna"证书，点击<strong>安装</strong><br>
                4. 输入密码确认安装
            </div>
        </div>
        
        <div class="step">
            <div class="step-title">
                <span class="step-number">3</span>
                信任证书
            </div>
            <div class="step-content">
                <strong>iPhone/iPad:</strong><br>
                1. 打开 <strong>设置</strong> > <strong>通用</strong> > <strong>关于本机</strong><br>
                2. 滚动到底部，点击 <strong>证书信任设置</strong><br>
                3. 找到"Luna"证书，打开<strong>信任开关</strong>
            </div>
        </div>
        
        <div class="step">
            <div class="step-title">
                <span class="step-number">4</span>
                访问网站
            </div>
            <div class="step-content">
                返回Safari，访问：<br>
                <div class="code">https://192.168.3.213:5001</div>
                现在应该可以正常使用了！
            </div>
            <a href="https://192.168.3.213:5001" class="btn btn-secondary">
                🌐 前往Luna测试页面
            </a>
        </div>
        
        <div class="success">
            <strong>✅ 安装完成后：</strong><br>
            • 可以使用摄像头拍照识别<br>
            • 可以使用麦克风录音识别<br>
            • 所有功能正常工作
        </div>
    </div>
</body>
</html>
    """
    return cert_install_html

@app.route('/test')
def luna_test_panel():
    """
    Luna 1.2.0 测试界面
    - 视觉单点测试
    - 危险 / 台阶单点测试
    - 导航状态 / 场景描述
    - Hook 事件观察
    """
    return render_template("luna_test_panel.html")

@app.route('/test_panel')
def test_panel():
    """测试界面v2 - 导航/视觉/任务链/记忆四块实时面板"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>Luna Badge 调试面板</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; }
    .tabs { display: flex; background: #222; color: #eee; }
    .tab { padding: 10px 16px; cursor: pointer; }
    .tab.active { background: #444; }
    .panel { display: none; padding: 12px; }
    .panel.active { display: block; }
    .log-area { height: 200px; overflow: auto; background: #111; color: #0f0; font-size: 12px; padding: 6px; }
    .section { margin-bottom: 12px; }
  </style>
</head>
<body>
  <div class="tabs">
    <div class="tab active" data-target="nav-panel">导航</div>
    <div class="tab" data-target="vision-panel">视觉</div>
    <div class="tab" data-target="task-panel">任务链</div>
    <div class="tab" data-target="memory-panel">记忆</div>
  </div>

  <div id="nav-panel" class="panel active">
    <h3>导航状态</h3>
    <div class="section">
      <pre id="nav-status"></pre>
    </div>
    <div class="section">
      <div>导航日志：</div>
      <div id="nav-log" class="log-area"></div>
    </div>
  </div>

  <div id="vision-panel" class="panel">
    <h3>视觉状态</h3>
    <div class="section">
      <pre id="vision-status"></pre>
    </div>
    <div class="section">
      <div>YOLO / OCR 日志：</div>
      <div id="vision-log" class="log-area"></div>
    </div>
  </div>

  <div id="task-panel" class="panel">
    <h3>任务链状态</h3>
    <div class="section">
      <pre id="task-status"></pre>
    </div>
    <div class="section">
      <div>任务链日志：</div>
      <div id="task-log" class="log-area"></div>
    </div>
  </div>

  <div id="memory-panel" class="panel">
    <h3>节点 / 区域 / 场景记忆</h3>
    <div class="section">
      <pre id="memory-status"></pre>
    </div>
    <div class="section">
      <div>记忆更新日志：</div>
      <div id="memory-log" class="log-area"></div>
    </div>
  </div>

  <script>
    // tab 切换
    document.querySelectorAll(".tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
        document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(tab.getAttribute("data-target")).classList.add("active");
      });
    });

    function appendLog(id, msg) {
      const el = document.getElementById(id);
      if (!el) return;
      const line = document.createElement("div");
      line.textContent = "[" + (new Date()).toLocaleTimeString() + "] " + msg;
      el.appendChild(line);
      el.scrollTop = el.scrollHeight;
    }

    // 前端钩子：让现有模块可以往测试面板写状态
    window.__debugPanel = {
      updateNavStatus(state) {
        document.getElementById("nav-status").textContent = JSON.stringify(state, null, 2);
      },
      updateVisionStatus(state) {
        document.getElementById("vision-status").textContent = JSON.stringify(state, null, 2);
      },
      updateTaskStatus(state) {
        document.getElementById("task-status").textContent = JSON.stringify(state, null, 2);
      },
      updateMemoryStatus(state) {
        document.getElementById("memory-status").textContent = JSON.stringify(state, null, 2);
      },
      logNav(msg) { appendLog("nav-log", msg); },
      logVision(msg) { appendLog("vision-log", msg); },
      logTask(msg) { appendLog("task-log", msg); },
      logMemory(msg) { appendLog("memory-log", msg); },
    };

    console.log("[TestPanel] 调试面板已就绪，等待导航/视觉/任务链模块写入状态。");
  </script>
</body>
</html>
"""


@app.route('/param_center')
def param_center():
    """参数中心页面 - 可调节系统参数"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>Luna Badge 参数中心</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 16px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 6px 8px; font-size: 13px; }
    th { background: #f5f5f5; }
    input { width: 100%; box-sizing: border-box; }
    .btn-row { margin-top: 12px; }
    button { padding: 6px 12px; margin-right: 8px; }
  </style>
</head>
<body>
  <h2>Luna Badge 参数中心</h2>
  <div>从后端拉取可调节参数，并支持调整后写回。</div>

  <table id="param-table">
    <thead>
      <tr>
        <th>Key</th>
        <th>当前值</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <div class="btn-row">
    <button id="btn-refresh">刷新</button>
    <button id="btn-save">保存修改</button>
  </div>

  <pre id="status"></pre>

  <script>
    let paramData = {};

    function setStatus(msg) {
      document.getElementById("status").textContent = msg;
    }

    function loadParams() {
      setStatus("加载中...");
      fetch("/api/v1/config/get")
        .then(r => r.json())
        .then(resp => {
          if (!resp.success) {
            setStatus("加载失败：" + resp.message);
            return;
          }
          const data = resp.data || {};
          paramData = data;
          const tbody = document.querySelector("#param-table tbody");
          tbody.innerHTML = "";
          Object.keys(data).forEach(key => {
            const row = document.createElement("tr");
            const info = data[key];
            const desc = info.description || "";
            const value = info.value;

            row.innerHTML = `
              <td>${key}</td>
              <td><input data-key="${key}" value="${value}"></td>
              <td>${desc}</td>
            `;
            tbody.appendChild(row);
          });
          setStatus("加载完成，共 " + Object.keys(data).length + " 项参数。");
        })
        .catch(err => {
          console.error(err);
          setStatus("加载异常：" + err);
        });
    }

    function saveParams() {
      const inputs = document.querySelectorAll("#param-table input[data-key]");
      const update = {};
      inputs.forEach(input => {
        const key = input.getAttribute("data-key");
        const raw = input.value;
        // 简单处理：字符串转数字/布尔
        let parsed = raw;
        if (raw === "true" || raw === "false") {
          parsed = (raw === "true");
        } else if (!isNaN(Number(raw))) {
          parsed = Number(raw);
        }
        update[key] = parsed;
      });

      setStatus("保存中...");
      fetch("/api/v1/config/set", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(update),
      })
        .then(r => r.json())
        .then(resp => {
          if (!resp.success) {
            setStatus("保存失败：" + resp.message);
            return;
          }
          setStatus("保存成功，已更新 " + Object.keys(resp.data.updated || {}).length + " 项。");
        })
        .catch(err => {
          console.error(err);
          setStatus("保存异常：" + err);
        });
    }

    document.getElementById("btn-refresh").addEventListener("click", loadParams);
    document.getElementById("btn-save").addEventListener("click", saveParams);

    loadParams();
  </script>
</body>
</html>
"""


@app.route('/ssl/cert.pem')
def download_cert():
    """下载证书文件"""
    cert_path = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    if os.path.exists(cert_path):
        return send_file(cert_path, mimetype='application/x-x509-ca-cert', 
                        as_attachment=True, download_name='luna-cert.pem')
    else:
        return "证书文件不存在", 404

if __name__ == '__main__':
    # 初始化所有模块
    if not init_all_modules():
        logger.warning("部分模块初始化失败，但服务器仍会启动")
    
    # 注册自动测试路由
    try:
        from routes.auto_test_routes import auto_test_api
        app.register_blueprint(auto_test_api, url_prefix="/api/auto")
        logger.info("✅ 自动测试 API 已注册")
    except Exception as e:
        logger.warning(f"注册自动测试路由失败: {e}")
    
    # 注册自动测试 UI 路由
    try:
        from routes.auto_test_ui_routes import auto_test_ui
        app.register_blueprint(auto_test_ui)
        logger.info("✅ 自动测试 UI 已注册")
    except Exception as e:
        logger.warning(f"注册自动测试 UI 失败: {e}")
    
    # v2.0: 注册设备上报接口（Telemetry）
    try:
        from routes.telemetry_routes import telemetry_api
        app.register_blueprint(telemetry_api, url_prefix="/api/telemetry")
        logger.info("✅ Telemetry API 已注册")
    except Exception as e:
        logger.warning(f"注册 Telemetry API 失败: {e}")
        logger.info("✅ 自动测试路由已注册")
    except Exception as e:
        logger.warning(f"⚠️ 自动测试路由注册失败: {e}")
    
    # 注意：端口5000和8080不可用，默认使用9001
    port = int(os.environ.get('PORT', 9001))
    
    # HTTPS配置
    ssl_cert_path = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    ssl_key_path = os.path.join(os.path.dirname(__file__), 'ssl', 'key.pem')
    use_https = os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path)
    
    logger.info(f"🚀 Luna 完整功能测试服务器启动中...")
    
    if use_https:
        # 获取本机IP地址
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "localhost"
        
        logger.info(f"🔒 HTTPS模式已启用")
        logger.info(f"📱 手机访问地址: https://{local_ip}:{port}")
        logger.info(f"💻 本地访问地址: https://localhost:{port}")
        logger.info(f"⚠️  首次访问需要在手机上信任自签名证书")
        app.run(host='0.0.0.0', port=port, debug=False, ssl_context=(ssl_cert_path, ssl_key_path))
    else:
        # 获取本机IP地址
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "localhost"
        
        logger.info(f"📱 手机访问地址: http://{local_ip}:{port}")
        logger.info(f"💻 本地访问地址: http://localhost:{port}")
        logger.warning(f"⚠️  HTTP模式：Safari浏览器无法使用摄像头/麦克风")
        logger.info(f"💡 提示：运行 'python3 generate_ssl_cert.py' 生成SSL证书启用HTTPS")
        app.run(host='0.0.0.0', port=port, debug=False)

