"""
导航状态机独立出来 (v1.2.0)
把 "开始 / 暂停 / 恢复 / 取消 / 完成 / 位置更新" 的逻辑，放在一个小 FSM 里
"""

from typing import Optional, Dict, Any, List
import time

from .navigation_state import NavigationStatus, NavRoute, NavStep


class NavigationFSM:
    """
    导航状态机（纯粹处理状态，不做IO、不调TTS、不写日志）
    """
    
    def __init__(self):
        self._status = NavigationStatus()
    
    # ========== 基础状态查询 ==========
    
    @property
    def status(self) -> NavigationStatus:
        """获取当前状态"""
        return self._status
    
    def is_idle(self) -> bool:
        """是否处于空闲状态"""
        return self._status.state == "IDLE"
    
    def is_navigating(self) -> bool:
        """是否正在导航"""
        return self._status.state == "NAVIGATING"
    
    def is_paused(self) -> bool:
        """是否处于暂停状态"""
        return self._status.state == "PAUSED"
    
    def is_completed(self) -> bool:
        """是否已完成"""
        return self._status.state == "COMPLETED"
    
    def is_canceled(self) -> bool:
        """是否已取消"""
        return self._status.state == "CANCELED"
    
    def is_error(self) -> bool:
        """是否处于错误状态"""
        return self._status.state == "ERROR"
    
    # ========== 事件：启动导航 ==========
    
    def start(self, route: NavRoute) -> bool:
        """
        启动导航
        
        Args:
            route: 导航路径
        
        Returns:
            是否成功启动
        """
        if not route or not route.steps:
            return False
        
        if not self.is_idle():
            # 已有导航在进行
            return False
        
        self._status.state = "NAVIGATING"
        self._status.route = route
        self._status.destination = route.destination
        self._status.current_step_index = 0
        self._status.reason = None
        self._status.last_update_ts = time.time()
        return True
    
    # ========== 事件：位置更新（可附带 hazard 信息） ==========
    
    def update_position(self, lat: float, lng: float,
                        hazards: Optional[List[Dict[str, Any]]] = None):
        """
        更新位置
        
        这里只做状态更新/进度推进，不做重规划。
        真正"要不要进下一步"可以后面再加策略模块。
        
        Args:
            lat: 纬度
            lng: 经度
            hazards: 危险信息列表（可选）
        """
        if not self.is_navigating():
            # 非导航状态下，位置更新仅记录时间
            self._status.last_update_ts = time.time()
            return
        
        self._status.extra["last_lat"] = lat
        self._status.extra["last_lng"] = lng
        self._status.last_update_ts = time.time()
        
        if hazards is not None:
            self._status.hazards = hazards
        
        # TODO: 将来可以在这里根据距离/方位推进 current_step_index
        # 先不做复杂逻辑，保证结构干净
    
    # ========== 事件：暂停 / 恢复 / 取消 / 完成 ==========
    
    def pause(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航
        
        Args:
            reason: 暂停原因
        
        Returns:
            是否成功暂停
        """
        if not self.is_navigating():
            return False
        
        self._status.state = "PAUSED"
        self._status.reason = reason
        self._status.last_update_ts = time.time()
        return True
    
    def resume(self) -> bool:
        """
        恢复导航
        
        Returns:
            是否成功恢复
        """
        if self._status.state != "PAUSED":
            return False
        
        self._status.state = "NAVIGATING"
        self._status.reason = None
        self._status.last_update_ts = time.time()
        return True
    
    def cancel(self, reason: str = "用户取消") -> bool:
        """
        取消导航
        
        Args:
            reason: 取消原因
        
        Returns:
            是否成功取消
        """
        if self._status.state not in ("NAVIGATING", "PAUSED"):
            return False
        
        self._status.state = "CANCELED"
        self._status.reason = reason
        self._status.last_update_ts = time.time()
        return True
    
    def complete(self) -> bool:
        """
        完成导航
        
        Returns:
            是否成功完成
        """
        if self._status.state not in ("NAVIGATING", "PAUSED"):
            return False
        
        self._status.state = "COMPLETED"
        self._status.reason = "已到达目的地"
        self._status.last_update_ts = time.time()
        return True
    
    def set_error(self, reason: str = "导航错误") -> bool:
        """
        设置错误状态
        
        Args:
            reason: 错误原因
        
        Returns:
            是否成功设置
        """
        self._status.state = "ERROR"
        self._status.reason = reason
        self._status.last_update_ts = time.time()
        return True
    
    # ========== 内部辅助：构建 NavRoute ==========
    
    @staticmethod
    def build_route(origin: str, destination: str,
                    route_data: Dict[str, Any]) -> NavRoute:
        """
        构建导航路径
        
        route_data 建议直接用 path_planner 的原始输出结构
        
        Args:
            origin: 起点
            destination: 终点
            route_data: 路径数据
        
        Returns:
            导航路径对象
        """
        steps_raw = route_data.get("steps") or route_data.get("segments") or []
        steps: List[NavStep] = []
        
        for idx, raw in enumerate(steps_raw):
            steps.append(
                NavStep(
                    index=idx,
                    instruction=raw.get("instruction") or raw.get("text") or "",
                    distance_m=raw.get("distance_m"),
                    action=raw.get("action"),
                    meta=raw,
                )
            )
        
        return NavRoute(
            origin=origin,
            destination=destination,
            steps=steps,
            raw_data=route_data,
        )



