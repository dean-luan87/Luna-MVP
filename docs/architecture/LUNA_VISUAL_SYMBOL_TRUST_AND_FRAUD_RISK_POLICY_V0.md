# LUNA — Visual Symbol Trust & Fraud Risk Policy v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose

为高风险视觉符号（印章/签名/证书标识/机构徽章等）冻结信任与欺诈风险字段口径，确保：

- 不因“看起来像”就写成事实
- 不做真假最终裁决
- 必须带 `trust / validity / TTL / revalidation` 的治理占位

## Core principles（写死）

1. **视觉符号不是普通文字读取问题**：必须保留视觉证据与来源记录。
2. OCR 只能作为辅助：`ocr_auxiliary_text` 不得作为单独确认依据。
3. 任何进入“强制记忆/高优先级候选”的符号都必须可追责：
   - `source_image_ref`、`crop_region`、`symbol_visual_signature.feature_hash`
   - `confirmation_method`、`trust_score`、`fraud_risk_status`
4. 不得直接判定文件真伪（禁止输出“该章为真/伪”的最终结论）。

## trust fields（冻结）

`trust` 字段必须包含：

- `visual_confidence`：视觉检测/匹配置信度占位（0.0–1.0）
- `context_confidence`：上下文可信度占位（0.0–1.0）
- `trust_score`：综合信任分（0.0–1.0；本阶段不冻结计算公式）
- `fraud_risk_status`：`unknown | suspected_forgery | verified`

约束：

- 默认 `fraud_risk_status=unknown`
- `verified` 只能来自可追责的 `external_verified` 或等价高可信确认链条；本阶段不实现外部验证，因此实现阶段应默认不产出 `verified`

## Risk classes（高风险类别）

以下 symbol_type 视为高风险：

- `seal_or_stamp`
- `signature`
- `certificate_mark`
- `emblem`（在“机构认证/官方身份”语境下）

高风险默认策略：

- `requires_revalidation=true`
- `memory_write_policy` 默认不得为 `forced_*`
- 若进入 `confirmed_memory_candidate`，必须提供 `confirmation` 记录

## TTL / revalidation（冻结口径）

- 所有 visual symbol evidence 默认必须 `requires_revalidation=true`
- TTL 策略不在本阶段冻结数值，但要求“必须可过期/可复核”

