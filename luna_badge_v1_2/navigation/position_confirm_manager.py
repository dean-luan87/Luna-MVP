"""
Position Confirm Manager (v1.4.8 StepB-3)

位置确认管理器：核心协调器

StepB-3 的唯一使命：
在关键时刻，回答一句话：
"我确信你现在就在你以为你在的地方。"
"""

from typing import Optional, Dict, Any, List
import time
from navigation.landmark_observation import LandmarkObservation, LandmarkType
from navigation.landmark_matcher import LandmarkMatcher, LocalMapLandmarkNode, LandmarkMatchResult


class PositionConfirmManager:
    """
    位置确认管理器
    
    职责：
    - 监听视觉地标观测
    - 与 LocalMap 匹配
    - 在关键时刻发布位置确认事件
    
    核心约束：
    - 不做定位，只做确认
    - 不生成当前位置坐标
    - 不接管 PositionAuthority
    - 不影响 FSM 状态
    - 只发布"位置已被确认"的证据事件
    """
    
    def __init__(
        self,
        event_bus=None,
        logger=None,
        min_confirm_confidence: float = 0.7
    ):
        """
        初始化位置确认管理器
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            min_confirm_confidence: 最小确认置信度（默认 0.7）
        """
        self.event_bus = event_bus
        self.logger = logger
        self.min_confirm_confidence = min_confirm_confidence
        
        # 初始化匹配器
        self.matcher = LandmarkMatcher(min_match_score=0.6)
        
        # 状态缓存
        self._current_fsm_state: Optional[str] = None
        self._local_map_nodes: List[LocalMapLandmarkNode] = []
        self._current_route_step: Optional[Dict[str, Any]] = None
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            # 监听视觉地标观测
            self.event_bus.subscribe("vision.landmark.observed", self._on_landmark_observed)
            
            # 可选：监听 FSM 状态变化
            self.event_bus.subscribe("nav.fsm.state.changed", self._on_fsm_state_changed)
            
            # 可选：监听 LocalMap 更新
            self.event_bus.subscribe("nav.local_map.updated", self._on_local_map_updated)
    
    def _on_landmark_observed(self, observation: LandmarkObservation) -> None:
        """处理视觉地标观测事件"""
        # 检查是否满足确认触发条件
        if not self._should_attempt_confirm(observation):
            return
        
        # 尝试确认
        self._attempt_confirm(observation)
    
    def _on_fsm_state_changed(self, event: Dict[str, Any]) -> None:
        """处理 FSM 状态变化事件"""
        self._current_fsm_state = event.get("state")
    
    def _on_local_map_updated(self, event: Dict[str, Any]) -> None:
        """处理 LocalMap 更新事件"""
        # 提取地标节点（简化版，实际应从 LocalMap 数据结构中提取）
        nodes = event.get("nodes", [])
        self._local_map_nodes = [
            LocalMapLandmarkNode(
                node_id=node.get("node_id", ""),
                landmark_type=LandmarkType(node.get("landmark_type", "crosswalk")),
                direction_hint=node.get("direction_hint")
            )
            for node in nodes
            if node.get("kind") == "LANDMARK"
        ]
    
    def _should_attempt_confirm(self, observation: LandmarkObservation) -> bool:
        """
        检查是否应该尝试确认
        
        确认触发条件（硬规则）：
        - 当前 FSM 状态 ∈ {PRE_TURN, TURNING, POST_TURN}
        - 或 landmark_type ∈ {INTERSECTION, CROSSWALK, ENTRANCE}
        
        Args:
            observation: 视觉观测
            
        Returns:
            bool: 是否应该尝试确认
        """
        # 检查 FSM 状态
        critical_fsm_states = {"PRE_TURN", "TURNING", "POST_TURN"}
        if self._current_fsm_state in critical_fsm_states:
            return True
        
        # 检查地标类型
        critical_landmark_types = {
            LandmarkType.INTERSECTION,
            LandmarkType.CROSSWALK,
            LandmarkType.ENTRANCE
        }
        if observation.landmark_type in critical_landmark_types:
            return True
        
        return False
    
    def _attempt_confirm(self, observation: LandmarkObservation) -> None:
        """
        尝试位置确认
        
        置信度融合规则（第一版，写死）：
        - vision + local_map: ≥ 0.9
        - vision + route_hint: ~ 0.7
        - vision only: ~ 0.5
        - 无匹配: 不发布
        
        Args:
            observation: 视觉观测
        """
        # 与 LocalMap 匹配
        match_result = self.matcher.match(observation, self._local_map_nodes)
        
        # 计算融合置信度
        confidence = 0.0
        sources = []
        matched_node = None
        
        if match_result.matched:
            # vision + local_map
            confidence = 0.9
            sources = ["vision", "local_map"]
            matched_node = match_result.node_id
        elif self._current_route_step:
            # vision + route_hint
            confidence = 0.7
            sources = ["vision", "route_hint"]
        else:
            # vision only
            confidence = 0.5
            sources = ["vision"]
        
        # 检查是否达到最小置信度
        if confidence < self.min_confirm_confidence:
            return
        
        # 发布确认事件（⚠️ 严禁发布 confirmed=False）
        self._publish_confirm(
            confidence=confidence,
            sources=sources,
            landmark_id=matched_node,
            observation=observation,
            match_result=match_result
        )
    
    def _publish_confirm(
        self,
        confidence: float,
        sources: List[str],
        landmark_id: Optional[str],
        observation: LandmarkObservation,
        match_result: LandmarkMatchResult
    ) -> None:
        """
        发布位置确认事件
        
        Args:
            confidence: 置信度
            sources: 证据来源列表
            landmark_id: 匹配的地标节点 ID
            observation: 视觉观测
            match_result: 匹配结果
        """
        event_data = {
            "confirmed": True,
            "confidence": confidence,
            "source": sources,
            "landmark_id": landmark_id,
            "evidence": {
                "vision": {
                    "landmark_type": observation.landmark_type.value,
                    "confidence": observation.confidence,
                    "direction_hint": observation.direction_hint,
                    "frame_id": observation.frame_id
                },
                "local_map": {
                    "matched": match_result.matched,
                    "score": match_result.score,
                    "node_id": match_result.node_id
                } if match_result.matched else None
            }
        }
        
        if self.event_bus:
            self.event_bus.publish("nav.position.confirmed", event_data)
        
        # 日志输出
        self._log_confirm(
            landmark_type=observation.landmark_type.value,
            node_id=landmark_id,
            confidence=confidence,
            sources="+".join(sources)
        )
    
    def _log_confirm(
        self,
        landmark_type: str,
        node_id: Optional[str],
        confidence: float,
        sources: str
    ) -> None:
        """
        记录确认日志
        
        Args:
            landmark_type: 地标类型
            node_id: 节点 ID
            confidence: 置信度
            sources: 证据来源
        """
        log_msg = (
            f"[PositionConfirm] "
            f"landmark={landmark_type} "
            f"node_id={node_id or 'N/A'} "
            f"confidence={confidence:.2f} "
            f"sources={sources}"
        )
        
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("PositionConfirmManager", "position_confirmed", {
                    "landmark_type": landmark_type,
                    "node_id": node_id,
                    "confidence": confidence,
                    "sources": sources
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)






