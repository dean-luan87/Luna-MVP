# LUNA — MidPlatform OCR Evidence Filtering & Blocking Policy v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Scope

本补丁阶段只定义：OCR evidence（raw text candidates/segments 证据）在 MidPlatform evidence layer 的 filtering/blocking 规则、block_reason/block_level 枚举、以及证据 retention 策略。

不实现 runtime，不接真实中台。

## Inputs / Outputs（合同视角）

输入：`MidPlatformOCREvidenceInput`

输出（供后续 candidate extraction 使用）：
- `filter_result`（过滤结果）
- 被阻断 evidence 的 retention + 证据引用（trace/replay/whitebox）
- 决定是否允许进入 `MidPlatformTextExtractionCandidate`

## block_reason 枚举（冻结）

`block_reason` 取值必须来自以下集合之一：

- `advertisement_like_text`
- `promotional_text`
- `background_static_text`
- `decorative_text`
- `low_confidence_text`
- `illegible_or_unreadable`
- `blurred_or_low_quality`
- `scribble_or_graffiti`
- `decorative_or_stylized`
- `fragmented_text`
- `non_actionable_text`
- `meaning_uncertain`
- `low_confidence_unstable_text`
- `reading_order_uncertain_long_text`
- `irrelevant_to_current_task`
- `task_context_mismatch`
- `repeated_non_task_text`
- `expired_scene_text`
- `duplicate_text_evidence`
- `unchanged_text_reused`
- `layout_uncertain`
- `source_attribution_missing`
- `governance_boundary_violation`
- `semantic_leakage_detected`
- `navigation_instruction_leakage_detected`
- `downstream_invocation_attempted`

## block_level 枚举（冻结）

`block_level` 取值必须来自：

- `soft_block`
  - 不进入 task_relevant candidate，但 evidence 保留用于复核。
- `hold_uncertain`
  - evidence 暂存，等待后续帧确认（不进入任务链）。
- `hard_block`
  - 发现治理越界/契约破坏：禁止进入任何后续候选（但仍保留可追责证据）。
- `reuse_skip`
  - 与旧信息一致：跳过重复提炼，复用旧结果（不生成新 extraction candidate）。
- `expired_skip`
  - 超出当前比较窗口：不进入当前窗口 candidate（但证据留档）。

## FilterResult 结构（冻结 schema）

