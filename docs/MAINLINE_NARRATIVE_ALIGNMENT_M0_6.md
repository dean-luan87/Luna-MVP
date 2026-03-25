# Mainline Narrative Alignment — M0.6

**文件**：`docs/MAINLINE_NARRATIVE_ALIGNMENT_M0_6.md`  
**性质**：工程收口（叙事口径对齐，不新增能力）  
**上位文档**：`docs/DECISION_MAINLINE_ARCHITECTURE.md`、`docs/WHITEBOX_OBSERVATION_ARCHITECTURE.md`、`docs/TRACE_LOGGING_AND_SUMMARY_PIPELINE.md`

---

## 1) 目标

把已落地主线对象在 **主线 → 白盒 → 日志 → Summary → 后处理入口** 的讲述顺序统一为同一骨架，减少“层层可见但说法打架”。

对象范围：

- `scheduled_source_state`
- `task_chain_state_snapshot`
- `memory_invocation_explanation`
- `mainline_state_snapshot`
- `run_summary_reference`
- `post_processing_summary_entry`

---

## 2) 统一叙事骨架（M0.6）

固定顺序：

1. `context`：当前上下文/场景位置  
2. `source`：主导源/冲突/覆盖  
3. `task`：任务位置与进度提示  
4. `memory`：记忆参与与效果  
5. `mainline`：主链状态/阶段  
6. `closure`：当前收口语义  
7. `risk`：风险与回溯提示

---

## 3) 工程落地

- 新增 `decision_monitor/mainline_narrative_alignment.py`：集中生成 `mainline_narrative_alignment`（只读表达层）。
- `builder`：在 `run_summary_reference` 后构建 `mainline_narrative_alignment`，再构建 `post_processing_summary_entry`。
- `run_summary_reference`：`summary_brief` 按统一骨架输出；新增 `mainline_narrative_brief`。
- `post_processing_summary_entry`：新增 `narrative_readable`，与 summary 口径一致但不越权。
- 聚合器：新增 `mainline_narrative_readable` 与原对象透传。
- Console/Viewer：新增 M0.6 卡片，按同骨架展示。

---

## 4) 术语统一（M0.6）

- `recovery`（主链状态） ≠ `recovering`（任务位置/模式）
- `pause`（主链状态） ≠ `paused`（任务模式）
- `local_success` ≠ `main_progress`
- `summary`（轻提炼） ≠ `summary_reference`（trace 派生对象） ≠ `post_processing_entry`（后处理入口契约）
- `warning`（提示） < `risk`（需关注/可能触发回溯）
- `conflict`（冲突）与 `override`（优先级覆盖）分开表达
- `supports_mainline` 与 `neutral_reference` 分开表达
- `task_position`（位置语义）与 `task_progress`（推进语义）分开表达
- `mainline_state`（状态）与 `mainline_phase`（阶段）分开表达

---

## 5) 边界

- 不改 Raw Trace/Structured Event 原义。
- 不让 Summary 冒充白盒，不让后处理入口冒充证据本体。
- 叙事对齐仅是表达层，不引入新证据层。

---

## 6) 主线—白盒—日志—Summary—后处理 串联检查

- **A 主线**：对象仍来自同一帧，不引入旁路伪对象。  
- **B 白盒**：按同骨架读到 source/task/memory/mainline。  
- **C 日志**：`run_summary_reference` 与 `post_processing_summary_entry` 落盘并可追溯。  
- **D 结论**：现有主线对象已在叙事层形成更统一的同链表达（M0.6）。
