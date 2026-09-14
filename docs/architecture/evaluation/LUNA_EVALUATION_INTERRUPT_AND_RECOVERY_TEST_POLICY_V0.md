# Luna Evaluation & Test Board — Interrupt & Recovery Test Policy v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**Level**：5（与 Level 4 batch/recovery 互补：Level 4 偏 **批处理与续跑**；Level 5 偏 **运行时取消语义**）  
**定位**：**Luna 全局** 中断、取消、暂停与恢复策略；**非 OCR 专属**。

---

## 1. 必须覆盖的中断类别（最低集合）

| 标识 | 说明 | 适用模块示例 |
|------|------|----------------|
| `user_cancel` | 用户显式取消 | OCR 长任务、Vision 长视频 |
| `system_timeout` | 系统/平台超时 | 全模块 |
| `high_priority_interrupt` | 高优任务抢占 | TaskChain、Voice 队列 |
| `power_degraded_interrupt` | 低电量/温控降级 | 端侧 Vision、OCR |
| `scene_changed_interrupt` | 场景变化导致前任务失效 | Vision、STCM |
| `safety_override` | 安全策略强制中止 | Risk、STCM |

---

## 2. 必须产出的审计产物

见 `LUNA_EVALUATION_TEST_ARTIFACT_STANDARD_V0.md` **§3**：`interrupt_trace.jsonl`、`recovery_state.json`、`cancellation_report.json`。

---

## 3. GO / NO_GO 条件

- **GO**：任务可被 **正确** 取消或恢复；**无** 误写下游；**无** 残留半状态导致后续运行污染；trace 与 `cancellation_report.json` 一致。  
- **NO_GO**：取消后仍写入 consumer；或无法恢复导致数据面 **静默分叉**；或未定义 `user_cancel` / `system_timeout` 行为。

---

## 4. 与 Level 4 的关系

- **Level 4**：进程级 crash、拆批、`resume_state`、merge metrics。  
- **Level 5**：协作式/系统级 **取消与语义**；二者均 **必填** 方可认为「中断恢复」治理闭环。

---

**非 OCR 专属声明**：Voice 播报队列、Vision 长视频、STCM deadline timeout 均须按本策略设计用例。
