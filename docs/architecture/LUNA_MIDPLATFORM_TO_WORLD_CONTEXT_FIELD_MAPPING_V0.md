# LUNA — MidPlatform → WorldContextEvidence Field Mapping Alignment v0

## Phase

- Phase-WorldModel-ContextEvidence-001-Fix
- MidPlatform World/Ambient Field Mapping Alignment v0

## Purpose

本阶段只做 **字段命名、枚举、映射关系对齐**：
- 把 MidPlatform 侧（`ambient_context_candidate` / world context 候选）的字段映射到
  Phase-WorldModel-ContextEvidence-001 的统一合同 `WorldContextEvidence`。

禁止：
- runtime 实现
- 写入真实世界模型
- 接推荐系统/任务执行/导航动作/播报

## Scope（映射对象）

MidPlatform 侧候选（此处为合同字段口径）：
- `AmbientContextCandidate`（ambient/commercial/experience enrichment 候选）
- `WorldModelContextEvidence`（001-Fix 的旧命名；本合同阶段映射到 `WorldContextEvidence`）
- `MidPlatformTextExtractionCandidate`（仅用于说明：它不直接进入世界证据层）

WorldModel 侧统一合同：
- `WorldContextEvidence`
- `CommercialActivityEvidence`（作为 `WorldContextEvidence.content` 的商业扩展占位语义）
- `WorldChangeEvent`（本阶段仅不展开映射到变化链）

## Naming disambiguation（旧命名消歧）

- MidPlatform 中的 `WorldModelContextEvidence`：统一作为 `WorldContextEvidence` 的“候选来源/旧命名别名”。
- 实现侧建议后续统一使用 `WorldContextEvidence`，避免并存两套 schema 名称导致 skeleton 漂移。

## Core mapping rules（字段对齐总则）

1) 强制存在性（contract invariants）
- `WorldContextEvidence.observed_at`
- `WorldContextEvidence.observed_where`
- `WorldContextEvidence.trust`
- `WorldContextEvidence.lifecycle`
- `WorldContextEvidence.world_model_policy`
- `WorldContextEvidence.trace_ref` / `whitebox_ref`

2) 来源字段可来自不同模块
- MidPlatform 候选只需要给出证据引用与可得的置信度；其余字段可用合同允许的“占位/保守值”，但字段必须存在。

3) TTL / revalidation 来自 MidPlatform 的到期策略
- MidPlatform：`expiry_policy` / `requires_revalidation`
- World：`lifecycle.ttl_policy` / `lifecycle.requires_revalidation`

## Mapping tables（关键字段映射）

### 1) Evidence identity / provenance

| MidPlatform 字段 | WorldContextEvidence 字段 | 映射规则 |
|---|---|---|
| `ambient_context_candidate_id` 或 `world_context_evidence_id` | `world_context_evidence_id` | 若两者并存：以 `world_context_evidence_id` 为主键；candidate id 作为 trace/whitebox 或内容引用的补充。 |
| `source_evidence_id`（ambient / world policy） | `source_evidence_refs[]` | 放入对应 evidence ref 列表；缺失时用占位 ref。 |
| `source_modalities`（若存在）或 `source_attribution` 可推导 | `source_modalities[]` | OCR→`ocr`，YOLO→`yolo`，其它模态占位。 |
| `trace_ref` | `trace_ref` | 直接映射。 |
| `whitebox_ref` | `whitebox_ref` | 直接映射。 |

### 2) Observed time（observed_at）

| MidPlatform 候选可得信息 | WorldContextEvidence 字段 | 映射规则 |
|---|---|---|
| MidPlatform clock / evidence input timestamp | `observed_at.timestamp_ms` | 取证据观测时刻；`time_source=midplatform_clock`。 |
| 若未知 | 仍需字段存在 | `timestamp_ms` 必须存在；未知时由后续阶段填充保守值（例如 0）但要保留 `time_source`。 |
| 系统确认机制 | `observed_at.date_confidence` | 保守设置为 `system_confirmed`（占位）；后续再细化。 |

### 3) Observed space（observed_where）

| MidPlatform 候选可得信息 | WorldContextEvidence 字段 | 映射规则 |
|---|---|---|
| scene/place hint（例如“某商场一楼”） | `observed_where.place_hint` | 直接映射或占位。 |
| 位置来源类型（GPS/POI/视觉地标/室内场景） | `observed_where.spatial_anchor_type` | 映射到合同枚举：`gps | map_poi | visual_landmark | indoor_scene | unknown`。 |
| geo定位/相对位置（若存在） | `observed_where.geo_location / relative_position` | 直接映射；缺失字段保留为 null。 |

