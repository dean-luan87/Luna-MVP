"""
FSM Policy State Store (v1.4.8 StepB-5)

只读证据缓存：订阅 StepB-1~4 的事件，形成证据快照
"""

from typing import Optional, Dict, Any
import time
from navigation.gps_gatekeeper import GPSMode
from navigation.gps_quality_monitor import GPSQuality


class FSMPolicyStateStore:
    """
    FSM 策略状态存储
    
    职责：
    - 订阅 StepB-1~4 的事件
    - 只存最新一份快照（或短窗口）
    - 对外提供 get_snapshot()
    """
    
    def __init__(self, event_bus=None):
        """
        初始化状态存储
        
        Args:
            event_bus: 事件总线（可选）
        """
        self.event_bus = event_bus
        
        # 证据快照
        self._gps_mode: Optional[GPSMode] = None
        self._gps_quality: Optional[GPSQuality] = None
        self._last_position_confirmed: Optional[Dict[str, Any]] = None
        self._map_consistency_score: Optional[float] = None
        self._map_consistency_mismatch: Optional[bool] = None
        self._map_consistency_reasons: list[str] = []
        self._current_scene: Optional[str] = None
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            # StepB-1: GPS 模式变化
            self.event_bus.subscribe("nav.gps.mode.changed", self._on_gps_mode_changed)
            
            # StepB-2: GPS 质量变化
            self.event_bus.subscribe("nav.gps.quality.changed", self._on_gps_quality_changed)
            
            # StepB-3: 位置确认
            self.event_bus.subscribe("nav.position.confirmed", self._on_position_confirmed)
            
            # StepB-4: 地图一致性更新
            self.event_bus.subscribe("nav.map.consistency.updated", self._on_map_consistency_updated)
            
            # 可选：FSM 状态变化
            self.event_bus.subscribe("nav.fsm.state.changed", self._on_fsm_state_changed)
    
    def _on_gps_mode_changed(self, event: Dict[str, Any]) -> None:
        """处理 GPS 模式变化事件"""
        self._gps_mode = event.get("mode")
    
    def _on_gps_quality_changed(self, event: Dict[str, Any]) -> None:
        """处理 GPS 质量变化事件"""
        self._gps_quality = event.get("quality")
    
    def _on_position_confirmed(self, event: Dict[str, Any]) -> None:
        """处理位置确认事件"""
        self._last_position_confirmed = {
            "ts": time.time(),
            "confidence": event.get("confidence", 0.0),
            "landmark_id": event.get("landmark_id"),
            "sources": event.get("source", [])
        }
    
    def _on_map_consistency_updated(self, event: Dict[str, Any]) -> None:
        """处理地图一致性更新事件"""
        self._map_consistency_score = event.get("score")
        self._map_consistency_mismatch = event.get("mismatch", False)
        self._map_consistency_reasons = event.get("reasons", [])
    
    def _on_fsm_state_changed(self, event: Dict[str, Any]) -> None:
        """处理 FSM 状态变化事件（可选）"""
        # 可以用于上下文，但不直接影响策略
        pass
    
    def get_snapshot(self) -> Dict[str, Any]:
        """
        获取证据快照
        
        Returns:
            Dict[str, Any]: 证据快照
        """
        return {
            "gps_mode": self._gps_mode.value if self._gps_mode else None,
            "gps_quality": self._gps_quality.value if self._gps_quality else None,
            "last_position_confirmed": self._last_position_confirmed,
            "map_consistency_score": self._map_consistency_score,
            "map_consistency_mismatch": self._map_consistency_mismatch,
            "map_consistency_reasons": self._map_consistency_reasons.copy(),
            "current_scene": self._current_scene
        }
    
    def set_scene(self, scene: str) -> None:
        """设置当前场景"""
        self._current_scene = scene






