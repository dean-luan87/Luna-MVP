## Phase-ModelOCR-002

OCR Candidate Capability Matrix v0

### 0. 本阶段边界（提醒）

本文件是盘点矩阵，不代表启用、下载或接入 runtime。

### 1. 字段说明（与主线要求对齐）

每个候选至少记录：

- candidate_id
- model_family
- current_version
- release_status
- source_url_or_repo
- local_offline_supported
- requires_network
- requires_api_key
- gpu_required
- cpu_supported
- supported_languages
- supports_chinese / supports_english / supports_digits
- supports_bbox / supports_confidence
- supports_orientation
- supports_layout
- supports_video_frame_input
- expected_input_format
- expected_output_format
- dependency_complexity
- weight_download_method
- license_or_usage_note
- realtime_suitability
- offline_batch_suitability
- navigation_short_text_suitability
- complex_document_suitability
- recommended_priority
- recommended_role
- risks

### 2. 矩阵（v0）

> 备注：以下为“盘点口径”，部分字段需要在 ModelOCR-003 通过实际安装/推理脚本验证后才能从 `unknown` 收敛为确定值；但本阶段不做安装与运行。

| candidate_id | model_family | current_version | source_url_or_repo | local_offline_supported | requires_network | requires_api_key | gpu_required | cpu_supported | supports_zh | supports_en | supports_digits | supports_bbox | supports_confidence | supports_orientation | supports_layout | supports_video_frame_input | expected_input_format | expected_output_format | dependency_complexity | weight_download_method | license_or_usage_note | realtime_suitability | offline_batch_suitability | navigation_short_text_suitability | complex_document_suitability | recommended_priority | recommended_role | risks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| paddleocr_ppocr_pipeline | PaddleOCR / PP-OCR | PaddleOCR v3.5.0; PP-OCRv5 path | `https://github.com/PaddlePaddle/PaddleOCR` | yes | no | no | no (optional) | yes | yes | yes | yes | yes | yes | yes (cls/rotate support typical) | partial (pipeline + PP-Structure optional) | yes | image/frame | raw text + bbox + confidence | medium | repo/models/HF (varies) | Apache-2.0 (repo) | high | high | high | medium | P1 | first_integration_candidate | 依赖较多但成熟；权重管理需 manifest 化；版本演进快 |
| macos_vision_ocr | Apple Vision OCR | macOS Vision (OS-provided) | `https://developer.apple.com/documentation/vision/recognizing_text_in_images` | yes (on-device) | no | no | no | yes | yes (supported langs configurable) | yes | yes | yes (normalized rect; convertible) | yes | partial (orientation handled by image/preprocess; API supports) | limited for complex layout parsing (text-only) | yes | image/frame | raw text + bbox + confidence (via observation/candidate) | low | none (system) | Apple platform SDK terms | medium | medium | high (dev fallback) | low-medium | P2 | fallback_or_baseline_comparator | bbox 为归一化坐标需转换；输出更偏“文本行/片段”，中文 bbox 行切分可能不稳定 |
| paddleocr_vl_series | PaddleOCR-VL | VL-1.5 (0.9B) | `https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5` | yes (likely) | no | no | yes (typical) | unknown/limited | yes | yes | yes | yes (supports text spotting) | unknown (likely) | yes | yes | yes (images; pdf) | image/document | parsed doc + text spotting; may output structured | high | HF/weights | varies (check model card) | low | high | low | high | P3 | complex_document_candidate | 体量/显存/依赖重；输出可能倾向结构化/markdown，需约束为 raw text candidates |
| deepseek_ocr_family | DeepSeek-OCR / OCR-2 | OCR (2025); OCR-2 (2026) | `https://github.com/deepseek-ai/DeepSeek-OCR-2` | yes (GPU) | no | no | yes | no | yes (likely) | yes | yes | unknown/depends | unknown/depends | yes (vision model) | yes (doc parsing) | yes | image/document | often image→text/markdown | very high | HF/download | MIT (OCR) / Apache-2.0 (OCR-2) | low | medium-high | low | high | P4 | comparator_only | 强依赖 CUDA/torch/vLLM/flash-attn；非轻量；输出形态偏“生成式文档转写”，需强约束避免语义提炼 |

### 3. A/B/C 分层映射（v0）

- A 类（轻量导航 OCR）：`paddleocr_ppocr_pipeline`
- B 类（复杂版面 OCR / OCR-VL）：`paddleocr_vl_series`, `deepseek_ocr_family`
- C 类（对照/ fallback）：`macos_vision_ocr`

