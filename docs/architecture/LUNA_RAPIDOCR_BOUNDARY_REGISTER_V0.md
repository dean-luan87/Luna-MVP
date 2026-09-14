# LUNA — RapidOCR Boundary Register v0

## Phase

- **Phase-ModelOCR-004C-Closure**
- **Nature:** RapidOCR 路径在 Luna 内的 **禁止项 / 非声明项**，与全局 OCR raw-text 边界一致并补强「默认源」条款。

## Prohibited（禁止）

| ID | 禁止项 |
|----|--------|
| R1 | **语义提炼**、意图/导航有效性判断（超越 raw text candidates） |
| R2 | **进入下游**（SceneTask / Fusion / Output / 中台契约交付） |
| R3 | **执行 / 播报**：`allows_execute_now=true`、`real_tts_invoked=true` |
| R4 | **直接替代 PaddleOCR** 作为「唯一主候选」声明（准确率路径仍以 Paddle + 004B 为准） |
| R5 | **直接设为 Luna 默认 OCR 主线 / default offline OCR source**（须经 **005 GT / 006 对照 / ModelOCR-Closure**） |
| R6 | **宣称已验收准确率默认 OCR**（尚无 **GT benchmark**） |

## Not claimed（不声明）

| ID | 说明 |
|----|------|
| N1 | **默认 OCR 源** — `default_ocr_source=not_yet` |
| N2 | **复杂版面/VL 能力** — 另候选层级（如 PaddleOCR-VL） |
| N3 | **端到端实时 SLA** — 仅归档 FPS/ms，未做导航场景门禁 |

## Required invariants（产出）

与 004C harness 一致：`semantic_interpretation_enabled=false`、`downstream_invoked=false`、trace/replay/whitebox 可追溯。

## Related

- `LUNA_RAPIDOCR_CAPABILITY_STATUS_MATRIX_V0.md`
- `LUNA_RAPIDOCR_RAW_TEXT_CANDIDATE_CLOSURE_REVIEW_V0.md`
