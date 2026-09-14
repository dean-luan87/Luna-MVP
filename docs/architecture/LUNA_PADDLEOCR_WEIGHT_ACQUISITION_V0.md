# LUNA — PaddleOCR Weight Acquisition v0

## Phase

- Phase: **Phase-ModelOCR-003-Fix-002**
- Goal: 解决 PaddleOCR lightweight（det/rec/cls）权重来源，并为后续 pinned 固定提供可追踪 provenance。

## Hard boundaries（强边界）

- 不进入 OCR runtime
- 不跑 OCR 推理 / benchmark（禁止对图片调用 `ocr()`）
- 不接 YOLO / 中台 / SceneTask / Fusion / Output
- 不做语义提炼；保持 raw-text only
- 默认不下载；只有显式 `--allow-download true` 才允许“init-only 触发下载”

## Primary routes

### Route A（优先）：受控 init-only 触发下载到缓存

- 工具：`tools/acquire_paddleocr_weights_v0.py`
- 仅允许：
  - import + 版本快照
  - init-only（创建 PaddleOCR 对象）用于触发内部模型下载
  - 扫描本地缓存目录，发现 inference 模型目录
- 禁止：
  - 调用 `ocr(img=...)`
  - 任何 benchmark 或样本识别输出

### Route B：手动下载/解压到本地目录

- 用户提供 `--source-root <manual_download_dir>`
- 直接进入 pinned 固定工具：`tools/prepare_paddleocr_pinned_weights_v0.py`

### Route C：失败则保持 NO_GO

- 网络/依赖/缓存均不可用时，必须保持 NO_GO，不得伪造 partial/ready。

## Acquisition output（证据）

本阶段应产出：

- acquisition log：`logs/paddleocr_weight_acquisition_*.json`
  - 记录 `paddleocr/paddle` 版本、缓存扫描、是否尝试 init-only、发现的 det/rec/cls 目录、来源说明

## Next step（进入 pinned 固定）

当 acquisition 找到 det/rec/cls 目录后，必须再运行：

- `tools/prepare_paddleocr_pinned_weights_v0.py`（固定到 `models/ocr/paddleocr_ppocrv5/`，生成 hash manifest，更新 OCR manifest）
- `tools/check_ocr_model_readiness_v0.py`（重跑 readiness）

