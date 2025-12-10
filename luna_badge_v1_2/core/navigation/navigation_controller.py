#!/usr/bin/env python3
"""
导航控制器完整对接
v1.4.2: 对接 TaskTransitionManager, QueryBus, MultiTargetBuffer, Vision Pipeline
"""
import logging
from typing import Optional, Dict, Any, List

from core.task.multi_target_buffer import MultiTargetBuffer, Target
from core.task.query_bus import QueryBus
from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)

logger = logging.getLogger(__name__)


class NavigationState:
    """
    导航状态
    """
    
    def __init__(self):
        self.distance_to_target: float = 0.0  # 米
        self.at_target: bool = False
        self.stationary_seconds: float = 0.0
        self.instruction: Optional[str] = None
        self.obstacle_distance: Optional[float] = None


class MapAPI:
    """
    地图 API（简化版本）
    实际项目中应该对接真实的地图服务
    """
    
    def update_with_vision(
        self,
        target: Target,
        vision_objects: Dict[str, Any]
    ) -> NavigationState:
        """
        基于视觉结果更新导航状态
        
        Args:
            target: 当前目标
            vision_objects: 视觉检测结果
        
        Returns:
            导航状态
        """
        state = NavigationState()
        
        # TODO: 实际实现应该：
        # 1. 从 GPS/定位系统获取当前位置
        # 2. 计算到目标的距离
        # 3. 基于视觉结果判断是否到达
        # 4. 生成导航指令
        
        # 模拟实现
        obstacles = vision_objects.get("objects", [])
        if obstacles:
            # 计算最近障碍物距离
            state.obstacle_distance = 2.0  # 简化：从视觉结果提取
        
        # 模拟距离计算
        state.distance_to_target = 5.0  # TODO: 实际计算
        state.at_target = state.distance_to_target < 1.5
        
        # 生成导航指令
        if state.at_target:
            state.instruction = f"已到达 {target.name}"
        elif state.distance_to_target < 5.0:
            state.instruction = f"距离 {target.name} 还有 {state.distance_to_target:.1f} 米"
        else:
            state.instruction = "继续前进"
        
        return state


