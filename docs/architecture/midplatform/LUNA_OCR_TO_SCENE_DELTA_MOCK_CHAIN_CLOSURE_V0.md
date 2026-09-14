# Luna — OCR → Scene Delta Mock 链阶段闭环归档 v0

**Phase**：`Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001`  
**性质**：**只读聚合与一致性校验**；不重新运行 OCR、不调用外部 provider、不调用真实 Scene Delta executor、不写 Scene Delta、不写数据库 / WAL / MidPlatform fact / WorldModel、不调用 AI 解释、不改 OCR routing。

## 输入阶段产物根目录（9）

链上各 phase 的 `_eval_out/...` 根目录由 runner 默认常量或 `--roots-json` 覆盖；详见评测文档 `LUNA_EVALUATION_OCR_TO_SCENE_DELTA_CHAIN_CLOSURE_V0.md`。

## 产出（归档包）

由 `tools/evaluation/midplatform/run_ocr_to_scene_delta_chain_closure_v0.py` 写入 smoke 根目录：

- `ocr_to_scene_delta_chain_closure_summary.json`
- `ocr_to_scene_delta_phase_matrix.json`
- `ocr_to_scene_delta_lineage_matrix.json`
- `ocr_to_scene_delta_no_write_boundary_matrix.json`
- `ocr_to_scene_delta_capability_closure_report.json`
- `ocr_to_scene_delta_non_claims_report.json`
- `ocr_to_scene_delta_open_followups.json`
- `ocr_to_scene_delta_chain_closure_notes.md`
- （可选）`ocr_to_scene_delta_chain_closure_errors.json` — 当聚合前置检查失败时

由 `tools/evaluation/midplatform/verify_ocr_to_scene_delta_chain_closure_v0.py` 写入：

- `ocr_to_scene_delta_chain_closure_verifier_report.json`

## 能力边界（本 phase 能证明什么）

- 九个前置 smoke 的 **verifier 均为 GO**、**blockers 为空**（由 phase matrix 汇总）。
- **Lineage**：从各阶段 JSON 串联 `text_joined`、ROI、`candidate_id`、`event_id`、`dry_run_id`、`trace_id`、mock `request_id` / `ack_id`、`contract_reference_mode`。
- **No-write boundary**：各阶段 audit 中统一关心的写入 / 解释类字段为 `false` 或 `na`（字段不存在视为 `na`）。
- **Non-claims**：显式否定生产 executor、生产写入路径等误读。

## 明确非宣称（Non-claims）

见产物 `ocr_to_scene_delta_non_claims_report.json` 与评测侧 GO/NO_GO 包；**local_skeleton 合同 conformance 不等于** 与真实生产 executor OpenAPI / proto 对齐。

## 实现位置

- 能力：`capabilities/midplatform/ocr_to_scene_delta_chain_closure_v0.py`
- Runner / Verifier：`tools/evaluation/midplatform/run_ocr_to_scene_delta_chain_closure_v0.py`、`verify_ocr_to_scene_delta_chain_closure_v0.py`
