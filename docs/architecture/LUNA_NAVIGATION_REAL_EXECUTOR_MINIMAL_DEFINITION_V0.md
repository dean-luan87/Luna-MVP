# Luna — Navigation Real Executor Minimal Definition v0（真实导航执行器本体：最小定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`  
**性质**：Phase-Next-22：真实导航执行器本体最小定义（冻结职责边界与最小能力面，不接执行器）  

关联：
- 接入就绪评审（v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`
- 最小接入顺序（设计冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器输入层边界（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- 执行器输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 接管层边界（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器本体最小定义”的设计文档。
- 当前目标：冻结执行器本体边界（它是什么/不是什么/最小能力面/最小运行状态/严格关系）。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做执行期监控实现。
- 当前不改变现有主线行为。

---

## B. 为什么现在必须先定义执行器本体

- 当前已经有执行器输入层、输入对象、接口契约、状态对象、接管边界等“接入前骨架”。
- 但系统里仍缺一个明确的“执行器本体定义”。
- 若没有这个定义，后续任何执行器接入都会出现职责混乱与越权扩张（例如把裁决/授权/输出治理塞进执行器）。
- 因此必须先冻结“执行器本体是什么，不是什么”，作为接入阶段的硬边界。

---

## C. 执行器本体的最小定义（写死）

执行器本体是：

- 在**合法接管之后**，负责把标准化执行输入转成实际导航执行行为的能力单元。
- 它处理的是“执行”。
- 它不是“裁决”，不是“放行”，不是“接管授权”，不是“输出治理”，不是“记忆治理”。

核心一句（写死）：

**执行器负责执行与执行期状态回传；上游负责决定能否执行、何时执行、如何回退。**

---

## D. 执行器本体明确不是什么（写死，逐项说明）

执行器本体不是：

- **formal decision**：裁决是否允许推进属于上游治理；执行器不得自作裁决。
- **readiness gate**：就绪判断属于执行前门控；执行器不得用运行时逻辑替代门控。
- **takeover authorization**：接管授权属于控制权移交边界；执行器不得自授权接管。
- **语音输出模块**：播报/提示是输出治理与语音策略的职责；执行器最多提供状态供其消费。
- **记忆模块**：记忆写入与治理属于上游；执行器不得直接写入记忆。
- **地图策略决策器**：是否选地图/非地图/混合由上游资源与策略治理决定；执行器只消费标准化后的资源模式。
- **回退策略最终裁决器**：执行器可上报异常/建议回退，但最终回退路径与切链裁决属于上游治理。
- **中台调度器**：任务编排与跨链调度属于中台；执行器不负责调度其它模块。

---

## E. 执行器最小能力面（只定义能力面，不展开实现）

1) **接收标准化执行输入**
- 只消费 `navigation_real_executor_input_v0`（或其正式实现版）
- 不允许直接读取上游候选 / stub / gate / raw metadata

2) **启动执行**
- 在合法接管后进入执行态
- 但不意味着执行器自行决定是否可以接管

3) **执行中持续运行**
- 能维持最小导航执行流程
- 能在能力可用时持续输出执行动作（动作的具体形态不在本定义展开）

4) **执行状态回传**
- 能把最小执行状态回传给中台/监控链
- 本轮不实现，但能力定义必须存在（与接口契约/状态对象兼容）

5) **异常上报**
- 发现执行失败/中断/不可执行时，必须回传
- 不得私自吞掉异常或静默结束

---

## F. 执行器本体最小运行状态（收敛为最小集合）

建议最小状态集合：

- `idle`
- `ready_to_takeover`
- `active`
- `degraded`
- `interrupted`
- `failed`
- `released`

说明（写死）：
- 这是执行器内部/对外语义的最小状态框架（当前不做代码实现）。
- 当前不要求与状态对象完全一一映射，但语义必须兼容（例如 `active` ≈ execution_running 语义域）。
- 这些状态不构成“上游裁决信号”，不得反向替代 formal decision/readiness。

---

## G. 执行器与各层的关系（写死）

### 与 formal decision

- formal decision 决定是否允许推进
- 执行器不参与正式裁决

### 与 readiness gate

- readiness gate 决定是否具备候选就绪前提
- 执行器不参与 readiness 判断

### 与 takeover 层

- takeover 层决定未来是否可合法移交控制权
- 执行器只能在接管层之后接手

### 与输入对象

- 输入对象是执行器唯一合法输入
- 执行器不应自己拼装输入

### 与状态对象

- 状态对象是执行器的标准化回传面
- 执行器应通过该对象对外表达状态（语义一致，结构由上游/契约冻结）

### 与语音 / 输出治理

- 执行器不负责决定播报策略
- 最多提供执行状态给输出治理层消费

### 与地图 / 非地图资源

- 执行器消费已标准化的资源模式
- 不负责决定是否选地图模式或非地图模式

---

## H. 当前仍然不能接入真实执行器的原因（写死）

- 当前只有执行器本体定义，没有执行器实现
- 当前没有输入对象实现版
- 当前没有状态对象实现版
- 当前没有真实监控闭环
- 当前没有真实回退/中断治理
- 当前没有启动策略真实接线
- 当前没有地图/非地图执行资源真实接入

---

## I. 当前不做（写死）

- 不做真实执行器实现
- 不做地图接入
- 不做执行期监控实现
- 不做语音启动实现
- 不做回退治理实现
- 不做自动切链
- 不做执行动作实现

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 执行器输入对象实现版 **或** 监控闭环最小定义
- 再之后才考虑：
  - 真实执行器最小接入实验线
- 当前不跨这两步

---

## K. 未来执行器本体的最小能力清单样例（仅说明，不实现、不落代码）

```json
{
  "executor_identity": "navigation_real_executor_v0",
  "can_consume_standard_input": true,
  "can_report_standard_status": true,
  "can_raise_execution_exception": true,
  "can_self_authorize_takeover": false
}
```

