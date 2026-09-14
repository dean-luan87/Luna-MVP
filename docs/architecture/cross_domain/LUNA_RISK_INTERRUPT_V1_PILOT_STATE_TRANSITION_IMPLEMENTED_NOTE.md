# risk_interrupt_v1 试点回退 telemetry 最小实现（V1）说明

## 补了什么 telemetry（P0）

新增一个专用观测事件类型：**`pilot_state_transition`**，用于记录“试点状态切换发生过”这一运行态治理事实，以便聚合工具可直接统计：

- `level2b_to_level2a`
- `level2a_to_level1`
- `any_to_level0`

最小字段（不扩张）：

- `timestamp`
- `transition`
- `reason`
- `related_request_id`（可选）
- `metadata`（可选，最小开关快照等）

## 为什么这是 P0

如果没有该事件，报告层只能看到“触发/闭合”，但无法知道：

- **是否真的执行过回退**
- **回退发生了几次**
- **回退退到了哪一层**

这会让试点评估长期半盲。该事件把“回退动作发生过”变成机器可统计事实，且不改变任何业务行为。

## 代码落点

- 事件结构：`capabilities/voice/observations/pilot_state_transition_observation.py`
- 发出位置（最小可行）：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - Level2B 链路不闭合时：发出 `level2b_to_level2a`
  - 运维开关触发的 on→off 变化：在主线每轮执行时检测并发出 `level2b_to_level2a` / `level2a_to_level1` / `any_to_level0`

> 说明：目前缺少集中“回退执行器”入口时，采用“检测开关变化并写观测”的最小方式补齐可统计性；这属于观测层补齐，不改变任何行为。

## 怎么验证

```bash
python3 tools/test_risk_interrupt_v1_pilot_state_transition.py
```

覆盖：

- 记录一次 `level2b_to_level2a`
- 记录一次 `level2a_to_level1`
- 记录一次 `any_to_level0`
- `tools/analyze_risk_interrupt_v1_pilot.py` 可直接统计 `fallback_to_level1_count` / `fallback_to_level0_count`

## 哪些还没补（明确）

- P1：cancel+replace 的越界检查字段（`risk_level` / `target_output_category`）已补齐；下一步若要继续增强一致性检查，应优先在 analyzer 侧做更严格的路径级越界报表与阈值规则（不改变试点边界）。

