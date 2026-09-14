# LUNA — macOS Vision OCR Raw Text Harness Closure Review v0

## Phase

- **Phase-ModelOCR-004A-Closure**
- **Purpose:** 正式复审 **Phase-ModelOCR-004A** 一次代表性运行与 verifier 结论，完成收口；**不新增代码**。

## Recorded run（归档）

| 项 | 值 |
|----|-----|
| **video_path** | `/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4` |
| **frame_step** | `30` |
| **max_sampled_frames** | `100` |
| **output_root** | `logs/macos_vision_ocr_raw_text_004a_20260429_094308` |
| **samples** | `100` |
| **Wall-clock（观测）** | 约 **46 秒**（100 帧 OCR，单机 macOS；非严格基准测试） |
| **折算吞吐（观测）** | 约 **0.46 秒/帧**；约 **2.1 FPS**（非实时；不适合 Luna 实时/准实时 OCR 主力，尤其导航读牌/出口等低延迟场景） |

## Harness 摘要（`ocr_raw_text_summary.json` 对齐）

| 指标 / 状态 | 值 |
|-------------|-----|
| **provider_available** | `true` |
| **ocr_result_generated_rate** | `1.0` |
| **raw_text_candidate_schema_valid_rate** | `1.0` |
| **bbox_present_or_declared_rate** | `1.0` |
| **confidence_present_or_declared_rate** | `1.0` |
| **raw_text_joined_present_rate** | `1.0` |

## Governance（硬边界达成）

| 字段 | 值 |
|------|-----|
| **semantic_interpretation_enabled** | `false` |
| **allows_execute_now** | `false` |
| **downstream_invoked** | `false` |
| **real_tts_invoked** | `false` |

## Verifier（`verify_macos_vision_ocr_raw_text_v0.py`）

| 项 | 结论 |
|----|------|
| **Checks** | A–L 全通过 |
| **verdict** | **GO** |
| **hard_blockers** | `[]` |

## 复审结论（定性）

1. **004A 结论：** **GO**（契约与 verifier 满足），但 **性能不满足实时/准实时 OCR 主力**（约 460 ms/帧量级）。
2. **004A 成立（工程含义）：** OCR **raw text** 离线 harness 已跑通；产物包含 summary / per-sample / trace / replay / whitebox。
3. **角色定位（冻结）：** macOS Vision OCR **仅**作为 **fallback / 对照基线 / Mac 开发期参考**，**不是** Luna 实时 OCR 默认源；见 `LUNA_MACOS_VISION_OCR_CAPABILITY_STATUS_MATRIX_V0.md`。
4. **性能观察：** ~2.1 FPS → **导航场景读出口/门牌/方向牌等低延迟需求不适用**；实时链优先评估 **PaddleOCR（pinned_partial + 依赖就绪）** 或 **轻量 ONNX 候选（如 RapidOCR，Phase-ModelOCR-004C）**。
5. **禁止误用：** Vision OCR **不是**最终默认主力 OCR；边界见 `LUNA_MACOS_VISION_OCR_BOUNDARY_REGISTER_V0.md`。

## Closure verdict

- **Phase-ModelOCR-004A-Closure：** **GO**（见 `LUNA_MACOS_VISION_OCR_CLOSURE_GO_NO_GO_PACK_V0.md`）。

## Recommended next（文档层面）

**优先 ModelOCR-004B：** PaddleOCR Raw Text Adapter Skeleton + **Dependency Readiness**（fail-closed；与 benchmark 隔离）。

可选并行叙事：**ModelOCR-005** OCR Ground Truth / raw text benchmark — **不在 Closure 阶段启动实现**。

## Cross-references

- `LUNA_MACOS_VISION_OCR_CAPABILITY_STATUS_MATRIX_V0.md`
- `LUNA_MACOS_VISION_OCR_BOUNDARY_REGISTER_V0.md`
- `LUNA_MACOS_VISION_OCR_RAW_TEXT_HARNESS_V0.md`
