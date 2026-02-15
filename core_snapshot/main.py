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
from dataclasses import asdict
from types import SimpleNamespace
from typing import Optional, Dict, Any

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
from config import MODEL_PATHS, CAMERA_CONFIG, PROCESSING_CONFIG, OUTPUT_CONFIG, DEBUG_CONFIG, RISK_SHADOW_MODE, A3_SHADOW_MODE
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
from a3.config import A3Config
from runtime.a3_runtime import A3Runtime
from runtime.clock import CLOCK
from runtime.context import RuntimeContext
from runtime.observation_loop import ObservationLoop
from runtime.observation_builders import (
    build_observation_frame,
    build_empty_observation_frame,
)
from runtime.a3_logger import (
    log_a3,
    log_a3_timeseries,
    log_advice_rhythm_event,
    log_arbitration_event,
    log_multimodal_conflict,
    log_shadow_decision,
    log_engaged_signal,
    build_arbitration_payload,
    write_arbitration_payload,
)
from pal.v0 import compute_pal_horizon_difficulty
from c3 import C3Config, C3Store, C3Learner
from c3.maintenance import c3_maintenance
from c3.gates import bucket_complexity
from c3.advice_map import ADVICE_TO_TENDENCY, ADVICE_TO_CATEGORY, FORBIDDEN_ADVICE_IDS
from advice.engine import AdviceEngine
from advice.schema import AdviceTask
from intervention.advice_rhythm_v0 import get_advice_rhythm_v0
from intervention.arbitrator_v0 import (
    get_arbitrator_v0,
    build_candidate_tasks,
)
from intervention.intent_k_v0 import get_intent_k_v0
from intervention.slot_l_v0 import get_slot_l_v0
from intervention.eligibility import infer_task_state
from intervention.task_state_override import TaskStateOverride
from intervention.multimodal_conflict_v0 import (
    resolve_multimodal_conflict,
    decisions_to_candidates,
    SOURCE_TASK,
    SOURCE_VISION,
)
from intervention.engaged_failure import compute_engaged_signal
from intervention.outcome_n_v0 import compute_outcome_v0
from intervention.outcome_q_v0 import OutcomeQRecorderV0
from intervention.observation_r_v0 import ObservationRCollectorV0
from intervention.stress_s_v0 import StressObserverSV0
from execution.p_executor_v0 import PExecutorV0, PExecutionResult
from intervention.p_executor_v1 import P1Executor, P1Outcome
from intervention.p_policy_v1 import P1Config
from intervention.p2_executor_v0 import P2Executor
from intervention.p3_executor_v0 import P3Executor
from intervention.p4_planner_v0 import P4Config, plan_speech_p4_v0
from intervention.p5_expression_plan_v0 import build_expression_plan_v0
from external.ocr_provider import OCRProvider
from external.map_provider import MapProvider
from external.speech_provider import SpeechProvider


class _TTSAdapterForP:
    """P v0：将 submit_tts(voice) 封装为 .say(text) 供 PExecutorV0 调用。"""
    def __init__(self, voice, submit_fn):
        self._voice = voice
        self._submit = submit_fn

    def say(self, text: str) -> None:
        if self._voice and getattr(self._voice, "is_available", True):
            self._submit(text, self._voice)


