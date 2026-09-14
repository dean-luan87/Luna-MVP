# Luna Evaluation — YOLO Real Positive Sample GO / NO_GO Pack v0

## GO

- `detection_count > 0`，`converted_evidence_count > 0`  
- `detector_mode=real_yolo`，`fixture_used=false`  
- 全部 evidence：`synthetic=false`，`fact_status=not_fact`  
- `network_request_invoked=false`  

## CONDITIONAL_GO

- 真实 YOLO 运行但零检测；或正样本缺失但有 gap report  

## NO_GO

- 触网；改 registry；标 fact；写事实层；导航  
