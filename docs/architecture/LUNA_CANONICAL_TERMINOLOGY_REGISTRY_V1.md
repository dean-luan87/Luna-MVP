# Luna Canonical Terminology Registry v1

## 1. Position and Scope

- Phase: `Phase-A1.6-Cognitive-Canonical-Terminology-Registry-v1-001`
- Execution Mode: Planning Only
- Constitutional reference: `docs/architecture/LUNA_ENGINEERING_ARCHITECTURE_CONSTITUTION_V1.md`
- Status: governance supplement pending human architecture review

This registry defines Luna's official engineering language. Future Modules, Protocols, Schemas, APIs, and Documentation must prefer the Canonical Name in this document. It establishes meaning; it does not rename existing files, alter registries, or change runtime behavior.

## 2. Registry Rules

- A Canonical Name has one meaning within its declared layer and owner boundary.
- A term must not be upgraded in meaning merely because an implementation changes, a model repeats it, or a storage system indexes it.
- Historical aliases may be read only through an explicit compatibility mapping; they must not create a parallel canonical vocabulary.
- `Candidate` is a lifecycle/authority qualifier, not a replacement for a domain object. For example, `Entity Candidate` is still an Entity-domain object with candidate status.
- Any change to a Canonical Name, definition, owner, allowed usage, or forbidden usage requires Constitution Change Control.

## 3. Canonical Terminology

| Canonical Name | 中文名称 | Definition | Belongs To Layer | Owner Module | Allowed Usage | Forbidden Usage | Historical Alias |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Observation | 观察事件 | 外部输入经过感知系统后形成的原始观察记录；保留来源、时间、trace 与不确定性。 | L1 Cognitive Flow / Perception Admission | Observation Event Protocol | 表示感知输入、事件候选、模拟观察。 | Fact、Truth、Conclusion、Decision。 | raw observation, sensor result, model output (only as source-specific descriptions) |
| Evidence | 证据 | 支撑认知过程的信息来源及其 provenance、source chain 与质量上下文。 | L1 Cognitive Flow with L2 Evidence governance | Evidence Reference Protocol / Evidence Chain | 关联 Observation、Hypothesis、Admission、Experience 的来源依据。 | Knowledge、Fact、Truth、自动结论。 | source material, proof (when not admission-authorized) |
| Fact | 事实 | 经过显式、拥有者明确的准入流程后，可进入指定世界状态用途的数据。 | L1 Field Kernel lifecycle | Authorized Fact Admission boundary (future explicit protocol) | 仅在准入 owner、生命周期和用途均已声明时使用。 | raw Observation、model output、Evidence、Hypothesis、majority opinion。 | truth, confirmed data (unless admission contract says so) |
| Entity | 实体候选 | 认知系统中的对象候选，如人、建筑、道路、入口；其身份和属性可保持不确定。 | L1 Field Kernel | Field Identity / Entity Protocol (future) | 记录对象候选、属性候选、证据和观察引用。 | 最终实体、未经准入的世界事实、模型标签即实体。 | object, detected object, target |
| Relation | 关系候选 | 实体之间的关联描述候选，如 belongs_to、near、contains、connected_to。 | L1 Field Kernel | Field Relation Protocol (future) | 表示有来源、范围、时间的候选关系。 | 自动因果事实、永久关系、未审查图边即真相。 | link, edge, association |
| Field | 场 | 由物理、社会、任务、关系共同构成的认知环境。 | L1 Field Kernel | Field Identity Protocol | 描述当前认知环境、边界、层级和上下文。 | 简单地图标签、单一模型分类、数据库集合。 | scene, place, environment, world model |
| Field State | 场状态 | Field 在特定时间窗口内的有效描述，由 admitted events 经 Reducer 组织并保留来源。 | L1 Field Kernel | Field State Reducer | 表示当前候选世界状态、时间有效性、read projection。 | Observation、Evidence、模型输出、任意记忆集合。 | world state, scene state, state cache |
| Hypothesis | 假设 | 基于当前信息、假设条件和替代解释形成的可能解释。 | L1 Cognitive Analysis | Hypothesis Protocol (future) | 表示可检验解释、预测、比较路径和不确定性。 | Decision、Conclusion、Fact、Action。 | inference result, answer, judgment |
| Information Gap | 信息缺口 | 影响理解或决策的不确定信息、缺失条件或待验证问题。 | L1 Cognitive Analysis | Information Gap Protocol (future) | 请求更多信息、标记不确定、形成探索候选。 | 自动工具调用许可、错误、空数据的同义词。 | missing data, unknown, uncertainty (without material relevance) |
| Decision Candidate | 决策候选 | 经过分析形成、仍待所属决策/授权边界处理的可选路径。 | L1 Cognitive Analysis → L2 Task governance boundary | Cognitive Delivery Protocol / Task Manager boundary | 表达建议、解释、澄清或待授权路径。 | Action、final decision、task execution、model command。 | recommendation, action plan, answer (unless explicitly candidate) |
| Experience | 经验 | 经历、行动、结果、上下文、证据与 review 形成的结构化沉淀。 | L1 Experience System | Experience Record Protocol (future) | 记录 Experience Episode、复盘和复用候选来源。 | Value、Truth、Fact、简单知识库条目。 | memory, case, knowledge, lesson |
| Experience Kernel | 经验核心 | 具有适用条件、来源、反例和 review 的可复用经验结构。 | L1 Experience System | Experience Kernel Protocol (future) | 支持受约束的经验检索、比较和复用候选。 | policy override、事实、模型权重、价值判断。 | pattern, rule of thumb, case template |
| Hive Experience Field | 蜂巢经验场 | 多个 Luna 经验形成的共享观察空间，用于关联、分支、冲突与历史演化。 | L5 Hive Experience Field | Experience Branch Protocol / sharing-governance boundary (future) | 表示跨 Luna 的经验关联、分歧和 game-analysis candidates。 | Central Brain、Voting System、统一意识、价值裁判、个人决策控制器。 | collective memory, shared brain, consensus engine |

