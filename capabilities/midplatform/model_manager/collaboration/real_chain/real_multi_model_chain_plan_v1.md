# Luna Model Manager — Real Multi-Model Chain Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001`  
**Layer:** Model Manager → Collaboration → Real Chain  
**Mode:** Planning only — 验证协作编排真实闭环，非同时接多个大模型。

---

## 1. 战略定位

Model OS 基础架构已冻结。本阶段验证：

```
Collaboration Slot → Model Manager Fill → Runtime Execution
    → Evidence Fusion → Validation → Fact Admission Candidate
```

**不是**「接 OCR + Grounding + Qwen」，而是证明第一条真实链的编排闭环成立。

---

## 2. 第一条真实链：店招识别

| 层 | 内容 |
|----|------|
| 目标 | `identify_place` |
| Situation | `shopfront_sign` |
| Agent Plan | `read_text` + `verify_context` |

### Collaboration Slots（不绑定模型）

```
slot_1: text_detection   → 哪里有文字
slot_2: text_recognition → 文字是什么
slot_3: context_reasoning → 上下文解释
```

### Model Manager Fill

```
slot_1 → detection_v1   (Text Detector)
slot_2 → ocr_v1         (OCR)
slot_3 → qwen_vl        (Context only — 不负责 OCR)
```

### 执行链

```
Image
  ↓ Text Detector
  ↓ text_region_candidate
  ↓ OCR
  ↓ ocr_text_candidate
  ↓ Qwen-VL Context
  ↓ context_evidence_candidate
  ↓ Evidence Fusion
  ↓ Validation
  ↓ Fact Admission Candidate
```

---

## 3. 为什么不用 SAM/Grounding 优先

错误路径：

```
SAM 找区域 → 猜是什么 → OCR
```

正确路径：

```
任务需要文字 → 文字能力优先 → 需要空间时再引入 SAM
```

SAM 未来角色：**mask refinement capability**，不是 **target discovery**。

本阶段 **不接** Grounding、InternVL、Gemini。

---

## 4. 明确不做

| 禁止 | 正确做法 |
|------|----------|
| OCR vs Qwen 竞争 | 职责不同 |
| 证据自动融合成答案 | Evidence Set + Validation |
| OCR 失败自动换 Qwen | failure evidence → L2 replan |

---

## 5. Smoke Cases

| Case | 场景 | 验证 |
|------|------|------|
| A | 正常店招 | 三 Slot 全通过 |
| B | OCR 模糊失败 | ocr_failure → challenge → request_more_evidence |
| C | Qwen 星巴克幻觉 | unsupported_claim reject |
| D | Detector 不可用 | collaboration_degradation → replan |

---

## 6. 模块结构

```
collaboration/real_chain/
├── real_multi_model_chain_plan_v1.md
├── real_chain_orchestrator_v1.py
├── slot_provider_binding_v1.py
├── evidence_fusion_adapter_v1.py
├── real_chain_validation_policy_v1.json
└── schemas/
    ├── execution_trace_schema.json
    ├── evidence_package_schema.json
    └── fusion_candidate_schema.json
```

---

## 7. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001`
