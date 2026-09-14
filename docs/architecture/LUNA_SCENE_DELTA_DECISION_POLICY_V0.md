# LUNA — Scene Delta Decision Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose

冻结 Scene Delta 的核心分流结果对象 `SceneDeltaDecision` 以及 `delta_status`/`delta_action` 的语义与默认规则。

本阶段只定义，不实现。

## SceneDeltaDecision（冻结 schema）

```json
{
  "delta_decision_id": "scene_delta_decision_001",
  "delta_input_id": "scene_delta_input_001",
  "matched_previous_state_ref": null,

  "delta_status": "new | unchanged | changed | duplicate | uncertain | expired | contradicted | task_context_changed | same_content_same_place | same_content_new_place | new_content_same_place | content_removed | content_replaced | content_expired | content_contradicted | carrier_removed | carrier_added | carrier_changed | frequently_changing_surface | stable_background_information",
  "delta_action": "reuse_previous | ignore_duplicate | partial_update | full_reprocess | hold_uncertain | expire_and_reprocess | block",

  "change_summary": {
    "text_changed": false,
    "object_changed": false,
    "layout_changed": false,
    "spatial_shift_ratio": 0.0,
    "confidence_delta": 0.0,
    "task_context_changed": false,
    "validity_changed": false
  },

  "decision_reason": "...",
  "allowed_to_downstream_candidate": false,
  "requires_revalidation": false,

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## delta_status（冻结枚举语义）

- `new`：无匹配历史状态
- `unchanged`：内容与锚点在容忍范围内一致
- `changed`：内容/对象/布局发生可观测变化
- `duplicate`：同窗口/同批次重复输入
- `uncertain`：低置信或不稳定，需要暂存等待更多证据
- `expired`：历史状态 TTL 过期，需要复核
- `contradicted`：新证据与旧证据冲突（不等于真假裁决）
- `task_context_changed`：任务上下文变化触发重评（即使内容未变）

（时空锚点增强：固定空间载体的内容演替与载体变化）

- `same_content_same_place`：同一内容同一位置（可复用）
- `same_content_new_place`：同一内容出现在新位置（空间模式变化）
- `new_content_same_place`：同一位置新内容出现（新增）
- `content_removed`：同一位置内容消失/下架（不等于事实否定）
- `content_replaced`：同一位置内容被替换（演替）
- `content_expired`：内容因 TTL/时效过期需要复核
- `content_contradicted`：内容冲突（冲突观测，不做真假裁决）
- `carrier_removed`：载体移除（例如围挡撤除）
- `carrier_added`：载体新增
- `carrier_changed`：载体发生变化（屏幕/海报栏/招牌替换）
- `frequently_changing_surface`：频繁更新面（例如海报栏）
- `stable_background_information`：稳定背景信息（例如长期导视牌）

## delta_action（冻结动作语义）

### 1) reuse_previous
适用：

- content signature 未变化（exact/near match）
- spatial_shift 低于阈值
- TTL 未过期
- task_context 未变化

动作：

- 复用 `SceneProcessedState.last_output_refs`
- seen_count +1，更新 last_seen_at
- 不进入后续完整处理链

### 2) ignore_duplicate
适用：

- 同一窗口内重复 evidence
- 与已处理状态完全一致且无新增价值

动作：

- 保留 trace/whitebox
- 不进入后续候选

### 3) partial_update
适用：

- 文本相同但位置变化
- 对象相同但置信度变化
- 布局变化但内容基本一致
- 世界上下文有轻微更新（不触发全量重处理）
  - 同一 anchor 上内容替换但载体稳定：可先记录为 content_replaced，并进入局部更新/重评路径

动作：

- 仅更新变化字段
- 保留 previous_state_ref / previous_result_ref

### 4) full_reprocess
适用：

- text/object/signature 改变
- task_context_changed 需要重新判断 relevance
- 原状态过期或 validity_changed

动作：

- 进入完整处理链（但仍是 candidate-only）
- 允许生成新的 downstream candidates（但禁止执行）

### 5) hold_uncertain
适用：

- 低置信度、reading_order uncertain
- 模糊/碎片/涂鸦类低价值信息
- 单帧不足以确认

动作：

- 暂存等待后续帧
- 默认不进入任务链，不写世界事实

### 6) expire_and_reprocess
适用：

- TTL 过期或需要 revalidation
- 商业活动/施工/店铺状态等需要复核
  - 固定空间节点（poster_board/screen）内容具有时效性，需要周期性复查

动作：

- 标记旧状态 expired
- 新证据重新进入处理链（full_reprocess）

### 7) block
适用：

- governance violation（source attribution 缺失等）
- 发现 semantic/navigation leakage
- downstream invocation 企图

动作：

- hard block（不进入后续候选）
- 证据仍保留用于审计

## Allowed fluctuation vs hard invariants（冻结）

允许波动（不作为 NO_GO）：

- 新/旧/变化/重复/不确定 的比例
- partial_update vs full_reprocess 的比例

硬不变量（任何出现都应视为 NO_GO）：

- 允许执行（allows_execute_now=true）
- 生成 navigation/action
- 真实播报
- 写入真实世界模型

