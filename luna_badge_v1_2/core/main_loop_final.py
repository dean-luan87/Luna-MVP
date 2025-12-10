#!/usr/bin/env python3
"""
Luna Badge v1.4.2 完整主循环（可直接运行）
整合所有模块：vision, system, navigation, speech, task
"""
import time
import logging
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager

# v1.4.2 模块
from core.vision.vision_pipeline import VisionPipeline
from core.system.system_loop import SystemLoop
from core.navigation.navigation_controller_integration import NavigationControllerIntegration
from core.speech.speech_pipeline_integration import SpeechPipelineIntegration
from core.task.task_transition_manager import (
    TaskTransitionManager,
    PositionState,
    UserIntentState,
)
from core.task.query_bus import QueryBus
from core.task.multi_target_buffer import MultiTargetBuffer, Target
from core.system.safe_mode import SafeModeManager

logger = LogManager.get_logger(__name__)


class MainLoopFinal:
    """
    v1.4.2 完整主循环
    """
    
    def __init__(self):
        """初始化所有模块"""
        logger.info("=" * 60)
        logger.info("[MAIN_LOOP] Initializing v1.4.2 main loop...")
        logger.info("=" * 60)
        
        # 1. 问询总线（需要先创建，因为其他模块会用到）
        self.query_bus = QueryBus(tts_say=self._tts_say)
        
        # 2. 任务转换管理器
        self.task_transition = TaskTransitionManager(
            ask_end_callback=self._ask_user_if_end_task
        )
        
        # 3. 多目标缓存
        self.multi_target_buffer = MultiTargetBuffer()
        
        # 4. 安全模式
        self.safe_mode = SafeModeManager(tts_say=self._tts_say)
        
        # 5. 系统循环（包含恢复中心）
        self.system_loop = SystemLoop(
            safe_mode=self.safe_mode,
            restart_vision=self._restart_vision,
            restart_speech=self._restart_speech,
            restart_navigation=self._restart_navigation,
        )
        
        # 6. 视觉管线
        self.vision_pipeline = VisionPipeline(
            model_predict=self._model_predict,
        )
        
        # 7. 导航控制器集成
        self.nav_controller = NavigationControllerIntegration(
            task_transition=self.task_transition,
            query_bus=self.query_bus,
            multi_target_buffer=self.multi_target_buffer,
            safe_mode=self.safe_mode,
        )
        
        # 8. 语音管线集成
        self.speech_pipeline = SpeechPipelineIntegration(
            query_bus=self.query_bus,
            asr_recognize=self._asr_recognize,
            tts_say=self._tts_say,
            nlu_parse=self._nlu_parse,
        )
        
        # 运行状态
        self.running = False
        self.frame_count = 0
        
        # 模拟数据（实际应该从真实模块获取）
        self._motion_detected = True
        self._task_priority = 5
        self._position_state = PositionState(
            at_target=False,
            distance_to_target=10.0,
            stationary_seconds=0.0,
        )
        self._user_intent = UserIntentState(
            want_stop=False,
            want_continue=False,
        )
        
        logger.info("[MAIN_LOOP] All modules initialized")
        logger.info("=" * 60)
    
    def _tts_say(self, text: str) -> None:
        """TTS 播报（需要对接实际 TTS 模块）"""
        logger.info(f"[TTS] {text}")
        # TODO: 对接实际 TTS 模块
        # from core.tts.tts_manager import TTSManager
        # TTSManager.speak(text)
    
    def _asr_recognize(self) -> Optional[str]:
        """ASR 识别（需要对接实际 ASR 模块）"""
        # TODO: 对接实际 ASR 模块
        # from core.asr.asr_manager import ASRManager
        # return ASRManager.recognize()
        return None
    
    def _nlu_parse(self, text: str) -> Dict[str, Any]:
        """NLU 解析（需要对接实际 NLU 模块）"""
        # TODO: 对接实际 NLU 模块
        # from core.nlu.nlu_manager import NLUManager
        # return NLUManager.parse(text)
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["是", "yes", "对", "好", "可以"]):
            return {"answer": "yes"}
        elif any(kw in text_lower for kw in ["否", "no", "不", "不要"]):
            return {"answer": "no"}
        return {"answer": "unknown"}
    
    def _model_predict(self, frame: Any) -> Dict[str, Any]:
        """模型推理（需要对接实际模型）"""
        # TODO: 对接实际模型
        # from core.yolo_detector import YoloDetector
        # return self.yolo_detector.infer(frame)
        
        # 模拟推理
        time.sleep(0.05)
        return {"objects": [], "obstacle_distance": 2.0}
    
    def _restart_vision(self) -> None:
        """重启视觉模块"""
        logger.warning("[MAIN_LOOP] Restarting vision module...")
        # TODO: 实现视觉模块重启逻辑
        # 1. 停止当前视觉线程
        # 2. 重新初始化模型
        # 3. 重启线程
        self.system_loop.update_heartbeat("vision")
        logger.info("[MAIN_LOOP] Vision module restarted")
    
    def _restart_speech(self) -> None:
        """重启语音模块"""
        logger.warning("[MAIN_LOOP] Restarting speech module...")
        # TODO: 实现语音模块重启逻辑
        self.system_loop.update_heartbeat("speech")
        logger.info("[MAIN_LOOP] Speech module restarted")
    
    def _restart_navigation(self) -> None:
        """重启导航模块"""
        logger.warning("[MAIN_LOOP] Restarting navigation module...")
        # TODO: 实现导航模块重启逻辑
        self.system_loop.update_heartbeat("navigation")
        logger.info("[MAIN_LOOP] Navigation module restarted")
    
    def _ask_user_if_end_task(self) -> None:
        """向用户问询是否结束任务"""
        query_id = self.query_bus.push_query(
            "您已经接近目的地，需要结束任务吗？",
            priority=10,
            timeout_seconds=15.0,
            on_resolved=self._on_task_end_query_resolved,
            on_timeout=self._on_task_end_query_timeout,
        )
        logger.info(f"[MAIN_LOOP] Pushed task end query: {query_id}")
    
    def _on_task_end_query_resolved(self, result: Dict[str, Any]) -> None:
        """任务结束问询的回复处理"""
        answer = result.get("answer", "").lower()
        if answer in ("yes", "是", "到了", "到达", "结束"):
            logger.info("[MAIN_LOOP] User confirmed task end")
            self.nav_controller.stop()
        else:
            logger.info("[MAIN_LOOP] User wants to continue")
    
    def _on_task_end_query_timeout(self) -> None:
        """任务结束问询超时处理"""
        logger.warning("[MAIN_LOOP] Task end query timeout, assuming continue")
        # 默认继续任务
    
    def _get_cpu_load(self) -> float:
        """获取 CPU 负载"""
        return self.system_loop.recovery_center._get_cpu_load()
    
    def _update_position_state(self, results: Dict[str, Any]) -> None:
        """更新位置状态（从视觉结果或导航模块）"""
        # TODO: 从实际导航模块获取
        # self._position_state = navigation.get_position_state()
        pass
    
    def _update_user_intent(self) -> None:
        """更新用户意图（从 ASR 结果）"""
        # TODO: 从实际 ASR/NLU 模块获取
        # asr_text = self.speech_pipeline.asr_recognize()
        # if asr_text:
        #     parsed = self.speech_pipeline.nlu_parse(asr_text)
        #     if parsed.get("intent") == "stop":
        #         self._user_intent.want_stop = True
        pass
    
    def run(self):
        """主循环"""
        logger.info("[MAIN_LOOP] Starting main loop...")
        self.running = True
        
        try:
            while self.running:
                loop_start = time.time()
                
                # 1) 系统健康检查（每秒一次）
                self.system_loop.tick()
                
                # 2) 问询总线 tick
                self.speech_pipeline.tick()
                
                # 3) 更新用户意图（从 ASR）
                self._update_user_intent()
                
                # 4) 处理 ASR 结果（如果有）
                asr_text = self._asr_recognize()
                if asr_text:
                    self.speech_pipeline.process_asr_result(asr_text)
                
                # 5) 安全模式检查
                if self.system_loop.is_safe_mode_active():
                    # 获取帧用于障碍物检测
                    frame, _ = self.vision_pipeline.get_frame()
                    if frame is not None:
                        # 简单障碍物检测（实际应该从视觉结果获取）
                        obstacle_distance = 2.0  # TODO: 从视觉结果获取
                        self.system_loop.handle_safe_mode_frame(obstacle_distance)
                    time.sleep(0.1)
                    continue
                
                # 6) 视觉管线处理
                cpu_load = self._get_cpu_load()
                results = self.vision_pipeline.process_frame(
                    context=None,  # TODO: 从导航状态获取上下文
                    cpu_load=cpu_load,
                    motion_detected=self._motion_detected,
                    task_priority=self._task_priority,
                )
                
                # 更新心跳
                if results is not None:
                    self.system_loop.update_heartbeat("vision")
                
                # 7) 更新位置状态
                if results:
                    self._update_position_state(results)
                    obstacle_distance = results.get("obstacle_distance")
                else:
                    obstacle_distance = None
                
                # 8) 导航逻辑
                nav_result = self.nav_controller.step(
                    objects=results or {},
                    position_state=self._position_state,
                    user_intent=self._user_intent,
                    obstacle_distance=obstacle_distance,
                )
                
                # 更新心跳
                self.system_loop.update_heartbeat("navigation")
                
                # 9) 检查目标完成
                if nav_result.get("action") == "stop":
                    # 检查是否有下一个目标
                    next_target = self.nav_controller.handle_target_complete()
                    if next_target:
                        # 等待用户回答（由 QueryBus 处理）
                        pass
                
                self.frame_count += 1
                
                # 控制循环频率（至少 20 FPS）
                loop_time = time.time() - loop_start
                if loop_time < 0.05:
                    time.sleep(0.05 - loop_time)
                
                # 每 100 帧打印一次统计
                if self.frame_count % 100 == 0:
                    self._print_stats()
                
        except KeyboardInterrupt:
            logger.info("[MAIN_LOOP] Received interrupt signal")
        except Exception as e:
            logger.exception(f"[MAIN_LOOP] Fatal error: {e}")
        finally:
            self.stop()
    
    def _print_stats(self) -> None:
        """打印统计信息"""
        vision_stats = self.vision_pipeline.get_stats()
        speech_stats = self.speech_pipeline.get_stats()
        health = self.system_loop.get_health_status()
        
        logger.info(f"[MAIN_LOOP] Stats - Frames: {self.frame_count}, "
                   f"Vision: {vision_stats['frame_count']}, "
                   f"FailSafe: {vision_stats['fail_safe_state']}, "
                   f"SafeMode: {self.system_loop.is_safe_mode_active()}, "
                   f"CPU: {health['cpu_load']*100:.1f}%")
    
    def stop(self):
        """停止主循环"""
        logger.info("[MAIN_LOOP] Stopping main loop...")
        self.running = False
        self.vision_pipeline.release()
        logger.info("[MAIN_LOOP] Main loop stopped")


def main():
    """主函数"""
    # 初始化配置和日志
    env = os.getenv("LUNA_ENV", "dev")
    ConfigCenter.init(env=env)
    LogManager.init()
    
    logger.info("=" * 60)
    logger.info("Luna Badge v1.4.2 Main Loop")
    logger.info("=" * 60)
    
    # 创建并运行主循环
    main_loop = MainLoopFinal()
    try:
        main_loop.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        main_loop.stop()


if __name__ == "__main__":
    main()




