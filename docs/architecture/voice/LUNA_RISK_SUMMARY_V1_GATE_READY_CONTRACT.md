# risk_summary_v1 — Gate-Ready Contract v0（冻结）

**文件**：`docs/architecture/voice/LUNA_RISK_SUMMARY_V1_GATE_READY_CONTRACT.md`  
**目标（写死）**：不实现 Risk Gate；不改主链行为；不改 `risk_summary_v1` 读取逻辑；不接白盒；不接 provenance；不碰视觉解释实现。  
**用途**：把 `risk_summary_v1` 从当前“观测/试点输入”推进为“**未来可进入 admission layer 的主链风险事实候选**”，先把契约（来源、字段、有效期、可用性条件）冻结。

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`（宪法高于本契约）  
- `docs/architecture/voice/LUNA_CONFLICT_TOPIC_03_RISK_GATE_V0.md`（Risk Gate 专题边界）  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`（执行准入层边界）  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（主线冻结面与硬约束）  

并强调：**主链事实高于辅助信号**；不得绕过 No Fabrication；系统级时空锚点仍只能消费中台统一基准。

---

## A. 文档定位

- 本文是 `risk_summary_v1` 的 **gate-ready 契约冻结文档（v0）**。  
- 当前目标不是实现 Risk Gate。  
- 当前目标是把 `risk_summary_v1` 从“观测输入”整理成“未来可被 admission layer 使用的主链风险事实候选”。  
- 当前不涉及：白盒、溯源、审批流、中台审核细则实现。

---

## B. 当前系统定位（写死）

- `risk_summary_v1` **当前仍不能被直接当作 Risk Gate 条件**。  
- 它当前最多是 **主链风险事实候选**（candidate mainline fact）。  
- 若未来要被 Risk Gate 使用，必须先满足本文定义的 **gate-ready 条件**（见 §E），且 Risk Gate 仍需遵守 Topic 03 的最小口径（只考虑 `high` 进入拦截候选）。

---

## C. 来源与边界（写死）

### C1. 来源约束

- `risk_summary_v1` 必须来自**外部/中台/上游稳定注入**（例如由统一风险服务或上游稳定模块写入 `runtime_context.metadata`）。  
- voice 侧只能**读取、传递、观察**，不得擅自创造或改写系统级风险事实。  
- 禁止：voice 模块根据文本/视觉摘要/语义影子“推断”并写入 `risk_summary_v1`。

### C2. 与辅助信号的边界

- `sidewalk_env_summary_v1` / `retail_env_summary_v1`、V3 `luna_voice_vision_semantic_v3_input`、V2 `vision_shadow`、V2 `semantic_v2_shadow` / `semantic_v2_assist_*` 均属于**辅助观察信号**：  
  - 可以为“风险观察/提示”提供背景  
  - **不得**直接生成、升级或替代 `risk_summary_v1`

---

## D. 最小字段集合（冻结建议，v0 极小）

> 只冻结最小集合，不做大而全 schema。字段必须可工程化、可稳定消费。

### D1. 结构（建议）

`risk_summary_v1` 建议为一个 dict（JSON 可序列化），最小字段：

- **`risk_level`**：`none | warning | high`  
- **`risk_type`**：极简枚举或字符串（例如 `traffic` / `fall` / `unknown`）  
- **`risk_reason`**：简短原因（≤ 120 字，描述性而非推理性）  
- **`confidence`**：0.0–1.0（缺失视为不满足 gate-ready）  
- **`source`**：来源标识（上游模块/服务名；必须非空）  
- **`is_gate_ready`**：bool（只能在满足 §E 条件时为 true）

### D2. 字段语义约束（写死）

- `risk_level`：只允许上述 3 值（大小写不敏感由消费侧处理；写入侧必须稳定）  
- `confidence`：必须是数值且在 \([0, 1]\) 内；未知不得用 -1/None 代替  
- `risk_reason`：只陈述上游给出的原因，不允许 voice 侧补写推理  
- `source`：必须可解释（可用于审计/排障），不得为空字符串  
- `is_gate_ready`：**不是“风险高低”的同义词**；它表达“是否满足作为 gate 输入的契约条件”

### D3. 哪些字段不能作为 gate 事实（v0）

为避免“观测字段冒充事实”，以下在 v0 均不得被视为 gate 条件（即使上游写入也只能观测）：

- 任意来自视觉摘要/语义影子推断的派生字段（例如 `derived_from_vision`、`semantic_risk_guess`）  
- 任意“未冻结枚举/未冻结结构”的扩展字段（例如嵌套对象、自由形态列表），除非后续专项评审纳入 schema

---

## E. Gate-Ready 条件（写死）

只有当以下条件全部满足时，`risk_summary_v1` 才有资格作为 future Risk Gate 的候选输入（candidate input）：

1) **`risk_level` 明确**且取值稳定（`none|warning|high`）  
2) **`source` 明确**且非空，可解释  
3) **`confidence` 存在**且为有效数值（0~1）  
4) **字段结构完整**：至少包含 §D1 的全部字段（允许额外字段存在，但不得影响 gate-ready 判定）  
5) **风险事实来自稳定注入**（外部/中台/上游），而不是 voice 本地推断  
6) **`is_gate_ready == true`** 只能在满足 1)~5) 时成立；否则必须为 false

（可选但推荐的工程约束，未来专项评审再冻结）：有效期/时间戳字段、schema_version 字段、以及“适用范围”（仅提示 vs 可拦截）字段。

---

## F. 当前明确禁止项（写死）

- 不允许仅凭视觉“像危险”就写成 gate-ready  
- 不允许仅凭语义/影子/assist 推断就写成 gate-ready  
- 不允许当前 voice 模块自己生成 `risk_level=high`（或改写上游给出的 risk_level）  
- 不允许把 `warning` 直接设计成未来 gate 拦截条件  
- 不允许在本契约文档里顺手实现 Risk Gate

---

## G. 与 V3 / V2 的关系（写死）

- `sidewalk_env_summary_v1` / `retail_env_summary_v1` / `vision_shadow`：可提供背景，但不能替代 `risk_summary_v1`。  
- `semantic_v2` 与 `assist` 系列：只能辅助“对照/确认/观测”，不能升格为系统风险事实。  
- 若未来 Risk Gate 消费 `risk_summary_v1`：必须继续服从“主链事实高于辅助信号”的原则与 No Fabrication 约束。

---

## H. 当前最小未来用法（只设计，不实现）

未来 Risk Gate 若实现：**只能消费 `is_gate_ready == true` 的 `risk_summary_v1`**；且 v0 **只考虑 `risk_level == high`** 进入 gate 候选；`warning` 仅提示/观测，不作拦截。

---

## I. 后续前置条件（写死）

- 在实现 Risk Gate 前，必须先冻结并遵守本契约。  
- 若要改 `risk_level` 分层、字段集合、来源口径或 gate-ready 条件，必须专项评审。  
- 若未来要接白盒/provenance：只能在本契约基础上扩 trace/证据链字段；不在本轮处理。

