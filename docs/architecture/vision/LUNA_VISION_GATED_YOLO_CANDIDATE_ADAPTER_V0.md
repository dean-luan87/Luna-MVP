# Luna — Gated YOLO Candidate Adapter v0

**Phase**：`Phase-Vision-Gated-YOLO-Candidate-Adapter-001`  
**性质**：evaluation-only gated adapter — **不接** Vision runtime 主线。

## 目的

在显式环境门控下，验证 **YOLO / Ultralytics**（或 YOLO-like fixture）输出能否转换为 **`vision_detection_evidence_v0`**，且全程 **fact_status=not_fact**。

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `LUNA_YOLO_EVAL_ONLY` | false | 必须为 true 才允许真实 YOLO |
| `LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0` | false | 启用 eval provider |
| `LUNA_YOLO_FORCE_FIXTURE_V0` | false | 强制 fixture |
| `LUNA_YOLO_MODEL_PATH` | — | 可选模型路径 |
| `LUNA_YOLO_MAX_INPUT_UNITS` | 5 | 最多 ROI unit 数 |

## 边界

- 只读 **vision_provider_input_pack_bundle** 中的 ROI crop，**不**整帧主线输入。  
- **不**修改 `vision_provider_registry` 默认值。  
- **不**写 MidPlatform / Scene Delta / WorldModel。

## 评测

[LUNA_EVALUATION_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md](../evaluation/LUNA_EVALUATION_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md)

## 建议下一跳

**Phase-Vision-Gated-YOLO-Real-Smoke-001**：见 [LUNA_VISION_GATED_YOLO_REAL_SMOKE_V0.md](./LUNA_VISION_GATED_YOLO_REAL_SMOKE_V0.md)。
