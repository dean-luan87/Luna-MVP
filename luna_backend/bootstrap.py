"""
启动引导 (Bootstrap) v1.2.0
负责初始化所有核心模块，并把实例挂到 services.runtime.rt 上
从 web_test_server.py 的 init_all_modules() 迁移而来
"""

import logging
import sys
import os
from services.runtime import rt

# 添加Luna_Badge路径以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge"))

logger = logging.getLogger(__name__)


def init_vision_modules():
    """
    初始化视觉相关模块：vision_engine / step_detector / hazard_detector etc.
    """
    try:
        # 视觉OCR引擎
        from core.vision_ocr_engine import VisionOCREngine
        logger.info("正在初始化视觉OCR引擎...")
        rt.vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if rt.vision_engine.load_models():
            logger.info("✅ 视觉OCR引擎初始化成功")
        else:
            logger.warning("⚠️ 视觉OCR引擎初始化失败")
    except Exception as e:
        logger.exception(f"❌ 视觉OCR引擎初始化失败: {e}")
    
    try:
        # 台阶检测器
        from core.step_detector import StepDetector
        logger.info("正在初始化台阶检测器...")
        rt.step_detector = StepDetector()
        logger.info("✅ 台阶检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 台阶检测器初始化失败: {e}")
    
    try:
        # 标识牌检测器
        from core.signboard_detector import SignboardDetector
        logger.info("正在初始化标识牌检测器...")
        rt.signboard_detector = SignboardDetector()
        logger.info("✅ 标识牌检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 标识牌检测器初始化失败: {e}")
    
    try:
        # 危险检测器
        from core.hazard_detector import HazardDetector
        logger.info("正在初始化危险检测器...")
        rt.hazard_detector = HazardDetector()
        logger.info("✅ 危险检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 危险检测器初始化失败: {e}")
    
    try:
        # 公共设施检测器
        from core.facility_detector import FacilityDetector
        logger.info("正在初始化公共设施检测器...")
        rt.facility_detector = FacilityDetector()
        logger.info("✅ 公共设施检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 公共设施检测器初始化失败: {e}")
    
    try:
        # 红绿灯检测器
        from core.traffic_light_detector import TrafficLightDetector
        logger.info("正在初始化红绿灯检测器...")
        rt.traffic_light_detector = TrafficLightDetector()
        logger.info("✅ 红绿灯检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 红绿灯检测器初始化失败: {e}")
    
    try:
        # 人群密度检测器
        from core.crowd_density_detector import CrowdDensityDetector
        logger.info("正在初始化人群密度检测器...")
        rt.crowd_density_detector = CrowdDensityDetector()
        logger.info("✅ 人群密度检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 人群密度检测器初始化失败: {e}")
    
    try:
        # 排队检测器
        from core.queue_detector import QueueDetector
        logger.info("正在初始化排队检测器...")
        rt.queue_detector = QueueDetector()
        logger.info("✅ 排队检测器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 排队检测器初始化失败: {e}")
    
    try:
        # 门牌号识别器
        from core.doorplate_reader import DoorplateReader
        logger.info("正在初始化门牌号识别器...")
        rt.doorplate_reader = DoorplateReader()
        logger.info("✅ 门牌号识别器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 门牌号识别器初始化失败: {e}")
    
    try:
        # 场景记忆系统
        from core.scene_memory_system import get_scene_memory_system
        logger.info("正在初始化场景记忆系统...")
        rt.scene_memory_system = get_scene_memory_system()
        logger.info("✅ 场景记忆系统初始化成功")
    except Exception as e:
        logger.exception(f"❌ 场景记忆系统初始化失败: {e}")
    
    try:
        # 本地地图生成器（旧版）
        from core.local_map_generator import LocalMapGenerator
        logger.info("正在初始化本地地图生成器...")
        rt.local_map_generator = LocalMapGenerator()
        logger.info("✅ 本地地图生成器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 本地地图生成器初始化失败: {e}")
    
    logger.info("✅ 视觉相关模块初始化完成")


