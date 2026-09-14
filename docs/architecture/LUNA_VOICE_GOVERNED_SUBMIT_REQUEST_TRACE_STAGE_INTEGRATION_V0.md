# Phase-Voice-OutputGovernance-008

# Governed Submit Shadow RequestTrace Stage Integration v0

**阶段定位**：在 Phase-007（submit 前 shadow readiness）与 Phase-005（Voice RequestTrace shadow chains）之间做**并行观测**集成：把 `governed_submit_shadow_gate` 作为追加 stage 挂到每条匹配的 request chain 上；**不接真实 submit**、**不真实播报**、**不修改 Phase-005 源文件**。

---

## 输入（只读）

- Phase-007 output：`voice_governed_submit_shadow_decisions.json`
- Phase-005 output：`voice_output_request_chains.json`

---

## 输出（output_root）

工具：`tools/evaluate_voice_governed_submit_request_trace_shadow_v0.py`

- `voice_governed_submit_request_trace_summary.json`
- `voice_governed_submit_enhanced_request_chains.json`
- `voice_governed_submit_stage_mapping.json`
- `voice_governed_submit_gate_position_matrix.json`
- `voice_governed_submit_hard_audit_summary.json`
- `voice_governed_submit_request_trace_trace.jsonl`
- `voice_governed_submit_request_trace_replay.jsonl`
- `voice_governed_submit_request_trace_whitebox.jsonl`
- `evaluation_notes.md`

---

## Join 规则

- **Primary**：`request_id`
- **Secondary（可追溯）**：`source_governance_decision_id` / audit envelope（来自 Phase-007 与 Phase-005 stages 内 refs）

未匹配的 Phase-007 decision 写入 summary `stats.unmatched_submit_decisions`。

---

## 边界（必须）

- 不真实播报、不执行真实 TTS、不接新 provider、不删 legacy voice、不改 env 语义  
- 不把治理链接入真实 submit、不修改真实主链源码  
- 不写世界模型、不上传蜂巢、不接推荐系统  
