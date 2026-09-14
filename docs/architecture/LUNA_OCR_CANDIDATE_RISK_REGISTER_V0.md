## Phase-ModelOCR-002

OCR Candidate Risk Register v0

### 0. 目的

登记候选 OCR 模型在“依赖、权重、GPU、在线/API、许可证、可复现性、输出形态”方面的风险，用于后续阶段（ModelOCR-003/004）的治理与隔离。

### 1. 风险字段（v0）

- `risk_id`
- `candidate_id`
- `risk_type`（dependency | weights | gpu | online | license | reproducibility | output_semantics | maintenance）
- `severity`（low | medium | high）
- `description`
- `mitigation`
- `owner_phase`（建议在哪个阶段解决）

### 2. 风险清单（v0）

#### 2.1 PaddleOCR / PP-OCR pipeline（A 类）

- **risk_id**: `r_paddleocr_weights_manifest_missing`  
  **candidate_id**: `paddleocr_ppocr_pipeline`  
  **risk_type**: weights / reproducibility  
  **severity**: medium  
  **description**: det/rec/cls 权重来源与版本组合多，若不做 manifest 固化，复现困难。  
  **mitigation**: ModelOCR-003 固化权重来源、hash、下载方式与本地缓存路径；离线可复现。  
  **owner_phase**: ModelOCR-003

- **risk_id**: `r_paddleocr_dependency_surface`  
  **candidate_id**: `paddleocr_ppocr_pipeline`  
  **risk_type**: dependency  
  **severity**: medium  
  **description**: 依赖链可能包含 paddle/paddle-inference/opencv 等，多平台差异较大。  
  **mitigation**: ModelOCR-003 做依赖清单与最小可运行配置；优先 CPU 路径。  
  **owner_phase**: ModelOCR-003

#### 2.2 macOS Vision OCR（C 类）

- **risk_id**: `r_macos_bbox_normalized_coords`  
  **candidate_id**: `macos_vision_ocr`  
  **risk_type**: output_semantics  
  **severity**: low  
  **description**: bbox 多为归一化坐标，需要统一转换到像素坐标；中文准确路径可能产生“行/片段 bbox”。  
  **mitigation**: ModelOCR-003/004 在适配层统一 bbox 表示与行合并策略（仍保持 raw text）。  
  **owner_phase**: ModelOCR-003

- **risk_id**: `r_macos_version_variance`  
  **candidate_id**: `macos_vision_ocr`  
  **risk_type**: reproducibility  
  **severity**: medium  
  **description**: 随 OS/SDK 版本变化，识别效果可能漂移。  
  **mitigation**: 在评测记录中冻结 OS 版本；作为 fallback/对照，不作为唯一主线来源。  
  **owner_phase**: ModelOCR-004

#### 2.3 PaddleOCR-VL（B 类）

- **risk_id**: `r_vl_gpu_heavy`  
  **candidate_id**: `paddleocr_vl_series`  
  **risk_type**: gpu / dependency  
  **severity**: high  
  **description**: 0.9B 级别 VLM，通常需要 GPU/较大显存与 transformers 依赖，难以作为实时短文本 OCR。  
  **mitigation**: 明确只作为离线/非实时复杂候选；不进入实时链。  
  **owner_phase**: ModelOCR-002 (policy), ModelOCR-004 (benchmark)

- **risk_id**: `r_vl_output_markdown_bias`  
  **candidate_id**: `paddleocr_vl_series`  
  **risk_type**: output_semantics  
  **severity**: high  
  **description**: 输出可能偏向结构化解析/markdown，容易越界为“语义提炼”。  
  **mitigation**: 适配层强约束为 raw text candidates；禁止 summary/指令字段。  
  **owner_phase**: ModelOCR-003/004

#### 2.4 DeepSeek-OCR / OCR-2（B/C 类对照）

- **risk_id**: `r_deepseek_gpu_and_stack`  
  **candidate_id**: `deepseek_ocr_family`  
  **risk_type**: gpu / dependency  
  **severity**: high  
  **description**: 常见要求 CUDA/torch/vLLM/flash-attn 等，环境重且版本绑定强。  
  **mitigation**: 仅作为对照；不作为第一接入候选；后续独立环境验证。  
  **owner_phase**: ModelOCR-003/004

- **risk_id**: `r_deepseek_generation_semantics`  
  **candidate_id**: `deepseek_ocr_family`  
  **risk_type**: output_semantics  
  **severity**: high  
  **description**: 模型常以 prompt 驱动生成“文档转 markdown”，非常容易混入总结/结构化重写。  
  **mitigation**: 后续若纳入对比，必须限制 prompt 与后处理只提取 raw text；审计输出。  
  **owner_phase**: ModelOCR-004

