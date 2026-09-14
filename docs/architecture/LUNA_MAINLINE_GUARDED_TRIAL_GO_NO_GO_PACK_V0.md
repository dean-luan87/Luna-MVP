# LUNA Guarded Trial GO / No-Go Pack v0

**Phase**：Phase-Mainline-RuntimeReadiness-002

---

## GO（本 Phase 定义交付）

下列条件 **同时** 满足 → **GO**：

- 三条 trial（YOLO / OCR / Qwen Voice）scope **齐全且互相独立**。  
- **Global kill switch** `LUNA_DISABLE_ALL_GUARDED_TRIALS` **已定义**（默认 false；true 时全员禁止）。  
- env flag 矩阵、acceptance、abort、rollback、TRW **均已写入 JSON**。  
- 全部 trial 的 `default_enabled` **均为 false**。  
- `max_allowed_readiness_level_after_pass` **仅为** `R3_guarded_wiring_ready`。  
- **未接** runtime；**未**真实调用 Qwen/TTS；**未**播报；**未**改主链与默认 provider。

**Summary verdict**：`phase_definition_documentation` = **GO**。

---

## CONDITIONAL_GO

- 个别 flag **命名**在首个接线 PR 中可能微调，但 **边界与优先级** 已冻结 → **CONDITIONAL_GO**（对接线实现）。  
- `LUNA_YOLO_TRIAL_MAX_FRAMES` 等 **数值默认** 依赖未来 PR 冻结具体常数。

**Summary verdict**：`guarded_wiring_implementation_next_phase` = **CONDITIONAL_GO**。

---

## NO_GO

任一成立 → **NO_GO**：

- **缺少** global kill switch 定义。  
- **任一** trial **默认开启**（`default_enabled=true`）。  
- **未**定义 abort/rollback 或 TRW 注入要求。  
- 在本 Phase **建议直接接真实 provider** 或 **修改默认 provider**。  
- 在本 Phase **接入真实 runtime** 或执行真实 TTS/播报。

**Summary verdict**：`real_runtime_activation` = **NO_GO**。

---

## Hard blockers（定义层之外）

- **实现层**：主链尚未按本矩阵接线；属后续 Phase，**不是** 002 定义缺失。

## Soft follow-ups

- 将本 JSON 与 CI verifier 纳入合并门禁（接线 PR）。  
- 为每条 trial 编写 **专用 evaluate**（仍可在 dry-run 下）。

---

## Recommended next phase

**Phase-Mainline-RuntimeReadiness-003（建议）**：在 **默认全部关闭** 前提下，将 trial 闸 **映射到代码路径**（独立 PR、可回滚）；仍 **禁止** 未经批准的 production 默认。

---

**一句话**：002 把「怎么安全升到 R3」写成 **手册 + 机器可读矩阵**；**真正接线** 属于下一阶段，且必须仍服从 global kill 与 NO_GO 红线。
