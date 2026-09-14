# LUNA Mainline Guarded Trial Hook Observability v0（Phase-005）

**Phase**：Phase-Mainline-RuntimeReadiness-005  
**定位**：在 **不改 Phase-004 hook 逻辑**、**不启用真实 trial**、**不调 provider / 不播报 / 不 TTS** 的前提下，将 Phase-004 `hook-in` 产物映射为 **RequestTrace shadow stage**、观测矩阵、副作用审计导出与可查询表，使闸门在白盒侧 **可见、可查、可审计**。

---

## 1. 输入 / 输出

| 角色 | 路径 |
|------|------|
| Hook-in 输入根（Phase-004） | `logs/mainline_guarded_trial_hook_in_004_final/`（或任意 `--hook-root`，须含 `mainline_guarded_trial_hook_results.json`） |
| 观测产物根（Phase-005） | `logs/mainline_guarded_trial_hook_observability_005_<UTC>/` |

**工具**：

- `tools/evaluate_mainline_guarded_trial_hook_observability_v0.py`
- `tools/verify_mainline_guarded_trial_hook_observability_v0.py`

---

## 2. 产出文件

- `mainline_guarded_trial_hook_observability_summary.json` — 元数据、`input_hook_results_sha256`、约束声明  
- `mainline_guarded_trial_hook_request_trace_stages.json` — 三条 capability 的 shadow stage 列表（`default_env` canonical）  
- `mainline_guarded_trial_hook_observability_matrix.json` — 观测矩阵  
- `mainline_guarded_trial_hook_side_effect_audit_export.json` — 副作用审计导出  
- `mainline_guarded_trial_hook_query_table.json` — 静态查询表（本阶段无 CLI query）  
- `mainline_guarded_trial_hook_trace.jsonl` / `replay.jsonl` / `whitebox.jsonl` — TRW 对齐占位（非空）  
- `evaluation_notes.md` — 运行备注  

---

## 3. Stage 命名空间

- `stage_name`：`request_trace.stage.runtime_readiness.guarded_trial_hook`  
- `stage_namespace`：`mainline_runtime_readiness_v0`  

详见：`docs/architecture/LUNA_MAINLINE_GUARDED_TRIAL_HOOK_REQUEST_TRACE_STAGE_MAPPING_V0.md`。

---

## 4. 边界（冻结）

本阶段 **仅只读** Phase-004 JSON；**不**修改 `yolo/ocr/qwen_voice` hook 实现；**不**把 hook 从 no-op 改为真实执行；**不**改 provider 默认策略与 env 语义。