class LunaBadgeMVP:
    """Luna 实体徽章 MVP 主类"""
    
    def __init__(self, video_path: str = None, force_engaged_test: bool = False, force_engaged_test_l2: bool = False):
        """初始化Luna徽章系统。video_path 不为空时从视频文件读取帧，否则使用摄像头。
        force_engaged_test：N 层验收，强制 ENGAGED、走 SPEAK 分支写 trace，默认不执行 SAY。
        force_engaged_test_l2：仅测试用，强制 L2 并允许真实执行 SAY，验证 P1–P5→Q/R/S 闭环。"""
        self.force_engaged_test = force_engaged_test
        self.force_engaged_test_l2 = force_engaged_test_l2
        # 设置日志
        self.logger = setup_logger('luna_badge')
        self.json_logger = JSONLogger()
        # 确保 CameraHandler 的日志能输出到控制台（便于确认 --video 时是否在用视频帧）
        setup_logger('utils.camera_handler')
        
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

        # === A3 Runtime (read-only, minimal intrusion) ===
        # Default enabled to ensure env_mode is written to logs/trace.
        a3_enabled = os.environ.get("A3_ENABLED", "true").lower() in ("1", "true", "yes")
        a3_log_enabled = os.environ.get("A3_LOG", "true").lower() in ("1", "true", "yes")
        self.runtime_ctx = RuntimeContext()
        self.a3_runtime = A3Runtime(
            A3Config(enabled=a3_enabled),
            SimpleNamespace(
                risk=self.risk_advisory_service,
                nav=self.decision_scheduler,
                vision=self.pipeline_controller if hasattr(self, "pipeline_controller") else None,
                advice=self.speech_gate,
                task=self.decision_scheduler,
            ),
        )
        self.a3_log_enabled = a3_log_enabled
        # 补丁 v1：单一采样节拍入口
        self.obs_loop = ObservationLoop()

        # C3.x v0 (只学习，不控制，默认关闭)
        c3_enabled = os.environ.get("C3_ENABLED", "false").lower() in ("1", "true", "yes")
        self.c3_cfg = C3Config(enabled=c3_enabled)
        self.c3_store = C3Store()
        self.c3_learner = C3Learner(self.c3_cfg, self.c3_store)
        self._last_c3_maintenance_ts = 0.0
        self._last_advice_event = None
        self._last_engagement_level = "L0"  # G) ENGAGED 退出时清空仲裁
        self._last_s_stress_level = None  # P1：上一条 S 的 stress_level（供 payload.s）
        self._last_negative_speech = {"text": None, "ts": 0.0}
        self._negative_feedback_hits = {}

        # AdviceEngine: 唯一 advice_id 语义源
        self.advice_engine = AdviceEngine()
        
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

        # P 层：P1 执行器（payload = m/engagement/rhythm/s/text，outcome 写回 trace）
        _tts_adapter = _TTSAdapterForP(self.voice, submit_tts) if self.voice else None
        self._p1_executor = (
            P1Executor(
                cfg=P1Config(
                    engaged_stable_s=3.0,
                    say_cooldown_s=15.0,
                    block_when_s_saturated=True,
                ),
                speak_fn=_tts_adapter.say if _tts_adapter else None,
            )
            if _tts_adapter else None
        )
        # P2 v0：内容质量门禁（仅在 P1.apply_now 时生效），不增加说话次数
        self._p2_executor = P2Executor() if self._p1_executor is not None else None
        # P3 v0：节律闸门（P2 通过后、SAY 前最后一道）
        self._p3_executor = P3Executor() if self._p2_executor is not None else None
        # P4 v0：表达结构控制（P1/P2/P3 通过后、SAY 前，只定 prefix/suffix/style）
        self._p4_cfg = P4Config() if self._p3_executor is not None else None
        # Q v0：执行回执记录器，P 尝试后写 q 到 trace（只做事实记录）
        self._q_recorder = OutcomeQRecorderV0()
        # R v0：执行后观测聚合器，只读统计/解释，不反向影响行为
        self._r_collector = ObservationRCollectorV0(rolling_window_sec=300)
        # S v0：系统打扰压力观测器，基于 R 统计判断执行压强（shadow-only）
        self._s_observer = StressObserverSV0()
        
        # v1.8.5 Phase B Step 1.1: CameraHandler 迁移到 PipelineController
        # 初始化视觉流水线控制器（包含 CameraHandler；支持 video_path 从视频文件读取）
        self.logger.info("正在初始化视觉流水线...")
        self.pipeline_controller = PipelineController(video_path=video_path)
        # A3: update vision manager once ready
        try:
            self.a3_runtime.provider.vision = self.pipeline_controller
        except Exception:
            pass
        
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

        # Phase 2.2: 外部感知经 Provider，main 不持缓存，只写 ObservationFrame
        self.ocr_provider = OCRProvider(interval_sec=1.0)
        self.map_provider = MapProvider(interval_sec=1.0)
        self.speech_provider = SpeechProvider()

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
    
    def _speak_safely(self, text: str, scene_hash: Optional[str] = None, shadow_context: Optional[Dict[str, Any]] = None):
        """
        安全的语音播报方法（v1.8.3a: 通过语音总闸统一入口）
        L) A3 Shadow Mode：算=全部照算，说=永远不说

        Args:
            text: 要播报的文本
            scene_hash: 场景哈希值（用于去重）
            shadow_context: L) 影子模式用 {task_id, level, type}，用于 trace
        """
        global audio_io_state

        # L) A3 影子运行模式：不执行，只记录
        if A3_SHADOW_MODE:
            log_shadow_decision(
                shadow_decision={
                    "would_speak": True,
                    "task_id": (shadow_context or {}).get("task_id"),
                    "level": (shadow_context or {}).get("level"),
                    "type": (shadow_context or {}).get("type"),
                    "text_preview": (text or "")[:50],
                },
                shadow_reason="SHADOW_MODE_ENABLED",
            )
            return

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
            # B) ENGAGED 介入强度 v0：只读调制 speak_cooldown
            engagement = getattr(self.runtime_ctx, "engagement", None)
            cooldown = None
            if engagement and engagement.get("level") not in ("L0", ""):
                cd = engagement.get("speak_cooldown_s")
                if cd is not None:
                    cooldown = float(cd)
            self.speech_gate.release(scene_hash=scene_hash, cooldown=cooldown)
    
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

    def _serialize_env_mode(self) -> Optional[Dict[str, Any]]:
        """
        A3 env_mode -> JSON-serializable dict for logs/trace.
        """
        try:
            mode = getattr(self.runtime_ctx, "env_mode", None)
            if mode is None:
                return None
            payload = asdict(mode)
            # Ensure enums are serialized as values
            if "safety_level" in payload and hasattr(mode.safety_level, "value"):
                payload["safety_level"] = mode.safety_level.value
            if "control_mode" in payload and hasattr(mode.control_mode, "value"):
                payload["control_mode"] = mode.control_mode.value
            return payload
        except Exception:
            return None
    
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

    def _build_real_obs(self, now: float, dt: float, seq: int):
        """补丁 v1：仅在采样时刻被 ObservationLoop 调用，从 A3 拉取 mode/signals 填 ObservationFrame。"""
        try:
            self.a3_runtime.tick(self.runtime_ctx, now_ms=int(now * 1000))
        except Exception:
            return build_empty_observation_frame(now, dt, seq)
        mode = self.a3_runtime.last_mode
        sig = self.a3_runtime.last_signals
        if mode is None or sig is None:
            return build_empty_observation_frame(now, dt, seq)
        motion = float(mode.debug.get("motion_instability", 0.0)) if mode.debug else 0.0
        path = float(mode.debug.get("path_instability", 0.0)) if mode.debug else 0.0
        branch = float(mode.debug.get("branch_load", 0.0)) if mode.debug else 0.0
        roi_load = float(mode.debug.get("roi_load", 0.0)) if mode.debug else 0.0
        roi = int(getattr(sig, "roi_count", 0))
        vc = float(getattr(sig, "view_confidence", 1.0))
        pal = compute_pal_horizon_difficulty(motion, path, branch, roi_load, vc)
        complexity = float(getattr(mode, "complexity_score", 0.5))
        frame_quality = str(getattr(sig, "frame_quality", "GOOD"))
        control_mode = getattr(mode, "control_mode", None)
        control_mode_str = control_mode.value if control_mode and hasattr(control_mode, "value") else (str(control_mode) if control_mode else "NONE")
        ocr_text, ocr_produced_ts = self.ocr_provider.poll(now)
        map_hint, map_produced_ts = self.map_provider.poll(now)
        speech_event, speech_produced_ts = self.speech_provider.poll(now)
        return build_observation_frame(
            ts=now,
            dt=dt,
            seq=seq,
            sampled=True,
            motion=motion,
            path=path,
            branch=branch,
            roi=roi,
            pal=pal,
            complexity=complexity,
            vc=vc,
            frame_quality=frame_quality,
            control_mode=control_mode_str,
            ocr_text=ocr_text,
            ocr_produced_ts=ocr_produced_ts,
            map_hint=map_hint,
            map_produced_ts=map_produced_ts,
            speech_event=speech_event,
            speech_produced_ts=speech_produced_ts,
        )
    
    def process_frame(self, frame: np.ndarray, context: Optional[Dict[str, Any]] = None) -> dict:
        """
        处理单帧图像，执行完整的识别流程
        
        Args:
            frame: 输入图像帧
            
        Returns:
            处理结果字典
        """
        global last_frame_ts
        
        # 补丁 v1：视频回放时用 current_ts（frame_ts）保证采样确定性；否则用 CLOCK
        now = getattr(self, "current_ts", None)
        if now is None:
            now = CLOCK.now()
            if now - last_frame_ts < FRAME_MIN_INTERVAL:
                self.logger.debug(f"[FrameThrottle] 帧节流：距离上次处理仅 {now - last_frame_ts:.2f}s，跳过")
                return None
        last_frame_ts = now

        start_time = time.time()
        timestamp = datetime.now().isoformat()

        self._maybe_run_c3_maintenance()

        try:
            # ===== v1.8.5 Phase B Step 2.4: 重构 process_frame() =====
            # 1. 先跑 Pipeline，再按「有效 tick」决定是否推进 A3/rhythm/engagement（避免空转循环污染时间累计）
            pipeline_result = None
            navigation_result = None
            modeling_result = None
            try:
                pipeline_result = self.pipeline_controller.process_frame(
                    frame=frame,
                    frame_id=f"frame_{int(time.time() * 1000)}",
                    task_state=None,  # TODO: 后续从上下文获取
                    context=context,  # 传递感知上下文（frame_valid / occlusion_state 等）
                    user_position=None,  # TODO: 后续从上下文获取
                )
                # 提取结构化结果
                navigation_result = pipeline_result.get("navigation_result")
                modeling_result = pipeline_result.get("modeling_result")
            except Exception as e:
                self.logger.warning(f"Pipeline 处理失败: {e}")
                navigation_result = None
                modeling_result = None
                pipeline_result = {}

            # Phase 2.2: 只向 Provider 喂数据，不持缓存；取值在 _build_real_obs 中 poll(now)
            self.ocr_provider.feed_pipeline_result(pipeline_result, now)
            self.map_provider.feed_context(context if context is not None else {}, now)

            # 补丁 v1：单一采样节拍，决策入口仅 on_observation(obs)；视频模式传入 now 保证确定性
            obs = self.obs_loop.step(self._build_real_obs, now=now)
            if obs.sampled:
                self.logger.info("开始视觉流水线处理... seq=%s ts=%.3f", obs.seq, obs.ts)
            else:
                self.logger.debug("pipeline frame (non-sampled)")
            try:
                decision = self.a3_runtime.on_observation(self.runtime_ctx, obs)
                if self.a3_log_enabled:
                    log_a3(obs, decision)
            except Exception as e:
                self.logger.debug(f"[A3] on_observation skipped: {e}")
            
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
            
            # 4. 语音输入处理（使用单一事实源）
            if self.voice_recognition:
                audio_input = self.voice_recognition.latest_transcript
            else:
                audio_input = ""
            
            processing_time = time.time() - start_time
            
            # v1.8.3: 计算运动状态（用于风险评估）
            motion_state = self._calculate_motion_state(objects, texts)
            
            system_facts = None
            if context:
                occlusion_state = context.get("occlusion_state")
                if hasattr(occlusion_state, "value"):
                    occlusion_state = occlusion_state.value
                system_facts = {
                    "frame_valid": context.get("frame_valid"),
                    "perception_state": context.get("perception_state"),
                    "occlusion_state": occlusion_state,
                    "avg_luminance": context.get("avg_luminance"),
                }

            # 构建结果
            result = {
                'timestamp': timestamp,
                'objects': objects,
                'texts': texts,
                'description': description,
                'audio_input': audio_input,
                'speech_input': audio_input,
                'system_facts': system_facts,
                'processing_time': processing_time,
                'motion_state': motion_state  # 新增
            }
            
            # 5. v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
            # N 层验收开关：强制 ENGAGED 且本 tick 不执行动作（仅测试用，不进入正式逻辑）
            if getattr(self, "force_engaged_test", False) or getattr(self, "force_engaged_test_l2", False):
                self.runtime_ctx.rhythm_state = "ENGAGED"
                self.runtime_ctx.engagement = {"level": "L2", "advice_scale": 0.7, "pal_lookahead_m": 8.0, "speak_cooldown_s": 8.0}
                if getattr(self, "force_engaged_test_l2", False):
                    self.runtime_ctx.engagement["reason"] = "FORCE_ENGAGED_TEST_L2"
                self.runtime_ctx.eligibility = {"allowed": True, "reason": "force_engaged_test" if getattr(self, "force_engaged_test", False) else "force_engaged_test_l2"}
            decision = self._handle_speech_decision(result)
            # 强制 ENGAGED 测试：必须走 SPEAK 分支才能跑仲裁与 P 层并写 trace；若本为 WAIT 则强制为 SPEAK
            if (getattr(self, "force_engaged_test", False) or getattr(self, "force_engaged_test_l2", False)) and decision.get("action") != "SPEAK":
                decision = {"action": "SPEAK", "reason": "force_engaged_test_l2" if getattr(self, "force_engaged_test_l2", False) else "force_engaged_test"}
            failure = self._execute_speech_decision(result, decision)
            if failure and failure.get("engaged_signal"):
                log_engaged_signal(
                    failure["engaged_signal"],
                    outcome_payload=failure.get("outcome"),
                    q_payload=failure.get("q"),
                    r_payload=failure.get("r"),
                    s_payload=failure.get("s"),
                )

            self._maybe_learn_negative_advice_from_speech(result)
            
            # 6. 输出结果
            self._output_results(result)
            
            # 7. 记录日志
            self.json_logger.log_recognition_result(
                timestamp=timestamp,
                objects=objects,
                texts=texts,
                description=description,
                audio_input=audio_input,
                speech_input=audio_input,
                system_facts=system_facts,
                processing_time=processing_time,
                env_mode=self._serialize_env_mode(),
                advice_id=result.get("advice_id"),
                advice_ids=result.get("advice_ids"),
                advice_category=result.get("advice_category"),
                advice_is_safety=result.get("advice_is_safety"),
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
    
    def _execute_speech_decision(self, result: dict, decision: dict) -> Optional[Dict[str, Any]]:
        """
        v1.8.3a 阶段 C: 执行决策结果
        v1.8.3: 支持 RISK_LV1 动作（强制插队）
        J) ENGAGED 且未执行时返回 engaged_signal payload，供 process_frame 写 trace；解释统一交给 N 层。

        Returns:
            None 或 {"engaged_signal": {...}}（仅当 ENGAGED 且本 tick 未说时）
        """
        self._did_speak_this_tick = False
        self._last_arbitration_winner = False
        self._last_p_outcome = None
        self._p_executed_this_tick = False
        now = time.time()
        self._last_cooldown_active = (
            now < getattr(self.speech_gate, "cooldown_until", 0)
            if self.speech_gate else False
        )
        action = decision.get("action")

        # 运行态：读取 ENGAGED 介入强度（由 A3 timeseries 写入 runtime_ctx.engagement）
        engagement = getattr(self.runtime_ctx, "engagement", None)
        eng_level = engagement.get("level", "L0") if engagement else "L0"
        env_mode = getattr(self.runtime_ctx, "env_mode", None)
        control_mode = getattr(env_mode, "control_mode", None)
        control_mode_str = getattr(control_mode, "value", str(control_mode)) if control_mode else "ASSISTED"
        complexity = getattr(env_mode, "complexity_score", 0.5) if env_mode else 0.5
        pal = complexity
        
        # v1.8.3: Debug 输出威胁语义（只读，不驱动行为）
        threat = decision.get("threat")
        if threat:
            self.logger.debug(
                f"[Threat] level={threat.level.value} type={threat.risk_type} reason={threat.reason}"
            )
        
        # v1.8.3: LV1 风险评估（最高优先级）
        if action == "RISK_LV1":
            self._did_speak_this_tick = True  # shadow 或真实都算「说了」
            if A3_SHADOW_MODE:
                log_shadow_decision(
                    shadow_decision={"would_speak": True, "task_id": "risk_lv1", "level": "LV1", "type": "SAFETY"},
                    shadow_reason="SHADOW_MODE_ENABLED",
                )
                return None
            self._handle_immediate_risk(decision.get("risk_result"))
            return None
        
        # v1.8.4: Risk Advisory（态势风险告知）
        # 优先级：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
        # ADVISORY 不强制插队，不绕过 speech_gate，不打断用户说话
        elif action == "ADVISORY":
            advisory_text = decision.get("advisory_text")
            if not advisory_text:
                return None
            
            # === v1.8.4: Shadow Mode 支持 ===
            # Shadow Mode = 只打日志，不播报
            # 正确顺序：模型输出 → RiskAdvisoryService → RiskDebugSnapshot（日志） → 人工/离线验证 → 确认稳定后开启播报
            if RISK_SHADOW_MODE:
                # Shadow Mode：只记录日志，不触发播报
                self.logger.info(
                    f"[RiskShadowMode] ADVISORY 被拦截（Shadow Mode 开启）: {advisory_text}"
                )
                return None
            
            # 构建场景状态（用于 scene_hash）
            # v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
            world_update = self._build_world_update_from_result(result)
            scene_state = self.scene_state_builder.build_state(
                world_update=world_update,
                risk_level=decision.get("risk_level")
            )
            
            # 走统一安全播报（尊重 speech_gate / 用户状态）
            self._did_speak_this_tick = True
            self._speak_safely(
                advisory_text,
                scene_hash=scene_state.scene_hash,
                shadow_context={"task_id": "advisory", "level": "ADVISORY", "type": "SAFETY"},
            )
            # C3 模板一：Advice 被采纳（ADVISORY 属于安全建议，默认不学习）
            self._maybe_learn_advice(env_mode=self.runtime_ctx.env_mode, advice_id=None, is_safety=True)
            return None

        # G/K/L：ENGAGED 时始终写 arbitration（即使本 tick 最终不说），便于体检与验收
        # - action != SPEAK 时没有候选 → winner=None，但仍记录 k/l
        if action != "SPEAK" and eng_level in ("L1", "L2", "L3"):
            arbitrator = get_arbitrator_v0()
            candidates = build_candidate_tasks([], now, eng_level, pal, complexity, arbitrator)
            winner, deferred, scores, fairness = arbitrator.pick(candidates, now, control_mode_str)
            self._last_arbitration_winner = winner is not None
            winner_type = winner.task_type if winner else None
            intent = get_intent_k_v0().decide(winner_type)
            signals = self.a3_runtime.last_signals
            if signals is not None:
                has_goal = getattr(signals, "has_goal", False)
                explore_mode = getattr(signals, "explore_mode", False)
                task_state = TaskStateOverride.get() or infer_task_state(has_goal, explore_mode)
                a3_signals = {
                    "path_instability": getattr(signals, "path_instability", None),
                    "path_stability": getattr(signals, "path_stability", 1.0),
                    "branch_load": getattr(signals, "branch_load", None),
                    "roi_count": getattr(signals, "roi_count", 0),
                    "motion_instability": getattr(signals, "motion_instability", 0.0),
                    "task_state": task_state.value if task_state else None,
                }
                l_result = get_slot_l_v0().decide(intent.value, a3_signals)
            else:
                l_result = {"slot_type": "NONE", "slot": None}
            m_ctx = {
                "level": eng_level,
                "pal": pal,
                "complexity": complexity,
                "vc": getattr(self.runtime_ctx, "view_confidence", 1.0),
                "eligible": self.runtime_ctx.eligibility["allowed"] if self.runtime_ctx.eligibility else False,
                "eligible_reason": self.runtime_ctx.eligibility.get("reason") if self.runtime_ctx.eligibility else None,
                "rhythm_state": getattr(self.runtime_ctx, "rhythm_state", "IDLE"),
                "control_mode": control_mode_str,
                "frame_quality": getattr(self.runtime_ctx, "frame_quality", "GOOD"),
                "cooldown_active": getattr(self, "_last_cooldown_active", False),
            }
            log_arbitration_event(
                {
                    "winner": winner.task_id if winner else None,
                    "winner_type": winner_type,
                    "deferred": [t.task_id for t in deferred],
                    "deferred_types": [t.task_type for t in deferred],
                    "scores": scores,
                    "fairness": fairness,
                },
                k={"intent": intent.value},
                l=l_result,
                context=m_ctx,
            )
        
        if action == "SPEAK":
            # 可以且应该说 → 调用 TTS
            # v1.8.5 Phase B Step 3.2: 从 result 字典构建 WorldUpdate
            world_update = self._build_world_update_from_result(result)
            scene_state = self.scene_state_builder.build_state(
                world_update=world_update,
                risk_level=None
            )
            voice_text = self._build_voice_text(result)

            # AdviceEngine → Decision（唯一 advice_id 注入点）
            task_decisions = self.advice_engine.generate_decisions(
                tasks=self._get_advice_tasks(env_mode=self.runtime_ctx.env_mode),
                now=time.time(),
                context={"env_mode": self.runtime_ctx.env_mode},
            )
            vision_decisions = []
            if voice_text:
                vision_decisions = [{
                    "type": "SPEAK",
                    "text": voice_text,
                    "advice_id": None,
                    "advice_category": "ENV_AWARENESS",
                    "is_safety": False,
                }]

            # K) 多模态输入冲突仲裁 v0：统一候选，按来源优先级选择
            now = time.time()
            # eng_level / control_mode_str / pal / complexity 已在函数开头读取

            candidates_by_source = {}
            if task_decisions:
                candidates_by_source[SOURCE_TASK] = decisions_to_candidates(
                    task_decisions, SOURCE_TASK, eng_level, pal, complexity
                )
            if vision_decisions and not task_decisions:
                candidates_by_source[SOURCE_VISION] = decisions_to_candidates(
                    vision_decisions, SOURCE_VISION, eng_level, pal, complexity
                )
            selected_cands, conflict_trace = resolve_multimodal_conflict(candidates_by_source)
            log_multimodal_conflict(conflict_trace)
            advice_decisions = [c.decision for c in selected_cands] if selected_cands else (vision_decisions if not task_decisions else task_decisions)

            spoken_advice_ids = []
            spoken_advice_categories = []
            spoken_advice_is_safety = []

            # G) ENGAGED 退出时清空仲裁状态
            if self._last_engagement_level in ("L1", "L2", "L3") and eng_level == "L0":
                get_arbitrator_v0().clear_state()
            self._last_engagement_level = eng_level

            # G) 多任务介入仲裁 v0：仅 ENGAGED 时触发；非 ENGAGED 时处理全部
            decisions_to_process = advice_decisions
            if eng_level in ("L1", "L2", "L3"):
                # ENGAGED 时始终跑仲裁 + K/L 并写 trace（无 candidates 时 winner=None，便于 K/L 验收）
                arbitrator = get_arbitrator_v0()
                candidates = build_candidate_tasks(
                    advice_decisions, now, eng_level, pal, complexity, arbitrator
                )
                winner, deferred, scores, fairness = arbitrator.pick(candidates, now, control_mode_str)
                self._last_arbitration_winner = winner is not None
                self._last_cooldown_active = now < getattr(self.speech_gate, "cooldown_until", 0)
                winner_type = winner.task_type if winner else None
                # K) 介入意图层 v0：G.winner -> K.intent，仅记录，不驱动
                intent = get_intent_k_v0().decide(winner_type)
                # L) 介入内容规划层 v0：K.intent + a3_signals -> slot_type + slot，仅记录
                signals = self.a3_runtime.last_signals
                if signals is not None:
                    has_goal = getattr(signals, "has_goal", False)
                    explore_mode = getattr(signals, "explore_mode", False)
                    task_state = TaskStateOverride.get() or infer_task_state(has_goal, explore_mode)
                    a3_signals = {
                        "path_instability": getattr(signals, "path_instability", None),
                        "path_stability": getattr(signals, "path_stability", 1.0),
                        "branch_load": getattr(signals, "branch_load", None),
                        "roi_count": getattr(signals, "roi_count", 0),
                        "motion_instability": getattr(signals, "motion_instability", 0.0),
                        "task_state": task_state.value if task_state else None,
                    }
                    l_result = get_slot_l_v0().decide(intent.value, a3_signals)
                else:
                    l_result = {"slot_type": "NONE", "slot": None}
                m_ctx = {
                    "level": eng_level,
                    "pal": pal,
                    "complexity": complexity,
                    "vc": getattr(self.runtime_ctx, "view_confidence", 1.0),
                    "eligible": self.runtime_ctx.eligibility["allowed"] if self.runtime_ctx.eligibility else False,
                    "eligible_reason": self.runtime_ctx.eligibility.get("reason") if self.runtime_ctx.eligibility else None,
                    "rhythm_state": getattr(self.runtime_ctx, "rhythm_state", "IDLE"),
                    "control_mode": control_mode_str,
                    "frame_quality": getattr(self.runtime_ctx, "frame_quality", "GOOD"),
                    "cooldown_active": getattr(self, "_last_cooldown_active", False),
                }
                # arbitration → K/L/M 已产出；P v0 唯一接线点：m 已生成，在 n_outcome 写入前执行 P，回写 outcome
                arb_payload = build_arbitration_payload(
                    {
                        "winner": winner.task_id if winner else None,
                        "winner_type": winner_type,
                        "deferred": [t.task_id for t in deferred],
                        "deferred_types": [t.task_type for t in deferred],
                        "scores": scores,
                        "fairness": fairness,
                    },
                    k={"intent": intent.value},
                    l=l_result,
                    context=m_ctx,
                )
                m_action = arb_payload.get("m")
                prepared_text = None
                if winner and getattr(winner, "decision", None):
                    prepared_text = winner.decision.get("text")
                if not prepared_text and m_action:
                    prepared_text = self._p_v0_say_text(m_action)
                # force_engaged_test：无 winner 时 m 常为 NOP，P1 会 BLOCKED_NOT_SAY；合成 SAY + 占位文本以跑通 P2/P3/P4
                # 占位需满足 P2：min_len>=6、非占位短语；首帧用固定句使 P2 通过一次以写 P4（后续帧会因 duplicate 被 P2 拒）
                if getattr(self, "force_engaged_test", False):
                    if (m_action or {}).get("action_type") != "SAY" or not (prepared_text or "").strip():
                        m_action = {**(m_action or {}), "action_type": "SAY", "apply_now": True}
                        arb_payload["m"] = m_action
                    prepared_text = "前方路况正常可以通行"
                    # 满足 P1 ENGAGED 稳定时间门槛（3s），否则 BLOCKED_ENGAGED_NOT_STABLE
                    if getattr(self._p1_executor, "_rhythm_entered_ts", None) is None:
                        self._p1_executor._rhythm_entered_ts = now - 5.0
                        self._p1_executor._rhythm_state_prev = "ENGAGED"

                rhythm_state = getattr(self.runtime_ctx, "rhythm_state", "IDLE")
                p_outcome = None
                if self._p1_executor is not None:
                    s_report = None if getattr(self, "force_engaged_test", False) else ({"stress_level": self._last_s_stress_level} if self._last_s_stress_level else None)
                    p1_payload = {
                        "m": m_action or {},
                        "engagement": {"level": eng_level},
                        "rhythm": {"state": rhythm_state},
                        "s": s_report,
                        "text": prepared_text or "",
                        "_defer_speak_to_p2": self._p2_executor is not None,
                    }
                    p_outcome = self._p1_executor.execute(payload=p1_payload, now_ts=now)

                # P1.apply_now 且存在 P2 时：经 P2 门禁后再决定是否执行 SAY
                if (
                    p_outcome is not None
                    and getattr(p_outcome, "apply_now", p_outcome.executed)
                    and self._p2_executor is not None
                    and (prepared_text or "")
                ):
                    p2_out = self._p2_executor.evaluate(text=prepared_text or "", now_ts=now)
                    p2_dict = p2_out.debug.get("p2") or p2_out.to_dict()
                    if p2_out.allowed:
                        # P3：节律闸门，P2 通过后才跑；顺序 P1 → P2 → P3 → SAY
                        p3_out = None
                        p3_dict = {}
                        if self._p3_executor is not None:
                            p3_out = self._p3_executor.evaluate(
                                rhythm_state=rhythm_state,
                                now_ts=now,
                            )
                            p3_dict = p3_out.debug.get("p3") or p3_out.to_dict()
                            if not p3_out.allowed:
                                p_outcome = P1Outcome(
                                    ts=p_outcome.ts,
                                    executed=False,
                                    outcome_type="NO_ACTION",
                                    reason=p3_out.reason,
                                    action_type=p_outcome.action_type,
                                    text_len=p_outcome.text_len,
                                    debug={**p_outcome.debug, "p2": p2_dict, "p3": p3_dict},
                                    apply_now=True,
                                )
                        # 无 P3 或 P3 通过：P4 定结构 → 执行 SAY
                        if self._p3_executor is None or (p3_out is not None and p3_out.allowed):
                            plan = None
                            if self._p4_cfg is not None:
                                plan = plan_speech_p4_v0(
                                    cfg=self._p4_cfg,
                                    winner_type=arb_payload.get("arbitration", {}).get("winner_type") or winner_type or "NONE",
                                    engagement_level=eng_level,
                                    control_mode=m_ctx.get("control_mode", "ASSISTED"),
                                    view_confidence=float(m_ctx.get("vc") or 0.0),
                                    complexity_effective=float(m_ctx.get("complexity") or 0.0),
                                    pal_horizon_difficulty=float(m_ctx.get("pal") or 0.0),
                                    speak_budget_scale=getattr(self.runtime_ctx, "advice_budget_scale", None),
                                )
                                arb_payload["p4"] = plan.to_dict()
                                arb_payload["g"] = {"winner_type": arb_payload.get("arbitration", {}).get("winner_type") or winner_type or "NONE"}
                            text_to_say = (plan.prefix + prepared_text + plan.suffix) if plan else prepared_text
                            try:
                                # force_engaged_test：只跑 P 层写 trace，不实际播报；force_engaged_test_l2：允许真实 SAY 验证闭环
                                skip_tts = getattr(self, "force_engaged_test", False) and not getattr(self, "force_engaged_test_l2", False)
                                if not skip_tts and getattr(self._p1_executor, "speak_fn", None):
                                    self._p1_executor.speak_fn(text_to_say)
                                    self._p1_executor.last_say_ts = now
                                if self._p3_executor is not None:
                                    self._p3_executor.mark_say_executed(ts=now)
                                if p3_out is not None:
                                    p3_dict = p3_out.debug.get("p3") or p3_out.to_dict()
                                p_outcome = P1Outcome(
                                    ts=p_outcome.ts,
                                    executed=not skip_tts,
                                    outcome_type="ACTION_EXECUTED" if not skip_tts else "NO_ACTION",
                                    reason="force_engaged_test" if skip_tts else "SAY_OK",
                                    action_type=p_outcome.action_type,
                                    text_len=len(text_to_say),
                                    debug={**p_outcome.debug, "p2": p2_dict, "p3": p3_dict},
                                    apply_now=True,
                                )
                            except Exception as e:
                                p_outcome = P1Outcome(
                                    ts=p_outcome.ts,
                                    executed=False,
                                    outcome_type="NO_ACTION",
                                    reason="FAILED_EXCEPTION",
                                    action_type=p_outcome.action_type,
                                    text_len=len(text_to_say),
                                    debug={**p_outcome.debug, "p2": p2_dict, "p3": p3_dict, "exc": repr(e)},
                                    apply_now=True,
                                )
                    else:
                        p_outcome = P1Outcome(
                            ts=p_outcome.ts,
                            executed=False,
                            outcome_type="NO_ACTION",
                            reason=p2_out.reason,
                            action_type=p_outcome.action_type,
                            text_len=p_outcome.text_len,
                            debug={**p_outcome.debug, "p2": p2_dict},
                            apply_now=True,
                        )

                if p_outcome is not None:
                    outcome = {
                        "outcome_type": p_outcome.outcome_type,
                        "reason": p_outcome.reason,
                        "apply_now": getattr(p_outcome, "apply_now", p_outcome.executed),
                        "executed": p_outcome.executed,
                        "confidence": 1.0 if p_outcome.executed else 0.0,
                        "evidence": p_outcome.debug,
                    }
                    # P2 写入 outcome.p2 供 verify 读取
                    if "p2" in p_outcome.debug:
                        p2_info = p_outcome.debug["p2"]
                        outcome["p2"] = {
                            "allow": p2_info.get("allow", p2_info.get("allowed")),
                            "reason": p2_info.get("reason", ""),
                            "checks": p2_info.get("checks", {}),
                        }
                    # P3 写入 outcome.p3
                    if "p3" in p_outcome.debug:
                        p3_info = p_outcome.debug["p3"]
                        outcome["p3"] = {
                            "allow": p3_info.get("allow", p3_info.get("allowed")),
                            "reason": p3_info.get("reason", ""),
                            "checks": p3_info.get("checks", {}),
                        }
                else:
                    outcome = {
                        "outcome_type": "NO_ACTION",
                        "reason": "NOT_ATTEMPTED",
                        "apply_now": False,
                    }

                self._p_executed_this_tick = bool(p_outcome and p_outcome.executed)
                if p_outcome and p_outcome.executed:
                    self._did_speak_this_tick = True

                arb_payload["outcome"] = outcome
                # P5 v0：表达形态规划（shadow-only，不改变执行）
                p4_d = arb_payload.get("p4") or {}
                p5_plan = build_expression_plan_v0(
                    p1_apply_now=outcome.get("apply_now", False),
                    p2_allowed=bool(outcome.get("p2", {}).get("allow") or outcome.get("p2", {}).get("allowed")) if outcome.get("p2") else False,
                    p4_style=p4_d.get("style"),
                    p4_reason=p4_d.get("reason"),
                    winner_type=arb_payload.get("arbitration", {}).get("winner_type") or (arb_payload.get("g") or {}).get("winner_type"),
                )
                arb_payload["p5"] = p5_plan.to_dict()
                # Q v0：同条 arbitration 行必有 Q
                if p_outcome is not None:
                    q = self._q_recorder.record(
                        action_type=p_outcome.action_type,
                        executed=p_outcome.executed,
                        reason=p_outcome.reason,
                        latency_ms=None,
                        extra_meta={"text_len": p_outcome.text_len},
                    )
                else:
                    q = self._q_recorder.record(
                        action_type="NONE",
                        executed=False,
                        reason=outcome.get("reason", "NOT_ATTEMPTED"),
                        latency_ms=None,
                        extra_meta={"source": "arbitration_no_p"},
                    )
                arb_payload["q"] = q.to_dict()
                # R v0：喂入 Q，若有可解释观测则写入同条（不要求每 tick 都有 r）
                r_obs = self._r_collector.feed(q.to_dict())
                if r_obs is not None:
                    arb_payload["r"] = r_obs.to_dict()
                    # S v0：基于 R 观测推导压力报告（不要求每条 R 都产出 s）
                    s_report = self._s_observer.observe(r_obs.to_dict())
                    if s_report is not None:
                        arb_payload["s"] = s_report.to_dict()
                        self._last_s_stress_level = s_report.stress_level.value
                write_arbitration_payload(arb_payload)
                self._last_p_outcome = outcome  # 供 J 路径同条 trace 使用，避免重复计算

                if winner:
                    decisions_to_process = [winner.decision]
                else:
                    decisions_to_process = []

            # E) Advice 内容类型节律 v0：在 AdviceEngine → Decision 之间做配额 gate
            advice_rhythm = get_advice_rhythm_v0()
            arbitrator = get_arbitrator_v0() if eng_level in ("L1", "L2", "L3") else None
            for speak_decision in decisions_to_process:
                # P v0：本 tick 已通过 P 执行 SAY 则不再走原有播报，避免重复
                if getattr(self, "_p_executed_this_tick", False):
                    continue
                if speak_decision.get("type") != "SPEAK":
                    continue
                speak_text = speak_decision.get("text")
                if not speak_text:
                    continue
                # E) 内容类型节律 gate：只读，允许/不允许这次说
                allowed, _, advice_type, advice_rhythm_trace = advice_rhythm.check(
                    advice_category=speak_decision.get("advice_category"),
                    is_safety=bool(speak_decision.get("is_safety")),
                    now=time.time(),
                )
                log_advice_rhythm_event(advice_rhythm_trace)
                if not allowed:
                    continue
                self._did_speak_this_tick = True
                self._speak_safely(
                    speak_text,
                    scene_hash=scene_state.scene_hash,
                    shadow_context={
                        "task_id": speak_decision.get("advice_id"),
                        "level": eng_level,
                        "type": advice_type,
                    },
                )
                advice_rhythm.record_spoken(advice_type, now=time.time())
                advice_id = speak_decision.get("advice_id")
                if arbitrator and advice_id:
                    arbitrator.record_spoken(advice_id, now)
                spoken_advice_ids.append(advice_id)
                spoken_advice_categories.append(speak_decision.get("advice_category"))
                spoken_advice_is_safety.append(speak_decision.get("is_safety"))
                if advice_id:
                    self._last_advice_event = {
                        "advice_id": advice_id,
                        "is_safety": bool(speak_decision.get("is_safety")),
                        "ts": now,
                    }

            if spoken_advice_ids:
                result["advice_id"] = next((aid for aid in spoken_advice_ids if aid), None)
                result["advice_ids"] = spoken_advice_ids
                result["advice_category"] = next((cat for cat in spoken_advice_categories if cat), None)
                result["advice_is_safety"] = next(
                    (flag for flag in spoken_advice_is_safety if flag is not None),
                    None,
                )
            
            # 兼容原有的描述播报（如果配置启用且与 voice_text 不同）
            if OUTPUT_CONFIG['play_audio'] and result.get('description'):
                description = result['description']
                if description != voice_text:
                    # 对描述单独决策
                    desc_decision = self._handle_speech_decision({"description": description, "objects": result.get("objects", []), "texts": result.get("texts", [])})
                    if desc_decision["action"] == "SPEAK":
                        self._did_speak_this_tick = True
                        self._speak_safely(description, scene_hash=scene_state.scene_hash)

            # C3 模板一：Advice 被采纳（仅对实际播报的 advice_id 学习，E gate 拦截的不学习）
            for speak_decision in advice_decisions:
                aid = speak_decision.get("advice_id")
                if aid and aid in spoken_advice_ids:
                    self._maybe_learn_advice(
                        env_mode=self.runtime_ctx.env_mode,
                        advice_id=aid,
                        is_safety=bool(speak_decision.get("is_safety")),
                    )
        
        elif action == "WAIT":
            # 不能说，但系统继续运行 → 不播报（明确：系统在运行，只是不说话）
            self.logger.debug(f"Decision=WAIT reason={decision['reason']}")
            pass

        elif decision["action"] == "YIELD":
            # 用户优先 → 主动让位（明确：用户优先，系统让位）
            self.logger.debug(f"Decision=YIELD reason={decision['reason']}")
            pass

        # J) ENGAGED 且未执行：产出事实信号（signal-only），由 process_frame 写 engaged_signal
        rhythm_state = getattr(self.runtime_ctx, "rhythm_state", None)
        engagement = getattr(self.runtime_ctx, "engagement", None)
        eng_level = engagement.get("level", "L0") if engagement else "L0"
        eligibility = getattr(self.runtime_ctx, "eligibility", None)
        eligible = bool(eligibility.get("allowed", False)) if eligibility else False
        vc = getattr(self.runtime_ctx, "view_confidence", None)
        frame_quality = getattr(self.runtime_ctx, "frame_quality", "GOOD")

        engaged = rhythm_state == "ENGAGED" and eng_level in ("L1", "L2", "L3")
        action_decided = getattr(self, "_last_arbitration_winner", False)
        action_executed = self._did_speak_this_tick
        arbitration_winner = None if not action_decided else "WON"  # 仅用于 block_stage 判断，不存 winner_type
        cooldown_active = getattr(self, "_last_cooldown_active", False)

        signal = compute_engaged_signal(
            engaged=engaged,
            action_decided=action_decided,
            action_executed=action_executed,
            rhythm_state=rhythm_state,
            arbitration_winner=arbitration_winner,
            cooldown_active=cooldown_active,
            extra_context={
                "eligible": eligible,
                "view_confidence": vc,
                "frame_quality": frame_quality,
            },
        )
        if signal is not None:
            # P v0：本 tick 已在 arbitration 行写入 outcome 时复用，否则走 shadow-only N
            if getattr(self, "_last_p_outcome", None) is not None:
                outcome_payload = self._last_p_outcome
                self._last_p_outcome = None
            else:
                outcome = compute_outcome_v0(engaged_signal=signal)
                outcome_payload = outcome.to_trace_dict() if outcome else None

            # Q/R/S 链：J 路径有 outcome 时也产出 q（并喂 R、S），使整链可观测
            q_payload = None
            r_payload = None
            s_payload = None
            if outcome_payload is not None:
                executed = outcome_payload.get("outcome_type") in ("ACTION_EXECUTED", "ACTION")
                reason = outcome_payload.get("reason", "UNKNOWN")
                q = self._q_recorder.record(
                    action_type="SAY",
                    executed=executed,
                    reason=reason,
                    latency_ms=None,
                    extra_meta={"source": "J_path"},
                )
                q_payload = q.to_dict()
                r_obs = self._r_collector.feed(q_payload)
                if r_obs is not None:
                    r_payload = r_obs.to_dict()
                    s_report = self._s_observer.observe(r_payload)
                    if s_report is not None:
                        s_payload = s_report.to_dict()

            return {
                "engaged_signal": signal.to_trace_dict(),
                "outcome": outcome_payload,
                "q": q_payload,
                "r": r_payload,
                "s": s_payload,
            }
        return None

    def _p_v0_say_text(self, m: Dict[str, Any]) -> str:
        """P v0：从 M 的 content_hint 生成最小播报文案（可回滚、可扩展）。"""
        hint = (m or {}).get("content_hint") or ""
        return {
            "environment_observation": "注意到环境变化",
            "task_state_update": "任务状态更新",
            "navigation_guidance": "正在导航",
            "safety_alert": "注意安全",
        }.get(hint, "收到") if hint else "收到"

    def _maybe_learn_advice(self, env_mode, advice_id: str, is_safety: bool) -> None:
        """
        C3 模板一：Advice 被反复采纳（最小实现）
        - 仅在 SAFE/ASSISTED/低复杂度下生效
        - 安全兜底建议不学习
        """
        if not self.c3_learner or is_safety:
            return
        if env_mode is None:
            return
        if not advice_id:
            return
        if advice_id in FORBIDDEN_ADVICE_IDS:
            return
        pattern, tendency = self._build_c3_pattern(env_mode, advice_id)
        if not pattern or not tendency:
            return

        self.c3_learner.observe(
            env_mode=env_mode,
            pattern=pattern,
            tendency=tendency,
            positive=True,
        )

    def _maybe_learn_negative_advice_from_speech(self, result: dict) -> None:
        if not self.c3_learner:
            return
        speech_input = result.get("speech_input") or ""
        if not speech_input.strip():
            return
        neg_type = self._classify_negative_feedback(speech_input)
        if not neg_type:
            return

        last_event = self._last_advice_event
        if not last_event:
            return
        if time.time() - last_event.get("ts", 0.0) > 30:
            return

        last_text = self._last_negative_speech.get("text")
        last_ts = self._last_negative_speech.get("ts", 0.0)
        if last_text == speech_input and time.time() - last_ts < 10:
            return

        env_mode = self.runtime_ctx.env_mode
        advice_id = last_event.get("advice_id")
        if not advice_id:
            return
        pattern, _ = self._build_c3_pattern(env_mode, advice_id)
        if not pattern:
            return

        now = time.time()
        self._last_negative_speech = {"text": speech_input, "ts": now}
        key = f"{advice_id}|{pattern}"
        hit = self._negative_feedback_hits.get(key, {"count": 0, "last_ts": 0.0})
        if now - hit["last_ts"] > self.c3_cfg.negative_window_sec:
            hit = {"count": 0, "last_ts": 0.0}
        hit["count"] += 1
        hit["last_ts"] = now
        self._negative_feedback_hits[key] = hit

        if neg_type == "timing" and hit["count"] < 2:
            return
        if hit["count"] < self.c3_cfg.negative_min_hits:
            return

        self._negative_feedback_hits[key] = {"count": 0, "last_ts": now}
        self._maybe_learn_negative_advice(
            env_mode=env_mode,
            advice_id=advice_id,
            is_safety=last_event.get("is_safety", False),
        )

    def _maybe_learn_negative_advice(self, env_mode, advice_id: str, is_safety: bool) -> None:
        if not self.c3_learner or is_safety:
            return
        if env_mode is None:
            return
        if not advice_id:
            return
        if advice_id in FORBIDDEN_ADVICE_IDS:
            return

        pattern, tendency = self._build_c3_pattern(env_mode, advice_id)
        if not pattern or not tendency:
            return

        self.c3_learner.observe(
            env_mode=env_mode,
            pattern=pattern,
            tendency=tendency,
            positive=False,
        )

    def _build_c3_pattern(self, env_mode, advice_id: str):
        tendency = ADVICE_TO_TENDENCY.get(advice_id)
        if not tendency:
            return None, None
        bucket = bucket_complexity(env_mode.complexity_score)
        bucket_map = {
            "LOW": "低复杂",
            "MID": "中复杂",
            "HIGH": "高复杂",
        }
        category = ADVICE_TO_CATEGORY.get(advice_id, "通用建议")
        pattern = f"{bucket_map.get(bucket, '低复杂')}环境 + {category}"
        return pattern, tendency

    def _classify_negative_feedback(self, text: str) -> str:
        lowered = text.lower()
        emotional_tokens = (
            "烦", "别烦", "生气", "讨厌", "滚", "闭嘴", "别吵", "吵死", "烦死",
            "annoy", "angry", "shut up",
        )
        if any(token in lowered for token in emotional_tokens):
            return ""
        emergency_tokens = ("快走", "快点", "危险", "赶紧", "hurry", "danger")
        if any(token in lowered for token in emergency_tokens):
            return ""
        factual_tokens = ("看错", "不是这样", "不对", "错了", "that's wrong", "you are wrong")
        if any(token in lowered for token in factual_tokens):
            return ""
        vague_tokens = ("算了", "没事", "随便", "whatever")
        if any(token in lowered for token in vague_tokens):
            return ""
        negation_tokens = (
            "不要", "别", "不需要", "不用", "不必", "别再", "不要再", "停止",
            "don't", "do not", "stop", "no need",
        )
        advice_tokens = ("提醒", "建议", "提示", "播报", "说", "讲", "talk", "remind", "suggest", "say")
        freq_tokens = ("一直", "每次", "频繁", "每回", "repeat", "every time", "too frequent", "often")
        timing_tokens = ("等会", "待会", "稍后", "现在不用", "not now", "later")
        autonomy_tokens = ("我知道", "我自己来", "我能处理", "我懂了", "我可以", "i know", "i can handle", "i got it", "i'm fine")
        has_negation = any(token in lowered for token in negation_tokens)
        has_advice_ref = any(token in lowered for token in advice_tokens)
        has_freq = any(token in lowered for token in freq_tokens)
        has_timing = any(token in lowered for token in timing_tokens)
        has_autonomy = any(token in lowered for token in autonomy_tokens)

        if has_negation and has_advice_ref:
            return "direct"
        if has_negation and has_freq:
            return "frequency"
        if has_autonomy:
            return "autonomy"
        if has_timing and (has_negation or has_advice_ref):
            return "timing"
        return ""

    def _maybe_run_c3_maintenance(self) -> None:
        if not self.c3_cfg.enabled:
            return
        now = time.time()
        if now - self._last_c3_maintenance_ts < 600:
            return
        self._last_c3_maintenance_ts = now
        c3_maintenance(self.c3_store, self.c3_cfg, now=now)

    def _get_advice_tasks(self, env_mode) -> list:
        """
        AdviceEngine 的任务来源（v0 最小接入）。
        """
        return [
            AdviceTask(
                task_type="REMINDER_FREQUENCY",
                context={
                    "env_mode": env_mode,
                    "reason": "speak_allowed",
                },
            )
        ]
    
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
    
    def run(self, show_camera: bool = True, max_seconds: Optional[float] = None):
        """
        运行主循环
        
        Args:
            show_camera: 是否显示摄像头画面
            max_seconds: 可选，运行满此时长后自动退出（用于 ACTIVE×视频 等限时测试）
        """
        # v1.8.5 Phase B Step 1.1: 通过 PipelineController 检查摄像头状态
        if not self.pipeline_controller.is_opened():
            self.logger.error("摄像头未打开，无法运行")
            return
        
        self.is_running = True
        self.logger.info("开始运行Luna徽章系统...")
        run_start = time.time()
        
        # 启动语音对话
        self._start_voice_conversation()
        
        # 视频模式下降速：按视频 FPS 节流，使播放接近实时（可选）
        video_fps = getattr(self.pipeline_controller, "video_fps", 0.0) or 0.0
        last_frame_time = time.time()
        
        try:
            while self.is_running:
                if max_seconds is not None and (time.time() - run_start) >= max_seconds:
                    self.logger.info("已达限时 %.0f 秒，退出主循环", max_seconds)
                    break
                # v1.8.5 Phase B Step 1.1: 通过 PipelineController 读取摄像头帧
                frame = self.pipeline_controller.read_frame()
                if frame is None:
                    if getattr(self.pipeline_controller, "input_ended", False):
                        self.logger.info("视频已播放完毕，退出主循环")
                        break
                    self.logger.warning("无法读取摄像头帧，跳过")
                    continue
                # 视频模式：按 FPS 节流，避免播放快于实时
                if video_fps > 0:
                    now = time.time()
                    target_interval = 1.0 / video_fps
                    elapsed = now - last_frame_time
                    if elapsed < target_interval:
                        time.sleep(target_interval - elapsed)
                    last_frame_time = time.time()
                else:
                    last_frame_time = time.time()
                frame_context = self.pipeline_controller.get_frame_context()
                
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
                        self.process_frame(frame, context=frame_context)
                        continue
                
                # 按间隔处理帧
                current_time = time.time()
                if current_time - self.last_process_time >= PROCESSING_CONFIG['process_interval']:
                    self.logger.info("开始处理当前帧...")
                    self.process_frame(frame, context=frame_context)
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
    parser.add_argument('--video', type=str, default=None,
                       help='使用视频文件作为输入（路径），不使用时为摄像头')
    parser.add_argument('--force-engaged-test', dest='force_engaged_test', action='store_true',
                       help='N 层验收：强制 ENGAGED 且本 tick 不执行动作，仅测试用')
    parser.add_argument('--force-engaged-test-l2', dest='force_engaged_test_l2', action='store_true',
                       help='执行链路测试：强制 L2 并允许真实 SAY，验证 P1–P5→Q/R/S 闭环（仅测试用）')
    
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
    
    # 创建并运行Luna徽章系统（支持 --video、--force-engaged-test、--force-engaged-test-l2）
    luna_badge = LunaBadgeMVP(
        video_path=args.video,
        force_engaged_test=getattr(args, "force_engaged_test", False),
        force_engaged_test_l2=getattr(args, "force_engaged_test_l2", False),
    )
    luna_badge.run(show_camera=not args.no_camera)


if __name__ == "__main__":
    main()
