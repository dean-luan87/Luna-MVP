"""
导航管理器 v3.0 (v1.2.0)
集成策略引擎，正式接管导航逻辑
"""

from typing import Dict, Any, Optional, List
from .navigation_context import NavigationContext
from .strategy_engine import StrategyEngine
from .strategy_loader import load_all_strategies

# 导入视觉导航子策略
from .strategies.base import FrameContext, StrategyRegistry
from .strategies.low_light import LowLightStrategy
from .strategies.reflective_surface import ReflectiveSurfaceStrategy
from .strategies.shadow import ShadowStrategy
from .strategies.multi_light import MultiLightStrategy
from .strategies.water_reflection import WaterReflectionStrategy
from .strategies.backlight import BacklightStrategy
from .strategies.dark_zone import DarkZoneStrategy

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class NavigationManager:
    """
    导航管理器（策略引擎集成版）
    
    负责：
    - 管理导航上下文（NavigationContext）
    - 加载和执行策略引擎（StrategyEngine）
    - 提供统一的导航接口
    """
    
    def __init__(self, log_manager=None, path_planner=None):
        """
        初始化导航管理器
        
        Args:
            log_manager: 日志管理器实例（可选）
            path_planner: 路径规划器实例（可选，用于多目标规划）
        """
        # 创建导航上下文
        self.context = NavigationContext()
        
        # 加载策略（按优先级排序，传入path_planner用于多目标规划）
        strategies = load_all_strategies(self.context, base_planner=path_planner)
        
        # 创建策略引擎
        self.engine = StrategyEngine(
            context=self.context,
            strategies=strategies
        )
        
        # 初始化视觉导航子策略注册器
        self._visual_strategy_registry = StrategyRegistry()
        self._register_visual_strategies()
        
        self.log_manager = log_manager
        self.path_planner = path_planner
    
    def update_observation(self, obs: Dict[str, Any]):
        """
        更新观察数据（从外部环境获取的信息）
        
        obs = {
            "position": {"lat": 31.23, "lng": 121.47},
            "heading": 90.0,
            "hazards": [...],
            "construction": False,
            "people_density": 0.3,
            "traffic_light_state": "GREEN",
            "vision": {...},
            "navigation_raw": {...},
            ...
        }
        
        Args:
            obs: 观察数据字典
        """
        # 更新GPS信息
        if "position" in obs:
            pos = obs["position"]
            if isinstance(pos, dict):
                self.context.update_from_gps(
                    lat=pos.get("lat", 0.0),
                    lng=pos.get("lng", 0.0),
                    heading=obs.get("heading")
                )
            elif isinstance(pos, (list, tuple)) and len(pos) >= 2:
                self.context.update_from_gps(
                    lat=float(pos[0]),
                    lng=float(pos[1]),
                    heading=obs.get("heading")
                )
        
        # 更新视觉数据
        if "vision" in obs:
            self.context.update_from_vision(obs["vision"])
        
        # 更新导航原始数据
        if "navigation_raw" in obs:
            self.context.update_from_navigation_raw(obs["navigation_raw"])
        
        # 更新其他属性
        for k, v in obs.items():
            if k in ["position", "vision", "navigation_raw"]:
                continue  # 已处理
            
            if hasattr(self.context, k):
                # 直接设置属性
                setattr(self.context, k, v)
    
    def run_step(self) -> Dict[str, Any]:
        """
        执行一次策略调度 → 返回行为dict
        
        Returns:
            策略执行结果字典，包含action, text, strategy等
        """
        system_log = _get_logger()
        system_log("NAV:RUN_STEP", {
            "context": self.context.to_dict()
        })
        
        # 执行策略引擎
        result = self.engine.run()
        
        # 记录日志（如果log_manager存在）
        if self.log_manager and hasattr(self.log_manager, 'log_navigation'):
            try:
                self.log_manager.log_navigation(
                    action="strategy_executed",
                    destination=self.context.current_step.get("destination") if self.context.current_step else None,
                    path_info=None,
                    system_response=result.get("text", ""),
                    metadata={
                        "strategy": result.get("strategy"),
                        "action": result.get("action"),
                        "result": result,
                    },
                )
            except Exception:
                pass
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取导航状态
        
        Returns:
            导航状态字典
        """
        return {
            "context": self.context.to_dict(),
            "current_strategy": self.engine.last_executed_strategy,
            "state": self.context.current_step,
        }
    
    def _register_visual_strategies(self):
        """
        注册所有默认启用的视觉导航策略（A-G）。
        """
        self._visual_strategy_registry.register(LowLightStrategy())
        self._visual_strategy_registry.register(ReflectiveSurfaceStrategy())
        self._visual_strategy_registry.register(ShadowStrategy())
        self._visual_strategy_registry.register(MultiLightStrategy())
        self._visual_strategy_registry.register(WaterReflectionStrategy())
        self._visual_strategy_registry.register(BacklightStrategy())
        self._visual_strategy_registry.register(DarkZoneStrategy())
    
    def analyze_frame_for_guidance(
        self,
        image_np: Any,
        detections: List[Dict[str, Any]],
        ocr_results: List[Dict[str, Any]],
        env_meta: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        统一的视觉导航策略入口：
        
        返回一个 list，里面是每个策略给出的 guidance：
        {
            "message": "...",
            "severity": "warning",
            "code": "NAV_STRAT_LOW_LIGHT",
            "extra": {...}
        }
        
        Args:
            image_np: 图像numpy数组
            detections: YOLO检测结果
            ocr_results: OCR识别结果
            env_meta: 环境元信息（可选）
        
        Returns:
            策略结果列表
        """
        ctx = FrameContext(
            image_np=image_np,
            detections=detections or [],
            ocr_results=ocr_results or [],
            env_meta=env_meta or {},
        )
        strategy_results = self._visual_strategy_registry.analyze(ctx)
        
        # 记录日志 & 转成API友好格式
        guidance_list: List[Dict[str, Any]] = []
        for res in strategy_results:
            guidance_list.append(
                {
                    "message": res.message,
                    "severity": res.severity,
                    "code": res.code,
                    "extra": res.extra,
                }
            )
            
            # 记录日志
            if self.log_manager:
                try:
                    if hasattr(self.log_manager, 'log_navigation'):
                        self.log_manager.log_navigation(
                            action="vision_strategy",
                            destination=None,
                            path_info=None,
                            system_response=res.message,
                            metadata={
                                "severity": res.severity,
                                "code": res.code,
                                "extra": res.extra,
                            },
                        )
                except Exception:
                    pass
        
        return guidance_list
    
    def reset(self):
        """
        重置导航管理器（清空上下文和策略状态）
        """
        self.context = NavigationContext()
        strategies = load_all_strategies(self.context, base_planner=self.path_planner)
        self.engine = StrategyEngine(
            context=self.context,
            strategies=strategies
        )
    
    def start_navigation(self, destination: str, route_segments: Optional[List] = None) -> bool:
        """
        启动导航（兼容旧接口）
        
        Args:
            destination: 目的地
            route_segments: 路径段列表（可选）
        
        Returns:
            是否成功启动
        """
        # 更新上下文
        self.context.current_step = "navigating"
        self.context.target_zone = destination
        
        return True
    
    def pause_navigation(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航（兼容旧接口）
        
        Args:
            reason: 暂停原因
        
        Returns:
            是否成功暂停
        """
        self.context.current_step = "paused"
        return True
    
    def resume_navigation(self) -> bool:
        """
        恢复导航（兼容旧接口）
        
        Returns:
            是否成功恢复
        """
        self.context.current_step = "navigating"
        return True
    
    def cancel_navigation(self, reason: str = "用户取消") -> bool:
        """
        取消导航（兼容旧接口）
        
        Args:
            reason: 取消原因
        
        Returns:
            是否成功取消
        """
        self.context.current_step = "idle"
        return True
    
    def complete_navigation(self) -> bool:
        """
        完成导航（兼容旧接口）
        
        Returns:
            是否成功完成
        """
        self.context.current_step = "completed"
        return True

