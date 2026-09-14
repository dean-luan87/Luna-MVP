# Phase-RealSceneReview-002 — Controlled Live Evidence Pipeline Quality Matrix v0（证据流水线质量矩阵冻结）

**目的**：对 Fix-001 补齐的 evidence pipeline（contract/manifest/notes/risk/validator）做矩阵化复审，判断是否“足以支持下一次 controlled live evidence 采集执行”。  

---

## 证据来源

- Fix-001 文档链 + validation tool A–L 结果（工具 recommendation=go）

---

## Pipeline Quality Matrix（v0）

| item | status | evidence_source | blocker_level | next_action |
|---|---|---|---|---|
| controlled_live_evidence_contract_complete | pass | `LUNA_CONTROLLED_LIVE_RUN_EVIDENCE_CAPTURE_CONTRACT_V0.md` | informational | 进入下一次 execution 时严格按 contract 落盘 |
| explicit_entry_fields_required | pass | capture contract + validator（B） | hard_blocker | 缺 entry_token/explicit_trial_intent 即禁止执行 |
| mode_entry_event_required | pass | capture contract + validator（B） | hard_blocker | 缺 mode_entry_event 即 no-go |
| trace_file_required | pass | required_files + validator（C） | hard_blocker | 缺 trace.jsonl 即 no-go |
| replay_file_required | pass | required_files + validator（D） | hard_blocker | 缺 replay.jsonl 即 no-go |
| whitebox_file_required | pass | required_files + validator（E） | hard_blocker | 缺 whitebox.jsonl 即 no-go |
| model_candidate_trace_required | pass | required_files | informational | 允许后续质量提升，但不得缺失文件 |
| output_candidate_trace_required | pass | required_files | hard_blocker | 缺输出候选 trace 即 no-go |
| operator_notes_required | pass | template + validator（F） | hard_blocker | 缺 notes 文件即 no-go |
| risk_events_required_or_none_declared | pass | template + validator（G/I） | hard_blocker | risk_events 必须存在；无风险必须 none_observed |
| archive_manifest_required | pass | manifest schema + validator | hard_blocker | 缺 manifest 即 no-go |
| sha256_hash_required | pass | manifest schema + validator | hard_blocker | required_files hash 缺失即 no-go |
| hash_mismatch_detection | pass | validator（H） | hard_blocker | mismatch 必须 hard fail |
| safety_assertion_false_detection | pass | validator（L） | hard_blocker | 任一断言 false 必须 hard fail |
| synthetic_abort_evidence_parse | pass | validator（J） | informational | execution 可不触发，但字段必须可记录 |
| synthetic_fallback_evidence_parse | pass | validator（K） | informational | 同上 |
| synthetic_degraded_evidence_parse | pass | validator（K） | informational | 同上 |
| post_run_summary_required | pass | required_files + validator | hard_blocker | 缺 post_run_summary 即 no-go |
| validation_tool_reproducible | pass | A–L expectation_mismatches=[] | informational | 保持工具可复现输出 |

---

## 矩阵级结论

- **hard_blocker**：无（pipeline 本体已覆盖并能检测 hard fail）  
- **soft_followup**：真实 controlled live run evidence 仍需下一阶段实际采集并归档（本阶段不执行）。  
- **是否允许进入下一次 controlled live run evidence collection execution**：是（GO）。  

