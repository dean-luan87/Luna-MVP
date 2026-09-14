# Phase-RealSceneTrial-001 — Controlled Real Scene Trial Run Record Template v0（单次试验记录模板）

**用途**：给操作员/记录责任人用于单次 run 的手工记录（也可由工具自动生成占位）。  

---

## 基本信息

- run_id：
- date：
- selected_option：
- scenario_id：
- mode：
- input_source：
- location (high-level, non-PII)：

## 人员

- operator_id：
- safety_observer_id：
- record_owner_id：

## 入口与配置

- explicit_trial_intent=true：
- entry_token：
- timebox_ms：
- continuous_run_timebox_ms：
- daily_trial_limit：
- replay_capture_enabled=true：
- whitebox_trace_enabled=true：

## Checklist（必须全为 true 才能开始）

- default_path_disabled=true：
- full_controlled_trial=false：
- side_effects_expansion=false：
- model_execution_authority=false：
- candidate_only=true：
- fallback/degraded available=true：
- trace/replay/whitebox available=true：
- privacy_area_checked=true：
- environment_allowed=true：

## 运行中事件（摘要）

- notable_observations：
- degraded_triggered：
- fallback_triggered：
- abort_triggered：
- abort_reason：

## 断言（必须为 true）

- no_execute_leakage_assertion=true：
- no_default_on_assertion=true：
- no_side_effect_expansion_assertion=true：

## 归档

- trace_ready：
- replay_ready：
- whitebox_ready：
- archive_path：
- post_run_summary_ready：

## 复盘结论

- scope_drift (0/1)：
- timebox_violation (0/1)：
- privacy_boundary_violation (0/1)：
- immediate_retry_without_review (0/1)：
- next_action：

