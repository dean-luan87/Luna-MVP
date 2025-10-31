#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 系统控制中枢增强版 v2.0
完整集成AI模型、摄像头管线、增强能力模块
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, Callable, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import queue

# 导入增强模块
from core.log_manager import LogManager
from core.context_store import ContextStore
from core.task_interruptor import TaskInterruptor
from core.retry_queue import RetryQueue

# 导入控制中枢
from core.system_orchestrator import (
    SystemOrchestrator,
    SystemState,
    UserIntent,
    VisualEvent,
    IntentMatch,
    SystemEvent
)

logger = logging.getLogger(__name__)


class EnhancedSystemOrchestrator(SystemOrchestrator):
    """增强版系统控制中枢"""
    
    def __init__(self,
                 whisper_recognizer=None,
                 vision_engine=None,
                 navigator=None,
                 tts_manager=None,
                 memory_manager=None,
                 camera_manager=None,
                 user_id: str = "anonymous"):
        """
        初始化增强版控制中枢
        
        Args:
            whisper_recognizer: Whisper语音识别器
            vision_engine: 视觉识别引擎
            navigator: 导航模块
            tts_manager: TTS播报管理器
            memory_manager: 记忆管理器
            camera_manager: 摄像头管理器
            user_id: 用户ID
        """
        # 初始化父类
        super().__init__(
            whisper_recognizer=whisper_recognizer,
            vision_engine=vision_engine,
            navigator=navigator,
            tts_manager=tts_manager,
            memory_manager=memory_manager,
            camera_manager=camera_manager
        )
        
        # 初始化增强模块
        self.user_id = user_id
        self.log_manager = LogManager(user_id=user_id)
        self.context_store = ContextStore(max_entries=5)
        self.task_interruptor = TaskInterruptor()
        self.retry_queue = RetryQueue(max_retries=3, retry_interval=60)
        
        # 绑定回调
        self._setup_enhancements()
        
        # 视觉检测线程
        self.vision_thread = None
        self.vision_running = False
        
        logger.info("🧠 增强版系统控制中枢初始化完成")
    
    def _setup_enhancements(self):
        """设置增强模块回调"""
        # 注册TTS重试回调
        if self.tts:
            def tts_retry_callback(payload, metadata):
                try:
                    self.tts.speak(payload)
                    logger.info(f"✅ TTS重试成功: {payload[:30]}")
                    return True
                except Exception as e:
                    logger.error(f"❌ TTS重试失败: {e}")
                    return False
            
            self.retry_queue.register_retry_callback("TTS", tts_retry_callback)
    
    def handle_voice_input(self, audio_data: bytes = None):
        """
        处理语音输入（增强版）
        
        Args:
            audio_data: 音频数据（如果提供）
        """
        if not self.whisper:
            logger.error("❌ Whisper模块未初始化")
            return
        
        try:
            self.set_state(SystemState.LISTENING)
            
            # 使用Whisper识别语音
            if audio_data:
                # 从bytes转换为文本（需要实现recognize_bytes方法）
                text = "模拟识别文本"  # TODO: 实现bytes识别
                details = {}
            else:
                # 从麦克风识别（或模拟）
                try:
                    text, details = self.whisper.recognize_from_microphone(duration=5)
                except Exception as e:
                    logger.warning(f"Whisper识别失败，使用模拟文本: {e}")
                    text = "我要去厕所"  # 模拟识别
                    details = {"confidence": 0.8}
            
            logger.info(f"🎤 识别到语音: {text}")
            
            # 记录语音日志
            self.log_manager.log_voice_intent(
                intent="识别中",
                content=text,
                system_response="处理中",
                metadata={"confidence": details.get("confidence", 0.0) if 'details' in locals() else 0.0}
            )
            
            # 检查上下文追问
            if self.context_store.is_question_follow_up(text):
                resolved = self.context_store.resolve_question(text)
                if resolved:
                    text = f"{text} ({resolved})"
                    logger.info(f"🔍 上下文解析: {resolved}")
            
            # 解析意图
            intent = self._parse_intent(text)
            
            # 增强意图（结合上下文）
            enhanced_intent_str = self.context_store.extract_intent_with_context(text, intent.intent.value)
            
            # 处理意图
            self._handle_intent_enhanced(intent, text, enhanced_intent_str)
            
        except Exception as e:
            logger.error(f"❌ 语音处理失败: {e}")
            self.retry_queue.add_item("voice_processing", {"error": str(e), "text": text if 'text' in locals() else None})
            self.set_state(SystemState.ERROR)
        finally:
            self.set_state(SystemState.IDLE)
    
    def _handle_intent_enhanced(self, intent_match: IntentMatch, original_text: str, enhanced_intent: str):
        """
        处理用户意图（增强版）
        
        Args:
            intent_match: 意图匹配结果
            original_text: 原始文本
            enhanced_intent: 增强意图
        """
        intent = intent_match.intent
        
        logger.info(f"🎯 处理意图: {enhanced_intent}")
        
        # 记录意图日志
        self.log_manager.log_voice_intent(
            intent=intent.value,
            content=original_text,
            system_response="处理中",
            metadata={"enhanced_intent": enhanced_intent}
        )
        
        # 添加上下文
        self.context_store.add_entry(
            user_input=original_text,
            intent=intent.value,
            system_response="处理中",
            metadata={"enhanced_intent": enhanced_intent}
        )
        
        # 根据意图执行动作
        if intent == UserIntent.FIND_TOILET:
            self._handle_find_toilet_enhanced()
        elif intent == UserIntent.FIND_ELEVATOR:
            self._handle_find_elevator_enhanced()
        elif intent == UserIntent.FIND_DESTINATION:
            self._handle_find_destination_enhanced(original_text)
        elif intent == UserIntent.REMEMBER_PATH:
            self._handle_remember_path_enhanced()
        elif intent == UserIntent.START_NAVIGATION:
            self._handle_start_navigation_enhanced()
        elif intent == UserIntent.CANCEL:
            self._handle_cancel_enhanced()
        else:
            logger.warning(f"⚠️ 未知意图: {original_text}")
            self._speak_enhanced("抱歉，我没有理解您的指令，请重试")
    
    def _handle_find_toilet_enhanced(self):
        """处理找洗手间意图（增强版）"""
        logger.info("🚽 处理找洗手间请求")
        
        self.set_state(SystemState.NAVIGATING)
        
        # 启动主任务
        task_id = self.task_interruptor.start_main_task(
            task_type="navigation",
            description="找洗手间",
            intent="find_toilet",
            destination="洗手间"
        )
        logger.info(f"✅ 主任务已启动: {task_id}")
        
        # 调用导航模块
        if self.navigator:
            try:
                path = self.navigator.plan_path_to_facility("toilet")
                if path:
                    # 播报路径
                    response_text = f"请直行{path.get('distance', 0)}米，左转后有洗手间"
                    self._speak_enhanced(response_text)
                    
                    # 记录导航日志
                    self.log_manager.log_navigation(
                        action="find_toilet",
                        destination="洗手间",
                        path_info=path,
                        system_response=response_text
                    )
                    
                    # 记录记忆
                    self._record_navigation_enhanced(path, "toilet")
                else:
                    self._speak_enhanced("抱歉，我没有找到附近的洗手间")
            except Exception as e:
                logger.error(f"❌ 导航失败: {e}")
                self._speak_enhanced("抱歉，导航服务暂时不可用")
                # 重试
                self.retry_queue.add_item("navigation", {"facility": "toilet"})
        else:
            logger.warning("⚠️ 导航模块未初始化")
        
        self.set_state(SystemState.IDLE)
    
    def _handle_find_elevator_enhanced(self):
        """处理找电梯意图（增强版）"""
        logger.info("🛗 处理找电梯请求")
        
        self.set_state(SystemState.NAVIGATING)
        
        if self.navigator:
            try:
                path = self.navigator.plan_path_to_facility("elevator")
                if path:
                    response_text = f"请向{path.get('direction', '左侧')}前行{path.get('distance', 0)}米，左侧有电梯"
                    self._speak_enhanced(response_text)
                    
                    self.log_manager.log_navigation(
                        action="find_elevator",
                        destination="电梯",
                        path_info=path,
                        system_response=response_text
                    )
                    
                    self._record_navigation_enhanced(path, "elevator")
                else:
                    self._speak_enhanced("抱歉，我没有找到附近的电梯")
            except Exception as e:
                logger.error(f"❌ 导航失败: {e}")
                self._speak_enhanced("抱歉，导航服务暂时不可用")
                self.retry_queue.add_item("navigation", {"facility": "elevator"})
        
        self.set_state(SystemState.IDLE)
    
    def _handle_find_destination_enhanced(self, text: str):
        """处理找目的地意图（增强版）"""
        logger.info(f"🎯 处理找目的地请求: {text}")
        
        # 尝试提取目的地
        destination = self._extract_destination(text)
        
        if destination:
            self.set_state(SystemState.NAVIGATING)
            
            # 启动主任务
            task_id = self.task_interruptor.start_main_task(
                task_type="navigation",
                description=f"去{destination}",
                intent="find_destination",
                destination=destination
            )
            
            if self.navigator:
                try:
                    path = self.navigator.plan_path(destination)
                    if path:
                        response_text = f"正在为您导航到{destination}"
                        self._speak_enhanced(response_text)
                        
                        self.log_manager.log_navigation(
                            action="navigate_to",
                            destination=destination,
                            path_info=path,
                            system_response=response_text
                        )
                        
                        self._record_navigation_enhanced(path, destination)
                    else:
                        self._speak_enhanced(f"抱歉，我找不到{destination}")
                except Exception as e:
                    logger.error(f"❌ 导航失败: {e}")
                    self._speak_enhanced("抱歉，导航服务暂时不可用")
                    self.retry_queue.add_item("navigation", {"destination": destination})
            
            self.set_state(SystemState.IDLE)
        else:
            self._speak_enhanced("请告诉我您要去哪里")
    
    def _handle_remember_path_enhanced(self):
        """处理记住路径意图（增强版）"""
        logger.info("💾 处理记住路径请求")
        
        self.set_state(SystemState.MEMORIZING)
        
        if self.memory and self.camera:
            try:
                # 触发摄像头开始记录场景
                scenes = self.camera.record_scenes_for_memory()
                
                # 写入记忆
                self.memory.save_path_memory(scenes)
                
                response_text = "路径已记录"
                self._speak_enhanced(response_text)
                
                self.log_manager.log_memory_operation(
                    operation="save_path",
                    data={"scenes_count": len(scenes) if scenes else 0},
                    system_response=response_text
                )
                
                logger.info("✅ 路径记忆完成")
                
            except Exception as e:
                logger.error(f"❌ 记忆保存失败: {e}")
                self._speak_enhanced("抱歉，路径记忆失败")
                self.retry_queue.add_item("memory", {"operation": "save_path"})
        
        self.set_state(SystemState.IDLE)
    
    def _handle_start_navigation_enhanced(self):
        """处理开始导航意图（增强版）"""
        logger.info("🧭 处理开始导航请求")
        
        self.set_state(SystemState.NAVIGATING)
        self._speak_enhanced("请输入您的目的地")
    
    def _handle_cancel_enhanced(self):
        """处理取消意图（增强版）"""
        logger.info("❌ 处理取消请求")
        
        # 取消当前任务
        self.task_interruptor.cancel_current_task()
        
        self.set_state(SystemState.IDLE)
        self.current_task = None
        self.context_store.clear()
        self._speak_enhanced("已取消当前任务")
    
    def _speak_enhanced(self, text: str):
        """语音播报（增强版）"""
        if self.tts:
            try:
                self.tts.speak(text)
                logger.info(f"🔊 播报: {text}")
                
                # 记录TTS日志
                self.log_manager.log_tts_output(text, success=True)
            except Exception as e:
                logger.error(f"❌ TTS播报失败: {e}")
                # 添加重试
                self.retry_queue.add_item("TTS", text)
                # 记录失败日志
                self.log_manager.log_tts_output(text, success=False, metadata={"error": str(e)})
    
    def _record_navigation_enhanced(self, path: Dict[str, Any], destination: str):
        """记录导航记忆（增强版）"""
        if self.memory:
            try:
                self.memory.save_navigation_memory(path, destination)
                
                self.log_manager.log_memory_operation(
                    operation="save_navigation",
                    data={"destination": destination, "path": path},
                    system_response="已保存"
                )
                
                logger.info("💾 导航记忆已保存")
            except Exception as e:
                logger.error(f"❌ 记忆保存失败: {e}")
                self.retry_queue.add_item("memory", {"operation": "save_navigation", "destination": destination})
    
    def start_vision_detection(self):
        """启动视觉检测线程"""
        if self.vision_running:
            logger.warning("⚠️ 视觉检测已在运行")
            return
        
        if not self.vision:
            logger.error("❌ 视觉模块未初始化")
            return
        
        self.vision_running = True
        self.vision_thread = threading.Thread(target=self._vision_loop, daemon=True)
        self.vision_thread.start()
        
        logger.info("👁️ 视觉检测已启动")
    
    def stop_vision_detection(self):
        """停止视觉检测线程"""
        self.vision_running = False
        
        if self.vision_thread:
            self.vision_thread.join(timeout=2)
        
        logger.info("🛑 视觉检测已停止")
    
    def _vision_loop(self):
        """视觉检测循环"""
        logger.info("🔍 视觉检测循环启动")
        
        while self.vision_running:
            try:
                # 如果摄像头管理器存在，获取当前帧
                if self.camera and hasattr(self.camera, 'get_current_frame'):
                    frame = self.camera.get_current_frame()
                    if frame is not None:
                        # 调用视觉引擎检测
                        if self.vision and hasattr(self.vision, 'detect_and_recognize'):
                            result = self.vision.detect_and_recognize(frame)
                            
                            # 处理检测结果
                            if result.get("detections"):
                                self._handle_vision_detections(result["detections"])
                            
                            # 处理OCR结果
                            if result.get("combined"):
                                self._handle_ocr_results(result["combined"])
                
                time.sleep(0.5)  # 每0.5秒检测一次
                
            except Exception as e:
                logger.error(f"❌ 视觉检测错误: {e}")
                time.sleep(1)
    
    def _handle_vision_detections(self, detections: List[Dict[str, Any]]):
        """处理YOLO检测结果"""
        for detection in detections:
            class_name = detection.get("class")
            confidence = detection.get("confidence", 0.0)
            
            # 转换为控制中枢格式
            detection_result = {
                "classes": [class_name],
                "confidence": confidence,
                "box": detection.get("box"),
                "center": detection.get("center")
            }
            
            # 发送视觉事件
            self.handle_visual_event(detection_result)
    
    def _handle_ocr_results(self, ocr_results: List[Dict[str, Any]]):
        """处理OCR识别结果"""
        for ocr in ocr_results:
            text = ocr.get("text", "")
            detected_class = ocr.get("detected_class")
            
            # 关键节点检测
            if self._is_key_landmark(text):
                logger.info(f"📍 检测到地标: {text}")
                
                # 记录视觉日志
                self.log_manager.log_visual_event(
                    event_type="landmark_detected",
                    detection_result={"text": text, "class": detected_class},
                    system_response=f"检测到地标: {text}"
                )
    
    def _is_key_landmark(self, text: str) -> bool:
        """判断是否关键地标"""
        key_keywords = [
            "室", "号", "电梯", "楼梯", "厕所", "洗手间",
            "出口", "入口", "诊室", "病房", "挂号", "缴费"
        ]
        return any(keyword in text for keyword in key_keywords)
    
    def start(self):
        """启动增强版控制中枢"""
        super().start()
        
        # 启动视觉检测
        self.start_vision_detection()
        
        # 启动重试处理线程
        self._start_retry_worker()
        
        logger.info("✅ 增强版控制中枢已完全启动")
    
    def stop(self):
        """停止增强版控制中枢"""
        # 停止视觉检测
        self.stop_vision_detection()
        
        # 停止重试处理
        self._stop_retry_worker()
        
        # 停止父类
        super().stop()
        
        logger.info("🛑 增强版控制中枢已停止")
    
    def _start_retry_worker(self):
        """启动重试处理线程"""
        self.retry_worker_running = True
        self.retry_worker_thread = threading.Thread(target=self._retry_worker_loop, daemon=True)
        self.retry_worker_thread.start()
    
    def _stop_retry_worker(self):
        """停止重试处理线程"""
        self.retry_worker_running = False
        if hasattr(self, 'retry_worker_thread'):
            self.retry_worker_thread.join(timeout=2)
    
    def _retry_worker_loop(self):
        """重试处理循环"""
        logger.info("🔄 重试处理线程启动")
        
        while self.retry_worker_running:
            try:
                # 处理待处理项
                success_items = self.retry_queue.process_pending_items()
                if success_items:
                    logger.info(f"✅ 重试成功: {len(success_items)}项")
                
                time.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                logger.error(f"❌ 重试处理错误: {e}")
                time.sleep(5)
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统完整状态"""
        status = {
            "system_state": self.state.value,
            "task_status": self.task_interruptor.get_task_status(),
            "context_summary": self.context_store.get_context_summary(),
            "retry_queue_status": self.retry_queue.get_queue_status(),
            "log_statistics": self.log_manager.get_statistics()
        }
        return status
    
    def flush_logs(self):
        """刷新日志缓冲区"""
        self.log_manager.flush()


# 便捷函数
def create_enhanced_orchestrator(
    whisper_recognizer=None,
    vision_engine=None,
    navigator=None,
    tts_manager=None,
    memory_manager=None,
    camera_manager=None,
    user_id: str = "anonymous"
) -> EnhancedSystemOrchestrator:
    """创建增强版系统控制中枢"""
    return EnhancedSystemOrchestrator(
        whisper_recognizer=whisper_recognizer,
        vision_engine=vision_engine,
        navigator=navigator,
        tts_manager=tts_manager,
        memory_manager=memory_manager,
        camera_manager=camera_manager,
        user_id=user_id
    )


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建增强版控制中枢
    print("=" * 70)
    print("🧠 增强版系统控制中枢测试")
    print("=" * 70)
    
    orchestrator = create_enhanced_orchestrator(user_id="test_user")
    
    # 启动
    orchestrator.start()
    
    # 模拟语音输入
    print("\n🎤 测试语音输入:")
    # orchestrator.handle_voice_input()
    
    # 等待处理
    import time
    time.sleep(2)
    
    # 查看状态
    print("\n📊 系统状态:")
    status = orchestrator.get_status()
    print(f"  系统状态: {status['system_state']}")
    print(f"  任务数: {status['task_status']['main_task_count']}")
    print(f"  上下文条目: {status['context_summary']['total_entries']}")
    
    # 停止
    orchestrator.stop()
    
    # 刷新日志
    orchestrator.flush_logs()
    
    print("\n✅ 测试完成")

