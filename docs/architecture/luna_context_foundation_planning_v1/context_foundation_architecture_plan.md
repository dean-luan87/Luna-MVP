# Luna Context Foundation Architecture Plan v1

Status: `PLANNING_CANDIDATE`

Phase: `Phase-Luna-Context-Foundation-v1-001`

Execution Mode: `Planning Only`

## 1. Context 的定位

Context 是多个独立 Owner 输出的只读 Projection 的组合，用于描述 Luna 当前所处的认知环境。

Context 回答：

> 现在是什么状态？

Context 不回答：

- 用户想做什么；
- 为什么会发生；
- 哪个目标更重要；
- 应该如何决策；
- 应该执行什么动作。

Context 是背景，不是结论。它不是新的数据 Owner，也不是数据库、Memory、PCN、Intent Engine、Causal Engine、Decision 或 Runtime。

Context Foundation 的唯一候选写范围是 `Context Envelope Candidate`。所有源对象继续由原 Owner 管理；读取、引用、组装和投影不产生所有权转移。

## 2. 输入结构

### 2.1 Field Context

来源：`Field State System`

提供：

- Current Field；
- World State Reference；
- Temporal Validity；
- current-Reality provenance；
- uncertainty and unknown references。

Field State Reducer 保留 Field 写权限。Context 不能修改 Field、Reality 或 Field 生命周期。

### 2.2 Observation Context

来源：`Observation Manager`

提供：

- Evidence Reference；
- Observation Candidate；
- Uncertainty；
- quality, provenance, and trace references。

Observation 是 Evidence，不是 Fact。Context 不能把 Observation Candidate 提升为 Fact、Intent、Causal Explanation 或 Decision。

### 2.3 Memory Context

来源：`Memory System`

提供：

- Historical Reference；
- Experience Reference；
- Compressed Memory Reference；
- relevance, confidence, unknown, and provenance references。

Context 只能消费 Memory Projection，不能直读 Raw Memory、Memory Store 或数据库，不能写入、合并、压缩、删除或重分类 Memory。Current Reality 始终优先于历史影响。

### 2.4 Self Context

来源：`Self System`

提供：

- Current Identity Reference；
- current capability, boundary, resource, and regulation references。

Self Context 不修改 Identity、Capability Reality、Constitution 或 Self State。

### 2.5 Role Context

来源：`Role System / Social Self`

提供：

- Current Role Reference；
- responsibility and role-boundary references；
- Field binding and temporal validity。

Current Role 在完整 Context 中可见，但仍由 Role/Social Self 拥有，不重新归入 Self System。

### 2.6 Relationship Context

来源：`Relationship System / Social Self`

提供：

- Relation Reference；
- Relation Importance Candidate；
- participant, history, state, boundary, confidence, and temporal references。

Context 不计算关系、不改变关系状态，也不把关系重要性候选当作 Value 或 Decision。

### 2.7 Emotion Context

来源：`Emotion Context Boundary / Integration Layer`

提供：

- Current Emotional State Reference or Emotion Context Candidate；
- Emotional Influence Candidate；
- evidence, confidence, temporal scope, provenance, unknown, and revocation references。

当前 Emotion 仍是轻量 Context Candidate。Context Foundation 不计算、推断、生成或表达 Emotion。Emotion 不能直接生成 Intent、Value、Decision 或 Action。

## 3. Temporal Context

Temporal Context 不是新的历史数据库。它在 Context Envelope 中组合：

- 当前事件窗口；
- 当前 Field 的 temporal validity；
- 最近保留的认知上下文；
- Memory System 提供的长期历史引用；
- expiry, suspension, reactivation, and reset conditions。

物理 Field 变化不会自动清空精神状态、Emotion Context 或短期保留内容。每个 carryover 必须保留来源、有效期、置信度和撤销条件。

## 4. Context Projection 结构

```text
Field Projection
Observation Projection
Memory Projection
Self Projection
Role Projection
Relationship Projection
Emotion Projection
        ↓
Context Foundation Assembly
        ↓
Current Context Candidate
```

Context Assembly 只组合引用，不复制源对象，不创建第二 Writer，也不拥有源对象生命周期。

必须保留：

- Unknown；
- Uncertain；
- Multiple Candidate；
- provenance；
- trace reference；
- temporal scope；
- source Owner and write authority。

## 5. 输出边界

允许输出：

- Current Context Candidate；
- Context Reference；
- Context Confidence；
- Temporal Scope；
- Unknown and competing-candidate references；
- Provenance and Trace Reference。

未来允许消费者：

- Personal Cognitive Network；
- Intent Governance；
- Causal Reasoning Governance。

Context 输出永远不能包含或宣称：

- Intent；
- Goal；
- Causal Explanation；
- Fact Generation；
- Decision；
- Action；
- Memory Mutation；
- Field Mutation。

## 6. 生命周期

Context 生命周期候选为：

```text
Create -> Activate -> Update -> Suspend -> Expire -> Archive
```

Update 只能由新的源 Projection、有效期变化或撤销事件触发。Suspend 不等于删除；Expire 不等于 Memory；Archive 只保存 Context Envelope 的审计引用，不取得源对象的归档或持久化权限。

## 7. 复杂度策略

Context 深度按问题需要展开：

- 天气、时间、简单查询：Low Context；
- 多约束任务与普通规划：Medium Context；
- 关系、情绪、长期规划、人生选择：High Context。

High Context 表示需要更多源 Projection 和更严格的时间/置信度校验，不表示 Context 获得推理、Intent 或 Decision 权限。

## 8. 与后续模块的边界

### PCN

PCN 消费 Context Reference，形成 Connection、Activation 和 Context Projection Candidate。Context Foundation 不预先执行网络连接或激活。

### Intent

Intent Governance 消费 Context 与未来 PCN Projection，形成 Intent Candidate。Context Foundation 不生成 Intent。

### Causal

Causal Reasoning 消费 Context、Intent、Evidence 与其他受治理引用，形成可修正的 Causal Candidate。Context Foundation 不解释“为什么”。

### Decision

Decision Arbitration 消费上游候选和约束。Context Foundation 不排序方案、不选择行动，也不向 Runtime 发送请求。

## 9. 场景验收原则

第一版只需证明：Luna 可以把现实、身份、角色、关系、记忆、情绪与观察引用组合为稳定且可追踪的当前 Context Candidate，同时保持 Unknown、多个候选和所有 Owner 边界。

在“用户下班回家但工作压力残留”的场景中，Context 可以表达：

- Physical Field: Home；
- Active Mental Context: Work Residual State；
- Role Reference: Employee；
- Emotion Context Reference: Residual Stress；
- Related Memory Reference: Recent Project Pressure。

`Need decompression / discussion` 属于未来 Intent Candidate，不是本阶段 Context 输出。

## 10. 当前阶段禁止

本阶段不实现 Context Skeleton、Context Runtime、PCN、Intent、Causal、Decision、Emotion Engine、Memory 重构、数据库访问、模型调用、Provider、Action 或 Runtime 集成。
