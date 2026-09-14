# Phase-Voice-OutputGovernance-007
# Governed Submit Shadow Decision Schema v0

本文件冻结 `VoiceGovernedSubmitShadowDecision` 的最小 schema（shadow-only）。

---

## 1. Decision schema（v0）

```json
{
  "submit_shadow_decision_id": "...",
  "request_id": "...",
  "source_governance_decision_id": "...",
  "source_audit_envelope_id": "...",
  "runtime_mode": "shadow",
  "candidate_text": "...",
  "submit_gate_position": "_maybe_submit_real_output_v1_pre | VoiceOutputPlane.submit_entry",
  "governance_final_action": "accepted_dry_run | suppressed | cancelled | fallback_candidate | rejected",
  "submit_shadow_result": "submit_allowed_shadow | submit_blocked_shadow | submit_expired_shadow | submit_cancelled_shadow | submit_fallback_candidate_shadow",
  "submit_allowed": false,
  "submit_block_reason": null,
  "expiry_checked": true,
  "cancel_checked": true,
  "speech_gate_checked": true,
  "provider_health_checked": true,
  "hard_audit": {
    "real_submit_invoked": false,
    "real_tts_invoked": false,
    "playback_invoked": false,
    "provider_invoked": false,
    "navigation_action": null,
    "downstream_invocation_count": 0
  },
  "trace_ref": "...",
  "replay_ref": "...",
  "whitebox_ref": "..."
}
```

---

## 2. 合同要点

- 不调用真实 submit：`real_submit_invoked=false`
- 不执行真实 TTS/播放：`real_tts_invoked=false`、`playback_invoked=false`、`provider_invoked=false`
- 不执行导航动作：`navigation_action=null`
- 不做下游调用：`downstream_invocation_count=0`
- `trace_id/session_id` 缺失不得伪造（本阶段不引入）

