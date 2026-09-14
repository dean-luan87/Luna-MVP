# LUNA — Low-Value / Uncertain Visual Text Handling Policy v0

## Phase

- 追加补丁挂靠：`Phase-ModelOCR-MidPlatform-Bridge-002-Fix`（也可作为 `Phase-ModelOCR-MidPlatform-Bridge-001-Fix` 的追加定义）

## Purpose（本阶段只做定义）

本补丁阶段只定义：无法识别、模糊、涂鸦/随手写、艺术化/装饰字导致可读性不稳定、碎片文字、以及无意义/不可执行文本的处理规则。

硬约束（所有规则都必须遵守）：

1. 不实现 runtime：只定义 filtering/blocking/候选生成边界与可追责字段。
2. 不做最终语义提炼：不得把“读不准/意图不明”的文本当作世界事实或可执行任务信息。
3. 不接真实中台：不写入真实世界模型持久层。
4. 默认不进入任务链（taskchain / primary task decision）。
5. 默认不进入世界模型持久层（即不写入 `WorldContextEvidence` 作为事实；仅保留证据引用用于审计与复核）。
6. 保留 `evidence ref`（`retained_evidence_ref` + trace/replay/whitebox 引用）用于审计。
7. 用户明确要求“读一下这个”时：允许作为 readout 尝试路径（contract 层升级为 `user_requested_text`），但必须返回不确定标记（uncertainty 标记/字段）。
8. 低置信度或不可判定时：返回“不确定”，不能强行解释。

## visual_text_relevance_class（新增枚举）

`visual_text_relevance_class` 取值新增以下类别：

- `illegible_text`
- `blurred_text`
- `scribble_or_graffiti_text`
- `decorative_or_stylized_text`
- `fragmented_text`
- `non_actionable_text`
- `meaning_uncertain_text`

## block_reason（新增枚举）

- `illegible_or_unreadable`
- `blurred_or_low_quality`
- `scribble_or_graffiti`
- `decorative_or_stylized`
- `fragmented_text`
- `non_actionable_text`
- `meaning_uncertain`
- `low_confidence_unstable_text`（低置信度但随时间波动/不可稳定判定的占位原因；默认也应触发 `requires_better_frame=true`）

## Default handling rules（默认处理规则；非 runtime）

对每类低价值/不确定视觉文本，默认策略必须满足：

- `allowed_to_task_candidate=false`（不进入任务链默认主候选）
- 默认不生成世界模型事实类写入（`WorldContextEvidence` 作为事实持久化）
- `retained_evidence_ref` 必须保留（不物理删除证据）

逐类规则：

### 1) illegible_text / blurred_text

- `block_level=hold_uncertain`
- `block_reason=illegible_or_unreadable | blurred_or_low_quality`
- `requires_better_frame=true`
- 默认不进入任务链（`allowed_to_task_candidate=false`）
- 默认不写世界模型持久层（`allowed_for_world_context_candidate=false`）
- 若 `user_requested_override=true`：
  - 允许通过 contract 升级为 readout（`user_requested_text` 路径）
  - 输出必须包含 uncertainty 字段（`readability_status/meaning_status/uncertainty_reason` 等）

### 2) scribble_or_graffiti_text

- `block_level=soft_block`
- `block_reason=scribble_or_graffiti`
- 默认不进入任务链、不写世界模型事实
- 默认保留证据引用用于复核
- 可选升级（需要额外治理条件；本阶段不实现 runtime）：
  - 若多帧稳定出现、位置固定、且与安全/区域风险强相关，可作为 `low_priority_world_context_candidate`
  - 升级必须 `requires_revalidation=true`

### 3) decorative_or_stylized_text

- 默认：`block_level=hold_uncertain`（或与 evidence quality 绑定为 soft_block；由 contract 字段驱动）
- `block_reason=decorative_or_stylized`
- 用户明确要求读取时：
  - 允许 readout（contract 层升级为 `user_requested_text`）
  - 必须提示不确定：不得强行解释为“真实店名/真实活动”

### 4) fragmented_text

- `block_level=hold_uncertain`
- `block_reason=fragmented_text`
- 默认不做 joined semantic（不得生成连贯语义总结）
- `requires_better_frame=true`

### 5) non_actionable_text

- `block_level=soft_block`
- `block_reason=non_actionable_text`
- 可读但无明确价值：不进入任务链
- 保留证据引用（不删除）

### 6) meaning_uncertain_text

- `block_level=hold_uncertain`
- `block_reason=meaning_uncertain`
- 不生成任务链语义事实；不得强行解释含义

## 新增字段（建议用于 FilterResult / trace / whitebox）

建议在 `filter_result`（以及 trace/whitebox 可追责字段）中加入：

```json
{
  "readability_status": "readable | partially_readable | illegible | blurred | fragmented | uncertain",
  "meaning_status": "meaningful | non_actionable | uncertain | decorative | unknown",
  "requires_better_frame": true,
  "eligible_for_recheck": true,
  "uncertainty_reason": "...",
  "allowed_for_user_requested_readout": true/false
}
```

约束说明：

- 对不可读/不可判定类别，`requires_better_frame=true`
- 对所有 low-value/uncertain 类，默认不允许把文本直接当作世界事实或任务可执行信息

## Monitoring metrics（新增指标口径；冻结字段名）

- `illegible_text_count`
- `blurred_text_count`
- `graffiti_text_count`（对应 `scribble_or_graffiti_text`）
- `fragmented_text_count`
- `decorative_text_count`（对应 `decorative_or_stylized_text`）
- `non_actionable_text_block_count`
- `meaning_uncertain_hold_count`
- `better_frame_required_count`
- `user_requested_uncertain_readout_count`

计数原则：

- 按 evidence 的 `visual_text_relevance_class` 归类计数
- `*_hold_*` 指在 contract 中进入 `hold_uncertain` 分支的数量

## Verifier test cases（新增用例；AE-AL）

此矩阵仅冻结意图与通过判据，不实现 runtime：

- AE. `blurred_text` 默认 `block_level=hold_uncertain`
- AF. `illegible_text` 不进入 task candidate（`allowed_to_task_candidate=false`）
- AG. `scribble_or_graffiti_text` 默认 `block_level=soft_block`，且不写世界模型事实（不产生 world evidence 写入意图）
- AH. `fragmented_text` 不生成 `semantic_summary`（不得强行 joined semantic）
- AI. `decorative_or_stylized_text`：用户请求时允许 readout candidate，但必须 uncertainty 标记
- AJ. `low_confidence_unstable_text` 必须 `requires_better_frame=true`
- AK. 被 block 的 uncertain evidence 必须保留（`retained_evidence_ref` 存在）
- AL. 不得把 unreadable text 强行转成世界事实（禁止作为 `WorldContextEvidence` 的事实性写入来源）

## Notes（避免的两个错误）

1. 不要“读不准也硬解释”：涂鸦/涂改/模糊字若被识别成店名/标牌，不得当作世界事实或可执行路径。
2. 不要“全部删除”：低价值但可能用于审计/复核/理解环境复杂度的证据必须保留引用，不允许物理删除。

