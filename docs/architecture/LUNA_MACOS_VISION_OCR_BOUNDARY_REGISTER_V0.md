# LUNA — macOS Vision OCR Boundary Register v0

## Phase

- **Phase-ModelOCR-004A-Closure**
- **Nature:** **register（登记簿）** — 写死禁止项与能力上限，供架构评审与实现门禁引用。

## Scope

适用于：通过 **`tools/evaluate_macos_vision_ocr_raw_text_v0.py`** / **`MacOSVisionOCRAdapterV0`** 产出的 macOS Vision OCR **原文（raw text）** harness，及任何将该路径接入 Luna 的设计文档。

---

## Prohibited（禁止）

| ID | 禁止项 |
|----|--------|
| B1 | **语义提炼**、意图推断、业务结构化字段输出（超越 raw text candidates 合同） |
| B2 | **进入下游链路**（SceneTask / Fusion / Output / 中台契约交付） |
| B3 | **执行类授权**：`allows_execute_now=true`、导航动作、自动化 execute |
| B4 | **真实播报**：`real_tts_invoked=true` |
| B5 | **将 Vision OCR 宣称为全仓「最终默认 OCR 主力」或唯一实时源** |
| B6 | **声明实时高频 OCR 能力**（与本 harness 观测延迟不符） |

---

## Not claimed（不声明）

| ID | 说明 |
|----|------|
| N1 | **实时默认 OCR** — `realtime_default=not_claimed` |
| N2 | **替代 PaddleOCR 作为「第一候选」离线引擎** — 权重与延迟画像不同；并排评审而非取代声明 |
| N3 | **完整 Reading Direction / Layout Order** — 见 OCR 路线图后续契约；当前 `raw_text_joined_strategy` 为启发式 |

---

## Required invariants（产出侧必须保持）

| 字段 / 行为 | 要求 |
|-------------|------|
| **semantic_interpretation_enabled** | `false` |
| **allows_execute_now** | `false` |
| **real_tts_invoked** | `false` |
| **downstream**（summary governance） | **不触发**；`downstream_invoked=false` |
| **输出** | **raw text candidates** 合同范围内；trace/replay/whitebox 可追溯 |

---

## Violation handling（工程语义）

若未来实现违反本 register：对应阶段 **NO_GO**，并回滚接入点至 harness 边界或关闭 Vision 路径。

## Related docs

- `LUNA_MACOS_VISION_OCR_CAPABILITY_STATUS_MATRIX_V0.md`
- `LUNA_MACOS_VISION_OCR_RAW_TEXT_HARNESS_CLOSURE_REVIEW_V0.md`
