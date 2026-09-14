# -*- coding: utf-8 -*-
"""
v1.8.4: 风险告知服务（RiskAdvisoryService）

职责：
- 每帧更新 registry → engine 计算 → policy 决策 → 返回需要播报的文本
- 确保一次提醒不反复（由 cooldown 保证）
"""

from __future__ import annotations
from typing import Optional, Tuple, List, Dict, Any
import time
import datetime
import logging

from core.risk.risk_registry import RiskRegistry
from core.risk.risk_engine import RiskEngine
from core.risk.warning_policy import WarningPolicy
from core.risk.hazard_evaluator import HazardEvaluator
from core.risk.dynamic_evaluator import is_active, apply_hazard_modifier
from core.risk.risk_debug import RiskDebugSnapshot, RiskObjectSnapshot

# v1.8.5 Phase A: Scene Modeling Layer（可选导入，避免循环依赖）
try:
    from core.scene.scene_registry import SceneRegistry
    from core.scene.scene_read_adapter import get_scene_for_risk
    SCENE_AVAILABLE = True
except ImportError:
    SCENE_AVAILABLE = False

logger = logging.getLogger(__name__)

XY = Tuple[float, float]


class RiskAdvisoryService:
    """
    风险告知服务
    
    核心流程：
    1. 清理过期风险对象
    2. 遍历所有风险对象，计算 RiskLevel
    3. 检测态势上升（ΔRisk）
    4. 判断是否触发警告
    5. 更新状态机
    """
    
    def __init__(
        self,
        registry: RiskRegistry,
        risk_engine: Optional[RiskEngine] = None,
        warning_policy: Optional[WarningPolicy] = None,
        hazard_evaluator: Optional[HazardEvaluator] = None,
        enable_debug: bool = False,
        scene_registry: Optional[Any] = None  # v1.8.5 Phase A: Scene Registry（可选）
    ) -> None:
        """
        初始化风险告知服务
        
        Args:
            registry: 风险对象注册表
            risk_engine: 风险引擎（如果为 None 则创建默认实例）
            warning_policy: 警告策略（如果为 None 则创建默认实例）
            hazard_evaluator: 危险评估器（如果为 None 则创建默认实例）
            enable_debug: 是否启用调试快照（默认 False）
            scene_registry: 场景注册表（v1.8.5 Phase A，可选）
        """
        self.registry = registry
        self.risk_engine = risk_engine or RiskEngine(trend_eps=0.25)
        self.warning_policy = warning_policy or WarningPolicy()
        self.hazard_evaluator = hazard_evaluator or HazardEvaluator()
        self.enable_debug = enable_debug
        self.scene_registry = scene_registry  # v1.8.5: Scene Registry
        self._last_debug_snapshot: Optional[RiskDebugSnapshot] = None
    
    def tick(self, user_xy: XY, ts: Optional[float] = None) -> Optional[str]:
        """
        每帧更新风险评估，返回需要播报的文本（若无触发则返回 None）
        
        Args:
            user_xy: 用户位置 (x, y)（局部坐标，单位米）
            ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Optional[str]: 需要播报的文本（如果无触发则返回 None）
        """
        if ts is None:
            ts = time.time()
        
        # 清理过期对象
        self.registry.cleanup_expired(ts)
        
        # === v1.8.4: 调试快照收集（如果启用） ===
        snapshots: List[RiskObjectSnapshot] = []
        advisory_text: Optional[str] = None
        
        # 遍历所有风险对象
        now_dt = datetime.datetime.fromtimestamp(ts)
        
        for risk_object in self.registry.get_all():
            try:
                # === v1.8.4: 动态区域激活判断（关键点） ===
                active = is_active(risk_object, now_dt)
                # 记录动态激活状态（用于调试）
                risk_object.runtime.is_dynamic_active = active
                risk_object.runtime.last_dynamic_check_ts = ts
                
                if not active:
                    # 未激活的动态区域：根据配置决定是否完全忽略
                    if risk_object.dynamic_profile and risk_object.dynamic_profile.ignore_when_inactive:
                        # 完全不参与 risk 计算，跳过本次循环
                        # 但如果是调试模式，需要记录快照
                        if self.enable_debug:
                            snapshots.append(
                                RiskObjectSnapshot(
                                    risk_id=risk_object.risk_id,
                                    risk_type=risk_object.risk_type,
                                    dynamic_active=False,
                                    hazard_level=risk_object.hazard_level,
                                    distance_m=None,
                                    trend="STABLE",
                                    risk_level=0.0,
                                    delta_risk=0.0,
                                    state=risk_object.runtime.state,
                                    reason="dynamic_inactive"
                                )
                            )
                        continue
                    else:
                        # 不忽略但也不计算 RiskLevel，保持 last_risk_level = 0.0
                        risk_object.runtime.last_risk_level = 0.0
                        if self.enable_debug:
                            snapshots.append(
                                RiskObjectSnapshot(
                                    risk_id=risk_object.risk_id,
                                    risk_type=risk_object.risk_type,
                                    dynamic_active=False,
                                    hazard_level=risk_object.hazard_level,
                                    distance_m=None,
                                    trend="STABLE",
                                    risk_level=0.0,
                                    delta_risk=0.0,
                                    state=risk_object.runtime.state,
                                    reason="dynamic_inactive_but_not_ignored"
                                )
                            )
                        continue
                
                # === v1.8.4: hazard 评估 + 动态修正 ===
                # 先评估基础 hazard
                base_hazard = self.hazard_evaluator.evaluate_hazard(risk_object)
                risk_object.hazard_level = base_hazard
                # 再应用动态修正
                risk_object.hazard_level = apply_hazard_modifier(risk_object)
                
                # 1) 计算当前 RiskLevel 和距离
                current_risk_level, distance_m = self.risk_engine.calculate_risk_level(
                    risk_object, user_xy
                )
                
                # 2) 计算趋势（基于距离变化）
                prev_dist = risk_object.runtime.edge_distance_m
                trend = self.risk_engine.calc_trend(prev_dist, distance_m)
                
                # 3) 计算 ΔRisk（必须在更新 last_risk_level 之前）
                last_risk = risk_object.runtime.last_risk_level
                delta_risk = current_risk_level - last_risk
                
                # 4) 判断是否应该触发警告（ΔRisk 上升触发 + cooldown）
                # 注意：必须在 update_runtime 之前判断，否则 last_risk_level 会被更新
                if self.risk_engine.should_warn(risk_object, current_risk_level, ts):
                    # 生成警告文本
                    advisory_text = self.warning_policy.generate_advisory_text(risk_object)
                    
                    # 更新状态机（进入 COOLDOWN）
                    self.risk_engine.update_state(risk_object, warned=True, now_ts=ts)
                    
                    # 更新注册表
                    self.registry.update(risk_object.risk_id, risk_object)
                    
                    # 记录日志
                    delta_risk = current_risk_level - risk_object.runtime.last_risk_level
                    logger.info(
                        f"[RiskAdvisory] 触发警告: risk_id={risk_object.risk_id}, "
                        f"type={risk_object.risk_type}, text={advisory_text}, "
                        f"risk_level={current_risk_level:.3f}, delta={delta_risk:.3f}, "
                        f"distance={distance_m:.2f}m, trend={trend}"
                    )
                    
                    # === v1.8.4: 调试快照收集（触发警告的对象） ===
                    if self.enable_debug:
                        snapshots.append(
                            RiskObjectSnapshot(
                                risk_id=risk_object.risk_id,
                                risk_type=risk_object.risk_type,
                                dynamic_active=risk_object.runtime.is_dynamic_active,
                                hazard_level=risk_object.hazard_level,
                                distance_m=distance_m,
                                trend=trend,
                                risk_level=current_risk_level,
                                delta_risk=delta_risk,
                                state=risk_object.runtime.state,
                            )
                        )
                        # 生成调试快照并返回
                        # v1.8.5 Phase A: 添加场景信息（只读，不参与判断）
                        scene_info = self._get_scene_info()
                        # v1.8.5 Phase B: 添加场景注册表状态（只读，不参与判断）
                        scene_registry_info = self._get_scene_registry_info()
                        self._last_debug_snapshot = RiskDebugSnapshot(
                            ts=ts,
                            user_xy=user_xy,
                            objects=snapshots,
                            advisory_triggered=True,
                            advisory_text=advisory_text,
                            scene=scene_info,  # v1.8.5 Phase A: 场景信息（只读）
                            scene_registry=scene_registry_info,  # v1.8.5 Phase B: 场景注册表状态（只读）
                        )
                    
                    return advisory_text
                else:
                    # 未触发警告，但仍需更新状态机（检查 cooldown 是否结束）
                    self.risk_engine.update_state(risk_object, warned=False, now_ts=ts)
                
                # 5) 更新运行时状态（距离、趋势、RiskLevel）
                # 注意：必须在 should_warn 判断之后更新，否则 delta 计算会出错
                risk_object.update_runtime(
                    current_risk_level, distance_m, trend, ts
                )
                
                # 6) 更新注册表
                self.registry.update(risk_object.risk_id, risk_object)
                
                # === v1.8.4: 调试快照收集（未触发警告的对象） ===
                if self.enable_debug:
                    snapshots.append(
                        RiskObjectSnapshot(
                            risk_id=risk_object.risk_id,
                            risk_type=risk_object.risk_type,
                            dynamic_active=risk_object.runtime.is_dynamic_active,
                            hazard_level=risk_object.hazard_level,
                            distance_m=distance_m,
                            trend=trend,
                            risk_level=current_risk_level,
                            delta_risk=delta_risk,
                            state=risk_object.runtime.state,
                        )
                    )
            
            except Exception as e:
                logger.error(
                    f"[RiskAdvisory] 处理风险对象失败: risk_id={risk_object.risk_id}, error={e}",
                    exc_info=True
                )
                continue
        
        # === v1.8.4: 生成调试快照（如果启用且未触发警告） ===
        if self.enable_debug:
            # v1.8.5 Phase A: 添加场景信息（只读，不参与判断）
            scene_info = self._get_scene_info()
            # v1.8.5 Phase B: 添加场景注册表状态（只读，不参与判断）
            scene_registry_info = self._get_scene_registry_info()
            self._last_debug_snapshot = RiskDebugSnapshot(
                ts=ts,
                user_xy=user_xy,
                objects=snapshots,
                advisory_triggered=False,
                advisory_text=None,
                scene=scene_info,  # v1.8.5 Phase A: 场景信息（只读）
                scene_registry=scene_registry_info,  # v1.8.5 Phase B: 场景注册表状态（只读）
            )
        
        return None
    
    def _get_scene_info(self) -> Optional[Dict[str, Any]]:
        """
        获取场景信息（v1.8.5 Phase A）
        
        从 Scene Registry 获取当前场景，并提取只读摘要信息。
        如果 Scene Registry 未就绪，返回 None。
        
        Returns:
            Optional[Dict[str, Any]]: 场景信息摘要（scene_id / scene_type / confidence）
        """
        if not SCENE_AVAILABLE or not self.scene_registry:
            return None
        
        try:
            current_scene = self.scene_registry.get_current_scene()
            return {
                "scene_id": current_scene.scene_id,
                "scene_type": current_scene.scene_type,
                "confidence": current_scene.confidence,
            }
        except Exception:
            # 如果 Scene Registry 未就绪，允许为空
            return None
    
    def _get_scene_registry_info(self) -> Optional[Dict[str, Any]]:
        """
        获取场景注册表状态（v1.8.5 Phase B）
        
        从 Scene Registry 获取状态机状态，包括 Active 和 Candidate。
        如果 Scene Registry 未就绪，返回 None。
        
        Returns:
            Optional[Dict[str, Any]]: 场景注册表状态（active_scene_id / active_confidence / candidate_scene_id / candidate_confidence）
        """
        if not SCENE_AVAILABLE or not self.scene_registry:
            return None
        
        try:
            active = self.scene_registry.get_active_scene()
            candidate = self.scene_registry.get_candidate_scene()
            
            return {
                "active_scene_id": active.scene_id if active else None,
                "active_confidence": active.confidence if active else None,
                "candidate_scene_id": candidate.scene_id if candidate else None,
                "candidate_confidence": candidate.confidence if candidate else None,
            }
        except Exception:
            # 如果 Scene Registry 未就绪，允许为空
            return None
    
    def get_last_debug_snapshot(self) -> Optional[RiskDebugSnapshot]:
        """
        获取最后一次调试快照
        
        Returns:
            Optional[RiskDebugSnapshot]: 最后一次调试快照，如果未启用调试或未调用过 tick() 则返回 None
        """
        return self._last_debug_snapshot
    
    def get_current_risk_bias(self) -> Optional[Any]:
        """
        v1.8.5 Phase C 包 A：返回当前 Scene/区域的综合风险偏置
        
        不触发播报、不影响状态机，只读方法。
        
        内部逻辑（一期极简）：
        - 取最近一帧 RiskLevel 最大的对象
        - 若 < ε（如 0.1）→ None
        - 否则返回 RiskBias
        
        Returns:
            Optional[RiskBias]: 风险偏置，如果无风险或未调用过 tick() 则返回 None
        """
        # 导入 RiskBias（避免循环依赖）
        from core.task_chain.types import RiskBias
        
        if not self._last_debug_snapshot:
            return None
        
        # 取最近一帧 RiskLevel 最大的对象
        max_item = None
        max_risk_level = 0.0
        
        for obj_snapshot in self._last_debug_snapshot.objects:
            # 跳过未激活的动态区域
            if obj_snapshot.dynamic_active is False:
                continue
            
            # 跳过未参与计算的对象
            if obj_snapshot.reason:
                continue
            
            if obj_snapshot.risk_level > max_risk_level:
                max_risk_level = obj_snapshot.risk_level
                max_item = obj_snapshot
        
        # 若 < ε（0.1）→ None
        if not max_item or max_risk_level < 0.1:
            return None
        
        # 返回 RiskBias
        return RiskBias(
            risk_level=max_risk_level,
            dominant_type=max_item.risk_type,
            source="risk_module",
        )

