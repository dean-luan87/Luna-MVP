# Phase-RealSceneReview-001 — Controlled Real Scene Trial Run Evidence Quality Matrix v0（证据质量矩阵冻结）

**目的**：把 run evidence 的关键质量项矩阵化（pass/partial/fail），并给出 blocker_level 与 next_action，避免“fixture pass=真实充分验证”。  

---

## 本次评审对象

- evidence 类型：**fixture evidence**
- selected_option：Option A（人行道短距离观察）

---

## 证据质量矩阵（v0）

| item | status | evidence_source | blocker_level | next_action |
|---|---|---|---|---|
| checklist_completed | pass | fixture run evidence + validator | informational | 真实 run 仍需逐项记录，不允许缺项开跑 |
| explicit_entry | partial | fixture 通过字段表达；未覆盖真实“显式入口事件落盘”全链 | soft_followup | 在 controlled live run evidence 中强制包含 entry_token 与 mode_entry_event 归档引用 |
| selected_option_allowed | pass | execution plan + scope allowlist | informational | 若扩场景必须先更新 scope/boundary 并再过 go/no-go |
| operator_present | pass | fixture evidence（placeholder） | informational | 真实 run 记录 operator_id（可占位但需稳定标识） |
| safety_observer_present | pass | fixture evidence（placeholder） | informational | 真实 run 记录 observer_id，并确保独立 abort 权限 |
| timebox_configured | pass | fixture evidence（timebox_ms） | informational | 真实 run 需记录单次/连续/单日上限 |
| timebox_respected | pass | fixture evidence（duration <= timebox） | informational | 真实 run 超时必须 abort 并归档 |
| trace_ready | pass | fixture evidence 标记 + validator | informational | 真实 run 下检查 trace 持续写入与可排序 |
| replay_ready | pass | fixture evidence 标记 + validator | informational | 真实 run 下必须可回放，归档路径必须可追踪 |
| whitebox_ready | pass | fixture evidence 标记 + validator | informational | 真实 run 下必须包含 errors/fallback_events/timings |
| model_candidate_trace_ready | pass | fixture evidence 标记 | informational | 真实 run 可允许为 partial，但不得缺失整体 trace |
| output_candidate_trace_ready | pass | fixture evidence 标记 | informational | 真实 run 必须可追踪输出候选与抑制 |
| post_run_summary_ready | pass | fixture evidence 标记 | informational | 真实 run 需产出最小 post-run summary（含断言、是否 abort、是否越界） |
| no_execute_leakage | pass | assertion=true + validator | hard_blocker | 任一泄漏即停止推进并进入 pause 或 fix |
| no_default_on | pass | assertion=true + validator | hard_blocker | 任一 default-on 风险即 no-go |
| no_side_effect_expansion | pass | assertion=true + validator | hard_blocker | 任一扩张即 no-go |
| scope_drift_count | pass | fixture evidence（0） | hard_blocker | 真实 run scope drift>0 即 no-go，禁止扩场景 |
| privacy_boundary_violation_count | pass | fixture evidence（0） | hard_blocker | 隐私边界违规即 no-go |
| abort_trigger_ready | partial | 文档已冻结；未用真实 run 触发验证链 | soft_followup | 真实 run 必须验证 abort 可执行与归档完整 |
| fallback_ready | partial | 文档已冻结；fixture 未覆盖失败路径 | soft_followup | 真实 run 至少验证 degraded/fallback 触发与记录 |
| degraded_ready | partial | 同上 | soft_followup | 同上 |

---

## 矩阵级结论

- **hard_blocker**：无（fixture evidence 下未触发）  
- **soft_followup**：存在（主要是“真实 controlled live 证据质量与中止/降级链路实证”）  
- **建议分流**：进入 Fix Sprint（先补齐真实 run evidence 质量与可复现性，再考虑扩场景）。  

