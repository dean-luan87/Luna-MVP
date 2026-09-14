# LUNA — macOS Vision OCR Capability Status Matrix v0

## Phase

- **Phase-ModelOCR-004A-Closure**
- **Subject:** Apple **VNRecognizeTextRequest**（经 Swift bridge）在本仓库中的**能力状态**，避免将 Vision OCR 误标为全功能或实时默认 OCR。

## Matrix（冻结声明）

| Capability dimension | Status | Notes |
|---------------------|--------|--------|
| **raw_text_harness** | **done** | `evaluate_macos_vision_ocr_raw_text_v0.py` + adapter；产物契约满足 004A |
| **fallback_candidate** | **ready** | manifest 侧可作为 system fallback；运行时启用策略不在本文冻结 |
| **comparison_baseline** | **ready** | 可作为 Paddle / 其他 OCR 的离线对照；须同源帧与相同 raw-text 合同 |
| **realtime_default** | **not_claimed** | 约 **0.46 s/帧**、**~2.1 FPS**（100 帧 ~46s）；**不**声明实时、高频默认源 |
| **semantic_understanding** | **prohibited** | 仅 raw text candidates；无语义字段输出义务 |
| **downstream_integration** | **not_allowed** | 不接 SceneTask/Fusion/Output；summary `downstream_invoked=false` |

## PaddleOCR 关系（交叉引用）

| 项 | 状态 |
|----|------|
| PaddleOCR weights | **pinned_partial**（Fix-004）；**非本矩阵运行时默认** |
| Paddle 下一步 | **004B** adapter skeleton + dependency readiness |

## Version

- **v0** — 与 004A Closure 同城归档；若 Vision 路径策略变更，升版或附录修订。
