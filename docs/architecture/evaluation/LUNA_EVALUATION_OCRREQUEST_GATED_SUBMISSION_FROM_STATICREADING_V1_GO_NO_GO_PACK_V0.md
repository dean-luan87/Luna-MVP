# GO / NO-GO Pack — OCRRequest Gated Submission from StaticReading v1

## GO

- 26 handoff / 34 region；`capture_status=not_captured`  
- 34 条 `ocr_input_allowed_now=false`；34 blocked OCRRequest candidates  
- future payload schema；EP v5 / Semantic / SV future plans  
- 无 OCR / provider / Memory / WM 写入；verifier=GO

## CONDITIONAL_GO

- 阻断为预期；无 captured frame 为预期

## NO_GO

- 提交 OCRRequest / 运行 OCR / provider bypass  
- mock text / full frame OCR / EP v5 现在生成  
- 写 Memory / WM / profile fact / routing change
