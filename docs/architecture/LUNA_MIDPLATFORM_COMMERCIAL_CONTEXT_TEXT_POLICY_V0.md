# LUNA — MidPlatform Commercial Context Text & Experience Enrichment Policy v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Purpose

定义：当 OCR evidence 中出现店铺活动、折扣、促销、营业信息等“商业补充信息”时，
MidPlatform evidence layer 如何把它们作为 **ambient/commercial experience enrichment 候选**输出，
而不改变 primary task decision（导航主路径）与不默认密集播报。

该策略解决的关键点：
1) 商业信息属于 ambient commercial context，而不是“噪声”；
2) 默认不驱动任务链主判断，只做体感增强候选；
3) 用户明确询问/请求读取时，可临时提升为 `user_requested_text` 并允许 readout；
4) 默认短 TTL + 必须 revalidation，避免长期污染世界模型。

参照：`LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_CLASSIFICATION_TABLE_V0.md`（统一枚举对照表与默认策略）
参照：`LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`（字段口径对齐映射）

## Non-governance boundary

- 不实现 runtime：只定义合同与默认策略。
- 不接真实中台，不进入任务链执行，不做导航动作，不做最终语义提炼，不真实播报。

## visual_text_relevance_class（与过滤合同联动）

本策略读取来自 `LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_AND_NOISE_FILTER_V0.md` 的 `visual_text_relevance_class`：
- `commercial_context_text`
- `promotional_text`
- `advertisement_like_text`
- `user_requested_text`

说明：`AmbientContextCandidate` 在本合同阶段按字段映射进入 `WorldContextEvidence`（001-Fix 统一世界证据合同），见 `LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`。

其中建议的语义分工：
- `commercial_context_text`：店铺活动、折扣、促销、营业时间、商品活动、新品等，对“当前场所理解/体验”有帮助，但默认不替代任务判断。
- `promotional_text`：强促销/交易强意图（例如扫码领券、限时秒杀、满减）。
- `advertisement_like_text`：泛广告/灯箱/海报/轮播屏等，可能与当前地点无强关系但仍具环境感知价值。

## AmbientContextCandidate（新增中台输出合同）

```json
{
  "ambient_context_candidate_id": "ambient_001",
  "source_evidence_id": "ocr_evidence_001",
  "text": "...",

  "context_type": "commercial_context_text | ambient_context_text | experience_enrichment_text",
  "task_relevance_status": "supplementary | user_requested | irrelevant",

  "allowed_for_primary_task_decision": false,
  "allowed_for_experience_enrichment": true,
  "allowed_when_user_requested": true,
  "requires_user_context_match": true,

  "expiry_policy": "short_ttl | scene_local_ttl",
  "requires_revalidation": true,

  "navigation_action": null,
  "speech_priority": "silent_by_default | user_requested_only | low_priority_hint",

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## Mapping rules（默认分层与路由）

### 1) 默认（无强用户请求、无强任务相关）
- `commercial_context_text` / `promotional_text`：
  - `allowed_for_primary_task_decision=false`
  - 输出为 `context_type=commercial_context_text`
  - `speech_priority=silent_by_default`
  - `expiry_policy=short_ttl` 且 `requires_revalidation=true`
- `advertisement_like_text`：
  - `allowed_for_primary_task_decision=false`
  - 输出为 `context_type=ambient_context_text`
  - `speech_priority=silent_by_default`
  - `expiry_policy=short_ttl` 且 `requires_revalidation=true`

### 2) 用户明确询问（override）
- 当 user_intent 明确为：
  - “这家店有什么活动？”
  - “广告上写什么？”
  - “有没有打折？”
  - 或“读一下这个促销/营业信息”
  
  则：
  - 将对应 evidence 升级为 `user_requested_text`
  - `speech_priority=user_requested_only`
  - 保持 `navigation_action=null`
  - 允许 readout candidate（但是否进入 primary task decision 仍为 false）

### 3) 用户当前任务与商业意图匹配（体验增强）
- 当 task_context 表明用户正在执行“购物/找店/找餐饮/找咖啡/找药店/找服务柜台”等商业相关任务时：
  - `commercial_context_text` / `promotional_text` 可升级为 `context_type=experience_enrichment_text`
  - `speech_priority=low_priority_hint`（仅作为体验增强提示，默认不密集播报）
  - 仍保持 `allowed_for_primary_task_decision=false`

## World model 写入约束（避免长期污染）

- 本策略默认不要求把商业补充信息长期写入世界模型；
- 若未来确需写入世界模型，必须遵循 `LUNA_MIDPLATFORM_WORLD_CONTEXT_TEXT_EVIDENCE_POLICY_V0.md` 的写入策略：
  - 默认 `expiry_policy=short_ttl`，`requires_revalidation=true`
  - 未经用户确认，不允许长期污染型 persistent 写入（除非进入 `user_confirmed_write` 分支）

## Monitoring metrics（冻结字段名/口径）

本补丁阶段只定义 metrics 字段与统计口径，不接 runtime：
- `commercial_context_candidate_count`
- `ambient_context_candidate_count`
- `experience_enrichment_candidate_count`
- `commercial_context_suppressed_count`
- `user_requested_commercial_readout_count`
- `commercial_context_expired_count`

统计口径（建议）：
- candidate_count：成功生成对应 `AmbientContextCandidate` 时计数；
- suppressed_count：因 `requires_user_context_match=false` 或默认抑制策略而未生成 candidate 时计数；
- expired_count：TTL 到期后仍被留存为证据但未再激活时计数（placeholder）。

