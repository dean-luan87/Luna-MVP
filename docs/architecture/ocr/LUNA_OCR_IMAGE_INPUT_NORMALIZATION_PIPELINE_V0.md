# LUNA OCR Image Input Normalization Pipeline v0

**阶段**：`Phase-OCR-ImageInput-Normalization-Pipeline-001`  
**实现入口**：`capabilities/ocr_runtime/ocr_image_normalization_pipeline_v0.py`

## 目的

在 **不调真实 OCR**、**不改 routing**、**不进入 MidPlatform / WorldModel** 的前提下，将 `ImageInputGate` 的输出与治理配置结合，形成 **可审计的输入规范化链**：元数据探测 → 规范化决策 →（可选）安全像素处理 → **`ocr_provider_input_pack_v0`**。

**中台总纲**：本阶段实现的是中台图像输入治理中的 **ImageSpecGate（规格子集）+ 最小 PerformanceAwareInputPlanner（无性能控制器接线）+ BestAvailableInputSource 的 OCR 侧最小载体（Input Pack）**。**超大图 tile 路径**见 `Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001`（`LUNA_ENABLE_OCR_TILE_PLANNER_V0`）。**多 tile 证据合并 stub** 见 `Phase-OCR-Tile-Evidence-Merge-Stub-001`；**局部证据补全候选（非事实补全）** 见 [LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md)。质量过滤（**ImageQualityGate**）、性能约束（**PerformanceControllerConstraint**）、STCM 与任务价值联合决策见：[LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md](../LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md)。

## 链路位置

```
OCRRequest → ImageInputGate（规格/像素预算，向 ImageSpecGate 收敛）
  → ImageInputNormalizationPipeline（规范化与组包）
  → OCRProviderInputPack（Best Available Input 的 OCR v0 载体）
  → Stub Provider → Evidence → Bridge
```

## 能力范围（本阶段最小集）

1. **Metadata probe**：宽高、MP、格式、通道、EXIF orientation、指纹等。  
2. **Input decision**：标记 RGB 转换、EXIF、降采样、切块、ROI、拒绝等布尔决策（部分为未来阶段预留）。  
3. **Safe normalization（可选）**：RGBA→RGB、EXIF 转正、按 `preferred_max_side` 降采样；写出 `normalized_image_ref`。  
4. **Coordinate transform**：记录原图与变换后尺寸及 `scale_x` / `scale_y`（含仅元数据恒等变换路径）。  
5. **Source chain**：字符串步骤列表，覆盖探测、变换、写出归一化图、组包等节点。

## 非目标

- 不调用 PaddleOCR / RapidOCR 或任何真实 provider。  
- 不实现完整 tiling / ROI 检测；切块策略仅在闸门与治理层以「决策/理由」形式出现。  
- 不合并多 tile 的 OCR 证据。

## 相关文档

- [LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md](../LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md)  
- [LUNA_OCR_PROVIDER_INPUT_PACK_V0.md](./LUNA_OCR_PROVIDER_INPUT_PACK_V0.md)  
- 评测：`docs/architecture/evaluation/LUNA_EVALUATION_OCR_IMAGE_INPUT_NORMALIZATION_SMOKE_V0.md`
