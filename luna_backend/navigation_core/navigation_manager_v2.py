"""
导航管理器 v2.0 (v1.2.0)
负责：
- 启动 / 暂停 / 恢复 / 取消 / 完成 导航
- 根据环境信息调用策略体系，生成下一步动作
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List
from core.response_builder import ResponseBuilder
from navigation_strategies.strategy_selector import StrategySelector
from config.error_codes_v2 import ErrorCode


@dataclass
class NavigationStatus:
    """导航状态"""
    state: str = "IDLE"  # IDLE / NAVIGATING / PAUSED / COMPLETED / CANCELLED
    destination: Optional[str] = None
    route_segments: Optional[List] = None
    current_step_index: int = 0
    target_room: Optional[str] = None  # 如 305
    last_action: Optional[str] = None
    last_strategy: Optional[str] = None
    last_error: Optional[str] = None


class NavigationManager:
    """
    导航管理器
    
    负责：
    - 启动 / 暂停 / 恢复 / 取消 / 完成 导航
    - 根据环境信息调用策略体系，生成下一步动作
    """
    
    def __init__(self, log_manager=None):
        """
        初始化导航管理器
        
        Args:
            log_manager: 日志管理器实例（可选）
        """
        self._status = NavigationStatus()
        self._selector = StrategySelector()
        self._log_manager = log_manager
    
    # -------- 状态只读接口 --------
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取导航状态
        
        Returns:
            导航状态字典
        """
        return asdict(self._status)
    
    def check_idle(self) -> bool:
        """
        检查是否处于空闲状态
        
        Returns:
            是否空闲
        """
        return self._status.state in ("IDLE", "COMPLETED", "CANCELLED")
    
    # -------- 控制接口 --------
    
    def start_navigation(self, destination: str, route_segments: Optional[List] = None) -> bool:
        """
        启动导航
        
        Args:
            destination: 目的地
            route_segments: 路径段列表（可选）
        
        Returns:
            是否成功启动
        """
        if not self.check_idle():
            return False
        
        self._status = NavigationStatus(
            state="NAVIGATING",
            destination=destination,
            route_segments=route_segments or [],
            current_step_index=0,
        )
        self._log("start_navigation", {"destination": destination})
        return True
    
    def pause_navigation(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航
        
        Args:
            reason: 暂停原因
        
        Returns:
            是否成功暂停
        """
        if self._status.state != "NAVIGATING":
            return False
        
        self._status.state = "PAUSED"
        self._log("pause_navigation", {"reason": reason})
        return True
    
    def resume_navigation(self) -> bool:
        """
        恢复导航
        
        Returns:
            是否成功恢复
        """
        if self._status.state != "PAUSED":
            return False
        
        self._status.state = "NAVIGATING"
        self._log("resume_navigation", {})
        return True
    
    def cancel_navigation(self, reason: str = "用户取消") -> bool:
        """
        取消导航
        
        Args:
            reason: 取消原因
        
        Returns:
            是否成功取消
        """
        if self._status.state not in ("NAVIGATING", "PAUSED"):
            return False
        
        self._status.state = "CANCELLED"
        self._log("cancel_navigation", {"reason": reason})
        return True
    
    def complete_navigation(self) -> bool:
        """
        完成导航
        
        Returns:
            是否成功完成
        """
        if self._status.state not in ("NAVIGATING", "PAUSED"):
            return False
        
        self._status.state = "COMPLETED"
        self._log("complete_navigation", {})
        return True
    
    # -------- 核心：基于策略计算下一步动作 --------
    
    def update_from_environment(self, env: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据环境信息更新导航状态并计算下一步动作
        
        env 由 routes 层组装，例如：
        {
          "gps": {...},
          "vision": {...},
          "hazards": [...],
          "navigation_raw": {...}
        }
        
        Args:
            env: 环境信息字典
        
        Returns:
            响应字典（包含success、data、nav_action等）
        """
        rb = ResponseBuilder()
        
        # 导航未启动时：直接返回当前状态
        if self._status.state not in ("NAVIGATING", "PAUSED"):
            return {
                "success": True,
                "data": {
                    "status": self.get_status(),
                    "nav_action": None,
                }
            }
        
        try:
            strategy = self._selector.select(env)
            self._status.last_strategy = getattr(strategy, "STRATEGY_NAME", strategy.__class__.__name__)
            
            # 状态级控制
            if strategy.should_pause(self._status.__dict__, env):
                self._status.state = "PAUSED"
            
            if strategy.should_reroute(self._status.__dict__, env):
                # 这里只发出 reroute 信号，不在这里做真实路线规划
                nav_action = {
                    "action": "reroute",
                    "description": "需要重新规划路线",
                    "strategy": self._status.last_strategy,
                }
                self._status.last_action = nav_action["action"]
                self._log("nav_reroute", {"env": env})
                
                return {
                    "success": True,
                    "data": {
                        "status": self.get_status(),
                        "nav_action": nav_action,
                    }
                }
            
            # 生成下一步动作
            nav_action = strategy.get_next_action(self._status.__dict__, env) or {}
            nav_action.setdefault("action", "noop")
            nav_action.setdefault("description", "未提供描述")
            nav_action["strategy"] = self._status.last_strategy
            
            self._status.last_action = nav_action["action"]
            
            # 步骤推进（如走廊、地铁换乘等）
            if strategy.should_advance_step(self._status.__dict__, env):
                self._status.current_step_index += 1
            
            # 如果策略认为已完成（检查should_complete方法，如果存在）
            if hasattr(strategy, 'should_complete') and strategy.should_complete(self._status.__dict__, env):
                self._status.state = "COMPLETED"
            
            self._log("nav_step", {"nav_action": nav_action, "env": env})
            
            return {
                "success": True,
                "data": {
                    "status": self.get_status(),
                    "nav_action": nav_action,
                }
            }
        
        except Exception as e:
            self._status.last_error = str(e)
            self._log(
                "nav_strategy_error",
                {"error": str(e), "env": env},
                level="error",
                code=ErrorCode.NAV.STRATEGY_EXEC_ERROR,
            )
            
            return {
                "success": False,
                "error_code": ErrorCode.NAV.STRATEGY_EXEC_ERROR,
                "message": f"导航策略执行异常: {str(e)}",
                "data": {"exception": str(e)}
            }
    
    # -------- 内部日志封装 --------
    
    def _log(self, event: str, metadata: Dict[str, Any], level: str = "info", code: Optional[str] = None):
        """
        记录日志
        
        Args:
            event: 事件名称
            metadata: 元数据
            level: 日志级别
            code: 错误码（可选）
        """
        if not self._log_manager:
            return
        
        try:
            if hasattr(self._log_manager, 'log_navigation'):
                self._log_manager.log_navigation(
                    action=event,
                    destination=self._status.destination,
                    path_info=self._status.route_segments,
                    system_response=f"nav_event:{event}",
                    metadata={
                        "status": self.get_status(),
                        "level": level,
                        "error_code": code,
                        **(metadata or {}),
                    },
                )
            else:
                # 使用utils.logger作为fallback
                from utils.logger import log_navigation
                log_navigation(event.upper(), metadata)
        except Exception:
            # 不让日志错误影响主流程
            pass



