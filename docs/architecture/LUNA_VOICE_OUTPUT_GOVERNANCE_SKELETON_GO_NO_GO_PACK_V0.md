# Phase-Voice-OutputGovernance-002
# Voice Output Governance Minimal Skeleton Go/No-Go Pack v0（决策包）

**目标**：产出可运行的“干跑治理骨架”，把输出治理链跑通（guard/gate/expiry/priority/cancel/provider health/audit/trace/replay/whitebox），但仍不真实播报。

---

## 1. GO 条件

- `guard_v1_speakable_text` **可 import**（Phase-001-Fix required followup #1 已解决）
- SpeechGate **被 skeleton 调用**，并在 decision/trace/whitebox 可观测（required followup #2 已解决）
- `sample_matrix` 覆盖：expiry/stale/priority/interrupt/cancel/provider health/guard block
- decisions 生成且数量与样本一致
- 不变量全部满足：
  - `real_tts_invoked=false`
  - `provider_invoked=false`
  - `playback_invoked=false`
  - `navigation_action=null`
  - `downstream_invocation_count=0`
- trace/replay/whitebox 非空
- `tools/verify_voice_output_governance_v0.py` 通过
- 不改 runtime 主链与现有 env 开关语义

---

## 2. CONDITIONAL_GO

- guard 以 alias/映射方式落地（不是同名函数），但：
  - 文档明确映射关系
  - verifier 能稳定 import 并验证 guard_name

---

## 3. NO_GO 条件

- guard 仍不可定位/不可 import
- SpeechGate 未被调用（或无法在输出中证明被调用）
- expired / stale / cancelled 样本被 accepted_dry_run
- low priority 可打断 safety
- 任一不变量被破坏（real_tts_invoked/playback_invoked/provider_invoked 任一为 true）
- 本阶段接新 provider 或删除 legacy voice

---

## 4. 验收输出

- output_root 目录下产物齐全：
  - `voice_output_governance_summary.json`
  - `voice_output_governance_inputs.json`
  - `voice_output_governance_decisions.json`
  - `voice_provider_health_states.json`
  - `voice_output_audit_envelopes.json`
  - `voice_output_trace.jsonl`
  - `voice_output_replay.jsonl`
  - `voice_output_whitebox.jsonl`
  - `verification_result.json`

