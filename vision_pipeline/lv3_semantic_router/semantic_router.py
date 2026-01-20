# -*- coding: utf-8 -*-
"""
LV3: Semantic Router（一级语义调度层）

职责：
- 决定这帧是否必须进入实时链路
- 只做粗分类，不做理解

核心判断问题：
这帧是否"可能影响当前任务的即时决策"？

输出两类：
- navigation_candidate: 需要进入实时链路
- non_navigation_candidate: 可以异步处理

⚠️ 分类阈值随任务态动态变化

本模块禁止做什么：
- ❌ 禁止做深度语义理解
- ❌ 禁止直接调用 LV4.1 或 LV4.2
- ❌ 禁止修改任务态
- ❌ 禁止触发感知重拍
"""

import time
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RouteResult:
    """
    路由结果
    
    字段说明：
    - frame_id: 帧 ID（可选）
    - route: 路由类型（"navigation" | "non_navigation"）
    - priority: 优先级（"high" | "low"）
    - reason: 路由原因（可选）
    """
    frame_id: Optional[str] = None
    route: str = "non_navigation"  # "navigation" | "non_navigation"
    priority: str = "low"  # "high" | "low"
    reason: Optional[str] = None


class SemanticRouter:
    """
    一级语义调度层
    
    核心逻辑：
    - 只做粗分类，不做理解
    - 判断问题只有一个：这帧是否"可能影响当前任务的即时决策"？
    - 分类阈值随任务态动态变化
    
    调度规则：
    - 同步
    - 可被任务态热更新
    - 策略来源只允许：
      - 上层控制中心
      - LV4.1 导航即时反馈
    """
    
    def __init__(
        self,
        navigation_threshold: float = 0.5,  # 导航路由阈值（可动态调整）
    ):
        """
        初始化语义路由器
        
        Args:
            navigation_threshold: 导航路由阈值（默认 0.5）
        """
        self.navigation_threshold = navigation_threshold
        self._task_state: Optional[Dict[str, Any]] = None
    
    def update_task_state(self, task_state: Dict[str, Any]) -> None:
        """
        更新任务态（来自上层控制中心）
        
        Args:
            task_state: 任务态字典，包含：
                - is_navigating: bool（是否在导航）
                - has_danger: bool（是否存在危险态）
                - is_idle: bool（是否空闲）
                - task_type: str（任务类型，可选）
        """
        self._task_state = task_state
    
    def route(
        self,
        frame_id: Optional[str] = None,
        quality_result: Optional[Any] = None,  # QualityResult
        task_state: Optional[Dict[str, Any]] = None,
    ) -> RouteResult:
        """
        路由帧到实时链路或异步链路
        
        Args:
            frame_id: 帧 ID（可选）
            quality_result: 质量评估结果（可选）
            task_state: 任务态（可选，如果提供则覆盖内部状态）
        
        Returns:
            RouteResult: 路由结果
        """
        # 使用提供的 task_state 或内部状态
        current_task_state = task_state or self._task_state or {}
        
        # 如果质量检查未通过，默认路由到 non_navigation（低优先级）
        if quality_result and not quality_result.passed:
            return RouteResult(
                frame_id=frame_id,
                route="non_navigation",
                priority="low",
                reason="quality_check_failed",
            )
        
        # 核心判断：这帧是否"可能影响当前任务的即时决策"？
        is_navigating = current_task_state.get("is_navigating", False)
        has_danger = current_task_state.get("has_danger", False)
        is_idle = current_task_state.get("is_idle", True)
        task_type = current_task_state.get("task_type", "unknown")
        
        # 判断逻辑（可动态调整阈值）
        navigation_score = 0.0
        
        # 1. 如果正在导航，提高导航路由分数
        if is_navigating:
            navigation_score += 0.6
        
        # 2. 如果存在危险，提高导航路由分数
        if has_danger:
            navigation_score += 0.4
        
        # 3. 如果空闲，降低导航路由分数
        if is_idle:
            navigation_score -= 0.3
        
        # 4. 根据任务类型调整（可扩展）
        if task_type in ("navigation", "path_finding", "obstacle_avoidance"):
            navigation_score += 0.3
        
        # 归一化到 [0, 1]
        navigation_score = min(1.0, max(0.0, navigation_score))
        
        # 判断路由
        if navigation_score >= self.navigation_threshold:
            route = "navigation"
            priority = "high" if navigation_score >= 0.7 else "medium"
            reason = f"navigation_score={navigation_score:.2f}"
        else:
            route = "non_navigation"
            priority = "low"
            reason = f"navigation_score={navigation_score:.2f}"
        
        return RouteResult(
            frame_id=frame_id,
            route=route,
            priority=priority,
            reason=reason,
        )

