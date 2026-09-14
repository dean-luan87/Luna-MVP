# Vision 外部 Supervision 适配实验 — GO / CONDITIONAL_GO / NO_GO v0

**Phase**：`Phase-Vision-External-Supervision-Adapter-Experiment-001`  
**Verifier**：`tools/evaluation/vision/verify_external_supervision_adapter_experiment_v0.py`

## GO

- 所有必需产物存在（probe、synthetic、roi candidate、feature matrix、audit、summary）。  
- `external_supervision_availability_probe.json` 中 `supervision_installed == true`（可 import）。  
- `vision_roi_proposal_candidate.json` 中 `roi_items` 数量 ≥ 1；每项含 `bbox_in_frame`（四元组）；candidate 含 `source_frame_id` 或 `source_image_ref`；`source_chain` 非空。  
- `external_supervision_audit_report.json`：`supervision_import_attempted == true`；`yolo_invoked`、`real_detector_invoked`、`navigation_decision_invoked`、`midplatform_fact_written`、`scene_delta_written`、`world_model_written`、`ai_interpretation_invoked`、`runtime_mainline_modified` 均为 **false**。  
- `external_supervision_adapter_experiment_summary.json` 中 **`supervision_marked_as_default_vision_module` 不得为 true**。

## CONDITIONAL_GO

- `supervision_installed == false`，但 **import_error** 已记录，且 summary 中 **`supervision_install_gap_report.complete == true`**（缺口报告完整）。  
- 合成 ROI candidate 与 audit 仍满足上述结构与安全字段；**无**越界写入或主线接管声明。

## NO_GO

- 缺任一必需产物或 ROI 结构不满足。  
- audit 缺失或任一禁止字段非 false、`supervision_import_attempted` 非 true。  
- 将 Supervision 标为默认 Vision 模块（`supervision_marked_as_default_vision_module == true`）。  
- 未安装 Supervision 且 **无**完整缺口报告（无法满足 CONDITIONAL 条件）。

## 非宣称

通过本实验 **不等于** Supervision 已纳入 Luna 主线；**不等于** 可跳过 Frame Input Governance / ROI stub；**不等于** 已做生产级 A/B 或证据治理。
