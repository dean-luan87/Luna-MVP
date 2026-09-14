# Field State Reducer Behavior Policy Controlled Skeleton Implementation v1

## 当前工作内容描述

本阶段将 Behavior Policy Technical Planning 资产映射为受控 Python Skeleton：类型、注册表、静态校验、占位决策、trace/replay、synthetic fixture、controlled skeleton runner 与阶段 verifier。仅建设受控骨架，不执行真实策略语义。

## 阶段位置

Phase-Luna-Field-State-Reducer-Behavior-Policy-Technical-Planning-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Skeleton-Implementation-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-DryRun-v1-001

## Planning-to-Code 映射

- registry -> behavior policy registry skeleton
- eligibility matrix -> eligibility skeleton placeholder output
- precedence matrix -> precedence skeleton registered rules
- composition contract -> composition skeleton boundary
- decision schema -> decision skeleton dataclass + trace shape
- replay contract -> replay snapshot/replay key fields
- negative guards -> skeleton guards and validators

## Skeleton 定位

- skeleton_only = true
- candidate_only = true
- policy_execution_executed = false
- state_mutation_executed = false
- fact_promotion_executed = false
- action_trigger_executed = false
- runtime_execution = false

## Registry Skeleton

- 11 个 policy 全部映射为静态注册行。
- 全部保持 implemented/runtime_callable/real_execution/fact_promotion/state_write/action_trigger 为 false。

## Eligibility Skeleton

- 只校验输入边界和静态候选 policy 列举。
- 输出 placeholder eligibility，不执行真实 eligibility 判定。

## Precedence Skeleton

- 注册撤销优先、冲突保留、证据不足回退、overlay 分层规则。
- 输出 placeholder precedence sequence，不执行真实 winner 裁决。

## Composition Skeleton

- 最大组合深度固定为 3。
- side effect/state write/action trigger 均禁止。
- 输出 placeholder composition sequence。

## Decision Skeleton

- 输入静态候选 policy 与 placeholder 结果。
- 输出 skeleton policy decision 与 no_state_change 边界。
- resulting_state_candidate 固定为 null。

## Trace / Replay

- 记录 candidate/eligible/rejected/selected/precedence/composition 输入痕迹。
- 构造 deterministic replay key 与 snapshot 版本字段。

## non-runtime 边界

- 不做真实 policy selection。
- 不做真实 policy execution。
- 不做真实 precedence/composition。
- 不做 confidence aggregation。
- 不做 conflict resolution。
- 不创建 active state。
- 不执行 state mutation/fact promotion/action trigger。
- 不进行 provider recall/external lookup/model call。

## 与下一阶段 Controlled DryRun 的关系

本阶段只完成可导入、可静态检查、可被 controlled dryrun 调用的骨架基础。下一阶段才进入受控 dryrun 执行与结果比对。

## 适可而止条件

- Required Final Files 完整。
- V0 静态检查完成。
- 不运行 Final Phase Verifier。

## 停止条件

输出 WAITING_FOR_USER_TERMINAL_VERIFICATION。
