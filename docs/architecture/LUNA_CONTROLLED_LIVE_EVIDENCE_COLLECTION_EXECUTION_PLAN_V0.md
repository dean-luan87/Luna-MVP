# Phase-RealSceneTrial-002 — Controlled Live Evidence Collection Execution Plan v0（执行计划冻结）

**阶段名**：Phase-RealSceneTrial-002  
**性质**：controlled live evidence collection（v0）；只为产出第一份非 fixture 的 controlled live run evidence；不扩场景。  

---

## 0) 明确声明（硬边界，写死）

- 不是扩场景；只允许 Option A 人行道短距离观察
- 不进入 full controlled trial
- 不开放真实用户测试
- 不开启默认路径（no default-on）
- 不扩大真实 side effects 面（candidate-only）
- 不让模型拿执行权
- 不允许长时间连续运行/无人监督

---

## 1) 本次唯一允许场景（写死）

- `selected_option`：Option A（人行道短距离行走观察）
- `scenario_id`：`sidewalk_short_walk_observe_v0`
- 环境：白天、低人流、平整人行道、短距离
- 输出：candidate/notice/warning/silence（不强制导航指令；不真实过街）

---

## 2) 人员与角色（必须到位）

必须具备并记录：
- `operator_id`
- `safety_observer_id`
- `record_owner_id`

---

## 3) 模式与证据归档（写死）

- mode：`controlled_live_input_mode`（必须显式 entry）
- evidence contract：`docs/architecture/LUNA_CONTROLLED_LIVE_RUN_EVIDENCE_CAPTURE_CONTRACT_V0.md`
- manifest schema：`docs/architecture/LUNA_REAL_SCENE_ARCHIVE_MANIFEST_SCHEMA_V0.md`
- notes/risk template：`docs/architecture/LUNA_REAL_SCENE_OPERATOR_NOTES_AND_RISK_EVENTS_TEMPLATE_V0.md`

必须产生 archive_root（目录）并包含 required_files（contract 写死）。

---

## 4) Timebox（写死）

必须配置并记录：
- `timebox_ms`（单次上限）
- `continuous_run_timebox_ms`
- `daily_trial_limit`

超时即 abort（按 RealScenePrep abort policy）。

---

## 5) 停止条件（写死）

任一触发即停止：
- 任一 abort trigger 命中（execute 泄漏/default-on/side effects expansion/trace broken/隐私边界等）
- timebox exceeded
- operator 或 safety observer 主动中止

---

## 6) 产出物（必须）

- `run_evidence.json`（controlled_live）
- `archive_manifest.json`（sha256 校验通过）
- trace/replay/whitebox/model_candidate/output_candidate traces
- operator_notes
- risk_events（或 none_observed）
- post_run_summary

