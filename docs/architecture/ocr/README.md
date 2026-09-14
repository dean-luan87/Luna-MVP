# Luna OCR 架构文档索引

本目录收录 **OCR 输入侧治理** 与 **证据链** 相关规范（静态设计层，不替代运行时实现）。

**架构原则（已冻结）**：[LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](./LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md) — OCR 为任务型精确识别，**非**世界建模默认主通道；后续 **OCR Activation Gate** 按本原则分层。

**中台级总纲**（图像类输入统一治理、质量闸 + 规格闸 + 性能感知规划）：见上一级 [LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md](../LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md)。

## OCR 主线阶段判定（当前建议写法）

| Phase ID | 建议判定 |
|----------|----------|
| OCR-Provider-Runtime-Governance-Standard-001 | GO（文档与静态验收；见 [LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md](./LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md)） |
| OCR-Input-Size-Governance-001 | GO（评测与治理包；见 evaluation 索引） |
| OCR-Mainline-Minimal-Bridge-001 | GO |
| OCR-Mainline-InputGate-Reject-Smoke-001 | GO |
| OCR-ImageInput-Normalization-Pipeline-001 | GO |
| OCR-Tile-Planner-And-Coordinate-Reconstruction-001 | GO |
| OCR-Tile-Coverage-And-Truncation-Policy-001 | GO |
| OCR-Tile-Evidence-Merge-Stub-001 | GO |
| OCR-Real-Provider-Adapter-Selection-001 | GO（以 `verify_ocr_provider_selection_smoke_v0` 为准） |
| OCR-Lightweight-Real-Provider-Adapter-001 | GO（以 `verify_ocr_lightweight_real_provider_adapter_smoke_v0` 为准；RapidOCR 依赖可选） |
| OCR-Lightweight-Provider-Text-Smoke-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_lightweight_provider_text_smoke_v0` 为准） |
| OCR-Lightweight-Provider-Normalized-Input-Smoke-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_lightweight_provider_normalized_input_smoke_v0` 为准） |
| OCR-Lightweight-Provider-ROI-Input-Smoke-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_lightweight_provider_roi_input_smoke_v0` 为准） |
| OCR-ROI-Evidence-Coordinate-Lift-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_roi_coordinate_lift_smoke_v0` 为准） |
| OCR-Lightweight-Provider-Multi-ROI-Smoke-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_lightweight_provider_multi_roi_smoke_v0` 为准） |
| OCR-Evidence-Consumer-ReadOnly-Smoke-001 | **GO 或 CONDITIONAL_GO**（以 `verify_ocr_evidence_readonly_consumer_smoke_v0` 为准；只读消费 `bridge_pack`，不写中台事实层） |
| OCR-Request-Submission-Gated-Smoke-001 | **GO 或 CONDITIONAL_GO**（Vision ROI candidate → `ocr_mainline_bridge` stub submission，evaluation-only） |
| OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001 | **GO 或 CONDITIONAL_GO**（Vision ROI → bridge → RapidOCR lightweight，evaluation-only） |
| Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001 | **GO**（RapidOCR submission collection 只读消费；空文本=有效 real 结果） |
| Vision-ROI-Text-Bearing-Sample-For-OCR-001 | **GO 或 CONDITIONAL_GO**（本地含字 ROI → bridge → RapidOCR 非空文本探针） |
| Vision-OCR-Evidence-ReadOnly-Consumer-001 | **GO 或 CONDITIONAL_GO**（只读消费 Vision-triggered OCR submission collection） |
| OCR-Partial-Evidence-Completion-Policy-001 | **DESIGN_RECORDED / FIELD_RESERVED**（策略与 merge 字段已落盘；无独立 phase verifier 前不宣称 GO） |
| OCR-Poster-Layout-Segmentation-Governance-001 | **GO**（海报版面治理 stub；`segment_first`，无 OCR） |
| OCR-Poster-Region-OCR-Plan-Stub-001 | **GO**（区域 OCR 计划 stub；仅 text regions） |
| OCR-Poster-VisualSymbolEvidence-Stub-001 | **GO**（Logo/QR/visual symbol 证据 stub） |
| Poster-Real-OCR-Gated-Execution-001 | **GO 或 CONDITIONAL_GO**（4 text regions gated real OCR；经 bridge；以 `verify_poster_real_ocr_gated_execution_v0` 为准） |
| Poster-Real-OCR-ReadOnly-Consumer-001 | **GO 或 CONDITIONAL_GO**（只读消费 layout text evidence；以 `verify_poster_real_ocr_readonly_consumer_v0` 为准） |
| CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001 | **GO 或 CONDITIONAL_GO**（RealVideo upper_sign_roi gated OCR submission；以 `verify_realvideo_ocr_request_gated_submission_v0` 为准） |
| RealVideo-OCR-Evidence-ReadOnly-Consumer-001 | **GO 或 CONDITIONAL_GO**（RealVideo OCR evidence 只读消费；以 `verify_realvideo_ocr_evidence_readonly_consumer_v0` 为准） |

| 文档 | 作用 |
|------|------|
| [LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](./LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md) | **已冻结**：OCR 任务导向能力原则；世界建模主路径 vs 精读链；OCR Activation Gate 占位。 |
| [LUNA_OCR_IMAGE_INPUT_GATE_V0.md](./LUNA_OCR_IMAGE_INPUT_GATE_V0.md) | ImageInputGate：所有 OCR 输入必经闸门与分支策略。 |
| [LUNA_OCR_IMAGE_SIZE_AND_PIXEL_BUDGET_POLICY_V0.md](./LUNA_OCR_IMAGE_SIZE_AND_PIXEL_BUDGET_POLICY_V0.md) | 宽高与像素预算、超限分流。 |
| [LUNA_OCR_ROI_FIRST_INPUT_POLICY_V0.md](./LUNA_OCR_ROI_FIRST_INPUT_POLICY_V0.md) | 实时路径 ROI-first 默认策略。 |
| [LUNA_OCR_DOWNSCALE_AND_TILING_POLICY_V0.md](./LUNA_OCR_DOWNSCALE_AND_TILING_POLICY_V0.md) | 降采样与分块（tiling）策略及上限。 |
| [LUNA_OCR_TILE_COORDINATE_RECONSTRUCTION_POLICY_V0.md](./LUNA_OCR_TILE_COORDINATE_RECONSTRUCTION_POLICY_V0.md) | 分块坐标到原图坐标的回填与去重。 |
| [LUNA_OCR_MAINLINE_MINIMAL_BRIDGE_V0.md](./LUNA_OCR_MAINLINE_MINIMAL_BRIDGE_V0.md) | 最小主线桥接骨架：request → gate → stub → evidence → bridge candidate（不接生产 routing）。 |
| [LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md](./LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md) | Provider runtime 治理总纲：dispatch、闸门与业务侧禁止直连 provider。 |
| [LUNA_OCR_IMAGE_INPUT_NORMALIZATION_PIPELINE_V0.md](./LUNA_OCR_IMAGE_INPUT_NORMALIZATION_PIPELINE_V0.md) | 图像输入规范化链：probe → decision → 安全归一化 → Provider Input Pack（不接真实 OCR）。 |
| [LUNA_OCR_TILE_PLANNER_AND_COORDINATE_RECONSTRUCTION_V0.md](./LUNA_OCR_TILE_PLANNER_AND_COORDINATE_RECONSTRUCTION_V0.md) | 超大图 tile 规划、裁剪落盘与逐 tile 坐标元数据（不接真实 OCR）。 |
| [LUNA_OCR_TILE_COVERAGE_AND_TRUNCATION_POLICY_V0.md](./LUNA_OCR_TILE_COVERAGE_AND_TRUNCATION_POLICY_V0.md) | 同步 tile 截断下的覆盖率、partial 证据语义与 source_chain 披露。 |
| [LUNA_OCR_TILE_EVIDENCE_MERGE_STUB_V0.md](./LUNA_OCR_TILE_EVIDENCE_MERGE_STUB_V0.md) | 多 tile stub 证据合并、坐标回填与 bridge_pack 扩展字段。 |
| [LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md) | 局部证据补全候选：分层、披露、风险闸门与 STCM/记忆/用户确认衔接（占位字段已挂 merge）。 |
| [LUNA_OCR_RUNTIME_PROVIDER_ADAPTER_SELECTION_V0.md](./LUNA_OCR_RUNTIME_PROVIDER_ADAPTER_SELECTION_V0.md) | Provider adapter 契约、registry、selection 与 audit（默认 stub；真实引擎仅占位且默认 disabled）。 |
| [LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md](./LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md) | RapidOCR 轻量真实 adapter：flag、input_pack 边长闸门、health/estimate_cost、与主线衔接。 |
| [LUNA_OCR_PROVIDER_INPUT_PACK_V0.md](./LUNA_OCR_PROVIDER_INPUT_PACK_V0.md) | `ocr_provider_input_pack_v0` 字段与语义摘要。 |
| [LUNA_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md](./LUNA_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md) | Vision ROI OCRRequest candidate 经 mainline bridge 的 gated submission（stub，evaluation-only）。 |
| [LUNA_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md) | Vision-triggered OCR submission collection 只读消费者（candidate/frame/roi 索引）。 |
| [LUNA_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md](./LUNA_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md) | Vision ROI OCRRequest → mainline bridge → RapidOCR lightweight（gated，evaluation-only）。 |
| [LUNA_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md](./LUNA_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md) | RealVideo upper_sign_roi OCRRequest → mainline bridge → RapidOCR（gated，evaluation-only）。 |
| [LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md) | RealVideo OCR evidence collection 只读消费与四类索引（evaluation-only）。 |
| [LUNA_VISION_TRIGGERED_RAPIDOCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_TRIGGERED_RAPIDOCR_EVIDENCE_READONLY_CONSUMER_V0.md) | RapidOCR submission collection 只读消费者（含 stub 对照）。 |
| [LUNA_VISION_ROI_TEXT_BEARING_OCR_SAMPLE_V0.md](./LUNA_VISION_ROI_TEXT_BEARING_OCR_SAMPLE_V0.md) | 含字 Vision ROI 本地 fixture → bridge → RapidOCR 非空 OCR 探针（evaluation-only）。 |
| [LUNA_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md](./LUNA_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md) | 海报版面分区治理 stub（禁止整图 OCR 默认路径）。 |
| [LUNA_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md](./LUNA_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md) | 海报 text 区域 OCR 计划 stub（不执行 OCR）。 |
| [LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md](./LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md) | Poster 4 区 gated real OCR smoke（RapidOCR + bridge；非事实证据候选）。 |
| [LUNA_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md](./LUNA_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md) | Poster real OCR evidence 只读消费者（索引/矩阵/TTL guard；不重跑 OCR）。 |
| [LUNA_OCR_POSTER_VISUAL_SYMBOL_EVIDENCE_STUB_V0.md](./LUNA_OCR_POSTER_VISUAL_SYMBOL_EVIDENCE_STUB_V0.md) | Logo/QR/visual symbol 证据 stub（与 OCR 链分流）。 |

评测侧配套见 `docs/architecture/evaluation/` 下 **OCR Input Size Governance**、**Mainline Minimal Bridge Smoke**、**Image Input Normalization Smoke**、**OCR Provider Selection Smoke**、**OCR Lightweight Real Provider Adapter Smoke**、**OCR Lightweight Provider Text Smoke**、**OCR Lightweight Provider Normalized Input Smoke**、**OCR Lightweight Provider ROI Input Smoke**、**OCR ROI Coordinate Lift Smoke**、**OCR Lightweight Provider Multi-ROI Smoke** 与 **OCR Evidence Read-Only Consumer Smoke** 文档。

**实证依据**：`Phase-PaddleOCR-Failed-Sample-Isolation-001` 产物目录  
`_eval_out/paddleocr_failed_sample_isolation_v0`（`labeled_007` / `labeled_019` 同图 **size_sensitive**；`labeled_010` 大图 **size_sensitive** 且 **native 风险残留**）。**禁止**据此放宽「整图大图实时 OCR」。
