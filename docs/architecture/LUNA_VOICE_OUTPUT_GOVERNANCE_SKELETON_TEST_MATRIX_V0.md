# Phase-Voice-OutputGovernance-002
# Voice Output Governance Skeleton Test Matrix v0（测试矩阵）

**目的**：保证最小骨架覆盖 expiry/priority/cancel/interrupt/provider health/guard/gate，并严格保持 dry-run 边界。

---

## 1. 样本矩阵入口

- `datasets/voice_output_governance_samples_v0/sample_matrix.json`

---

## 2. 覆盖点（必须命中）

- **normal_speakable_dry_run**：可播报文本 → accepted_dry_run
- **expired_request**：过期 → suppressed_expired
- **stale_navigation_instruction**：stale → suppressed_stale
- **cancelled_request**：cancel_requested → cancelled
- **duplicate_low_priority**：cooldown_key 重复 → suppressed_duplicate_or_cooldown
- **low_priority_interrupt_attempt**：chat 试图打断 safety → interrupt_denied
- **high_priority_interrupt_allowed**：safety 打断 chat（policy allow）→ accepted_dry_run（interrupt allowed）
- **provider_unhealthy**：provider unhealthy/dep not ready → fallback_candidate（不执行 provider）
- **unspeakable_text**：占位/内部文本 → guard_blocked
- **uncertain_text_must_not_be_certain**：不确定 + 绝对确定混用 → guard degrade（文本被降级）

---

## 3. 边界断言（所有样本都必须）

- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`
- trace/replay/whitebox 产物非空

