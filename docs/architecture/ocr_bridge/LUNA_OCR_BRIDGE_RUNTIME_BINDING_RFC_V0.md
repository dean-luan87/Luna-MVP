# LUNA OCR Bridge — Runtime Binding RFC v0 (Phase-OCRBridge-Implementation-RFC-001)

**阶段**：仅 **RFC / 接线方案 / 绑定点盘点**。**不**改 runtime 代码、**不**真实接线、**不**调用 MidPlatform。

**前置冻结**：`LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md`、`LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md`、Review-001 产物。

---

## 1. OCR provider invocation 输出处（候选装配点）

| 候选路径 | 说明 |
|----------|------|
| `capabilities/guarded_trial/ocr_stage2_controlled_provider_executor_v0.py` | Stage2 **受控** RapidOCR（及未来扩展 executor）调用链；**OcrEvidencePack** 将来可在此链 **shadow** 侧从 invocation record + 行级结果装配。 |
| `capabilities/model_ocr/rapidocr_adapter_v0.py` | RapidOCR 适配层；可作为 **provider 原始输出** 与 **ocr_provider_invocation_ref** 的语义来源之一。 |
| `capabilities/model_ocr/rapidocr_variant_adapter_v0.py` | 变体适配；同上，多 provider 时纳入 **invocation_ref** 维度。 |
| *（预留）* `PaddleOCR` / `CnOCR` executor | 文档占位；**实现另开 phase**，本 RFC 只登记类别。 |

**产出关注点**：`raw_text_candidate`、`provider payload`、行/块级 **bbox**、**confidence**、与调用 id 可追溯。

---

## 2. OCR raw_text candidate 生成处

| 候选概念 | 绑定意图 |
|----------|----------|
| raw_text_candidate | 与 **`raw_candidate_ref`** 一一或一对多可追溯；**不得**单独作为 MidPlatform 输入。 |
| provider payload | 归入 **`ocr_provider_invocation_ref`** 子结构或侧车索引。 |
| bbox / confidence / layout fields | 进入 **`OcrEvidencePackV0`** 各 evidence 条目及 **layout_governance_ref** 交叉引用。 |

---

## 3. Layout / symbol / glyph governance 输出处

| 候选路径 | 说明 |
|----------|------|
| `capabilities/guarded_trial/ocr_layout_symbol_governance_v0.py` | **visual_symbol_candidates**、**visual_glyph_candidates**、**layout_groups**、**reading_order_candidates** 等治理结构；装配 **layout_governance_ref**、**reading_order_ref** 的首选语义源。 |
| `capabilities/guarded_trial/ocr_stage2_static_config_validator_v0.py` | 配置与 stage 边界校验；与 **shadow** 开关、**fail-closed** 策略对齐。 |

---

## 4. OCR input quality gate 输出处

| 候选路径 | 说明 |
|----------|------|
| `capabilities/evaluation/ocr/ocr_input_image_quality_gate_v0.py` | 评测/门控逻辑原型；runtime 侧应对应 **image_quality_gate_ref**（实现阶段迁移到非 eval 管线）。 |
| *（主线未来）* 感知管道内 quality 模块 | 本 RFC 仅要求：**blur / contrast / text scale / skew / preprocess suggestion** 可绑定到 pack 级 **uncertainty** 与 **source_quality_gate_ref**。 |

---

## 5. OCR eligibility gate 输出处

| 候选来源 | 说明 |
|----------|------|
| Evaluation：`capabilities/evaluation/ocr/ocr_eligibility_gate_simulator_v0.py` | **仅设计/评测**；runtime **不得**直接消费 eval routing pack 作为 source。 |
| *（未来 runtime）* 与主线对齐的 **eligibility gate** 模块 | 产出 **eligible / conditional / rejected** 分流结论，写入 **`eligibility_gate_ref`** 与 evidence 路由。 |

---

## 6. RequestTrace / TRW 输出处

| 候选概念 | 说明 |
|----------|------|
| `trace_ref` | RequestTrace / TRW **jsonl** 或等价流的可解析句柄。 |
| `replay_ref` | **replay jsonl** 或切片 id。 |
| `audit_ref` | hard audit / evaluation audit / whitebox-lite（若启用）导出键。 |
| `request_id` / `trace_id` / `session_id` | **禁止伪造**；缺失则 **missing_fields** + **fail-closed**（见 Source Ref Plan）。 |

---

## 与 OcrEvidencePackV0 的关系

上述绑定点仅定义 **「未来在何处采集字段、写入何种 ref」**；**装配行为**须遵守 `LUNA_OCR_BRIDGE_SHADOW_ONLY_WIRING_STRATEGY_V0.md` 与 flag 策略，且 **MidPlatform 转发前 hard gate** 见同 phase 文档矩阵。
