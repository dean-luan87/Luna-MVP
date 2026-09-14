# Luna Field Kernel Technical Architecture v1

## A. Kernel Purpose

Field Kernel 负责：
- 接收 FieldEvent
- 维护 Field State
- 管理 Field Timeline
- 保留多种现实定义
- 处理时间有效性
- 处理冲突和共存
- 处理临时覆盖
- 支持撤回和修正
- 生成 Active Field Projection
- 为 Expectation、Attention、Interaction 提供输入

Field Kernel 不得负责：
- 直接调用模型
- 直接生成公共事实
- 直接修改人格
- 直接执行动作
- 直接生成情绪
- 覆盖 Safety Constitution

## B. Core Components

### Field Event Intake
- purpose: 接收和统一 FieldEvent，作为 Field Kernel 的唯一入口。
- inputs: 原始事件载荷、来源标识、接收时间。
- outputs: 标准化 FieldEvent、初始事件元数据。
- state ownership: 无状态；负责事件入口忠实转发。
- allowed mutations: 标准化事件字段、补齐缺失元数据。
- prohibited mutations: 不得修改事件本身语义，不得直接更新 FieldState。
- failure mode: 无效事件格式、缺失必要 Anchor、非法来源。
- rollback point: 事件被拒绝前。
- governance refs: Runtime Boundary、Evidence Chain、Trace and Diagnostics。
- verifier requirements: 验证事件类型、时间戳、来源字段、FieldEvent 标识完整性。

### Event Validator
- purpose: 验证 FieldEvent 是否满足 Field Kernel 接受规则。
- inputs: 标准化 FieldEvent、当前时间、安全约束。
- outputs: 验证结果、拒绝原因、validation trace。
- state ownership: 无状态；只读当前时间和安全约束。
- allowed mutations: 标记事件为 valid / invalid、附加拒绝原因。
- prohibited mutations: 不得直接修改事件内容、不得修改 FieldState。
- failure mode: 违反时间有效性、缺失 SpaceAnchor、与安全约束冲突。
- rollback point: 验证失败事件拒绝前。
- governance refs: Permission / Owner Approval、Negative Guards、Human Correction。
- verifier requirements: 验证 validation_steps、invalid event 检测、event_before_mutation 规则。

### Evidence Normalizer
- purpose: 将多源证据转为统一的 Field Kernel 证据语义包。
- inputs: FieldEvent 证据片段、attachment reference、观察时间。
- outputs: normalized evidence items、evidence provenance。
- state ownership: 无持久状态；维护证据标准化规则集。
- allowed mutations: 规范字段名称、添加统一证据类别标签。
- prohibited mutations: 不得变更原始证据事实，不得导出为事实条目。
- failure mode: 证据格式不一致、缺失必要证据字段。
- rollback point: 证据标准化失败前。
- governance refs: Evidence Chain、Veriﬁer、Human Correction。
- verifier requirements: 证据规范化规则、missing evidence 检测、evidence chain 引用完整性。

### Space and Time Anchor Resolver
- purpose: 解析事件中的 SpaceAnchor 与时间锚点，生成稳定定位。
- inputs: FieldEvent、current time、时间范围、位置参考。
- outputs: resolved anchors、temporal anchors、anchor certainty。
- state ownership: 无持久状态；拥有解析规则与 anchor 映射。
- allowed mutations: 补齐 anchor 维度，矫正时间格式。
- prohibited mutations: 不得创建全新实际定义；不得直接修改 FieldState。
- failure mode: anchor 缺失、解析冲突、时间无法解释。
- rollback point: anchor 解析失败前。
- governance refs: Map Anchor Conflict and Freshness Policy、Negative Guards。
- verifier requirements: anchor_resolution_steps、missing SpaceAnchor 检测、recurrence and temporal consistency。

