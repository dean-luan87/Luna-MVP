#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视觉多模型融合配置（混合模式: 本地优先 + 云端补强）
"""

import os


class VisionFusionConfig:
    """
    视觉多模型融合配置（混合模式: 本地优先 + 云端补强）
    """

    # 是否启用多模型融合总开关
    ENABLE_FUSION = True

    # 是否启用云端视觉（OpenAI 或其他服务）
    ENABLE_CLOUD_VISION = bool(os.getenv("LUNA_ENABLE_CLOUD_VISION", "1") == "1")

    # 本地检测的"足够好"阈值（检测到的有效标签数量 / 置信度）
    MIN_LOCAL_OBJECTS = 2           # 少于 2 个物体时，优先考虑云端补强
    MIN_LOCAL_CONFIDENCE = 0.45     # YOLO 低于这个分数的物体不计入"有效"

    # 云端请求超时时间（秒）
    CLOUD_TIMEOUT_SEC = 12

    # OpenAI 配置（可以按你现有习惯调整）
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    # 使用的视觉模型名（可后续调整）
    CLOUD_VISION_MODEL = os.getenv("LUNA_CLOUD_VISION_MODEL", "gpt-4o-mini")

    # 是否在 /api/navigation/describe_scene 返回融合中间信息（测试环境用）
    DEBUG_RETURN_FUSION_DETAIL = bool(os.getenv("LUNA_DEBUG_VISION_FUSION", "0") == "1")


