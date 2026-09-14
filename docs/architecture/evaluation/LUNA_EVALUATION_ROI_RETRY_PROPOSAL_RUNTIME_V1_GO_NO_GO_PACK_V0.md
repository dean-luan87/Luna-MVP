# Luna — ROI Retry Proposal Runtime v1 GO/NO_GO Pack v0

## GO

- `require_roi_retry` 分支正确 intake（smoke：27 项）
- `roi_retry_proposal_generated=true`；`proposal_count > 0`
- `roi_crop_executed=false`；`ocr_request_generated=false`；`ocr_invoked=false`；`provider_invoked=false`
- `no_write_boundary`：`boundary_ok=true`；`violations=[]`；`verifier=GO`

## CONDITIONAL_GO

- proposal 数量随输入变化（非固定 27）
- 部分 `proposed_roi_bbox_xyxy=null`，但 `bbox_source=future_detector_required` 或 `proposal_type=better_frame_required`
- SQ_E 项路由 `hold_low_quality` 仍生成 better-frame proposal（不执行 OCR）

## NO_GO

- 执行真实 crop；生成 OCRRequest；调用 OCR provider
- 生成 Evidence Pack / Semantic Candidate；写 fact / WM / Scene Delta
- benchmark / provider comparison claim；改 runtime routing；audit 缺失
