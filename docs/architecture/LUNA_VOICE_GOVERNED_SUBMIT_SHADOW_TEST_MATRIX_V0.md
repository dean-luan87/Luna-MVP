# Phase-Voice-OutputGovernance-007
# Governed Submit Shadow Test Matrix v0

**样本来源**：沿用 Phase-002 的 10 个样本（`voice_output_governance_decisions.json`）。

---

## A. Roots 可读性

- A1：governance root 可读
- A2：request trace root 可读

---

## B. 产物生成

- B1：shadow inputs/decisions/audit envelopes 生成
- B2：trace/replay/whitebox JSONL 生成且非空

---

## C. 映射覆盖（核心）

- C1：`accepted_dry_run` → `submit_allowed_shadow`
- C2：expired → `submit_expired_shadow`
- C3：cancelled / cancel_requested → `submit_cancelled_shadow`
- C4：fallback_candidate → `submit_fallback_candidate_shadow`
- C5：unspeakable / suppressed / rejected → `submit_blocked_shadow`

---

## D. 两种 gate position（只模拟）

- D1：每个 request_id 至少有两条 shadow decision：
  - `_maybe_submit_real_output_v1_pre`
  - `VoiceOutputPlane.submit_entry`

---

## E. Hard Audit 不变量

- `real_submit_invoked=false`
- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

