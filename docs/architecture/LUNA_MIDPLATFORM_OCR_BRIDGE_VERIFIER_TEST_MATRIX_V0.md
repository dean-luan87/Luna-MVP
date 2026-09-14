# LUNA — MidPlatform OCR Bridge Verifier Test Matrix v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Scope

后续实现阶段的 verifier A-L（此处只冻结测试意图与通过/失败判据），覆盖：
- OCR evidence filtering/blocking
- delta decision -> reuse/partial/full/hold
- signatures 的可追溯性与引用完整性
- evidence retention（被 block 证据不丢）

参照：`LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_CLASSIFICATION_TABLE_V0.md`（统一枚举对照表与默认策略）

## Test matrix (A-L)

A. OCR evidence schema valid
- 期望：filter_result.block_applied=false 或进入后续 delta 决策路径

B. duplicate evidence -> reuse/ignore_duplicate
- 条件：同窗口 multiple evidence 的 `text_signature` 相同
- 期望：
  - `delta_decision = ignore_duplicate 或 reuse_previous`
  - block_level= `reuse_skip`（或不产生 candidate）

C. changed text
- 条件：`text_signature` 不同
- 期望：`delta_decision=partial_update 或 full_reprocess`

D. low confidence / uncertain line order
- 条件：低置信或 `line_order_status=uncertain`
- 期望：`delta_decision=hold_uncertain`

E. advertisement_like_text
- 条件：命中广告/宣传类占位规则
- 期望：
  - `block_reason=advertisement_like_text`
  - `block_level=soft_block`
  - `allowed_to_task_candidate=false`

M. advertisement_like_text 默认 soft_block
- 条件：visual_text_relevance_class=advertisement_like_text
- 期望：soft_block + evidence retained + 不生成任务候选

N. promotional_text 默认 soft_block
- 条件：visual_text_relevance_class=promotional_text
- 期望：soft_block + block_reason=promotional_text + evidence retained

O. world_context_text 不进入 task candidate
- 条件：visual_text_relevance_class=world_context_text
- 期望：soft_block + allowed_to_task_candidate=false + evidence retained

P. task_context 变化时允许重新评估 blocked evidence
- 条件：task_context override 命中（明确需要识别店铺/广告/商品名称）
- 期望：同 evidence 可从 default block 状态重新分类并允许后续 candidate 生成（计数 relevance_reclassified_count / task_context_override_count）

Q. blocked promotional evidence retained
- 条件：命中 promotional_text 并 block
- 期望：retained_evidence_ref 存在，且 trace/whitebox 引用完整

R. OCR provider 不得提前删除广告/世界背景文字 evidence
- 条件：出现 advertisement_like_text / promotional_text / world_context_text 类证据
- 期望：OCR provider 层不会因“广告判断”而物理丢弃 evidence（中台通过 retention 证明）

S. advertisement_like_text 默认不进入 task candidate，但进入 world_context_candidate
- 条件：visual_text_relevance_class=advertisement_like_text
- 期望：
  - block_reason=advertisement_like_text
  - block_level=soft_block
  - allowed_for_taskchain=false
  - 同时产生 WorldModelContextEvidence（world_context_candidate）

T. user requested advertisement text 可升级为 user_requested_text
- 条件：task/user_intent 明确要求“读这个牌子/念一下广告/看看上面写什么”
- 期望：
  - visual_text_relevance_class=user_requested_text（或等价升级）
  - allowed_when_user_requested=true
  - navigation_action 仍为 null

U. world context evidence 必须有 TTL / revalidation
- 条件：产生 WorldModelContextEvidence
- 期望：
  - expiry_policy 明确
  - requires_revalidation=true（除非 user_confirmed_write 且策略另行允许）

V. promotional text 不得长期持久化，除非 user_confirmed
- 条件：visual_text_relevance_class=promotional_text
- 期望：
  - 默认使用短 TTL / 需要 revalidation
  - 只有 user_requested_text 且触发 user_confirmed_write 时才允许 persistent_requires_revalidation

W. allowed_for_taskchain=false 时不得生成 navigation_action
- 条件：allowed_for_taskchain=false
- 期望：navigation_action=null（硬门槛）

X. OCR evidence retained even when task blocked
- 条件：任意非任务类（advertisement/promotional/background/world）被 blocked
- 期望：retained_evidence_ref 存在；trace/replay/whitebox 引用完整

Y. commercial_context_text 不进入 primary task decision
- 条件：visual_text_relevance_class=commercial_context_text
- 期望：
  - allowed_to_task_candidate=false（不生成 `MidPlatformTextExtractionCandidate`）
  - navigation_action=null

Z. commercial_context_text 可进入 ambient_context_candidate
- 条件：visual_text_relevance_class=commercial_context_text
- 期望：
  - allowed_for_ambient_context_candidate=true
  - ambient_context_candidate_context_type=commercial_context_text

AA. user requested commercial text 可升级为 user_requested_text
- 条件：user_intent 明确询问“店铺活动/折扣/促销/营业信息”，且 evidence 命中 commercial 类
- 期望：
  - visual_text_relevance_class=user_requested_text（或等价升级）
  - speech_priority=user_requested_only
  - allowed_when_user_requested=true
  - navigation_action=null

AB. commercial text 不得生成 navigation_action
- 条件：任意商业补充信息（commercial/promotional/advertisement_like）被允许生成 ambient/readout candidate
- 期望：navigation_action=null

AC. commercial text 默认 short_ttl / requires_revalidation
- 条件：ambient_context_candidate_context_type in {commercial_context_text, ambient_context_text, experience_enrichment_text}
- 期望：
  - expiry_policy=short_ttl（或 contract 允许的短策略）
  - requires_revalidation=true

F. source attribution missing
- 条件：`source_attribution` 缺失或证据契约字段缺失
- 期望：
  - `block_level=hard_block`
  - `block_reason=source_attribution_missing`
  - evidence retention 仍保留 trace/whitebox

G. semantic_summary not null
- 条件：`semantic_summary` 被生成（违反本阶段 contract）
- 期望：hard_block

H. navigation_action not null
- 条件：出现导航动作（违反 contract）
- 期望：hard_block

I. downstream_invocation_attempted
- 条件：监测到 downstream invocation（违反 contract）
- 期望：hard_block，并生成治理告警占位字段

J. blocked evidence retained
- 条件：任意 block_level=true
- 期望：`retained_evidence_ref` 必须存在且 trace/whitebox 引用完整

K. trace/replay/whitebox refs present
- 期望：filter_result_id 与 trace_ref/whitebox_ref 可追溯

L. task candidate only after delta/filter pass
- 期望：当 block_level 为 soft_block/hold_uncertain 时，`task_relevant_text_candidate` 不得生成

AE. blurred_text 默认 hold_uncertain
AF. illegible_text 不进入 task candidate
AG. graffiti_text 默认 soft_block 且不写世界模型事实
AH. fragmented_text 不生成 semantic_summary
AI. decorative_or_stylized_text 用户请求时允许 readout candidate 但必须 uncertainty 标记
AJ. low_confidence_unstable_text 必须 requires_better_frame=true
AK. blocked uncertain evidence retained
AL. 不得把 unreadable text 强行转成世界事实

## Verdict guidance
- 若发生 runtime/midplatform wiring 跳过 delta control -> NO_GO

