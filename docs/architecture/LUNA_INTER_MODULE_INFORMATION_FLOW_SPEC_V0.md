# Luna — Inter-Module Information Flow & Processing Spec v0（模块间信息流与处理规范：占位）

Protocol/Spec Name: LUNA_INTER_MODULE_INFORMATION_FLOW_SPEC_V0  
Version: v0  
Status: Draft (Placeholder)  
Owner: System / Mid-Platform Governance (placeholder)  
Last Updated: 2026-04-15  
Change Summary: 初版占位：冻结信息对象分层、跨模块传输原则、升格纪律与追踪要求；不替代现有协议、不做强校验。  
Where Used: docs-level system governance; future cross-module protocol governance (placeholder)  

---

## A. 文档定位（写死）

- 这是 Luna 的**模块间信息流与处理规范**占位文档。
- 当前只冻结方向与分层原则：
  - 定义模块间到底传什么
  - 什么对象允许跨模块流转
  - 如何避免建议/候选/裁决/执行结果混用
- 当前不替代各模块已有协议，不做代码强制校验，不做全系统重构。

---

## B. 为什么需要这份规范

- 当前系统已出现多类对象：`slice / candidate / routing_suggestion / consumption_stub / execution_stub / formal_decision` 等。
- 若缺少系统级信息流规范，后续将高概率出现：
  - 越级使用（下游把低层对象当高层事实）
  - 重复解释（同一对象被下游当“原始输入”再解释）
  - 字段漂移（同名字段跨模块语义不一致）
  - 模块越权（建议层/占位层偷偷变成裁决器）
- 因此必须先冻结系统级规则与分层纪律，作为后续协议治理与中台收口的上位约束。

---

## C. 信息对象分层（系统语义层级，占位）

> 本节不展开具体 schema，只冻结“层级语义”与“是什么/不是什么”。

### C1. raw_input

- **是什么**：原始输入或上游原始观测的“未经解释”载体（例如原始文本/原始传感/原始检测输出占位）。
- **不是什么**：候选、建议、事实、裁决。

### C2. interpreted_candidate

- **是什么**：解释后的候选对象（可被中台消费的候选层输入）。
- **不是什么**：正式裁决、已执行结果。

### C3. routing_suggestion

- **是什么**：只读分流建议（例如是否需要导航的建议），用于中台后续裁决参考。
- **不是什么**：执行令、任务切换令。

### C4. dispatch_consumption_seen

- **是什么**：消费占位/观察结果（证明某层“接住了”某对象），用于可观测与回归。
- **不是什么**：裁决结果、执行结果。

### C5. formal_decision

- **是什么**：中台正式裁决层输出的正式判定结果（允许/挂起/阻断/切分支等）。
- **不是什么**：执行器动作；更不是下游可自由扩写的“事实”。

### C6. execution_stub

- **是什么**：执行前承接/门控的只读占位结果（ready/blocked/pending 等）。
- **不是什么**：真实执行启动；不应绕过正式裁决层。

### C7. executed_result

- **是什么**：真实执行之后产生的结果/回执/状态（占位）。
- **不是什么**：候选或建议。

---

## D. 模块间传输原则（必须写死）

1. **模块间只传标准化对象，不传私有内部中间态**  
2. **每个跨模块对象必须带层级语义与来源信息**（至少：level + source + upstream refs）  
3. **下游模块不得把低层对象当高层事实使用**  
4. **只有被授权的层才能把对象升格到更高语义层**（例如 formal decision 主权归中台）  
5. **对象一旦升格，下游不得再把它当原始输入重新解释**（避免重复解释与事实漂移）  
6. **建议层、占位层、承接层、正式裁决层必须严格区分**（任何“越权替代”禁止）  

---

## E. 模块处理权限规范（占位原则，不做全量映射）

- **可以产出 candidate 的模块类型**：视角解释/纠偏层、规则引擎候选层（占位描述）。  
- **可以产出 suggestion 的模块类型**：分流建议层（routing suggestion layers）。  
- **可以产出 formal decision 的模块类型**：**仅中台正式裁决层**（Source of Truth）。  
- **只能观察/只读/转发的模块类型**：consume stub / execution stub 等占位层。  
- **不能升格信息对象的模块类型**：语音模板层、局部支链建议层、视角前端检测层等（占位原则）。  

---

## F. 来源与追踪要求（写要求，不全量补）

未来正式跨模块对象至少应可追踪：
- source module
- upstream refs
- object level / status
- schema version（先写要求）

---

## G. 当前不做（写死）

- 不做现有协议大迁移
- 不做自动依赖分析
- 不做代码层强校验
- 不做全量对象注册中心
- 不改现有主线行为

---

## H. 后续专题入口（占位）

- Object Level Registry v0
- Object Escalation Rules v0
- Cross-Module Processing Permission Matrix v0

