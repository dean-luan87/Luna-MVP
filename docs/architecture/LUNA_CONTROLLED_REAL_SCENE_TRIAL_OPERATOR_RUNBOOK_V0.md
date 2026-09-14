# Phase-RealScenePrep-001 — Controlled Real Scene Trial Operator Runbook v0（操作员手册冻结）

**目的**：定义人工操作员如何启动、观察、中止、归档一次受控真实场景试验（前置阶段）。  
**注意**：本 runbook 只定义规则与流程，不授予任何自动执行权。  

---

## 1) 角色与职责（写死）

- **operator**：启动/停止试验；执行 checklist；记录关键事件
- **safety observer**：拥有独立 abort 权限；安全优先
- **record owner**：归档证据；生成 post-run summary；负责可复现性

---

## 2) 启动前（必须完成，写死）

- 选择场景：必须在 allowlist（scope 文档）内，且仅 1–2 个场景
- 配置 timebox：单次/单日/连续运行上限全部设置
- 完成 entry checklist：A/B/C/D 全部为 true
- 确认观测与证据 contract：replay/whitebox/trace 输出路径已配置
- 明确 abort triggers：操作员与安全观察员均确认

---

## 3) 启动动作（写死）

启动必须：
- 记录 `explicit_trial_intent`（entry_token）
- 记录 `mode_entry_event`
- 启用 `replay_capture_enabled=true`
- 明确 `candidate_only=true` 与三条断言将被记录（no execute / no default-on / no side effects expansion）

禁止：
- 任何默认开启（default-on）
- 任何长时间无上限运行

---

## 4) 运行中观察（写死）

运行中必须持续检查：
- 输出是否仍为候选（无 execute 语义）
- trace/replay/whitebox 是否持续写入
- 低置信是否触发降级或求助（不强行确定）
- 设备资源异常（温度/CPU/内存）是否触发 degraded

---

## 5) 中止（abort）规则（写死）

任一 abort trigger 出现：
- operator 或 safety observer 立即发起 abort
- 立刻停止试验输入（stop_trial）
- 标记 run aborted，并进入 degraded/closed-safe
- 保全所有 logs/trace/replay/whitebox
- 禁止未经 review 的重试

---

## 6) 结束与归档（写死）

结束后必须：
- 写入 `post_run_summary_ready=true`
- 归档 `archive_path`（可追踪）
- 记录：
  - run_id / scenario_id / timebox
  - enabled/disabled modules
  - abort events（若有）
  - fallback/degraded events（若有）
  - 三条断言结果（必须为 true）