### 4) Content（content）

| MidPlatform 字段 | WorldContextEvidence.content.* | 映射规则 |
|---|---|---|
| `text` | `content.text` | 直接映射。 |
| `entity_type`（若存在）或由 `context_type` / `visual_text_relevance_class` 推导 | `content.entity_type` | commercial/activity 类映射到 `store_promotion / store_business_hours / store_opening_closing / ...`（占位枚举）。 |
| `entity_name`（若存在） | `content.entity_name` | 直接映射；缺失为 null 或占位。 |
| `details`（若存在） | `content.details` | 直接映射。 |
| `valid_time_text`（若存在） | `content.valid_time_text` | 直接映射。 |
| `extracted_from`（例如 ocr_raw_text） | `content.extracted_from` | 从 evidence 来源推导；缺失占位。 |

### 5) Trust（trust）

| MidPlatform 可得置信度 | WorldContextEvidence.trust.* | 映射规则 |
|---|---|---|
| OCR 置信度 | `trust.ocr_confidence` | 直接映射。缺失则保守占位。 |
| YOLO 置信度（若有） | `trust.yolo_confidence` | 直接映射或保守占位。 |
| 其它来源置信度 | `trust.source_confidence` | 由多源/候选来源推导；缺失保守占位。 |
| 可验证性（同空间多次出现、跨模态一致、用户确认） | `trust.cross_validation_status` | 映射：single_source / multi_source_confirmed / contradicted / expired / unknown（保守未知）。 |
| 最终信任度 | `trust.trust_score` | 占位映射（例如由置信度聚合）；本阶段只要求字段存在。 |
| 欺诈风险状态 | `trust.fraud_risk_status` | 占位 unknown/suspected/verified_safe/suspected_fraud。 |

### 6) Lifecycle（lifecycle）

| MidPlatform 字段 | WorldContextEvidence.lifecycle.* | 映射规则 |
|---|---|---|
| `expiry_policy`（short_ttl/scene_local_ttl/persistent_requires_revalidation） | `lifecycle.ttl_policy` | 枚举一一映射；未提供时禁止 skeleton 假设，必须使用占位但字段存在。 |
| `requires_revalidation` | `lifecycle.requires_revalidation` | 直接映射。 |
| `evidence_status`（active/stale/expired...） | `lifecycle.evidence_status` | 若 MidPlatform 未提供：默认 `active`（占位），但允许后续复核更新。 |
| `expires_at`（若 MidPlatform 未提供） | `lifecycle.expires_at` | 允许为 null，但字段必须存在。 |
| `last_seen_at / seen_count` | lifecycle.* | 若缺失则保守占位（0/1）。 |

### 7) World model policy（world_model_policy）

| MidPlatform 字段 | WorldContextEvidence.world_model_policy.* | 映射规则 |
|---|---|---|
| `world_model_write_policy` | `world_model_policy.write_policy` | 枚举直接映射：no_write / low_priority_candidate / scene_local_candidate / persistent... / user_confirmed_write。 |
| `allowed_for_taskchain=false` / `allowed_for_primary_task_decision=false` | `task_planning_impact` | 映射为 `none`（默认）。若存在“允许作为补充”则映射 `weak`（占位）。 |
| `requires_user_confirmation`（由 user_requested_override / 用户确认分支推导） | `requires_user_confirmation` | 用户未明确确认：false。用户明确确认：true（占位）。 |
| 共享到跨 Luna | `shareable_to_hive` | 默认 false；只有在 trust_score 与 fraud_risk 门控满足时允许提升（本阶段只定义字段）。 |

### 8) Trace / whitebox / replay

| MidPlatform 字段 | WorldContextEvidence 字段 | 映射规则 |
|---|---|---|
| `trace_ref` | `trace_ref` | 直接映射 |
| `whitebox_ref` | `whitebox_ref` | 直接映射 |
| `replay_ref`（若存在） | contract 未显式要求 | 可作为 trace_ref 的附加引用字段（占位），但不改变合同字段集合。 |

## What belongs to MidPlatform vs WorldContract（归属声明）

- MidPlatform 临时候选字段：
  - `allowed_for_task_candidate` / `allowed_for_ambient_context_candidate` / `speech_priority`
  - `context_type` / `task_relevance_status`（仅作为路由与输出控制）
- WorldContract 必须字段：
  - `observed_at / observed_where / trust / lifecycle / share_policy / privacy_policy / world_model_policy`

实现侧建议：skeleton 生成 `WorldContextEvidence` 时，以该 contract 字段集合为准，不携带多余“语义重复”的世界证据结构名。

