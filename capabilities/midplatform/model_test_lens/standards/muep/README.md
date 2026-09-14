# MUEP V1 — Minimal Unified Evaluation Protocol

Model Test Lens 统一评估标准，供 OCR / SAM / SLAM / ASR / VLM 等模型共用。

## 统一输入

```json
{
  "model_type": "slam | ocr | sam | asr | vlm",
  "input": { "data": "image | video | sequence", "metadata": {} },
  "task": { "prompt": "", "mode": "single | batch | stream" }
}
```

## 统一输出

```json
{
  "prediction": {},
  "intermediate": {},
  "metrics": {},
  "failure_modes": [],
  "confidence": 0.0
}
```

## 三层 Metric

| Layer | 含义 | 示例 |
|-------|------|------|
| A — Task | 任务正确性 | IoU, ATE, WER |
| B — Robustness | 稳定性 | 低光、运动模糊敏感度 |
| C — Structural | 结构质量 | 轨迹平滑、边界稳定 |

## 统一评分

```
final_score = 0.6 * task + 0.25 * robustness + 0.15 * structural
```

## Failure Mode Taxonomy

见 `failure_mode_taxonomy_v1.json`。

## 治理

- 评估结果为 candidate-only，非 fact
- 不授予 runtime_ready
- 分数用于研发对比，非产品准入唯一依据
