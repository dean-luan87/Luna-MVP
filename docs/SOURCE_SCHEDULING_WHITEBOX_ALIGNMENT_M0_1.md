# Source Scheduling × Whitebox Alignment M0.1 交付

## 1. 本轮目标

在 `scheduled_source_state` 最小接入（M0）基础上，增强白盒第二层解释力，使其可区分：

- 主链本身问题
- 数据源调度问题
- 两者耦合问题

## 2. 本轮增强

- 调度层新增轻解释字段：
  - `dominant_source_reason_summary`
  - `source_scheduling_event_summaries`
  - `source_scheduling_warning_summary`
- 时间轴增强：
  - `dominant_source_selected`
  - `source_conflict_detected`
  - `priority_override_applied`
  - `dynamic_source_overrode_static_source`
  - `memory_source_overrode_observation`
  - `task_source_became_dominant`
- 结构树摘要增强：
  - `source=...`
  - `source_conflict=...`
  - `source_override=...`
  - `source_t=...`
  - `source_conf=...`
- Console/Viewer/Aggregator 增强：
  - 可读摘要 `scheduled_source_readable_summary`
  - warning 与 event 列表可见

## 3. 主线—白盒—日志同链

- 主线：`scheduled_source_state` 继续由主路径 frame 携带
- 白盒：第二层已从“字段可见”升级为“事件+原因+告警可解释”
- 日志：增强字段与事件进入 frame/JSONL/聚合链可追溯

## 4. 本轮边界

- 不引入复杂调度算法
- 不重写主链行为
- 不实现评分公式与治理深能力

## 5. 结论

白盒第二层已与数据源调度层形成更强同链解释闭环（M0.1）。