## 4. Canonical Relationship Paths

### 4.1 World Understanding Path

```text
Observation
  -> Evidence
  -> Candidate
  -> Fact Admission
  -> Field State
```

The path requires explicit lifecycle owners. `Fact Admission` is a transition boundary, not a synonym for Observation or Evidence.

### 4.2 Cognitive and Experience Path

```text
Observation
  -> Hypothesis
  -> Decision Candidate
  -> Outcome
  -> Experience
```

The second path may use Evidence and Field State as inputs, but no arrow turns a Hypothesis into a Decision or Experience into Value.

## 5. Terminology Boundary Notes

- `Observation Event` is a protocol/object expression of canonical `Observation`; it is not a separate cognitive category.
- `Evidence Reference` is a protocol/object expression of canonical `Evidence`.
- `Entity Candidate`, `Relation Candidate`, `Field Reference Candidate`, and `State Candidate` are explicitly candidate-only primitives. They do not alter the canonical definitions of Entity, Relation, Field, or Field State.
- `Field State` is reserved for the Reducer-owned temporal representation. `State Candidate` must not be abbreviated to `Field State`.
- `Decision Candidate` is the only approved term for an analysis output that may later reach an authorization boundary. `Action` is reserved for an execution-side concept.
- `Hive Experience Field` is the only approved name for the L5 association domain. Terms implying central cognition, consensus, or unified value are prohibited.

## 6. Change Control

This registry is governed by Constitution Change Control. A proposed terminology change must specify:

1. affected Canonical Name and exact proposed replacement or clarification;
2. layer and owner impact;
3. protocol/schema/API/document compatibility impact;
4. historical-alias and migration mapping;
5. lifecycle and authority impact;
6. review authority and rollback plan.

No module implementation may silently redefine a term, introduce a competing synonym, or use an alias to claim broader authority.

## 7. Current Phase Boundary

This phase creates this registry document only. It creates no code, schema, runtime, runner, verifier, registry entry, migration, or file rename. The next planned phase is existing-asset alignment planning; implementation work remains outside the current phase.

