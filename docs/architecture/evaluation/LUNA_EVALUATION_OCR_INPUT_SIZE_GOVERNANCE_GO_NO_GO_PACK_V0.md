# Luna Evaluation — OCR Input Size Governance GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`

## GO（治理包闭环）

1. **ImageInputGate**、**像素预算**、**ROI-first**、**downscale**、**tiling**、**坐标重建**、**source chain**、**STCM 协同** 均有独立文档 + `ocr_image_input_governance_v0.example.json` 字段对应。  
2. `full_image_realtime_allowed=false` 且 `roi_first_required=true`。  
3. 文档明确引用 **paddleocr_failed_sample_isolation_v0** 的 **size_sensitive** 实证。  
4. 文档 **禁止** 超大图无治理直进实时 OCR；**禁止** tile 结果丢弃坐标映射。  
5. Verifier `verify_ocr_input_size_governance_v0.py` 输出 **GO**。

## CONDITIONAL_GO

- 文档与配置齐全，但具体阈值（如 `tile_max_side`）标为「待负载实测调参」。  
- 部分路径仅定义 async，未定义 sync 上限（需在下一轮补全）。

## NO_GO（任一即不合格）

- 未禁止 **超大图整图实时 OCR**，或配置允许 `full_image_realtime_allowed=true` 且无等效硬闸门描述。  
- 未定义 **ROI-first**、**downscale**、**tiling** 之一。  
- 未定义 **坐标回填** 或允许丢弃 tile 坐标。  
- 未定义 **source chain** 或 **STCM** 超时/过期语义。  
- 允许 OCR 结果 **直写** MidPlatform / WorldModel。

## 一句话

本包 **GO** 只表示「输入治理规范与静态校验闭环」；**不**表示 PaddleOCR 或任意 provider 已全量稳定。
