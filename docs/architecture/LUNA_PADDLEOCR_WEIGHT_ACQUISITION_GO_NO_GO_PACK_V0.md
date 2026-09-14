# LUNA — PaddleOCR Weight Acquisition Go/No-Go Pack v0

## Phase

- Phase: **Phase-ModelOCR-003-Fix-002**
- Decision subject: 是否已经获得可固定（pinned）的 PaddleOCR det/rec/cls 权重来源，并完成 pinned_local / pinned_partial。

## Hard boundaries（必须满足）

- 不进入 OCR runtime；不跑 OCR 推理/benchmark
- 不伪造权重、不伪造 hash、不伪造 ready/pass
- `raw_text_only=true`、`semantic_interpretation_enabled=false`
- `allows_execute_now=false`、`real_tts_invoked=false`
- macOS Vision OCR fallback 保持（manifest 保留 fallback_policy）

## Decision states

### GO

满足全部：

- acquisition log 产出且记录 provenance（cache/root 或 download notes）
- det/rec/cls 均已固定到：
  - `models/ocr/paddleocr_ppocrv5/det`
  - `models/ocr/paddleocr_ppocrv5/rec`
  - `models/ocr/paddleocr_ppocrv5/cls`
- `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json` 存在且完整
- OCR manifest 更新为 `weights_source=pinned_local` 且包含 `model_files_manifest_path` + `directory_hash_summary`
- readiness report `readiness_status=ready`

### CONDITIONAL_GO

允许：

- det/rec 已固定并完成 hash manifest
- cls 暂缺，但 OCR manifest 显式 `weights_policy.cls_optional=true`，且 `weights_source=pinned_partial`
- readiness report `readiness_status=partial`（但不得出现 hard_blockers/伪造）

### NO_GO

出现任一：

- det/rec 权重仍缺失或无法定位来源目录
- hash/size 清单未生成
- manifest 仍为 `manual_download_required`
- 权重缺失但标记 `pinned_local` 或 readiness 伪造 ready
- 触发了 OCR 推理/benchmark（违规）

## Required evidence（必须产物）

- `logs/paddleocr_weight_acquisition_*.json`
- `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`（若已 pinned）
- readiness report：`logs/ocr_model_readiness_*.json`

