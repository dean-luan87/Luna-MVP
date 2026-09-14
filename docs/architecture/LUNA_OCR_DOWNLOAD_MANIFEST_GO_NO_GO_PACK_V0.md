## Phase-ModelOCR-003

OCR Download & Manifest Readiness Go/No-Go Pack v0

### 1. 本阶段边界（必须）

- 只做 OCR 下载/本地权重/manifest/readiness 准备
- 不接 OCR runtime
- 不接 YOLO / 不接中台 / 不进 SceneTask/Fusion/Output
- 不做文本语义提炼
- 不执行导航动作
- 不真实播报
- 不进入 controlled_live_stream
- 不扩 Option A

### 2. 产物清单（本阶段必须新增/更新）

目录骨架：

- `models/ocr/`（及子目录占位）
- `configs/models/ocr/`（manifest 存放）

manifest（至少）：

- `configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`
- `configs/models/ocr/macos_vision_ocr_manifest_v0.json`
- `configs/models/ocr/paddleocr_vl_model_manifest_v0.json`（candidate pending）
- `configs/models/ocr/deepseek_ocr_model_manifest_v0.json`（candidate pending）

工具：

- `tools/build_ocr_model_manifest_v0.py`
- `tools/check_ocr_model_readiness_v0.py`
- `tools/verify_ocr_manifest_readiness_v0.py`

文档：

- `docs/architecture/LUNA_OCR_MODEL_MANIFEST_READINESS_DEFINITION_V0.md`
- `docs/architecture/LUNA_OCR_MODEL_MANIFEST_SCHEMA_V0.md`
- `docs/architecture/LUNA_OCR_MODEL_READINESS_CHECK_POLICY_V0.md`
- `docs/architecture/LUNA_OCR_DOWNLOAD_MANIFEST_TEST_MATRIX_V0.md`
- `docs/architecture/LUNA_OCR_DOWNLOAD_MANIFEST_GO_NO_GO_PACK_V0.md`

### 3. GO / CONDITIONAL_GO / NO_GO

#### GO 条件（全部满足）

- PaddleOCR lightweight manifest schema 完整（字段齐全）
- readiness 工具可结构化检查依赖与权重（缺失能识别）
- macOS Vision fallback manifest 完成
- `raw_text_only` / `no semantic` / `no execute` / `no tts` 边界可被 readiness 强校验
- verifier A–J 通过
- 本阶段未接 runtime、未进入下游链路

#### CONDITIONAL_GO 条件

- PaddleOCR 权重尚未完整准备（manifest 可为 pending/partial）
- 部分依赖尚未安装（dependency check 为 partial）
- PaddleOCR-VL / DeepSeek-OCR manifest 仅 candidate pending（不下载）
- 但 manifest/readiness 框架完整且禁止项严格

#### NO_GO 条件（任一触发）

- 伪造权重/hash/size
- manifest 允许 semantic summary / navigation instruction（或等价越权字段）
- readiness 检查进入 runtime 或试图跑 OCR 主链
- 缺少 system fallback 候选（macOS Vision）或未分层

### 4. 推荐下一阶段

- **Phase-ModelOCR-004**：OCR Adapter Skeleton & Offline Harness（只做离线适配壳与候选输出对齐；仍保持 raw text only；不进下游链路）

