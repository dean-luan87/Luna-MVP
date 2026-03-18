# Confirmation Whitebox Trace M0（确认输入白盒轨迹 M0）交付

## 1. 目标与定位

在已通过的：
- Grid Search Whitebox Trace M0
- Recheck Whitebox Trace M0
- Action Hint Whitebox Trace M0
- Confirmation Input Bridge M0

基础上，为 `confirmation_input_bridge` 建立正式白盒轨迹，使系统不仅输出确认结果字段，还能解释：
- 为什么把用户输入映射成该 `confirmation_input_type`
- 为什么 `confirmation_bridge_next_effect` 是这个，而不是别的
- 为什么没映射成其它类型 / 没选其它推进效果
- 当前 flow / search 阶段 / Action Hint 上下文如何影响判断
- 用户可见层如何解释本次判断（短句映射，不直出内部 JSON）

**本轮定位**：不改 Confirmation Input Bridge 主逻辑；不做 NLU 升级；只做白盒化 + 用户可见解释层。

## 2. 核心原则（写死）

- **沿用统一白盒模板**：reasoning_steps / weight_allocation / exclusion_log / interaction_trace / whitebox_summary+whitebox_applied
- **同时解释映射与推进**：type 映射原因 + next_effect 选择原因
- **用户可见解释层必须存在**：不得直出内部 weight JSON
- **结果与过程并存**：不替代 `confirmation_input_bridge` 原字段

## 3. 代码交付

- 新增：`decision_monitor/confirmation_whitebox_trace.py`
- 接入：`decision_monitor/builder.py`（在 `confirmation_input_bridge` 已构建后生成）
- Frame：`decision_monitor/schema.py` 新增 `confirmation_whitebox_trace`
- Viewer：`tools/decision_monitor_viewer.py` 新增卡片「确认输入白盒轨迹 / Confirmation Whitebox Trace (M0)」
- Smoke：`tools/smoke_confirmation_whitebox_trace.py`
- 单测：`tests/test_confirmation_whitebox_trace.py`

## 4. 数据结构（五块骨架 + 用户可见层）

- `ConfirmationReasoningStep`
- `ConfirmationWeightItem`
- `ConfirmationExclusionItem`
- `ConfirmationInteractionItem`
- `ConfirmationUserVisibleExplanation`
- `ConfirmationWhiteboxTraceResult`

## 5. 推理过程（固定 4 步）

1. `read_confirmation_context`
2. `map_confirmation_type`
3. `select_next_effect`
4. `compose_confirmation_outcome`

## 6. 验收标准

1. frame 中存在 `confirmation_whitebox_trace`
2. reasoning_steps ≥ 4
3. weight_allocation 至少包含 selected type + 1~2 个排除类型
4. exclusion_log ≥ 1
5. interaction_trace 能记录“有输入”或“无输入”
6. user_visible_explanation 存在
7. Viewer 可展开查看结构
8. 不破坏 confirmation_input_bridge / object_search_interaction / action_hint / recheck / grid 主逻辑

## 7. 本轮结论（写死）

- **实现通过**：已接入 frame/viewer/jsonl
- **单测通过**：`tests/test_confirmation_whitebox_trace.py`（5 类覆盖）
- **smoke/JSONL 验证通过**：`tools/smoke_confirmation_whitebox_trace.py` 生成 `logs/smoke_confirmation_whitebox_trace_*.jsonl`，并验证 `confirmation_whitebox_trace` 存在且 reasoning_steps≥4