```json
{
  "filter_result_id": "ocr_filter_001",
  "evidence_id": "ocr_evidence_001",

  "visual_text_relevance_class": "task_relevant_text | context_relevant_text | world_context_text | commercial_context_text | advertisement_like_text | promotional_text | decorative_text | user_requested_text | irrelevant_or_noise_text | uncertain_relevance_text | illegible_text | blurred_text | scribble_or_graffiti_text | decorative_or_stylized_text | fragmented_text | non_actionable_text | meaning_uncertain_text",

  "block_applied": true,
  "block_level": "soft_block | hold_uncertain | hard_block | reuse_skip | expired_skip",
  "block_reason": "advertisement_like_text | ...",

  "retained_evidence_ref": "...",
  "evidence_retention_policy": "keep_for_recheck | keep_for_audit_only",
  "eligible_for_recheck": true,

  "allowed_to_task_candidate": false,
  "allowed_for_primary_task_decision": false,
  "allowed_for_ambient_context_candidate": false,
  "ambient_context_candidate_context_type": "commercial_context_text | ambient_context_text | experience_enrichment_text | null",
  "speech_priority": "silent_by_default | user_requested_only | low_priority_hint",
  "requires_human_or_later_review": false,

  "readability_status": "readable | partially_readable | illegible | blurred | fragmented | uncertain",
  "meaning_status": "meaningful | non_actionable | uncertain | decorative | unknown",
  "requires_better_frame": true,
  "uncertainty_reason": "...",
  "allowed_for_user_requested_readout": true/false,

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## 过滤/阻断判定规则（冻结高层逻辑）

### 1) Governance & contract violations（硬门槛）
- 如果发现 `source_attribution` 缺失、契约字段缺失、candidate 试图进入执行/导航/下游，则：
  - `block_level=hard_block`
  - `block_reason` 使用 `source_attribution_missing | governance_boundary_violation | navigation_instruction_leakage_detected | downstream_invocation_attempted` 等对应原因

### 2) Semantic leakage / navigation leakage（硬门槛）
- 如果 evidence 试图携带最终语义总结或导航指令（违反 `semantic_summary=null`、`navigation_action=null`）：
  - `block_level=hard_block`
  - `block_reason` 使用 `semantic_leakage_detected | navigation_instruction_leakage_detected`

### 3) Delta control 复用类（跳过/复用）
- 如果 delta control 判定复用：
  - `block_level=reuse_skip`
  - `block_reason=unchanged_text_reused | duplicate_text_evidence`

### 4) 不确定/低置信（暂存/软阻断）
- `low_confidence_text`：
  - `block_level=hold_uncertain` 或 `soft_block`（由后续 verifier/follow-up 决定）
- `reading_order_uncertain_long_text` / `layout_uncertain`：
  - `block_level=hold_uncertain`

### 5) 无关/过期（阻断但留档）
- `irrelevant_to_current_task`：
  - `block_level=soft_block`
- `task_context_mismatch`：
  - `block_level=soft_block`
- `repeated_non_task_text`：
  - `block_level=reuse_skip`
- `expired_scene_text`：
  - `block_level=expired_skip`

### 6) Visual Text Relevance & Promotional Noise 默认阻断（软阻断/暂存）

引用子模块：`LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_AND_NOISE_FILTER_V0.md`

- `world_context_text`：
  - 默认 `block_level=soft_block`
  - `allowed_to_task_candidate=false`
  - 可进入 `WorldModelContextEvidence`（世界模型环境知识候选；见世界模型策略）
- `commercial_context_text`：
  - 默认 `block_level=soft_block`
  - `allowed_to_task_candidate=false`
  - 可进入 `AmbientContextCandidate`（context_type=commercial_context_text；商业补充体感增强候选）
  - `allowed_for_ambient_context_candidate=true`
  - `speech_priority=silent_by_default`
- `promotional_text`：
  - 默认 `block_level=soft_block`
  - `block_reason=promotional_text`
  - `allowed_to_task_candidate=false`
  - 可进入 `AmbientContextCandidate`（context_type=commercial_context_text；强促销商业补充候选）
  - `allowed_for_ambient_context_candidate=true`
  - `speech_priority=silent_by_default`
- `advertisement_like_text`：
  - 默认 `block_level=soft_block`
  - `block_reason=advertisement_like_text`
  - `allowed_to_task_candidate=false`
  - 可进入 `AmbientContextCandidate`（context_type=ambient_context_text；泛广告环境体感增强候选）
  - `allowed_for_ambient_context_candidate=true`
  - `speech_priority=silent_by_default`
- `decorative_text`：
  - 默认 `block_level=soft_block` 或 `hold_uncertain`
  - evidence 保留；不默认进入任务链
- `uncertain_relevance_text`：
  - 默认 `block_level=hold_uncertain`
  - evidence 暂存；等待任务上下文或后续帧

- `illegible_text | blurred_text | fragmented_text | meaning_uncertain_text`：
  - 默认 `block_level=hold_uncertain`
  - 不进入任务链
  - 不写世界模型持久层
  - 允许后续更清晰帧重新识别（保留 evidence ref 用于审计）

- `scribble_or_graffiti_text`：
  - 默认 `block_level=soft_block`
  - 不进入任务链
  - 默认不写世界模型持久层（如需更进一步需更强治理：多帧稳定 + requires_revalidation）

- `decorative_or_stylized_text | non_actionable_text`：
  - 默认 `block_level=hold_uncertain | soft_block`
  - 不进入默认任务链
  - 用户明确要求读取时，允许 readout（`user_requested_text` 路径），但输出必须带 uncertainty 标记

例外允许（不删除，仅重新分类/重估）：
- 若 `task_context_override` 明确要求识别店铺/广告/商品名称，则可以将对应类别从默认阻断状态恢复为可用候选（同时计数 `task_context_override_count`）。
- 若 `user_requested_override=true`（用户明确要求读取某牌子/店名/屏幕文字等；包含商业活动/折扣/促销/营业信息），则可临时提升到 `user_requested_text`，允许产生 readout candidate。
  - 同时：`AmbientContextCandidate.speech_priority=user_requested_only`
  - 且：`allowed_for_ambient_context_candidate=true`
  - 导航动作仍必须为 `null`，且是否进入 primary task decision 仍为 `allowed_to_task_candidate=false`（本阶段只做证据治理/候选生成）。

## Evidence Retention（必须规则）

1. 被 block 的 OCR evidence 不得删除（只能从 candidate pipeline 中阻断）。
2. 必须保留证据原始引用：`retained_evidence_ref` 与原始 `trace_ref/whitebox_ref`。
3. 必须记录 `filter_result_id`、`block_reason`、`block_level`。
4. `hard_block` 仍然保留 trace/whitebox（用于审计复盘）。
5. `eligible_for_recheck` 用于表示后续帧是否允许重新评估（即使本次不进入 candidate）。

