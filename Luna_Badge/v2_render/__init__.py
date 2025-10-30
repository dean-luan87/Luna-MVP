"""
v2_render: 插画式情绪地图渲染模块
负责地图视觉表现和情绪叙事注入
"""

from .emotion_map_renderer import EmotionMapRenderer
from .emotion_story_injector import EmotionStoryInjector

__all__ = ['EmotionMapRenderer', 'EmotionStoryInjector']

