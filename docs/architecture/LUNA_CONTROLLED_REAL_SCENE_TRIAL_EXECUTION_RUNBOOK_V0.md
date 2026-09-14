# Phase-RealSceneTrial-001 — Controlled Real Scene Trial Execution Runbook v0（执行手册冻结）

**目的**：把 RealScenePrep 的 operator runbook 落到本次执行（Option A）的具体步骤，保证启动/观察/中止/归档/复盘可执行。  
**注意**：本手册不授予任何自动执行权；不允许 default-on；candidate-only。  

---

## 1) Run 前置（必须完成）

- 读取并确认 scope：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_SCOPE_AND_BOUNDARY_V0.md`
- 完成 entry checklist：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_ENTRY_CHECKLIST_V0.md`
- 确认 abort policy：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_ABORT_FALLBACK_ROLLBACK_POLICY_V0.md`
- 确认 evidence contract：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_OBSERVABILITY_AND_EVIDENCE_CONTRACT_V0.md`
- 确认本次执行计划：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_EXECUTION_PLAN_V0.md`

---

## 2) 启动步骤（必须记录）

1. 指派并记录角色：operator / safety observer / record owner
2. 生成并记录 `run_id`
3. 记录 `explicit_trial_intent=true` 与 `entry_token`
4. 设置 timebox（单次/连续/单日上限）并记录
5. 启动 `controlled_live_input_mode`（显式 entry 事件必须落盘）
6. 确认 `replay_capture_enabled=true`、`whitebox_trace_enabled=true`
7. 写入三条断言占位并在 run 结束时验证为 true：
   - `no_execute_leakage_assertion`
   - `no_default_on_assertion`
   - `no_side_effect_expansion_assertion`

任一项缺失：不得开始 run。

---

## 3) 运行中观察（持续）

operator 与 safety observer 持续检查：
- 禁止语义：execute/release/retry/reopen（任一出现即 abort）
- default-on 风险（任一出现即 abort）
- side effects expansion（任一出现即 abort）
- trace/replay/whitebox 写入是否持续（断裂即 abort）
- 低置信是否触发降级/求助（不强行确定）
- timebox 是否接近上限（超时即 abort）
- 隐私敏感区域进入（无策略即 abort）
- 设备异常（过热/资源异常）→ degraded 或 abort

---

## 4) 中止（abort）与后置动作

任一 abort trigger 命中：
- safety observer 可直接发起 abort（优先级最高）
- 立即 `stop_trial`
- 标记 `mark_run_aborted=true`
- 保全 logs/trace/replay/whitebox
- 进入 degraded/closed-safe
- 禁止无复盘立即重试

---

## 5) 结束与归档（必须完成）

run 结束后 record owner 必须：
- 生成并归档 run evidence（按 evidence schema）
- 生成 `post_run_summary`（最小：发生了什么、是否 abort、是否越界、三条断言结果）
- 写入 `archive_path` 与 manifest/hash（v0 可占位但必须可追踪）

---

## 6) 复盘（必须）

复盘最小输出：
- scope 是否越界（0/1）
- abort 是否正确执行（若发生）
- trace/replay/whitebox 是否完整
- 是否存在任何泄漏/default-on/side effects 扩大（必须为 0）
- 是否需要进入 fix sprint（若出现软问题）

