# LUNA — PaddleOCR Alternative Weight Source Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-003-Fix-003**（主定义）
- **Phase-ModelOCR-003-Fix-004**（见下方「已记录结果」；HF 成功收口）

## GO

- det + rec 推理文件已固定到 `models/ocr/paddleocr_ppocrv5/det|rec`  
- （可选）cls 已固定或已声明 optional 且 manifest 为 `pinned_partial`  
- `model_files_manifest_v0.json` 已生成，file-level **sha256 / size** 完整  
- `paddleocr_ppocrv5_model_manifest_v0.json` 为 `pinned_local` 或 `pinned_partial`，且 **不是** `manual_download_required`  
- `tools/check_ocr_model_readiness_v0.py` 无伪造 pass  
- **未**在本阶段执行 OCR 推理或 benchmark  
- **未**接入 OCR runtime / 下游链  

## CONDITIONAL_GO

- cls 缺失但 `--cls-optional` + manifest/readiness 一致声明 partial  
- 依赖版本（paddle/paddleocr）尚需在后续阶段核对（不作为本阶段唯一门禁）  

## NO_GO

- 下载来源不明或无法写入 provenance / hash  
- 权重缺失却标记 pinned_local / readiness pass  
- 主路径依赖「运行时自动下载」  
- 混入语义/导航/TTS/execute 等字段或非 raw-text 契约  

## Recommended next

- 权重 pinned 通过后：**ModelOCR-004B（PaddleOCR Raw Text Adapter Skeleton）**；须 dependency readiness 或 fail-closed（仍不接主 runtime，除非另有阶段定义）。
- 可并行：**ModelOCR-004A（macOS Vision OCR raw text harness）**。

---

## Recorded outcome — Hugging Face alternative source（Phase-ModelOCR-003-Fix-004）

**Verdict: CONDITIONAL_GO**（相对「默认托管路径曾 NO_GO」，替代源 HF 路径满足本 pack 的 CONDITIONAL_GO / pinned_partial 条件。）

**Evidence（示例一次成功运行；staging 目录名随运行变化）：**

- 日志：`logs/paddleocr_alternative_acquire_hf.json`
- acquire：`ok: true`，`hard_blockers: []`
- prepare：`returncode: 0`，manifest `weights_source_set_to`: `pinned_partial`
- readiness：`ok: true`，`readiness_status: partial`
- det/rec：HF `PP-OCRv5_mobile_det` / `PP-OCRv5_mobile_rec`，核心文件 `inference.json` + `inference.pdiparams`，`downloads[]` 含 `sha256` 与 `source_url`
- cls：`cls_dir: null`（与 `--cls-optional` 一致）
- 依赖探针：`paddle` / `paddleocr` / `PIL` 在示例 venv 未安装——**不**作为 acquire 阶段失败条件；见 `LUNA_PADDLEOCR_PINNED_PARTIAL_READINESS_REVIEW_V0.md`

**Detail docs:** `LUNA_PADDLEOCR_PINNED_PARTIAL_READINESS_REVIEW_V0.md`，`LUNA_PADDLEOCR_PINNED_PARTIAL_CAPABILITY_BOUNDARY_V0.md`。
