# Phase-DeviceEnv-001 — Option A Controlled Live Run Manual Operation Guide v0（人工操作指南冻结）

**目的**：给操作员一份实际执行指南：如何启动、如何录制、如何停止、如何归档、如何验证。  
**注意**：本指南不扩场景、不放权、不 default-on；仅 Option A；真实 run 必须人工监督。  

---

## 1) 准备（开跑前）

先逐项通过：
- `docs/architecture/LUNA_OPTION_A_CONTROLLED_LIVE_DEVICE_SETUP_CHECKLIST_V0.md`

必须确定：
- `run_id`（建议现场生成）
- `archive_root_path`：`runs/controlled_live/option_a/<run_id>/`
- `operator_id / safety_observer_id / record_owner_id`
- timebox（单次/连续/单日）
- abort 方法（观察员与操作员均可立即中止）

---

## 2) 启动（必须显式入口）

启动时必须做到：
- 进入 `controlled_live_input_mode`
- 记录 `entry_token`
- 落盘 `mode_entry_event_present=true`
- 标记 `controlled_live_input_started=true`
- 开始写入 trace/replay/whitebox

禁止：
- 无 entry_token 开跑
- 未落盘 mode entry 就开始录制

---

## 3) 运行中（持续监控）

持续检查（任一触发立即 abort）：
- execute/release/retry/reopen 泄漏风险
- default-on 风险
- side effects expansion 风险
- trace/replay/whitebox 断裂
- 隐私敏感区域进入或未授权拍摄
- scope drift（偏离 Option A）
- timebox 超时
- 设备异常（过热/资源异常）

---

## 4) 中止（abort）

任一 abort trigger：
- safety_observer 可直接发起 abort（最高优先级）
- 立即停止采集
- 保全所有已写文件
- 进入 degraded/closed-safe
- 生成 post_run_summary（必须写明 abort_reason）
- 禁止无复盘立即重试

---

## 5) 停止与归档（run 正常结束）

停止时必须：
- 标记 `controlled_live_input_ended=true`
- 生成 `run_evidence.json`（按 Fix-001 contract）
- 生成 `risk_events.jsonl`（无风险也必须写入 `none_observed`）
- 生成 `operator_notes.md`
- 生成 `post_run_summary.md`
- 生成 `archive_manifest.json`（sha256；`archive_ready=true`）

---

## 6) 验证（必须）

把 `archive_root_path` 拷贝/同步到本仓库可访问路径后运行：

```bash
python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root "<archive_root_path>"
```

输出 `go`：
- 允许进入 Review-003  
否则：
- 视为 evidence 不合格；回到 Fix Sprint 或暂停（按 review 策略）。

