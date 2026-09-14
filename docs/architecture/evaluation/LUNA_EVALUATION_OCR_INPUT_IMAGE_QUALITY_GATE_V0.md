# LUNA Evaluation Tools — OCR Input Image Quality Gate v0 (Phase-EvaluationTools-OCR-004)

## Why

现有门控已覆盖文件存在性、sha256/size、字体可见性/tofu、GT 一致性、以及 OCR 输出质量指标。  
但 OCR 的稳定性还强依赖 **输入图像质量与像素尺度**（过小/过大/模糊/低对比/曝光/压缩噪声/倾斜/文字尺度/文本占比）。

因此引入一个独立的 Evaluation Tools 阶段：**OCR Input Image Quality Gate & Pixel Scale Validation**。

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox
- 不调用 OCR providers（纯图像统计与启发式）
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence / semantic / 语音链路

## Metrics (v0)

- `image_width` / `image_height`
- `megapixels`
- `blur_score`（Laplacian variance）
- `contrast_score`（gray std）
- `brightness_mean` + `brightness_status`（under/over/normal）
- `compression_artifact_score`（jpeg blockiness 弱检测）
- `text_area_ratio`（阈值/形态学粗估）
- `text_component_height_stats`（近似文字组件高度统计）
- `skew_angle_deg`（Hough lines 弱估计）

## Output (per image; v0)

```json
{
  "image_quality_gate": "GO | CONDITIONAL_GO | NO_GO",
  "image_width": 1200,
  "image_height": 700,
  "megapixels": 0.84,
  "blur_score": 123.4,
  "contrast_score": 32.1,
  "brightness_status": "normal",
  "text_scale_status": "acceptable",
  "text_area_ratio": 0.08,
  "skew_angle_deg": 3.2,
  "scale_action": "accept | upscale | downscale | crop_required | reject",
  "recommended_preprocess": ["none | upscale | downscale | crop_required | deskew"],
  "reason": []
}
```

## Tooling (v0)

- `tools/evaluation/ocr/run_ocr_input_image_quality_gate_v0.py`
  - 支持 `--dataset-root`（manifest）或 `--images-dir`（目录扫描）
- `tools/evaluation/ocr/verify_ocr_input_image_quality_gate_v0.py`

## Notes

v0 是启发式门控，用于评测/样本筛选与后续合同抽象；不应直接接入主线自动决策。

