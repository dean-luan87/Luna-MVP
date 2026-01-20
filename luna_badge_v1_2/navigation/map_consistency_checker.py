"""
Map Consistency Checker (v1.4.8 StepB-4)

LocalMap × 路线一致性校验（Consistency Check）

StepB-4 不做导航决策，只做一致性评估

核心职责：
- 评估"当前理解的世界"与"路线预期"是否一致
- 输出 ConsistencyScore + MismatchFlag 作为证据
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from navigation.landmark_observation import LandmarkType


@dataclass
class ConsistencyResult:
    """
    一致性评估结果
    """
    score: float              # 0.0 ~ 1.0
    mismatch: bool
    reasons: List[str]


class MapConsistencyChecker:
    """
    地图一致性检查器
    
    职责：
    - 评估 LocalMap 与路线的一致性
    - 输出一致性分数和失配标志
    
    核心约束：
    - 不改变 FSM
    - 不修正路线
    - 不发布控制指令
    - 只评估并输出证据
    """
    
    def __init__(
        self,
        event_bus=None,
        logger=None,
        mismatch_threshold: float = 0.6,
        distance_error_window_pct: float = 0.2,
        distance_error_window_m: float = 10.0
    ):
        """
        初始化一致性检查器
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            mismatch_threshold: 失配阈值（默认 0.6）
            distance_error_window_pct: 距离误差窗百分比（默认 0.2 = 20%）
            distance_error_window_m: 距离误差窗绝对值（米，默认 10.0）
        """
        self.event_bus = event_bus
        self.logger = logger
        self.mismatch_threshold = mismatch_threshold
        self.distance_error_window_pct = distance_error_window_pct
        self.distance_error_window_m = distance_error_window_m
        
        # 状态缓存
        self._current_route_step: Optional[Dict[str, Any]] = None
        self._last_confirmed_landmark: Optional[Dict[str, Any]] = None
        self._local_map_nodes: List[Dict[str, Any]] = []
        self._structure_evidence_count: int = 0
        self._last_structure_check_time: Optional[float] = None
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            # 监听位置确认（来自 StepB-3）
            self.event_bus.subscribe("nav.position.confirmed", self._on_position_confirmed)
            
            # 监听路线步进变化
            self.event_bus.subscribe("nav.route.step.changed", self._on_route_step_changed)
            
            # 监听 LocalMap 更新
            self.event_bus.subscribe("nav.local_map.updated", self._on_local_map_updated)
    
    def _on_position_confirmed(self, event: Dict[str, Any]) -> None:
        """处理位置确认事件"""
        self._last_confirmed_landmark = event.get("evidence", {}).get("vision")
        
        # 触发一致性检查
        self._check_consistency()
    
    def _on_route_step_changed(self, event: Dict[str, Any]) -> None:
        """处理路线步进变化事件"""
        self._current_route_step = event
        
        # 重置结构证据计数
        self._structure_evidence_count = 0
        self._last_structure_check_time = event.get("timestamp")
        
        # 触发一致性检查
        self._check_consistency()
    
    def _on_local_map_updated(self, event: Dict[str, Any]) -> None:
        """处理 LocalMap 更新事件"""
        self._local_map_nodes = event.get("nodes", [])
        
        # 触发一致性检查
        self._check_consistency()
    
    def _check_consistency(self) -> None:
        """
        执行一致性检查
        
        一致性维度（3 个）：
        1. 转向一致性（Turn Consistency）
        2. 距离一致性（Distance Consistency）
        3. 结构一致性（Topology Consistency）
        """
        if not self._current_route_step:
            return
        
        # 执行评估
        result = self._evaluate_consistency()
        
        # 发布事件
        self._publish_consistency(result)
    
    def _evaluate_consistency(self) -> ConsistencyResult:
        """
        评估一致性
        
        Returns:
            ConsistencyResult: 一致性评估结果
        """
        scores = []
        reasons = []
        
        # 1. 转向一致性（Turn Consistency）
        turn_score, turn_reasons = self._check_turn_consistency()
        scores.append(turn_score)
        reasons.extend(turn_reasons)
        
        # 2. 距离一致性（Distance Consistency）
        distance_score, distance_reasons = self._check_distance_consistency()
        scores.append(distance_score)
        reasons.extend(distance_reasons)
        
        # 3. 结构一致性（Topology Consistency）
        structure_score, structure_reasons = self._check_structure_consistency()
        scores.append(structure_score)
        reasons.extend(structure_reasons)
        
        # 计算综合分数（简单平均）
        final_score = sum(scores) / len(scores) if scores else 0.0
        
        # Mismatch 判定规则：score < 0.6 → mismatch = True
        mismatch = final_score < self.mismatch_threshold
        
        return ConsistencyResult(
            score=final_score,
            mismatch=mismatch,
            reasons=reasons
        )
    
    def _check_turn_consistency(self) -> tuple[float, List[str]]:
        """
        检查转向一致性
        
        Returns:
            tuple[float, List[str]]: (分数, 原因列表)
        """
        if not self._current_route_step:
            return 0.5, []
        
        expected_turn = self._current_route_step.get("expected_turn")
        if not expected_turn:
            return 0.5, []
        
        # 从 LocalMap 或视觉证据中获取实际转向
        actual_turn = None
        
        # 尝试从最后确认的地标中获取方向提示
        if self._last_confirmed_landmark:
            direction_hint = self._last_confirmed_landmark.get("direction_hint")
            if direction_hint:
                # 简化映射：left -> left, right -> right, forward -> straight
                if direction_hint == "left":
                    actual_turn = "left"
                elif direction_hint == "right":
                    actual_turn = "right"
                elif direction_hint == "forward":
                    actual_turn = "straight"
        
        # 尝试从 LocalMap 节点中获取转向信息
        if not actual_turn:
            for node in self._local_map_nodes:
                if node.get("kind") == "TURN":
                    turn_direction = node.get("direction")
                    if turn_direction:
                        actual_turn = turn_direction.lower()
                        break
        
        if not actual_turn:
            return 0.5, []  # 无证据，返回中性分数
        
        # 比较转向
        if actual_turn == expected_turn.lower():
            return 1.0, []
        else:
            return 0.2, ["turn_mismatch"]
    
    def _check_distance_consistency(self) -> tuple[float, List[str]]:
        """
        检查距离一致性
        
        误差窗：±20% 或 ±10m（取大）
        
        Returns:
            tuple[float, List[str]]: (分数, 原因列表)
        """
        if not self._current_route_step:
            return 0.5, []
        
        expected_distance_m = self._current_route_step.get("expected_distance_m")
        if not expected_distance_m or expected_distance_m <= 0:
            return 0.5, []
        
        # 计算误差窗
        error_window_pct = expected_distance_m * self.distance_error_window_pct
        error_window = max(error_window_pct, self.distance_error_window_m)
        
        # 从最后确认的地标获取距离信息（简化：假设有距离字段）
        actual_distance_m = None
        if self._last_confirmed_landmark:
            # 这里简化处理，实际应从空间参考中获取
            actual_distance_m = self._last_confirmed_landmark.get("distance_m")
        
        if actual_distance_m is None:
            return 0.5, []  # 无证据，返回中性分数
        
        # 计算距离偏差
        distance_diff = abs(actual_distance_m - expected_distance_m)
        
        if distance_diff <= error_window:
            # 在误差窗内
            ratio = 1.0 - (distance_diff / error_window)
            return max(0.5, ratio), []
        else:
            # 超出误差窗
            return 0.3, ["distance_mismatch"]
    
    def _check_structure_consistency(self) -> tuple[float, List[str]]:
        """
        检查结构一致性
        
        是否在"应出现路口/拐点"的时机看到了结构性地标
        若 route 预期拐点但持续无结构证据 → 降分
        
        Returns:
            tuple[float, List[str]]: (分数, 原因列表)
        """
        if not self._current_route_step:
            return 0.5, []
        
        expected_turn = self._current_route_step.get("expected_turn")
        
        # 如果预期是直行，结构一致性检查不适用
        if expected_turn and expected_turn.lower() == "straight":
            return 1.0, []
        
        # 检查是否有结构性地标（路口、拐角等）
        structural_landmarks = {
            LandmarkType.INTERSECTION,
            LandmarkType.TURN_CORNER,
            LandmarkType.CROSSWALK
        }
        
        has_structure = False
        
        # 检查最后确认的地标
        if self._last_confirmed_landmark:
            landmark_type_str = self._last_confirmed_landmark.get("landmark_type")
            if landmark_type_str:
                try:
                    landmark_type = LandmarkType(landmark_type_str)
                    if landmark_type in structural_landmarks:
                        has_structure = True
                        self._structure_evidence_count += 1
                except ValueError:
                    pass
        
        # 检查 LocalMap 节点
        for node in self._local_map_nodes:
            if node.get("kind") in ["TURN", "INTERSECTION"]:
                has_structure = True
                self._structure_evidence_count += 1
                break
        
        if has_structure:
            return 1.0, []
        else:
            # 如果预期有拐点但无结构证据，根据等待时间降分
            if self._structure_evidence_count == 0:
                return 0.4, ["missing_intersection"]
            else:
                return 0.6, []
    
    def _publish_consistency(self, result: ConsistencyResult) -> None:
        """
        发布一致性评估事件
        
        Args:
            result: 一致性评估结果
        """
        event_data = {
            "score": result.score,
            "mismatch": result.mismatch,
            "reasons": result.reasons,
            "evidence": {
                "route_step_id": self._current_route_step.get("step_id") if self._current_route_step else None,
                "local_map_nodes": len(self._local_map_nodes),
                "last_confirmed_landmark": self._last_confirmed_landmark.get("landmark_type") if self._last_confirmed_landmark else None
            }
        }
        
        if self.event_bus:
            self.event_bus.publish("nav.map.consistency.updated", event_data)
        
        # 日志输出
        self._log_consistency(result)
    
    def _log_consistency(self, result: ConsistencyResult) -> None:
        """
        记录一致性评估日志
        
        Args:
            result: 一致性评估结果
        """
        reasons_str = ",".join(result.reasons) if result.reasons else "[]"
        
        log_msg = (
            f"[MapConsistency] "
            f"score={result.score:.2f} "
            f"mismatch={result.mismatch} "
            f"reasons=[{reasons_str}]"
        )
        
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("MapConsistencyChecker", "consistency_updated", {
                    "score": result.score,
                    "mismatch": result.mismatch,
                    "reasons": result.reasons
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)






