# Luna-2 V1.8.0 版本说明

**版本号**: 1.8.0  
**发布日期**: 2026-02-27  
**版本类型**: Decision Monitor 主线 1.1/1.2 封版

## 版本概述

本版将决策显示器的目标层与后果层由占位升级为基于运行态的规则生成，实现「可看」到「可信」。

## 核心变更

### 目标层真实化（goal_resolver）
- **模块**: `decision_monitor/goal_resolver.py`
- **职责**: 根据当前运行态解析 goal_type、goal_description、subgoal_description、goal_status、goal_switch_reason
- **支持类型**: observe_navigate、hold_for_floor、slow_down_observe、recheck_environment、run_detector_check、run_ocr_check
- **规则优先级**: 守底/escape_hatch → B2 介入 → 子目标(detector/ocr check) → 默认观测导航

### 后果层轻量真实化（consequence_evaluator）
- **模块**: `decision_monitor/consequence_evaluator.py`
- **职责**: 根据决策与输出输出 expected_gain/cost/risk、consequence_confidence、rollback_hint、post_action_check_needed
- **规则分支**: floor_guard 守底、b2_impact、controller 正常采样、sampling_gate 节流跳过

### Builder 接入
- `decision_monitor/builder.py` 使用 `goal_resolver.resolve(ctx)` 与 `consequence_evaluator.evaluate(ctx, decision, outputs)` 替代原占位实现

### 契约与文档
- `decision_monitor/CONTRACT.md` 更新「当前字段来源」表

## 验收

- goal 随运行态变化，不再固定
- consequence 随决策类型变化
- Viewer 顶部一句话与卡片展示真实内容
- `python3 -m pytest tests/test_decision_monitor.py` 全通过

## 约束

未接复杂任务系统、大模型意图、复杂后果模拟；未改 Dynamic Policy / B2 契约。
