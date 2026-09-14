# Luna — OCR / StaticReading / Poster / RealVideo Regression Route Compliance v1

**Phase**：`OCR-StaticReading-Poster-RealVideo-Regression-RouteCompliance-v1-001`  
**性质**：回归 / 路线合规；只读历史 `_eval_out` 产物；不执行新 runtime

## 验证范围

| 路线 | 预期 |
|------|------|
| RealVideo | Frame Sample → 历史 OCR evidence → readonly consumer；无 fusion / 无事实写入 |
| Poster | Layout Governance → segment_first → TTL/Policy Gate hold；无 SceneDelta / WM |
| StaticReading | RRD → handoff → stub `not_captured` → OCRRequest 全阻断；无 EP v5 |
| Memory | append-only handoff dry-run；无 Memory 写入 |
| Hardware | Adapter Stub；`real_camera_enabled=false`；无采帧 |

## 边界

- `regression_runtime_executed=false`
- 不 camera / 不新 OCR / 不写 WorldModel / Memory
- 所有输出 `fact_status=not_fact`，`write_allowed=false`

## 实现

- `capabilities/midplatform/ocr_staticreading_poster_realvideo_regression_route_compliance_v1.py`
- `tools/evaluation/midplatform/run_ocr_staticreading_poster_realvideo_regression_route_compliance_v1.py`
- `tools/evaluation/midplatform/verify_ocr_staticreading_poster_realvideo_regression_route_compliance_v1.py`

## Smoke 输出

`_eval_out/ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0/`

## 后续

- **OCR-Mainline-Governance-Closure-v1-001** = GO（正式 OCR 治理收口）
