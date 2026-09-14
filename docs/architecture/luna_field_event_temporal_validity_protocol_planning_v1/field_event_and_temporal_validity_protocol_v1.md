# Field Event and Temporal Validity Protocol v1

## A. Protocol Purpose

该协议负责：
- 所有 Field State 变化必须由事件驱动。
- 事件必须带来源、证据、时间、立场和治理信息。
- 时间有效性决定定义当前是否可参与 Active Projection。
- 支持历史回放、撤回、失效、修正和临时覆盖。

协议不得负责：
- 执行模型。
- 直接生成事实。
- 实现 Reducer。
- 选择存储产品。
- 修改人格。
- 生成情感。
- 执行动作。

## B. Field Event Taxonomy

### Observation Events

#### field_definition_observed
- purpose: 记录对场定义的观察输入。
- source requirements: 传感器、用户观察、系统监控。
- evidence requirements: 需要原始观察证据引用。
- temporal requirements: observed_at, occurred_at。
- perspective requirements: perspective_scope, field_scope。
- allowed target types: field_definition, space_anchor。
- prohibited mutations: 不得直接创建事实状态。
- governance refs: Evidence Chain, Trace and Diagnostics。
- replay behavior: 可回放为观察经历。
- rollback behavior: 事件拒绝前回滚。

#### field_relation_observed
- purpose: 记录场之间关系的观察。
- source requirements: 观察者、系统分析。
- evidence requirements: 关系证据、空间锚点。
- temporal requirements: observed_at, occurred_at。
- perspective requirements: perspective_scope。
- allowed target types: field_relation。
- prohibited mutations: 不得直接构建关系事实。
- governance refs: Evidence Chain, Human Correction。
- replay behavior: 用于恢复关系候选。
- rollback behavior: 事件验证失败前回滚。

#### entity_field_relation_observed
- purpose: 记录 Entity Candidate 在当前 Field Context 中被观察到的候选关系。
- source requirements: 已 admission 的观察事件、Entity/Relation Candidate 引用。
- evidence requirements: 视觉证据、Entity Candidate、Relation Candidate lineage。
- temporal requirements: observed_at, occurred_at。
- perspective requirements: perspective_scope, field_scope。
- allowed target types: entity_field_relation_candidate。
- prohibited mutations: 不得直接构建关系事实、Field Truth 或 World Truth。
- replay behavior: 用于恢复 candidate-only Entity↔Field observation relation。
- rollback behavior: 事件验证失败前回滚。

#### social_activity_observed
- purpose: 记录社交活动的观察。
- source requirements: 群体行为观测、社交传感器。
- evidence requirements: 活动证据、时间窗口。
- temporal requirements: observed_at, duration。
- perspective requirements: social perspective。
- allowed target types: social_definition, temporary_overlay。
- prohibited mutations: 不得直接写入 institutional 定义。
- governance refs: Social Coexistence Policy, Trace and Diagnostics。
- replay behavior: 支持社交活动历史回放。
- rollback behavior: 事件无效前回滚。

#### institutional_condition_observed
- purpose: 记录制度性条件的观察。
- source requirements: 规则引用、监管记录。
- evidence requirements: 法规证据、审批引用。
- temporal requirements: observed_at, asserted_at。
- perspective requirements: institutional perspective。
- allowed target types: institutional_definition。
- prohibited mutations: 不得自动升级为 public fact。
- governance refs: Permission / Owner Approval, Evidence Chain。
- replay behavior: 用于制度状态重建。
- rollback behavior: 事件拒绝前回滚。

#### temporary_overlay_observed
- purpose: 记录临时覆盖的观察输入。
- source requirements: 现场观察、事件通告。
- evidence requirements: overlay 证据、时间范围。
- temporal requirements: observed_at, expected_duration。
- perspective requirements: overlay scope。
- allowed target types: temporary_overlay。
- prohibited mutations: 不得持久改变 substrate。
- governance refs: Temporary Overlay Policy, Trace and Diagnostics。
- replay behavior: 用于 overlay 生命周期回放。
- rollback behavior: 事件验证失败前回滚。

