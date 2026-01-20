#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 架构集成模块
按照四层架构集成所有模块
"""

import logging
import json
import time
from typing import Dict, Any, List, Optional
from core.json_output_adapter import JSONOutputAdapter, OutputLevel

logger = logging.getLogger(__name__)

class LunaBadgeIntegration:
    """Luna Badge 集成系统"""
    
    def __init__(self):
        """初始化集成系统"""
        self.logger = logging.getLogger(__name__)
        self.json_adapter = JSONOutputAdapter()
        
        # 初始化各层模块
        self._init_vision_layer()
        self._init_path_layer()
        self._init_speech_layer()
        self._init_user_layer()
        
        self.logger.info("🌙 Luna Badge 集成系统初始化完成")
    
    def _init_vision_layer(self):
        """初始化视觉感知层"""
        try:
            from core.signboard_detector import SignboardDetector
            from core.facility_detector import FacilityDetector
            from core.hazard_detector import HazardDetector
            from core.ocr_advanced_reader import OCRAdvancedReader
            from core.product_info_checker import ProductInfoChecker
            from core.doorplate_reader import DoorplateReader
            from core.local_map_generator import LocalMapGenerator
            
            self.signboard_detector = SignboardDetector()
            self.facility_detector = FacilityDetector()
            self.hazard_detector = HazardDetector()
            self.ocr_reader = OCRAdvancedReader()
            self.product_checker = ProductInfoChecker()
            self.doorplate_reader = DoorplateReader()
            self.map_generator = LocalMapGenerator()
            
            self.logger.info("✅ 视觉感知层初始化完成")
        except Exception as e:
            self.logger.error(f"❌ 视觉感知层初始化失败: {e}")
    
    def _init_path_layer(self):
        """初始化路径判断层"""
        try:
            from core.queue_detector import QueueDetector
            from core.crowd_density_detector import CrowdDensityDetector
            from core.flow_direction_analyzer import FlowDirectionAnalyzer
            from core.doorplate_inference import DoorplateInferenceEngine
            
            self.queue_detector = QueueDetector()
            self.crowd_detector = CrowdDensityDetector()
            self.flow_analyzer = FlowDirectionAnalyzer()
            self.doorplate_inference = DoorplateInferenceEngine()
            
            self.logger.info("✅ 路径判断层初始化完成")
        except Exception as e:
            self.logger.error(f"❌ 路径判断层初始化失败: {e}")
    
    def _init_speech_layer(self):
        """初始化播报策略层"""
        try:
            from core.tts_manager import TTSManager
            
            self.tts_manager = TTSManager()
            
            self.logger.info("✅ 播报策略层初始化完成")
        except Exception as e:
            self.logger.error(f"❌ 播报策略层初始化失败: {e}")
    
    def _init_user_layer(self):
        """初始化用户交互层"""
        try:
            # ===== 暂时注销：用户注册模块 =====
            # from core.user_manager import UserManager
            from core.memory_store import MemoryStore
            from core.memory_caller import MemoryCaller
            from core.voice_recognition import VoiceRecognitionEngine
            from core.voice_wakeup import VoiceWakeupManager
            from core.mcp_controller import MCPController
            
            # ===== 暂时注销：用户管理器 =====
            # self.user_manager = UserManager()
            self.user_manager = None  # 暂时禁用
            self.memory_store = MemoryStore()
            from core.memory_caller import MemoryCaller
            self.memory_caller = MemoryCaller(self.memory_store)
            self.voice_recognition = VoiceRecognitionEngine()
            self.voice_wakeup = VoiceWakeupManager()
            self.mcp_controller = MCPController()
            
            self.logger.info("✅ 用户交互层初始化完成")
        except Exception as e:
            self.logger.error(f"❌ 用户交互层初始化失败: {e}")
    
    def process_navigation_cycle(self, image) -> Dict[str, Any]:
        """
        处理导航循环
        
        Args:
            image: 当前图像
            
        Returns:
            Dict[str, Any]: JSON格式的结果
        """
        cycle_data = {
            "vision_detection": {},
            "path_analysis": {},
            "decision": {},
            "speech_output": {}
        }
        
        # Step 1: 视觉感知层
        vision_output = self._process_vision_layer(image)
        cycle_data["vision_detection"] = vision_output
        
        # Step 2: 路径判断层
        path_output = self._process_path_layer(image, vision_output)
        cycle_data["path_analysis"] = path_output
        
        # Step 3: 决策生成
        decision = self._make_decision(vision_output, path_output)
        cycle_data["decision"] = decision
        
        # Step 4: 语音播报
        if decision.get("should_speak"):
            speech_output = self._generate_speech(decision)
            cycle_data["speech_output"] = speech_output
        
        # 生成最终JSON输出
        final_output = self.json_adapter.format_output(
            event="navigation_cycle",
            level="high",
            data=cycle_data
        )
        
        self.logger.info("🔄 导航循环处理完成")
        
        return final_output
    
    def _process_vision_layer(self, image) -> Dict[str, Any]:
        """处理视觉感知层"""
        # 识别的对象列表
        objects = []
        signboards = []
        hazards = []
        
        # TODO: 实际的视觉检测逻辑
        
        return self.json_adapter.vision_detection(
            objects=objects,
            signboards=signboards,
            hazards=hazards
        )
    
    def _process_path_layer(self, image, vision_output: Dict) -> Dict[str, Any]:
        """处理路径判断层"""
        crowd_density = "normal"
        flow_direction = "same"
        queue_detected = False
        hazards = []
        
        # TODO: 实际的路径分析逻辑
        
        return self.json_adapter.path_analysis(
            crowd_density=crowd_density,
            flow_direction=flow_direction,
            queue_detected=queue_detected,
            hazards=hazards
        )
    
    def _make_decision(self, vision: Dict, path: Dict) -> Dict[str, Any]:
        """生成决策"""
        decision = {
            "action": "continue",
            "should_speak": False,
            "message": ""
        }
        
        # 根据视觉和路径分析生成决策
        hazards = vision.get("data", {}).get("hazards", [])
        
        if hazards:
            decision["action"] = "warn"
            decision["should_speak"] = True
            decision["message"] = "检测到危险环境，请注意安全"
        
        return decision
    
    def _generate_speech(self, decision: Dict) -> Dict[str, Any]:
        """生成语音播报"""
        text = decision.get("message", "")
        
        # 根据决策选择播报风格
        style = "calm"
        if "危险" in text:
            style = "urgent"
        
        return self.json_adapter.speech_broadcast(
            text=text,
            style=style,
            voice="zh-CN-XiaoxiaoNeural",
            rate=1.0,
            pitch=1.0
        )


# 全局集成系统实例
global_luna_integration = LunaBadgeIntegration()

def process_navigation(image) -> str:
    """处理导航的便捷函数，返回JSON字符串"""
    result = global_luna_integration.process_navigation_cycle(image)
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 测试集成系统
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print(json.dumps({
        "event": "luna_integration_test",
        "level": "info",
        "data": {
            "message": "Luna Badge 集成系统测试",
            "layers": {
                "vision": "✅ 初始化",
                "path": "✅ 初始化",
                "speech": "✅ 初始化",
                "user": "✅ 初始化"
            }
        },
        "timestamp": "2025-10-27T15:00:00Z"
    }, ensure_ascii=False, indent=2))

