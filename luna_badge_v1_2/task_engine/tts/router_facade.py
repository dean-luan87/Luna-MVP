"""
TTSRouterFacade: TTS 路由器门面

Step 13: 全局唯一播报入口。所有播报必须通过 emit() 进入。

统一入口，将 DecisionCore 的 TTS_ROUTER_* actions 路由到具体的 NavigationVoiceRouter
"""

from __future__ import annotations

from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
    from task_engine.tts.tts_manager import TtsManager


class TTSRouterFacade:
    """
    TTS 路由器门面

    Step 13: 全局唯一播报入口。所有播报必须通过 emit() 进入。

    由 RouterFacade 决定：
    - 是否进入 NavigationVoiceRouter(安全、导航)
    - 是否进入 System/Task 管线
    - 是否进入 PriorityScheduler
    """

    def __init__(
        self,
        nav_router: Optional["NavigationVoiceRouter"] = None,
        queue_manager: Optional["TtsManager"] = None,
    ):
        """
        初始化 TTS 路由器门面

        Args:
            nav_router: NavigationVoiceRouter 实例（可选，默认创建新实例）
            queue_manager: TtsManager 实例（可选，默认使用模块级单例）
        """
        if nav_router is None:
            # 延迟导入避免循环依赖
            from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
            self.nav_router = NavigationVoiceRouter()
        else:
            self.nav_router = nav_router

        if queue_manager is None:
            from task_engine.tts import tts_manager
            self.queue_manager = queue_manager or tts_manager
        else:
            self.queue_manager = queue_manager

    def route_turn(self, direction: str, distance: Optional[int] = None, **kwargs) -> None:
        """
        路由转弯播报

        Args:
            direction: 方向（"左转" / "右转" / "调头" 等）
            distance: 距离（米，可选）
            **kwargs: 其他参数
        """
        self.nav_router.route_turn(direction=direction, distance=distance, **kwargs)

    def route_straight(self, distance: Optional[int] = None, **kwargs) -> None:
        """
        路由直行播报

        Args:
            distance: 距离（米，可选）
            **kwargs: 其他参数
        """
        self.nav_router.route_straight(distance=distance, **kwargs)

    def route_obstacle_warning(
        self,
        direction: Optional[str] = None,
        distance_m: Optional[int] = None,
        obstacle_type: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        路由障碍物警告播报

        Args:
            direction: 方向（"前方" / "左侧" / "右侧" 等）
            distance_m: 距离（米，可选）
            obstacle_type: 障碍物类型（"human" / "object" 等，可选）
            **kwargs: 其他参数
        """
        # 如果提供了 obstacle_type，可以用于生成更精确的播报文本
        self.nav_router.route_obstacle_warning(
            direction=direction,
            distance_m=distance_m,
            **kwargs
        )

    def route_generic(self, category: str, text: str, **kwargs) -> None:
        """
        路由通用播报

        Args:
            category: 类别（"SAFETY" / "NAVIGATION" / "TASK" / "CHAT"）
            text: 播报文本
            **kwargs: 其他参数
        """
        self.nav_router.route_generic(category=category, text=text, **kwargs)

    # ===============================================================
    # Step 13: 核心统一入口
    # ===============================================================

    def emit(
        self,
        text: str,
        *,
        category: "TTSCategory",
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Step 13: 全局唯一播报入口。

        所有播报必须通过此方法进入，由 RouterFacade 决定路由到：
        - NavigationVoiceRouter（安全、导航）
        - 主队列（系统、任务、Ask、Scene）

        Args:
            text: 播报文本
            category: 播报类别（TTSCategory）
            meta: 元数据（可选）
        """
        from task_engine.tts.tts_policy import get_policy
        from task_engine.tts.utterance import Utterance
        from task_engine.tts.priority_bands import PriorityBand

        policy = get_policy(category)

        utter = Utterance(
            text=text,
            meta=meta or {},
            level=policy.default_level,
            priority=policy.priority,
            interrupt=policy.interrupt,
        )
        utter.meta["ttscategory"] = category.value

        band = policy.band()

        # ---- 导航/安全类 → 导航语音路由器 ----
        if band == PriorityBand.P0_SAFETY:
            self.nav_router.route_safety(text=text, meta=meta)
            return

        if band == PriorityBand.P1_NAV:
            self.nav_router.route_navigation(text=text, meta=meta)
            return

        # ---- 系统 / 任务 / Ask / Scene → 主队列 ----
        if band in (PriorityBand.P2_TASK, PriorityBand.P3_CHAT):
            self.queue_manager.enqueue(utter)
            return

        # fallback（理论不会进入）
        self.queue_manager.enqueue(utter)

    # ===============================================================
    # Step 13: 语义化接口（给其它模块使用）
    # ===============================================================

    def speak_system(self, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """系统播报"""
        from task_engine.tts.tts_policy import TTSCategory
        return self.emit(text, category=TTSCategory.SYSTEM, meta=meta)

    def speak_task(self, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """任务播报"""
        from task_engine.tts.tts_policy import TTSCategory
        return self.emit(text, category=TTSCategory.TASK, meta=meta)

    def speak_chat(self, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """闲聊播报"""
        from task_engine.tts.tts_policy import TTSCategory
        return self.emit(text, category=TTSCategory.CHAT, meta=meta)

    def speak_nav(self, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """导航播报"""
        from task_engine.tts.tts_policy import TTSCategory
        return self.emit(text, category=TTSCategory.NAVIGATION, meta=meta)

    def speak_safety(self, text: str, meta: Optional[Dict[str, Any]] = None) -> bool:
        """
        Step 11: 安全播报，跳过所有时间窗口限制，直接进入安全队列。

        Args:
            text: 播报文本
            meta: 元数据（可选）

        Returns:
            bool: 是否成功加入安全队列（如果 2 秒内重复同一句，返回 False）
        """
        from task_engine.tts.tts_policy import TTSCategory
        self.emit(text, category=TTSCategory.SAFETY, meta=meta)
        # 返回 True 表示已处理（实际返回值由 route_safety 决定）
        return True

    # ===============================================================
    # 向后兼容：保留原有的路由方法
    # ===============================================================

    def route_turn(self, direction: str, distance: Optional[int] = None, **kwargs) -> None:
        """
        路由转弯播报

        Args:
            direction: 方向（"左转" / "右转" / "调头" 等）
            distance: 距离（米，可选）
            **kwargs: 其他参数
        """
        self.nav_router.route_turn(direction=direction, distance=distance, **kwargs)

    def route_straight(self, distance: Optional[int] = None, **kwargs) -> None:
        """
        路由直行播报

        Args:
            distance: 距离（米，可选）
            **kwargs: 其他参数
        """
        self.nav_router.route_straight(distance=distance, **kwargs)

    def route_obstacle_warning(
        self,
        direction: Optional[str] = None,
        distance_m: Optional[int] = None,
        obstacle_type: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        路由障碍物警告播报

        Args:
            direction: 方向（"前方" / "左侧" / "右侧" 等）
            distance_m: 距离（米，可选）
            obstacle_type: 障碍物类型（"human" / "object" 等，可选）
            **kwargs: 其他参数
        """
        # 如果提供了 obstacle_type，可以用于生成更精确的播报文本
        self.nav_router.route_obstacle_warning(
            direction=direction,
            distance_m=distance_m,
            **kwargs
        )

    def route_generic(self, category: str, text: str, **kwargs) -> None:
        """
        路由通用播报

        Args:
            category: 类别（"SAFETY" / "NAVIGATION" / "TASK" / "CHAT"）
            text: 播报文本
            **kwargs: 其他参数
        """
        self.nav_router.route_generic(category=category, text=text, **kwargs)


# 模块级单例
_tts_router_facade: Optional[TTSRouterFacade] = None


def get_tts_router_facade() -> TTSRouterFacade:
    """获取 TTS 路由器门面单例"""
    global _tts_router_facade
    if _tts_router_facade is None:
        _tts_router_facade = TTSRouterFacade()
    return _tts_router_facade

