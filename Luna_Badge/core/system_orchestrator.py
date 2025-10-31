#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 系统控制中枢 (System Orchestrator)
统一调度语音、视觉、地图、TTS等子系统，实现"一个指令，多模态响应"
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, Callable, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import queue

logger = logging.getLogger(__name__)


class SystemState(Enum):
    """系统状态"""
    IDLE = "idle"                    # 空闲
    LISTENING = "listening"          # 监听中
    NAVIGATING = "navigating"        # 导航中
    MEMORIZING = "memorizing"        # 记忆中
    PROCESSING = "processing"        # 处理中
    ERROR = "error"                  # 错误


class UserIntent(Enum):
    """用户意图"""
    FIND_TOILET = "find_toilet"              # 找洗手间
    FIND_ELEVATOR = "find_elevator"          # 找电梯
    FIND_DESTINATION = "find_destination"    # 找目的地
    REMEMBER_PATH = "remember_path"          # 记住路径
    START_NAVIGATION = "start_navigation"    # 开始导航
    CANCEL = "cancel"                        # 取消
    UNKNOWN = "unknown"                      # 未知


class VisualEvent(Enum):
    """视觉事件"""
    STAIRS_DETECTED = "stairs_detected"      # 台阶检测
    ELEVATOR_DETECTED = "elevator_detected"  # 电梯检测
    TOILET_SIGN_DETECTED = "toilet_sign"     # 卫生间标识
    EXIT_SIGN_DETECTED = "exit_sign"         # 出口标识
    OBSTACLE_DETECTED = "obstacle_detected"  # 障碍物
    SAFE = "safe"                           # 安全


@dataclass
class IntentMatch:
    """意图匹配结果"""
    intent: UserIntent
    confidence: float
    extracted_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemEvent:
    """系统事件"""
    event_type: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        elif self.timestamp is None:
            self.timestamp = datetime.now()


