# Field State Reducer Technical Plan v1

## 1. Reducer 定位
- Field State Reducer 是 Field State 的唯一合法 mutation authority。
- 所有 Field State 创建、更新、降级、挂起、过期、撤销、恢复必须经 Reducer 决策。
- Reducer 仅属于技术规划层，不实现 runtime。

## 2. 单一 Mutation Authority
- reducer_is_single_mutation_authority = true
- vision_state_mutation_allowed = false
- ocr_state_mutation_allowed = false
- speech_state_mutation_allowed = false
- navigation_state_mutation_allowed = false
- memory_state_mutation_allowed = false
- planner_state_mutation_allowed = false
- skill_state_mutation_allowed = false
- provider_state_mutation_allowed = false

## 3. 输入与输出边界
- 输入仅允许已准入 Field Events 与版本化快照。
- 输出仅允许 state decision 与 trace，不包含 action trigger。
- Reducer 不得调用外部模型补齐信息。

## 4. 归约生命周期
1. Input boundary 校验
2. Event ordering 计算
3. Temporal gating
4. Conflict resolution
5. Confidence aggregation
6. State transition legality check
7. State write proposal generation
8. Provenance trace generation

## 5. Deterministic Replay
- 相同 event set、ordering policy、reducer version、registry version、temporal evaluation time、config snapshot 产生相同结果。
- replay 禁止 provider recall、external lookup、action trigger。

## 6. Conflict Handling
- 冲突优先保留而非强行消解。
- 不满足安全消解条件时状态进入 conflicted 或 unresolved。
- fact_promotion_allowed 始终为 false。

## 7. Temporal Handling
- expired 事件不可继续作为 active support。
- revoked 事件不可重新激活。
- suspended 事件不可自动恢复。
- temporary overlay 不可永久写入 substrate state。
- overlay 结束后必须 refresh 再评估 substrate evidence。

## 8. Provenance
- 每次归约必须留下完整输入、排序、接受/拒绝、冲突、结果哈希与 replay key。
- state 标记 derived_not_observed = true。

## 9. Versioning
- reducer_version
- reduction_policy_version
- event_registry_version
- temporal_snapshot_ref
- configuration_snapshot_ref

## 10. Failure Policy
- 输入不合法时拒绝归约。
- 冲突不可安全消解时保留 unresolved。
- transition 非法时拒绝状态变更并记录 blocker。

## 11. 上下游关系
- 上游：Field Event Temporal Validity Protocol 输出。
- 下游：Field State Read Model / Query Surface。
- Reducer 不具备 Fact Admission 权限。

## 12. 非目标
- 不实现 Reducer runtime。
- 不实现数据库或 scheduler。
- 不实现消息队列与实时消费。
- 不接入 Vision/OCR/Navigation/Task Manager runtime。

## 13. 停止条件
- 本目录 22 个正式文件全部就位。
- JSON 合法，Verifier 全通过。
- blocker_count = 0。
- 不进入 Skeleton Implementation。
