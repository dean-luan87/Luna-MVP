# Scheduled Source State 最小接入 M0 交付

## 1. 目标

把 `scheduled_source_state` 以最小闭环接入 **主链 → 白盒 → 日志**，不做复杂调度算法。

## 2. 本轮接入

- 新增：`decision_monitor/information_source_scheduler.py`
- 主链：`DecisionMonitorBuilder` 在 frame 形成后生成 `scheduled_source_state`
- 白盒：
  - 结构树摘要追加 `source=<dominant_source>`
  - 时间轴追加事件 `scheduled_source_state_formed`
  - Console/Viewer 展示最小调度摘要
- 日志：
  - `scheduled_source_state` 落入 frame/JSONL
  - aggregator 暴露 `scheduled_dominant_source`、冲突摘要、覆盖摘要
  - `runtime/context.py` 预留调度摘要字段

## 3. 最小结构

- `participating_sources`
- `dominant_source`
- `source_conflict_summary`
- `priority_override_summary`
- `timeliness_pressure`
- `source_confidence_summary`
- `scheduled_source_state_applied`

## 4. 本轮边界

- 仅做最小显式化与可观察化
- 不实现复杂优先级引擎、可信度学习、多模型调度

## 5. 验收结论

`scheduled_source_state` 已进入主链 frame，白盒可见，日志可落地，形成 M0 最小同链闭环。

