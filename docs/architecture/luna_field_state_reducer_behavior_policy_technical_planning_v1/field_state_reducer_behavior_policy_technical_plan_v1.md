# Field State Reducer Behavior Policy Technical Planning v1

## 当前工作内容描述
本阶段只定义 Policy Layer 技术规划合同：策略注册、可适用性、优先级、组合、状态类型映射、时间影响、置信度影响、冲突保留、Owner Correction、Overlay 隔离、Replay 快照与最小案例。仅规划，不实现策略函数。

## 阶段位置
Phase-Luna-Field-State-Reducer-Controlled-DryRun-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Technical-Planning-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Skeleton-Implementation-v1-001

## Policy Layer 定位
- Policy Layer 为 Reducer 决策输入层，不是宪法层。
- Policy Layer 不拥有 Fact Admission 权。
- Policy Layer 不拥有 Action Trigger 权。
- Policy Layer 不拥有直接 State Store 写权。

## 与 Reducer Technical Planning 的关系
- 复用现有 11 个 policy 名称与 state/temporal/conflict/confidence 基础合同。
- 细化 policy eligibility、precedence、composition 与 replay 快照要求。

## 与 Controlled Skeleton / DryRun 的关系
- 保持 implemented=false、runtime_callable=false。
- 保持 candidate-only 与 no-state-mutation 边界。
- 保持 deterministic ordering / replay key 思路，不引入真实归约执行。

## Policy Selection
- 先按 state_type 与 temporal/conflict/confidence 条件过滤候选策略。
- 再按 precedence class 与 deterministic tie-breaker 选取策略序列。
- 若无安全可执行策略，回退 no_state_change 或 unresolved。

## Policy Eligibility
- admitted_only=true。
- revoked/expired/suspended 采用显式行为约束，不允许隐式恢复。
- owner correction 仅在 governed candidate 条件下允许。

## Policy Precedence
- revocation_override 优先于普通 support selection。
- conflict_preservation 优先于不安全单一 winner。
- insufficient_evidence_unresolved 优先于 fabricated state。
- temporary_overlay_separation 优先于 substrate overwrite。
- expiration_degrade 优先于继续使用 expired support。

## Policy Composition
- sequential / guarded / fallback / overlay_parallel / conflict_parallel_preservation。
- 组合深度受限，顺序 deterministic。
- 组合过程禁止 side effect、state write、action trigger。

## State Type Mapping
- 覆盖 12 个 state types。
- 每个 state type 定义 allowed/prohibited/default_fallback/minimum_support 与 policy refs。
- latest/highest confidence 不能作为全局默认。

## Temporal Influence
- 覆盖 8 个 temporal statuses。
- expired/revoked/superseded 不能继续作为 active support。
- suspended 不允许自动恢复。
- unknown 不允许自动变 active。

## Confidence Influence
- 按 state type 差异化定义 aggregation_mode 与 threshold。
- simple average 不能全局默认。
- no automatic 100 confidence。
- fabricated confidence 不允许。

## Conflict Preservation
- 冲突无法安全消解时，优先 preserve_conflict 与 unresolved。
- 不允许伪造 winner 推进 state。

## Owner Correction
- owner correction 是 candidate，不是 fact。
- 需要 supporting evidence、contradiction review、provenance。
- 未经评审不得覆盖 confirmed fact。

## Overlay Separation
- overlay 与 substrate 分层。
- overlay 可临时 mask，不可永久替换 substrate。
- overlay 结束需要 substrate refresh，不允许无证据自动恢复。

## Replay Versioning
- 回放锁定：policy registry / eligibility / precedence / composition / state mapping / confidence / temporal / conflict snapshots。
- 禁止 replay 时 external lookup/provider recall/action trigger。

## Provenance
- Decision schema 记录 candidate/eligible/rejected/selected policies、precedence steps、inputs、outcome、snapshot versions。
- 保证可解释、可追踪、可重放。

## Failure Policy
- 不满足 eligibility 或冲突无法安全决策时：mark_unresolved / preserve_conflict / no_state_change。

## Non-Goals
- 不实现真实 policy function。
- 不执行真实 policy selection/composition/confidence aggregation/conflict resolution。
- 不创建 active state，不执行 state mutation。

## 适可而止条件
- 本阶段 20 个文件齐备。
- JSON 全部可解析。
- phase verifier 语法可编译且检查项齐备。

## 停止条件
- 完成静态检查后停止，等待用户终端执行最终 phase verifier。
