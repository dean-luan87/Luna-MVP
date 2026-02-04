# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性验证模块（Robustness Harness）

职责：
- 位置噪声注入
- 极端场景脚本
- Shadow Mode 支持

原则：
- 不改 risk 核心
- 不改 decision
- 不改 speech
- 只"喂数据 + 看日志"
"""

from .noise_position_provider import NoisePositionProvider
from .scenario_runner import Scenario, ScenarioStep, ScenarioLibrary
from .summary_generator import SummaryGenerator, ScenarioSummary, RunSummary
from .fingerprint import calculate_risk_params_fingerprint, get_build_info

__all__ = [
    "NoisePositionProvider",
    "Scenario",
    "ScenarioStep",
    "ScenarioLibrary",
    "SummaryGenerator",
    "ScenarioSummary",
    "RunSummary",
    "calculate_risk_params_fingerprint",
    "get_build_info",
]

