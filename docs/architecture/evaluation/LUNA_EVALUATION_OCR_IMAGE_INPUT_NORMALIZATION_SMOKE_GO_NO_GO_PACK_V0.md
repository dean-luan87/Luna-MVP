# OCR Image Input Normalization Smoke — GO / NO_GO Pack v0

## GO（本阶段验收）

1. **小图与大图** smoke 均 `success`，verifier 报告 `verdict=GO`。  
2. **Provider Input Pack** 存在且通过 `validate_provider_input_pack_v0`。  
3. **大图** `input_gate.oversized=true`，且 **audit** 中 `original_image_used_directly` ≠ `true`。  
4. **降采样** 路径下：`downscale_applied=true` ⇒ `coordinate_transform_matrix` 与 pack 顶层 `coordinate_transform` 字段完整。  
5. `input_units` 非空；`source_chain` 含 `build_provider_input_pack` 等关键节点。  
6. **Stub** 的 `provider_result.input_pack_id` 非空（证明消费了 input pack）。  
7. **禁止类 audit** 不得为 `true`：`real_provider_invoked`、`paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written`。

## CONDITIONAL_GO（记录用，本 verifier 仅输出 NO_GO）

- 大图策略或坐标矩阵仍待补齐，但 **未**发生原图直通 provider。  
- 或大图被 **正确 REJECT** 且未调用真实 OCR（本阶段主线目标为 downscale 成功路径，故默认不以此作为 GO）。

## NO_GO（硬失败）

- 大图仍以原图作为 provider 输入（`original_image_used_directly=true`）。  
- 超限仍生成「未降采样整图」作为唯一实时输入且无有效坐标变换。  
- 调用真实 OCR 或修改 routing / 写入 MidPlatform / WorldModel。  
- 缺 `source_chain` / `input_units` / metadata probe 等关键产物。
