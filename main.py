# -*- coding: utf-8 -*-
"""
Luna 实体徽章 MVP - 主程序
实现"看得见、说得出、记得下"的完整流程
"""

import cv2
import time
import json
import numpy as np
from datetime import datetime
import argparse
import sys
import os
from typing import Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# v1.8.5 Phase B Step 3.2: 导入 WorldUpdate
from core.world_model.common.types import WorldUpdate

# ===== Phase 1 测试期硬开关 =====
# 禁止 TTS 重初始化，避免音频系统自激振荡
ENABLE_TTS_REINIT = False

# 音频 IO 状态管理（防止 TTS 和 ASR 同时抢设备）
audio_io_state = "IDLE"  # IDLE / RECORDING / SPEAKING

# 帧节流：测试期降低处理频率，避免 CPU 被抢
FRAME_MIN_INTERVAL = 0.5  # 500ms，测试期不追求实时性
last_frame_ts = 0

# 导入配置和工具模块
from config import MODEL_PATHS, CAMERA_CONFIG, PROCESSING_CONFIG, OUTPUT_CONFIG, DEBUG_CONFIG, RISK_SHADOW_MODE
from utils import (
    WhisperProcessor, TTSProcessor, setup_logger, JSONLogger
)
# v1.8.5 Phase B Step 1.4: QwenVLProcessor 迁移到 ModelingExecutor，不再直接导入
# from utils import QwenVLProcessor  # 已迁移到 vision_pipeline.lv4_executors.modeling_executor
# v1.8.5 Phase B Step 1.3: OCRProcessor 迁移到 ModelingExecutor，不再直接导入
# from utils import OCRProcessor  # 已迁移到 vision_pipeline.lv4_executors.modeling_executor
# v1.8.5 Phase B Step 1.2: YOLODetector 迁移到 NavigationExecutor，不再直接导入
# from utils import YOLODetector  # 已迁移到 vision_pipeline.lv4_executors.navigation_executor
# v1.8.5 Phase B Step 1.1: CameraHandler 迁移到 PipelineController，不再直接导入
# from utils import CameraHandler  # 已迁移到 vision_pipeline
from vision_pipeline import PipelineController
from utils.system_voice_recognition import SystemVoiceRecognition, listen_and_recognize
from modules.voice import Voice
from core.audio_playback_guard import acquire_audio_lock, release_audio_lock
from core.audio_worker import submit_tts, start_audio_worker, stop_audio_worker
from core.scene_state_builder import SceneStateBuilder
from core.system_memory import SystemMemory
from core.decision_scheduler import DecisionScheduler
from core.speech_gate import SpeechGate
from core.decision_controller import decide, UserState
from core.risk import (
    RiskAdvisoryService, UserPositionProvider, RiskRegistry, RiskObjectFactory
)


