# LUNA Mainline Runtime Readiness Capability Status Matrix v0（Phase-006）

**Phase**：Phase-Mainline-RuntimeReadiness-006  
**用途**：按能力（YOLO / OCR / Qwen Voice）汇总 **definition → gate → hook → observability** 收口状态。

---

## 1. 矩阵列（机器可读镜像）

运行 `run_mainline_runtime_readiness_regression_v0.py` 生成的 `mainline_runtime_readiness_capability_matrix.json` 每行包含：

| 字段 | 含义 |
|------|------|
| `capability` | `yolo` / `ocr` / `qwen_voice` |
| `trial_name` | `*_guarded_trial_v1` / `qwen_voice_governed_entry_trial_v1` |
| `definition_002` | Phase-002 汇总 JSON 是否存在（或文档锚点） |
| `gate_module_003` | 仓库内 gate/trw/abort 模块齐备 |
| `hook_wrapper_in_repo` | 对应 `*_guarded_trial_hook_v0.py` 存在 |
| `hook_result_default_env_004` | Phase-004 `default_env` hook 结果中含该能力 |
| `observability_stage_005` | Phase-005 RequestTrace stage 列表中含该 trial |

---

## 2. 当前主线结论（语义）

- 三条 trial 在 **定义与代码结构** 上齐备；**默认**均为 **关闭 / no-op**。  
- **真实推理与播报** 不在本闭包范围内。