### Assertion Events

#### field_definition_asserted
- purpose: 断言场定义。
- source requirements: 认证主体、领域专家。
- evidence requirements: assertion 证据、引用来源。
- temporal requirements: asserted_at, valid_from。
- perspective requirements: owner_scope, perspective_scope。
- allowed target types: field_definition。
- prohibited mutations: 不得直接写入事实。
- governance refs: Candidate / Fact Admission, Permission / Owner Approval。
- replay behavior: 用于断言历史回放。
- rollback behavior: 事件撤回前回滚。

#### personal_name_asserted
- purpose: 记录用户对场所名称的个人断言。
- source requirements: 用户声明。
- evidence requirements: 命名声明。
- temporal requirements: asserted_at, valid_from。
- perspective requirements: personal perspective。
- allowed target types: personal_definition。
- prohibited mutations: 不得转为公共事实。
- governance refs: Personal Public Isolation, Trace and Diagnostics。
- replay behavior: 个人命名历史可回放。
- rollback behavior: 更正前回滚。

#### social_convention_asserted
- purpose: 记录社会惯例或共识断言。
- source requirements: 社区声明、社交证据。
- evidence requirements: 社会证据、时间范围。
- temporal requirements: asserted_at, valid_from。
- perspective requirements: social perspective。
- allowed target types: social_definition。
- prohibited mutations: 不得自动覆盖 institutional 定义。
- governance refs: Coexistence Policy, Human Correction。
- replay behavior: 用于社会惯例回放。
- rollback behavior: 更正前回滚。

#### institutional_rule_asserted
- purpose: 记录制度规则断言。
- source requirements: 官方来源、监管文档。
- evidence requirements: 规则文本、授权证据。
- temporal requirements: asserted_at, valid_from。
- perspective requirements: institutional perspective。
- allowed target types: institutional_definition。
- prohibited mutations: 不得直接生成行为事实。
- governance refs: Permission / Owner Approval, Change Control。
- replay behavior: 规则变化可回放。
- rollback behavior: 规则撤回前回滚。

#### user_confirmation_asserted
- purpose: 记录用户确认或否认。
- source requirements: 用户交互。
- evidence requirements: 确认凭证。
- temporal requirements: asserted_at。
- perspective requirements: user perspective。
- allowed target types: candidate_definition, personal_definition。
- prohibited mutations: 不得直接写入 substrate。
- governance refs: Human Correction, Trace and Diagnostics。
- replay behavior: 确认历史可以回放。
- rollback behavior: 更正前回滚。

### Lifecycle Events

#### field_candidate_activated
- purpose: 标记候选场定义进入活跃候选。
- source requirements: admission、governance approval。
- evidence requirements: admission evidence、governance tags。
- temporal requirements: occurred_at, valid_from。
- perspective requirements: perspective_scope。
- allowed target types: candidate_definition。
- prohibited mutations: 不得直接将 candidate 视为事实。
- governance refs: Candidate / Fact Admission, Post-Review / Freeze。
- replay behavior: activation 历史可回放。
- rollback behavior: activation 申请失败前回滚。

#### field_candidate_suspended
- purpose: 标记候选进入挂起状态。
- source requirements: conflict detection、temporary overlay。
- evidence requirements: conflict evidence、temporal evidence。
- temporal requirements: occurred_at, suspension window。
- perspective requirements: field_scope。
- allowed target types: admitted_candidate。
- prohibited mutations: 不得删除候选。
- governance refs: Change Control, Temporary Overlay Policy。
- replay behavior: 挂起历史可回放。
- rollback behavior: 挂起前回滚。

