# LUNA — MidPlatform World Context Text Evidence Policy v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Purpose

定义：当 OCR evidence 被判定为“非当前任务文本 / world context 文本”时，MidPlatform 如何把它写入（或暂存）世界模型侧的环境知识证据层。

注：商业补充信息（店铺活动/折扣/促销/营业信息等）默认按 `LUNA_MIDPLATFORM_COMMERCIAL_CONTEXT_TEXT_POLICY_V0.md` 作为 ambient/commercial 体感候选处理，避免长期污染世界模型。

参照：`LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_CLASSIFICATION_TABLE_V0.md`（统一枚举对照表与默认策略）
参照：`LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`（字段口径对齐映射）

本策略解决两点：
1) 非任务信息不是“垃圾”，默认不进入 TaskChain，但可进入 WorldModelContextEvidence 作为低优先级环境知识；
2) 用户明确要求“读一下这个牌子/看看上面写什么/这家店叫什么”等时，可临时提升为 `user_requested_text` 并允许 readout candidate（但导航动作仍为 `null`）。

## Key output schema（世界模型证据）

### `WorldModelContextEvidence`

说明：本阶段将 `WorldModelContextEvidence` 作为 `WorldContextEvidence` 的旧命名别名进行字段映射（见 `LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`）。

```json
{
  "world_context_evidence_id": "world_text_001",
  "source_evidence_id": "ocr_evidence_001",
  "text": "...",

  "visual_text_relevance_class": "world_context_text",
  "task_relevance_status": "not_currently_relevant",

  "world_model_write_policy": "low_priority_candidate",
  "expiry_policy": "scene_local_ttl | short_ttl | persistent_requires_revalidation",
  "requires_revalidation": true,

  "allowed_for_taskchain": false,
  "allowed_when_user_requested": true,

  "user_requested_override": false,

  "source_attribution": {},

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## world_model_write_policy（写入策略冻结）

`world_model_write_policy` 取值：
- `no_write`：不写入世界模型，只保留 evidence 供审计与潜在复核
- `low_priority_candidate`：低优先级环境知识候选（默认广告/促销/店招类）
- `scene_local_candidate`：场景局部环境候选（店名/商铺/公共设施类默认）
- `persistent_candidate_requires_revalidation`：候选可持久化但必须二次复核后才能稳定
- `user_confirmed_write`：用户明确请求后写入（允许保持更高置信优先级）

## Classification mapping（默认映射，禁止主观“垃圾”命名）

当 `visual_text_relevance_class` 为以下类别时，世界模型侧（`WorldModelContextEvidence`）策略采用：

1) `world_context_text`（店名/品牌/公共标语/楼层导视等场景环境文本）
- 默认：
  - `allowed_for_taskchain=false`
  - `world_model_write_policy=scene_local_candidate`
  - `allowed_when_user_requested=true`
- TTL：
  - `expiry_policy=scene_local_ttl`
  - `requires_revalidation=true`

2) `commercial_context_text` / `promotional_text` / `advertisement_like_text`（商业补充信息）
- 默认：
  - `world_model_write_policy=no_write`（默认不写入世界模型，作为 `AmbientContextCandidate` 做短期体验增强）
  - 如需要留档用于审计/复核，必须使用短 TTL + `requires_revalidation=true`
- 只有在后续 `user_confirmed_write` 分支（用户明确确认偏好/持续保留）时，才允许持久化写入。

3) `decorative_text`
- 默认：
  - `allowed_for_taskchain=false`
  - `world_model_write_policy` 根据证据置信：
    - 置信足够：`low_priority_candidate`
    - 置信不足：`no_write`（保留 evidence 供复核）

4) `uncertain_relevance_text`
- 默认：
  - `world_model_write_policy=no_write`
  - `requires_revalidation=true`
  - 仅在任务上下文明确需要或后续帧证据增强时升级

5) `irrelevant_or_noise_text`
- 默认：
  - `world_model_write_policy=no_write`
  - 只保留 trace/whitebox 与 evidence_retention

## user_requested override（用户明确请求优先级）

当 user_intent 明确为以下之一：
- “读一下这个牌子”
- “看看这个广告写什么”
- “这家店叫什么”
- “屏幕上写什么”
- “这个海报说什么”
- “帮我念一下”

则：
- `user_requested_override=true`
- `visual_text_relevance_class` 可升级为 `user_requested_text`（用于审计与统计）
- 世界模型 write（不默认持久化，避免长期污染）：
  - 若属于 `world_context_text`：`world_model_write_policy=low_priority_candidate`，`expiry_policy=short_ttl`，`requires_revalidation=true`
  - 若属于 `commercial_context_text / promotional_text / advertisement_like_text`：默认保持 `world_model_write_policy=no_write`（由商业策略产生日式 ambient/readout 候选）
- 允许 readout candidate：
  - `allowed_when_user_requested=true`
- 导航动作仍必须为 `null`（本策略不定义 runtime，也不生成 navigation）

## Retention & expiry（保留与过期冻结）

1) 非任务信息不删除
- 被阻断 taskchain 的 evidence 不允许物理删除；
- 可以转入 world context candidate，但仍需记录 `trace_ref/whitebox_ref`。

2) 必须可过期
- `expiry_policy` 必须显式记录；
- `requires_revalidation=true` 默认开启（除非 user_confirmed_write 且后续复核门控放行）。

3) 未经确认的商业补充信息不得长期污染世界模型
- 默认 `commercial_context_text / promotional_text / advertisement_like_text` 不写入（`no_write`），仅短 TTL + `requires_revalidation=true` 可留档用于审计复核。

## Evidence attribution（审计要求）

`WorldModelContextEvidence.source_attribution` 必须可追溯到：
- 原始 `source_evidence_id`
- OCR evidence / yolo_ocr_bridge 的来源引用
- trace/whitebox 证据引用字段

