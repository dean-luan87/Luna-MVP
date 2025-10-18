#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Navigation 模块
语音导航和路径规划功能
"""

__version__ = "1.0.0"
__author__ = "Luna Team"

# 延迟导入，避免依赖问题
def get_voice_navigator():
    """获取语音导航器"""
    from .voice_navigator import VoiceNavigator
    return VoiceNavigator

def get_route_planner():
    """获取路径规划器"""
    from .route_planner import RoutePlanner
    return RoutePlanner

# 直接导入基础模块（无额外依赖）
try:
    from .voice_navigator import VoiceNavigator
except ImportError:
    VoiceNavigator = None

try:
    from .route_planner import RoutePlanner
except ImportError:
    RoutePlanner = None

__all__ = [
    'VoiceNavigator',
    'RoutePlanner',
    'get_voice_navigator',
    'get_route_planner'
]
