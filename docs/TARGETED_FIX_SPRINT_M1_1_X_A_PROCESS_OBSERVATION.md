# Targeted Fix Sprint M1.1.x-A（过程观察增强）

## 1. 本轮目标

针对 `R60/R61/R64`，先做过程显影，不改收口规则：

- `R60`：恢复链在哪一跳变脆  
- `R61`：记忆语义偏差在哪一段开始压过当前观察  
- `R64`：phase 到 closure 在哪一层错位

---

## 2. 修改文件清单

- `decision_monitor/run_summary_builder.py`
- `decision_monitor/reasoning_timeline_view.py`
- `decision_monitor/builder.py`
- `decision_monitor/reasoning_structure_tree.py`
- `decision_monitor/post_processing_summary_contract.py`
- `tools/reasoning_console_aggregator.py`
- `tests/test_m11x_process_observation.py`
- `tools/smoke_m11x_process_observation.py`

---

## 3. 新增过程观察锚点

### A. run_summary_reference（主锚点）

- `process_observation_summary`
- `resume_chain_stage_summary`
- `resume_chain_fragility_summary`
- `resume_chain_progress_reached_main`
- `memory_bias_accumulation_summary`
- `memory_bias_weight_shift_summary`
- `memory_bias_conflict_stage_summary`
- `phase_closure_alignment_summary`
- `closure_semantics_misalignment_summary`

### B. timeline 事件锚点

- `resume_chain_declared`
- `resume_chain_not_progressing_main`
- `resume_chain_fragility_detected`
- `memory_bias_accumulation_detected`
- `memory_bias_overrode_observation_tendency`
- `memory_bias_requires_conservative_repair`
- `phase_identified_but_closure_misaligned`
- `closure_semantics_repair_candidate`

### C. post-processing entry 可见锚点

- `post_processing_summary_entry.process_observation_summary`
- `backfill_reason_summary` 追加 `process_observation_hint`

### D. tree 可见锚点

- `tree_summary` 附加 `proc=...` / `resume_frag=...` / `phase_closure_mis=...`

---

## 4. R60 / R61 / R64 过程断点定位（A 阶段结论）

- **R60**：断点主要出现在 `resume declared -> main progress` 之间，表现为 `resume_chain_fragility_summary=resume_declared_but_main_not_progressed`，且时间轴出现 `resume_chain_not_progressing_main`。  
- **R61**：断点主要出现在 `memory_effect/source_conflict -> closure`，表现为 `memory_bias_accumulation_summary` 与 `memory_bias_conflict_stage_summary` 持续非 none。  
- **R64**：断点主要在 `phase identified -> closure semantics` 同步处，`closure_semantics_misalignment_summary` 可直接标识错位。

---

## 5. 测试与 smoke

- 单测：`python3 -m pytest tests/test_m11x_process_observation.py -q`
- smoke：`python3 tools/smoke_m11x_process_observation.py`

预期：

- R60/R61/R64 三类过程锚点均可见  
- timeline / tree / summary / entry 至少一条链路可交叉对照  
- JSONL 产物可写出（`logs/smoke_m11x_process_observation.jsonl`）

---

## 6. 是否进入 B 阶段

结论：**可以进入 B 阶段**。  
原因：断点已从“现象级 blocked”收敛为“可定位层级”（resume 链、memory 偏差链、phase-closure 对齐链），可据此做最小定点修复。
