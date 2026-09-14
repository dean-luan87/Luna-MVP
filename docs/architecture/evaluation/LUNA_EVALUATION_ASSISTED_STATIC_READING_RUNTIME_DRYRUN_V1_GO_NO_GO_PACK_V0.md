# GO / NO_GO — Assisted Static Reading Runtime DryRun v1

## GO

- mode entry + FSM 停在 `WAITING_FOR_USER_STABILIZATION`
- readiness 不伪造通过；`static_capture_ready_now=false`
- `ocrrequest_eligible_now=false`，`eligible_later=true`
- `final_decision=WAIT_FOR_USER_STABILIZATION`
- 无 runtime action；verifier=GO

## NO_GO

- TTS/VOP/camera/OCR/OCRRequest/事实层写入
- 伪造 `static_capture_ready_now=true` 或 `ocrrequest_eligible_now=true`

## 一句话

Runtime dry-run 验证静态阅读路径可推进到等待用户停稳，不执行采集与 OCR。
