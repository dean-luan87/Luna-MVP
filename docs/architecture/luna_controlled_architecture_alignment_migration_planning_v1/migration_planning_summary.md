# Luna Controlled Architecture Alignment Migration Planning Summary v1

## 1. 当前架构状态

Luna Dynamic Cognitive Architecture v2 已经形成候选架构与迁移治理门禁，但工程实现成熟度并不相同：

- Field State Reducer、Field State Read Model、Observation Manager、Task Manager、
  Model Manager、Protocol Manager、OCR Manager、Vision Manager 已有 active module
  baseline；
- Memory 已有完整认知架构和位于 `docs/runtime/` 的受控骨架资产，但本阶段不把该骨架视为生产 Runtime；
- Self、Role、Relationship、Emotion、Value、Intent、Decision、Action 与 A/B Route
  主要处于架构或边界合同状态；
- Causal Reasoning 与 Experience Compression 主要是 planning-only 资产；
- Personal Cognitive Network 只有架构边界，没有 canonical 工程实现；
- 根目录 `runtime/` 是既有 A3 Runtime 表面，不能因为包含 `intent` 或 `decision`
  字段就推断为 Dynamic Cognitive Architecture v2 Runtime；
- `tools/` 中的 runner/verifier 是工程验证证据，不是 Runtime 或架构 Owner。

本次扫描采用 baseline-first targeted read-only 模式，并明确排除
`_tmp_eval_out` 与 `_eval_out`。没有重新执行全仓盘点，也没有使用历史评估
输出作为 Runtime 输入。

## 2. 新架构目标状态

目标不是建立第二套认知系统，而是让现有资产在同一架构中拥有唯一位置：

```text
Observation / Evidence
  ↓
Field System
  ↓
Personal Cognitive Network Projection
  ↓
Intent
  ↓
Causal Reasoning
  ↓
A/B Route Boundary
  ↓
Decision Arbitration
  ↓
Task Orchestration
  ↓
Action Boundary / Runtime
  ↓
Feedback / Experience
```

该顺序在本阶段表示迁移依赖，不取代既有 Runtime 数据流。Self、Role、
Relationship、Memory、Emotion 与 Value 始终由各自 Owner 管理，Personal
Cognitive Network 只提供跨对象连接、激活和上下文投影。

## 3. 已确认保持模块

以下资产保持正式 mainline、路径与核心职责：

- Observation Manager：候选观察与 Evidence 协调；
- Task Manager：任务生命周期、依赖和能力路由，不执行 Action；
- Model Manager：模型资产、准入和路由候选，不产生认知结论；
- OCR Manager 与 Vision Manager：Evidence 提供者，不直接形成事实；
- Action Boundary：Decision 与执行之间的唯一治理边界；
- Self Governance：身份、能力、资源和边界 Owner；
- Memory System：持久化、巩固、激活和检索 Owner；
- 根目录 A3 Runtime：保持现状并明确排除在本阶段迁移之外；
- 现有 evaluation tools：只作为未来回归证据入口。

## 4. 需要调整模块

调整均为规划候选，不在本阶段执行：

- Field State Reducer：补充 Field Context projection contract，禁止新 reducer；
- Field State Read Model 与 Protocol Manager：只对齐 Owner 元数据；
- Cognitive Attention：文档上与感知注意协调明确分离；
- Role、Relationship、Memory、Intent、Value、Decision、A/B Route：补充跨层候选合同；
- Emotion：明确为 Integration signal，不拥有 Value、Intent、Decision 或 Self；
- Experience Compression：对齐 Memory admission 与 network-evolution candidate；
- Causal Reasoning：未来只复用现有 candidate 资产，不创建平行 Causal Engine；
- Personal Cognitive Network：未来首先定义 projection-only 技术合同，不创建源对象存储。

## 5. 不允许发生的迁移行为

- 不修改任何现有代码或 Runtime；
- 不移动、重命名或删除现有文件；
- 不修改 active baseline 来适配新架构；
- 不创建第二个 Field Reducer、Intent Engine、Causal Engine、Memory Store、
  Task Manager、Model Manager 或认知 Runtime；
- 不把 Personal Cognitive Network 变成 Self、Role、Relationship、Memory、
  Emotion 或 Value Owner；
- 不允许 Task Manager 进行因果判断、最终决策或 Action 执行；
- 不允许 Model/OCR/Vision 输出绕过 Evidence Admission 成为事实；
- 不允许 Memory 直接修改 Cognitive Core；
- 不允许 B Route 覆盖 A Route 当前现实；
- 不跳过 M4 Migration Integrity Validation 或 M5 Architecture Freeze；
- 不削弱检查、不硬编码通过、不把 `_tmp_eval_out`/`_eval_out` 当成 baseline。

## 6. 下一阶段建议

本规划经用户终端 V2 和 ChatGPT V3 审核后，下一步只能进入一个单独授权的
**Controlled Architecture Alignment Migration — M0 Documentation Alignment**
阶段。M0 只处理文档与 canonical terminology，对代码、Runtime、schema、
目录和 baseline 保持零修改。

只有 M0 验证完成后，才可按顺序准备 M1 Contract Alignment。不得直接进入
批量迁移、PCN Skeleton、Intent Engine 或 Causal Runtime。

## Current boundary

```text
Planning only
Migration executed: false
Runtime modified: false
Existing assets modified: false
Directory structure changed: false
Next phase automatic: false
```

