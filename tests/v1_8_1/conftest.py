#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.8.1 自动化测试配置

统一控制开关和测试工具
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock


class SystemRunner:
    """
    系统运行器（Mock / Stub / Real Runner）
    
    用于运行系统并收集结果
    """
    
    def __init__(self):
        self.config = {}
        self.outputs = []
        self.task_flow = []
    
    def set_config(self, **kwargs):
        """设置配置"""
        self.config.update(kwargs)
    
    def run_baseline_v18(self) -> Dict[str, Any]:
        """
        运行 v1.8 基线版本
        
        Returns:
            Dict[str, Any]: 包含 outputs 和 task_flow
        """
        # TODO: 实现 v1.8 基线运行逻辑
        # 这里应该是真实的 v1.8 系统运行
        return {
            "outputs": self.outputs,
            "task_flow": self.task_flow,
            "version": "v1.8"
        }
    
    def run_current(self) -> Dict[str, Any]:
        """
        运行当前版本（v1.8.1）
        
        Returns:
            Dict[str, Any]: 包含 outputs 和 task_flow
        """
        # TODO: 实现 v1.8.1 运行逻辑
        # 这里应该是真实的 v1.8.1 系统运行
        return {
            "outputs": self.outputs,
            "task_flow": self.task_flow,
            "version": "v1.8.1",
            "observer_mode_enabled": self.config.get("OBSERVER_MODE_ENABLED", False)
        }


class LogCollector:
    """
    日志收集器
    
    用于收集和分析日志
    """
    
    def __init__(self):
        self.logs = []
    
    def clear(self):
        """清空日志"""
        self.logs = []
    
    def collect(self, log: Dict[str, Any]):
        """收集日志"""
        self.logs.append(log)
    
    def fetch(self) -> List[Dict[str, Any]]:
        """获取所有日志"""
        return self.logs
    
    def has_observer_fields(self) -> bool:
        """检查是否存在 observer_* 字段"""
        for log in self.logs:
            if isinstance(log, dict):
                # 检查 metadata 中是否有 observer_* 字段
                metadata = log.get("metadata", {})
                if any(key.startswith("observer_") for key in metadata.keys()):
                    return True
                # 检查日志内容中是否有 observer_* 字段
                content = str(log.get("content", ""))
                if "observer_" in content.lower():
                    return True
        return False


@pytest.fixture
def system_runner():
    """
    系统运行器 Fixture
    
    用于测试中运行系统
    """
    return SystemRunner()


@pytest.fixture
def log_collector():
    """
    日志收集器 Fixture
    
    用于测试中收集日志
    """
    return LogCollector()


@pytest.fixture
def observer_mode_enabled():
    """
    Observer Mode 启用状态 Fixture
    
    默认返回 False（测试回滚等价性）
    """
    return False


@pytest.fixture
def observer_mode_disabled():
    """
    Observer Mode 禁用状态 Fixture
    
    用于测试回滚等价性
    """
    return False


