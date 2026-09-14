# LUNA — macOS Vision OCR Raw Text Test Matrix v0

## Phase

- **Phase-ModelOCR-004A**

## Verifier A–L（`tools/verify_macos_vision_ocr_raw_text_v0.py`）

| ID | 测试 | 输入 / 条件 | 期望 |
|----|------|----------------|------|
| **A** | Provider 可用性 | 本机执行 | Darwin + `swift` 在 PATH + `tools/macos_vision_ocr_bridge_v0.swift` 存在（**不**要求 PyObjC） |
| **B** | 输入可读 / 产物存在 | `output_root` | summary + per-sample 存在；且 **`input.missing_input_samples`** 不得为 true（否则 missing_input_samples NO_GO） |
| **C** | Schema 合法率 | 每样本 | envelope 含 `provider_method`、`raw_text_joined_strategy`；候选含 `bbox_status`/`confidence_status` 且与 `bbox`/`confidence` 一致；**全失败** → NO_GO；**部分失败** → soft + **CONDITIONAL_GO** |
| **C2** | 样本级 hard_blockers | 每样本 | 有 hb 的样本记入 **soft_followups**（不单独作为 hard blocker，避免与真实 Vision 失败冲突；严格 GO 需无 hb + verifier 全绿） |
| **D** | bbox 声明 | 每样本 | 每条 candidate：`bbox` 为四维数组或 **`null`**（字段不得缺失） |
| **E** | confidence 声明 | 每样本 | 每条 candidate：`confidence` 为 float 或 **`null`** |
| **F** | `raw_text_joined` | 每样本 | 字段存在（可为 `""`） |
| **G** | `allows_execute_now` | 每样本 | 恒 **`false`** |
| **H** | `semantic_interpretation_enabled` | 每样本 | 恒 **`false`** |
| **I** | `real_tts_invoked` | 每样本 | 恒 **`false`** |
| **J** | 下游未触发 | `summary.governance` | `downstream_invoked=false` |
| **K** | trace / replay / whitebox | `output_root` | `ocr_raw_text_trace.jsonl`、`_replay.jsonl`、`_whitebox.jsonl` **存在且非空** |
| **L** | 禁止键扫描 | summary + per_sample | 不出现导航/语义类禁止键（见 verifier 内 `FORBIDDEN_KEYS`）；`count>0` → NO_GO |

## 手工 / 场景补充（文档层）

- 无文字帧：允许 **empty** `raw_text_candidates`，schema 仍须合法。
- 视频抽帧：验证 `frames/` 与 `replay` 中路径一致（可重放）。
