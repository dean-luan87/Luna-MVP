# Reasoning Timeline View M0（推理时间轴视图 M0）交付

## 1. 定位（写死）

- **结构树**：表达分支、假设、排除、收敛关系
- **时间轴**：表达先后顺序、关键转折、状态切换

两者是并列视角，不互相替代。时间轴只消费现有主线结果，不重算主逻辑。

本轮 M0 只做事件顺序层：用 `event_index` 表达逻辑顺序，不做复杂时间系统/动画/回放器。

## 2. 交付件

- 实现：`decision_monitor/reasoning_timeline_view.py`
- frame 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `reasoning_timeline_view`）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`（结构树附近 Timeline 区块）
- 单测：`tests/test_reasoning_timeline_view.py`
- smoke：`tools/smoke_reasoning_timeline_view.py`（生成 `logs/smoke_reasoning_timeline_view_*.jsonl`）

## 3. 数据结构

### ReasoningTimelineEvent

- event_index
- event_type
- event_summary
- event_source_module
- event_importance（high/medium/low）
- related_node_id（可空）
- related_issue_type（可空）
- related_quality_flag（可空）

### ReasoningTimelineViewResult

- events（按逻辑顺序）
- key_transition_count
- key_transition_summary（1~3 个关键转折）
- timeline_applied

## 4. 最小事件类型（M0）

- flow_entered
- hypothesis_selected
- path_switched
- feedback_received
- issue_detected
- quality_changed
- fallback_triggered
- optimization_hint_generated
- validation_result_changed
- continuity_changed
- resolution_updated
- **context_premise_recorded**（Environment & Task Context Reserve M0：builder 在生成 `environment_task_context_reserve` 后追加一条「一句话前提」事件；实现见 `append_context_premise_event`）

## 5. 抽取与排序规则（M0）

事件默认来自主线字段（flow/hypothesis/metrics/quality/recheck/feedback/optimization/continuity/resolution），按固定逻辑顺序生成：

1) flow_entered → 2) hypothesis_selected → 3) path_switched → 4) feedback_received → 5) continuity_changed →  
6) issue_detected → 7) fallback_triggered → 8) quality_changed → 9) optimization_hint_generated →  
10) validation_result_changed → 11) resolution_updated  
12)（可选）context_premise_recorded：由 builder 在 timeline 初算完成后追加，不插入到上述固定序的中间。

## 6. Console 接入（写死）

在 **Reasoning Structure Tree** 附近新增轻量 Timeline 区块，展示：

- key_transition_count / key_transition_summary
- 事件列表（纵向文本即可；高重要事件通过 importance 字段可读）

不做独立时间线页面，不做动画与复杂交互回放。

## 7. CONTRACT 强约束（写死）

推理过程的“结构视角”与“时间视角”应并列存在：结构树负责表达分支与收敛关系，时间轴负责表达事件先后与关键转折。后续相关能力应优先接入这两条统一视角，而不是另起平行展示体系。

## 8. 结论（M0）

时间轴视图已接入 frame/JSONL/Console，并能从既有主线结果抽取 4~10 条关键事件序列与转折摘要，为后续“定位转折点/卡点”提供统一时间视角。

