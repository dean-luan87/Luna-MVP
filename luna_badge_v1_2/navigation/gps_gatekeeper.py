"""
GPS Gatekeeper (v1.4.8 StepB-1)

GPS 门控：决定当前 GPS 处于哪种工作模式

核心职责：
- 决定当前 GPS 处于哪种工作模式
- 输出给系统的是"GPS 使用权限"，不是坐标

全局设计约束：
1. 视角为主，GPS 为辅
2. 室内场景：GPS 关闭
3. 距离 ≤ 50m：GPS 仅验证，不得影响主权
4. 距离 > 50m 且室外：GPS 才允许参与
5. 任何模块不得直接"使用 GPS 坐标作为最终位置"
"""

from enum import Enum
from typing import Optional


class GPSMode(Enum):
    """GPS 工作模式"""
    OFF = "off"                # 完全关闭（室内）
    VERIFY_ONLY = "verify"     # 仅用于验证（≤50m）
    ACTIVE = "active"          # 可参与融合（>50m）


class GPSGatekeeper:
    """
    GPS 门控器
    
    职责：
    - 决定 GPS 当前的使用模式
    - 基于场景和距离输出 GPSMode
    """
    
    def __init__(self, event_bus=None):
        """
        初始化 GPS 门控器
        
        Args:
            event_bus: 事件总线（可选）
        """
        self.event_bus = event_bus
        self._current_mode: Optional[GPSMode] = None
        self._distance_threshold_m = 50.0  # 50m 阈值
    
    def resolve_mode(
        self,
        scene: str,
        distance_to_target_m: float
    ) -> GPSMode:
        """
        决定 GPS 当前的使用模式
        
        决策规则（硬编码，不可配置）：
        - if scene == "indoor": GPSMode.OFF
        - elif scene == "outdoor":
            - if distance_to_target_m <= 50: GPSMode.VERIFY_ONLY
            - else: GPSMode.ACTIVE
        - elif scene == "transition": GPSMode.VERIFY_ONLY
        
        Args:
            scene: 场景类型（"indoor" / "outdoor" / "transition"）
            distance_to_target_m: 到目标距离（米）
            
        Returns:
            GPSMode: GPS 工作模式
        """
        # 决策规则
        if scene == "indoor":
            mode = GPSMode.OFF
        elif scene == "outdoor":
            if distance_to_target_m <= self._distance_threshold_m:
                mode = GPSMode.VERIFY_ONLY
            else:
                mode = GPSMode.ACTIVE
        elif scene == "transition":
            mode = GPSMode.VERIFY_ONLY
        else:
            # 默认保守策略
            mode = GPSMode.VERIFY_ONLY
        
        # 如果模式发生变化，发布事件
        if self._current_mode != mode:
            self._current_mode = mode
            self._publish_mode_changed(mode, scene, distance_to_target_m)
        
        return mode
    
    def _publish_mode_changed(
        self,
        mode: GPSMode,
        scene: str,
        distance_m: float
    ) -> None:
        """
        发布 GPS 模式变化事件
        
        Args:
            mode: GPS 模式
            scene: 场景类型
            distance_m: 到目标距离（米）
        """
        if self.event_bus:
            self.event_bus.publish(
                "nav.gps.mode.changed",
                {
                    "mode": mode,
                    "scene": scene,
                    "distance_m": distance_m
                }
            )
        else:
            # 如果没有 event_bus，至少打印日志
            print(
                f"[GPS_GATEKEEPER] mode={mode.value} scene={scene} distance={distance_m:.1f}m"
            )
    
    def get_current_mode(self) -> Optional[GPSMode]:
        """获取当前 GPS 模式"""
        return self._current_mode






