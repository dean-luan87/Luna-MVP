#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 离线地图导航测试脚本
支持无WiFi环境下的完整导航功能测试
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.navigation_manager import NavigationManager, NavigationStatus
from core.path_planner import PathPlanner
from core.scene_memory_system import SceneMemorySystem
from core.local_map_generator import LocalMapGenerator
from core.signboard_detector import SignboardDetector
from core.step_detector import StepDetector
from core.vision_ocr_engine import VisionOCREngine
from core.tts_manager import TTSManager
from core.whisper_recognizer import WhisperRecognizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OfflineNavigationTester:
    """离线导航测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.navigation_manager = NavigationManager()
        self.scene_memory = SceneMemorySystem()
        self.path_planner = PathPlanner(self.scene_memory)
        self.map_generator = LocalMapGenerator()
        self.signboard_detector = SignboardDetector()
        self.step_detector = StepDetector()
        self.vision_engine = None
        self.tts_manager = TTSManager()
        self.whisper_recognizer = WhisperRecognizer(model_name="base", language="zh")
        
        # 测试数据
        self.test_route = []
        self.current_position = None
        self.destination = None
        
        logger.info("🧭 离线导航测试器初始化完成")
    
    def init_vision_engine(self):
        """初始化视觉引擎"""
        try:
            from core.vision_ocr_engine import VisionOCREngine
            self.vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
            if self.vision_engine.load_models():
                logger.info("✅ 视觉引擎初始化成功")
                return True
            else:
                logger.warning("⚠️ 视觉引擎初始化失败，将使用模拟模式")
                return False
        except Exception as e:
            logger.warning(f"⚠️ 视觉引擎初始化异常: {e}")
            return False
    
    def get_gps_position(self) -> Optional[Tuple[float, float]]:
        """
        获取GPS位置（如果可用）
        
        Returns:
            Optional[Tuple[float, float]]: (纬度, 经度) 或 None
        """
        try:
            # 尝试使用geopy或其他GPS库
            # 这里提供一个模拟接口，实际使用时需要真实的GPS数据
            logger.info("📍 GPS定位功能需要真实GPS数据")
            logger.info("💡 提示：可以使用手机GPS或手动输入位置")
            return None
        except Exception as e:
            logger.warning(f"GPS定位失败: {e}")
            return None
    
    def manual_set_position(self, lat: float, lng: float):
        """手动设置当前位置"""
        self.current_position = (lat, lng)
        if self.navigation_manager:
            self.navigation_manager.update_position(lat, lng)
        logger.info(f"📍 当前位置已设置: ({lat}, {lng})")
    
    def start_navigation_test(self, destination: str, start_position: Optional[Tuple[float, float]] = None):
        """
        开始导航测试
        
        Args:
            destination: 目的地名称
            start_position: 起始位置 (lat, lng)，如果为None则使用GPS或手动设置
        """
        logger.info("=" * 60)
        logger.info("🧭 开始离线导航测试")
        logger.info("=" * 60)
        
        # 设置起始位置
        if start_position:
            self.manual_set_position(start_position[0], start_position[1])
        else:
            gps_pos = self.get_gps_position()
            if gps_pos:
                self.manual_set_position(gps_pos[0], gps_pos[1])
            else:
                logger.warning("⚠️ 无法获取GPS位置，请手动设置起始位置")
                logger.info("💡 使用方法: tester.manual_set_position(纬度, 经度)")
                return
        
        # 设置目的地
        self.destination = destination
        
        # 启动导航
        if self.navigation_manager.start_navigation(destination):
            logger.info(f"✅ 导航已启动: 前往 {destination}")
            self._run_navigation_loop()
        else:
            logger.error("❌ 导航启动失败")
    
    def _run_navigation_loop(self):
        """运行导航循环"""
        logger.info("🔄 开始导航循环...")
        logger.info("💡 提示：")
        logger.info("  1. 使用摄像头拍摄路标和标识牌")
        logger.info("  2. 系统会自动识别并更新导航路径")
        logger.info("  3. 语音播报导航指令")
        logger.info("  4. 按Ctrl+C停止导航")
        
        try:
            step_count = 0
            while True:
                # 检查导航状态
                if not self.navigation_manager.current_navigation:
                    logger.info("导航已结束")
                    break
                
                if self.navigation_manager.current_navigation.status != NavigationStatus.ACTIVE:
                    logger.info(f"导航状态: {self.navigation_manager.current_navigation.status.value}")
                    break
                
                # 模拟导航步骤
                step_count += 1
                logger.info(f"\n📍 导航步骤 {step_count}")
                
                # 检查是否需要视觉辅助
                if step_count % 3 == 0:
                    self._visual_assistance_step()
                
                # 生成导航指令
                instruction = self._generate_navigation_instruction(step_count)
                logger.info(f"🗣️ 导航指令: {instruction}")
                
                # 语音播报（如果TTS可用）
                try:
                    self.tts_manager.speak_sync(instruction)
                except:
                    logger.info("TTS播报跳过（可能无音频输出）")
                
                # 等待用户移动
                time.sleep(5)  # 模拟移动时间
                
                # 更新位置（模拟）
                if self.current_position:
                    # 模拟向前移动（实际应该使用GPS或步数）
                    self._simulate_movement()
                
        except KeyboardInterrupt:
            logger.info("\n⚠️ 用户中断导航")
            self.navigation_manager.cancel_navigation("用户中断")
    
    def _visual_assistance_step(self):
        """视觉辅助步骤"""
        logger.info("👁️ 视觉辅助检测中...")
        logger.info("💡 请使用摄像头拍摄当前环境（标识牌、路标等）")
        logger.info("💡 提示：在实际使用中，系统会自动进行视觉检测")
        
        # 这里可以集成实际的摄像头检测
        # 当前为模拟模式
    
    def _generate_navigation_instruction(self, step: int) -> str:
        """生成导航指令"""
        instructions = [
            "请向前直行约50米",
            "前方100米处右转",
            "继续直行，注意前方台阶",
            "前方50米到达目的地",
            "请向左转",
            "前方有标识牌，请注意查看"
        ]
        
        if step <= len(instructions):
            return instructions[step - 1]
        else:
            return f"继续前行，距离目的地约{100 - step * 10}米"
    
    def _simulate_movement(self):
        """模拟移动（实际应使用GPS）"""
        if self.current_position:
            # 模拟向前移动10米（约0.0001度）
            lat, lng = self.current_position
            new_lat = lat + 0.0001
            self.manual_set_position(new_lat, lng)
    
    def test_visual_navigation(self, image_path: str):
        """
        测试视觉导航（识别标识牌、台阶等）
        
        Args:
            image_path: 图片路径
        """
        logger.info(f"👁️ 测试视觉导航: {image_path}")
        
        if not self.vision_engine:
            if not self.init_vision_engine():
                logger.error("视觉引擎不可用")
                return
        
        try:
            import cv2
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"无法读取图片: {image_path}")
                return
            
            # 标识牌检测
            signboards = self.signboard_detector.detect_signboards(image)
            logger.info(f"🚏 检测到 {len(signboards)} 个标识牌:")
            for sb in signboards:
                logger.info(f"  - {sb.text} ({sb.type.value}, 置信度: {sb.confidence:.2f})")
            
            # 台阶检测
            step_result = self.step_detector.detect_step(image)
            if step_result:
                logger.info(f"🪜 检测到台阶: {step_result.get('direction', '未知')}")
            
            # OCR识别
            ocr_results = self.vision_engine.recognize_text(image)
            logger.info(f"📝 识别到 {len(ocr_results)} 段文字:")
            for ocr in ocr_results[:5]:  # 只显示前5个
                logger.info(f"  - {ocr.text} (置信度: {ocr.confidence:.2f})")
            
            # 生成导航建议
            self._generate_navigation_suggestion(signboards, step_result, ocr_results)
            
        except Exception as e:
            logger.error(f"视觉导航测试失败: {e}")
    
    def _generate_navigation_suggestion(self, signboards, step_result, ocr_results):
        """根据视觉识别结果生成导航建议"""
        suggestions = []
        
        # 检查标识牌
        for sb in signboards:
            if sb.type.value in ['exit', 'toilet', 'elevator']:
                suggestions.append(f"发现{sb.text}标识牌，可以前往")
        
        # 检查台阶
        if step_result:
            direction = step_result.get('direction', '')
            if direction:
                suggestions.append(f"前方有台阶，方向: {direction}")
        
        # 检查OCR中的导航关键词
        nav_keywords = ['出口', '入口', '电梯', '楼梯', '厕所', '洗手间']
        for ocr in ocr_results:
            for keyword in nav_keywords:
                if keyword in ocr.text:
                    suggestions.append(f"识别到导航信息: {ocr.text}")
                    break
        
        if suggestions:
            logger.info("\n💡 导航建议:")
            for i, suggestion in enumerate(suggestions, 1):
                logger.info(f"  {i}. {suggestion}")
        else:
            logger.info("💡 未发现明显的导航信息")
    
    def save_test_route(self, file_path: str = "data/test_navigation_route.json"):
        """保存测试路线"""
        route_data = {
            "destination": self.destination,
            "start_position": list(self.current_position) if self.current_position else None,
            "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "navigation_status": self.navigation_manager.current_navigation.status.value if self.navigation_manager.current_navigation else None
        }
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(route_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 测试路线已保存: {file_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("🧭 Luna 离线地图导航测试")
    print("=" * 60)
    print()
    print("功能说明：")
    print("1. 支持离线导航（无需WiFi）")
    print("2. 视觉辅助导航（标识牌、台阶识别）")
    print("3. 语音播报导航指令")
    print("4. GPS定位（如果可用）或手动设置位置")
    print()
    
    tester = OfflineNavigationTester()
    
    # 初始化视觉引擎
    print("正在初始化视觉引擎...")
    tester.init_vision_engine()
    
    # 测试菜单
    while True:
        print("\n" + "=" * 60)
        print("请选择测试模式：")
        print("1. 开始导航测试（需要设置起始位置和目的地）")
        print("2. 测试视觉导航（识别标识牌、台阶等）")
        print("3. 手动设置当前位置")
        print("4. 查看当前导航状态")
        print("5. 退出")
        print("=" * 60)
        
        choice = input("请输入选项 (1-5): ").strip()
        
        if choice == "1":
            destination = input("请输入目的地: ").strip()
            if not destination:
                print("❌ 目的地不能为空")
                continue
            
            # 询问起始位置
            use_gps = input("是否使用GPS定位？(y/N): ").strip().lower() == 'y'
            start_pos = None
            
            if not use_gps:
                pos_input = input("请输入起始位置（格式：纬度,经度，例如：31.2304,121.4737）: ").strip()
                try:
                    lat, lng = map(float, pos_input.split(','))
                    start_pos = (lat, lng)
                except:
                    print("❌ 位置格式错误，使用默认位置")
                    start_pos = (31.2304, 121.4737)  # 上海默认位置
            
            tester.start_navigation_test(destination, start_pos)
            
        elif choice == "2":
            image_path = input("请输入图片路径: ").strip()
            if os.path.exists(image_path):
                tester.test_visual_navigation(image_path)
            else:
                print(f"❌ 图片不存在: {image_path}")
        
        elif choice == "3":
            pos_input = input("请输入位置（格式：纬度,经度）: ").strip()
            try:
                lat, lng = map(float, pos_input.split(','))
                tester.manual_set_position(lat, lng)
                print(f"✅ 当前位置已设置: ({lat}, {lng})")
            except:
                print("❌ 位置格式错误")
        
        elif choice == "4":
            if tester.navigation_manager.current_navigation:
                nav = tester.navigation_manager.current_navigation
                print(f"目的地: {nav.destination}")
                print(f"状态: {nav.status.value}")
                print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nav.start_time))}")
            else:
                print("当前没有进行中的导航")
        
        elif choice == "5":
            print("👋 退出测试")
            break
        
        else:
            print("❌ 无效选项")

if __name__ == "__main__":
    main()







