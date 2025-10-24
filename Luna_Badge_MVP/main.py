#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge MVP 主程序
整合所有模块，实现完整的实时执行链路
"""

import cv2
import time
import signal
import sys
import logging
import threading
from typing import Optional, Dict, Any
import numpy as np

# 导入核心模块
from core.state_tracker import StateTracker
from core.cooldown_manager import CooldownManager
from core.logger import setup_logger
from core.debug_logger import DebugLogger, get_debug_logger, EventType, LogLevel
from core.debug_ui import DebugUI
from core.ota_manager import OTAUpdateManager, get_ota_manager
from core.config_manager import ConfigManager, get_config_manager
from core.voice_pack_manager import VoicePackManager, get_voice_pack_manager
from vision.yolov5_detector import YOLOv5Detector
from vision.deepsort_tracker import DeepSortTracker
from vision.path_predict import PathPredictor
from speech.speech_engine import SpeechEngine

class LunaBadgeMVP:
    """Luna Badge MVP系统"""
    
    def __init__(self, debug_mode: bool = False):
        """初始化系统"""
        self.running = False
        self.camera = None
        self.frame_count = 0
        self.debug_mode = debug_mode
        
        # 初始化日志
        self.logger = setup_logger("LunaBadgeMVP")
        
        # 初始化调试日志管理器
        self.debug_logger = get_debug_logger("LunaBadgeMVP", debug_mode)
        self.debug_ui = DebugUI(self.debug_logger)
        
        # 初始化OTA更新管理器
        self.ota_manager = get_ota_manager()
        self.config_manager = get_config_manager()
        self.voice_pack_manager = get_voice_pack_manager()
        
        # 初始化核心组件
        self.state_tracker = StateTracker()
        self.cooldown_manager = CooldownManager()
        self.speech_engine = SpeechEngine()
        
        # 初始化视觉组件
        self.yolo_detector = YOLOv5Detector()
        self.tracker = DeepSortTracker()
        self.path_predictor = PathPredictor()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("🌙 Luna Badge MVP系统初始化开始")
        self.debug_logger.log_event(EventType.SYSTEM, LogLevel.INFO, "Luna Badge MVP系统初始化开始", {
            "debug_mode": debug_mode
        })
        
        # 检查OTA更新
        self._check_ota_updates()
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        self.logger.info(f"⚠️ 接收到信号 {signum}，正在关闭系统...")
        self.stop()
    
    def _check_ota_updates(self):
        """检查OTA更新"""
        try:
            self.logger.info("🔍 检查OTA更新...")
            
            # 检查本地更新
            updates = self.ota_manager.check_local_updates()
            
            if updates:
                self.logger.info(f"📁 发现 {len(updates)} 个本地更新")
                self.debug_logger.log_event(EventType.SYSTEM, LogLevel.INFO, f"发现 {len(updates)} 个本地更新", {
                    "update_count": len(updates),
                    "updates": updates
                })
                
                # 应用更新
                results = self.ota_manager.apply_all_updates(updates, backup=True)
                
                if results["success"] > 0:
                    self.logger.info(f"✅ 成功应用 {results['success']} 个更新")
                    self.debug_logger.log_event(EventType.SYSTEM, LogLevel.INFO, f"成功应用 {results['success']} 个更新", results)
                    
                    # 重新加载配置
                    self._reload_configurations()
                else:
                    self.logger.warning("⚠️ 没有成功应用任何更新")
            else:
                self.logger.info("📁 没有发现本地更新")
                
        except Exception as e:
            self.logger.error(f"❌ OTA更新检查失败: {e}")
            self.debug_logger.log_error(f"OTA更新检查失败: {e}")
    
    def _reload_configurations(self):
        """重新加载配置"""
        try:
            self.logger.info("🔄 重新加载配置...")
            
            # 重新加载配置管理器
            self.config_manager.reload_all_configs()
            
            # 重新加载语音包管理器
            self.voice_pack_manager.voice_pack_cache.clear()
            
            self.logger.info("✅ 配置重新加载完成")
            self.debug_logger.log_event(EventType.SYSTEM, LogLevel.INFO, "配置重新加载完成")
            
        except Exception as e:
            self.logger.error(f"❌ 配置重新加载失败: {e}")
            self.debug_logger.log_error(f"配置重新加载失败: {e}")
    
    def initialize(self) -> bool:
        """
        初始化所有组件
        
        Returns:
            bool: 是否初始化成功
        """
        try:
            self.logger.info("🔧 开始初始化系统组件...")
            
            # 初始化状态跟踪器
            if not self.state_tracker.initialize():
                self.logger.error("❌ 状态跟踪器初始化失败")
                return False
            
            # 初始化冷却管理器
            if not self.cooldown_manager.initialize():
                self.logger.error("❌ 冷却管理器初始化失败")
                return False
            
            # 初始化语音引擎
            if not self.speech_engine.initialize():
                self.logger.error("❌ 语音引擎初始化失败")
                return False
            
            # 初始化YOLO检测器
            if not self.yolo_detector.initialize():
                self.logger.error("❌ YOLO检测器初始化失败")
                return False
            
            # 初始化跟踪器
            if not self.tracker.initialize():
                self.logger.error("❌ 跟踪器初始化失败")
                return False
            
            # 初始化路径预测器
            if not self.path_predictor.initialize():
                self.logger.error("❌ 路径预测器初始化失败")
                return False
            
            # 初始化摄像头
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self.logger.error("❌ 摄像头初始化失败")
                return False
            
            # 设置摄像头参数
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.logger.info("✅ 摄像头初始化完成")
            
            # 播报系统启动消息
            self._announce_system_startup()
            
            self.logger.info("✅ 系统初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 系统初始化失败: {e}")
            return False
    
    def _announce_system_startup(self):
        """播报系统启动消息"""
        try:
            # 使用语音引擎播报
            self.speech_engine.speak("Luna系统启动完成", priority=0)
            self.logger.info("🗣️ 系统启动消息已播报")
        except Exception as e:
            self.logger.error(f"❌ 启动消息播报失败: {e}")
    
    def _process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        处理图像帧
        
        Args:
            frame: 输入图像帧
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        result = {
            "detections": [],
            "tracks": [],
            "path_prediction": None,
            "should_speak": False,
            "speech_text": None,
            "priority": 1
        }
        
        try:
            # YOLO目标检测
            if self.frame_count % 5 == 0:  # 每5帧检测一次
                detections = self.yolo_detector.detect(frame)
                result["detections"] = detections
                
                # 记录检测事件
                self.debug_logger.log_detection(detections)
                
                # 目标跟踪
                tracks = self.tracker.update(detections)
                result["tracks"] = tracks
                
                # 记录跟踪事件
                self.debug_logger.log_tracking(tracks)
                
                # 路径预测
                path_prediction = self.path_predictor.predict(tracks)
                result["path_prediction"] = path_prediction
                
                # 记录预测事件
                if path_prediction:
                    self.debug_logger.log_prediction(path_prediction)
                
                # 判断是否需要播报
                if path_prediction and path_prediction.get("obstructed", False):
                    if self.cooldown_manager.can_trigger("path_obstructed"):
                        result["should_speak"] = True
                        result["speech_text"] = "前方有障碍物，请注意安全"
                        result["priority"] = 0  # 高优先级
                        self.cooldown_manager.trigger("path_obstructed")
                        self.state_tracker.set_flag("path_obstructed_announced", True)
                        
                        # 记录语音事件
                        self.debug_logger.log_speech(result["speech_text"], result["priority"], "queued")
                        
                        # 记录冷却事件
                        self.debug_logger.log_cooldown("path_obstructed", False, 
                                                     self.cooldown_manager.get_remaining_time("path_obstructed"))
                        
                elif path_prediction and not path_prediction.get("obstructed", True):
                    if self.cooldown_manager.can_trigger("path_clear"):
                        result["should_speak"] = True
                        result["speech_text"] = "前方路径畅通"
                        result["priority"] = 1
                        self.cooldown_manager.trigger("path_clear")
                        self.state_tracker.set_flag("path_clear_announced", True)
                        
                        # 记录语音事件
                        self.debug_logger.log_speech(result["speech_text"], result["priority"], "queued")
                        
                        # 记录冷却事件
                        self.debug_logger.log_cooldown("path_clear", False, 
                                                     self.cooldown_manager.get_remaining_time("path_clear"))
            
            # 更新调试信息
            self.debug_ui.update_debug_info({
                "frame_count": self.frame_count,
                "detection_count": len(result["detections"]),
                "track_count": len(result["tracks"]),
                "debug_mode": self.debug_mode
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 帧处理失败: {e}")
            self.debug_logger.log_error(f"帧处理失败: {e}", {"frame_count": self.frame_count})
            return result
    
    def run(self):
        """运行主循环"""
        if not self.initialize():
            self.logger.error("❌ 系统初始化失败，无法启动")
            return
        
        self.running = True
        self.logger.info("🚀 Luna Badge MVP系统启动完成，开始主循环")
        
        try:
            while self.running:
                # 读取摄像头帧
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.error("❌ 无法读取摄像头帧")
                    break
                
                # 处理帧
                result = self._process_frame(frame)
                
                # 播报语音
                if result["should_speak"] and result["speech_text"]:
                    self.speech_engine.speak(result["speech_text"], result["priority"])
                
                # 显示图像（带调试信息）
                if self.debug_mode:
                    debug_frame = self.debug_ui.draw_debug_overlay(frame, result["detections"], result["tracks"], result["path_prediction"])
                    self.debug_ui.show_debug_window(debug_frame)
                else:
                    self._draw_debug_info(frame, result)
                    cv2.imshow("Luna Badge MVP", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # 更新帧计数
                self.frame_count += 1
                
                # 控制帧率
                time.sleep(1.0 / 30)
                
        except KeyboardInterrupt:
            self.logger.info("⚠️ 用户中断")
        except Exception as e:
            self.logger.error(f"❌ 主循环运行失败: {e}")
        finally:
            self.stop()
    
    def _draw_debug_info(self, frame: np.ndarray, result: Dict[str, Any]):
        """
        在图像上绘制调试信息
        
        Args:
            frame: 图像帧
            result: 处理结果
        """
        try:
            # 绘制帧计数
            cv2.putText(frame, f"Frame: {self.frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制检测结果
            if result["detections"]:
                cv2.putText(frame, f"Detections: {len(result['detections'])}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制跟踪结果
            if result["tracks"]:
                cv2.putText(frame, f"Tracks: {len(result['tracks'])}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制路径预测结果
            if result["path_prediction"]:
                if result["path_prediction"].get("obstructed", False):
                    cv2.putText(frame, "Path: OBSTRUCTED", (10, 150), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Path: CLEAR", (10, 150), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制语音状态
            if result["should_speak"]:
                cv2.putText(frame, f"SPEAKING (P{result['priority']})", (10, 190), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # 绘制系统状态
            cv2.putText(frame, "Luna Badge MVP", (10, 230), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
        except Exception as e:
            self.logger.error(f"❌ 调试信息绘制失败: {e}")
    
    def stop(self):
        """停止系统"""
        self.logger.info("🛑 正在停止Luna Badge MVP系统...")
        
        self.running = False
        
        # 停止语音引擎
        if self.speech_engine:
            self.speech_engine.stop()
            self.logger.info("✅ 语音引擎已停止")
        
        # 释放摄像头
        if self.camera:
            self.camera.release()
            self.logger.info("✅ 摄像头已释放")
        
        # 关闭OpenCV窗口
        cv2.destroyAllWindows()
        
        # 保存状态
        if self.state_tracker:
            self.state_tracker.save()
            self.logger.info("✅ 状态已保存")
        
        # 导出调试日志
        if self.debug_logger:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            log_file = f"logs/debug_export_{timestamp}.json"
            self.debug_logger.export_logs(log_file)
            self.logger.info(f"✅ 调试日志已导出: {log_file}")
        
        self.logger.info("✅ Luna Badge MVP系统已停止")
        self.debug_logger.log_event(EventType.SYSTEM, LogLevel.INFO, "Luna Badge MVP系统已停止")

def main():
    """主函数"""
    print("🌙 Luna Badge MVP 主程序启动")
    print("=" * 50)
    
    # 检查是否启用调试模式
    debug_mode = "--debug" in sys.argv
    
    if debug_mode:
        print("🔍 调试模式已启用")
        print("调试功能:")
        print("  - 按 'd' 键切换调试显示")
        print("  - 按 'l' 键导出调试日志")
        print("  - 按 'c' 键清除调试信息")
        print("  - 按 'q' 键退出程序")
        print("=" * 50)
    
    try:
        # 创建Luna Badge MVP系统
        luna_system = LunaBadgeMVP(debug_mode=debug_mode)
        
        # 运行系统
        luna_system.run()
        
    except Exception as e:
        print(f"❌ 主程序运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("✅ Luna Badge MVP 主程序结束")

if __name__ == "__main__":
    main()
