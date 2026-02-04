#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试 & 场景描述相关配置
"""

import os


class AutoTestConfig:
    """
    自动化测试 & 场景描述相关配置
    """

    # 场景描述 API 基地址（默认本机 9001）
    SCENE_DESC_API_BASE_URL = os.getenv(
        "SCENE_DESC_API_BASE_URL",
        "http://localhost:9001"
    )

    # 场景描述接口路径
    SCENE_DESC_API_PATH = "/api/navigation/describe_scene"

    # HTTP 请求超时时间（秒）
    HTTP_TIMEOUT = float(os.getenv("AUTO_TEST_HTTP_TIMEOUT", "10"))

    # 视频抽帧步长：每多少帧取一帧
    VIDEO_FRAME_STEP = int(os.getenv("AUTO_TEST_VIDEO_FRAME_STEP", "10"))

    # 视频最多抽取多少帧
    VIDEO_MAX_FRAMES = int(os.getenv("AUTO_TEST_VIDEO_MAX_FRAMES", "30"))


