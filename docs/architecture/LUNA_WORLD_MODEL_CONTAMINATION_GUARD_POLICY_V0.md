# LUNA — World Model Contamination Guard Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

定义世界模型写入前的污染防护：识别污染来源、给出处理动作，并明确强禁止项，防止世界模型结构坍塌。

本阶段只定义，不实现 runtime。

## Contamination sources（污染来源）

- `low_confidence_ocr`
- `fabricated_gps`
- `missing_source_chain`
- `expired_commercial_info`
- `promotional_bias`
- `fraudulent_ad`
- `unconfirmed_visual_symbol`
- `metaphor_as_fact`
- `user_falsehood_as_fact`
- `contradicted_evidence`
- `stale_scene_delta`
- `duplicate_amplification`

## Guard actions（处理动作）

- `reject`
- `quarantine`
- `downgrade_write_level`
- `require_revalidation`
- `require_user_confirmation`
- `require_multi_source_validation`
- `rollback_previous_write`

## Forbidden（强禁止）

- 把广告/促销直接写成长期事实
- 把用户幻想写成物理事实
- 把低置信 OCR 写成世界事实
- 把过期活动当作当前有效
- 把单一来源欺诈信息共享给蜂巢（未来分支也必须先多源验证）
- 把重复证据当作多源验证（duplicate amplification）

## Notes（v0）

- `quarantine` 的目标不是“冷处理”，而是隔离后进入复核/多源验证/人工审查流程（后续阶段实现）
- `reject` 必须保留审计链（trace/whitebox），用于解释“为何不写”

