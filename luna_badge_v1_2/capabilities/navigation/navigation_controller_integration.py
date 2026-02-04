#!/usr/bin/env python3
"""
导航控制器集成点
v1.4.2: 整合 TaskTransitionManager, QueryBus, MultiTargetBuffer, SafeMode
"""
import logging
from typing import Optional, Dict, Any

from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)
from core.task.query_bus import QueryBus
from core.task.multi_target_buffer import MultiTargetBuffer, Target
from core.system.safe_mode import SafeModeManager

logger = logging.getLogger(__name__)


class NavigationControllerIntegration:
    """
    导航控制器集成：整合任务转换、问询、多目标、安全模式
    """
    
    def __init__(
        self,
        task_transition: Optional[TaskTransitionManager] = None,
        query_bus: Optional[QueryBus] = None,
        multi_target_buffer: Optional[MultiTargetBuffer] = None,
        safe_mode: Optional[SafeModeManager] = None,
    ):
        """
        初始化导航控制器集成
        
        Args:
            task_transition: 任务转换管理器
            query_bus: 问询总线
            multi_target_buffer: 多目标缓存
            safe_mode: 安全模式管理器
        """
        self.task_transition = task_transition
        self.query_bus = query_bus
        self.multi_target_buffer = multi_target_buffer
        self.safe_mode = safe_mode
        
        # 导航状态
        self.navigation_active = False
        self.current_target: Optional[Target] = None
        
        logger.info("[NAV_CONTROLLER] Initialized")
    
    def step(
        self,
        objects: Dict[str, Any],
        position_state: Optional[PositionState] = None,
        user_intent: Optional[UserIntentState] = None,
        obstacle_distance: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        导航单步处理
        
        Args:
            objects: 视觉检测结果
            position_state: 位置状态
            user_intent: 用户意图
            obstacle_distance: 障碍物距离
        
        Returns:
            导航决策结果
        """
        # 1. 检查安全模式
        if self.safe_mode and self.safe_mode.is_active():
            logger.debug("[NAV_CONTROLLER] Safe mode active, skipping navigation")
            if obstacle_distance is not None:
                from core.system.safe_mode import SafeModeContext
                ctx = SafeModeContext(obstacle_distance=obstacle_distance)
                self.safe_mode.handle_frame(ctx)
            return {
                "action": "safe_mode",
                "navigation_active": False,
            }
        
        # 2. 如果没有位置状态，使用默认值
        if position_state is None:
            position_state = PositionState(
                at_target=False,
                distance_to_target=10.0,
                stationary_seconds=0.0,
            )
        
        # 3. 如果没有用户意图，使用默认值
        if user_intent is None:
            user_intent = UserIntentState(
                want_stop=False,
                want_continue=False,
            )
        
        # 4. 任务转换判断
        if self.task_transition:
            task_ctx = TaskContext(
                position=position_state,
                intent=user_intent,
            )
            decision = self.task_transition.decide(task_ctx)
            
            if decision == TaskDecision.END:
                logger.info("[NAV_CONTROLLER] Task ended by user")
                self.navigation_active = False
                return {
                    "action": "stop",
                    "navigation_active": False,
                    "reason": "user_requested",
                }
            
            if decision == TaskDecision.ASK_END:
                logger.info("[NAV_CONTROLLER] Asking user if task should end")
                # ASK_END 由 QueryBus 处理，这里只记录
                return {
                    "action": "ask_end",
                    "navigation_active": True,
                }
        
        # 5. 正常导航逻辑（KEEP）
        return {
            "action": "continue",
            "navigation_active": True,
        }
    
    def handle_target_complete(self) -> Optional[Target]:
        """
        处理目标完成
        
        Returns:
            下一个目标，如果没有则返回 None
        """
        if not self.multi_target_buffer:
            logger.warning("[NAV_CONTROLLER] MultiTargetBuffer not available")
            return None
        
        # 完成当前目标
        next_target = self.multi_target_buffer.complete_current()
        
        if next_target:
            logger.info(f"[NAV_CONTROLLER] Target completed, next: {next_target.name}")
            
            # 问询用户是否继续下一个目标
            if self.query_bus:
                query_id = self.query_bus.push_query(
                    f"是否继续前往 {next_target.name}？",
                    priority=8,
                    timeout_seconds=15.0,
                    on_resolved=self._on_next_target_answer,
                    on_timeout=self._on_next_target_timeout,
                )
                logger.info(f"[NAV_CONTROLLER] Pushed next target query: {query_id}")
        else:
            logger.info("[NAV_CONTROLLER] All targets completed")
            self.navigation_active = False
        
        return next_target
    
    def _on_next_target_answer(self, result: Dict[str, Any]) -> None:
        """下一个目标问询的回复处理"""
        answer = result.get("answer", "").lower()
        if answer in ("yes", "是", "继续", "去"):
            next_target = self.multi_target_buffer.get_current()
            if next_target:
                logger.info(f"[NAV_CONTROLLER] User confirmed next target: {next_target.name}")
                self.current_target = next_target
                self.navigation_active = True
            else:
                logger.warning("[NAV_CONTROLLER] No next target available")
        else:
            logger.info("[NAV_CONTROLLER] User declined next target, going idle")
            self.navigation_active = False
    
    def _on_next_target_timeout(self) -> None:
        """下一个目标问询超时处理"""
        logger.warning("[NAV_CONTROLLER] Next target query timeout, assuming continue")
        # 默认继续下一个目标
        next_target = self.multi_target_buffer.get_current()
        if next_target:
            self.current_target = next_target
            self.navigation_active = True
    
    def stop(self) -> None:
        """停止导航"""
        self.navigation_active = False
        logger.info("[NAV_CONTROLLER] Navigation stopped")
    
    def start(self, target: Optional[Target] = None) -> None:
        """启动导航"""
        if target:
            self.current_target = target
        elif self.multi_target_buffer:
            self.current_target = self.multi_target_buffer.get_current()
        
        if self.current_target:
            self.navigation_active = True
            logger.info(f"[NAV_CONTROLLER] Navigation started: {self.current_target.name}")
        else:
            logger.warning("[NAV_CONTROLLER] No target available, cannot start navigation")












