# Phase-RealSceneTrial-002 — Controlled Live Evidence Collection Runbook v0（执行手册冻结）

**目的**：定义 Trial-002 的具体操作步骤（启动/观察/中止/归档/复盘），只为产出真实 controlled live evidence，不扩场景。  

---

## 0) 预读（必须）

- Plan：`docs/architecture/LUNA_CONTROLLED_LIVE_EVIDENCE_COLLECTION_EXECUTION_PLAN_V0.md`
- Evidence capture contract：`docs/architecture/LUNA_CONTROLLED_LIVE_RUN_EVIDENCE_CAPTURE_CONTRACT_V0.md`
- Archive manifest schema：`docs/architecture/LUNA_REAL_SCENE_ARCHIVE_MANIFEST_SCHEMA_V0.md`
- Notes/Risk template：`docs/architecture/LUNA_REAL_SCENE_OPERATOR_NOTES_AND_RISK_EVENTS_TEMPLATE_V0.md`
- Abort policy（RealScenePrep）：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_ABORT_FALLBACK_ROLLBACK_POLICY_V0.md`

---

## 1) Run 前置（必须完成）

- 角色到位：operator / safety observer / record owner
- 环境确认：白天、低人流、平整路段、非隐私敏感区域
- timebox 配置完成（单次/连续/单日上限）
- abort triggers 确认（operator 与 observer 都可中止）
- archive_root_path 配置完成（确保可落盘）

---

## 2) 启动（必须记录）

必须在 `run_evidence.json` 中记录：
- `explicit_trial_intent=true` + `entry_token`
- `mode_entry_event_present=true`
- `controlled_live_input_started=true`

并确保三条断言为 true：
- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`

---

## 3) 运行中观察（持续）

持续监控：
- execute/release/retry/reopen 泄漏
- default-on 风险
- side effects expansion
- trace/replay/whitebox 写入状态
- device anomaly（过热/资源异常）
- privacy boundary（进入未授权/敏感区域）
- scope drift（偏离 Option A）

任一异常触发 abort。

---

## 4) Abort（必须可执行）

触发条件：遵循 RealScenePrep abort triggers（含 timebox exceeded、operator/observer abort 等）。  
abort 后必须：
- `mark_run_aborted=true`
- `stop_trial`
- `preserve logs`
- `enter degraded_or_closed_safe`
- `generate post_run_summary`
- `forbid immediate retry without review`

---

## 5) 结束与归档（必须完成）

run 结束后必须：
- `controlled_live_input_ended=true`
- 产出 required_files（见 contract）
- 生成 `archive_manifest.json`（sha256 校验通过）
- `risk_events.jsonl` 若无事件必须含 `none_observed` 声明记录
- 生成 `post_run_summary`

---

## 6) 验证（必须）

对 archive_root 执行：
- `tools/validate_controlled_live_run_evidence_capture_v0.py --archive_root <archive_root>`

验证输出必须为 `go`，否则不得进入下一阶段 review。

