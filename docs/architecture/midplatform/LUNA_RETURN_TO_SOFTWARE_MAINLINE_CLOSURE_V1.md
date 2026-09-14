# Luna — Return To Software Mainline Closure v1

**Phase**：`Return-To-Software-Mainline-Closure-v1-001`  
**性质**：阶段性收口；不执行 runtime、不新增能力

## 已闭合链路

| 链路 | 状态 | 最后 Phase | 关键决策 |
|------|------|------------|----------|
| 硬件 | **frozen** | Adapter Stub v1 | `STUB_READY_SOFTWARE_BOUNDARY_CLOSED` |
| 静态阅读 OCR | **blocked_until_captured_frame** | OCRRequest StaticReading Gate v1 | `BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME` |
| Memory Handoff | **handoff_dryrun_ready** | Memory Handoff DryRun v1 | `READY_FOR_MEMORY_GOVERNANCE_HANDOFF_RUNTIME_LATER` |
| WorldModel | not_started_for_write | — | 禁止写入 |
| Fragment Weaving | future_direction_only | — | 仅治理规划 |

## 硬阻断点（预期）

- `capture_status=not_captured` → 34 OCRRequest blocked  
- 无 EP v5 / Semantic v5 / SV v3（缺 OCR result）  
- 硬件 GuardedTrial **later only**

## 最终决策

**`SOFTWARE_MAINLINE_READY_FOR_NEXT_PLANNING`**

## 收口前回归

- **OCR-StaticReading-Poster-RealVideo-Regression-RouteCompliance-v1-001** = CONDITIONAL_GO（见 `LUNA_OCR_STATICREADING_POSTER_REALVIDEO_REGRESSION_ROUTE_COMPLIANCE_V1.md`）

## OCR 治理收口

- **OCR-Mainline-Governance-Closure-v1-001** = GO（`OCR_MAINLINE_CLOSED_FOR_GOVERNANCE`；见 `LUNA_OCR_MAINLINE_GOVERNANCE_CLOSURE_V1.md`）

## 推荐下一批（软件主线）

1. **WorldModel-Lookup-for-Reading-DryRun-v1**  
3. Fragment-Evidence-Weaving-Governance-v1  
4. Emotional-Context-Background-Candidate-DryRun-v1  

## 实现

- `capabilities/midplatform/return_to_software_mainline_closure_v1.py`  
- `tools/evaluation/midplatform/run_return_to_software_mainline_closure_v1.py`  
- `tools/evaluation/midplatform/verify_return_to_software_mainline_closure_v1.py`