### Field Candidate Builder
- purpose: 基于事件、证据与锚点构建候选场定义。
- inputs: resolved anchors、normalized evidence、current FieldState、candidate templates。
- outputs: candidate_definition、candidate_metadata、confidence components。
- state ownership: candidate_definition_state 的临时候选池。
- allowed mutations: 聚合证据、计算置信度组成、标记 unresolved 条目。
- prohibited mutations: 不得直接改写 substrate_state 或 active_projection_state。
- failure mode: 候选缺乏必要定义、证据矛盾导致 unresolved。
- rollback point: 候选构建失败前。
- governance refs: Candidate / Fact Admission、Model / Skill Admission、Human Correction。
- verifier requirements: candidate build steps 完整、unresolved_candidate 产生规则。

### Field State Reducer
- purpose: 将候选定义与当前 FieldState 归约为新 FieldState 视图。
- inputs: admitted candidates、current FieldState、temporal anchors、governance guards。
- outputs: substrate_state update proposal、admitted_candidate_state、suspended_state、expired_state。
- state ownership: substrate_state、admitted_candidate_state、suspended_state、expired_state。
- allowed mutations: 更新候选状态、标记过期/挂起、生成撤回指令。
- prohibited mutations: 不得直接生成 ActiveFieldProjection、不得跳过 event_before_mutation。
- failure mode: partial state update、conflicting evidence 无法归约。
- rollback point: state mutation proposal前。
- governance refs: Change Control、Rollback / Revocation、Post-Review / Freeze。
- verifier requirements: reducer determinism test、partial failure rollback test、event_before_mutation。

### Temporal Field Graph
- purpose: 维护时间关系和有效性网络，支撑多时序场定义。
- inputs: temporal definitions、valid_from/valid_until、recurrence、refresh_policy。
- outputs: active temporal definitions、expired markers、refresh recommendations。
- state ownership: expired_state、temporal validity metadata、projection eligibility标签。
- allowed mutations: 标记 definition expiry、更新时间窗口、标记 refresh 请求。
- prohibited mutations: 不得直接改变 definition semantics、不应修改 active_projection_state。
- failure mode: stale temporal definition、recurrence 解析失败、refresh policy 失效。
- rollback point: temporal graph update前。
- governance refs: Runtime Boundary、Change Control、Temporal Validity Policy。
- verifier requirements: temporal type completeness、expiry rules、refresh rules。

### Field Belief Manager
- purpose: 管理场定义置信度与信念状态，支持 evidence update 与 user confirmation。
- inputs: prior confidence、supporting evidence、contradicting evidence、user confirmation weight。
- outputs: confidence_new、belief state、unresolved indicators。
- state ownership: belief confidence、unresolved_state、personal relevance标记。
- allowed mutations: 调整 confidence、标记 unresolved、维护 belief update trace。
- prohibited mutations: 不得将置信度当作事实准入、不得将情感强度作为 evidence strength。
- failure mode: contradictory evidence 无法合并、confidence overflow、unknown 被错误归类。
- rollback point: belief adjustment proposal前。
- governance refs: Evidence Chain、Human Correction、Permission / Owner Approval。
- verifier requirements: belief update model 定义、confidence 不是事实准入、personal relevance 与 public truth 区分。

### Conflict and Coexistence Resolver
- purpose: 处理并存定义、冲突定义和权重选择。
- inputs: admitted_candidate_state、active_field_state、multi-reality definitions、perspective weights。
- outputs: coexistence set、conflict reports、suppressed definition refs。
- state ownership: coexisting relations、conflict matrix、unresolved_state。
- allowed mutations: 标记 conflicts_with、coexists_with、suppressed definitions。
- prohibited mutations: 不得自动覆盖底层定义、不允许以单一标签覆盖所有定义。
- failure mode: 无法解决冲突、conflict spillover、incorrect coexistence标记。
- rollback point: conflict resolution proposal前。
- governance refs: Coexistence Policy、Human Correction、Negative Guards。
- verifier requirements: multi-reality coexistence test、conflict and coexistence resolver 规则。