#### field_candidate_expired
- purpose: 标记候选过期。
- source requirements: temporal expiry 规则。
- evidence requirements: expiry evidence。
- temporal requirements: expired_at, valid_until。
- perspective requirements: field_scope。
- allowed target types: admitted_candidate。
- prohibited mutations: 不得自动恢复为 active。
- governance refs: Temporal Validity Policy, Trace and Diagnostics。
- replay behavior: 过期历史可回放。
- rollback behavior: expiry 申明失败前回滚。

#### field_candidate_superseded
- purpose: 标记候选被新定义替代。
- source requirements: revision event、governance approval。
- evidence requirements: supersession evidence。
- temporal requirements: occurred_at。
- perspective requirements: field_scope。
- allowed target types: candidate_definition。
- prohibited mutations: 不得删除旧候选。
- governance refs: Change Control, Rollback / Revocation。
- replay behavior: supersession 历史可回放。
- rollback behavior: supersession 申请失败前回滚。

#### field_candidate_revoked
- purpose: 标记候选撤回。
- source requirements: revocation request、human correction。
- evidence requirements: revocation evidence。
- temporal requirements: occurred_at, revoked_at。
- perspective requirements: owner_scope。
- allowed target types: candidate_definition。
- prohibited mutations: 不得隐性删除事件。
- governance refs: Human Correction, Rollback / Revocation。
- replay behavior: 撤回历史必须保留。
- rollback behavior: revocation 失败前回滚。

#### field_candidate_archived
- purpose: 标记候选归档为历史记录。
- source requirements: timeline retention。
- evidence requirements: 归档凭证。
- temporal requirements: occurred_at。
- perspective requirements: field_scope。
- allowed target types: candidate_definition。
- prohibited mutations: 不得改变 archive 数据。
- governance refs: Trace and Diagnostics, Post-Review / Freeze。
- replay behavior: 归档事件可回放。
- rollback behavior: archive 前回滚。

### Temporal Events

#### temporal_interval_started
- purpose: 记录时间区间的开始。
- source requirements: event or assertion。
- evidence requirements: interval definition。
- temporal requirements: valid_from。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得自动写回 substrate。
- governance refs: Temporal Validity Policy, Trace and Diagnostics。
- replay behavior: interval 开始可回放。
- rollback behavior: interval 开始前回滚。

#### temporal_interval_ended
- purpose: 记录时间区间结束。
- source requirements: expiry detection。
- evidence requirements: interval end evidence。
- temporal requirements: valid_until, expired_at。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得自动恢复旧状态。
- governance refs: Temporal Validity Policy。
- replay behavior: interval 结束可回放。
- rollback behavior: end event 失败前回滚。

#### recurrence_window_opened
- purpose: 记录周期窗口开始。
- source requirements: recurrence schedule。
- evidence requirements: recurrence pattern evidence。
- temporal requirements: recurrence start。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得视为确定性事实。
- governance refs: Negative Guards, Temporal Validity Policy。
- replay behavior: recurrence window 可回放。
- rollback behavior: window 开始前回滚。

#### recurrence_window_closed
- purpose: 记录周期窗口结束。
- source requirements: recurrence schedule。
- evidence requirements: recurrence evidence。
- temporal requirements: recurrence end。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得视为周期永远成立。
- governance refs: Temporal Validity Policy。
- replay behavior: recurrence window 结束可回放。
- rollback behavior: window 关闭前回滚。

#### temporary_overlay_started
- purpose: 记录临时覆盖开始。
- source requirements: overlay evidence。
- evidence requirements: overlay activation evidence。
- temporal requirements: observed_at, expected_duration。
- perspective requirements: overlay scope。
- allowed target types: temporary_overlay。
- prohibited mutations: 不得持久改变 substrate。
- governance refs: Temporary Overlay Policy, Safety Overlay。
- replay behavior: overlay 开始可回放。
- rollback behavior: overlay 开始前回滚。

