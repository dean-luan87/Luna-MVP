# LUNA — RapidOCR Capability Status Matrix v0

## Phase

- **Phase-ModelOCR-004C-Closure**
- **Subject:** **RapidOCR + ONNXRuntime** 在 Luna OCR 主线中的**冻结状态**（相对 004C 归档跑）。

## Matrix

| Dimension | Status | Notes |
|-----------|--------|--------|
| **raw_text_candidate** | **done** | 004C harness + verifier **GO**；仅 **raw text** 合同 |
| **lightweight_candidate** | **ready** | 依赖 wheel 内 ONNX；本地推理路径成立 |
| **realtime_candidate** | **conditional** | ~**106 ms/帧**、~**9.4 FPS**（归档观测）；**未**经场景级延迟 SLA 与 GT 准确率验收 |
| **default_ocr_source** | **not_yet** | **禁止**单独设为默认 OCR；需 **005/006/Closure** 决策 |
| **semantic_understanding** | **prohibited** | 与全局 OCR raw-text 合同一致 |
| **downstream_integration** | **not_allowed** | 不接 SceneTask/Fusion/Output |

## 与 Vision / Paddle 关系（只读）

| 引擎 | 定位 |
|------|------|
| **macOS Vision** | fallback / 对照基线；~460 ms/帧，**非实时主力** |
| **RapidOCR** | 轻量 **候选**；延迟优于 Vision；**无 GT benchmark 前不升格默认** |
| **PaddleOCR** | 主候选之一（准确率路径）；**pinned_partial** → **004B** |

## Version

- **v0** — 与 004C Closure 同城；基准数字变更时升版或附录。