### Temporary Overlay Manager
- purpose: 管理临时场、临时覆盖和 overlay 生命周期。
- inputs: temporary definitions、expected_duration、observed_at、asserted_at、expired_at。
- outputs: temporary_overlay_state、expiration events、overlay resolution建议。
- state ownership: temporary field state、overlay expiration markers、suspended_state。
- allowed mutations: 启动临时覆盖、结束 overlay、生成 expiration event。
- prohibited mutations: 不得永久写入 substrate、不得让 overlay 改写 substrate definition。
- failure mode: temporary overlay 未按时结束、overlay 与长期定义冲突。
- rollback point: overlay state write前。
- governance refs: Runtime Boundary、Temporary Overlay Policy、Rollback / Revocation。
- verifier requirements: temporary overlay test、expiration event 规则。

### Field Lifecycle Manager
- purpose: 管理场定义的生命周期、修订、撤回和 superseded 状态。
- inputs: revision proposals、revocation requests、expiration events、approval signals。
- outputs: superseded_state、revoked_state、revision records。
- state ownership: superseded_state、revoked_state、revision history。
- allowed mutations: 标记 revision、supersede definition、触发 revocation event。
- prohibited mutations: 不得直接删除 substrate 记录、不得绕过 revocation event。
- failure mode: revocation failure、revision loop、history 不一致。
- rollback point: lifecycle mutation前。
- governance refs: Change Control、Post-Review / Freeze、Revocation。
- verifier requirements: revocation rules、revocation failure coverage。

### Active Field Projection Builder
- purpose: 根据当前 FieldState 生成候选 ActiveFieldProjection。
- inputs: current field state、definition weights、selected perspective、suppressed definitions。
- outputs: ActiveFieldProjection、projection eligibility、attention priors、expectation seeds。
- state ownership: active_projection_state、projection metadata。
- allowed mutations: 生成 projection candidates、标记 projection eligibility。
- prohibited mutations: 不得修改 substrate_state、不得将 projection 写回底层定义。
- failure mode: projection failure、误将候选转为事实。
- rollback point: projection生成前。
- governance refs: Projection Boundary、Candidate / Fact Admission、Trace and Diagnostics。
- verifier requirements: projection contract 完整性、projection_mutates_substrate false。

### Field Timeline Store Interface
- purpose: 定义 Field Timeline 的存储与追加接口。
- inputs: timeline append requests、event ids、snapshot refs。
- outputs: timeline append confirmations、timeline snapshots。
- state ownership: interface contract，仅定义不实现。
- allowed mutations: interface metadata调整。
- prohibited mutations: 不得依赖具体数据库，不得实施具体后端。
- failure mode: timeline append 失败、snapshot corruption。
- rollback point: timeline store request前。
- governance refs: Persistence Abstraction、Trace and Diagnostics。
- verifier requirements: persistence interface 完整、backend_agnostic。

### Revision and Revocation Manager
- purpose: 负责撤回事件、修正记录和历史状态控制。
- inputs: revocation event、correction event、approval metadata。
- outputs: revocation status、rollback targets、replay directives。
- state ownership: revoked_state、revision history。
- allowed mutations: 标记 revoked、生成 replay requirements。
- prohibited mutations: 不得强制删除历史事件、不得绕过 event-sourced replay。
- failure mode: revocation failure、human correction conflict。
- rollback point: revocation apply前。
- governance refs: Human Correction、Change Control、Rollback / Revocation。
- verifier requirements: revocation rules、human correction conflict coverage。

### Trace and Diagnostics
- purpose: 提供可追踪的事件流、状态变化记录和故障诊断。
- inputs: event trace、state transition日志、projection trace。
- outputs: trace records、failure reports、replay线索。
- state ownership: trace store metadata、diagnostics索引。
- allowed mutations: 记录 trace、生成 diagnostic event。
- prohibited mutations: 不得更改 FieldState 或 projection semantics。
- failure mode: trace丢失、diagnostics 不一致。
- rollback point: trace commit前。
- governance refs: Trace and Diagnostics、Model Test Lens、Post-Review / Freeze。
- verifier requirements: trace steps 完整、mermaid 图 trace 表达。