#### temporary_overlay_ended
- purpose: 记录临时覆盖结束。
- source requirements: overlay expiration。
- evidence requirements: end evidence。
- temporal requirements: expired_at。
- perspective requirements: overlay scope。
- allowed target types: temporary_overlay。
- prohibited mutations: 不得直接恢复旧状态。
- governance refs: Temporary Overlay Policy.
- replay behavior: overlay 结束可回放。
- rollback behavior: overlay 结束前回滚。

#### refresh_due
- purpose: 记录定义需要刷新证据。
- source requirements: refresh policy。
- evidence requirements: refresh trigger evidence。
- temporal requirements: refresh_at。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得自动触发状态恢复。
- governance refs: Change Control, Trace and Diagnostics。
- replay behavior: refresh request 可回放。
- rollback behavior: refresh 标记前回滚。

#### temporal_definition_stale
- purpose: 标记 temporal 定义变得 stale。
- source requirements: stale threshold。
- evidence requirements: lack of fresh evidence。
- temporal requirements: stale_after。
- perspective requirements: field_scope。
- allowed target types: temporal_definition。
- prohibited mutations: 不得直接激活 stale 定义。
- governance refs: Negative Guards, Trace and Diagnostics。
- replay behavior: stale 历史可回放。
- rollback behavior: stale 标记前回滚。

### Correction Events

#### human_correction_submitted
- purpose: 提交人工更正事件。
- source requirements: human operator。
- evidence requirements: correction rationale。
- temporal requirements: occurred_at, asserted_at。
- perspective requirements: owner_scope。
- allowed target types: any affected definition。
- prohibited mutations: 不得绕过 event pipeline。
- governance refs: Human Correction, Trace and Diagnostics。
- replay behavior: correction 可回放。
- rollback behavior: correction申请前回滚。

#### field_definition_corrected
- purpose: 记录场定义修正。
- source requirements: correction event。
- evidence requirements: corrected evidence。
- temporal requirements: asserted_at。
- perspective requirements: field_scope。
- allowed target types: field_definition。
- prohibited mutations: 不得直接覆盖历史。
- governance refs: Revision / Revocation, Change Control。
- replay behavior: correction 历史可回放。
- rollback behavior: correction前回滚。

#### evidence_retracted
- purpose: 标记证据被撤销。
- source requirements: source rescind.
- evidence requirements: retraction rationale。
- temporal requirements: occurred_at。
- perspective requirements: evidence_scope。
- allowed target types: evidence_refs.
- prohibited mutations: 不得直接删除事实。
- governance refs: Evidence Chain, Trace and Diagnostics。
- replay behavior: retraction 历史可回放。
- rollback behavior: retraction前回滚。

#### revocation_requested
- purpose: 请求事件撤回。
- source requirements: revoke authority.
- evidence requirements: revocation rationale.
- temporal requirements: occurred_at.
- perspective requirements: owner_scope.
- allowed target types: target_event_ref.
- prohibited mutations: 不得删除历史事件。
- governance refs: Rollback / Revocation, Human Correction.
- replay behavior: revocation 请求可回放。
- rollback behavior: 请求失败前回滚。

#### revision_applied
- purpose: 记录修订已应用。
- source requirements: revision approval.
- evidence requirements: revision evidence.
- temporal requirements: occurred_at.
- perspective_requirements: field_scope.
- allowed target types: revised_definition.
- prohibited mutations: 不得删除旧定义历史。
- governance refs: Change Control, Trace and Diagnostics.
- replay behavior: revision 应用可回放。
- rollback behavior: 应用前回滚。

### Transition Events

#### field_transition_detected
- purpose: 记录场状态变化检测。
- source requirements: 状态变化算法。
- evidence requirements: transition evidence.
- temporal requirements: occurred_at.
- perspective requirements: field_scope.
- allowed target types: field_definition, field_relation.
- prohibited mutations: 不得直接应用状态。
- governance refs: Trace and Diagnostics.
- replay behavior: transition 历史可回放。
- rollback behavior: detection前回滚。

