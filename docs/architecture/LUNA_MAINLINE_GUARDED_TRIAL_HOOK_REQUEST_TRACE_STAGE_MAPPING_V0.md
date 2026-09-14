# LUNA Mainline Guarded Trial Hook → RequestTrace Stage Mapping v0

**Phase**：Phase-Mainline-RuntimeReadiness-005  
**源**：`mainline_guarded_trial_hook_results.json` 中 `scenario == "default_env"` 的 `hook_result` 行（YOLO / OCR / Qwen Voice 各一条）。

---

## 1. Shadow stage 记录（每条 hook 一条）

| 字段 | 来源 |
|------|------|
| `stage_name` | 常量 `request_trace.stage.runtime_readiness.guarded_trial_hook` |
| `stage_namespace` | 常量 `mainline_runtime_readiness_v0` |
| `trial_name` | `hook_result.trial_name` |
| `capability` | `hook_result.capability`（`yolo` \| `ocr` \| `qwen_voice`） |
| `hook_result_id` | `hook_result.hook_result_id` |
| `gate_decision_ref` | `hook_result.gate_decision_ref` |
| `enabled` | `hook_result.enabled` |
| `no_op` | `hook_result.no_op` |
| `reason` | `hook_result.reason` |
| `global_kill_switch` | `hook_result.debug.gate_decision.global_kill_switch` |
| `trial_mode` | `hook_result.debug.gate_decision.trial_mode` |
| `hard_audit` | 由 `hook_result` 副作用字段组装（与 schema 一致） |
| `trace_ref` / `replay_ref` / `whitebox_ref` | 指向本阶段输出目录内对应 jsonl 与 `hook_result_id`（人类可读引用） |

---

## 2. 非目标

- 不在运行时 RequestTrace 管线内 **嵌入** 执行路径；本阶段仅为 **离线对齐 / 导出**。  
- 不把 Phase-004 的多 scenario 全部展开为矩阵主行；canonical 观测取 **`default_env`** 三条线。
