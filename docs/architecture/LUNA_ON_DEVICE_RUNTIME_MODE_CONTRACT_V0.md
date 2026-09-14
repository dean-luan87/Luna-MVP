# Phase-Device-001 — On-Device Runtime Mode Contract v0（设备运行模式契约冻结）

**目的**：冻结 Device-001 设备运行模式与入口记录要求，确保“显式开启、可回放、可降级”，并禁止 default-on 与不受控 live 模式。  

---

## 1) 模式枚举（v0 写死）

必须至少支持 4 种模式（字符串枚举）：

1. `replay_device_mode`
2. `test_device_mode`
3. `controlled_live_input_mode`
4. `degraded_device_mode`

---

## 2) 模式语义（写死）

### 2.1 replay_device_mode
- 输入：已记录 video/log/replay（离线）
- 目标：链路复现与回放一致性验证
- 约束：不接真实环境；不允许 default-on；不允许真实执行放权

### 2.2 test_device_mode
- 输入：设备上受控测试输入（可用 fixture/mock perception signal）
- 目标：验证设备环境链路“可运行、可记录、可降级”
- 约束：candidate-only；不允许真实执行放权

### 2.3 controlled_live_input_mode
- 输入：受控真实摄像头/麦克风输入
- 目标：验证“真实输入→链路→输出候选→记录”在设备上可跑通
- 约束（硬）：
  - 必须显式开启（explicit entry event）
  - 不允许 default-on / 自动进入
  - 不允许进入真实执行放权（candidate-only）

### 2.4 degraded_device_mode
- 触发：设备性能不足、输入异常、模块失败、低置信/高风险无法决策等
- 目标：保守输出、可回退/停止、主链不崩溃
- 约束：必须记录 degraded 原因与触发点；输出必须更保守（可 silence / ask_for_help / wait_or_observe）

---

## 3) 禁止模式（Hard Denylist）

以下模式在 v0 明确禁止（出现即 no-go）：
- `uncontrolled_live_mode`
- `default_live_mode`
- `auto_execute_mode`
- `long_running_unbounded_mode`

---

## 4) 显式入口记录（写死）

当进入任一模式时，必须记录一条 `mode_entry_event`（结构化）：
- `run_id`
- `timestamp_ms`
- `mode`
- `explicit_entry`（bool；除 degraded 可为 false 外，其余必须为 true）
- `operator_intent`（字符串/枚举；v0 可为 `"manual_test"`）
- `default_on`（必须为 false）
- `no_execute_leakage`（必须为 true）
- `reason_codes`（至少 1 个）

---

## 5) 全模式共同硬约束（写死）

- 默认路径仍未开启（default-on=false）
- `allows_execute_now` 相关字段/语义不得出现放权
- 任何 execute/release/retry/reopen 语义不得出现（出现必须阻断并计入泄漏）

