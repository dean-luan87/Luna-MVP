#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TC-07: 日志零污染测试

目标：验证 observer_mode=false 时，不得写 observer_* 日志

重点：日志必须完全不污染
任何 observer_* 字段的存在 → FAIL（版本不可存在）
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.v1_8_1.conftest import LogCollector


def test_no_observer_logs_when_disabled(log_collector):
    """
    TC-07: 日志零污染测试
    
    observer_mode=false 时，不得写 observer_* 日志
    
    判定标准：
    - 任何 observer_* 字段的存在 → FAIL
    """
    # 清空日志
    log_collector.clear()
    
    # 运行系统（observer_mode=false）
    # TODO: 实现系统运行逻辑，并收集日志
    # run_system(observer_enabled=False, log_collector=log_collector)
    
    # 获取所有日志
    logs = log_collector.fetch()
    
    # 验证：日志中不存在 observer_* 字段
    assert all("observer_" not in str(log) for log in logs), \
        "observer_mode=false 时，日志中存在 observer_* 字段"


def test_log_format_consistency_when_disabled(log_collector):
    """
    TC-07 扩展：验证日志格式与 v1.8 完全一致
    
    测试范围：
    - 日志字段结构与 v1.8 一致
    - 日志内容格式与 v1.8 一致
    """
    # 清空日志
    log_collector.clear()
    
    # 运行系统（observer_mode=false）
    # TODO: 实现系统运行逻辑
    # run_system(observer_mode=False, log_collector=log_collector)
    
    # 获取所有日志
    logs = log_collector.fetch()
    
    # 验证：日志格式与 v1.8 一致
    # TODO: 实现日志格式对比逻辑
    # v18_logs = get_v18_baseline_logs()
    # assert log_format_matches(logs, v18_logs)


def test_no_observer_log_source_when_disabled(log_collector):
    """
    TC-07 扩展：验证不存在 observer_mode 日志来源
    
    测试范围：
    - 日志来源（source）不应包含 "observer_mode"
    """
    # 清空日志
    log_collector.clear()
    
    # 运行系统（observer_mode=false）
    # TODO: 实现系统运行逻辑
    # run_system(observer_mode=False, log_collector=log_collector)
    
    # 获取所有日志
    logs = log_collector.fetch()
    
    # 验证：不存在 observer_mode 日志来源
    for log in logs:
        if isinstance(log, dict):
            source = log.get("source", "")
            assert source != "observer_mode", \
                f"日志中存在 observer_mode 来源: {log}"


def test_log_metadata_no_observer_fields(log_collector):
    """
    TC-07 扩展：验证日志 metadata 中不存在 observer_* 字段
    
    测试范围：
    - metadata 字段结构与 v1.8 一致
    - 不存在任何 observer_* 字段
    """
    # 清空日志
    log_collector.clear()
    
    # 运行系统（observer_mode=false）
    # TODO: 实现系统运行逻辑
    # run_system(observer_mode=False, log_collector=log_collector)
    
    # 获取所有日志
    logs = log_collector.fetch()
    
    # 验证：metadata 中不存在 observer_* 字段
    observer_fields = [
        "observer_trigger_reason",
        "observer_level",
        "observer_user_response",
        "observer_enabled",
        "observer_bypass_reason",
    ]
    
    for log in logs:
        if isinstance(log, dict):
            metadata = log.get("metadata", {})
            for field in observer_fields:
                assert field not in metadata, \
                    f"日志 metadata 中存在 {field} 字段: {log}"

