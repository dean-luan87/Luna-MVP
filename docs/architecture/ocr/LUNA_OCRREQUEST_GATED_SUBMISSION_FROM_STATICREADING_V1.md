# Luna — OCRRequest Gated Submission from StaticReading v1

**Phase**：`OCRRequest-Gated-Submission-from-StaticReading-v1-001`  
**性质**：gate dry-run only；验证无 captured frame 时 OCRRequest 阻断，并定义 future payload schema

## 当前状态（冻结）

- RRD：34 readable region candidates，26 static capture handoff candidates  
- Hardware Adapter Stub：`capture_status=not_captured`，`frame_ref=null`  
- **OCRRequest**：`eligible_now=false`，`submitted_now=false`

## 决策

**Final**：`BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME`

## 未来链路（capture 成功后）

`static_capture_result` → OCRRequest payload → raw OCR → EP v5 → Semantic v5 → SV v3（均 later；须保留 Memory Governance `source_chain`）

## 实现

- `capabilities/ocr_runtime/ocrrequest_gated_submission_from_staticreading_v1.py`  
- `tools/evaluation/ocr/run_ocrrequest_gated_submission_from_staticreading_v1.py`  
- `tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_staticreading_v1.py`

## 建议下一 phase

- **Return-To-Software-Mainline-Closure-v1**（推荐）  
- `Evidence-Pack-Adapter-v5-StaticReading`  
- `Hardware-Camera-Control-GuardedTrial-Precheck-v1`

## 软件主线收口

[../midplatform/LUNA_RETURN_TO_SOFTWARE_MAINLINE_CLOSURE_V1.md](../midplatform/LUNA_RETURN_TO_SOFTWARE_MAINLINE_CLOSURE_V1.md) — 本 gate 已正式闭合于 Closure v1。
