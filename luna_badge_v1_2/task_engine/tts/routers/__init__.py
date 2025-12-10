"""
TTS Routers: 语音路由层

负责在 TTS 播报前进行路由决策，包括：
- 优先级控制
- 时间窗口节流
- 类别过滤

注意：NavigationVoiceRouter 有两个实现：
1. Navigation 层：task_engine/navigation/navigation_voice_router.py（当前 NavigationTask 使用）
2. TTS Routers 层：task_engine/tts/routers/navigation_voice_router.py（推荐新代码使用，本模块）

详见：docs/navigation_voice_router_architecture.md
"""

from .time_window_gate import TimeWindowGate
from .navigation_voice_router import (
    NavigationVoiceRouter as TTSRoutersLayerRouter,
    navigation_voice_router as tts_routers_layer_router,
)

__all__ = [
    "TimeWindowGate",
    # 推荐使用：TTS Routers 层实现
    "TTSRoutersLayerRouter",
    "tts_routers_layer_router",
    # 别名（推荐新代码使用）
    "NavigationVoiceRouter",
    "navigation_voice_router",
]

# 推荐新代码使用的别名
NavigationVoiceRouter = TTSRoutersLayerRouter
navigation_voice_router = tts_routers_layer_router

