# Luna — Navigation Real Executor Interface Contract v0（真实导航执行器接口契约：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`  
**性质**：Phase-Next-18：真实导航执行器接口契约最小设计（冻结 I/O 与状态语义，不接执行器）  

关联：
- 执行器输入层边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- 执行器输入对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象只读占位输出：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 执行器接管合法入口冻结：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- readiness gate stub（统一只读出口）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- 执行器标准化状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 状态对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器接口契约”的最小设计文档。
- 当前目标：冻结执行器接口边界（输入/输出/状态回传的最小语义契约）。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做执行期监控实现。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先定义接口契约

- 当前已经有执行器输入层与输入对象占位（输入侧骨架已具备“统一对象出口”）。
- 但还没有“执行器本体必须如何对接系统”的统一契约。
- 若不先冻结契约，后续不同执行器实现会各自返回不同状态、不同字段、不同语义，导致不可治理、不可回归。
- 因此必须先冻结接口契约，确保执行器作为黑盒能力单元仍可被系统一致治理与观测。

---

## C. 执行器未来唯一合法输入（写死）

- 执行器未来只应接收**标准化输入对象**：`navigation_real_executor_input_v0`
- 不允许执行器直接读取：
  - advice / candidate / gate / stub / raw metadata
- 不允许执行器自己去拼接上游对象（禁止越层取数与自造授权）

说明（写死）：
- `navigation_real_executor_input_v0` 的产出与治理属于上游控制链与输入层职责。
- 执行器只能把它作为“唯一输入面”，不得旁路读取其它 key。

---

## D. 执行器最小输出类别（只定义类别与语义，不做复杂 schema）

> 口径：只定义语义类别，不做字段细表，不做实现。

1) **接管状态输出**
- 接管是否开始（started）
- 接管是否激活（active）
- 接管是否释放（released）

2) **执行状态输出**
- 执行中（running）
- 执行完成（completed）
- 执行失败（failed）
- 执行中断（interrupted）

3) **偏航 / 异常输出**
- 是否检测到偏航 / 不可执行 / 环境突变等异常
- 是否建议上游回退（建议语义，不是最终裁决）

4) **资源 / 能力状态输出**
- 当前执行器能力是否退化（degraded）
- 当前是否还能继续执行（能/不能继续，语义回传）

---

## E. 执行器最小回传状态集合（收敛为最小集合，写死）

建议最小集合（语义枚举，当前不实现）：

- `takeover_started`
- `takeover_active`
- `takeover_released`
- `execution_running`
- `execution_completed`
- `execution_failed`
- `execution_interrupted`
- `execution_degraded`

并写死：
- 这些是执行器回传给中台/监控链的最小状态语义
- 当前不实现具体回传链路与对象

---

## F. 执行器明确不负责的事情（写死，关键边界）

执行器不负责：
- 正式裁决（formal decision）
- readiness 判断
- takeover 合法性判断
- 语音输出策略
- 记忆写入
- 地图能力选择策略（由上游策略/资源治理决定；执行器只消费输入层标准化后的资源模式）
- 回退策略最终裁决（执行器只能回传建议/异常，最终回退决策归上游治理）

也就是说（写死）：
- 执行器负责执行与执行期状态回传
- 上游负责决定“能不能执行、何时执行、如何回退”

---

## G. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 只负责能否推进
- 不直接成为执行器接口

### 与 readiness gate

- readiness gate 只负责最后门控候选就绪
- 不直接成为执行器接口

### 与 takeover 层

- takeover 层负责未来控制权移交边界
- 执行器接口应在 takeover 之后

### 与执行器输入对象

- 执行器只吃 `navigation_real_executor_input_v0`（或其正式版本）
- 这是执行器唯一合法输入面

### 与监控 / 回传链

- 执行器必须把最小状态回传给中台/监控链
- 但当前不实现具体回传链路

---

## H. 当前仍然不能接真实执行器的原因（写死）

- 当前只有接口契约，没有执行器实现
- 当前没有真实输入对象实现版（当前仅有 placeholder / 只读占位输出）
- 当前没有真实地图/非地图资源接入
- 当前没有执行期监控闭环实现
- 当前没有输出治理/启动策略真实接线
- 当前没有回退/中断治理真实接线

---

## I. 当前不做（写死）

- 不做执行器实现
- 不做地图接入
- 不做执行期监控实现
- 不做语音启动实现
- 不做回退治理实现
- 不做自动切链

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 执行器输出对象 / 状态对象占位设计
- 再之后才考虑：
  - 真实执行器接入方案
- 当前不跨这两步

---

## K. 未来接口对象样例（仅说明，不实现、不落代码）

输入样例（仅说明）：

```json
{
  "executor_input_present": true,
  "executor_input_scope": "navigation_real_executor_input_v0",
  "takeover_authorized": true
}
```

输出样例（仅说明）：

```json
{
  "executor_status_scope": "navigation_real_executor_status_v0",
  "takeover_state": "takeover_active",
  "execution_state": "execution_running"
}
```

