# LUNA OCR Guarded Trial Hook-In v0

**Phase**：Phase-Mainline-RuntimeReadiness-004  \n
**Hook wrapper**：`capabilities/runtime_readiness/ocr_guarded_trial_hook_v0.py`  \n
**候选挂接点**：`capabilities/model_ocr/offline_source_policy_v0.py::select_ocr_offline_source_v0`

---

## 目标

在 OCR source policy selector 入口挂接 gate 评估，但 **不得**改变 provider 选择与默认 offline policy 语义；默认必须 no-op。

---

## 默认行为（必须）

- gate decision 默认 `disabled`
- hook result `enabled=false`、`no_op=true`
- 不触发 OCR provider 调用
- 不开启语义下游（`semantic_interpretation_enabled` 仍受原逻辑约束）

---

## 禁止项

- 不调用任何 OCR provider
- 不进入下游/导航/世界模型
- 不改变默认 `DEFAULT_OFFLINE_OCR_CHAIN`

