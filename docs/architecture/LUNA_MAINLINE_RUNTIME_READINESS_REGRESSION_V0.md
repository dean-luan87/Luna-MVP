# LUNA Mainline Runtime Readiness Regression v0（Phase-006）

**Phase**：Phase-Mainline-RuntimeReadiness-006  
**定位**：对 Phase-001～005 进行 **只读回归汇总**，不接真实 runtime、不接 provider、不做白盒产品化。

---

## 1. 工具

| 脚本 | 作用 |
|------|------|
| `tools/run_mainline_runtime_readiness_regression_v0.py` | 聚合历史 `logs/` 产物与仓库锚点，写出 regression / matrix / closure JSON |
| `tools/verify_mainline_runtime_readiness_regression_v0.py` | 校验汇总产物与冻结边界字段 |

默认输入根（可通过 CLI 覆盖；缺失则记入 `missing_roots`，不致命退出）：

- `logs/mainline_runtime_readiness_001_20260506_final`
- `logs/mainline_guarded_trial_definition_002_20260506_final`
- `logs/mainline_guarded_trial_wiring_path_003_final`
- `logs/mainline_guarded_trial_hook_in_004_final`
- `logs/mainline_guarded_trial_hook_observability_005_*`（取最新 mtime）

---

## 2. 输出目录

`logs/mainline_runtime_readiness_regression_006_<UTC>/`

含：`mainline_runtime_readiness_regression_summary.json`、`phase_matrix`、`capability_matrix`、`gate_hook_matrix`、`observability_matrix`、`boundary_summary`、`closure_recommendation.json`、`regression_notes.md`。

---

## 3. 边界

与 Phase-001～005 一致：**不**激活真实 trial、**不**调用 Qwen/TTS/播报、**不**改主链 YOLO/OCR/Voice 实现、**不**展开白盒后台或 UI。
