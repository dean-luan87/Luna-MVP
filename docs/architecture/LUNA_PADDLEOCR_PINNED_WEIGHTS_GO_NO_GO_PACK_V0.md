# LUNA — PaddleOCR Pinned Weights Go/No-Go Pack v0

## Phase

- Phase: **Phase-ModelOCR-003-Fix**（主定义）
- **Phase-ModelOCR-003-Fix-004** 已记录一次 HF det+rec **pinned_partial** 达标情形（见文末）
- Decision subject: PaddleOCR lightweight（ppocrv5 pipeline）权重资产 pinned readiness

## Hard boundaries（必须满足）

- 不进入 OCR runtime；不做 OCR 推理/benchmark
- 不伪造权重、不伪造 hash、不伪造 pass
- 不启用语义输出：`raw_text_only=true` 且 `semantic_interpretation_enabled=false`
- `allows_execute_now=false` 且 `real_tts_invoked=false`
- macOS Vision OCR fallback（`macos_vision_ocr_system_v0`）保持可用（manifest 侧保留 fallback）
- 不把大权重纳入 git 跟踪（工程流程要求；本 pack 不替代仓库级保护）

## Decision states

### GO

满足全部：

- `weights_source=pinned_local`
- det/rec/cls 资产均存在
- `model_files_manifest_v0.json` 存在，且 readiness 校验 `ok=true`
- readiness report `readiness_status=ready`（或至少不为 `not_ready`，并无 hard_blockers）

### CONDITIONAL_GO

允许：

- `weights_source=pinned_partial`
- cls 缺失但 **显式** `weights_policy.cls_optional=true`
- 仍满足：det/rec 资产存在 + file-manifest 完整 + hash/size 记录完整 + readiness 无伪造

### NO_GO

出现任一：

- 权重缺失但标记 `pinned_local`
- file-manifest 缺失或校验失败但标记 pass/ready
- readiness tool 进入 OCR 推理（禁止）
- fallback 被移除或被标记为不可用（在本阶段语境下）

## Required evidence（必须产物）

- `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`
- 更新后的 `configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`
- readiness report：`logs/ocr_model_readiness_*.json`

---

## Recorded outcome — pinned_partial（HF det+rec，cls 缺失）（Phase-ModelOCR-003-Fix-004）

一次已归档的成功路径满足本 pack **CONDITIONAL_GO**：

- `weights_source=pinned_partial`
- det/rec 已通过 `prepare_paddleocr_pinned_weights_v0.py` 写入 `models/ocr/paddleocr_ppocrv5/`，file-manifest 与 hash 记录完整
- cls 未纳入；与 manifest/readiness **partial** 一致；须在业务侧接受能力边界（见 `LUNA_PADDLEOCR_PINNED_PARTIAL_CAPABILITY_BOUNDARY_V0.md`）
- acquire 侧 `hard_blockers: []`；readiness `ok: true`，`readiness_status=partial`
- **不**将训练/推理 Python 依赖缺失算作本条「权重 pinned」NO_GO 条件；推理就绪单列 **dependency readiness**（004B）

**Review:** `LUNA_PADDLEOCR_PINNED_PARTIAL_READINESS_REVIEW_V0.md`

