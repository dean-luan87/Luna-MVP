"""
集中管理系统级单例对象 & 初始化入口 (v1.2.0)
把原来 web_test_server.py 里的 init_all_modules() 相关内容逐步搬到这里
"""

import sys
import os

# 添加Luna_Badge路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge"))

from typing import Optional
from core.logger import logger

# ==================== 全局单例对象 ====================

# 视觉模块
vision_engine = None
step_detector = None
signboard_detector = None
hazard_detector = None
facility_detector = None
traffic_light_detector = None
crowd_density_detector = None
queue_detector = None
doorplate_reader = None
local_map_generator = None

# 场景记忆
scene_memory_system = None

# 视觉增强
saliency_roi = None
temporal_fusion = None
visual_language_fusion = None

# 系统模块
log_manager = None
graceful_degrader = None

# 其他
whisper_recognizer = None
tts_manager = None
path_planner = None
navigation_manager = None


def init_all_modules():
    """
    初始化所有模块
    把原来 web_test_server.py 里所有模块初始化逻辑搬进来
    """
    global vision_engine, step_detector, signboard_detector, hazard_detector
    global facility_detector, traffic_light_detector, crowd_density_detector
    global queue_detector, doorplate_reader, local_map_generator
    global scene_memory_system, saliency_roi, temporal_fusion
    global visual_language_fusion, log_manager, graceful_degrader
    global whisper_recognizer, tts_manager, path_planner, navigation_manager
    
    success_count = 0
    
    # 1. 视觉OCR引擎
    try:
        from core.vision_ocr_engine import VisionOCREngine
        logger.info("正在初始化视觉OCR引擎...", module="Vision")
        vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if vision_engine.load_models():
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
        logger.info("✅ 台阶检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 台阶检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 3. 标识牌检测器
    try:
        from core.signboard_detector import SignboardDetector
        logger.info("正在初始化标识牌检测器...", module="Vision")
        signboard_detector = SignboardDetector()
        logger.info("✅ 标识牌检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 标识牌检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 4. 危险检测器
    try:
        from core.hazard_detector import HazardDetector
        logger.info("正在初始化危险检测器...", module="Vision")
        hazard_detector = HazardDetector()
        logger.info("✅ 危险检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 危险检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 5. 公共设施检测器
    try:
        from core.facility_detector import FacilityDetector
        logger.info("正在初始化公共设施检测器...", module="Vision")
        facility_detector = FacilityDetector()
        logger.info("✅ 公共设施检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 公共设施检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 6. 红绿灯检测器
    try:
        from core.traffic_light_detector import TrafficLightDetector
        logger.info("正在初始化红绿灯检测器...", module="Vision")
        traffic_light_detector = TrafficLightDetector()
        logger.info("✅ 红绿灯检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 红绿灯检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 7. 人群密度检测器
    try:
        from core.crowd_density_detector import CrowdDensityDetector
        logger.info("正在初始化人群密度检测器...", module="Vision")
        crowd_density_detector = CrowdDensityDetector()
        logger.info("✅ 人群密度检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 人群密度检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 8. 排队检测器
    try:
        from core.queue_detector import QueueDetector
        logger.info("正在初始化排队检测器...", module="Vision")
        queue_detector = QueueDetector()
        logger.info("✅ 排队检测器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 排队检测器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 9. 门牌号识别器
    try:
        from core.doorplate_reader import DoorplateReader
        logger.info("正在初始化门牌号识别器...", module="Vision")
        doorplate_reader = DoorplateReader()
        logger.info("✅ 门牌号识别器初始化成功", module="Vision")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 门牌号识别器初始化异常", details={"error": str(e)}, module="Vision")
    
    # 10. 本地地图生成器
    try:
        from core.local_map_generator import LocalMapGenerator
        logger.info("正在初始化本地地图生成器...", module="Navigation")
        local_map_generator = LocalMapGenerator()
        logger.info("✅ 本地地图生成器初始化成功", module="Navigation")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 本地地图生成器初始化异常", details={"error": str(e)}, module="Navigation")
    
    # 11. 场景记忆系统
    try:
        from core.scene_memory_system import get_scene_memory_system
        logger.info("正在初始化场景记忆系统...", module="Scene")
        scene_memory_system = get_scene_memory_system()
        logger.info("✅ 场景记忆系统初始化成功", module="Scene")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 场景记忆系统初始化异常", details={"error": str(e)}, module="Scene")
    
    # 12. 日志管理器
    try:
        from core.log_manager import LogManager
        logger.info("正在初始化日志管理器...", module="System")
        log_manager = LogManager(user_id="web_test_user")
        logger.info("✅ 日志管理器初始化成功", module="System")
        success_count += 1
    except Exception as e:
        logger.warn("⚠️ 日志管理器初始化异常", details={"error": str(e)}, module="System")
    
    logger.info(f"✅ 模块初始化完成: {success_count} 个模块成功", module="System")
    
    return success_count > 0



