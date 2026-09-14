# Experience Governance Whitebox Trace M0（经验治理白盒轨迹 M0）交付

## 1. 定位（写死）

本模块用于**解释**（不改写）：
- `experience_evolution` 的治理结果为何为 watchlist/promotable/blocked/rejected
- repeated/support/confirm/fallback/contradiction/scope 等因素如何影响治理
- 用户反馈是否改变经验沉淀方向（展示层规则解释）

输出遵循统一白盒五块骨架，并提供用户可见解释层；同时要求可挂接到 Reasoning Structure Tree。

## 2. 交付件

- 实现：`decision_monitor/experience_governance_whitebox_trace.py`
- 接入：`decision_monitor/builder.py` + `decision_monitor/schema.py`
- 单测：`tests/test_experience_governance_whitebox_trace.py`

## 3. 白盒结构（统一五块骨架）

- reasoning_steps
- weight_allocation（规则版：repeat/support/confirm/penalty 等）
- exclusion_log（至少 1 条：未采用 outcome）
- interaction_trace（有反馈时）
- result_summary：`whitebox_summary / whitebox_applied`

并提供：
- user_visible_explanation（用户可见解释层）

## 4. 关键解释口径

- **治理 outcome**：复述 evolution_status + evolution_reason + future_use_scope
- **权重拆解**：repeat/support/confirm/contradiction/fallback/risk 等组件
- **排除**：至少排除一个未选择 outcome
- **反馈影响**：反馈影响 confirm/denied/contradiction 的统计口径（M0 解释层）

## 5. 接入结构树（要求）

结构树至少可见：
- governance 节点（以 resolution 节点呈现 outcome）
- governance exclusion 节点（未选择 outcome）
- feedback-driven 标记（有反馈时）

## 6. 结论（M0）

经验治理白盒轨迹已形成可审计输出（骨架+用户可见解释），并能进入结构树形成“成长链”可视化。

