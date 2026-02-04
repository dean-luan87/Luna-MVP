"""
Navigation Task (v1.3.0)

导航任务

将 F2-F8 串联为一个可控、可暂停、可恢复的导航任务
"""

import time
import logging
from typing import Optional, Dict, Any, List

from .navigation_state import NavigationState
from .navigation_context import NavigationContext

logger = logging.getLogger(__name__)


class NavigationTask:
    """
    导航任务

    核心任务类，负责管理整个导航流程
    """

    def __init__(
        self,
        context: NavigationContext,
        navigation_engine=None,
        navigator=None,
        speech_manager=None,
        logger_instance=None,
        tts_manager=None,
    ):
        """
        初始化导航任务

        Args:
            context: 导航上下文
            navigation_engine: NavigationEngine 实例（优先使用，如果提供则忽略 navigator/speech_manager）
            navigator: F7 Navigator 实例（向后兼容，如果不提供 navigation_engine）
            speech_manager: F8 NavSpeechManager 实例（向后兼容，如果不提供 navigation_engine）
            logger_instance: 日志记录器（可选）
            tts_manager: TTS 管理器（可选）
        """
        self.context = context
        self.engine = navigation_engine
        self.navigator = navigator  # 向后兼容
        self.speech_manager = speech_manager  # 向后兼容
        self.logger = logger_instance or logger
        self.tts_manager = tts_manager  # TTS 管理器（可选）

        # 状态
        self.state = NavigationState.IDLE

        # 日志记录（每帧的事件）
        self.event_log: List[Dict[str, Any]] = []

        # 偏航检测
        self.consecutive_stops = 0  # 连续 STOP 次数
        self.max_consecutive_stops = 10  # 最大连续 STOP 次数（触发偏航提示）

        if self.engine:
            self.logger.info(f"导航任务初始化完成（使用 NavigationEngine），目标: {context.target}")
        else:
            self.logger.info(f"导航任务初始化完成（使用 Navigator/SpeechManager），目标: {context.target}")

    def start(self) -> bool:
        """
        开始导航

        Returns:
            bool: 是否成功启动
        """
        if not self.state.can_transition_to(NavigationState.ACTIVE):
            self.logger.warning(f"无法从 {self.state} 转换到 ACTIVE")
            return False

        self.state = NavigationState.ACTIVE
        self.context.start_time = time.time()
        self.context.frame_count = 0
        self.context.decision_count = {}

        self._log_event("task_start", {
            "target": self.context.target,
            "target_location": self.context.target_location,
        })

        # 尝试记录状态变化事件
        try:
            from core.tracking import track_event
            track_event(
                "navigation_task",
                "navigation_task_state_change",
                {"state": "ACTIVE", "target": self.context.target}
            )
        except Exception:
            pass

        self.logger.info(f"导航任务已启动，目标: {self.context.target}")
        return True

    def pause(self, reason: str = "user_request") -> bool:
        """
        暂停导航

        Args:
            reason: 暂停原因

        Returns:
            bool: 是否成功暂停
        """
        if not self.state.can_transition_to(NavigationState.PAUSED):
            self.logger.warning(f"无法从 {self.state} 转换到 PAUSED")
            return False

        self.state = NavigationState.PAUSED
        self.context.pause_time = time.time()

        self._log_event("task_pause", {"reason": reason})

        # 尝试记录状态变化事件
        try:
            from core.tracking import track_event
            track_event(
                "navigation_task",
                "navigation_task_state_change",
                {"state": "PAUSED", "reason": reason}
            )
        except Exception:
            pass

        self.logger.info(f"导航任务已暂停，原因: {reason}")
        return True

    def resume(self) -> bool:
        """
        恢复导航

        Returns:
            bool: 是否成功恢复
        """
        if not self.state.can_transition_to(NavigationState.ACTIVE):
            self.logger.warning(f"无法从 {self.state} 转换到 ACTIVE")
            return False

        self.state = NavigationState.ACTIVE
        self.context.resume_time = time.time()

        self._log_event("task_resume", {})

        # 尝试记录状态变化事件
        try:
            from core.tracking import track_event
            track_event(
                "navigation_task",
                "navigation_task_state_change",
                {"state": "ACTIVE", "action": "resume"}
            )
        except Exception:
            pass

        self.logger.info("导航任务已恢复")
        return True

    def stop(self, reason: str = "user_request") -> bool:
        """
        停止导航

        Args:
            reason: 停止原因

        Returns:
            bool: 是否成功停止
        """
        if not self.state.can_transition_to(NavigationState.STOPPED):
            self.logger.warning(f"无法从 {self.state} 转换到 STOPPED")
            return False

        self.state = NavigationState.STOPPED
        self.context.end_time = time.time()

        self._log_event("task_stop", {"reason": reason})

        # 尝试记录状态变化事件
        try:
            from core.tracking import track_event
            track_event(
                "navigation_task",
                "navigation_task_state_change",
                {"state": "STOPPED", "reason": reason}
            )
        except Exception:
            pass

        self.logger.info(f"导航任务已停止，原因: {reason}")
        return True

    def arrived(self) -> bool:
        """
        标记到达目标

        Returns:
            bool: 是否成功标记
        """
        if not self.state.can_transition_to(NavigationState.ARRIVED):
            self.logger.warning(f"无法从 {self.state} 转换到 ARRIVED")
            return False

        self.state = NavigationState.ARRIVED
        self.context.end_time = time.time()

        duration = self.context.get_active_duration()

        self._log_event("task_arrived", {
            "duration": duration,
        })

        # 尝试记录状态变化事件
        try:
            from core.tracking import track_event
            track_event(
                "navigation_task",
                "navigation_task_state_change",
                {"state": "ARRIVED", "duration": duration}
            )
        except Exception:
            pass

        self.logger.info(f"导航任务已完成，到达目标: {self.context.target}")
        return True

    def update(
        self,
        frame: Any,
        walkable_grid: Optional[Any] = None,
        walkable_scores: Optional[Any] = None,
        risk_map: Optional[Any] = None
    ) -> Optional[Dict[str, Any]]:
        """
        每帧更新导航任务

        Args:
            frame: 输入图像帧
            walkable_grid: F6 可走路径网格（可选，向后兼容，如果提供 navigation_engine 则忽略）
            walkable_scores: F6 可走性分数（可选，向后兼容）
            risk_map: F4 风险地图（可选，向后兼容）

        Returns:
            dict | None: 语音事件（如果需要播报），或 None
        """
        # 只在 ACTIVE 状态下处理
        if self.state != NavigationState.ACTIVE:
            return None

        self.context.frame_count += 1

        try:
            # 优先使用 NavigationEngine（F10 新方式）
            if self.engine is not None:
                # 调用 NavigationEngine 处理整帧
                result = self.engine.process_frame(frame)

                if result is None:
                    self.logger.warning("NavigationEngine 处理失败")
                    return None

                nav_decision = result.get("nav_result")
                speech_event = result.get("speech_event")

                if nav_decision:
                    self.context.update_decision(nav_decision)
                if speech_event:
                    self.context.update_speech_event(speech_event)

                # 检测偏航（连续 STOP）
                if nav_decision:
                    decision = nav_decision.get("decision", "")
                    if decision == "STOP":
                        self.consecutive_stops += 1
                        if self.consecutive_stops >= self.max_consecutive_stops:
                            self._handle_reroute()
                    else:
                        self.consecutive_stops = 0

                # 更新上下文
                self.context.last_frame = frame

                # TTS 播报
                if speech_event and self.tts_manager:
                    try:
                        self.tts_manager.speak(speech_event)
                    except Exception as e:
                        self.logger.warning(f"TTS 播报失败: {e}")

                # 日志埋点
                self._log_frame_event(
                    frame_id=self.context.frame_count,
                    nav_decision=nav_decision or {},
                    speech_event=speech_event,
                )

                # 尝试记录任务级日志
                try:
                    from core.tracking import track_event
                    track_event(
                        "navigation_task",
                        "navigation_task_frame",
                        {
                            "frame_id": self.context.frame_count,
                            "state": self.state.value,
                            "nav_decision": nav_decision,
                            "speech_event": speech_event,
                        }
                    )
                except Exception:
                    pass

                return speech_event

            # 向后兼容：使用 Navigator + SpeechManager（F9 旧方式）
            else:
                # Step 1: F7 导航决策
                if self.navigator is None:
                    self.logger.warning("Navigator 未初始化，跳过导航决策")
                    return None

                # 如果提供了 walkable_grid，直接使用；否则需要从 frame 计算（这里简化处理）
                nav_decision = self.navigator.decide(
                    walkable_grid=walkable_grid,
                    walkable_scores=walkable_scores,
                    risk_map=risk_map
                )

                if nav_decision is None:
                    return None

                # 更新上下文
                self.context.update_decision(nav_decision)
                self.context.last_frame = frame

                # Step 2: 检测偏航（连续 STOP）
                decision = nav_decision.get("decision", "")
                if decision == "STOP":
                    self.consecutive_stops += 1
                    if self.consecutive_stops >= self.max_consecutive_stops:
                        self._handle_reroute()
                else:
                    self.consecutive_stops = 0

                # Step 3: F8 语音策略
                speech_event = None
                if self.speech_manager is not None:
                    # 判断是否为危险场景（可根据 risk_map 或其他信息）
                    danger = risk_map is not None and risk_map.max() > 0.6 if hasattr(risk_map, 'max') else False

                    speech_event = self.speech_manager.build_from_nav(
                        nav_decision,
                        danger=danger
                    )

                    if speech_event:
                        self.context.update_speech_event(speech_event)

                # Step 4: 日志埋点
                self._log_frame_event(
                    frame_id=self.context.frame_count,
                    nav_decision=nav_decision,
                    speech_event=speech_event,
                )

                return speech_event

        except Exception as e:
            self.logger.error(f"导航任务更新失败: {e}", exc_info=True)
            self._log_event("task_error", {
                "error": str(e),
                "frame_id": self.context.frame_count,
            })
            return None

    def _handle_reroute(self):
        """
        处理偏航情况

        1.3.0 版本：只提示用户，不重新规划路线
        """
        self.logger.warning("检测到偏航，连续多次 STOP")
        self._log_event("reroute_detected", {
            "consecutive_stops": self.consecutive_stops,
        })

        # 可以在这里触发一个特殊的语音提示
        # 但 1.3.0 不做路线重规划

    def _log_event(self, event_type: str, payload: Dict[str, Any]):
        """
        记录任务级事件

        Args:
            event_type: 事件类型
            payload: 事件数据
        """
        event = {
            "ts": time.time(),
            "task": "navigation",
            "event_type": event_type,
            "state": self.state.value,
            "context": self.context.to_dict(),
        }
        event.update(payload)

        self.event_log.append(event)

        # 也可以发送到后台（这里简化处理）
        if self.logger:
            self.logger.debug(f"[NavTask] {event_type}: {payload}")

    def _log_frame_event(
        self,
        frame_id: int,
        nav_decision: Dict[str, Any],
        speech_event: Optional[Dict[str, Any]],
    ):
        """
        记录帧级事件

        Args:
            frame_id: 帧ID
            nav_decision: 导航决策
            speech_event: 语音事件（可选）
        """
        event = {
            "ts": time.time(),
            "task": "navigation",
            "state": self.state.value,
            "frame_id": frame_id,
            "nav_decision": nav_decision,
            "speech_event": speech_event,
            "position": None,  # 预留 GPS 位置
            "error_code": None,
        }

        self.event_log.append(event)

    def get_state(self) -> NavigationState:
        """
        获取当前状态

        Returns:
            NavigationState: 当前状态
        """
        return self.state

    def get_context(self) -> NavigationContext:
        """
        获取导航上下文

        Returns:
            NavigationContext: 导航上下文
        """
        return self.context

    def get_event_log(self) -> List[Dict[str, Any]]:
        """
        获取事件日志

        Returns:
            List[Dict]: 事件日志列表
        """
        return self.event_log.copy()

    def reset(self):
        """
        重置任务（清除所有状态）
        """
        self.state = NavigationState.IDLE
        self.context = NavigationContext()
        self.event_log = []
        self.consecutive_stops = 0
        self.logger.debug("导航任务已重置")

