# Phase-RealSceneTrial-001 — Controlled Real Scene Trial Execution Plan v0（执行计划冻结）

**阶段名**：Phase-RealSceneTrial-001  
**性质**：第一次受控真实场景试验执行（v0）；严格在 RealScenePrep-001 边界内；candidate-only。  

---

## 0) 明确声明（硬边界，写死）

- 不是开放真实用户测试
- 不是 full controlled trial
- 不是产品发布
- 不开启默认路径（no default-on）
- 不扩大真实 side effects 面（candidate-only）
- 不让模型拿执行权
- 不允许输出层触发 execute/retry/reopen/release
- 不允许长时间连续运行/无人监督
- 不允许 scope 临时扩散

---

## 1) 本次执行选择（v0）

- `selected_option`：**Option A（人行道短距离行走观察）**
- `scenario_id`：`sidewalk_short_walk_observe_v0`

允许条件（写死）：
- 白天
- 低人流
- 平整人行道
- 短距离（不做长距离连续导航）
- operator + safety observer + record owner 在场
- 输出仅 candidate/notice/warning/silence（不强制导航执行）

禁止条件（写死）：
- 复杂路口/高密人流/夜间/雨天
- 单人测试
- 强制过街/执行指令

---

## 2) 运行模式与输入源（写死）

- mode：`controlled_live_input_mode`（必须显式 entry）
- input_source：`controlled_live`
- `replay_capture_enabled=true`
- `whitebox_trace_enabled=true`

---

## 3) 人员配置（写死）

必须具备并记录：
- `operator_id`
- `safety_observer_id`
- `record_owner_id`

---

## 4) Timebox（写死）

必须配置并记录：
- `timebox_ms`（单次上限）
- `continuous_run_timebox_ms`
- `daily_trial_limit`

硬规则：
- 超时即 abort（见 abort policy）

---

## 5) 停止条件（写死）

任一触发即停止：
- 任一 abort trigger 命中（execute 泄漏/default-on/side effects expansion/trace broken/隐私边界等）
- timebox exceeded
- operator 或 safety observer 主动中止

---

## 6) 输出证据要求（写死）

每次 run 必须产出：
- run evidence（按 evidence schema）
- trace/replay/whitebox
- operator notes
- post-run summary

