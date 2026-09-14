# LUNA Mainline Controlled Trial Precheck & Post-Report v0

**Phase**：Phase-Mainline-GuardedTrial-001

---

## 1. Pre-trial checklist（每次 trial 前）

- `LUNA_DISABLE_ALL_GUARDED_TRIALS` 状态符合演练策略（紧急熔断除外）。  
- **仅一条** trial entry flag 为 true（YOLO / OCR / Qwen Voice 三选一）。  
- 其余无关 trial flags 均为 false。  
- RequestTrace、trace/replay/whitebox 输出路径可写。  
- Rollback 命令已文档化；abort 条件处于监控下。  
- **操作者确认** trial 窗口；若需前置 Stage，前置 Stage 已为 **GO**。  
- Global kill switch **一键全关** 可达。

机器可读：`mainline_controlled_trial_precheck_matrix.json`。

---

## 2. Post-trial report（每个 trial 必须产出）

必填字段见：`mainline_controlled_trial_post_report_schema.json`（含 `trial_id`、`capability`、时间窗、`sample_count`、`env_snapshot`、pass/fail、abort/rollback 事件、TRW 完整性、hard audit、side effect、**recommendation**：`GO_next_window` / `CONDITIONAL_GO_repeat` / `NO_GO_rollback_and_fix`）。

本 Phase **只定义 schema**，不生成真实报告实例。
