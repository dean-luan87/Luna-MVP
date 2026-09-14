# Narrative / Evidence Tension Review M0（语义张力 / 证据支撑审计增强）

**文件**：`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`

**依据上下文**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`、`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`、`logs/real_scenario_pack_m12.json`、`logs/benchmark_triage_board_m12.json`

---

## §1. 本轮定位

1. **不是**主线拍板功能开发，**不是** benchmark / triage 规则变更。  
2. 在 **M0.6 冻结基线**之上，对「主线通顺、白盒一致、日志已落地，但叙事与证据之间仍可能存在张力」的情况，建立**可审计、可复盘、可判定**的观察口径。  
3. 产出为只读 **`narrative_evidence_tension_review`** 对象，挂到 **frame 顶层**，并进入 **Console 聚合链 / Viewer**，与现有 Summary / Entry **解耦**（不反向改写）。

---

## §2. 为什么需要 tension review（与 M1.2 的关系）

M1.2 整包在 harness 上可 **全绿**，但仍存在用户关心的 **语义张力**：

- 叙事、summary、entry **读起来顺**；  
- 与 **structured event / timeline 密度**、**closure/outcome 口径**、**backfill 契约**、**局部 vs 全局推进**、**记忆参与倾向** 之间，可能出现 **「顺但不硬」** 的错位。

本轮把这些从 **主观感觉** 收束为 **工程对象**，便于后续决定是否升级评测、是否开第十三批扩包、是否引入 advisory / soft-fail，而**不**在本轮改 benchmark。

---

## §3. 五类 tension 定义（M0 启发式）

| 维度 | 含义（审计视角） |
|------|------------------|
| **narrative_trace_support_tension** | 叙事可读长度与 **structured_event 事件数 / 时间轴事件** 的覆盖关系是否失衡。 |
| **phase_closure_outcome_tension** | **mainline phase / closure 语义** 与 **terminal / outcome 叙述** 是否出现「过程对齐、结果过满或错位」迹象（参考 `closure_semantics_misalignment_summary` 等）。 |
| **summary_backfill_tension** | **post_processing_summary_entry** 在契约上是否仍要求 trace/event/whitebox backfill，与 **narrative_readable「完整感」** 是否冲突。 |
| **local_global_progress_tension** | **resume / task_chain 过程显影** 是否呈现 **局部连贯但全局主任务未前进**（如 resume fragility 摘要）。 |
| **memory_bias_tension** | **个性化语义偏差**：记忆参与、调度与 **memory_bias_accumulation** 等信号是否值得单独回看（**不用「污染」表述**）。 |

每维取值：`none` / `low` / `medium` / `high` / `unknown`（**非**评分模型，仅为档位）。

---

## §4. 最小对象与工程接入

**模块**：`decision_monitor/narrative_evidence_tension_review.py`  
**构建**：`build_narrative_evidence_tension_review(frame_dict)`，**只读** frame，**不修改**入参 dict。

**对象字段（摘要）**：

- 五维：`narrative_trace_support_tension`、`phase_closure_outcome_tension`、`summary_backfill_tension`、`local_global_progress_tension`、`memory_bias_tension`  
- `tension_review_brief`：一行紧凑档位  
- `tension_review_readable`：多行中文可读说明  
- `tension_reason_summaries`：各维简短理由（键与维度对应）  
- `suggested_backfill_direction_summary`：建议回溯方向（聚合句，**非**执行指令）  
- `narrative_evidence_tension_review_applied`：当且仅当 **`run_summary_reference.summary_reference_applied`** 为真时置 `true`（否则整对象为空审计默认）

**接入**：

- **`decision_monitor/builder.py`**：在 `run_summary_reference`、`mainline_narrative_alignment`、`post_processing_summary_entry` 生成之后，**追加** tension review（独立 try，失败则 `null`）。  
- **`decision_monitor/schema.py`**：`DecisionMonitorFrame.narrative_evidence_tension_review`  
- **`tools/reasoning_console_aggregator.py`**：`narrative_evidence_tension_review`、`tension_review_readable`、`tension_review_brief`  
- **`tools/decision_monitor_viewer.py` / `tools/reasoning_console_server.py`**：展示块 + 调试表条目  

**读取源（只读）**：`run_summary_reference`、`post_processing_summary_entry`、`mainline_narrative_alignment`、`mainline_state_snapshot`、`task_chain_state_snapshot`、`memory_invocation_explanation`、`scheduled_source_state`、`reasoning_timeline_view`（与 `structured_event_layer_snapshot` 等已有切片一致）。

---

## §5. 当前观测能力边界

- **不是裁决器**：不修改 recheck、不改 post-processing 契约、不改变 benchmark/triage。  
- **不是硬失败来源**：默认 **不** 进入 `scenario_benchmark_harness` 的 pass/fail。  
- **启发式**：同一帧在不同数据下可出现档位变化；以 **复盘与文档化** 为主。

---

## §6. 后续可用方向

- 是否将部分维度 **升级为 soft-fail / advisory**（需单独变更 benchmark 策略，**非本轮**）。  
- 是否在 **第十三批真实场景** 中增加「专门压 tension 档位」的用例。  
- 是否与 **图书馆 / 记忆写入** 等能力解耦推进（仍属架构文档中的 reserve 序列）。

---

补记：已进入 **Real Scenario Pack M1.3** 真实场景实压观察（见 `docs/REAL_SCENARIO_PACK_M1_3_DELIVERY.md`）；`tension_audit` 仅作 pack 摘要字段，**不**改变 harness 判定。

补记：已完成 **Tension Audit Calibration Review M0**（见 `docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`）——对 M1.3 全量 tension 分布做去噪与分级建议；**不**修改审计对象字段，**不**升级 benchmark。

---

## §7. 本轮是否通过

**通过。**

理由：已实现审计对象、builder 落地、聚合与 Viewer/Console 可读、单测与 smoke 通过；未改 benchmark/triage 规则，未动主链拍板与契约回写。

---

## 主线—白盒—日志一致性检查

- **A 主线**：tension review **不参与**拍板，仅在 summary 链之后只读挂载。  
- **B 白盒**：依据 **同帧** `run_summary` / `mainline_narrative` / `post_processing` / 时间轴与快照字段做启发式对齐说明。  
- **C 日志**：review 随 **frame** 序列化；smoke 写入 `logs/smoke_narrative_evidence_tension_review.jsonl`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（审计层为增量观察，不改变既有 M0.6 冻结结论）。