### Human Correction Adapter
- purpose: 接受人工更正并将其建模为事件。
- inputs: correction input、user身份、current FieldState、affected definitions。
- outputs: correction FieldEvent、validation result、replay需求。
- state ownership: 无持久状态；负责 human correction event 生成。
- allowed mutations: 规范 correction 事件、包装 provenance。
- prohibited mutations: 不得直接修改 FieldState、不允许 bypass event-sourced path。
- failure mode: human correction conflict、invalid correction request。
- rollback point: correction event 生成前。
- governance refs: Human Correction、Permission / Owner Approval。
- verifier requirements: human correction test、correction event 形成规则。

### Governance Gate
- purpose: 在 FieldState 更新与投影前应用治理检查。
- inputs: candidate proposals、projection candidates、policy exceptions。
- outputs: governance approval、block/reject signal、audit tags。
- state ownership: governance gate metadata。
- allowed mutations: 标记 governance result。
- prohibited mutations: 不得直接更改 candidate semantics或 FieldState。
- failure mode: governance gate reject、missing approval。
- rollback point: governance gate fail前。
- governance refs: Permission / Owner Approval、Negative Guards、Post-Review / Freeze。
- verifier requirements: governance reuse定义、required_governance 完整。

## C. Event-Sourced Architecture

- FieldEvent → Validation → Evidence and Anchor Resolution → Candidate Construction → State Reducer → Field State Snapshot → Timeline Append → Active Projection
- event_before_state_mutation = true
- 当前状态可由事件回放重建；FieldState 的所有修改必须来源于 event replay。
- 不允许无事件直接修改 FieldState。
- Human Correction 也必须形成 event。
- 撤回必须形成 revocation event。
- 临时场结束必须形成 expiration event。

## D. Kernel State Model

### State Layers
- substrate_state: 底层定义和长期事实。
- candidate_definition_state: 新建候选和待审定义。
- admitted_candidate_state: 被接纳并进入归约的候选。
- active_field_state: 当前 projection 依据的活跃定义集合。
- suspended_state: 暂停的候选或定义。
- expired_state: 失效定义与历史记录。
- superseded_state: 已被新定义替代或修订的记录。
- revoked_state: 被撤回的定义与事件。
- unresolved_state: 冲突或证据不足的未定项。
- active_projection_state: 当前生成的 ActiveFieldProjection。

### 区分
- substrate: 底层真实定义与可重放历史。
- candidate: 候选状态与审查过程。
- active projection: 仅用于当前視角展示，不可写回 substrate。

Active Projection 不得重写 substrate。

## E. Multi-Reality Handling

支持：
- physical reality
- institutional reality
- social reality
- personal reality

定义：
- 同一 SpaceAnchor 可拥有多条并存定义。
- 不按单一标签覆盖。
- personal definition 隔离，不直接影响 public definition。
- institutional 与 social 冲突可同时保留。
- Perspective 只改变使用权重，不改变底层定义。
- 时间有效性决定当前是否活跃。

## F. Field Hierarchy and Relations

支持：
- macro field
- functional field
- micro field
- interaction unit
- temporary field

关系：
- contains
- belongs_to
- adjacent_to
- overlaps
- inherits_rules_from
- temporarily_overrides
- transitions_to
- coexists_with
- conflicts_with

规则：
- Parent Field 与 Child Field 的规则继承必须明确，子场继承父场约束但不自动修改父场。
- 局部覆盖不能自动修改父场。
- 大场和小场可以同时活跃。
- 最小场由认知规则变化决定，不由固定面积决定。

## G. Belief Update Model

解释模型：
- confidence_new = prior + supporting_evidence - contradicting_evidence - temporal_decay + user_confirmation_weight + repeated_observation_weight