#### child_field_entered
- purpose: 记录进入子场。
- source requirements: 观察或推断。
- evidence requirements: child field evidence.
- temporal requirements: occurred_at.
- perspective requirements: field_scope.
- allowed target types: micro_field.
- prohibited mutations: 不得修改 parent_field.
- governance refs: Field Hierarchy, Trace and Diagnostics.
- replay behavior: child field入口可回放。
- rollback behavior: entry前回滚。

#### parent_field_exited
- purpose: 记录退出父场。
- source requirements: 观察或推断。
- evidence requirements: exit evidence.
- temporal requirements: occurred_at.
- perspective requirements: field_scope.
- allowed target types: macro_field.
- prohibited mutations: 不得修改 child_field.
- governance refs: Field Hierarchy.
- replay behavior: exit event可回放。
- rollback behavior: exit前回滚。

#### overlapping_field_activated
- purpose: 记录重叠场激活。
- source requirements: overlap detection.
- evidence requirements: overlap evidence.
- temporal requirements: occurred_at.
- perspective requirements: field_scope.
- allowed target types: overlapping_field.
- prohibited mutations: 不得破坏 coexistence.
- governance refs: Multi-Reality Coexistence.
- replay behavior: overlap activation可回放。
- rollback behavior: activation前回滚。

#### active_projection_changed
- purpose: 记录 ActiveFieldProjection 变化。
- source requirements: projection engine output.
- evidence requirements: projection rationale.
- temporal requirements: occurred_at.
- perspective requirements: selected_perspective.
- allowed target types: projection_candidate.
- prohibited mutations: 不得写回 substrate.
- governance refs: Candidate / Fact Admission, Trace and Diagnostics.
- replay behavior: projection change可回放。
- rollback behavior: change前回滚。

## C. Unified FieldEvent Envelope

FieldEvent Envelope 必须包含：
- event_id
- event_type
- schema_version
- occurred_at
- observed_at
- asserted_at
- recorded_at
- source_scope
- owner_scope
- perspective_scope
- field_scope
- space_anchor_refs
- target_object_refs
- evidence_refs
- trace_refs
- governance_refs
- temporal_validity
- confidence
- candidate_only
- not_fact
- revision
- supersedes_event_ref
- correlation_id
- causation_event_ref
- replayable
- reversible
- revoked
- revocation_reason
- extension_data

必须明确：
- candidate_only 默认 true。
- not_fact 默认 true。
- extension_data 不能绕过正式协议。
- revoked 事件仍保留历史，但不能继续产生当前有效状态。

## D. Event Admission

事件准入流程包含：
- schema validation
- source admission
- owner scope validation
- evidence admission
- temporal validation
- perspective validation
- target existence validation
- duplicate detection
- contradiction detection
- permission check
- governance check

结果类型：
- admitted_event_candidate
- rejected_event_candidate
- quarantined_event_candidate
- duplicate_event_candidate
- unresolved_event_candidate
- correction_required_candidate

必须明确：事件准入不等于 Fact Admission。

## E. Temporal Validity Types

类型覆盖：
- persistent
- interval
- recurring
- temporary
- seasonal
- event_driven
- until_revoked
- inherited
- unknown_validity

每种类型必须说明：
- activation_rule
- deactivation_rule
- expiry_rule
- refresh_rule
- recurrence_rule
- inheritance_rule
- projection_eligibility
- evidence_requirement
- replay_behavior

## F. Temporal Validity Object

字段至少包含：
- temporal_type
- valid_from
- valid_until
- recurrence_pattern
- recurrence_timezone
- expected_duration
- activation_event_refs
- deactivation_event_refs
- refresh_at
- refresh_policy
- temporal_confidence
- decay_policy
- inherited_from_ref
- until_revoked
- grace_period
- stale_after
- expired_at
- current_temporal_status