class SystemOrchestrator:
    """系统控制中枢"""
    
    def __init__(self,
                 whisper_recognizer=None,
                 vision_engine=None,
                 navigator=None,
                 tts_manager=None,
                 memory_manager=None,
                 camera_manager=None):
        """
        初始化控制中枢
        
        Args:
            whisper_recognizer: Whisper语音识别器
            vision_engine: 视觉识别引擎
            navigator: 导航模块
            tts_manager: TTS播报管理器
            memory_manager: 记忆管理器
            camera_manager: 摄像头管理器
        """
        # 模块引用
        self.whisper = whisper_recognizer
        self.vision = vision_engine
        self.navigator = navigator
        self.tts = tts_manager
        self.memory = memory_manager
        self.camera = camera_manager
        
        # 系统状态
        self.state = SystemState.IDLE
        self.current_task = None
        self.context = {}  # 上下文信息
        
        # 事件队列
        self.event_queue = queue.Queue()
        self.event_handlers = {}
        
        # 运行标志
        self.is_running = False
        self.event_thread = None
        
        # 日志记录
        self.action_logs = []
        
        logger.info("🧠 系统控制中枢初始化完成")
    
    def start(self):
        """启动控制中枢"""
        if self.is_running:
            logger.warning("⚠️ 控制中枢已在运行")
            return
        
        self.is_running = True
        self.event_thread = threading.Thread(target=self._event_loop, daemon=True)
        self.event_thread.start()
        
        logger.info("✅ 控制中枢已启动")
    
    def stop(self):
        """停止控制中枢"""
        self.is_running = False
        
        if self.event_thread:
            self.event_thread.join(timeout=2)
        
        logger.info("🛑 控制中枢已停止")
    
    def handle_voice_input(self, audio_data: bytes = None):
        """
        处理语音输入
        
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
                text = self.whisper.recognize_bytes(audio_data)
            else:
                text = self.whisper.recognize_audio_file()
            
            logger.info(f"🎤 识别到语音: {text}")
            
            # 解析意图
            intent = self._parse_intent(text)
            
            # 处理意图
            self._handle_intent(intent, text)
            
        except Exception as e:
            logger.error(f"❌ 语音处理失败: {e}")
            self.set_state(SystemState.ERROR)
        finally:
            self.set_state(SystemState.IDLE)
    
    def handle_visual_event(self, detection_result: Dict[str, Any]):
        """
        处理视觉检测事件
        
        Args:
            detection_result: YOLO检测结果
        """
        if not self.vision:
            logger.error("❌ 视觉模块未初始化")
            return
        
        try:
            # 解析检测结果
            event = self._parse_visual_event(detection_result)
            
            if event:
                # 发送事件到队列
                system_event = SystemEvent(
                    event_type="visual",
                    timestamp=datetime.now(),
                    data={"visual_event": event, "detection": detection_result}
                )
                self.event_queue.put(system_event)
                
                logger.info(f"👁️ 视觉事件: {event}")
                
        except Exception as e:
            logger.error(f"❌ 视觉处理失败: {e}")
    
    def _parse_intent(self, text: str) -> IntentMatch:
        """
        解析用户意图
        
        Args:
            text: 语音识别文本
            
        Returns:
            意图匹配结果
        """
        text_lower = text.lower()
        
        # 意图关键词映射
        intent_keywords = {
            UserIntent.FIND_TOILET: ["厕所", "卫生间", "洗手间", "toilet", "washroom"],
            UserIntent.FIND_ELEVATOR: ["电梯", "elevator", "lift"],
            UserIntent.FIND_DESTINATION: ["去", "到", "找", "go to", "find"],
            UserIntent.REMEMBER_PATH: ["记住", "记录", "remember", "record"],
            UserIntent.START_NAVIGATION: ["开始导航", "启动导航", "start navigation"],
            UserIntent.CANCEL: ["取消", "停止", "cancel", "stop"]
        }
        
        # 匹配意图
        best_match = None
        best_confidence = 0.0
        extracted_data = {}
        
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    confidence = len(keyword) / len(text_lower)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent
                        extracted_data["keyword"] = keyword
                        break
        
        if not best_match:
            best_match = UserIntent.UNKNOWN
            best_confidence = 0.1
        
        return IntentMatch(intent=best_match, confidence=best_confidence, extracted_data=extracted_data)
    
    def _handle_intent(self, intent_match: IntentMatch, original_text: str):
        """
        处理用户意图
        
        Args:
            intent_match: 意图匹配结果
            original_text: 原始文本
        """
        intent = intent_match.intent
        
        logger.info(f"🎯 处理意图: {intent.value}")
        
        # 记录动作日志
        self._log_action("voice_intent", {
            "intent": intent.value,
            "text": original_text,
            "confidence": intent_match.confidence
        })
        
        # 根据意图执行动作
        if intent == UserIntent.FIND_TOILET:
            self._handle_find_toilet()
        
        elif intent == UserIntent.FIND_ELEVATOR:
            self._handle_find_elevator()
        
        elif intent == UserIntent.FIND_DESTINATION:
            self._handle_find_destination(original_text)
        
        elif intent == UserIntent.REMEMBER_PATH:
            self._handle_remember_path()
        
        elif intent == UserIntent.START_NAVIGATION:
            self._handle_start_navigation()
        
        elif intent == UserIntent.CANCEL:
            self._handle_cancel()
        
        else:
            logger.warning(f"⚠️ 未知意图: {original_text}")
            self._speak("抱歉，我没有理解您的指令，请重试")
    
    def _parse_visual_event(self, detection_result: Dict[str, Any]) -> Optional[VisualEvent]:
        """
        解析视觉检测事件
        
        Args:
            detection_result: 检测结果
            
        Returns:
            视觉事件
        """
        if not detection_result:
            return None
        
        detected_classes = detection_result.get("classes", [])
        
        # 事件关键词映射
        event_keywords = {
            VisualEvent.STAIRS_DETECTED: ["stairs", "楼梯", "台阶"],
            VisualEvent.ELEVATOR_DETECTED: ["elevator", "电梯"],
            VisualEvent.TOILET_SIGN_DETECTED: ["toilet", "卫生间", "洗手间", "厕所"],
            VisualEvent.EXIT_SIGN_DETECTED: ["exit", "出口", "emergency"],
            VisualEvent.OBSTACLE_DETECTED: ["obstacle", "障碍物", "barrier"]
        }
        
        # 匹配事件
        for event, keywords in event_keywords.items():
            for keyword in keywords:
                for cls in detected_classes:
                    if keyword in cls.lower():
                        return event
        
        return VisualEvent.SAFE
    
    def _handle_find_toilet(self):
        """处理找洗手间意图"""
        logger.info("🚽 处理找洗手间请求")
        
        self.set_state(SystemState.NAVIGATING)
        
        # 调用导航模块
        if self.navigator:
            try:
                path = self.navigator.plan_path_to_facility("toilet")
                if path:
                    # 播报路径
                    self._speak(f"请直行{path.get('distance', 0)}米，左转后有洗手间")
                    
                    # 记录记忆
                    self._record_navigation(path, "toilet")
                else:
                    self._speak("抱歉，我没有找到附近的洗手间")
            except Exception as e:
                logger.error(f"❌ 导航失败: {e}")
                self._speak("抱歉，导航服务暂时不可用")
        
        self.set_state(SystemState.IDLE)
    
    def _handle_find_elevator(self):
        """处理找电梯意图"""
        logger.info("🛗 处理找电梯请求")
        
        self.set_state(SystemState.NAVIGATING)
        
        if self.navigator:
            try:
                path = self.navigator.plan_path_to_facility("elevator")
                if path:
                    self._speak(f"请向{path.get('direction', '左侧')}前行{path.get('distance', 0)}米，左侧有电梯")
                    self._record_navigation(path, "elevator")
                else:
                    self._speak("抱歉，我没有找到附近的电梯")
            except Exception as e:
                logger.error(f"❌ 导航失败: {e}")
                self._speak("抱歉，导航服务暂时不可用")
        
        self.set_state(SystemState.IDLE)
    
    def _handle_find_destination(self, text: str):
        """处理找目的地意图"""
        logger.info(f"🎯 处理找目的地请求: {text}")
        
        # 尝试提取目的地
        destination = self._extract_destination(text)
        
        if destination:
            self.set_state(SystemState.NAVIGATING)
            
            if self.navigator:
                try:
                    path = self.navigator.plan_path(destination)
                    if path:
                        self._speak(f"正在为您导航到{destination}")
                        self._record_navigation(path, destination)
                    else:
                        self._speak(f"抱歉，我找不到{destination}")
                except Exception as e:
                    logger.error(f"❌ 导航失败: {e}")
                    self._speak("抱歉，导航服务暂时不可用")
            
            self.set_state(SystemState.IDLE)
        else:
            self._speak("请告诉我您要去哪里")
    
    def _handle_remember_path(self):
        """处理记住路径意图"""
        logger.info("💾 处理记住路径请求")
        
        self.set_state(SystemState.MEMORIZING)
        
        if self.memory and self.camera:
            try:
                # 触发摄像头开始记录场景
                scenes = self.camera.record_scenes_for_memory()
                
                # 写入记忆
                self.memory.save_path_memory(scenes)
                
                self._speak("路径已记录")
                logger.info("✅ 路径记忆完成")
                
            except Exception as e:
                logger.error(f"❌ 记忆保存失败: {e}")
                self._speak("抱歉，路径记忆失败")
        
        self.set_state(SystemState.IDLE)
    
    def _handle_start_navigation(self):
        """处理开始导航意图"""
        logger.info("🧭 处理开始导航请求")
        
        self.set_state(SystemState.NAVIGATING)
        self._speak("请输入您的目的地")
    
    def _handle_cancel(self):
        """处理取消意图"""
        logger.info("❌ 处理取消请求")
        
        self.set_state(SystemState.IDLE)
        self.current_task = None
        self.context = {}
        self._speak("已取消当前任务")
    
    def _extract_destination(self, text: str) -> Optional[str]:
        """从文本中提取目的地"""
        # 简单的提取逻辑（可以后续优化为NER）
        import re
        
        # 匹配房间号、科室名等
        patterns = [
            r'(\d+)号诊室',
            r'(\d+)室',
            r'(\d+)F',
            r'(\d+)楼',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        # 提取关键名词
        keywords = ["诊室", "病房", "大厅", "挂号", "缴费", "取药"]
        for keyword in keywords:
            if keyword in text:
                return keyword
        
        return None
    
    def _speak(self, text: str):
        """语音播报"""
        if self.tts:
            try:
                self.tts.speak(text)
                logger.info(f"🔊 播报: {text}")
                
                # 记录动作日志
                self._log_action("tts_speak", {"text": text})
            except Exception as e:
                logger.error(f"❌ TTS播报失败: {e}")
    
    def _record_navigation(self, path: Dict[str, Any], destination: str):
        """记录导航记忆"""
        if self.memory:
            try:
                self.memory.save_navigation_memory(path, destination)
                logger.info("💾 导航记忆已保存")
            except Exception as e:
                logger.error(f"❌ 记忆保存失败: {e}")
    
    def _event_loop(self):
        """事件循环"""
        logger.info("🔄 事件循环启动")
        
        while self.is_running:
            try:
                # 从队列获取事件
                event = self.event_queue.get(timeout=1)
                
                # 处理事件
                self._process_event(event)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 事件处理错误: {e}")
    
    def _process_event(self, event: SystemEvent):
        """处理系统事件"""
        logger.info(f"⚡ 处理事件: {event.event_type}")
        
        # 视觉事件处理
        if event.event_type == "visual":
            self._handle_visual_feedback(event.data)
    
    def _handle_visual_feedback(self, data: Dict[str, Any]):
        """处理视觉反馈"""
        visual_event = data.get("visual_event")
        
        if not visual_event:
            return
        
        # 视觉事件 -> 语音提醒映射
        feedback_map = {
            VisualEvent.STAIRS_DETECTED: "前方有台阶，请小心",
            VisualEvent.ELEVATOR_DETECTED: "已到达电梯，请注意看标识",
            VisualEvent.TOILET_SIGN_DETECTED: "左侧有卫生间标识",
            VisualEvent.EXIT_SIGN_DETECTED: "前方有出口标识",
            VisualEvent.OBSTACLE_DETECTED: "前方有障碍物，请绕行"
        }
        
        feedback_text = feedback_map.get(visual_event)
        
        if feedback_text:
            self._speak(feedback_text)
            logger.info(f"👁️ 视觉反馈: {feedback_text}")
    
    def set_state(self, state: SystemState):
        """设置系统状态"""
        self.state = state
        logger.debug(f"🔄 状态切换: {state.value}")
    
    def _log_action(self, action_type: str, data: Dict[str, Any]):
        """记录动作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "data": data
        }
        
        self.action_logs.append(log_entry)
        
        # 限制日志长度
        if len(self.action_logs) > 1000:
            self.action_logs = self.action_logs[-1000:]
    
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取最近的日志"""
        return self.action_logs[-limit:]
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        self.event_handlers[event_type] = handler
        logger.info(f"✅ 注册事件处理器: {event_type}")


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建控制中枢
    orchestrator = SystemOrchestrator()
    
    print("=" * 60)
    print("🧠 Luna Badge 系统控制中枢测试")
    print("=" * 60)
    
    # 测试语音输入
    print("\n🎤 测试语音输入:")
    orchestrator.handle_voice_input()
    
    # 测试视觉事件
    print("\n👁️ 测试视觉事件:")
    detection = {
        "classes": ["stairs", "person"],
        "confidence": 0.95
    }
    orchestrator.handle_visual_event(detection)
    
    print("\n✅ 测试完成")