class NavigationController:
    """
    导航控制器：整合地图、任务转换、多目标、问询
    """
    
    def __init__(
        self,
        map_api: Optional[MapAPI] = None,
        tts: Optional[Any] = None,
        multi_target_buffer: Optional[MultiTargetBuffer] = None,
        query_bus: Optional[QueryBus] = None,
        task_transition: Optional[TaskTransitionManager] = None,
    ):
        """
        初始化导航控制器
        
        Args:
            map_api: 地图 API
            tts: TTS 模块
            multi_target_buffer: 多目标缓存
            query_bus: 问询总线
            task_transition: 任务转换管理器
        """
        self.map_api = map_api or MapAPI()
        self.tts = tts
        self.buffer = multi_target_buffer
        self.query_bus = query_bus
        self.task_transition = task_transition
        
        self.current_target: Optional[Target] = None
        self.navigation_active = False
        self.last_stationary_ts = 0.0
        self.last_position = None
        
        logger.info("[NAV_CONTROLLER] Initialized")
    
    def start(self, target: Optional[Target] = None) -> None:
        """
        启动导航
        
        Args:
            target: 目标（如果为 None 则从 buffer 获取）
        """
        if target:
            self.current_target = target
        elif self.buffer:
            self.current_target = self.buffer.get_current()
            if not self.current_target:
                self.current_target = self.buffer.start()
        
        if self.current_target:
            self.navigation_active = True
            if self.tts:
                self.say(f"开始前往 {self.current_target.name}")
            logger.info(f"[NAV_CONTROLLER] Navigation started: {self.current_target.name}")
        else:
            logger.warning("[NAV_CONTROLLER] No target available, cannot start navigation")
    
    def stop(self) -> None:
        """停止导航"""
        self.navigation_active = False
        if self.tts:
            self.say("导航已停止")
        logger.info("[NAV_CONTROLLER] Navigation stopped")
        self.current_target = None
    
    def step(self, vision_objects: Dict[str, Any]) -> Optional[NavigationState]:
        """
        导航单步处理
        
        Args:
            vision_objects: 视觉检测结果
        
        Returns:
            导航状态，如果导航未激活则返回 None
        """
        if not self.navigation_active or not self.current_target:
            return None
        
        # 1) 基于视觉结果更新导航状态
        nav_state = self.map_api.update_with_vision(
            self.current_target,
            vision_objects
        )
        
        # 2) 更新静止时间
        if self.last_position:
            # TODO: 实际应该比较位置变化
            # 如果位置没变化，增加静止时间
            pass
        else:
            self.last_position = nav_state
        
        # 3) 生成导航提示
        if nav_state.instruction and self.tts:
            self.say(nav_state.instruction)
        
        # 4) 检查是否到达目标
        if nav_state.at_target:
            logger.info(f"[NAV_CONTROLLER] Reached target: {self.current_target.name}")
            self._handle_target_reached()
        
        # 5) 任务转换判断
        if self.task_transition:
            task_ctx = self._build_task_context(nav_state)
            decision = self.task_transition.decide(task_ctx)
            
            if decision == TaskDecision.END:
                logger.info("[NAV_CONTROLLER] Task ended by decision")
                self.stop()
                return nav_state
            
            if decision == TaskDecision.ASK_END:
                # ASK_END 由 QueryBus 处理（已在 TaskTransitionManager 中触发）
                logger.info("[NAV_CONTROLLER] Task end query triggered")
        
        return nav_state
    
    def _build_task_context(self, nav_state: NavigationState) -> TaskContext:
        """构建任务上下文"""
        # TODO: 从实际用户意图模块获取
        user_intent = UserIntentState(
            want_stop=False,
            want_continue=False,
        )
        
        position_state = PositionState(
            at_target=nav_state.at_target,
            distance_to_target=nav_state.distance_to_target,
            stationary_seconds=nav_state.stationary_seconds,
        )
        
        return TaskContext(
            position=position_state,
            intent=user_intent,
        )
    
    def _handle_target_reached(self) -> None:
        """处理目标到达"""
        if not self.buffer:
            # 没有多目标缓存，直接停止
            self.stop()
            return
        
        # 完成当前目标
        next_target = self.buffer.complete_current()
        
        if next_target:
            # 有下一个目标，问询用户
            if self.query_bus:
                query_id = self.query_bus.push_query(
                    f"是否继续前往 {next_target.name}？",
                    priority=10,
                    timeout_seconds=15.0,
                    on_resolved=self._on_next_target_answer,
                    on_timeout=self._on_next_target_timeout,
                )
                logger.info(f"[NAV_CONTROLLER] Pushed next target query: {query_id}")
            else:
                # 没有 QueryBus，直接开始下一个目标
                self.current_target = next_target
        else:
            # 没有下一个目标，停止导航
            self.stop()
    
    def _on_next_target_answer(self, result: Dict[str, Any]) -> None:
        """下一个目标问询的回复处理"""
        answer = result.get("answer", "").lower()
        if answer in ("yes", "是", "继续", "去"):
            next_target = self.buffer.get_current()
            if next_target:
                logger.info(f"[NAV_CONTROLLER] User confirmed next target: {next_target.name}")
                self.current_target = next_target
                self.navigation_active = True
            else:
                logger.warning("[NAV_CONTROLLER] No next target available")
        else:
            logger.info("[NAV_CONTROLLER] User declined next target, stopping navigation")
            self.stop()
    
    def _on_next_target_timeout(self) -> None:
        """下一个目标问询超时处理"""
        logger.warning("[NAV_CONTROLLER] Next target query timeout, assuming continue")
        # 默认继续下一个目标
        next_target = self.buffer.get_current()
        if next_target:
            self.current_target = next_target
            self.navigation_active = True
        else:
            self.stop()
    
    def say(self, text: str) -> None:
        """TTS 播报"""
        if self.tts:
            if hasattr(self.tts, 'speak'):
                self.tts.speak(text)
            elif hasattr(self.tts, 'say'):
                self.tts.say(text)
            logger.info(f"[NAV_CONTROLLER] TTS: {text}")
    
    def get_state(self) -> Dict[str, Any]:
        """获取导航状态"""
        return {
            "active": self.navigation_active,
            "current_target": self.current_target.name if self.current_target else None,
            "has_next_target": self.buffer.get_next() is not None if self.buffer else False,
        }




