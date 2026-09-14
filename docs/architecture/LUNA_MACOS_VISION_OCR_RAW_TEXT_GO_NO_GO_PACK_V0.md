# LUNA — macOS Vision OCR Raw Text Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-004A**
- **Decision:** 是否允许进入 **ModelOCR-005：OCR raw text ground truth benchmark**（及并行准备 **ModelOCR-004B** Paddle adapter + dependency readiness）。

## GO

全部满足：

- Harness 可运行：`tools/evaluate_macos_vision_ocr_raw_text_v0.py` 产出完整 `output_root`（含 summary、per-sample、三个 jsonl、`evaluation_notes.md`）。
- macOS 上 **Vision 桥**可执行；raw text candidates 契约满足（含 `bbox`/`confidence` 显式或 `null`）。
- `tools/verify_macos_vision_ocr_raw_text_v0.py`  verdict = **GO**（无 `hard_blockers`、无需跟进的 soft）。
- 强边界保持：无语义、无下游、无 TTS、无执行授权。
- Verifier **A–L** 通过。

## CONDITIONAL_GO

允许：

- 部分样本无文字 → empty candidates，schema 仍合法。
- bbox/confidence 系统不可得但字段 **`null`**（非缺字段）。
- Verifier 对部分样本 schema 未通过但非全 fail → **partial_schema_valid** soft follow-up → verdict **CONDITIONAL_GO**（exit 0）。

仍必须满足：

- **无** governance 破坏（G/H/I/J）。
- **无**禁止语义键（L）。
- trace/replay/whitebox **齐全非空**（K）。

## NO_GO

出现任一：

- 输出导航建议、语义总结、SceneTask/Fusion/Output 类负载。
- `allows_execute_now=true` 或 `real_tts_invoked=true`。
- trace/replay/whitebox **缺失或空文件**。
- Provider 不可用（非 Darwin / 无 swift / 无桥接脚本）且无法补救。
- **全部**样本 schema 非法（`schema_invalid_all_samples`）。
- `forbidden_semantic_nav_fields_detected`（L 失败）。
- `no_samples_in_output`（空跑）。

## Verdict 与 exit code

| verdict | `verify` exit |
|---------|----------------|
| GO / CONDITIONAL_GO | 0 |
| NO_GO | 2 |

## Recommended next phase

| 顺序 | 阶段 | 说明 |
|------|------|------|
| 1 | **004B** | PaddleOCR raw text adapter skeleton + **dependency readiness**（与 benchmark 隔离） |
| 2 | **004A 并行** | 本 harness 已通则可继续打磨样本与 trace |
| 3 | **005** | Raw text ground truth benchmark |

**明确不包含本阶段：** PaddleOCR 权重推理、YOLO、中台、语义提炼、下游链路。

## Cross-reference

- Harness 说明：`LUNA_MACOS_VISION_OCR_RAW_TEXT_HARNESS_V0.md`
- Test matrix：`LUNA_MACOS_VISION_OCR_RAW_TEXT_TEST_MATRIX_V0.md`
