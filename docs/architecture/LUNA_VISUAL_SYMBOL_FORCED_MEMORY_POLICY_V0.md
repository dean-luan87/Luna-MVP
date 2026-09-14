# LUNA — Visual Symbol Forced Memory Policy v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose

定义 Visual Symbol Evidence 的“记忆分级写入策略（forced memory）”边界，明确：

- **强制记忆不是无条件写入**
- 未确认前只能是候选（candidate_only）
- 强制记忆必须有确认方式与可追责字段

本阶段只定义 policy，不接真实记忆写入、不接真实世界模型写入。

## memory_write_policy（冻结枚举）

- `no_write`：不写入（仅保留证据引用）
- `candidate`：候选（candidate_only；不写长期记忆）
- `confirmed_memory_candidate`：含义已确认，可进入记忆候选（仍需 revalidation/TTL）
- `forced_with_user_confirmation`：用户明确确认后允许强制记忆（仍需可追责与 revalidation）
- `persistent_requires_revalidation`：允许持久化候选，但必须 revalidation（例如长期存在的品牌标识；不等于事实锁死）

## 分级口径（冻结）

### 1) candidate_only

条件：

- `meaning_status in {unknown, suspected}` 或 `confirmation_method=none`
- 或属于高风险类别但尚无确认链条（印章/签名/证书标识）

约束：

- 必须保留 `source_image_ref` + `crop_region` + `symbol_visual_signature.feature_hash`
- `requires_revalidation=true`

### 2) confirmed_memory_candidate

条件：

- `meaning_status=confirmed`
- `confirmation_method != none`

约束：

- 仍不得生成导航动作
- 默认 `requires_revalidation=true`（除非后续另有闭环机制）

### 3) forced_with_user_confirmation

条件（必须同时满足）：

- `confirmation_method=user_confirmed`
- `meaning_status=confirmed`
- `trust.trust_score` 达到策略阈值（本阶段不冻结阈值数值，但要求存在）

约束：

- 仍必须 `requires_revalidation=true`
- 必须记录用户确认的可追责引用（`trace_ref`）

### 4) trusted_institutional_symbol（政策标签；非枚举字段）

用于描述“高可信场景出现的机构符号”（如医院章/公司章/证书章），但**本阶段不允许直接判真伪**。

要求：

- 仍必须有 `source_attribution` 与 `fraud_risk_status`
- 若缺少确认链条，仍只能停留在 `candidate` 或 `confirmed_memory_candidate`

### 5) rejected_or_uncertain（政策结果；通过组合表达）

当出现冲突/被否定：

- `meaning_status=contradicted`
- `memory_write_policy=no_write`
- `requires_revalidation=true`

## 必须字段（强制记忆相关）

当 `memory_write_policy` 不为 `no_write` 时，必须存在：

- `confirmation.confirmation_method`
- `trust.trust_score`
- `trust.fraud_risk_status`
- `observed_at` / `observed_where`
- `source_image_ref` / `crop_region`

