# LUNA Evaluation — STCM Event Skeleton GO / NO-GO Pack v0（Phase-STCM-Event-Skeleton-001）

## GO

- **事件骨架主文档**、**事件类型注册表文档**、**example registry JSON** 齐全。  
- **至少 9 类** `stcm_*` 事件定义完整，且 **每类** 含 **`event_id` + `event_type`**，且含 **`trace_id` 和/或 `call_id`**（按 registry）。  
- **`stcm_model_call_timeout`** 含 **`notified_midplatform`**。  
- **`stcm_voice_notice_requested`** 含 **`deadline_at` + `expires_at`**。  
- **`stcm_result_discarded`** 含 **`discard_reason`**。  
- **`stcm_anchor_revalidated`** 含 **`spatial_anchor_valid`**。  
- 文档明确 **不接 runtime / 不实装 MidPlatform**。  
- **README** 含 **STCM-Event-Skeleton-001** 索引。  
- **verifier `verdict = GO`**。

## CONDITIONAL_GO

- 9 类事件齐全，但 **某模态特化扩展字段**（如 Map/Memory 专有）标为后续补齐；**gap 报告**记录完整。

## NO_GO

- **缺** timeout / voice notice / result discard / anchor revalidation **任一类**。  
- 事件 **无** `trace_id`/`call_id` 锚定。  
- timeout **无** `notified_midplatform`。  
- 文档 **暗示已接 runtime** 或 **README 无索引**。
