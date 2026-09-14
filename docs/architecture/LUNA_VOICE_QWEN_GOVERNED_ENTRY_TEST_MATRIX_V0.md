# LUNA Voice — Governed Entry Skeleton Test Matrix v0（Phase-Voice-Qianwen-002）

**样本根**：`logs/voice_output_governance_002_test_run`（Phase-002 十个 governance 样例）。

---

## 1. 样本 → 期望（dry-run）

| sample_id | governance final_action（期望） | online_prefer_qwen（dry-run 选中） | offline_only（dry-run 选中） |
|-----------|----------------------------------|-------------------------------------|-------------------------------|
| normal_speakable_dry_run | accepted_dry_run | qwen | piper |
| expired_request | suppressed | none | none |
| stale_navigation_instruction | suppressed | none | none |
| cancelled_request | cancelled | none | none |
| duplicate_low_priority | suppressed | none | none |
| low_priority_interrupt_attempt | suppressed | none | none |
| high_priority_interrupt_allowed | accepted_dry_run | qwen | piper |
| provider_unhealthy | fallback_candidate | piper（健康回退语义） | piper |
| unspeakable_text | suppressed | none | none |
| uncertain_text_must_not_be_certain | accepted_dry_run | qwen | piper |

---

## 2. 专项断言

- **blocked / suppressed / cancelled**：**不得**出现 `selected_provider=qwen`。  
- **offline_only**：任意 `entry_allowed` 样本 **`provider_order` 不含 qwen**，且 **`selected_provider != qwen`**。  
- **uncertain_text**：允许 guard 归一化 → `text_diff_audit.text_changed=true` 且 **`rewrite_allowed=true`**（guard 路径）。  
- **hard_audit**：所有样本 **`real_qwen_invoked=false`、`real_tts_invoked=false`、`provider_invoked=false`**。

---

## 3. Verifier

由 `tools/verify_voice_qwen_governed_entry_skeleton_v0.py` 对照上述矩阵做静态校验（含 trace/replay/whitebox 非空、`voice_tts_config.yaml` 基线不变）。