def init_navigation_modules():
    """
    初始化导航模块：path_planner / navigation_manager / local_map_service
    """
    try:
        # 路径规划器
        from core.path_planner import PathPlanner
        logger.info("正在初始化路径规划器...")
        if rt.scene_memory_system:
            rt.path_planner = PathPlanner(rt.scene_memory_system)
            logger.info("✅ 路径规划器初始化成功")
        else:
            logger.warning("⚠️ 场景记忆系统未初始化，跳过路径规划器")
    except Exception as e:
        logger.exception(f"❌ 路径规划器初始化失败: {e}")
    
    try:
        # 导航管理器（使用新的v3版本）
        from services.navigation.navigation_manager_v3 import NavigationManager
        logger.info("正在初始化导航管理器...")
        rt.navigation_manager = NavigationManager(
            log_manager=rt.log_manager,
            path_planner=rt.path_planner
        )
        logger.info("✅ 导航管理器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 导航管理器初始化失败: {e}")
    
    try:
        # 本地地图服务（新版）
        from services.navigation.local_map_service import LocalMapService
        logger.info("正在初始化本地地图服务...")
        rt.local_map_service = LocalMapService()
        logger.info("✅ 本地地图服务初始化成功")
    except Exception as e:
        logger.exception(f"❌ 本地地图服务初始化失败: {e}")
    
    logger.info("✅ 导航模块初始化完成")


def init_voice_modules():
    """
    初始化语音识别 + TTS + 缓存
    """
    try:
        # 语音识别器（延迟加载）
        from core.whisper_recognizer import WhisperRecognizer
        logger.info("语音识别器将在首次使用时加载...")
        rt.whisper_recognizer = WhisperRecognizer(model_name="base", language="zh")
        logger.info("✅ 语音识别器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 语音识别器初始化失败: {e}")
    
    try:
        # TTS管理器
        from core.tts_manager import TTSManager
        logger.info("正在初始化TTS管理器...")
        rt.tts_manager = TTSManager()
        logger.info("✅ TTS管理器初始化成功")
    except Exception as e:
        logger.exception(f"❌ TTS管理器初始化失败: {e}")
    
    try:
        # 快速TTS缓存系统
        from core.fast_tts_cache import FastTTSCache
        logger.info("正在初始化快速TTS缓存系统...")
        rt.fast_tts_cache = FastTTSCache(cache_dir="tts_cache")
        logger.info("✅ 快速TTS缓存系统初始化成功")
    except Exception as e:
        logger.exception(f"❌ 快速TTS缓存系统初始化失败: {e}")
    
    logger.info("✅ 语音/TTS 模块初始化完成")


def init_logging_and_degrade():
    """
    初始化日志管理 / 降级器 / 性能指标
    """
    try:
        # 日志管理器
        from core.log_manager import LogManager
        logger.info("正在初始化日志管理器...")
        rt.log_manager = LogManager(user_id="web_test_user", log_dir="logs/web_test")
        logger.info("✅ 日志管理器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 日志管理器初始化失败: {e}")
    
    try:
        # 优雅降级器
        from core.graceful_degrader import GracefulDegrader
        logger.info("正在初始化优雅降级器...")
        rt.graceful_degrader = GracefulDegrader()
        logger.info("✅ 优雅降级器初始化成功")
    except Exception as e:
        logger.exception(f"❌ 优雅降级器初始化失败: {e}")
    
    # 性能指标字典
    rt.performance_metrics = {
        "vision_latency": [],
        "audio_latency": [],
        "memory_usage": [],
        "fps": []
    }
    
    logger.info("✅ 日志 & 降级模块初始化完成")


def init_task_engine():
    """
    初始化后台任务引擎（如 HospitalTask / NavigationTask 的调度器）
    """
    try:
        from services.task.task_engine import TaskEngine
        logger.info("正在初始化任务引擎...")
        rt.task_engine = TaskEngine()
        logger.info("✅ 任务引擎初始化成功")
    except Exception as e:
        logger.exception(f"❌ 任务引擎初始化失败: {e}")


def init_all_modules() -> bool:
    """
    对外唯一入口：被 create_app / app.py 调用
    
    返回 bool 表示是否"基本成功"
    """
    logger.info("🚀 开始初始化 Luna 模块...")
    
    ok = True
    for fn in (
        init_logging_and_degrade,  # 先初始化日志，方便后续记录
        init_vision_modules,
        init_navigation_modules,
        init_voice_modules,
        init_task_engine,
    ):
        try:
            fn()
        except Exception as e:
            logger.exception(f"❌ 子模块初始化异常: {fn.__name__} - {e}")
            ok = False
    
    logger.info(f"✅ 模块初始化完成，基本成功: {ok}")
    return ok
