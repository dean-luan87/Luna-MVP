## Phase-ModelOCR-003

OCR Download & Manifest Readiness Definition v0

### 0. 本阶段边界（硬约束）

本阶段只做 OCR 候选模型的“本地资产准备 + manifest + readiness check”。

- 不接 OCR runtime
- 不接 YOLO
- 不接中台
- 不接 SceneTask/Fusion/Output
- 不做文本语义提炼（raw text only）
- 不执行导航动作
- 不真实播报
- 不进入 controlled_live_stream
- 不扩 Option A
- 不跑 OCR 主链/benchmark（可做依赖 import 检查与文件 hash 检查）

### 1. 本阶段目标（v0）

- 建立 OCR 模型本地目录结构（不放大权重入 git）
- 为 Priority 1（PaddleOCR lightweight / PP-OCRv5 路线）准备 manifest 骨架与可校验字段
- 为 macOS Vision OCR（system provider）准备 manifest（无权重）
- 为 PaddleOCR-VL / DeepSeek-OCR 写 candidate manifest（允许 pending/not_prepared）
- 提供 readiness check 工具：
  - 依赖是否可 import（best-effort，不安装）
  - 权重路径存在性/sha256/size（仅当文件存在才计算，禁止伪造）
  - 禁止项与边界字段检查（raw_text_only/no semantic/no execute/no tts）
  - provider kind/system provider 可用性初检

### 2. 目录结构（推荐，v0）

```
models/ocr/
  paddleocr_ppocrv5/
    det/
    rec/
    cls/
  paddleocr_vl/
  macos_vision/
  deepseek_ocr/

configs/models/ocr/
  paddleocr_ppocrv5_model_manifest_v0.json
  macos_vision_ocr_manifest_v0.json
  paddleocr_vl_model_manifest_v0.json
  deepseek_ocr_model_manifest_v0.json
```

原则：

- Priority 1 的 PaddleOCR lightweight manifest 必须先完成（可为 pending/partial，但 schema 必须完整）
- system provider manifest 不需要权重
- 大权重不得提交到 git；manifest 只记录路径/hash/size（若文件存在）

### 3. Readiness 输出（报告）要求（v0）

readiness report 至少包含：

- `model_config_id`, `model_family`, `candidate_tier`, `manifest_path`
- `dependency_check`
- `weights_check`（paths/missing/mismatch/sha256/sizes）
- `provider_check`
- `raw_text_contract_check`
- `forbidden_semantic_check`
- `fallback_check`
- `readiness_status`：`ready | partial | not_ready`
- `hard_blockers`, `soft_followups`
- `recommendation`：固定为 `do_not_enter_runtime`