current_temporal_status 允许：
- pending
- active
- inactive
- stale
- expired
- suspended
- revoked
- unknown

## G. Recurrence Model

支持：
- daily
- weekly
- monthly
- seasonal
- event_calendar
- custom_window

必须明确：
- 周期规律只是候选。
- 当前视觉或用户证据可以否定周期预期。
- “通常晚上有夜市”不得自动等于“今晚一定有夜市”。
- recurrence 需要 refresh 和反证机制。

## H. Temporary Overlay Protocol

支持：
- temporary event
- construction
- enforcement inspection
- festival
- emergency
- crowd control
- weather disruption
- business closure
- pop-up activity

必须明确：
- 临时覆盖不删除基础定义。
- Overlay 有明确优先级和有效期。
- Overlay 结束后重新计算 Active Projection。
- 不允许直接恢复旧状态，必须重新验证时间和证据。
- Safety Overlay 拥有最高运行优先级。

## I. Revision and Revocation

定义：
- event correction
- event supersession
- evidence retraction
- object revision
- event revocation
- derived state invalidation
- projection refresh

必须明确：
- 历史事件不可物理删除。
- 更正通过新事件表达。
- 撤回影响所有派生状态。
- 派生状态必须保存 lineage。
- Human Correction 必须进入同一事件流。

## J. Replay Protocol

定义：
- full replay
- partial replay
- replay from snapshot
- replay by field scope
- replay by time range
- replay by correlation_id
- replay after correction
- replay after revocation

必须明确：
- replay 必须 deterministic。
- 相同事件序列产生相同 Field State。
- 非确定性 Provider 输出不得在 replay 时重新调用。
- replay 使用已冻结的 Evidence Candidate。
- replay 不得触发生产动作。

## K. Conflict and Coexistence

区分：
- evidence conflict
- temporal conflict
- perspective conflict
- owner conflict
- institutional-social conflict
- personal-public conflict
- duplicate assertion
- incompatible overlay

结果允许：
- coexist
- prioritize_for_projection
- suppress_for_task
- unresolved
- request_more_evidence
- human_review
- revoke_candidate

不得强制压缩成唯一标签。

## L. “小北门”时间线案例

1. 白天：
- road active
- entrance_exit active
- night_market inactive

2. 傍晚：
- recurrence_window_opened
- vendor evidence observed
- night_market candidate activated

3. 城管检查：
- enforcement overlay started
- night_market suspended
- road and entrance remain active

4. 检查结束：
- overlay ended
- 不自动恢复夜市
- request refresh evidence

5. 用户命名：
- personal_name_asserted = 小北门
- valid until revoked
- personal scope only

6. 打车：
- internet ride-hailing 使用 institutional/map naming
- local taxi conversation 可使用 social/personal naming candidate

说明：同一 SpaceAnchor 在不同时间和任务下产生不同 Active Projection。

## M. Governance Reuse

引用：
- Candidate / Fact Admission
- Evidence Chain
- Runtime Boundary
- Permission / Owner Approval
- Human Correction
- Negative Guards
- Trace and Diagnostics
- Change Control
- Post-Review / Freeze
- Rollback / Revocation
- Input / Output Symmetry

## N. Negative Guards

至少包含：
- no direct state mutation
- no silent event drop
- no candidate-to-fact promotion
- no personal-to-public promotion
- no revoked event activation
- no expired definition activation
- no recurrence treated as certainty
- no overlay deleting substrate
- no replay triggering external provider
- no replay triggering action
- no correction without lineage
- no extension_data governance bypass

## O. Stop Conditions

- 不实现 Event Store
- 不实现 Reducer
- 不实现 scheduler
- 不创建数据库
- 不绑定具体时间库
- 不执行真实事件
- 不接 Provider
- 不改现有代码
- 不迁移目录
- 不进入 Perspective Engine
