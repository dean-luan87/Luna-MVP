#!/usr/bin/env python3
"""
Luna Badge v1.4.2 主循环
多轨调度主循环：整合 camera_router, vision_scheduler, fail_safe, recovery_center, safe_mode, task_transition, query_bus
"""
import time
import logging
from typing import Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.vision.camera_router import CameraRouter
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
from core.vision.vision_fail_safe import VisionFailSafe
from core.system.system_recovery_center import RecoveryCenter
from core.system.safe_mode import SafeModeManager, SafeModeContext
from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext as TransitionTaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)
from core.task.query_bus import QueryBus
from core.task.multi_target_buffer import MultiTargetBuffer

logger = LogManager.get_logger(__name__)


class MainLoopV142:
    """
    v1.4.2 主循环：多轨调度架构
    """
    
    def __init__(self):
        """初始化所有模块"""
        logger.info("[MAIN_LOOP] Initializing v1.4.2 main loop...")
        
        # 1. 摄像头路由
        self.camera_router = CameraRouter()
        
        # 2. 视觉调度器
        self.vision_scheduler = VisionScheduler()
        self.last_infer_ts = 0.0
        
        # 3. 视觉降级
        self.vision_fail_safe = VisionFailSafe()
        self.vision_fail_safe.set_degraded_callback(self._on_vision_degraded)
        self.vision_fail_safe.set_critical_callback(self._on_vision_critical)
        
        # 4. 系统恢复中心
        self.recovery_center = RecoveryCenter(
            get_cpu_load=self._get_cpu_load,
            safe_mode_enter=self._enter_safe_mode,
            restart_vision=self._restart_vision,
            restart_speech=self._restart_speech,
        )
        self._register_modules()
        
        # 5. 安全模式
        self.safe_mode = SafeModeManager(tts_say=self._tts_say)
        
        # 6. 任务转换管理器
        self.task_transition = TaskTransitionManager(
            ask_end_callback=self._ask_user_if_end_task
        )
        
        # 7. 问询总线
        self.query_bus = QueryBus(tts_say=self._tts_say)
        
        # 8. 多目标缓存
        self.multi_target_buffer = MultiTargetBuffer()
        
        # 运行状态
        self.running = False
        self.frame_count = 0
        
        logger.info("[MAIN_LOOP] All modules initialized")
    
    def _register_modules(self):
        """注册需要监控的模块"""
        self.recovery_center.register_module("vision", timeout_seconds=5.0)
        self.recovery_center.register_module("speech", timeout_seconds=5.0)
        self.recovery_center.register_module("navigation", timeout_seconds=10.0)
    
    def _get_cpu_load(self) -> float:
        """获取 CPU 负载（0.0 ~ 1.0）"""
        if PSUTIL_AVAILABLE:
            try:
                return psutil.cpu_percent(interval=0.1) / 100.0
            except Exception:
                return 0.5  # 默认值
        return 0.5
    
    def _tts_say(self, text: str) -> None:
        """TTS 播报（需要对接实际 TTS 模块）"""
        logger.info(f"[TTS] {text}")
        # TODO: 对接实际 TTS 模块
        # from core.tts.tts_manager import TTSManager
        # TTSManager.speak(text)
    
    def _on_vision_degraded(self) -> None:
        """视觉降级回调"""
        logger.error("[MAIN_LOOP] Vision degraded, switching to tiny model")
        # TODO: 切换模型
        # self.model_switcher.switch_to_tiny()
        # self.vision_scheduler._intervals["degraded"] = 0.8
    
    def _on_vision_critical(self) -> None:
        """视觉严重错误回调"""
        logger.critical("[MAIN_LOOP] Vision critical, entering SafeMode")
        self._enter_safe_mode()
    
    def _enter_safe_mode(self) -> None:
        """进入安全模式"""
        self.safe_mode.enter()
    
    def _restart_vision(self) -> None:
        """重启视觉模块"""
        logger.warning("[MAIN_LOOP] Restarting vision module...")
        # TODO: 实现视觉模块重启逻辑
        # 1. 停止当前视觉线程
        # 2. 重新初始化模型
        # 3. 重启线程
        self.recovery_center.update_heartbeat("vision")
    
    def _restart_speech(self) -> None:
        """重启语音模块"""
        logger.warning("[MAIN_LOOP] Restarting speech module...")
        # TODO: 实现语音模块重启逻辑
        self.recovery_center.update_heartbeat("speech")
    
    def _ask_user_if_end_task(self) -> None:
        """向用户问询是否结束任务"""
        query_id = self.query_bus.push_query(
            "您是否已到达目的地？",
            priority=8,
            timeout_seconds=15.0,
            on_resolved=self._on_task_end_query_resolved,
            on_timeout=self._on_task_end_query_timeout,
        )
        logger.info(f"[MAIN_LOOP] Pushed task end query: {query_id}")
    
    def _on_task_end_query_resolved(self, result: dict) -> None:
        """任务结束问询的回复处理"""
        answer = result.get("answer", "").lower()
        if answer in ("yes", "是", "到了", "到达"):
            logger.info("[MAIN_LOOP] User confirmed task end")
            # TODO: 结束当前任务
            # self.task_manager.end_current_task()
        else:
            logger.info("[MAIN_LOOP] User wants to continue")
    
    def _on_task_end_query_timeout(self) -> None:
        """任务结束问询超时处理"""
        logger.warning("[MAIN_LOOP] Task end query timeout, assuming continue")
        # 默认继续任务
    
    def _get_motion_detected(self) -> bool:
        """检测是否有移动（需要对接实际移动检测）"""
        # TODO: 对接实际移动检测模块
        # 可以从视觉结果中判断，或者从传感器数据判断
        return True  # 临时返回 True
    
    def _get_task_priority(self) -> int:
        """获取当前任务优先级（1~10）"""
        # TODO: 从任务管理器获取
        return 5  # 默认中等优先级
    
    def _get_position_state(self) -> PositionState:
        """获取位置状态（需要对接导航模块）"""
        # TODO: 对接导航模块获取实际位置
        return PositionState(
            at_target=False,
            distance_to_target=10.0,
            stationary_seconds=0.0,
        )
    
    def _get_user_intent(self) -> UserIntentState:
        """获取用户意图（需要对接语义理解模块）"""
        # TODO: 对接语义理解模块
        return UserIntentState(
            want_stop=False,
            want_continue=False,
        )
    
    def _run_vision_inference(self, frame) -> Optional[dict]:
        """执行视觉推理（需要对接实际推理模块）"""
        try:
            # TODO: 对接实际推理模块
            # from core.yolo_detector import YoloDetector
            # results = self.yolo_detector.infer(frame)
            
            # 模拟推理
            time.sleep(0.05)  # 模拟推理时间
            return {"objects": []}
        except Exception as e:
            logger.exception(f"[MAIN_LOOP] Vision inference error: {e}")
            self.vision_fail_safe.report_infer_timeout()
            return None
    
    def run(self):
        """主循环"""
        logger.info("[MAIN_LOOP] Starting main loop...")
        self.running = True
        
        recovery_tick_interval = 1.0  # 每1秒检查一次恢复中心
        last_recovery_tick = 0.0
        
        try:
            while self.running:
                loop_start = time.time()
                
                # 1. 获取摄像头帧
                frame, cam_id = self.camera_router.get_frame()
                if frame is None:
                    self.vision_fail_safe.report_camera_error()
                    time.sleep(0.1)
                    continue
                
                # 2. 检查安全模式
                if self.safe_mode.is_active():
                    # 安全模式下只做基础防撞检测
                    ctx = SafeModeContext(obstacle_distance=None)  # TODO: 从视觉结果获取
                    self.safe_mode.handle_frame(ctx)
                    time.sleep(0.1)
                    continue
                
                # 3. 视觉调度：判断是否需要推理
                now = time.time()
                scheduler_ctx = SchedulerContext(
                    cpu_load=self._get_cpu_load(),
                    motion_detected=self._get_motion_detected(),
                    task_priority=self._get_task_priority(),
                    last_infer_ts=self.last_infer_ts,
                    now_ts=now,
                )
                
                if self.vision_scheduler.should_infer(scheduler_ctx):
                    # 执行推理
                    try:
                        results = self._run_vision_inference(frame)
                        if results is not None:
                            self.last_infer_ts = now
                            self.recovery_center.update_heartbeat("vision")
                        else:
                            # 推理失败
                            self.vision_fail_safe.report_infer_timeout()
                    except Exception as e:
                        logger.exception(f"[MAIN_LOOP] Inference error: {e}")
                        self.vision_fail_safe.report_infer_timeout()
                
                # 4. 恢复中心 tick（每1秒）
                if now - last_recovery_tick >= recovery_tick_interval:
                    self.recovery_center.tick()
                    last_recovery_tick = now
                
                # 5. 问询总线 tick
                self.query_bus.tick()
                
                # 6. 任务转换判断
                task_ctx = TransitionTaskContext(
                    position=self._get_position_state(),
                    intent=self._get_user_intent(),
                )
                decision = self.task_transition.decide(task_ctx)
                if decision == TaskDecision.END:
                    logger.info("[MAIN_LOOP] Task ended by user")
                    # TODO: 结束任务
                
                # 7. 更新心跳
                self.recovery_center.update_heartbeat("navigation")
                
                self.frame_count += 1
                
                # 控制循环频率
                loop_time = time.time() - loop_start
                if loop_time < 0.05:  # 至少 20 FPS
                    time.sleep(0.05 - loop_time)
                
        except KeyboardInterrupt:
            logger.info("[MAIN_LOOP] Received interrupt signal")
        except Exception as e:
            logger.exception(f"[MAIN_LOOP] Fatal error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """停止主循环"""
        logger.info("[MAIN_LOOP] Stopping main loop...")
        self.running = False
        self.camera_router.release()
        logger.info("[MAIN_LOOP] Main loop stopped")


if __name__ == "__main__":
    # 初始化配置和日志
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    # 创建并运行主循环
    main_loop = MainLoopV142()
    try:
        main_loop.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        main_loop.stop()




