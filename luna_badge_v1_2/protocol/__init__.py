#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 协议层（Protocol Layer）

版本: 1.0.0
用途: 统一前后端数据格式验证和转换
"""

__version__ = "1.0.0"

from .framespec import FrameSpec
from .inferspec import InferSpec
from .heartbeatspec import HeartbeatSpec
from .perflogspec import PerfLogSpec
from .errorspec import ErrorSpec

__all__ = [
    "FrameSpec",
    "InferSpec",
    "HeartbeatSpec",
    "PerfLogSpec",
    "ErrorSpec",
    "__version__",
]


