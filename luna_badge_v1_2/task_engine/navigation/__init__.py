"""
Navigation Module: 导航模块

提供导航相关的语音适配和工具函数。

注意：NavigationVoiceRouter 有两个实现：
1. Navigation 层：task_engine/navigation/navigation_voice_router.py（当前 NavigationTask 使用）
2. TTS Routers 层：task_engine/tts/routers/navigation_voice_router.py（推荐新代码使用）

详见：docs/navigation_voice_router_architecture.md
"""

from .navigation_voice_adapter import NavigationVoiceAdapter, navigation_voice
from .nav_phrase_mapper import NavPhraseMapper, nav_phrase_mapper
from .nav_event_post_processor import NavigationEventPostProcessor, nav_event_post_processor
from .navigation_voice_router import (
    NavigationVoiceRouter as NavigationLayerRouter,
    navigation_voice_router as navigation_layer_router,
)
from .navigation_scheduler import (
    NavigationScheduler,
    TurnEvent,
    StraightEvent,
    ObstacleEvent,
)

__all__ = [
    "NavigationVoiceAdapter",
    "navigation_voice",
    "NavPhraseMapper",
    "nav_phrase_mapper",
    "NavigationEventPostProcessor",
    "nav_event_post_processor",
    # 向后兼容：保留旧名称
    "NavigationLayerRouter",
    "navigation_layer_router",
    # 别名（向后兼容）
    "NavigationVoiceRouter",
    "navigation_voice_router",
    # Step 10: NavigationScheduler
    "NavigationScheduler",
    "TurnEvent",
    "StraightEvent",
    "ObstacleEvent",
]

# 向后兼容别名
NavigationVoiceRouter = NavigationLayerRouter
navigation_voice_router = navigation_layer_router

