"""
Luna Backend 服务层初始化
将原 web_test_server.py 中的 init_all_modules 逻辑迁移到这里
"""

from typing import Dict, Any
from core.logger import logger
import sys
import os

# 添加Luna_Badge路径以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge"))


def init_services() -> Dict[str, Any]:
    """
    初始化所有服务模块
    返回服务实例字典，用于注入到Flask app.extensions
    
    Returns:
        Dict[str, Any]: 服务实例字典
    """
    services = {}
    success_count = 0
    
    # 1. 视觉OCR引擎
    try:
        from core.vision_ocr_engine import VisionOCREngine
        logger.info("正在初始化视觉OCR引擎...", module="Vision")
        vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if vision_engine.load_models():
            services["vision_engine"] = vision_engine
            logger.info("✅ 视觉OCR引擎初始化成功", module="Vision")
            success_count += 1
        else:
            logger.warn("⚠️ 视觉OCR引擎初始化失败", module="Vision")
    except Exception as e:
        logger.warn("⚠️ 视觉OCR引擎初始化异常", details={"error": str(e)}, module="Vision")
    
    # 2. 台阶检测器
    try:
        from core.step_detector import StepDetector
        logger.info("正在初始化台阶检测器...", module="Vision")
        step_detector = StepDetector()
        services["step_detector"] = step_detector
        logger.info("✅ 台阶检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 台阶检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 3. 标识牌检测器
    try:
        from core.signboard_detector import SignboardDetector
        logger.info("正在初始化标识牌检测器...", module="Vision")
        signboard_detector = SignboardDetector()
        services["signboard_detector"] = signboard_detector
        logger.info("✅ 标识牌检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 标识牌检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 4. 危险检测器
    try:
        from core.hazard_detector import HazardDetector
        logger.info("正在初始化危险检测器...", module="Vision")
        hazard_detector = HazardDetector()
        services["hazard_detector"] = hazard_detector
        logger.info("✅ 危险检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 危险检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 5. 语音识别器（延迟加载）
    try:
        from core.whisper_recognizer import WhisperRecognizer
        logger.info("语音识别器将在首次使用时加载...", module="Voice")
        whisper_recognizer = WhisperRecognizer(model_name="base", language="zh")
        services["whisper_recognizer"] = whisper_recognizer
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 语音识别器初始化异常", details={"error": str(e)}, module="Voice")
    
    # 6. TTS管理器
    try:
        from core.tts_manager import TTSManager
        logger.info("正在初始化TTS管理器...", module="TTS")
        tts_manager = TTSManager()
        services["tts_manager"] = tts_manager
        logger.info("✅ TTS管理器初始化成功", module="TTS")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ TTS管理器初始化异常", details={"error": str(e)}, module="TTS")
    
    # 7. 场景记忆系统
    try:
        from core.scene_memory_system import get_scene_memory_system
        logger.info("正在初始化场景记忆系统...", module="Scene")
        scene_memory_system = get_scene_memory_system()
        services["scene_memory_system"] = scene_memory_system
        logger.info("✅ 场景记忆系统初始化成功", module="Scene")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 场景记忆系统初始化异常", details={"error": str(e)}, module="Scene")
    
    # 8. 路径规划器
    try:
        from core.path_planner import PathPlanner
        logger.info("正在初始化路径规划器...", module="Navigation")
        scene_memory_system = services.get("scene_memory_system")
        if scene_memory_system:
            path_planner = PathPlanner(scene_memory_system)
            services["path_planner"] = path_planner
            logger.info("✅ 路径规划器初始化成功", module="Navigation")
            success_count += 1
        else:
            logger.warn("⚠️ 场景记忆系统未初始化，跳过路径规划器", module="Navigation")
    except Exception as e:
        logger.warn("⚠️ 路径规划器初始化异常", details={"error": str(e)}, module="Navigation")
    
    # 9. 快速TTS缓存系统
    try:
        from core.fast_tts_cache import FastTTSCache
        fast_tts_cache = FastTTSCache(cache_dir="tts_cache")
        services["fast_tts_cache"] = fast_tts_cache
        logger.info("✅ 快速TTS缓存系统初始化成功", module="TTS")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 快速TTS缓存系统初始化失败", details={"error": str(e)}, module="TTS")
    
    # 10. 导航管理器
    try:
        from core.navigation_manager import NavigationManager
        logger.info("正在初始化导航管理器...", module="Navigation")
        
        # TTS播报回调
        tts_manager = services.get("tts_manager")
        def tts_broadcast_callback(text: str, style: str = "calm"):
            """TTS播报回调"""
            if tts_manager:
                try:
                    import threading
                    def async_speak():
                        try:
                            tts_manager.speak(text, style)
                        except Exception as e:
                            logger.warn("TTS播报失败", details={"error": str(e)}, module="TTS")
                    thread = threading.Thread(target=async_speak)
                    thread.daemon = True
                    thread.start()
                except Exception as e:
                    logger.warn("TTS播报线程启动失败", details={"error": str(e)}, module="TTS")
        
        navigation_manager = NavigationManager(tts_callback=tts_broadcast_callback)
        services["navigation_manager"] = navigation_manager
        logger.info("✅ 导航管理器初始化成功（已启用语音播报）", module="Navigation")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 导航管理器初始化异常", details={"error": str(e)}, module="Navigation")
    
    # 11-15. 其他检测器（公共设施、红绿灯、人群密度、排队、门牌号）
    detector_modules = [
        ("core.facility_detector", "FacilityDetector", "公共设施检测器", "facility_detector"),
        ("core.traffic_light_detector", "TrafficLightDetector", "红绿灯检测器", "traffic_light_detector"),
        ("core.crowd_density_detector", "CrowdDensityDetector", "人群密度检测器", "crowd_density_detector"),
        ("core.queue_detector", "QueueDetector", "排队检测器", "queue_detector"),
        ("core.doorplate_reader", "DoorplateReader", "门牌号识别器", "doorplate_reader"),
    ]
    
    for module_path, class_name, display_name, service_key in detector_modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            detector_class = getattr(module, class_name)
            logger.info(f"正在初始化{display_name}...", module="Vision")
            detector = detector_class()
            services[service_key] = detector
            logger.info(f"✅ {display_name}初始化成功", module="Vision")
            success_count += 1
        except Exception as e:
            logger.warn(f"⚠️ {display_name}初始化异常", details={"error": str(e)}, module="Vision")
    
    # 16. 本地地图生成器
    try:
        from core.local_map_generator import LocalMapGenerator
        logger.info("正在初始化本地地图生成器...", module="Navigation")
        local_map_generator = LocalMapGenerator()
        services["local_map_generator"] = local_map_generator
        logger.info("✅ 本地地图生成器初始化成功", module="Navigation")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 本地地图生成器初始化异常", details={"error": str(e)}, module="Navigation")
    
    # 17. 日志管理器
    try:
        from core.log_manager import LogManager
        logger.info("正在初始化日志管理器...", module="System")
        log_manager = LogManager(user_id="web_test_user")
        services["log_manager"] = log_manager
        logger.info("✅ 日志管理器初始化成功", module="System")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 日志管理器初始化异常", details={"error": str(e)}, module="System")
    
    # 18. 性能指标字典
    performance_metrics = {
        "vision_latency": [],
        "audio_latency": [],
        "memory_usage": [],
        "fps": []
    }
    services["performance_metrics"] = performance_metrics
    
    # 19. 优雅降级器（如果有）
    try:
        from core.graceful_degrader import GracefulDegrader
        graceful_degrader = GracefulDegrader()
        services["graceful_degrader"] = graceful_degrader
        logger.info("✅ 优雅降级器初始化成功", module="System")
    except Exception as e:
        logger.warn("⚠️ 优雅降级器初始化异常", details={"error": str(e)}, module="System")
    
    logger.info(f"✅ 模块初始化完成: {success_count} 个模块成功", module="System")
    
    return services
