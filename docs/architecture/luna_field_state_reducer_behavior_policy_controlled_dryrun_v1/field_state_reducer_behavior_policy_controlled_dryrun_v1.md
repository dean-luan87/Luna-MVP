# Field State Reducer Behavior Policy Controlled DryRun v1

## 当前工作内容描述

本阶段在不改变上一阶段 Skeleton 语义的前提下，执行 synthetic、isolated、no-side-effect 的 Behavior Policy Controlled DryRun，验证调用链稳定性与边界约束。

## 阶段位置

Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Skeleton-Implementation-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-DryRun-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Policy-Evaluation-Technical-Planning-v1-001

## Positive Cases

- registry_loading_case
- baseline_placeholder_chain_case
- repeated_identical_input_case
- reversed_candidate_order_case
- conflict_preservation_candidate_case
- temporary_overlay_candidate_case
- owner_correction_candidate_case
- insufficient_evidence_no_state_change_case

## Negative Cases

- unknown_policy_id_rejection_case
- unknown_state_type_rejection_case
- missing_policy_registry_snapshot_case
- missing_eligibility_snapshot_case
- missing_precedence_snapshot_case
- missing_composition_snapshot_case
- runtime_request_rejection_case
- direct_state_write_rejection_case
- fact_promotion_rejection_case
- action_trigger_rejection_case
- provider_recall_rejection_case
- external_lookup_rejection_case

## Skeleton Chain

Validator -> Eligibility Skeleton -> Precedence Skeleton -> Composition Skeleton -> Decision Skeleton -> Trace/Replay.

## Determinism

相同输入与相同快照必须产生相同核心输出。非确定性字段（created_at、run_id、duration 等）排除于核心比较之外。

## Candidate Order

reversed_candidate_order_case 验证候选输入顺序不是最终权威，核心输出与 replay key 保持稳定。

## Fixture Immutability

Runner 对 fixture 使用 deep copy，执行前后比较原始 fixture 不可变。

## Registry Immutability

Runner 执行前后比较 registry 快照，不允许变更。

## Trace / Replay

验证 decision/trace 输出中的 candidate/eligible/rejected/selected、precedence/composition、replay_key 字段完整。

## non-runtime 边界

- 不执行真实 Policy Evaluation / Selection / Function。
- 不创建 active state。
- 不做 state mutation / fact promotion / action trigger。
- 不执行 provider recall / external lookup / model call。
- 不创建 database / scheduler / message queue / event consumer / runtime loop。

## 与下一阶段关系

本阶段仅验证受控 dryrun 链路稳定，下一阶段进入 Controlled Policy Evaluation Technical Planning。

## 适可而止条件

- Required Final Files 完整。
- 一次 V0 完成。
- 一次 Runner 完成。
- 一次 Result Verifier 完成。

## 停止条件

Agent 停止在 WAITING_FOR_USER_TERMINAL_VERIFICATION 或 BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION。
