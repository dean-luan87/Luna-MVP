"""
导航管理器 (v1.2.0)
对外给 routes 用的 "门面"
FSM 只管状态，Manager 负责：接 path_planner、调 log_manager、将来对接 TTS / 任务链 / Luna 情绪系统
"""

from typing import Optional, Dict, Any, List
from utils.logger import log_navigation
from .navigation_fsm import NavigationFSM
from .navigation_state import NavigationStatus, NavRoute
from navigation_strategies import StrategySelector


class NavigationManager:
    """
    导航管理器
    - 持有 FSM
    - 调用 path_planner 规划路线
    - 做简单的业务规则（禁止重复启动等）
    """
    
    def __init__(self, path_planner=None, log_manager=None):
        """
        初始化导航管理器
        
        Args:
            path_planner: 路径规划器实例
            log_manager: 日志管理器实例
        """
        self.fsm = NavigationFSM()
        self.path_planner = path_planner
        self.log_manager = log_manager
        self.strategy_selector = StrategySelector()  # 策略选择器
    
    # ========== 对外状态 ==========
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取导航状态
        
        Returns:
            导航状态字典
        """
        return self.fsm.status.to_dict()
    
    def is_idle(self) -> bool:
        """
        是否处于空闲状态
        
        Returns:
            是否空闲
        """
        return self.fsm.is_idle()
    
    # ========== 路径规划 ==========
    
    def plan_route(self, start: str, destinations: List[str]) -> Dict[str, Any]:
        """
        规划路径
        
        Args:
            start: 起点
            destinations: 目的地列表
        
        Returns:
            路径规划结果
        
        Raises:
            RuntimeError: 路径规划器未初始化
        """
        if not self.path_planner:
            raise RuntimeError("路径规划器未初始化")
        
        # 你现在 web_test_server 里的逻辑可以直接搬到这里
        result = self.path_planner.plan_route(start, destinations)
        
        # 建议在这里就把 raw route 保留下来
        return result
    
    # ========== 启动导航 ==========
    
    def start_navigation(self, destination: str,
                         route_segments: Optional[Dict[str, Any]] = None) -> bool:
        """
        启动导航
        
        Args:
            destination: 目的地
            route_segments: 预计算的路径段（可选）
        
        Returns:
            是否成功启动
        
        Raises:
            RuntimeError: 路径规划器未初始化
        """
        if route_segments is None:
            # 如果没传预计算路线，可以在这里通过 path_planner 现算
            if not self.path_planner:
                raise RuntimeError("路径规划器未初始化")
            
            route_raw = self.path_planner.plan_route(
                start="当前定位", destinations=[destination]
            )
        else:
            route_raw = route_segments
        
        route = self.fsm.build_route(
            origin=route_raw.get("origin", "当前定位"),
            destination=destination,
            route_data=route_raw,
        )
        
        ok = self.fsm.start(route)
        
        if ok:
            # 记录日志
            log_navigation("START", {
                "destination": destination,
                "route_info": route_raw,
            })
            
            # 如果log_manager存在，也记录
            if self.log_manager:
                try:
                    if hasattr(self.log_manager, 'log_navigation'):
                        self.log_manager.log_navigation(
                            action="start_navigation",
                            destination=destination,
                            path_info=route_raw,
                            system_response=f"导航已启动到 {destination}",
                        )
                except Exception:
                    pass
        
        return ok
    
    # ========== 位置更新 ==========
    
    def update_position(self, lat: float, lng: float,
                        hazards: Optional[List[Dict[str, Any]]] = None,
                        vision_data: Optional[Dict[str, Any]] = None):
        """
        更新位置（支持策略系统）
        
        Args:
            lat: 纬度
            lng: 经度
            hazards: 危险信息列表（可选）
            vision_data: 视觉数据（可选，用于策略选择）
        """
        self.fsm.update_position(lat, lng, hazards)
        
        # 构建环境信息用于策略选择
        env = {
            "vision": vision_data or {},
            "navigation_raw": {
                "lat": lat,
                "lng": lng,
            }
        }
        
        if vision_data:
            env["vision"]["hazards"] = hazards or []
        
        # 获取当前状态
        status_dict = self.fsm.status.to_dict()
        
        # 使用策略选择器获取动作建议
        action = self.strategy_selector.get_next_action(status_dict, env)
        
        # 检查是否需要推进步骤
        if self.strategy_selector.should_advance_step(status_dict, env):
            # TODO: 推进到下一步（需要扩展FSM支持）
            pass
        
        # 检查是否需要重新规划
        if self.strategy_selector.should_reroute(status_dict, env):
            # TODO: 触发重新规划（需要扩展Manager支持）
            log_navigation("REROUTE_SUGGESTED", {"reason": "strategy_suggested"})
        
        # 检查是否需要暂停
        if self.strategy_selector.should_pause(status_dict, env):
            if self.fsm.is_navigating():
                self.fsm.pause("策略建议暂停")
        
        # 记录日志
        log_navigation("UPDATE_POSITION", {
            "lat": lat,
            "lng": lng,
            "hazards_count": len(hazards) if hazards else 0,
            "strategy": self.strategy_selector.get_current_strategy().name() if self.strategy_selector.get_current_strategy() else None,
            "action": action,
        })
        
        # 如果log_manager存在，也记录
        if self.log_manager:
            try:
                if hasattr(self.log_manager, 'log_navigation'):
                    self.log_manager.log_navigation(
                        action="update_position",
                        destination=self.fsm.status.destination,
                        path_info=None,
                        system_response="位置已更新",
                        metadata={
                            "lat": lat,
                            "lng": lng,
                            "hazards_count": len(hazards) if hazards else 0,
                            "strategy": self.strategy_selector.get_current_strategy().name() if self.strategy_selector.get_current_strategy() else None,
                        },
                    )
            except Exception:
                pass
    
    # ========== 控制类操作 ==========
    
    def pause(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航
        
        Args:
            reason: 暂停原因
        
        Returns:
            是否成功暂停
        """
        ok = self.fsm.pause(reason)
        if ok:
            log_navigation("PAUSE", {"reason": reason})
        return ok
    
    def resume(self) -> bool:
        """
        恢复导航
        
        Returns:
            是否成功恢复
        """
        ok = self.fsm.resume()
        if ok:
            log_navigation("RESUME", {})
        return ok
    
    def cancel(self, reason: str = "用户取消") -> bool:
        """
        取消导航
        
        Args:
            reason: 取消原因
        
        Returns:
            是否成功取消
        """
        ok = self.fsm.cancel(reason)
        if ok:
            log_navigation("CANCEL", {"reason": reason})
        return ok
    
    def complete(self) -> bool:
        """
        完成导航
        
        Returns:
            是否成功完成
        """
        ok = self.fsm.complete()
        if ok:
            log_navigation("COMPLETE", {})
        return ok

