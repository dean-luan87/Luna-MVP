# LUNA Guarded Trial 验收与回滚 Playbook v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**关联 JSON**：`mainline_guarded_trial_acceptance_matrix.json`、`mainline_guarded_trial_abort_rollback_matrix.json`、`mainline_guarded_trial_matrix.json`

---

## 1. 验收总则

- 每条 trial **独立** 验收；**禁止**混用「一个大开关过了就算」。  
- 验收通过仅允许将对应能力声明至 **R3_guarded_wiring_ready**（见矩阵字段 `max_allowed_readiness_level_after_pass`）。  
- **Global kill**：验收脚本与环境准备须先确认 `LUNA_DISABLE_ALL_GUARDED_TRIALS` 不为 true（除非刻意测 short-circuit）。

---

## 2. YOLO trial playbook

| 阶段 | 动作 |
|------|------|
| 准入 | Global kill=false；`LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1=true`；模式由 `LUNA_YOLO_TRIAL_MODE` 约束 |
| 运行 | 采集 frame/detection/TRW；与 shadow 可选对比 |
| 通过 | 满足 `acceptance_checks` 全条；**下游调用为 0** |
| Abort | 触发任一 `abort_conditions` → 单次 tick 或整轮 trial 中止（实现可选），并写审计 |
| Rollback | 关闭入口 flag → offline/shadow-only；日志按 `trial_id` 保留 |

---

## 3. OCR trial playbook

| 阶段 | 动作 |
|------|------|
| 准入 | Global kill=false；`LUNA_ENABLE_OCR_GUARDED_TRIAL_V1=true`；`semantic_interpretation_enabled` 全程 false |
| 运行 | policy → provider 或 fallback/not_available；写 raw_text + TRW |
| 通过 | **governance_leakage=0**；**downstream_invocation_count=0**；schema 合法 |
| Abort | policy 缺失、语义输出、下游调用、`real_tts_invoked` 等 |
| Rollback | 关闭入口 flag；强制 not_available 或 shadow-only |

---

## 4. Qwen Voice trial playbook

| 阶段 | 动作 |
|------|------|
| 准入 | Global kill=false；`LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1=true`；默认 **不允许** playback/provider（除非子闸） |
| 运行 | governance → governed entry → dry-run / controlled 模式递进 |
| 通过 | governance/decision/diff_audit（按模式）；blocked→`selected_provider=none`；hard audit 一致 |
| Abort | 任一 voice abort 条件；env 与 global kill **语义冲突** |
| Rollback | 关闭 trial；`offline_only`；不确定则 `selected_provider=none` |

---

## 5. TRW 缺失处理

若 `trace_id`/`session_id` 缺失：**不得伪造**；记入 `missing_fields`；**不得**升级到 `controlled_provider`（见 `mainline_guarded_trial_trw_requirement_matrix.json`）。

---

## 6. 与 Phase-001 的关系

Phase-001 给出 R2 现状与接线候选点；本 Phase 将 **trial 行为** 写成 **可执行 playbook + JSON**，仍为 **定义层**，**不接真实 runtime**。
