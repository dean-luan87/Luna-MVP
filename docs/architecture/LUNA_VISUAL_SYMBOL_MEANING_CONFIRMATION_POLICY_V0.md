# LUNA — Visual Symbol Meaning Confirmation Policy v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose

定义 Visual Symbol 的“含义确认（meaning confirmation）”状态机与确认方法枚举，确保：

- 未确认前只能是 `visual_symbol_candidate`，不是事实
- OCR 只能辅助，不能单独确认含义
- 任何确认都必须可追责（记录方法、来源、置信度与时间）

## meaning_status（冻结枚举）

- `unknown`：未知（仅检测到疑似符号）
- `suspected`：疑似（有候选含义，但不足以确认为事实）
- `confirmed`：已确认（通过明确确认方式得到）
- `contradicted`：被否定/冲突（后续证据否定先前含义）

状态迁移硬约束：

1. `unknown → confirmed` 不允许仅靠 OCR 文本；必须有确认链条（见下文）
2. `suspected → confirmed` 必须提升 `confirmation`，并记录证据来源
3. 任意状态出现强冲突证据可进入 `contradicted`，且必须触发 revalidation

## confirmation_method（冻结枚举）

- `none`：无确认
- `user_confirmed`：用户明确确认（推荐用于强制记忆前置）
- `multi_observation`：多次观测一致（多帧/多次出现 + 特征签名一致）
- `trusted_context`：可信上下文验证（例如医院窗口办理流程、带权威上下文的标识场景；但仍不等于真伪裁决）
- `manual_annotation`：人工标注（内部标注/审核）
- `external_verified`：外部验证（仅记录“验证来源”，本阶段不接外部系统）

## Confirmation record（确认记录必须字段）

当 `meaning_status` 不为 `unknown` 时，必须记录：

- `confirmation.confirmation_method`
- `confirmation.confirmation_confidence`（0.0–1.0）
- `confirmation.confirmed_at`（时间戳或可追责引用）

当 `confirmation_method=user_confirmed` 时，建议记录：

- `confirmation.confirmed_by`：`user`
- `trace_ref` 指向用户确认事件的审计记录（占位引用）

## 禁止项（强制）

- 禁止：仅凭 `ocr_auxiliary_text` 就把 `seal_or_stamp/signature/certificate_mark` 的含义提升为 `confirmed`
- 禁止：在未确认前将其映射为世界模型“事实性”实体（见 mapping 与 forced memory policy）

