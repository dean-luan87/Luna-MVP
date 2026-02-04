# -*- coding: utf-8 -*-
"""
LV4.1: Navigation Executor（主线）

职责：
- 保证行走安全与路径正确
- 封装现有导航逻辑（TaskPlanner + RiskAdvisoryService + DecisionController）

设计原则：
- B 阶段不拆逻辑，只做封装
- 内部照旧调用现有模块
- 对外只暴露一个统一接口

本模块禁止做什么：
- ❌ 禁止写世界模型（只读）
- ❌ 禁止调用 LV4.2
- ❌ 禁止修改任务态
- ❌ 禁止触发内容抽取
"""

import time
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
import numpy as np

# v1.8.5 Phase B Step 1.2: YOLODetector 迁移到 NavigationExecutor
from utils.model_interfaces import YOLODetector


@dataclass
class NavigationResult:
    """
    导航执行结果
    
    字段说明：
    - navigation_action: 导航动作（可选）
    - confidence: 置信度（"high" | "medium" | "low"）
    - requires_reobserve: 是否需要重新观察
    - risk_level: 风险等级（可选）
    - advisory_text: 建议文本（可选）
    - objects: YOLO 检测结果（可选，v1.8.5 Phase B Step 2.1 迁移）
    """
    navigation_action: Optional[str] = None
    confidence: str = "medium"  # "high" | "medium" | "low"
    requires_reobserve: bool = False
    risk_level: Optional[float] = None
    advisory_text: Optional[str] = None
    objects: Optional[list] = None  # v1.8.5 Phase B Step 2.1: YOLO 检测结果


class NavigationExecutor:
    """
    导航执行器（主线）
    
    核心逻辑：
    - 导航标识识别
    - 路径判断
    - 危险检测
    - 偏航判断
    
    调度规则：
    - 最高优先级
    - 可抢占其他 LV4 任务
    - 唯一允许请求前端重拍的模块之一
    
    注意：
    - B 阶段不拆逻辑，只做封装
    - 内部调用现有模块（TaskPlanner, RiskAdvisoryService, DecisionController）
    """
    
    def __init__(
        self,
        task_planner=None,  # TaskPlanner 实例（可选）
        risk_advisory_service=None,  # RiskAdvisoryService 实例（可选）
        decision_controller=None,  # DecisionController 实例（可选）
        yolo_detector=None,  # YOLODetector 实例（可选，如果为 None 则创建默认实例）
    ):
        """
        初始化导航执行器
        
        Args:
            task_planner: TaskPlanner 实例（可选）
            risk_advisory_service: RiskAdvisoryService 实例（可选）
            decision_controller: DecisionController 实例（可选）
            yolo_detector: YOLODetector 实例（可选，如果为 None 则创建默认实例）
        """
        self.task_planner = task_planner
        self.risk_advisory_service = risk_advisory_service
        self.decision_controller = decision_controller
        # v1.8.5 Phase B Step 1.2: YOLODetector 迁移到 NavigationExecutor
        self.yolo_detector = yolo_detector or YOLODetector()
    
    def run(
        self,
        frame: np.ndarray,
        context: Dict[str, Any],
        user_position: Optional[Tuple[float, float]] = None,
    ) -> NavigationResult:
        """
        执行导航任务
        
        Args:
            frame: 输入图像帧
            context: 上下文（包含 scene, map_hint, memory_bias, risk_bias 等）
            user_position: 用户位置（可选，用于风险评估）
        
        Returns:
            NavigationResult: 导航执行结果
        """
        # B 阶段：只做封装，不重写逻辑
        # 内部调用现有模块，但对外统一接口
        
        # v1.8.5 Phase B Step 2.1: YOLO 检测迁移到 NavigationExecutor
        objects = None
        if self.yolo_detector:
            try:
                objects = self.yolo_detector.detect(frame)
                
                # B: 用 observation_mode 控制视觉关注范围（ROI / 方向）
                # 不在图像层面裁剪，而是在结果过滤层面
                observation_mode = context.get("observation_mode", "forward")
                if objects and observation_mode:
                    from .observation_filter import filter_objects_by_mode
                    frame_shape = frame.shape if hasattr(frame, 'shape') else None
                    objects = filter_objects_by_mode(
                        objects=objects,
                        observation_mode=observation_mode,
                        frame_shape=frame_shape,
                    )
            except Exception:
                pass  # 静默失败，不阻塞
        
        # 1. 风险评估（如果可用）
        risk_level = None
        advisory_text = None
        if self.risk_advisory_service and user_position:
            try:
                advisory_text = self.risk_advisory_service.tick(
                    user_xy=user_position,
                    ts=time.time(),
                )
                # 获取风险等级
                risk_bias = self.risk_advisory_service.get_current_risk_bias()
                if risk_bias:
                    risk_level = risk_bias.risk_level
            except Exception:
                pass  # 静默失败，不阻塞
        
        # 2. 路径规划（如果可用）
        navigation_action = None
        confidence = "medium"
        if self.task_planner and context.get("paths"):
            try:
                from core.task_chain.types import ContextBundle
                context_bundle = ContextBundle(
                    scene=context.get("scene"),
                    map_hint=context.get("map_hint"),
                    memory_bias=context.get("memory_bias"),
                    risk_bias=context.get("risk_bias"),
                    emotional_context=context.get("emotional_context"),
                )
                chosen_path, score, reasons = self.task_planner.choose_path(
                    paths=context.get("paths"),
                    context=context_bundle,
                )
                navigation_action = chosen_path.path_id
                # 根据评分确定置信度
                if score >= 0.8:
                    confidence = "high"
                elif score >= 0.5:
                    confidence = "medium"
                else:
                    confidence = "low"
            except Exception:
                pass  # 静默失败，不阻塞
        
        # 3. 决策判断（如果可用）
        if self.decision_controller:
            try:
                # 这里可以调用决策控制器，但 B 阶段先简化
                pass
            except Exception:
                pass  # 静默失败，不阻塞
        
        return NavigationResult(
            navigation_action=navigation_action,
            confidence=confidence,
            requires_reobserve=False,  # B 阶段暂不实现重拍逻辑
            risk_level=risk_level,
            advisory_text=advisory_text,
            objects=objects,  # v1.8.5 Phase B Step 2.1: YOLO 检测结果
        )

