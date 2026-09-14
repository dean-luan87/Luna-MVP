# LUNA — Visual Symbol Evidence Verifier Test Matrix v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001-Fix**

## Purpose（本阶段只补 verifier 定义）

补齐 Visual Symbol Evidence 的 verifier 测试矩阵与验收规则，覆盖：

- 分类（symbol_type）
- 含义确认（meaning confirmation）
- 强制记忆分级（forced memory）
- 信任与欺诈风险（trust/fraud risk）
- OCR 辅助边界（ocr_auxiliary_text）
- 映射到 `WorldContextEvidence` 的 candidate-only 边界

硬边界（不得违反）：

- 不实现 runtime
- 不接真实记忆写入
- 不接真实世界模型写入
- 不做真假最终裁决
- 不执行导航动作
- 不真实播报

## Required artifacts（verifier 需要可读的字段）

被测对象：`VisualSymbolEvidence`（或等价结构），必须至少包含：

- `visual_symbol_evidence_id`
- `symbol_type`
- `source_image_ref`
- `crop_region`
- `symbol_visual_signature.feature_hash`
- `meaning_status`
- `confirmation.confirmation_method`
- `memory_policy.memory_write_policy`
- `trust.trust_score`
- `trust.fraud_risk_status`
- `observed_at` / `observed_where`
- `trace_ref` / `whitebox_ref`

## Hard blockers（硬阻断条件；任一触发即 NO_GO）

- **HB-N**: 缺少 `source_image_ref`（无法追责）
- **HB-N2**: 缺少 `crop_region`（无法复核）
- **HB-N3**: 缺少 `trust` 或 `fraud_risk_status`（高风险符号不可缺省）
- **HB-O**: `memory_write_policy` 为 `forced_*` 但 `confirmation_method` 为空或 `none`
- **HB-O2**: `memory_write_policy` 为 `forced_*` 但 `meaning_status != confirmed`
- **HB-Q**: 任意 `navigation_action` 非空（本阶段禁止）
- **HB-Q2**: 任意真实播报/执行字段被置为 true（本阶段禁止）
- **HB-H**: 仅凭 `ocr_auxiliary_text` 就把 `meaning_status` 提升为 `confirmed`（禁止）
- **HB-P**: 映射到 `WorldContextEvidence` 时，未确认符号被当作事实性写入（禁止）

## Test matrix (A–Q)

### A. signature 只能生成 visual_symbol_candidate，未确认不得写事实记忆
- **given**: `symbol_type=signature`，`meaning_status in {unknown,suspected}`，`confirmation_method=none`
- **expect**:
  - `memory_write_policy in {no_write,candidate}`
  - `requires_revalidation=true`

### B. seal_or_stamp 必须带 fraud_risk_status
- **given**: `symbol_type=seal_or_stamp`
- **expect**:
  - `trust.fraud_risk_status` 存在且不为缺省空值

### C. stylized_logo 不得强行走 OCR raw text 主链确认
- **given**: `symbol_type=stylized_logo`，存在 `ocr_auxiliary_text`
- **expect**:
  - 不因 `ocr_auxiliary_text` 单独将 `meaning_status` 提升为 `confirmed`
  - `confirmation_method` 若为 `none` 则不得进入强制记忆分支

### D. brand_mark 必须保留 source_image_ref 与 crop_region
- **given**: `symbol_type=brand_mark`
- **expect**:
  - `source_image_ref` 非空
  - `crop_region` 完整（x1,y1,x2,y2）

### E. watermark 不得生成 navigation_action
- **given**: `symbol_type=watermark`
- **expect**:
  - `navigation_action=null`（或等价禁止字段缺省）

### F. handwritten_mark 未确认时 meaning_status=unknown 或 suspected
- **given**: `symbol_type=handwritten_mark`，缺少确认链条
- **expect**:
  - `meaning_status in {unknown,suspected}`

### G. certificate_mark 不得直接判定真伪
- **given**: `symbol_type=certificate_mark`
- **expect**:
  - 不输出“真/伪”的最终裁决字段（本阶段禁止）
  - `fraud_risk_status` 默认允许为 `unknown/suspected_forgery`，但不允许“最终 verified（无外部验证链条时）”

### H. ocr_auxiliary_text 不得单独确认 symbol meaning
- **given**: 任意 `symbol_type`，仅有 `ocr_auxiliary_text` 且无其他确认来源
- **expect**:
  - `confirmation_method != external_verified` 且 `confirmation_method != user_confirmed` 时，不得 `meaning_status=confirmed`

### I. user_confirmed 才允许 forced_memory_with_user_confirmation
- **given**: `memory_write_policy=forced_with_user_confirmation`
- **expect**:
  - `confirmation_method=user_confirmed`
  - `meaning_status=confirmed`

### J. trusted_context 只能提升 confidence，不能跳过 source attribution
- **given**: `confirmation_method=trusted_context`
- **expect**:
  - `source_image_ref` 与 `crop_region` 仍必须存在
  - 不允许将确认链条“折叠成无来源结论”

### K. contradicted symbol 不得进入 persistent memory
- **given**: `meaning_status=contradicted`
- **expect**:
  - `memory_write_policy=no_write` 或降级为 `candidate`
  - 必须 `requires_revalidation=true`

### L. all symbol evidence 必须有 trust / lifecycle / revalidation
- **given**: 任意 `VisualSymbolEvidence`
- **expect**:
  - `trust.trust_score` 存在
  - `memory_policy.requires_revalidation=true`（或等价 lifecycle 字段表达）

### M. fraud_risk suspected 时不得默认共享给其他 Luna
- **given**: `trust.fraud_risk_status=suspected_forgery`
- **expect**:
  - 映射到世界证据/记忆候选时必须禁止 share（用 `world_model_policy.shareable_to_hive=false` 或等价字段表达；若无映射对象则记录为白盒约束）

### N. missing source_image_ref → hard_block
- **given**: `source_image_ref` 缺失
- **expect**:
  - 触发 hard blocker（HB-N）

### O. missing confirmation_method 但 memory_write_policy=forced → hard_block
- **given**: `memory_write_policy` 以 `forced_*` 开头但 `confirmation_method` 缺失/none
- **expect**:
  - 触发 hard blocker（HB-O）

### P. visual symbol mapping to WorldContextEvidence 必须保持 candidate-only（未确认）
- **given**: `meaning_status in {unknown,suspected}`，存在 world evidence 映射产物
- **expect**:
  - `world_model_policy.write_policy=no_write`（或等价 candidate-only 策略）
  - `requires_revalidation=true`

### Q. no runtime / no navigation / no TTS
- **given**: 任意评测输出包
- **expect**:
  - 不出现 runtime 执行字段
  - `navigation_action=null`
  - 不出现真实播报标记

## Verdict guidance

- 若触发任何 Hard blocker → **NO_GO**
- 若 A–Q 覆盖项存在缺口或无法表达（字段缺失导致不可验证）→ **NO_GO**

