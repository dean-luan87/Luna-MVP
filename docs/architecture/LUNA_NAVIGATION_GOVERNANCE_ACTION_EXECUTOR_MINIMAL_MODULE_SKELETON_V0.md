# Luna — Navigation Governance Action Executor Minimal Module Skeleton v0（治理动作执行器本体最小模块骨架：设计与落地）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`  
**性质**：Phase-Next-33：把“治理动作执行器本体定义”推进为“可接入但不可执行”的模块骨架（skeleton）  

关联：
- 治理动作执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作边界层冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界层最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理决策最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`
- Real Executor 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`

---

## A. 文档定位（写死）

- 这是“治理动作执行器本体最小模块骨架”的设计与落地文档。
- 当前目标：把治理动作执行器本体从定义推进到**模块骨架**（可导入、可被未来接线，但当前不可执行治理动作）。
- 当前不做真实治理动作实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在要做 skeleton

- 治理动作执行器本体定义已经冻结。
- 若没有模块骨架，后续即使 action boundary / approved action / status output 的对象面已清晰，也没有统一的“实体挂载点”承载：
  - 输入接口（只接受批准后的动作边界）
  - 状态回传接口（标准化 action status）
  - 异常上报接口（标准化 exception）
- 因此必须先把治理动作执行器实体化为**模块骨架**，但仍严格禁止真实治理动作执行。

---

## C. skeleton 的最小定义（写死）

- 它不是可运行治理器（不是 runtime governance executor）。
- 不是 governance entry / decision / action boundary。
- 不是中台调度器。
- 它只是一个“可被未来接线的治理动作执行器壳子”：
  - 有固定 identity/scope
  - 有最小接口占位
  - 默认只返回 placeholder / inactive / not_implemented 级别结果

---

## D. skeleton 最小能力面（写死）

1) 模块身份  
- 固定 identity / scope，例如：`navigation_governance_action_executor_v0`

2) 输入接口占位  
- 未来只接受“被批准的 action boundary”正式对象  
- 当前只做接口占位，不做真实消费，不触发动作

3) 状态回传接口占位  
- 未来只回标准化治理动作状态对象  
- 当前只做接口占位，不生成真实动作状态

4) 异常上报接口占位  
- 未来异常必须走标准接口  
- 当前只做占位，不做真实异常处理/恢复

---

## E. skeleton 默认行为（写死）

- 默认不执行真实回退动作
- 默认不执行真实中断动作
- 默认不执行真实释放控制权动作
- 默认不改路线
- 默认不驱动语音
- 默认不驱动记忆
- 默认不触发中台真实迁移
- 默认只返回 `not_implemented / inactive / placeholder` 级别结果

---

## F. 与现有链路的关系（写清）

### 与 governance action boundary

- skeleton 未来只吃“被批准的 action boundary”结果。
- 当前不直接消费普通 `request_*` 建议结果来执行真实动作。

### 与 governance decision

- skeleton 不参与治理决策分类；只在后续阶段可能被接上。

### 与 executor 本体（navigation real executor）

- executor 本体负责导航执行。
- governance action executor 负责治理动作执行。
- 两者不能混为一个模块。

### 与中台

- 中台未来可批准/调度治理动作。
- skeleton 当前不直接接中台真实迁移链、不触发迁移。

---

## G. 当前不允许做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接吃未批准的 action boundary / recommendation
- 不允许直接回临时状态字段冒充标准状态对象
- 不允许绕过 action boundary / 批准链 / 状态对象边界

