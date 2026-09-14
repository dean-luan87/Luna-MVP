# Phase-Voice-OutputGovernance-004
# Voice Output TRW Stage Namespace v0（阶段命名空间）

**目标**：统一 voice output governance 的 stage 命名空间与阶段顺序，供 TRW extractor/白盒抽链规则使用。

---

## 1. Namespace

- `voice_output_governance_v0`

---

## 2. Ordered stages（顺序固定）

1. candidate_input
2. speakable_guard
3. speech_gate
4. expiry_check
5. stale_check
6. cancellation_check
7. priority_check
8. interruption_check
9. suppression_check
10. provider_health_check
11. final_governance_decision
12. audit_envelope

---

## 3. 解释口径（最小）

- `status` 建议枚举：passed / blocked / suppressed / cancelled / fallback_candidate / dry_run_accepted
- `reason`：优先使用 suppression_reason / gate reason / provider health reason 的短字符串
- `hard_audit`：必须随 record 一起输出，用于“是否触发真实副作用”的硬审计

