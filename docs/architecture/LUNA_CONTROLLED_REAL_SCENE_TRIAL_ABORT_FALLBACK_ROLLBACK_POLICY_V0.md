# Phase-RealScenePrep-001 — Controlled Real Scene Trial Abort / Fallback / Rollback Policy v0（中止与回退策略冻结）

**目的**：写死 abort/fallback/rollback/degraded 的触发条件与后置动作，确保“可中止、可降级、可归档、禁止无复盘重试”。  

---

## 1) Abort triggers（任一触发即 abort，写死）

- default path risk detected
- execute/release/retry/reopen leakage detected
- trace/replay broken
- fallback unavailable
- low confidence forced action detected
- unexpected side effects expansion
- timebox exceeded
- operator abort
- safety observer abort
- uncontrolled environment detected
- device overheating or severe resource anomaly
- privacy-sensitive area detected without policy

---

## 2) Abort 后必须执行的动作（写死）

abort 后必须：
- `stop_trial`（立即停止受控真实输入试验）
- `preserve_logs=true`（保留 logs/trace/replay/whitebox）
- `mark_run_aborted=true`
- `enter_degraded_or_closed_safe=true`
- `forbid_retry_without_review=true`
- `generate_post_run_summary=true`

---

## 3) Fallback 策略（写死）

允许的 fallback（candidate-only）：
- 从 `controlled_live_input_mode` 降级到 `degraded_device_mode`
- 退回 replay/fixture 对照复现（不继续 live）
- 禁用 model shadow（model_disabled）后继续 baseline 链路（仍 candidate-only）

禁止的 fallback：
- 任何形式的“绕过护栏继续执行”
- 任何形式的“打开 default-on 继续运行”

---

## 4) Rollback 语义（写死）

本阶段的 rollback 指：
- 回滚到“受控试验前”的安全状态与配置（closed-safe / candidate-only）
- 回滚到 baseline（禁用 live input / 禁用可疑模块）

明确禁止：
- 使用 rollback 名义触发任何真实 side effects 扩展

---

## 5) Degraded 触发与要求（写死）

degraded 触发条件（任一满足）：
- 输入不稳定/缺失（camera drop / decode error）
- 资源异常（CPU/内存/温度）
- 低置信且无法安全给出候选
- 观测链路不完整（trace/replay 断裂）

degraded 状态要求：
- 输出更保守（允许 silence / ask_for_help / wait_or_observe）
- 必须记录 degraded 原因与时间戳
- 不允许自动恢复为 live（必须显式重新 entry 且再次过 checklist）