说明：
- confidence 不是事实准入。
- emotional intensity 不等于 evidence strength。
- personal relevance 不等于 public truth。
- 证据冲突时允许 unresolved。
- 未知应保持未知。

## H. Temporal Model

支持：
- valid_from
- valid_until
- recurrence
- expected_duration
- observed_at
- asserted_at
- expired_at
- refresh_policy
- temporal_decay
- temporary_overlay

定义示例：
- 周期性夜市
- 临时活动
- 装修状态
- 临时停摆
- 场定义变更
- 历史 Field 保留
- 当前 Active Field 切换

## I. Perspective Projection Interface

Kernel 输入：
- current field state
- task
- user goal
- current time
- emotion candidate
- personality preference
- safety constraints

Kernel 输出给 Perspective Engine：
- available field definitions
- active temporal definitions
- unresolved conflicts
- field relations
- evidence summaries
- personal definitions
- social definitions
- institutional definitions
- projection eligibility

Perspective Engine 返回：
- selected perspective
- definition weights
- suppressed definitions
- attention priors
- interaction naming preference

最终输出：
- ActiveFieldProjection

## J. Fast Loop and Slow Loop

Fast Loop:
- Observation → Event Intake → Reducer → Projection → Expectation / Attention

Slow Loop:
- Timeline → Pattern Consolidation → Field Growth Profile → Meaning / Memory Candidate → Perspective Preference Candidate

说明：
- Slow Loop 不得直接修改生产人格。
- Growth 输出必须是 candidate。
- Fast Loop 必须满足实时安全需求。
- 两个循环共享事件和 trace，但拥有不同时间尺度。

## K. Persistence Abstraction

接口定义：
- EventStoreInterface
- FieldSnapshotStoreInterface
- TemporalGraphInterface
- AttachmentStoreInterface
- TraceStoreInterface

说明：
- 当前禁止选择 Neo4j、PostgreSQL、MongoDB 或其他具体产品。
- Kernel 不依赖具体数据库。
- 第一版允许内存 fixture 实现。
- 后续可替换存储后端。

## L. Failure and Recovery

覆盖：
- invalid event
- missing evidence
- conflicting evidence
- stale temporal definition
- missing SpaceAnchor
- projection failure
- partial state update
- corrupted snapshot
- revocation failure
- human correction conflict

定义：
- abort
- rollback
- replay
- quarantine
- request_more_evidence
- unresolved_candidate

## M. Governance Reuse

复用：
- Candidate / Fact Admission
- Evidence Chain
- Runtime Boundary
- Model / Skill Admission
- Permission / Owner Approval
- Negative Guards
- Verifier
- Model Test Lens
- Human Correction
- Trace and Diagnostics
- Change Control
- Post-Review / Freeze
- Rollback / Revocation

## N. Test Strategy

测试：
- reducer determinism test
- event replay test
- temporal expiry test
- multi-reality coexistence test
- temporary overlay test
- perspective projection boundary test
- candidate-to-fact leak test
- revocation test
- human correction test
- partial failure rollback test
- unresolved state test

## O. Minimum Case: 小北门

SpaceAnchor:
- road
- gate
- entrance_exit

Institutional:
- road regulation
- occupancy restriction

Social:
- evening temporary night market

Personal:
- name: 小北门
- home entrance

Temporal:
- daytime
- evening
- enforcement inspection
- temporary suspension

Tasks:
- find food
- go home
- internet ride-hailing
- communicate with local taxi driver

说明：Field Kernel 维护定义但不执行完整 DryRun；它保留 physical/institutional/social/personal 定义，标记 temporal 状态并生成 ActiveFieldProjection 候选。

## P. Stop Conditions

- 不实现 Runtime
- 不写 Reducer 代码
- 不创建数据库
- 不选数据库产品
- 不接模型
- 不读图
- 不训练神经网络
- 不修改现有工程
- 不迁移目录
- 不实现情感或人格成长