class LunaBadgeMVP:
    """Luna 实体徽章 MVP 主类"""
    
    def __init__(self):
        """初始化Luna徽章系统"""
        # 设置日志
        self.logger = setup_logger('luna_badge')
        self.json_logger = JSONLogger()
        
        # v1.8.3a 修复：先初始化决策层，再初始化 TTS
        # 初始化顺序：decision_scheduler → speech_gate → tts_engine
        # 处理状态
        self.is_running = False
        self.last_process_time = 0
        # v1.8.4: Risk 调试快照频率控制
        self._last_risk_debug_ts = 0.0
        
        # v1.8.3: 系统级调度与串联层（System Orchestration）
        # ⚠️ 必须在 TTS 之前初始化，否则 TTS 初始化时会访问不存在的 scheduler
        self.scene_state_builder = SceneStateBuilder()
        self.system_memory = SystemMemory()
        self.decision_scheduler = DecisionScheduler(system_memory=self.system_memory)
        # v1.8.3a: 语音总闸（系统级"注意力与发言权中枢"）
        self.speech_gate = SpeechGate(cooldown_seconds=3.0)
        # v1.8.3a 阶段 C: 用户状态（用于决策闭环）
        self.user_state = UserState()
        # v1.8.3: 风险上下文缓存（用于 LV2）
        self.risk_context_cache = {}
        # v1.8.4: 风险告知系统初始化
        self.risk_registry = RiskRegistry(object_ttl_seconds=60.0)
        self.risk_object_factory = RiskObjectFactory()
        self.user_position_provider = UserPositionProvider()
        self.risk_advisory_service = RiskAdvisoryService(
            registry=self.risk_registry,
            enable_debug=DEBUG_CONFIG.get("enable_risk_debug", False)  # v1.8.4: 启用调试快照生成
        )
        self.logger.info("v1.8.3 系统级调度层已初始化")
        self.logger.info("v1.8.4 风险告知系统已初始化")
        
        # 现在才初始化 TTS（此时 decision_scheduler 和 speech_gate 已存在）
        self.logger.info("正在初始化语音播报模块...")
        try:
            self.voice = Voice()
            if self.voice.is_available:
                self.logger.info("语音播报模块初始化成功")
                # 播放启动提示音
                # 第二层修复：改为异步投递，不直接播放
                self._speak_safely("Luna 已启动", scene_hash=None)
            else:
                self.logger.warning("语音播报模块不可用，将静默运行")
        except Exception as e:
            self.logger.error(f"语音播报模块初始化失败: {e}")
            self.voice = None
        
        # v1.8.5 Phase B Step 1.1: CameraHandler 迁移到 PipelineController
        # 初始化视觉流水线控制器（包含 CameraHandler）
        self.logger.info("正在初始化视觉流水线...")
        self.pipeline_controller = PipelineController()
        
        # 检查摄像头状态（通过 PipelineController）
        if not self.pipeline_controller.is_opened():
            self.logger.error("摄像头初始化失败，程序可能无法正常运行")
            self.logger.info("请检查:")
            self.logger.info("1. 摄像头是否已连接")
            self.logger.info("2. 摄像头是否被其他程序占用")
            self.logger.info("3. 系统权限设置（Mac需要摄像头权限）")
            # 语音提示摄像头问题
            # v1.8.3a: 通过语音总闸统一入口
            self._speak_safely("摄像头初始化失败，请检查摄像头连接", scene_hash=None)
        else:
            self.logger.info("摄像头初始化成功")
            # 语音提示摄像头正常
            # v1.8.3a: 通过语音总闸统一入口
            self._speak_safely("摄像头初始化成功", scene_hash=None)
        
        self.logger.info("正在初始化AI模型...")
        # v1.8.5 Phase B Step 1.2: YOLODetector 迁移到 NavigationExecutor，不再在此初始化
        # self.yolo_detector = YOLODetector()  # 已迁移到 NavigationExecutor
        # v1.8.5 Phase B Step 1.3: OCRProcessor 迁移到 ModelingExecutor，不再在此初始化
        # self.ocr_processor = OCRProcessor()  # 已迁移到 ModelingExecutor
        # v1.8.5 Phase B Step 1.4: QwenVLProcessor 迁移到 ModelingExecutor，不再在此初始化
        # self.qwen_processor = QwenVLProcessor()  # 已迁移到 ModelingExecutor
        self.whisper_processor = WhisperProcessor()
        self.tts_processor = TTSProcessor()
        
        # 初始化语音识别模块
        self.logger.info("正在初始化系统语音识别模块...")
        try:
            self.voice_recognition = SystemVoiceRecognition()
            if self.voice_recognition.is_available:
                self.logger.info("系统语音识别模块初始化成功")
                # 测试麦克风
                if self.voice_recognition.test_microphone():
                    self.logger.info("麦克风测试成功")
                else:
                    self.logger.warning("麦克风测试失败")
            else:
                self.logger.warning("语音识别模块不可用")
        except Exception as e:
            self.logger.error(f"语音识别模块初始化失败: {e}")
            self.voice_recognition = None
        
        # v1.8.3a 修复：初始化顺序已在上面完成（在 TTS 初始化之前）
        # 处理状态（已在上面初始化，这里只是确认）
        # self.is_running 和 self.last_process_time 已在第60-61行初始化
        
        self.logger.info("Luna 实体徽章 MVP 初始化完成")
        
        # 启动音频工作线程（第二层修复：音频播放脱离主循环）
        start_audio_worker()
        self.logger.info("音频工作线程已启动")
        
        # 语音提示系统就绪（异步投递，不阻塞）
        # v1.8.3a: 通过语音总闸统一入口
        self._speak_safely("系统初始化完成，开始运行", scene_hash=None)
    
    def _speak_safely(self, text: str, scene_hash: Optional[str] = None):
        """
        安全的语音播报方法（v1.8.3a: 通过语音总闸统一入口）
        
        关键原则：
        - 必须通过 speech_gate.can_speak() 检查
        - 不等待
        - 不阻塞
        - 主循环永远不能等音频
        
        Args:
            text: 要播报的文本
            scene_hash: 场景哈希值（用于去重）
        """
        global audio_io_state
        
        # 第一层修复：录音时禁止 TTS
        if audio_io_state == "RECORDING":
            self.logger.debug("[SpeechGate] 正在录音中，跳过语音播报")
            return
        
        if not text or not text.strip():
            return
        
        if not self.voice:
            self.logger.warning("语音模块未初始化")
            return
            
        if not self.voice.is_available:
            self.logger.warning("语音模块不可用")
            return
        
        # v1.8.3a: 通过语音总闸检查（系统级"注意力与发言权中枢"）
        # 检查用户是否正在说话（从 decision_scheduler 获取状态）
        user_speaking = getattr(self.decision_scheduler, 'user_speaking', False)
        
        can_speak, reason = self.speech_gate.can_speak(
            scene_hash=scene_hash,
            user_speaking=user_speaking
        )
        
        if not can_speak:
            self.logger.debug(f"[SpeechGate] 禁止播报: {text[:30]}... (原因: {reason})")
            return
        
        # 获取说话权
        if not self.speech_gate.acquire(owner="speak_safely"):
            self.logger.warning("[SpeechGate] 获取说话权失败")
            return
        
        try:
            # 第二层修复：投递到音频工作线程，不直接播放
            success = submit_tts(text, self.voice)
            if success:
                self.logger.debug(f"[SpeechGate] 已投递播放任务: {text[:50]}...")
            else:
                # 队列满，已丢弃（测试期允许漏播）
                self.logger.debug(f"[SpeechGate] 队列已满，丢弃播放任务: {text[:30]}...")
        finally:
            # 释放说话权（设置冷却）
            self.speech_gate.release(scene_hash=scene_hash)
    
    def _handle_immediate_risk(self, risk_result):
        """
        v1.8.3: 处理 LV1 即时风险（强制播报）
        
        Args:
            risk_result: 风险评估结果
        """
        if not risk_result:
            return
        
        if not self.speech_gate:
            return
        
        # 强制占用 speech_gate（可以打断系统播报）
        if self.speech_gate.force_acquire(owner="risk_lv1", source="RISK"):
            try:
                warning = self._generate_risk_warning(risk_result)
                if warning:
                    self.logger.warning(
                        f"[RiskAssessor] LV1 警报触发: {risk_result.reason} "
                        f"(ttc={risk_result.ttc}, distance={risk_result.distance})"
                    )
                    # 直接调用 TTS，不经过 _speak_safely（因为已经强制获取了锁）
                    if self.voice and self.voice.is_available:
                        from core.audio_worker import submit_tts
                        submit_tts(warning, self.voice)
            finally:
                # 释放锁（LV1 不设置冷却，因为已经强制清除了）
                self.speech_gate.release(scene_hash=None, cooldown=0.0)
    
    def _generate_risk_warning(self, risk_result) -> str:
        """
        v1.8.3: 生成风险警告文本
        
        Args:
            risk_result: 风险评估结果
        
        Returns:
            str: 警告文本
        """
        if not risk_result:
            return ""
        
        reason = risk_result.reason
        if reason == "water_edge":
            return "前方存在危险，请立即停下"
        elif reason == "road":
            return "前方有潜在危险，请注意安全"
        else:
            return "前方有潜在危险，请注意安全"
    
    def _build_voice_text(self, result: dict) -> str:
        """
        构建语音播报内容
        
        Args:
            result: 识别结果字典
            
        Returns:
            构建的语音文本
        """
        try:
            voice_parts = []
            
            # 添加检测到的物体信息
            if result['objects']:
                object_names = [obj['label'] for obj in result['objects']]
                if len(object_names) == 1:
                    voice_parts.append(f"检测到{object_names[0]}")
                else:
                    voice_parts.append(f"检测到{len(object_names)}个物体：{', '.join(object_names)}")
            
            # 添加识别的文字信息
            if result['texts']:
                text_contents = [text['text'] for text in result['texts']]
                if len(text_contents) == 1:
                    voice_parts.append(f"识别到文字：{text_contents[0]}")
                else:
                    voice_parts.append(f"识别到{len(text_contents)}个文字：{', '.join(text_contents)}")
            
            # 添加AI描述
            if result['description']:
                voice_parts.append(result['description'])
            
            # 如果没有检测到任何内容
            if not voice_parts:
                voice_parts.append("当前场景较为空旷，未检测到特殊物体或文字")
            
            return "。".join(voice_parts) + "。"
            
        except Exception as e:
            self.logger.warning(f"构建语音文本失败: {e}")
            return result.get('description', '')
    
    def _build_world_update_from_result(self, result: dict) -> WorldUpdate:
        """
        v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
        
        Args:
            result: 处理结果字典（包含 objects 和 texts）
        
        Returns:
            WorldUpdate: 世界更新对象
        """
        # 从 result 字典中提取 objects 和 texts（如果存在）
        objects = result.get("objects", [])
        texts = result.get("texts", [])
        
        # 构建 WorldUpdate（即使 objects 和 texts 为空，也创建空的 WorldUpdate）
        return WorldUpdate(
            update_type="content",
            structured_data={
                "objects": objects,
                "texts": texts,
            },
            confidence=1.0 if (objects or texts) else 0.0,  # 如果没有任何数据，置信度为 0
            source="modeling_executor",
        )
    
    def _calculate_motion_state(self, objects: list, texts: list):
        """
        v1.8.3: 计算运动状态（最小占位实现）
        
        当前版本：只返回占位数据，为 v1.9/v2.0 预留接口
        
        Args:
            objects: YOLO 检测结果列表
            texts: OCR 识别结果列表
        
        Returns:
            MotionState: 运动状态对象
        """
        from core.risk_assessor import MotionState
        
        # 最小占位实现：返回默认值
        # TODO: v1.9 从连续帧变化中提取真实运动信息
        motion_state = MotionState()
        motion_state.is_moving_towards_edge = False
        motion_state.estimated_ttc = None
        motion_state.estimated_distance = None
        
        return motion_state
    
    def _start_voice_conversation(self):
        """启动语音对话功能"""
        try:
            if not self.voice_recognition or not self.voice_recognition.is_available:
                self.logger.warning("语音识别模块不可用，跳过语音对话")
                return
            
            # 语音提示用户开始说话
            # v1.8.3a: 通过语音总闸统一入口
            self._speak_safely("请开始说话", scene_hash=None)
            
            # 在新线程中启动语音识别
            import threading
            voice_thread = threading.Thread(target=self._voice_conversation_loop, daemon=True)
            voice_thread.start()
            
            self.logger.info("语音对话功能已启动")
            
        except Exception as e:
            self.logger.error(f"启动语音对话失败: {e}")
    
    def _voice_conversation_loop(self):
        """语音对话循环"""
        global audio_io_state
        
        try:
            while self.is_running:
                # 等待语音输入
                self.logger.info("等待语音输入...")
                
                # 修改 3: 录音前设置状态，禁止 TTS
                audio_io_state = "RECORDING"
                # v1.8.3: 用户开始说话，系统进入聆听态
                self.decision_scheduler.set_user_speaking(True)
                # v1.8.3a 阶段 C: 更新用户状态
                self.user_state.is_speaking = True
                try:
                    recognized_text = self.voice_recognition.listen_and_recognize(timeout=5)
                finally:
                    # 录音结束后恢复状态
                    audio_io_state = "IDLE"
                    # v1.8.3: 用户停止说话，退出聆听态
                    self.decision_scheduler.set_user_speaking(False)
                    # v1.8.3a 阶段 C: 更新用户状态
                    self.user_state.is_speaking = False
                    # v1.8.3: 检查是否有待处理的 LV1 风险，立即补播
                    if "pending_lv1" in self.risk_context_cache:
                        pending_risk = self.risk_context_cache.pop("pending_lv1")
                        self._handle_immediate_risk(pending_risk)
                
                if recognized_text and recognized_text.strip():
                    # 识别到语音
                    self.logger.info(f"识别到语音: {recognized_text}")
                    
                    # 语音回应（此时 audio_io_state 已恢复为 IDLE）
                    # v1.8.3a: 通过语音总闸统一入口
                    response = f"你刚才说的是：{recognized_text}"
                    self._speak_safely(response, scene_hash=None)  # 用户回应不需要场景去重
                    
                    # 等待语音播报完成
                    time.sleep(2)
                    
                else:
                    # 没有识别到语音
                    self.logger.warning("5秒内无声音输入")
                    # 不播报，避免干扰
                    # self._speak_safely("我没有听清，再说一遍？")
                    
                    # 短暂等待后继续
                    time.sleep(1)
                    
        except Exception as e:
            self.logger.error(f"语音对话循环出错: {e}")
        finally:
            # 确保状态恢复
            audio_io_state = "IDLE"
    
    def process_frame(self, frame: np.ndarray) -> dict:
        """
        处理单帧图像，执行完整的识别流程
        
        Args:
            frame: 输入图像帧
            
        Returns:
            处理结果字典
        """
        global last_frame_ts
        
        # 止血改造 4: 帧节流（测试期不追求实时性）
        now = time.time()
        if now - last_frame_ts < FRAME_MIN_INTERVAL:
            self.logger.debug(f"[FrameThrottle] 帧节流：距离上次处理仅 {now - last_frame_ts:.2f}s，跳过")
            return None
        last_frame_ts = now
        
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        
        try:
            # ===== v1.8.5 Phase B Step 2.4: 重构 process_frame() =====
            # 不再假设 objects / texts / description 的直接存在
            # 只能从 pipeline_controller.process_frame() 的返回结果中取数据
            # 使用 navigation_result / modeling_result 的结构化字段
            
            # 1. 通过 PipelineController 处理帧（统一入口）
            self.logger.info("开始视觉流水线处理...")
            pipeline_result = None
            navigation_result = None
            modeling_result = None
            try:
                pipeline_result = self.pipeline_controller.process_frame(
                    frame=frame,
                    frame_id=f"frame_{int(time.time() * 1000)}",
                    task_state=None,  # TODO: 后续从上下文获取
                    context=None,  # TODO: 后续从上下文获取
                    user_position=None,  # TODO: 后续从上下文获取
                )
                # 提取结构化结果
                navigation_result = pipeline_result.get("navigation_result")
                modeling_result = pipeline_result.get("modeling_result")
            except Exception as e:
                self.logger.warning(f"Pipeline 处理失败: {e}")
                # 降级处理：使用空结果
                navigation_result = None
                modeling_result = None
            
            # 2. 从结构化结果中提取数据（不再直接假设存在）
            # 2.1 从 NavigationResult 中提取 objects
            objects = []
            if navigation_result and navigation_result.objects:
                objects = navigation_result.objects
            
            # 2.2 从 ModelingResult 中提取 texts（从 content_candidates 中提取 raw_text）
            texts = []
            if modeling_result:
                for candidate in modeling_result.content_candidates:
                    if candidate.raw_text:
                        # 转换为原有格式（dict with 'text' and 'confidence'）
                        texts.append({
                            "text": candidate.raw_text,
                            "confidence": candidate.confidence,
                        })
            
            # 2.3 从 ModelingResult 中提取场景描述
            description = None
            if modeling_result:
                for candidate in modeling_result.content_candidates:
                    if candidate.content_type == "scene_description" and candidate.description:
                        description = candidate.description
                        break
            if description is None:
                description = ""  # 降级处理：使用空字符串
            
            # 4. 语音输入处理（模拟）
            audio_input = self.whisper_processor.transcribe(np.array([]))  # 模拟音频数据
            
            processing_time = time.time() - start_time
            
            # v1.8.3: 计算运动状态（用于风险评估）
            motion_state = self._calculate_motion_state(objects, texts)
            
            # 构建结果
            result = {
                'timestamp': timestamp,
                'objects': objects,
                'texts': texts,
                'description': description,
                'audio_input': audio_input,
                'processing_time': processing_time,
                'motion_state': motion_state  # 新增
            }
            
            # 5. v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
            decision = self._handle_speech_decision(result)
            self._execute_speech_decision(result, decision)
            
            # 6. 输出结果
            self._output_results(result)
            
            # 7. 记录日志
            self.json_logger.log_recognition_result(
                timestamp=timestamp,
                objects=objects,
                texts=texts,
                description=description,
                audio_input=audio_input,
                processing_time=processing_time
            )
            
            return result
            
        except Exception as e:
            error_msg = f"帧处理失败: {e}"
            self.logger.error(error_msg)
            self.json_logger.log_error(timestamp, error_msg, "processing_error")
            return None
    
    def _handle_speech_decision(self, result: dict) -> dict:
        """
        v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
        v1.8.4: 集成 Risk Advisory（态势风险告知）
        
        这是唯一允许调用 TTS 的地方，禁止任何模块绕过决策层直呼 TTS
        
        ⚠️ 禁止事项：
        - ❌ YOLO / OCR 里直接调用 TTS
        - ❌ ASR 里直接触发反馈播报
        - ❌ "检测到就说"
        
        Args:
            result: 处理结果字典
        
        Returns:
            Dict[str, Any]: 决策结果，包含 action 和 reason
                - action: "SPEAK" | "WAIT" | "YIELD" | "RISK_LV1" | "ADVISORY"
                - reason: str 决策原因
        """
        if not result:
            return {"action": "WAIT", "reason": "no_result"}
        
        # === v1.8.4: Risk Advisory 注入点（新增） ===
        # 说明：ADVISORY 是"环境态势判断"，不是语言生成
        # 因此不应被 _build_voice_text() 影响，不应依赖 result 是否有 description
        # 必须在 decide() 之前判断，优先级：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
        advisory = None
        if self.risk_advisory_service and self.user_position_provider:
            pos = self.user_position_provider.get()
            if pos:
                advisory_text = self.risk_advisory_service.tick(
                    user_xy=pos.xy,
                    ts=pos.ts
                )
                if advisory_text:
                    advisory = {
                        "action": "ADVISORY",
                        "reason": "risk_trend_up",
                        "advisory_text": advisory_text,
                    }
        
        # v1.8.3: 构建场景状态（把瞬时识别结果变成可判断的状态）
        # v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
        world_update = self._build_world_update_from_result(result)
        scene_state = self.scene_state_builder.build_state(
            world_update=world_update,
            risk_level=None  # 自动判断
        )
        
        # v1.8.3a 阶段 C: 使用决策控制器（只做三态判断，不调用 TTS）
        # v1.8.3: 从 result 中获取 motion_state（禁止凭空创建）
        motion_state = result.get('motion_state')  # 允许为 None
        decision_result = decide(
            scene_state=scene_state,
            speech_gate=self.speech_gate,
            user_state=self.user_state,
            motion_state=motion_state
        )
        
        # === v1.8.4: 优先级裁决 ===
        # RISK_LV1 > ADVISORY > 其他
        if decision_result.get("action") == "RISK_LV1":
            # RISK_LV1 最高优先级，直接返回
            return decision_result
        elif advisory:
            # ADVISORY 优先级高于普通 SPEAK/WAIT/YIELD
            return advisory
        else:
            # 其他情况返回 decide() 的结果
            return decision_result
    
    def _execute_speech_decision(self, result: dict, decision: dict):
        """
        v1.8.3a 阶段 C: 执行决策结果
        v1.8.3: 支持 RISK_LV1 动作（强制插队）
        
        主循环必须明确消费决策结果，没有 default，没有 else
        
        Args:
            result: 处理结果字典
            decision: 决策结果（包含 action 和 reason）
        """
        action = decision.get("action")
        
        # v1.8.3: Debug 输出威胁语义（只读，不驱动行为）
        threat = decision.get("threat")
        if threat:
            self.logger.debug(
                f"[Threat] level={threat.level.value} type={threat.risk_type} reason={threat.reason}"
            )
        
        # v1.8.3: LV1 风险评估（最高优先级）
        if action == "RISK_LV1":
            # LV1: 强制插队，必须发声
            self._handle_immediate_risk(decision.get("risk_result"))
            return
        
        # v1.8.4: Risk Advisory（态势风险告知）
        # 优先级：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
        # ADVISORY 不强制插队，不绕过 speech_gate，不打断用户说话
        elif action == "ADVISORY":
            advisory_text = decision.get("advisory_text")
            if not advisory_text:
                return
            
            # === v1.8.4: Shadow Mode 支持 ===
            # Shadow Mode = 只打日志，不播报
            # 正确顺序：模型输出 → RiskAdvisoryService → RiskDebugSnapshot（日志） → 人工/离线验证 → 确认稳定后开启播报
            if RISK_SHADOW_MODE:
                # Shadow Mode：只记录日志，不触发播报
                self.logger.info(
                    f"[RiskShadowMode] ADVISORY 被拦截（Shadow Mode 开启）: {advisory_text}"
                )
                return
            
            # 构建场景状态（用于 scene_hash）
            # v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
            world_update = self._build_world_update_from_result(result)
            scene_state = self.scene_state_builder.build_state(
                world_update=world_update,
                risk_level=decision.get("risk_level")
            )
            
            # 走统一安全播报（尊重 speech_gate / 用户状态）
            self._speak_safely(
                advisory_text,
                scene_hash=scene_state.scene_hash
            )
            return
        
        if action == "SPEAK":
            # 可以且应该说 → 调用 TTS
            # v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
            world_update = self._build_world_update_from_result(result)
            scene_state = self.scene_state_builder.build_state(
                world_update=world_update,
                risk_level=None
            )
            voice_text = self._build_voice_text(result)
            if voice_text:
                self._speak_safely(voice_text, scene_hash=scene_state.scene_hash)
            
            # 兼容原有的描述播报（如果配置启用且与 voice_text 不同）
            if OUTPUT_CONFIG['play_audio'] and result.get('description'):
                description = result['description']
                if description != voice_text:
                    # 对描述单独决策
                    desc_decision = self._handle_speech_decision({"description": description, "objects": result.get("objects", []), "texts": result.get("texts", [])})
                    if desc_decision["action"] == "SPEAK":
                        self._speak_safely(description, scene_hash=scene_state.scene_hash)
        
        elif action == "WAIT":
            # 不能说，但系统继续运行 → 不播报（明确：系统在运行，只是不说话）
            self.logger.debug(f"Decision=WAIT reason={decision['reason']}")
            pass
        
        elif decision["action"] == "YIELD":
            # 用户优先 → 主动让位（明确：用户优先，系统让位）
            self.logger.debug(f"Decision=YIELD reason={decision['reason']}")
            pass
        
        # 硬规则：不要 else，不要兜底说一句，WAIT/YIELD 都不播报
    
    def _should_dump_risk_debug(self) -> bool:
        """
        v1.8.4: Risk 调试快照频率控制
        
        每 0.5 秒最多输出一次，避免刷屏
        
        Returns:
            bool: 是否应该输出调试快照
        """
        now = time.time()
        last = self._last_risk_debug_ts
        if now - last >= 0.5:  # 每 0.5 秒最多一次
            self._last_risk_debug_ts = now
            return True
        return False
    
    def _output_results(self, result: dict):
        """
        输出处理结果
        
        Args:
            result: 处理结果字典
        """
        if not result:
            return
        
        # === v1.8.4: Risk Debug Snapshot 日志输出（debug only） ===
        # 说明：只读快照，不反向影响 risk / decision / speech
        # 频率控制：每 0.5 秒最多输出一次，避免刷屏
        if DEBUG_CONFIG.get("enable_risk_debug", False):
            snap = self.risk_advisory_service.get_last_debug_snapshot()
            if snap and self._should_dump_risk_debug():
                self.logger.debug(
                    "[RiskDebugSnapshot] %s",
                    snap.to_dict()
                )
        
        # === 方案二：CLI 运行态面板（P0.5，暂不实现） ===
        # if DEBUG_CONFIG.get("enable_risk_console", False):
        #     from core.risk.risk_debug_console import render_risk_snapshot
        #     snap = self.risk_advisory_service.get_last_debug_snapshot()
        #     if snap:
        #         render_risk_snapshot(snap)
        
        # === 方案三：运行态 Overlay（P1，v1.8.5+，暂不实现） ===
        # if DEBUG_CONFIG.get("enable_risk_overlay", False):
        #     from core.risk.risk_debug_overlay import render_risk_overlay
        #     snap = self.risk_advisory_service.get_last_debug_snapshot()
        #     if snap:
        #         render_risk_overlay(frame, snap)
        
        # 打印识别结果
        if OUTPUT_CONFIG['print_results']:
            print("\n" + "="*50)
            print(f"时间: {result['timestamp']}")
            print(f"处理时间: {result['processing_time']:.2f}秒")
            
            # 打印检测到的物体
            if result['objects']:
                print("\n检测到的物体:")
                for obj in result['objects']:
                    print(f"  - {obj['label']}: {obj['confidence']:.2f}")
            else:
                print("\n未检测到物体")
            
            # 打印识别的文字
            if result['texts']:
                print("\n识别的文字:")
                for text in result['texts']:
                    print(f"  - {text['text']}: {text['confidence']:.2f}")
            else:
                print("\n未识别到文字")
            
            # 打印AI描述
            print(f"\nAI场景描述: {result['description']}")
            
            if result['audio_input']:
                print(f"语音输入: {result['audio_input']}")
            
            print("="*50)
        
        # v1.8.2: 所有 TTS 调用已统一在 _handle_speech_decision() 中处理
        # 这里不再直接调用 TTS，避免绕过 PolicyEngine
    
    def run(self, show_camera: bool = True):
        """
        运行主循环
        
        Args:
            show_camera: 是否显示摄像头画面
        """
        # v1.8.5 Phase B Step 1.1: 通过 PipelineController 检查摄像头状态
        if not self.pipeline_controller.is_opened():
            self.logger.error("摄像头未打开，无法运行")
            return
        
        self.is_running = True
        self.logger.info("开始运行Luna徽章系统...")
        
        # 启动语音对话
        self._start_voice_conversation()
        
        try:
            while self.is_running:
                # v1.8.5 Phase B Step 1.1: 通过 PipelineController 读取摄像头帧
                frame = self.pipeline_controller.read_frame()
                if frame is None:
                    self.logger.warning("无法读取摄像头帧，跳过")
                    continue
                
                # 显示摄像头画面
                if show_camera and OUTPUT_CONFIG['show_camera_feed']:
                    cv2.imshow('Luna Badge MVP - 摄像头画面', frame)
                    
                    # 检查按键
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        self.logger.info("用户按下'q'键，退出程序")
                        break
                    elif key == ord('s'):
                        self.logger.info("用户按下's'键，立即处理当前帧")
                        self.process_frame(frame)
                        continue
                
                # 按间隔处理帧
                current_time = time.time()
                if current_time - self.last_process_time >= PROCESSING_CONFIG['process_interval']:
                    self.logger.info("开始处理当前帧...")
                    self.process_frame(frame)
                    self.last_process_time = current_time
                
        except KeyboardInterrupt:
            self.logger.info("用户中断程序")
        except Exception as e:
            self.logger.error(f"运行过程中发生错误: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("开始清理资源...")
        self.is_running = False
        
        # 停止音频工作线程（第二层修复）
        try:
            stop_audio_worker()
            self.logger.info("音频工作线程已停止")
        except Exception as e:
            self.logger.warning(f"停止音频工作线程失败: {e}")
        
        # 停止音频工作线程（第二层修复）
        try:
            stop_audio_worker()
            self.logger.info("音频工作线程已停止")
        except Exception as e:
            self.logger.warning(f"停止音频工作线程失败: {e}")
        
        # 停止语音播报
        if self.voice:
            try:
                self.voice.stop()
            except Exception as e:
                self.logger.warning(f"停止语音播报失败: {e}")
        
        # 停止语音识别
        if self.voice_recognition:
            try:
                # 语音识别模块会自动停止
                self.logger.info("语音识别模块已停止")
            except Exception as e:
                self.logger.warning(f"停止语音识别失败: {e}")
        
        # v1.8.5 Phase B Step 1.1: 通过 PipelineController 释放摄像头资源
        if self.pipeline_controller:
            self.pipeline_controller.release()
        
        cv2.destroyAllWindows()
        self.logger.info("资源清理完成")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Luna 实体徽章 MVP')
    parser.add_argument('--no-camera', action='store_true', help='不显示摄像头画面')
    parser.add_argument('--interval', type=float, default=PROCESSING_CONFIG['process_interval'], 
                       help='处理间隔（秒）')
    parser.add_argument('--camera-index', type=int, default=CAMERA_CONFIG['camera_index'],
                       help='摄像头索引')
    
    args = parser.parse_args()
    
    # 更新配置
    PROCESSING_CONFIG['process_interval'] = args.interval
    CAMERA_CONFIG['camera_index'] = args.camera_index
    
    print("Luna 实体徽章 MVP 启动中...")
    print("="*50)
    print("功能说明:")
    print("- 摄像头识别：检测人、车、障碍物、标志牌")
    print("- 文字识别：识别画面中的文字内容")
    print("- 场景描述：AI生成自然语言描述")
    print("- 语音播报：TTS语音输出")
    print("- 日志记录：JSON格式记录所有结果")
    print("="*50)
    print("操作说明:")
    print("- 按 'q' 键退出程序")
    print("- 按 's' 键立即处理当前帧")
    print("="*50)
    
    # 创建并运行Luna徽章系统
    luna_badge = LunaBadgeMVP()
    luna_badge.run(show_camera=not args.no_camera)


if __name__ == "__main__":
    main()
